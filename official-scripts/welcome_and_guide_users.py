import argparse
import asyncio
import os
import subprocess  # nosec

from pymirokai.models.data_models import Location
from pymirokai.robot import Robot, connect
from pymirokai.utils.get_local_ip import get_local_ip
from pymirokai.utils.run_until_interruption import run_until_interruption


def clear_screen():
    # Cross-platform clear screen
    subprocess.run(["cls"] if os.name == "nt" else ["clear"], check=True)  # nosec


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

        r: Robot = robot
        locations: list[Location] = await r.list_all_locations()
        location_ids = [location.id for location in locations]

        while True:
            location_id = input(f"Choose a default location for the robot [{location_ids}]: ")
            if location_id in location_ids:
                break
            print(f"Invalid location. Please choose one of the following: {location_ids}")

        pddl_domain = ""
        pddl_problem = ""
        plan = ""
        runtime_prompt_id = "dialog_objective"

        try:
            r.set_autonomous_goals(
                goals=[
                    {
                        "goal_definition": "focused_user_imply_is_told",
                        "parameters": {"text_to_say": "Hello, I am Miroki"},
                    },
                    {
                        "goal_definition": "focused_user_imply_set_runtime_prompt",
                        "parameters": {
                            "key": runtime_prompt_id,
                            "value": "Your objective in the conversation is to know where the user wants to go and "
                            "then to call this tool: set_where_the_user_wants_to_be() with appropriate arguments. "
                            "Do not hesitate to be proactive in the conversation "
                            "in order to call the tool as soon as possible. "
                            "You are talking to an unidentified human.",
                        },
                    },
                    {
                        "goal_definition": "users_at_desired_location",
                        "parameters": {},
                    },
                    {
                        "goal_definition": "users_at_desired_location_imply_reset_robot_focus",
                        "parameters": {},
                    },
                    {
                        "goal_definition": "robot_at",
                        "parameters": {"location": location_id},
                    },
                    {
                        "goal_definition": "focus_any_user",
                        "parameters": {},
                    },
                ]
            )

            while True:
                pddl_domain = await r.pddl_domain()
                pddl_problem = await r.pddl_problem()
                plan = await r.autonomous_planning_output()

                clear_screen()
                print("Current plan:\n" + plan)
                await asyncio.sleep(1)

        finally:
            await r.set_autonomous_goals(goals=[]).completed()
            await r.set_runtime_prompt(key=runtime_prompt_id, value="").completed()

            while True:
                res = input("Do you want to print the last PDDL domain, problem and plan result in files? [y:N]: ")
                if res.lower() in ["y", "yes"]:
                    output_dir = "planning_context"
                    os.makedirs(output_dir, exist_ok=True)
                    with open(os.path.join(output_dir, "domain.pddl"), "w") as f:
                        f.write(pddl_domain)
                    with open(os.path.join(output_dir, "problem.pddl"), "w") as f:
                        f.write(pddl_problem)
                    with open(os.path.join(output_dir, "plan.txt"), "w") as f:
                        f.write(plan)
                    print(f"Files have been successfully written to the '{output_dir}' folder.")
                    break
                if res.lower() in ["n", "no", ""]:
                    break


if __name__ == "__main__":
    run_until_interruption(main)
