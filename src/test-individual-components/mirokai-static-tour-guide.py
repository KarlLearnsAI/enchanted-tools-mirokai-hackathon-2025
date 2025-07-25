import asyncio
from pymirokai.robot import connect
from pymirokai.models.data_models import Coordinates
from pymirokai.core.video_api import VideoAPI
import time
import cv2
import numpy as np
import random

# PARAMETERS
ROBOT_IP = "10.6.57.247" # "10.6.32.15"
API_KEY  = "admin"
INTRO_SPEECHES = [
    "Hello, museum enthusiasts!",
    "Now, let's move to the next exhibit to see the Mona Lisa.",
    "Now, let's move to the next exhibit to see the Rosetta Stone.",
    "Now let's head to the dinosaur exhibit.",
    "Thank you for visiting the museum! I hope you enjoyed the tour. Let's head back to the entrance."
]
SPEECH_CONTENTS = [
    "Napoleon Bonaparte was a French military leader who rose to prominence during the French Revolution and crowned himself Emperor in 1804.",
    "The Mona Lisa, painted by Leonardo da Vinci, is one of the most famous works of art in the world, known for its enigmatic smile.",
    "The Rosetta Stone is a granodiorite stele inscribed with a decree issued in Memphis, Egypt in 196 BC.",
    "The T-Rex, or Tyrannosaurus rex, was one of the largest land carnivores of all time, living during the late Cretaceous period.",
    "Feel free to reach out to us from Enchanted Tools to book our services for your own events! Have a great day!"
]
SPEECH_DURATIONS = [7, 4, 4, 4, 4] # TODO: Adjust to real world
CHECKPOINT_NAMES = [
    "first",
    "second",
    "third",
    "fourth",
    "fifth (FINAL)"
]
COORDS_LIST = [
    Coordinates(x=1.0, y=0.0, theta=0.0),
    Coordinates(x=1.0, y=1.0, theta=0.0),
    Coordinates(x=2.0, y=2.0, theta=0.0),
    Coordinates(x=3.0, y=2.0, theta=0.0),
    Coordinates(x=4.0, y=4.0, theta=0.0)
]

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

async def go_to_museum_checkpoint(robot, video_api: VideoAPI, full_url: str, *, use_absolute_coords: bool = True, coords: Coordinates, intro_speech: str, speech_content: str, speech_duration: float, checkpoint_name: str):
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
    print(f"{checkpoint_name} walk done")

    # start yapping about museum checkpoint
    speech = robot.say(speech_content)
    await asyncio.sleep(speech_duration)
    print(f"{checkpoint_name} speech done")

    # take frame of audience
    try:
        await asyncio.to_thread(take_snapshot, video_api, full_url)
    except Exception as e:
        print(f"[ERROR] snapshot at {checkpoint_name}: {e}")

    # analyze aduience and say something
    # TODO

async def main():
    full_url = f"rtsp://{ROBOT_IP}:8554/head_color"
    video_api = VideoAPI(display=False, timeout=5000)
    video_api.start(full_url)
    await asyncio.sleep(2)  # let buffer fill 
    async with connect(API_KEY, ROBOT_IP) as robot:
        for i in range(len(INTRO_SPEECHES)):
            await go_to_museum_checkpoint(robot, video_api, full_url, use_absolute_coords=True, coords=COORDS_LIST[i], intro_speech=INTRO_SPEECHES[i], speech_content=SPEECH_CONTENTS[i], speech_duration=SPEECH_DURATIONS[i], checkpoint_name=CHECKPOINT_NAMES[i])
        outro = robot.say("If you want your photos from today's exhibit, simply send send me an email and I'll send the photos back to you.")
        print("SUCCESS!!!")
        
if __name__ == "__main__":
    asyncio.run(main())