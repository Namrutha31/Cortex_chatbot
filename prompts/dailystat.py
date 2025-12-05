prompt_dailystat = """
 ###Instruction:
 In interpreation of question, do not change any words or context, or do not assume to add anything.
   **Do not alter the meaning or context in your interpretation of question, if the user question is related to (best/worst,poor/best performance, ineffective, inefficiency) do not interpret only negative values, include all values along with all savings columns, do not reside on 1 or 2 columns; keep it exactly as it is.**
   **For all peak demand queries, you should retrieve data from "FACT_POWER_BILLING_PERIODS","FACT_STEAM_BILLING_PERIODS","FACT_GAS_BILLING_PERIODS", refer below peak demand verified queries to join tables, do not mention i can not able to join tables.**
   **For all peak demand queries, strictly use all below 3 table to analyze:**
        -  FACT_POWER_BILLING_PERIODS (all columns); use 'POWERDEMANDSTATS' AS DEMANDTYPE
        -  FACT_STEAM_BILLING_PERIODS (all columns); use 'STEAMDEMANDSTATS' AS DEMANDTYPE
        -  FACT_GAS_BILLING_PERIODS (all columns); use 'GASDEMANDSTATS' AS DEMANDTYPE
   **for all peak demand queries, Incase there is no time period in question, then strictly use last month as date**        
   **If the user query matches (or closely resembles) any of the verified queries, strictly use the verified query as a reference to formulate the response.**
   **Conditions to Trigger Analysis**:
        If the input contains phrases such as:
        - 'compare yesterday's daily stats'
        - 'doing well'
        - 'performing'
        - 'performing the best'
        - 'compared to other buildings' 
    **Time Zone**:
        - Strictly add time_zone column, for all queries related to table fact_building_daily_stats           
    **Data to Analyze**:
        1. From the `fact_daily_building_stats` table, retrieve and analyze **all columns**.
        2. From the `fact_buildings` table, retrieve and analyze **columns starting with 'USES_'** (e.g., USES_ELECTRICITY, USES_GAS, USES_WATER).
        3. From the `fact_weather_forecasts` table, analyze the `temperature` and `icon` columns.
    **Instructions for Analysis**:
        - Consider any input, even if unrelated to the phrases above, that involves querying or comparing data from these tables.
        - Focus on retrieving and analyzing the relevant data points based on the tables and columns described.
        - Provide detailed insights and highlight meaningful comparisons for any specified or implied buildings, locations, or scenarios.
    **Response Requirements**:
        - Explain your findings clearly, ensuring all comparisons are supported by data.
        - Avoid adding information that is not present in the data. Stay factual and data-driven.    
        - **Strictly round off all values to 0 decimal places, except for energy intensity queries.**
###Generate an SQL query based on the following verified queries;
verified_queries:
  - name: Building stats of y for user z 
    question: compare yesterday building daily stat of x and y for user z
    sql: "SELECT distinct
            bs.id,
            bs.building_id,
            bs.date,
            bs.dow,
            bs.year_quarter,
            bs.excluded_from_calculations,
            bs.operating,
            bs.holiday,
            bs.operation_start_time, 
            bs.operation_turn_off_time,
            bs.recommended_operation_start_time,
            bs.quarter,
            bs.day_of_week,
            bs.start_time_difference_in_minutes,
            bs.time_in_bounds,
            bs.rt,
            bs.startup_minutes_from_lease_start,
            bs.excess_run_time,bs.alerts,bs.time_zone
            FROM fact_building_daily_stats AS bs
            JOIN dim_buildings AS db ON bs.building_id = db.id
            JOIN fact_buildings AS fb ON db.id = fb.id 
            JOIN dim_building_users AS bu ON bu.building_id = db.id
            JOIN dim_users AS du ON du.id = bu.user_id
            where du.first_name ilike 'z' AND bs.date = (current_date -4)   AND db.name ilike 'y' and operation_start_time is not null;"

  - name: last week Building stats of building y for user z 
    question: last week Building stats of building y for user z 
    sql: "SELECT distinct
            bs.id,
            bs.building_id,
            bs.date,
            bs.dow,
            bs.year_quarter,
            bs.excluded_from_calculations,
            bs.operating,
            bs.holiday,
            bs.operation_start_time, 
            bs.operation_turn_off_time,
            bs.recommended_operation_start_time,
            bs.quarter,
            bs.day_of_week,
            bs.start_time_difference_in_minutes,
            bs.time_in_bounds,
            bs.rt,
            bs.startup_minutes_from_lease_start,
            bs.excess_run_time,bs.alerts,bs.time_zone
            
        FROM
            fact_building_daily_stats AS bs
        JOIN
            dim_buildings AS db ON bs.building_id = db.id
        JOIN
            fact_buildings AS fb ON db.id = fb.id
        JOIN
            dim_building_users AS bu ON bu.building_id = db.id
        JOIN
            dim_users AS du ON du.id = bu.user_id 
        WHERE   bs.date >= DATE_TRUNC('WEEK', CURRENT_DATE - INTERVAL '1 WEEK')
        AND bs.date < DATE_TRUNC('WEEK', CURRENT_DATE)  and du.first_name  ilike 'z' and db.name ilike 'y' and operation_start_time is not null;"            


  - name: Building stats on specific consumption; (About dataset:measurement_types(SteamMeasurement,GasMeasurement,ChilledWaterDemandMeasurement,PowerMeasurement[electric]))
    question: What was the electricity consumption for building 'X' on date Y?
    sql: "SELECT 
            db.name,
            ROUND(bdc.consumption_total_actual) AS consumption_total_actual,
            bdc.measurement_type
        FROM fact_building_daily_consuption AS bdc
        JOIN fact_buildings AS fb ON fb.id = bdc.building_id
        JOIN dim_buildings AS db ON db.id = bdc.building_id
        WHERE 
            bdc.measurement_type = 'PowerMeasurement' 
            AND db.name ilike 'X' 
            AND bdc.date ilike 'Y';"  

  - name: Building stats on consumption; (About dataset:measurement_types(SteamMeasurement,GasMeasurement,ChilledWaterDemandMeasurement,PowerMeasurement[electric]))
    question: What was the consumption for building 'X' on date Y?
    sql: "SELECT 
            db.name,
            ROUND(bdc.consumption_total_actual) AS consumption_total_actual,
            bdc.measurement_type
        FROM fact_building_daily_consuption AS bdc
        JOIN fact_buildings AS fb ON fb.id = bdc.building_id
        JOIN dim_buildings AS db ON db.id = bdc.building_id
        WHERE 
            bdc.measurement_type = 'PowerMeasurement' 
            AND db.name ilike 'X' 
            AND bdc.date ilike 'Y';" 

          
  - name: Peak Demand for user 
    question: When did I set my peak on date y? for user x
    sql: "WITH USER_BUILDINGS AS (
                SELECT DISTINCT DB.ID, DB.NAME
                FROM DIM_BUILDINGS AS DB
                JOIN FACT_BUILDINGS AS FB ON DB.ID = FB.ID
                JOIN DIM_BUILDING_USERS AS DBU ON DBU.BUILDING_ID = DB.ID
                JOIN DIM_USERS AS DU ON DU.ID = DBU.USER_ID
                WHERE DU.FIRST_NAME ILIKE 'x'
            )
            SELECT 
                UB.ID,
                UB.NAME,
                ROUND(PBP.MEASURED_DEMAND_PEAK) AS MEASURED_DEMAND_PEAK, 
                PBP.MEASURED_DEMAND_PEAK_DATE, 
                'POWERDEMANDSTATS' AS DEMANDTYPE,
                PBP.STARTS_ON,
                PBP.ENDS_ON
            FROM FACT_POWER_BILLING_PERIODS AS PBP
            JOIN USER_BUILDINGS AS UB ON PBP.BUILDING_ID = UB.ID
            WHERE 'y' BETWEEN PBP.STARTS_ON AND PBP.ENDS_ON

            UNION ALL

            SELECT 
                UB.ID,
                UB.NAME,
                ROUND(GBP.MEASURED_DEMAND_PEAK) AS MEASURED_DEMAND_PEAK, 
                GBP.MEASURED_DEMAND_PEAK_DATE, 
                'GASDEMANDSTATS' AS DEMANDTYPE,
                GBP.STARTS_ON,
                GBP.ENDS_ON
            FROM FACT_GAS_BILLING_PERIODS AS GBP
            JOIN USER_BUILDINGS AS UB ON GBP.BUILDING_ID = UB.ID
            WHERE 'y' BETWEEN GBP.STARTS_ON AND GBP.ENDS_ON

            UNION ALL

            SELECT 
                UB.ID,
                UB.NAME,
                ROUND(SBP.MEASURED_DEMAND_PEAK) AS MEASURED_DEMAND_PEAK, 
                SBP.MEASURED_DEMAND_PEAK_DATE, 
                'STEAMDEMANDSTATS' AS DEMANDTYPE,
                SBP.STARTS_ON,
                SBP.ENDS_ON
            FROM FACT_STEAM_BILLING_PERIODS AS SBP
            JOIN USER_BUILDINGS AS UB ON SBP.BUILDING_ID = UB.ID
            WHERE 'y' BETWEEN SBP.STARTS_ON AND SBP.ENDS_ON;"

  - name: Maximum or highest peak demand for user 
    question: When did I set my highest peak on date y? for user x
    sql: "WITH USER_BUILDINGS AS (
                SELECT DISTINCT DB.ID, DB.NAME
                FROM DIM_BUILDINGS AS DB
                JOIN FACT_BUILDINGS AS FB ON DB.ID = FB.ID
                JOIN DIM_BUILDING_USERS AS DBU ON DBU.BUILDING_ID = DB.ID
                JOIN DIM_USERS AS DU ON DU.ID = DBU.USER_ID
                WHERE DU.FIRST_NAME ILIKE 'x'
            )
            SELECT 
                UB.ID,
                UB.NAME,
                ROUND(PBP.MEASURED_DEMAND_PEAK) AS MEASURED_DEMAND_PEAK, 
                PBP.MEASURED_DEMAND_PEAK_DATE, 
                'POWERDEMANDSTATS' AS DEMANDTYPE,
                PBP.STARTS_ON,
                PBP.ENDS_ON
            FROM FACT_POWER_BILLING_PERIODS AS PBP
            JOIN USER_BUILDINGS AS UB ON PBP.BUILDING_ID = UB.ID
            WHERE 'y' BETWEEN PBP.STARTS_ON AND PBP.ENDS_ON

            UNION ALL

            SELECT 
                UB.ID,
                UB.NAME,
                ROUND(GBP.MEASURED_DEMAND_PEAK) AS MEASURED_DEMAND_PEAK, 
                GBP.MEASURED_DEMAND_PEAK_DATE, 
                'GASDEMANDSTATS' AS DEMANDTYPE,
                GBP.STARTS_ON,
                GBP.ENDS_ON
            FROM FACT_GAS_BILLING_PERIODS AS GBP
            JOIN USER_BUILDINGS AS UB ON GBP.BUILDING_ID = UB.ID
            WHERE 'y' BETWEEN GBP.STARTS_ON AND GBP.ENDS_ON

            UNION ALL

            SELECT 
                UB.ID,
                UB.NAME,
                ROUND(SBP.MEASURED_DEMAND_PEAK) AS MEASURED_DEMAND_PEAK, 
                SBP.MEASURED_DEMAND_PEAK_DATE, 
                'STEAMDEMANDSTATS' AS DEMANDTYPE,
                SBP.STARTS_ON,
                SBP.ENDS_ON
            FROM FACT_STEAM_BILLING_PERIODS AS SBP
            JOIN USER_BUILDINGS AS UB ON SBP.BUILDING_ID = UB.ID
            WHERE 'y' BETWEEN SBP.STARTS_ON AND SBP.ENDS_ON;" 

  - name: Energy Usage of buildings; (About dataset:measurement_types(SteamMeasurement,GasMeasurement,ChilledWaterDemandMeasurement,PowerMeasurement[electric]))
    question:Which day last month did I use the most energy for building y? or provide me when i used most energy in last month for building y 
    sql: " WITH RankedConsumption AS (
              SELECT
                  measurement_type,
                  building_id,
                  ROUND(consumption_total_actual) AS consumption_total_actual,
                  date,
                  db.name,
                  ROW_NUMBER() OVER (
                      PARTITION BY measurement_type
                      ORDER BY consumption_total_actual DESC
                  ) AS rn
              FROM fact_building_daily_consuption 
              JOIN fact_buildings AS fb ON building_id = fb.id
              JOIN dim_buildings AS db ON building_id = db.id
              WHERE 
                  date BETWEEN '2025-02-01' AND '2025-02-28' 
                  AND db.name ILIKE 'y'
          )
          SELECT
              name,
              measurement_type,
              building_id,
              consumption_total_actual AS max_consumption,
              date
          FROM RankedConsumption
          WHERE rn = 1
          ORDER BY measurement_type;
          "      
"""