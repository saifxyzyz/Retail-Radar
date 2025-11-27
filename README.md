# 📈 PriceTracker ADK: AI-Powered Market Analysis

**A cutting-edge solution for real-time price intelligence, built for the Google ADK Kaggle Hackathon.**

## 🚀 Elevator Pitch

In today's dynamic e-commerce landscape, maintaining a competitive edge requires constant market awareness. Manual price tracking is not only tedious but also prone to errors and delays. PriceTracker ADK is an AI-powered, autonomous market analysis tool that leverages the power of Google's Gemini Pro to provide real-time price intelligence. Our solution empowers businesses to make data-driven pricing decisions, optimize their product positioning, and maximize profitability.

## ✨ Key Features

*   **🤖 AI-Powered Analysis:** At its core, PriceTracker ADK utilizes a sophisticated AI agent built with Google's Gemini Pro. This agent orchestrates the entire workflow, from data extraction to analysis and reporting.
*   **📊 Automated Price Tracking:** Our tool automatically scrapes Google Shopping for the latest product prices, providing you with up-to-the-minute market data.
*   **🧹 Smart Data Filtering:** The AI agent intelligently filters out irrelevant listings, such as refurbished products or those with misleading prices, ensuring the accuracy of your analysis.
*   **📈 Competitive Benchmarking:** PriceTracker ADK calculates the average market price for your products, allowing you to benchmark your pricing strategy against the competition.
*   **📝 Automated Reporting:** The final analysis is presented in a clean, easy-to-read Excel report, complete with your current prices and the calculated market averages.
*   **🧠 Actionable Insights:** Our `analyst_agent` provides high-level business insights, suggesting whether to increase or decrease prices based on the market data.

## 🛠️ Tech Stack

*   **AI/ML:** Google Gemini (`gemini-2.5-flash`)
*   **Programming Language:** Python
*   **Libraries:**
    *   `google-adk`: For building and managing our AI agents.
    *   `serpapi`: For real-time Google Shopping data extraction.
    *   `openpyxl` & `xlsxwriter`: For seamless Excel integration.
    *   `asyncio`: For high-performance, asynchronous operations.

## ⚙️ How It Works

1.  **Data Ingestion:** The process begins by reading a list of your products from an Excel file (`book.xlsx`).
2.  **Price Scraping:** The `track_price` tool, powered by SerpApi, scrapes Google Shopping for the current prices of each product.
3.  **AI-Powered Analysis:** The `search_agent`, a specialized Gemini Pro agent, processes the scraped data. It calculates the average price, filters out noise, and prepares the data for reporting.
4.  **Report Generation:** The `save_search` tool generates a detailed Excel report in the `verdict` folder, comparing your prices to the market average.
5.  **Business Insights:** The `analyst_agent` provides a final layer of analysis, offering strategic recommendations for your pricing strategy.

## 🚀 Getting Started

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
    *   Open `my_tools.py` and replace `"YOUR_SERPAPI_API_KEY"` with your actual SerpApi API key.
4.  **Prepare your product list:**
    *   Open `book.xlsx` and replace the sample data with your own product list. Make sure to follow the specified format.
5.  **Run the agent:**
    ```bash
    python agent.py
    ```
6.  **Check the results:**
    *   The final report will be saved in the `verdict` folder.

## 🔮 Future Work

*   **Interactive Dashboard:** A web-based dashboard for visualizing pricing trends and market data.
*   **Historical Price Analysis:** Track price changes over time to identify trends and seasonality.
*   **Multi-Platform Support:** Expand the tool to track prices from other e-commerce platforms like Amazon and eBay.
*   **Advanced Anomaly Detection:** Implement more sophisticated algorithms for detecting and filtering out anomalous data points.

---
*This project was developed for the Google ADK Kaggle Hackathon.*
