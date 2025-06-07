import argparse
from pymirokai.robot import connect
from pymirokai.mission import Mission
from pymirokai.utils.get_local_ip import get_local_ip
from pymirokai.utils.run_until_interruption import run_until_interruption


async def main() -> None:
    """Main entry point for the script."""
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
        await Mission(robot, "set_autonomous_goals", goals=[]).completed()


if __name__ == "__main__":
    run_until_interruption(main)
