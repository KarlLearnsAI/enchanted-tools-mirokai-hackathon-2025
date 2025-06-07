import asyncio
from pymirokai.robot import connect
from pymirokai.models.data_models import Coordinates

robot_ip = "10.32.38.150"
api_key  = "admin"

async def main():  
    async with connect(api_key, robot_ip) as robot:
        mission = robot.go_to_relative(Coordinates(x=1.0, y=2.0, theta=0.0))
        mission = robot.say("Hello, world!")

if __name__ == "__main__":
    asyncio.run(main())