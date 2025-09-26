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