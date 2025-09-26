# MarketMind: AI-Powered Investment Analyst

This project is an AI-powered investment analyst that uses a system of autonomous agents to conduct financial research. It automatically gathers and synthesizes company data, including news, financials, SEC filings, and LSEG Tick History data to generate comprehensive investment reports.

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [LSEG Tick History Integration](#lseg-tick-history-integration)
- [Tick History SQL Queries](#tick-history-sql-queries)
- [Extending with Custom Agents](#extending-with-custom-agents)
- [Why Google's Agents Development Kit (ADK)?](#why-googles-agents-development-kit-adk)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation & Configuration](#installation--configuration)
- [Deployment & Usage](#deployment--usage)
- [Sample Questions](#sample-questions)
- [Potential Customers](#potential-customers)
- [Contributing](#contributing)

## Features
*   **Automated Data Gathering**: Fetches company profiles, latest news, basic financials, insider sentiment, and SEC filings.
*   **LSEG Tick History Integration**: Utilizes LSEG Tick History data to perform Volume Weighted Average Price (VWAP) analysis.
*   **Intelligent Synthesis**: Uses a final-layer agent to synthesize all collected data into a coherent, structured investment report.
*   **Dynamic Symbol Lookup**: Automatically finds the correct stock ticker for a given company name.
*   **Modular & Extensible**: New data sources or analytical capabilities can be added by creating new agents.
*   **Parallel Processing**: Leverages parallel agent execution to speed up the data collection process significantly.

## Architecture
MarketMind is built using a multi-agent system, where each agent is a specialized worker responsible for a specific task. This architecture is orchestrated using Google's ADK.

1.  **`symbol_lookup_agent`**: The entry point. It takes a company name and finds the corresponding stock symbol.
2.  **`data_retrieval_agent` (`ParallelAgent`)**: Once the symbol is found, this agent triggers multiple sub-agents to run concurrently, each fetching a different piece of information:
    *   `company_news_agent`
    *   `company_profile_agent`
    *   `company_basic_financials_agent`
    *   `insider_sentiment_agent`
    *   `sec_filings_agent`
    *   `vwap_agent`: Converts the stock symbol to a RIC and calculates the VWAP using LSEG Tick History data.
3.  **`report_creation_agent`**: After all data is collected, this agent receives the outputs from the parallel agents. It synthesizes the information into a single, comprehensive financial report.

This entire workflow is wrapped in a `SequentialAgent` (`sqeuential_agent`) to ensure the steps run in the correct order: Symbol Lookup -> Data Retrieval -> Report Creation.

## LSEG Tick History Integration

The project integrates with LSEG Tick History via Google BigQuery to provide deep, market-data-driven insights. The `vwap_agent` is responsible for this integration.

The agent first converts a company's stock symbol (e.g., "NVDA") into a Reuters Instrument Code (RIC) (e.g., "NVDA.OQ"). This RIC is then used to query the LSEG Tick History dataset in BigQuery.

The `getVWAP` function in `investment_analyst_agent/tickhistorytool/tickhistory.py` constructs and executes a SQL query to calculate the Volume Weighted Average Price (VWAP) for the given RIC over a specified date range. The results are then returned as a JSON object to be included in the final investment report.

## Tick History SQL Queries

The primary SQL query used for Tick History analysis is the VWAP calculation. The query is defined in `vwap.sql` and executed by the `getVWAP` function.

Here is a breakdown of the query:

```sql
### Obtain VWAP for RIC
WITH AllTrades AS(
    SELECT Date_Time,RIC,Price,Volume, Ask_Price,Ask_Size,Bid_Price,Bid_Size,Qualifiers
    FROM `dbd-sdlc-prod.NYS_NORMALISED.NYS_NORMALISED`
    WHERE Price IS NOT NULL
    -- Specific Date/Time range:
    AND (Date_Time BETWEEN "{1} 00:00:00.000000" AND "{2} 23:59:59.999999")
    AND Type = "Trade"
    AND VOLUME > 0
    AND PRICE > 0
    -- All trades reported as "On Book" & "Regular Trades"
    -- This is according to the FIX specs, most European trading venues adhere to this
    -- AND RIGHT(REGEXP_EXTRACT(Qualifiers, r";(.*)\[MMT_CLASS\]"),14) LIKE "12%"
)
SELECT CAST (extract(DATE FROM Date_Time) AS STRING) AS date_time, RIC, ROUND(SAFE_DIVIDE(SUM(Volume*Price),SUM(Volume)),3) AS VWAP,SUM(Volume) AS TotalVolume,AVG(Price) AS AvgPrice,
COUNT(RIC) AS NumTrades, MAX(Ask_Price) AS MaxAskPrice,MAX(Ask_Size) as MaxAskSize,
    MAX(Bid_Price) AS MaxBidPrice, MAx(Bid_Size) AS MaxBidSize
FROM AllTrades
WHERE RIC IN (\'{0}\'')
GROUP BY RIC, date_time
ORDER BY 1,2
```

-   **`WITH AllTrades AS (...)`**: This Common Table Expression (CTE) filters the raw tick data from the `dbd-sdlc-prod.NYS_NORMALISED.NYS_NORMALISED` table. It selects trades within a specific date range, ensuring that they have a valid price and volume.
-   **`SELECT ...`**: The main query calculates the following metrics for each RIC and date:
    -   `VWAP`: The Volume Weighted Average Price, calculated as `SUM(Volume * Price) / SUM(Volume)`.
    -   `TotalVolume`: The total trading volume.
    -   `AvgPrice`: The average trade price.
    -   `NumTrades`: The number of trades.
    -   `MaxAskPrice`, `MaxAskSize`, `MaxBidPrice`, `MaxBidSize`: Maximum ask and bid prices and sizes.
-   **`WHERE RIC IN (\'{0}\'')`**: This filters the data for the specific RIC provided to the agent.
-   **`GROUP BY RIC, date_time`**: The results are grouped by RIC and date to provide daily calculations.

## Extending with Custom Agents

The integration with LSEG Tick History opens up numerous possibilities for building more advanced custom agents. Here are a few examples:

*   **Intraday Momentum Agent**: An agent that analyzes intraday price and volume patterns to identify momentum trading opportunities. This agent could query Tick History for minute-by-minute data and apply technical indicators like Moving Average Convergence Convergence (MACD) or Relative Strength Index (RSI).
*   **Market Microstructure Agent**: An agent that examines the bid-ask spread, order book depth, and trade sizes to analyze market liquidity and trading behavior. This could be used to assess the market impact of large trades or to detect signs of market manipulation.
*   **Event Study Agent**: An agent that measures the impact of news events (e.g., earnings announcements, mergers) on a stock's price and trading volume. This agent would correlate news data with high-frequency Tick History data to perform event studies.
*   **Algorithmic Trading Backtesting Agent**: An agent that backtests algorithmic trading strategies using historical tick data. This would allow quantitative analysts to simulate their strategies and evaluate their performance before deploying them in a live market.

## Why Google's Agents Development Kit (ADK)?
The choice of Google's ADK was pivotal for building a sophisticated and maintainable agent-based system.

*   **Powerful Orchestration**: ADK provides high-level abstractions like `SequentialAgent` and `ParallelAgent` that make it simple to design and implement complex agent workflows. Orchestrating a multi-step, parallel data-gathering process becomes declarative and easy to understand.
*   **Modularity and Reusability**: The framework encourages breaking down large problems into smaller, manageable tasks, each handled by a distinct agent. These agents (`company_news_agent`, `sec_filings_agent`, etc.) are self-contained and can be easily reused in other financial analysis applications.
*   **Seamless Tool Integration**: ADK simplifies the process of equipping agents with tools. The project seamlessly integrates custom tools (like the Finnhub API wrappers and the LSEG Tick History tool) and pre-built Google tools (`google_search`), allowing agents to interact with external data sources and services effectively.
*   **Scalability**: The modular, agent-based design is inherently scalable. To add a new data source (e.g., social media sentiment), we only need to create a new tool and a corresponding agent and plug it into the `data_retrieval_agent` without refactoring the core logic.

## Getting Started

### Prerequisites
*   Python 3.9+
*   A Google Cloud Project with the Secret Manager and BigQuery APIs enabled.
*   Google Cloud SDK installed and authenticated.
*   A Finnhub API Key.
*   Access to the LSEG Tick History BigQuery dataset (`dbd-sdlc-prod.NYS_NORMALISED.NYS_NORMALISED`).

### Installation & Configuration

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd marketmind-lseg-adk
    ```

2.  **Set up a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    The `requirements.txt` file has been updated with all necessary packages.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Authenticate with Google Cloud:**
    This allows the application to access GCP services like Secret Manager and BigQuery.
    ```bash
    gcloud auth application-default login
    ```

5.  **Store your Finnhub API Key in Secret Manager:**
    Replace `[YOUR_PROJECT_ID]` with your Google Cloud Project ID and `[YOUR_FINNHUB_API_KEY]` with your key. The application is hardcoded to look for a secret named `FinHubAccessKey`.
    ```bash
    gcloud secrets create FinHubAccessKey --replication-policy="automatic" --project="[YOUR_PROJECT_ID]"
    echo -n "[YOUR_FINNHUB_API_KEY]" | gcloud secrets versions add FinHubAccessKey --data-file=-
    ```

## Deployment & Usage
This project is designed as a library of agents. You can import and run the main agent (`root_agent`) from your own Python scripts.

1.  **Create a `run.py` file in the root directory (a sample has been provided):**

    ```python
    # run.py
    import asyncio
    from investment_analyst_agent.agent import root_agent

    async def main():
        """
        Main function to run the investment analyst agent.
        """
        company_name = "NVIDIA"
        print(f"🚀 Starting analysis for: {company_name}")

        try:
            result = await root_agent.invoke(company_name)
            print("\n✅ Analysis Complete. Final Report:")
            print("------------------------------------")
            print(result)
            print("------------------------------------")
        except Exception as e:
            print(f"An error occurred during analysis: {e}")

    if __name__ == "__main__":
        asyncio.run(main())
    ```

2.  **Run the script:**
    From your terminal, simply execute the file:
    ```bash
    python3.12 run.py
    ```
    The agent will then begin the analysis process, printing the final, synthesized report to the console upon completion.

## Sample Questions
Here are some sample questions you can ask the agent:

*   "Can you give me a full investment report on Microsoft?"
*   "What is the latest news and financial standing of Tesla?"
*   "Analyze Apple's performance over the last quarter."
*   "I want to know about insider sentiment for Google."
*   "Generate a report on Amazon, including its recent SEC filings and VWAP analysis."

## Potential Customers
This automated financial research agent can provide significant value to a wide range of users in the financial industry:

*   **Asset Managers & Investment Analysts**: Automates the time-consuming process of data collection and preliminary analysis, allowing them to focus on high-level strategic decision-making and alpha generation.
*   **Hedge Funds**: Can be integrated into quantitative and qualitative analysis pipelines to quickly generate due diligence reports on potential investment targets, increasing the speed and breadth of market coverage.
*   **Retail Investors**: Empowers sophisticated individual investors with institutional-grade research tools, enabling them to make more informed decisions.
*   **Fintech Platforms**: Robo-advisors and financial content platforms can use this as a backend engine to provide automated, data-rich company analysis to their users.
*   **Financial Consultants & M&A Advisors**: Speeds up the initial due diligence phase when evaluating companies for mergers, acquisitions, or strategic partnerships.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs, feature requests, or improvements.
