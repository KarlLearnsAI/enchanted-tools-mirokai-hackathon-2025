import asyncio
from pymirokai.robot import connect
from pymirokai.models.data_models import Coordinates
import time

robot_ip = "10.6.32.15"
api_key  = "admin"

async def main():  
    async with connect(api_key, robot_ip) as robot:
        greet_guests = robot.say("Hello, museum enthusiasts!")
        walk = robot.go_to_relative(Coordinates(x=2.0, y=2.0, theta=0.0))
        await walk.completed()
        checkpoint1 = robot.say("Napoleon Bonaparte was a French military leader who rose to prominence during the French Revolution and crowned himself Emperor of the French in 1804.")
        await asyncio.sleep(3)
        
        cont2 = robot.say("Now, let's move to the next exhibit to see the Mona Lisa.")
        walk2 = robot.go_to_relative(Coordinates(x=0.0, y=2.0, theta=0.0))
        await walk2.completed()
        checkpoint2 = robot.say("The Mona Lisa, painted by Leonardo da Vinci, is one of the most famous works of art in the world, known for its enigmatic smile.")
        await asyncio.sleep(3)
        
        cont3 = robot.say("Next, we will visit the ancient Egyptian artifacts.")
        walk3 = robot.go_to_relative(Coordinates(x=2.0, y=2.0, theta=0.0))
        await walk3.completed()
        checkpoint3 = robot.say("The Rosetta Stone is a granodiorite stele inscribed with a decree issued in Memphis, Egypt in 196 BC.")
        await asyncio.sleep(3)
        
        # cont4 = robot.say("Now let's head to the dinosaur exhibit.")
        # walk4 = robot.go_to_relative(Coordinates(x=4.0, y=2.0, theta=0.0))
        # await walk4.completed()
        # checkpoint4 = robot.say("The T-Rex, or Tyrannosaurus rex, was one of the largest land carnivores of all time, living during the late Cretaceous period.")
        # time.sleep(1)
        
        cont5 = robot.say("Thank you for visiting the museum! I hope you enjoyed the tour. Let's head back to the entrance.")
        walk5 = robot.go_to_relative(Coordinates(x=-4.0, y=-6.0, theta=0.0)) # -8, -8
        await walk5.completed()
        checkpoint4 = robot.say("Feel free to reach out to us from Enchanted Tools to book our services for your own events! Have a great day!")
        time.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())