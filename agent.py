from dis import Instruction
from os import name
from requests import session
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from my_tools import track_price, extract_main_file, save_search
import asyncio
import re
import os
from google.genai import types
from google.adk.models.google_llm import Gemini
GEMINI_MODEL = "gemini-2.5-flash"
retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)
search_agent = Agent(
    model = Gemini(model=GEMINI_MODEL, retry_options = retry_config),
    name = "search_assistant",
    instruction="""You are a skilled data analyst, your purpose is to:
        1. fetch the product names and prices using 'extract_main_file' tool, path to main file is book.xlsx
        2. fetch the prices of the products using the track_price tool
        2. filter out the shady products that are either on emi, refurbished or have an insanely low price compared to others
        3. The fetched information will be in JSON format
        5. I want you to calculate the average price of the products and pass the json data included the listing price retrieved using extract_main_file and the
        calculated price to the 'save_search' tool

        IMPORTANT XLSX RULES:
        - Do NOT use commas inside the Price column numbers (e.g. write 70000, NOT ₹70,000).
        - The price column must only contain numerical values, if the price column contains any other value, ignore the whole row
        - If a price has a comma, Excel will break the file. Remove it.
        """,
    tools=[extract_main_file, track_price, save_search]
)
#
# analyst_agent = Agent(
#     name="analyst",
#     model= GEMINI_MODEL,
#     Instruction= """You are a skilled business analyst, your purpose is to take the response from
#     the search agent and advice the user on whether to buy the product or not"""
# )


async def main_async():
    session_id = "session-1"
    user_id = "user-1"
    app_name = "price-tracker"
    # user_input = input("What product do you want me to look for? ")
    runner = InMemoryRunner(agent=search_agent, app_name=app_name)
    # usr_msg = Content(parts=[Part(text=user_input)])
    print("--- preparing Agent ---")
    await runner.session_service.create_session(
        session_id = session_id,
        user_id = user_id,
        app_name = app_name
    )
    query = "start the product analysis pipeline immediately"
    print(f"User Query: {query}")
    content = types.Content(role='user', parts=[types.Part(text=query)])
    print("--- Session Created ---")
    async for event in runner.run_async(
        user_id = user_id,
        session_id = session_id,
        new_message = content
    ):
        print(event)
        # if hasattr(event, 'content') and event.content and event.content.parts:
        #     for part in event.content.parts:
        #         if part.text:
        #             match = re.search(r"```csv\n(.*?)\n```", part.text, re.DOTALL)
        #             if match:
        #                 csv_content = match.group(1)
        #                 folder = "thesis"
        #                 count = 0
        #                 filename = f"{user_input.replace(' ', '_')}_prices.csv"
        #                 finalfilepath = os.path.join(folder, filename)
        #                 if not os.path.exists(folder):
        #                     os.mkdir(folder)
        #                 while os.path.exists(finalfilepath):
        #                     count += 1
        #                     filename = f"{user_input.replace(' ', '_')}_prices{count}.csv"
        #                     finalfilepath = os.path.join(folder, filename)
        #
        #                 try:
        #                     with open(finalfilepath, "w", encoding="utf-8-sig") as f:
        #                         f.write(csv_content)
        #                     print(f"\n✅ SUCCESS: Data saved to {filename}!")
        #                 except Exception as e:
        #                     print(f"❌ Error saving file: {e}")
if __name__ == "__main__":
    asyncio.run(main_async())

