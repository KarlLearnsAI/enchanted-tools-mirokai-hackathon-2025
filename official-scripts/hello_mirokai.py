import asyncio
from pymirokai.robot import connect
from pymirokai.models.data_models import Coordinates

robot_ip = "10.32.38.150"
api_key  = "admin"
from pymirokai.models.data_models import Coordinates

async def main():  
    async with connect(api_key, robot_ip) as robot:
        # Example of code using the connected robot object
        # await robot.say("Hello world").completed()
        mission = robot.go_to_relative(Coordinates(x=1.0, y=2.0, theta=0.0))
    # When the scope is finished, the robot object is disconnected

if __name__ == "__main__":
    # asyncio.run() will create the event loop, run main(), and close the loop
    asyncio.run(main())
