from dis import Instruction
from os import name
from requests import session
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from my_tools import track_price
import asyncio
from google.genai.types import Content, Part
import re
import os


GEMINI_MODEL = "gemini-2.0-flash"

search_agent = Agent(
    name = "search_assistant",
    model = GEMINI_MODEL,
    instruction="""You are a skilled data analyst, your purpose is to:
        1. fetch the prices of the product desired by the user using the track_price tool
        2. filter out the shady products, the list shouldn't include products on EMI or rent
        3. The fetched information will be in JSON format
        5.I want you to list all the products in an csv file, with the column names title, price, seller and link.

        IMPORTANT CSV RULES:
        - Do NOT use commas inside the Price column numbers (e.g. write 70000, NOT ₹70,000).
        - The price column must only contain numerical values, if the price column contains any other value, ignore the whole row
        - If a price has a comma, Excel will break the file. Remove it.
        """,
    tools=[track_price]
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
    user_input = input("What product do you want me to look for? ")
    runner = InMemoryRunner(agent=search_agent, app_name=app_name)
    usr_msg = Content(parts=[Part(text=user_input)])
    print("--- preparing Agent ---")
    await runner.session_service.create_session(
        session_id = session_id,
        user_id = user_id,
        app_name = app_name
    )
    print("--- Session Created ---")
    async for event in runner.run_async(
        user_id = user_id,
        session_id = session_id,
        new_message = usr_msg,
    ):
        print(event)
        if hasattr(event, 'content') and event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    match = re.search(r"```csv\n(.*?)\n```", part.text, re.DOTALL)
                    if match:
                        csv_content = match.group(1)
                        folder = "thesis"
                        count = 0
                        filename = f"{user_input.replace(' ', '_')}_prices.csv"
                        finalfilepath = os.path.join(folder, filename)
                        if not os.path.exists(folder):
                            os.mkdir(folder)
                        while os.path.exists(finalfilepath):
                            count += 1
                            filename = f"{user_input.replace(' ', '_')}_prices{count}.csv"
                            finalfilepath = os.path.join(folder, filename)

                        try:
                            with open(finalfilepath, "w", encoding="utf-8-sig") as f:
                                f.write(csv_content)
                            print(f"\n✅ SUCCESS: Data saved to {filename}!")
                        except Exception as e:
                            print(f"❌ Error saving file: {e}")
if __name__ == "__main__":
    asyncio.run(main_async())

