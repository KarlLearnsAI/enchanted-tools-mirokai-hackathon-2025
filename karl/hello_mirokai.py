import asyncio
from pymirokai.robot import connect
from pymirokai.models.data_models import Coordinates

robot_ip = "10.6.32.15"
api_key  = "admin"

async def main():  
    async with connect(api_key, robot_ip) as robot:
        walk = robot.go_to_relative(Coordinates(x=1.0, y=2.0, theta=0.0))
        await walk.completed()
        greet_guests = robot.say("Hello, museum enthusiasts!")
        walk2 = robot.go_to_relative(Coordinates(x=3.0, y=3.0, theta=0.0))
        await walk2.completed()

if __name__ == "__main__":
    asyncio.run(main())