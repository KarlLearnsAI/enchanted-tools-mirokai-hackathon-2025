import asyncio
from pymirokai.robot import connect
from pymirokai.models.data_models import Coordinates
# from pymirokai.robot.video import VideoStreamManager
from pymirokai.core.video_api import VideoAPI
import time
import cv2
import numpy as np
import random

robot_ip = "10.6.57.247" # "10.6.32.15"
api_key  = "admin"

async def stream_head_color(robot_ip: str):
    # 1) make VideoAPI, start capture thread
    video_api = VideoAPI(display=False, timeout=5000)
    full_url = f"rtsp://{robot_ip}:8554/head_color"
    video_api.start(full_url)

    # 2) give it a couple of seconds to fill the buffer
    await asyncio.sleep(2)

    # random snapshot filename
    num = np.random.randint(1000, 9999)

    def _capture_loop():
        frame = None
        try:
            while frame is None:
                frame = video_api.get_current_frame()
                if frame is not None:
                    cv2.imshow("head_color", frame)
                    cv2.imwrite(f"frames/head_color_snapshot_{num}.png", frame)
                    print(f"Saved frames/head_color_snapshot_{num}.png")
                # break on 'q'
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        except Exception as e:
            print(f"An error occurred in capture loop: {e}")
        finally:
            video_api.stop()
            cv2.destroyAllWindows()

    # 3) run the blocking OpenCV loop off the main event loop
    await asyncio.to_thread(_capture_loop)

def take_snapshot(
    video_api: VideoAPI,
    full_url: str,
    snapshot_dir: str = "frames",
    max_attempts: int = 30,
    retry_delay: float = 0.1,
) -> str:
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
    fname = f"{snapshot_dir}/head_color_snapshot_{num}.png"
    cv2.imwrite(fname, frame)
    cv2.imshow("head_color", frame)
    cv2.waitKey(1)
    print(f"Saved {fname}")
    return fname

# async def go_to_museum_checkpoint(robot, robot_ip: str, *, use_absolute_coords: bool = False, coords: Coordinates, speech_content: str, speech_timer: float, checkpoint_name: str):
    # move to museum checkpoint
    # if use_absolute_coords:
    #     print(f"going to absolute coords {coords} for {checkpoint_name} checkpoint")
    #     walk = robot.go_to_absolute(coords)
    # else:
    #     print(f"going to relative coords {coords} for {checkpoint_name} checkpoint")
    #     walk = robot.go_to_relative(coords)
#     await walk.completed()
#     print(f"finished {checkpoint_name} walk")

#     # start yapping about museum checkpoint
#     checkpoint1 = robot.say(speech_content)
#     # await robot.say(speech_content)
#     await asyncio.sleep(speech_timer) # wait for speech to finish
#     print(f"finished {checkpoint_name} talk")

#     # take frame of audience
#     try:
#         await stream_head_color(robot_ip)
#     except Exception as e:
#         print(f"[ERROR] Stream failed at {checkpoint_name}: {e}")
    
    
#     # analyze aduience and say something
#     # TODO

async def go_to_museum_checkpoint(robot, video_api: VideoAPI, full_url: str, *, use_absolute_coords: bool = False, coords: Coordinates, intro_speech: str, speech_content: str, pause: float, checkpoint_name: str):
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
    await asyncio.sleep(pause)
    print(f"{checkpoint_name} talk done")

    # snapshot (offload blocking I/O)
    try:
        await asyncio.to_thread(take_snapshot, video_api, full_url)
    except Exception as e:
        print(f"[ERROR] snapshot at {checkpoint_name}: {e}")

async def main():
    intro_speeches = [
        "Hello, museum enthusiasts!",
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
        "Feel free to reach out to us from Enchanted Tools to book our services for your own events! Have a great day!"
    ]

    pauses = [7, 4, 4, 4, 4]

    checkpoint_names = [
        "first",
        "second",
        "third",
        "fourth",
        "fifth (FINAL)"
    ]
    
    coords_list = [Coordinates(x=2.0, y=0.0, theta=0.0)] * len(intro_speeches)
    
    full_url = f"rtsp://{robot_ip}:8554/head_color"
    video_api = VideoAPI(display=False, timeout=5000)
    video_api.start(full_url)
    await asyncio.sleep(2)  # let buffer fill
    
    async with connect(api_key, robot_ip) as robot:
        # first stop
        # greet_guests = robot.say("Hello, museum enthusiasts!")
        for i in range(len(intro_speeches)):
            await go_to_museum_checkpoint(robot, video_api, full_url, coords=coords_list[i], intro_speech=intro_speeches[i], speech_content=speech_contents[i], pause=pauses[i], checkpoint_name=checkpoint_names[i])
        
        # await go_to_museum_checkpoint(
        #     robot, video_api, full_url,
        #     coords=Coordinates(x=2.0, y=0.0, theta=0.0),
        #     intro_speech="Hello, museum enthusiasts!",
        #     speech_content=(
        #         "Napoleon Bonaparte was a French military leader who rose to prominence "
        #         "during the French Revolution and crowned himself Emperor in 1804."
        #     ),
        #     pause=7,
        #     checkpoint_name="first"
        # )

        # # second stop
        # await go_to_museum_checkpoint(
        #     robot, video_api, full_url,
        #     coords=Coordinates(x=2.0, y=0.0, theta=0.0),
        #     intro_speech="Now, let's move to the next exhibit to see the Mona Lisa.",
        #     speech_content=(
        #         "The Mona Lisa, painted by Leonardo da Vinci, is one of the most famous works "
        #         "of art in the world, known for its enigmatic smile."
        #     ),
        #     pause=4,
        #     checkpoint_name="second"
        # )

        # # third stop
        # await go_to_museum_checkpoint(
        #     robot, video_api, full_url,
        #     coords=Coordinates(x=2.0, y=0.0, theta=0.0),
        #     intro_speech="Now, let's move to the next exhibit to see the Rosetta Stone.",
        #     speech_content=(
        #         "The Rosetta Stone is a granodiorite stele inscribed with a decree issued in Memphis, Egypt in 196 BC."
        #     ),
        #     pause=4,
        #     checkpoint_name="third"
        # )

        # # fourth stop
        # await go_to_museum_checkpoint(
        #     robot, video_api, full_url,
        #     coords=Coordinates(x=2.0, y=0.0, theta=0.0),
        #     intro_speech="Now let's head to the dinosaur exhibit.",
        #     speech_content=(
        #         "The T-Rex, or Tyrannosaurus rex, was one of the largest land carnivores of all time, living during the late Cretaceous period."
        #     ),
        #     pause=4,
        #     checkpoint_name="fourth"
        # )
        
        # # fifth stop
        # await go_to_museum_checkpoint(
        #     robot, video_api, full_url,
        #     coords=Coordinates(x=2.0, y=0.0, theta=0.0),
        #     intro_speech="Thank you for visiting the museum! I hope you enjoyed the tour. Let's head back to the entrance.",
        #     speech_content=(
        #         "Feel free to reach out to us from Enchanted Tools to book our services for your own events! Have a great day!"
        #     ),
        #     pause=4,
        #     checkpoint_name="fifth (FINAL)"
        # )
        
        print("SUCCESS!!!")

        
if __name__ == "__main__":
    asyncio.run(main())