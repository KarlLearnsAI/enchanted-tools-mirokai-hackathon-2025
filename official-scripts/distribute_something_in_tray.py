import argparse
from pymirokai.robot import connect, Robot
from pymirokai.models.data_models import Location
from pymirokai.utils.get_local_ip import get_local_ip
from pymirokai.utils.run_until_interruption import run_until_interruption


async def main() -> None:
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "-i",
        "--ip",
        help="Set the IP of the robot you want to connect.",
        type=str,
        default=get_local_ip(),
    )
    parser.add_argument(
        "-k",
        "--api-key",
        help="Set the API key of the robot you want to connect.",
        type=str,
        default="",
    )
    args = parser.parse_args()

    async with connect(ip=args.ip, api_key=args.api_key) as robot:

        object_to_distribute = input("What do you want to distribute in a tray: ")

        r: Robot = robot
        locations: list[Location] = await r.list_all_locations()
        location_ids = [location.id for location in locations]
        print(f"The robot will try to distribute {object_to_distribute} in these locations {location_ids}")
        input(
            f"Please prepare the {object_to_distribute} in the tray, and then press Enter to start the distribution. :)"
        )

        print("Grasping the tray...")
        await r.grasp_tray().completed()
        print(f"Distributing the {object_to_distribute}...")
        await r.distribute_something_in_tray(object_to_distribute).completed()


if __name__ == "__main__":
    run_until_interruption(main)
