import asyncio
from pymirokai.robot import connect
from pymirokai.models.data_models import Coordinates
# from pymirokai.robot.video import VideoStreamManager
from pymirokai.core.video_api import VideoAPI
import time
import cv2
import numpy as np
import random
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision import transforms
from PIL import Image
import torch

robot_ip = "10.6.57.247" # "10.6.32.15"
api_key  = "admin"


def take_snapshot(video_api: VideoAPI, full_url: str, snapshot_dir: str = "frames", max_attempts: int = 30, retry_delay: float = 0.1,) -> str:
    """
    Try up to `max_attempts` to read one frame from `video_api`.
    If no frame appears, restart the stream and try once more.
    Returns the filepath of the saved snapshot.
    """
    # try to get one frame
    for attempt in range(max_attempts):
        frame = video_api.get_current_frame()
        if frame is not None:
            break
        time.sleep(retry_delay)
    else:
        # no frame after max_attempts: restart the stream once
        video_api.stop()
        video_api.start(full_url)
        time.sleep(2)  # let buffer refill
        frame = video_api.get_current_frame()
        if frame is None:
            raise RuntimeError("Stream dead even after restart")

    # save & show
    num = np.random.randint(1000, 9999)
    fname = f"{snapshot_dir}/exhibit_{num}.png"
    cv2.imwrite(fname, frame)
    cv2.waitKey(1)
    print(f"Saved {fname}")
    return fname

async def go_to_museum_checkpoint(robot, video_api: VideoAPI, full_url: str, *, use_absolute_coords: bool = True, coords: Coordinates, intro_speech: str, speech_content: str, pause: float, checkpoint_name: str):
    # intro to next checkpoint
    introduction = robot.say(intro_speech)
    
    # move to museum checkpoint
    if use_absolute_coords:
        print(f"going to absolute coords {coords} for {checkpoint_name} checkpoint")
        walk = robot.go_to_absolute(coords)
    else:
        print(f"going to relative coords {coords} for {checkpoint_name} checkpoint")
        walk = robot.go_to_relative(coords)
    await walk.completed()
    # await asyncio.sleep(3)
    print(f"{checkpoint_name} walk done")

    # start yapping about museum checkpoint
    speech = robot.say(speech_content)
    # rotate = robot.go_to_absolute(Coordinates(x=i, y=0.0, theta=0.0))
    # print(f"fixing location for speech -> going back to x={i}, y={0.0}, theta={0.0}")
    await asyncio.sleep(pause)
    print(f"{checkpoint_name} talk done")

    # take frame of audience
    try:
        await asyncio.to_thread(take_snapshot, video_api, full_url)
    except Exception as e:
        print(f"[ERROR] snapshot at {checkpoint_name}: {e}")

    # analyze aduience and say something
    # TODO

def count_people_in_image(model, path: str) -> int:
    frame = cv2.imread(path)
    if frame is None:
        raise FileNotFoundError(f"Could not load image from {path}")
    
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    tensor = transforms.ToTensor()(img).unsqueeze(0)
    with torch.no_grad():
        outputs = model(tensor)[0]

    people = [
        score.item() for label, score in zip(outputs['labels'], outputs['scores'])
        if label.item() == 1 and score.item() > 0.5
    ]
    return len(people)

async def main():
    intro_speeches = [
        "We will first take a look at one of the most adventurous people that ever existed. Napolean Bonaparte.",
        "Now, let's move to the next exhibit to see the Mona Lisa.",
        "Now, let's move to the next exhibit to see the Rosetta Stone.",
        "Now let's head to the dinosaur exhibit.",
        "Thank you for visiting the museum! I hope you enjoyed the tour. Let's head back to the entrance."
    ]

    speech_contents = [
        "Napoleon Bonaparte was a French military leader who rose to prominence during the French Revolution and crowned himself Emperor in 1804.",
        "The Mona Lisa, painted by Leonardo da Vinci, is one of the most famous works of art in the world, known for its enigmatic smile.",
        "The Rosetta Stone is a granodiorite stele inscribed with a decree issued in Memphis, Egypt in 196 BC.",
        "The T-Rex, or Tyrannosaurus rex, was one of the largest land carnivores of all time, living during the late Cretaceous period.",
        "Feel free to reach out to us from Enchanted Tools to book our autonomous robotics services for your own events! Bon journee!"
    ]

    pauses = [7, 4, 4, 4, 4]

    checkpoint_names = [
        "first",
        "second",
        "third",
        "fourth",
        "fifth (FINAL)"
    ]
    
    # coords_list = [Coordinates(x=1.0, y=0.0, theta=0.0)] * len(intro_speeches)
    coords_list = [Coordinates(x=2.05, y=2.73, theta=0.0), Coordinates(x=0.98, y=4.74, theta=0.0), Coordinates(x=3.59, y=4.34, theta=0.0), Coordinates(x=6.53, y=5.67, theta=0.0), Coordinates(x=0.0, y=0.0, theta=0.0)]
    
    model = fasterrcnn_resnet50_fpn(pretrained=True)
    model.eval()

    full_url = f"rtsp://{robot_ip}:8554/head_color"
    video_api = VideoAPI(display=False, timeout=5000)
    video_api.start(full_url)
    await asyncio.sleep(2)  # let buffer fill
    
    async with connect(api_key, robot_ip) as robot:
        try:
            snapshot_path = await asyncio.to_thread(take_snapshot, video_api, full_url)
            print("got img")
            await asyncio.sleep(0.3)
            people_in_frame = await asyncio.to_thread(count_people_in_image, model, snapshot_path)
            print("counted people")
            encounter_intro = robot.say(f"Hello, museum enthusiasts! I can see {people_in_frame} people joined our museum tour for today. It's exciting to see that our autonomous Mirokai tours are getting more popular.")
            print(f"I can see {people_in_frame} people. I saved the people detection analysis with bounding boxes inside the frames folder for you.")
            # encounter_intro = robot.say(f"I can see {people_in_frame} people. I saved the people detection analysis with bounding boxes inside the frames folder for you.")
            await asyncio.sleep(3)
        except Exception as e:
            print(f"[ERROR]: {e}")
            people_in_frame = -1

        print("analysis done")

        for i in range(len(intro_speeches)):
            await go_to_museum_checkpoint(robot, video_api, full_url, use_absolute_coords=True, coords=coords_list[i], intro_speech=intro_speeches[i], speech_content=speech_contents[i], pause=pauses[i], checkpoint_name=checkpoint_names[i])
        outro = robot.say("If you want your photos from today's exhibit, simply send send me an email and I'll send the photos back to you.")
        print("SUCCESS!!!")
        
if __name__ == "__main__":
    asyncio.run(main())