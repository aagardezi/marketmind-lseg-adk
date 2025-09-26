### Obtain VWAP for RIC
        WITH AllTrades AS(
            SELECT Date_Time,RIC,Price,Volume, Ask_Price,Ask_Size,Bid_Price,Bid_Size,Qualifiers
            FROM `dbd-sdlc-prod.NYS_NORMALISED.NYS_NORMALISED`
            WHERE Price IS NOT NULL
            -- Specific Date/Time range:
            AND (Date_Time BETWEEN "2025-09-18 00:00:00.000000" AND "2025-09-19 23:59:59.999999")
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
        WHERE RIC IN ('KO.N','GOOG.OQ')
        GROUP BY RIC, date_time
        ORDER BY 1,2




SELECT * FROM `dbd-sdlc-prod.NYS_NORMALISED.NYS_NORMALISED` 
where RIC='KO.N' and Date_Time>='2025-09-19 11:00:00' and Date_Time<='2025-09-20 12:00:00'
LIMIT 1000
