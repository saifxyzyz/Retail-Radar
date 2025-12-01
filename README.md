# PriceTracker ADK: AI-Powered Market Analysis

**A cutting-edge solution for real-time price intelligence, built for the Google ADK Kaggle Hackathon.**


## Elevator Pitch

In today's dynamic e-commerce landscape, maintaining a competitive edge requires constant market awareness. Manual price tracking is not only tedious but also prone to errors and delays. PriceTracker ADK is an AI-powered, autonomous market analysis tool that leverages the power of Google's Gemini Pro to provide real-time price intelligence. Our solution empowers businesses to make data-driven pricing decisions, optimize their product positioning, and maximize profitability.

## Web Interface

PriceTracker ADK now features an interactive web interface that allows you to run the analysis and view the results in real-time. The interface provides a "Start Analysis" button to initiate the process and displays the agent's output as it happens.

## Key Features

*   **AI-Powered Analysis:** At its core, PriceTracker ADK utilizes a sophisticated AI agent built with Google's Gemini Pro. This agent orchestrates the entire workflow, from data extraction to analysis and reporting.
*   **Automated Price Tracking:** Our tool automatically scrapes Google Shopping for the latest product prices, providing you with up-to-the-minute market data.
*   **Smart Data Filtering:** The AI agent intelligently filters out irrelevant listings, such as refurbished products or those with misleading prices, ensuring the accuracy of your analysis.
*   **Competitive Benchmarking:** PriceTracker ADK calculates the average market price for your products, allowing you to benchmark your pricing strategy against the competition.
*   **Detailed Product Analysis:** The analysis now includes product 'Status', 'Maximum Number of reviews', and 'Average of all ratings'.
*   **Automated Reporting:** The final analysis is presented in a clean, easy-to-read Excel report, complete with your current prices and the calculated market averages.
*   **Actionable Insights:** Our `analyst_agent` provides high-level business insights, suggesting whether to increase or decrease prices based on the market data.

## Tech Stack

*   **AI/ML:** Google Gemini (`gemini-2.5-flash`)
*   **Programming Language:** Python
*   **Backend:** FastAPI
*   **Libraries:**
    *   `google-adk`: For building and managing our AI agents.
    *   `serpapi`: For real-time Google Shopping data extraction.
    *   `openpyxl` & `xlsxwriter`: For seamless Excel integration.
    *   `asyncio`: For high-performance, asynchronous operations.

## How It Works

1.  **Data Ingestion:** The process begins by reading a list of your products from an Excel file (`book.xlsx`).
2.  **Price Scraping:** The `track_price` tool, powered by SerpApi, scrapes Google Shopping for the current prices of each product.
3.  **AI-Powered Analysis:** A `SequentialAgent` manages the workflow, first using a `search_agent` to process the scraped data. It calculates the average price, filters out noise, and prepares the data for reporting.
4.  **Report Generation:** The `save_search` tool generates a detailed Excel report in the `verdict` folder, comparing your prices to the market average.
5.  **Business Insights:** The `analyst_agent` provides a final layer of analysis, offering strategic recommendations for your pricing strategy.
6.  **Real-time Updates:** The FastAPI backend uses a WebSocket to stream the agent's output to the web interface in real-time.

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/saifxyzyz/Retail-Radar.git
    cd Retail-Radar
    ```
2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Add your SerpApi API key:**
    *   Create a `.env` file, paste this `SERPAPI_KEY= #YOUR_API_KEY_HERE`, and replace the comment with your actual [SerpApi](https.serpapi.com/) key
4.  **Prepare your product list:**
    *   Open `book.xlsx` and replace the sample data with your own product list. Make sure to follow the specified format.
5.  **Run the agent:**
    *   **CLI:**
        ```bash
        python agent.py
        ```
    *   **Web Interface:**
        ```bash
        python backend.py
        ```
        Then wait for the application to pop-up on your browser.
6.  **Check the results:**
    *   The final report will be saved in the `verdict` folder.

## Future Work

*   **Enhanced Interactive Dashboard:** A more advanced web-based dashboard for visualizing pricing trends and market data.
*   **Historical Price Analysis:** Track price changes over time to identify trends and seasonality.
*   **Full Multi-Platform Support:** Expand the tool to officially support tracking prices from other e-commerce platforms like Amazon and eBay.
*   **Advanced Anomaly Detection:** Implement more sophisticated algorithms for detecting and filtering out anomalous data points.

---
*This project was developed for the Google ADK Kaggle Hackathon.*
