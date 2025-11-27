from itertools import product
from serpapi import GoogleSearch
import json
import openpyxl
import time
import csv
import xlsxwriter
from datetime import datetime

def track_price(product):
    params = {
        "engine": "google_shopping",
        "q": product,
        "location": "Hyderabad, Telangana, India",
        "sort_by": "1",
        "num": "5",
        "google_domain": "google.com",
        "hl": "en",
        "gl": "in",
        "api_key": "82f43ef55075a1e29270f6d8bfa52e708bf4a4eb3e9dada2dc9144552d050443"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    json_output = json.dumps(results, ensure_ascii=False)
    return json_output


def extract_main_file(file_name: str) -> dict[str, list[str]]:
    """
    Extracts the list of product names from the 3rd column of the main Excel file.
    Args:
        file_name: The path to the .xlsx file (e.g., "book.xlsx").
    """
    print(f"\n[TOOL] Extracting products from {file_name}...")
    try:
        # Load the workbook using openpyxl
        main_data = openpyxl.load_workbook(file_name, data_only=True)
        sheet = main_data.active
        product_names = []
        product_prices = ["My Prices"]
        # Iterate through the 3rd column (C)
        for namerow in sheet.iter_rows(min_col=3, max_col=3):
            cell = namerow[0]
            product_name = cell.value
            # Filter out empty cells or headers if necessary
            if product_name and isinstance(product_name, str) and product_name.lower() != "product name":
                product_names.append(product_name)
        
        for namerow in sheet.iter_rows(min_col=4, max_col=4):
            cell = namerow[0]
            product_price = cell.value
            # Filter out empty cells or headers if necessary
            if product_price and isinstance(product_price, int):
                product_prices.append(product_price)
        fin_dict = dict(zip(product_names, product_prices))
        print(f"[TOOL] Found {len(product_names)} products: {product_names} and {len(product_prices)} product prices: {product_prices}, final dict: {fin_dict}")

        return fin_dict

    except Exception as e:
        print(f"[ERROR] Failed to read Excel file: {e}")
        return {"products": [], "error": str(e)}
extract_main_file('book.xlsx')

def save_search(data_json: str) -> dict[str, str]:
    """
    Saves the final calculated product data to a CSV file.
    Args:
        data_json: A JSON string. The agent usually sends a list of objects 
                   like: '[{"Product": "Laptop", "Average Price": 50000}, ...]'
    """
    print(f"\n[TOOL] Saving final report...")
    now = datetime.now()
    current_datetime = now.strftime("%Y%m%d_%H%M%S")
    filename = f"final_market_analysis_{current_datetime}.xlsx"

    try:
        # 1. Parse the incoming JSON string
        data = json.loads(data_json)
        # 2. Normalize the data (Ensure it is a list of dictionaries)
        # Sometimes the agent wraps the list in a key like {"products": [...]}
        if isinstance(data, dict):
            # Take the first value found in the dict (e.g., the list inside "products")
            data = list(data.values())[0]
        if not isinstance(data, list):
            # If it's a single item, wrap it in a list
            data = [data]

        if not data:
            print("[TOOL] Warning: No data to save.")
            return {"status": "Error", "message": "Data list was empty."}

        # 3. Write to CSV
        # We dynamically get headers from the keys of the first item (e.g., "Product Name", "Average Price")
        fieldnames = data[0].keys()
        #
        # with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        #     dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        #     dict_writer.writeheader()
        #     dict_writer.writerows(data)
        #
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        for col_num, field in enumerate(fieldnames):
            worksheet.write(0, col_num, field)

        row_num = 1 
        for row_data in data:
            for col_num, field in enumerate(fieldnames):
                worksheet.write(row_num, col_num, row_data.get(field, ""))
            row_num += 1
        workbook.close()
        print(f"[SUCCESS] File saved as '{filename}' with {len(data)} rows.")
        return {
            "status": "Success", 
            "message": f"Successfully saved {len(data)} products to {filename}"
        }

    except json.JSONDecodeError:
        print(f"[ERROR] JSON Decode Failed. Input was: {data_json[:100]}...")
        return {"status": "Error", "message": "Agent provided invalid JSON."}
    except Exception as e:
        print(f"[ERROR] File Write Failed: {e}")
        return {"status": "Error", "message": str(e)}

