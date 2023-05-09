# Copyright (c) Microsoft. All rights reserved.

import asyncio
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.planning.basic_planner import BasicPlanner
from util import import_prompt


windupaskTemplate = import_prompt("./prompt/windupask.txt");
planprompt = import_prompt("./prompt/planprompt.txt");
    
kernel = sk.Kernel()

deployment, api_key, endpoint = sk.azure_openai_settings_from_dot_env()

kernel.add_chat_service("chart",AzureChatCompletion(deployment, endpoint, api_key))

chat_functions = kernel.import_semantic_skill_from_directory("./prompt", "windup")

async def chat() -> bool:

    # try:
    #     user_input = input("What platform do you want to migrate:> ")

    # except KeyboardInterrupt:
    #     print("\n\nExiting chat...")
    #     return False
    # except EOFError:
    #     print("\n\nExiting chat...")
    #     return False

    # if user_input == "exit":
    #     print("\n\nExiting chat...")
    #     return False
    
    planner = BasicPlanner()
    plan = await planner.create_plan_async(windupaskTemplate, kernel)
    print(plan.generated_plan.result)
    results = await planner.execute_plan_async(plan, kernel)
    print(results);
    return True


async def main() -> None:
    # chatting = True
    # while chatting:
    #     chatting = await chat()
    await chat()

    
if __name__ == "__main__":
    asyncio.run(main())


