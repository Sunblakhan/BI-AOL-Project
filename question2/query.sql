SELECT
    DQI.CATEGORY,
    T."hour",
    T."weekday",
    COUNT(F.QUERYID) AS Total_Searches,
    SUM(CASE WHEN F.CLICK = TRUE THEN 1 ELSE 0 END) AS Total_Clicks,
    -- Calculate CTR: (Total Clicks / Total Searches) * 100
    CAST(SUM(CASE WHEN F.CLICK = TRUE THEN 1 ELSE 0 END) AS DECIMAL(18,4)) * 100 / COUNT(F.QUERYID) AS CTR_Percentage
FROM
    AOL_SCHEMA.FACTS F
JOIN
    AOL_SCHEMA.TIMEDIM T ON F.TIMEID = T.ID
-- FAST JOIN: Join FACTS to the pre-calculated list of digital queries
JOIN
    AOL_SCHEMA.DIGITAL_QUERY_IDS DQI ON F.QUERYID = DQI.QUERYID 
WHERE
    -- Use time filter only if necessary, otherwise the DQI table restricts the scope
    T."year" = '2006' 
GROUP BY GROUPING SETS (
    (DQI.CATEGORY),            -- 1. Aggregation by Category only (Highest CTR)
    (DQI.CATEGORY, T."hour"),  -- 2. Aggregation by Category and Hour (Peak Search Time)
    (DQI.CATEGORY, T."weekday") -- 3. Aggregation by Category and Weekday (Peak Search Day)
)
ORDER BY 
    DQI.CATEGORY, 
    T."hour", 
    T."weekday";