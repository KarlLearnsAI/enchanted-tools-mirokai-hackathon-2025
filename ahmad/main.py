import asyncio
# from pymirokai.robot import Robot
from pymirokai.robot import connect
from pymirokai.models.data_models import Coordinates
import time

robot_ip = "10.6.32.15"
api_key  = "admin"

async def main():  
    async with connect(api_key, robot_ip) as robot:
        navigation_mission = robot.go_to_relative(Coordinates(x=2, y=0.0, theta=0.0))
        print("Going to the provided location...")
        await navigation_mission.completed()
        # saving_location_mission = robot.add_new_location_at_robot_position("Napoleon Bonaparte")
        # time.sleep(5)
        

        print(await robot.list_all_locations())

# robot.list_all_locations() might be useful


if __name__ == "__main__":
    asyncio.run(main())
