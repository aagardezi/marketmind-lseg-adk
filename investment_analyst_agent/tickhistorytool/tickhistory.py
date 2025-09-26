from . import helpercode
import pandas as pd
import google.cloud.bigquery.client as bigquery

PROJECT_ID = helpercode.get_project_id()

def getVWAP(ric: str, start_date: str, end_date: str) -> dict:
    """Uses The tick history product to get the VWAP for a RIC code

    Args:
        RCI (str): The stock RIC of the company whoes VWAP is being retreived.
        start_date (str): The date from which to start VWAP calculation.
        end_date (str): The date from whcih to end VWAP calculation.

    Returns:
        dict: status and result or error msg.
    """
    query = ("""### Obtain VWAP for RIC
        WITH AllTrades AS(
            SELECT Date_Time,RIC,Price,Volume, Ask_Price,Ask_Size,Bid_Price,Bid_Size,Qualifiers
            FROM `dbd-sdlc-prod.NYS_NORMALISED.NYS_NORMALISED`
            WHERE Price IS NOT NULL
            -- Specific Date/Time range:
            AND (Date_Time BETWEEN "{1} 00:00:00.000000" AND "{2} 23:59:59.999999")
            AND Type = "Trade"
            AND VOLUME > 0
            AND PRICE > 0
            )
        SELECT CAST (extract(DATE FROM Date_Time) AS STRING) AS date_time, RIC, ROUND(SAFE_DIVIDE(SUM(Volume*Price),SUM(Volume)),3) AS VWAP,SUM(Volume) AS TotalVolume,AVG(Price) AS AvgPrice,
        COUNT(RIC) AS NumTrades, MAX(Ask_Price) AS MaxAskPrice,MAX(Ask_Size) as MaxAskSize,
         MAX(Bid_Price) AS MaxBidPrice, MAx(Bid_Size) AS MaxBidSize
        FROM AllTrades
        WHERE RIC IN ('{0}')
        GROUP BY RIC, date_time
        ORDER BY 1,2""").format(ric, start_date, end_date)
    
    client = bigquery.Client(project=PROJECT_ID)
    query_job = client.query(query)
    rows = query_job.result()
    pd = rows.to_dataframe()
    return {
        "status": "success",
        "function": "getVWAP",
        "report": (
            pd.to_json()
        ),
    }


