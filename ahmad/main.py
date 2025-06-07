import asyncio
from pymirokai.robot import Robot
from pymirokai.models.data_models import Coordinates

robot_ip = "10.6.32.15"
api_key  = "admin"

async def main():  
    async with Robot.connect(api_key, robot_ip) as robot:
        mission = robot.go_to_relative(Coordinates(x=1.0, y=2.0, theta=0.0))
        robot.add_new_location_at_robot_position("Napoleon Bonaparte")
        print(robot.list_all_locations())

# robot.list_all_locations() might be useful


if __name__ == "__main__":
    asyncio.run(main())
