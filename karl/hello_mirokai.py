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

async def go_to_museum_checkpoint(robot, robot_ip: str, *, use_absolute_coords: bool = False, coords: Coordinates, speech_content: str, speech_timer: float, checkpoint_name: str):
    # move to museum checkpoint
    if use_absolute_coords:
        print(f"going to absolute coords {coords} for {checkpoint_name} checkpoint")
        walk = robot.go_to_absolute(coords)
    else:
        print(f"going to relative coords {coords} for {checkpoint_name} checkpoint")
        walk = robot.go_to_relative(coords)
    await walk.completed()
    print(f"finished {checkpoint_name} walk")

    # start yapping about museum checkpoint
    checkpoint1 = robot.say(speech_content)
    # await robot.say(speech_content)
    await asyncio.sleep(speech_timer) # wait for speech to finish
    print(f"finished {checkpoint_name} talk")

    # take frame of audience
    try:
        await stream_head_color(robot_ip)
    except Exception as e:
        print(f"[ERROR] Stream failed at {checkpoint_name}: {e}")
    
    # analyze aduience and say something
    # TODO

async def main():
    async with connect(api_key, robot_ip) as robot:
        # greeting + first checkpoint
        # await robot.say("Hello, museum enthusiasts!")
        greet_guests = robot.say("Hello, museum enthusiasts!")
        await go_to_museum_checkpoint(robot, robot_ip, use_absolute_coords=False, coords=Coordinates(x=2.0, y=0.0, theta=0.0),
            speech_content=(
                "Napoleon Bonaparte was a French military leader who rose to prominence "
                "during the French Revolution and crowned himself Emperor of the French in 1804."
            ),
            speech_timer=7,
            checkpoint_name="first"
        )       
        
        # walk = robot.go_to_relative(Coordinates(x=2.0, y=0.0, theta=0.0))
        # await walk.completed()
        # print("finished first walk")
        # # checkpoint1 = robot.say("Napoleon Bonaparte was a French military leader who rose to prominence during the French Revolution and crowned himself Emperor of the French in 1804.")
        # await asyncio.sleep(7)
        # print("finished first talk")
        # try:
        #     await stream_head_color(robot_ip)
        # except Exception as e:
        #     print(f"[ERROR] Stream failed: {e}")
        # print("got first frame")
        
        greet_guests = robot.say("Now, let's move to the next exhibit to see the Mona Lisa.")
        await go_to_museum_checkpoint(robot, robot_ip, use_absolute_coords=False, coords=Coordinates(x=2.0, y=0.0, theta=0.0),
            speech_content=(
                "The Mona Lisa, painted by Leonardo da Vinci, is one of the most famous works of art in the world, known for its enigmatic smile."
            ),
            speech_timer=4,
            checkpoint_name="second"
        )
        
        # cont2 = robot.say("Now, let's move to the next exhibit to see the Mona Lisa.")
        # walk2 = robot.go_to_relative(Coordinates(x=2.0, y=0.0, theta=0.0))
        # await walk2.completed()
        # print("finished second walk")
        # checkpoint2 = robot.say("The Mona Lisa, painted by Leonardo da Vinci, is one of the most famous works of art in the world, known for its enigmatic smile.")
        # await asyncio.sleep(3)
        # print("finished second talk")
        # try:
        #     await stream_head_color(robot_ip)
        # except Exception as e:
        #     print(f"[ERROR] Stream failed: {e}")
        # print("got second frame")
        
        greet_guests = robot.say("Next, we will visit the ancient Egyptian artifacts.")
        await go_to_museum_checkpoint(robot, robot_ip, use_absolute_coords=False, coords=Coordinates(x=2.0, y=0.0, theta=0.0),
            speech_content=(
                "The Rosetta Stone is a granodiorite stele inscribed with a decree issued in Memphis, Egypt in 196 BC."
            ),
            speech_timer=4,
            checkpoint_name="third"
        )
        
        # cont3 = robot.say("Next, we will visit the ancient Egyptian artifacts.")
        # walk3 = robot.go_to_relative(Coordinates(x=2.0, y=0.0, theta=0.0))
        # await walk3.completed()
        # print("finished third walk")
        # checkpoint3 = robot.say("The Rosetta Stone is a granodiorite stele inscribed with a decree issued in Memphis, Egypt in 196 BC.")
        # await asyncio.sleep(3)
        # print("finished third talk")
        # try:
        #     await stream_head_color(robot_ip)
        # except Exception as e:
        #     print(f"[ERROR] Stream failed: {e}")
        # print("got third frame")
        
        greet_guests = robot.say("Now let's head to the dinosaur exhibit.")
        await go_to_museum_checkpoint(robot, robot_ip, use_absolute_coords=False, coords=Coordinates(x=2.0, y=0.0, theta=0.0),
            speech_content=(
                "The T-Rex, or Tyrannosaurus rex, was one of the largest land carnivores of all time, living during the late Cretaceous period."
            ),
            speech_timer=5,
            checkpoint_name="fourth"
        )
        
        # cont4 = robot.say("Now let's head to the dinosaur exhibit.")
        # walk4 = robot.go_to_relative(Coordinates(x=2.0, y=0.0, theta=0.0))
        # await walk4.completed()
        # print("finished fourth walk")
        # checkpoint4 = robot.say("The T-Rex, or Tyrannosaurus rex, was one of the largest land carnivores of all time, living during the late Cretaceous period.")
        # await asyncio.sleep(3)
        # print("finished fourth talk")
        # try:
        #     await stream_head_color(robot_ip)
        # except Exception as e:
        #     print(f"[ERROR] Stream failed: {e}")
        # print("got fourth frame")
        
        greet_guests = robot.say("Thank you for visiting the museum! I hope you enjoyed the tour. Let's head back to the entrance.")
        await go_to_museum_checkpoint(robot, robot_ip, use_absolute_coords=False, coords=Coordinates(x=2.0, y=0.0, theta=0.0),
            speech_content=(
                "Feel free to reach out to us from Enchanted Tools to book our services for your own events! Have a great day!"
            ),
            speech_timer=5,
            checkpoint_name="fifth"
        )
        
        # cont5 = robot.say("Thank you for visiting the museum! I hope you enjoyed the tour. Let's head back to the entrance.")
        # walk5 = robot.go_to_relative(Coordinates(x=-8.0, y=0.0, theta=0.0)) # -8, -8
        # await walk5.completed()
        # print("finished fifth walk")
        # checkpoint4 = robot.say("Feel free to reach out to us from Enchanted Tools to book our services for your own events! Have a great day!")
        # await asyncio.sleep(3)
        # print("finished fifth talk")
        # try:
        #     await stream_head_color(robot_ip)
        # except Exception as e:
        #     print(f"[ERROR] Stream failed: {e}")
        # print("got fifth frame")
        # print("Program completed successfully!!! :)")
        
        
        ### WORKING
        # # 1) make VideoAPI, start capture thread
        # video_api = VideoAPI(display=False, timeout=5000)
        # full_url = f"rtsp://{robot_ip}:8554/head_color"
        # video_api.start(full_url)

        # # 2) give it a couple of seconds to fill the buffer
        # time.sleep(2)
        
        # num = np.random.randint(1000, 9999)
        # # 3) display frames until you hit 'q'
        # try:
        #     while True:
        #         frame = video_api.get_current_frame()
        #         if frame is not None:
        #             cv2.imshow("head_color", frame)
        #             cv2.imwrite(f"frames/head_color_snapshot_{num}.png", frame)
        #             print(f"save frames/head_color_snapshot_{num}.png")
        #         if cv2.waitKey(1) & 0xFF == ord("q"):
        #             break
        # except Exception as e:
        #     print(f"An error occurred: {e}")
        
        
        # WORKING STREAMER
        # vsm = robot.video_stream_manager
        # vsm.stream_base_url = "rtsp://10.6.32.15:8554"
        # vsm.add_stream("head_color", "head_color")
        # vsm.set_display("head_color", True)
        # # hang indefinitely (or until the user presses “q” in the window)
        # await asyncio.Future()
        
        # vsm = robot.video_stream_manager
        # vsm.stream_base_url = f"rtsp://{robot_ip}:8554"
        # vsm.add_stream("head_color", "head_color")
        # vsm.set_display("head_color", False)  # or True if you want
        
        ### END
        
        
if __name__ == "__main__":
    asyncio.run(main())