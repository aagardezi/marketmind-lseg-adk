import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.tools import agent_tool, AgentTool
from google.adk.tools import google_search
from .tools.generaltools import get_current_date
from .tools.finhubtools import symbol_lookup, company_news, company_profile, company_basic_financials, insider_sentiment, financials_reported, sec_filings
from .tickhistorytool.tickhistory import getVWAP
from .config import config



search_agent = Agent(
    name="search_agent",
    # model="gemini-2.5-flash",
    model=config.gemini_model,
    description=(
        "Agent to search about anything"
    ),
    instruction="I can answer your questions by searching the internet. Just ask me anything!",
    tools=[google_search],
)

symbol_to_ric_agent = Agent(
    name="symbol_to_ric_agent",
    # model="gemini-2.5-flash",
    model=config.gemini_model,
    description=(
        "Agent to convert symbol to RIC"
    ),
    instruction=(
        "convert the stock symbol to the RIC code and return the ric code in the response"
        "Get the RIC code for common stock traded on the New York Stock Exchange (NYSE)"
    ),
    tools=[google_search],
)

vwap_agent = Agent(
    name="vwap_agent",
    # model="gemini-2.5-flash",
    model=config.gemini_model,
    description=(
        "Agent to get the VWAP for a stock RIC"
    ),
    instruction=(
        "You are an investemnt helper agent that gets the VWAP for a stock RIC code."
        "Use the symbol_to_ric_agent to first get the ric code and use it as input to the getVWAP tool"
        "Return the VWAP table in the repsonse and an analysis of the results"
    ),
    tools=[AgentTool(agent=symbol_to_ric_agent), get_current_date, getVWAP],
    output_key="vwap_result"
)



symbol_lookup_agent = Agent(
    name="symbol_lookup_agent",
    # model="gemini-2.5-flash",
    model=config.gemini_model,
    description=(
        "You are an agent helping an investment analyst get a stock symbol name from a company name"
    ),
    instruction=(
        "You are an invesnt analysis agent looking at a company name to get the symbol"
        "You are a symbol lookup agent. Use the symbol_lookup tool to get a symbol from a company name"
        "use the symbol_lookup tool to get a stock symbol from a company name"
        "the symbol will be needed for subsiquent sub agents"
        "if you retrieive multiple symbols, make an assumption about what is the most likely symbol"
        "return the symbol in the response"
    ),
    tools=[symbol_lookup],
    output_key="symbol_lookup_result"
)

company_news_agent = Agent(
    name="company_news_agent",
    # model="gemini-2.5-flash",
    model=config.gemini_model,
    description=(
        "You are an agent helping an investment analyst get news for a stock symbol"
    ),
    instruction=(
        "You are an invesnt analysis agent looking at news for a company"
        "Use the company sumbol to retrieve company news and create a detailed summary of the news"
        "use the company_news tool to get the company news for the company"
        "The news can be used as part of analysing investment stratagies"
        "Output a detaild summary of thge finding"
        "Use the get_current_date tool to get the date for the news"
    ),
    tools=[get_current_date, company_news],
    output_key="company_news_result"
)

company_profile_agent = Agent(
    name="company_profile_agent",
    # model="gemini-2.5-flash",
    model=config.gemini_model,
    description=(
        "You are an agent helping an investment analyst a company profile for a stock symbol"
    ),
    instruction=(
        "You are an invesnt analysis agent looking at company profile for a company"
        "Use the company symbol to retrieve company profile and create a detailed summary of the profile"
        "use the company_profile tool to get the company profile for the company"
        "The profile can be used as part of analysing investment stratagies"
        "Output a detaild summary of thge finding"
    ),
    tools=[company_profile],
    output_key="company_profile_result"
)

company_basic_financials_agent = Agent(
    name="company_basic_financials_agent",
    # model="gemini-2.5-flash",
    model=config.gemini_model,
    description=(
        "You are an agent helping an investment analyst a get the company basic financials for a stock symbol"
    ),
    instruction=(
        "You are an invesnt analysis agent looking at company basic financials for a company"
        "Use the company symbol to retrieve company basic financials and create a detailed summary of the financial statement of the company"
        "use the company_basic_financials tool to get the company basic financials for the company"
        "The financials can be used as part of analysing investment stratagies"
        "Output a detaild summary of thge finding"
    ),
    tools=[company_basic_financials],
    output_key="company_basic_financials_result"
)

# financials_reported_agent = Agent(
#     name="financials_reported_agent",
#     model="gemini-2.5-flash",
#     description=(
#         "You are an agent helping an investment analyst a analysing financials reported for a stock symbol"
#     ),
#     instruction=(
#         "You are an invesnt analysis agent looking at financials reported for a company"
#         "Use the company symbol to retrieve the financials reported for the company create a detailed summary of the financial statement of the company"
#         "use the financials_reported tool to get the financials reported for the company"
#         "The financials can be used as part of analysing investment stratagies"
#         "Output a detaild summary of thge finding"
#     ),
#     tools=[financials_reported],
#     output_key="financials_reported_result"
# )

sec_filings_agent = Agent(
    name="sec_filings_agent",
    # model="gemini-2.5-flash",
    model=config.gemini_model,
    description=(
        "You are an agent helping an investment analyst a analysing sec filings for a company based on its stock symbol"
    ),
    instruction=(
        "You are an invesnt analysis agent looking at SEC filings for a company"
        "Use the company symbol to retrieve the sec filings for the company and create a detailed summary of the filings"
        "use the sec_filings tool to get the sec filings for the company"
        "The filings can be used as part of analysing investment stratagies"
        "Output a detaild summary of thge finding"
    ),
    tools=[sec_filings],
    output_key="sec_filings_result"
)

insider_sentiment_agent = Agent(
    name="insider_sentiment_agent",
    # model="gemini-2.5-flash",
    model=config.gemini_model,
    description=(
        "You are an agent helping an investment analyst a analysing insider sentiment for a company based on its stock symbol"
    ),
    instruction=(
        "You are an invesnt analysis agent looking at insider sentiment for a company"
        "Use the company symbol to retrieve the insider sentiment for the company and create a detailed summary of it"
        "use the insider_sentiment tool to get the insider sentiment for the company"
        "The insider sentiment can be used as part of analysing investment stratagies"
        "Output a detaild summary of thge finding"
        "Use the get_current_date tool to get the date"
    ),
    tools=[get_current_date,insider_sentiment],
    output_key="insider_sentiment_result"
)

report_creation_agent = Agent(
    name="report_creation_agent",
    # model="gemini-2.5-flash",
    model=config.gemini_model,
    description=(
        "You are an agent helping an investment analyst create a report on an asset or stock"
    ),
    instruction=(
        """
        Your primary task is to synthesize the following research summaries, clearly attributing findings to their source areas. Structure your response using headings for each topic. Ensure the report is coherent and integrates the key points smoothly.
        **Crucially: Your entire response MUST be grounded *exclusively* on the information provided in the 'Input Summaries' below. Do NOT add any external knowledge, facts, or details not present in these specific summaries.**
         **Input Summaries:**

 *   **Company Profile:**
     {company_profile_result}:**
     **Company News:**
     {company_news_result}
 *   **Basic Financials:**
     {company_basic_financials_result}
     {vwap_result}
     **SEC Filings:**
     {sec_filings_result}
     **Insider Sentiment:**
     {insider_sentiment_result}




        **Comprehensive Report:** Your report should be comprehensive, detailed and contain the following sections:
                            *   **Company Profile:**  Include a detailed overview of the company, its industry, and its business model. Use the data above to get the company profile.
                            *   **Company News:** Summarize the latest significant news impacting the company. Make it detailed. Use the data above to get the company news.
                            *   **Basic Financials:** Present key financial metrics and ratios for the company, covering recent periods (using current year as default period). Use the data above to get the company basic financials. Include a section on the VWAP analysis.
                            *   **Insider Sentiment:**  Report on insider trading activity and overall sentiment expressed by company insiders. Use the data above to get the insider sentiment.
                            *   **SEC Filings:**  Provide an overview of the company's recent SEC filings, highlighting any significant disclosures and a summary of the findings. Make it detailed. Use the data above to get the sec filings.




                        **4. Data Handling and Error Management:**

                        *   **Data Completeness:** If a function requires date that is not present or unavailable, use the current year as the default period. Report missing data but don't let it stop you.
                        *   **Function Execution:** Execute functions carefully, ensuring you have the necessary data, especially dates and symbols, before invoking any function.
                        *   **Clear Output:** Present results in a clear and concise manner, suitable for an asset management investor.

                        **5. Analytical Perspective:**

                        *   **Asset Management Lens:** Conduct all analysis with an asset manager's perspective in mind. Evaluate the company as a potential investment, focusing on risk, return, and long-term prospects."""
    )
)

data_retrieval_agent = ParallelAgent(
    name="data_retrieval_agent",
    # model="gemini-2.5-flash",
    description=(
        "You are an agent that helps a financial analyst to retreive info about a company or stock"
    ),
    # instruction=(
    #     "You are a financal assistant agent that uses all the sub agents to retreive info about a company or a stock"
    #     "Use the company_news_agent to get company news"
    #     "Use the company_profile_agent to get company profile"
    #     "Use the company_basic_financials_agent to get company basic financials"
    #     "Use the insider_sentiment_agent to get insider sentiment"
    #     "Use the financials_reported_agent to get financials reported"
    #     "Use the sec_filings_agent to get sec filings"
    # ),
    sub_agents=[company_news_agent,company_profile_agent, company_basic_financials_agent, insider_sentiment_agent, sec_filings_agent, vwap_agent]
)


sequential_agent = SequentialAgent(
    name="sequential_agent",
    description=(
        "you are the agent that runs the process for collecting the data and creating the report"
    ),
    sub_agents=[symbol_lookup_agent, data_retrieval_agent, report_creation_agent]
)


root_agent = Agent(
    name="investment_agent",
    # model="gemini-2.5-flash",
    model=config.gemini_model,
    description=(
        "You are an agent helping an investment analyst at an asset manager"
    ),
    instruction=(
        # "You are an investment analyst agent that creates an analysis of assets and stock"
        # "You use the tools and subagents at your disposal to get the data and summarise the data"
        # "Include a detailed summary in the response"
        # "use the get_current_date tool to get the current data in order to use with any of the subagents"
        # "use the symbol_lookup_agent to get a stock symbol from a company name"
        # "use the news subagent to get company news"
        # "In the response include a detailed section on the news"
        # "If the user does not specify a start date or end date, use the current date as the start date using the get_current_date tool"
        # "use the date from 6 months ago as the end date"
        # "If the user specifies the date as a duration, use get_current_date to get the start date and calculate it"
        # "make sure to always use the get_current_date tool to do the date calculation"
        # "use all the sub agnets to create a report on the investment"
        """You are a highly skilled financial analyst specializing in asset management. Your task is to conduct thorough financial analysis and generate detailed reports from an investor's perspective. Follow these guidelines meticulously:

                        **1. Symbol Identification and Lookup:**

                        *   **Primary Symbol Focus:** When multiple symbols exist for a company, prioritize the *primary* symbol, which typically does *not* contain a dot (".") in its name (e.g., "AAPL" instead of "AAPL.MX").
                        *   **Mandatory Symbol Lookup:** Before executing any other functions, always use the `symbol_lookup` function to identify and confirm the correct primary symbol for the company under analysis. Do not proceed without a successful lookup.
                        *   **Handle Lookup Failures:** If `symbol_lookup` fails to identify a symbol, inform the user and gracefully end the analysis.

                        **2. Date Handling:**

                        *   **Current Date Determination:** Use the `get_current_date` function to obtain the current date at the beginning of each analysis. This date is critical for subsequent time-sensitive operations.
                        *   **Default Year Range:** If a function call requires a date range and the user has not supplied one, calculate the start and end dates for the *current year* using the date obtained from `current_date`. Use these as the default start and end dates in the relevant function calls.
                        *   Make sure you get the date and calculate the start and end date based on the current date if the prompt asks.
                        If the prompt already mentions a start and end date then use it.
                        Do not generate code to handle date, use the the get_current_date tool to do the date calculation.

                        **3. Analysis Components:**

                        Use the data_retrieval_agent to collect data for the following sections

                        *   **Comprehensive Report:** Your report should be comprehensive, detailed and contain the following sections:
                            *   **Company Profile:**  Include a detailed overview of the company, its industry, and its business model. 
                            *   **Company News:** Summarize the latest significant news impacting the company. Make it detailed. 
                            *   **Basic Financials:** Present key financial metrics and ratios for the company, covering recent periods (using current year as default period). 
                            *   **Insider Sentiment:**  Report on insider trading activity and overall sentiment expressed by company insiders. 
                            *   **SEC Filings:**  Provide an overview of the company's recent SEC filings, highlighting any significant disclosures and a summary of the findings. Make it detailed.


                        **4. Data Handling and Error Management:**

                        *   **Data Completeness:** If a function requires date that is not present or unavailable, use the current year as the default period. Report missing data but don't let it stop you.
                        *   **Function Execution:** Execute functions carefully, ensuring you have the necessary data, especially dates and symbols, before invoking any function.
                        *   **Clear Output:** Present results in a clear and concise manner, suitable for an asset management investor.

                        **5. Analytical Perspective:**

                        *   **Asset Management Lens:** Conduct all analysis with an asset manager's perspective in mind. Evaluate the company as a potential investment, focusing on risk, return, and long-term prospects.

                        **Example Workflow (Implicit):**

                        1.  Get the current date using `get_current_date`.
                        2.  Use `symbol_lookup_agent` to identify the primary symbol for the company provided by the user.
                        3.  If no symbol is found, end the process and report back.
                        4.  Calculate the start and end date by using the result of the get_current_date tool.
                        5.  Call the data_retrieval_agent retrieve the company_profile_agent, company_news_agent, company_basic_financials_agent, insider_sentiment_agent, financials_reported_agent, and sec_filings_agent, news, financials, insider sentiment, and SEC filings. Use the current year start and end date when required, or the date specified by the user.
                        6.  Assemble a detailed and insightful report that addresses each of the sections mentioned above using report_creation_agent.
                        
                        "Make sure you run all the sub agents" 
                        "Use the report_creation_agent to create a report on the investment and return it"
                        "in order to analyse a company use the data_retrieval_agent"
                        "report_creation_agent should be called right at the end of the analysis to create the final report."
                        Always call report_creation_agent at the end of the analysis.

                        """

    ),
    tools=[get_current_date],
    # sub_agents=[symbol_lookup_agent, data_retrieval_agent, report_creation_agent]
    sub_agents=[sequential_agent]
)