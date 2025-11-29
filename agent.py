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
from my_tools import file_to_analyze
from google.adk.agents import SequentialAgent

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
    instruction="""You are a granular Market Research Orchestrator. Follow this strict execution plan:

    PHASE 1: INVENTORY LOADING
    1. Call 'extract_main_file' (file: 'book.xlsx') to get the list of products and their internal costs.

    PHASE 2: MARKET DISCOVERY (CRITICAL: ITERATION REQUIRED)
    2. You must now loop through EVERY single product found in Phase 1. 
       - For EACH product, call the 'track_price' tool individually.
       - You must wait for the tool to return the list of competitor prices for that specific product.
       - DO NOT skip any products. If there are 5 products, you must call 'track_price' 5 times.

    PHASE 3: DATA REFINEMENT & CALCULATION
    3. For EACH product's specific search results:
       - Filter out outliers (refurbished/EMI/illogical prices).
       - Calculate the 'Market Average' strictly based on the NEW data fetched from 'track_price'. 
       - DO NOT average the prices from the original Excel file.
       - DO NOT calculate one global average for all products; I need one average PER product.

    PHASE 4: REPORTING
    4. Compile a final JSON list containing:
        - Product Name
        - Original Listing Price (from Phase 1)
        - Market Average Price (calculated in Phase 3)
        - Status (e.g., "Overpriced" if Listing > Market Average)
        - Maximum Number of reviews
        - Average of all ratings
    5. Pass this final JSON to 'save_search'.

    IMPORTANT DATA RULES:
    - Ignore rows with non-numerical prices in the source file.
    - Remove commas from numbers before processing.
        """,
    tools=[extract_main_file, track_price, save_search]
)

analyst_agent = Agent(
    name="analyst",
    model= GEMINI_MODEL,
    instruction = """ You are an expert analyst for a retail electronic store, use the file_to_analyze tools to retrieve data and repond with a breif report on each
    listed product, make suggestions to the retail store, for example if the market price of a product is lower than the listed price of the retail store, suggest the store to increase their \
    listed price, also look into the ratings to know if the product is good and the number of reviews to get to know the demand of the product""",
    tools=[file_to_analyze]
)

root_agent = SequentialAgent(
    name = "root_agent",
    sub_agents = [search_agent, analyst_agent],
    description = "Manages the execution of the sub agents"
)

async def main_async():
    session_id = "session-1"
    user_id = "user-1"
    app_name = "price-tracker"
    runner = InMemoryRunner(agent=root_agent, app_name=app_name)
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

