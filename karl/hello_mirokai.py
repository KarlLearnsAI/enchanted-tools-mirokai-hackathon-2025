import asyncio
from pymirokai.robot import connect
from pymirokai.models.data_models import Coordinates
# from pymirokai.robot.video import VideoStreamManager
import time
import cv2

robot_ip = "10.6.32.15"
api_key  = "admin"

async def main():  
    async with connect(api_key, robot_ip) as robot:
        
        vsm = robot.video_stream_manager
        vsm.stream_base_url = "rtsp://10.6.32.15:8554"
        vsm.add_stream("head_color", "head_color")
        vsm.set_display("head_color", True)
        # hang indefinitely (or until the user presses “q” in the window)
        await asyncio.Future()
        
        # greet_guests = robot.say("Hello, museum enthusiasts!")
        # walk = robot.go_to_relative(Coordinates(x=2.0, y=2.0, theta=0.0))
        # await walk.completed()
        # checkpoint1 = robot.say("Napoleon Bonaparte was a French military leader who rose to prominence during the French Revolution and crowned himself Emperor of the French in 1804.")
        # await asyncio.sleep(3)
        
        
        # robot.video_stream_manager.add_stream(stream_name="head_color", stream_url="head_color")
        # # get the frame
        # cur_frame = robot.video_stream_manager.get_frame()
        # # visualize the frame
        
        ### start
        
        # Display frames
         # 1) Point it at your robot’s RTSP endpoint
    # vsm = VideoStreamManager(stream_base_url="rtsp://10.6.32.15:8554")

    # # 2) Add your camera feed by name
    # vsm.add_stream(stream_name="head_color", stream_url="head_color")

    # # 3) Turn display ON for that feed
    # vsm.set_display("head_color", True)

    # # 4) Let it run until you hit Ctrl+C (or window “q”)
    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     pass
    # finally:
    #     # 5) Clean up all windows and threads
    #     vsm.close_all_streams()
        
        
        # Save a frame
        vsm = robot.video_stream_manager
        # 1) MUST set the base URL so VideoStreamManager.add_stream works
        vsm.stream_base_url = f"rtsp://{robot_ip}:8554"

        # 2) actually add the stream
        vsm.add_stream("head_color", "head_color")

        # 3) let it start grabbing
        await asyncio.sleep(2)

        # 4) now get and save
        frame = vsm.get_frame("head_color")
        if frame is None:
            print("No frame available yet!")
        else:
            cv2.imwrite("head_color_snapshot.png", frame)
            print("Saved head_color_snapshot.png")
        
        
        
        
        # vsm = robot.video_stream_manager
        
        # # Make sure your base URL is set before adding:
        # # robot.video_stream_manager.stream_base_url = "rtsp://10.6.32.15:8554"
        
        # # vsm.add_stream(stream_name="head_color", stream_url="head_color")
        
        # # Give the capture thread a little time to start pulling frames
        # await asyncio.sleep(2)
        
        # # Now ask for the latest frame by name
        # frame = vsm.get_frame("head_color")
        # if frame is None:
        #     print("No frame available yet!")
        # else:
        #     # Save to disk (it's just a numpy array)
        #     cv2.imwrite("head_color_snapshot.png", frame)
        #     print("Saved head_color_snapshot.png")
        
        # # …rest of your tour logic…
        # await robot.say("Now, let's move to the next exhibit…").completed()
        
        
        ### end
        
        
        # cont2 = robot.say("Now, let's move to the next exhibit to see the Mona Lisa.")
        # walk2 = robot.go_to_relative(Coordinates(x=0.0, y=2.0, theta=0.0))
        # await walk2.completed()
        # checkpoint2 = robot.say("The Mona Lisa, painted by Leonardo da Vinci, is one of the most famous works of art in the world, known for its enigmatic smile.")
        # await asyncio.sleep(3)
        
        # cont3 = robot.say("Next, we will visit the ancient Egyptian artifacts.")
        # walk3 = robot.go_to_relative(Coordinates(x=2.0, y=2.0, theta=0.0))
        # await walk3.completed()
        # checkpoint3 = robot.say("The Rosetta Stone is a granodiorite stele inscribed with a decree issued in Memphis, Egypt in 196 BC.")
        # await asyncio.sleep(3)
        
        # # cont4 = robot.say("Now let's head to the dinosaur exhibit.")
        # # walk4 = robot.go_to_relative(Coordinates(x=4.0, y=2.0, theta=0.0))
        # # await walk4.completed()
        # # checkpoint4 = robot.say("The T-Rex, or Tyrannosaurus rex, was one of the largest land carnivores of all time, living during the late Cretaceous period.")
        # # await asyncio.sleep(3)
        
        # cont5 = robot.say("Thank you for visiting the museum! I hope you enjoyed the tour. Let's head back to the entrance.")
        # walk5 = robot.go_to_relative(Coordinates(x=-4.0, y=-6.0, theta=0.0)) # -8, -8
        # await walk5.completed()
        # checkpoint4 = robot.say("Feel free to reach out to us from Enchanted Tools to book our services for your own events! Have a great day!")
        # await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(main())