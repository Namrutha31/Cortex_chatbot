prompt_demand = """
 ###Instruction:
 In interpreation of question, do not change any words or context, or do not assume to add anything.
   **For all peak demand queries, you should retrieve data from "FACT_POWER_BILLING_PERIODS","FACT_STEAM_BILLING_PERIODS","FACT_GAS_BILLING_PERIODS", refer below peak demand verified queries to join tables, do not mention i can not able to join tables.**
   **For all peak demand queries, strictly use all below 3 table to analyze:**
        -  FACT_POWER_BILLING_PERIODS (all columns); use 'POWERDEMANDSTATS' AS DEMANDTYPE
        -  FACT_STEAM_BILLING_PERIODS (all columns); use 'STEAMDEMANDSTATS' AS DEMANDTYPE
        -  FACT_GAS_BILLING_PERIODS (all columns); use 'GASDEMANDSTATS' AS DEMANDTYPE
    **Incase there is no time period in question, then strictly use this month as date**
    **If the user requests a specific month (X month), the query should strictly check whether any date within that month falls between STARTS_ON and ENDS_ON**
        - For example, if query requests for August and month 2024, then the date must be "WHERE DATE_TRUNC('MONTH', STARTS_ON) IN (DATE_TRUNC('MONTH', TO_DATE('2024-05', 'YYYY-MM')), DATE_TRUNC('MONTH', TO_DATE('2024-08', 'YYYY-MM'))) AND DATE_TRUNC('MONTH', ENDS_ON) IN (DATE_TRUNC('MONTH', TO_DATE('2024-05', 'YYYY-MM')), DATE_TRUNC('MONTH', TO_DATE('2024-08', 'YYYY-MM')))"**
   **Strictly use below verified queries for generating queries like, "max peak deamnd for user", "power/steam/gas demand of user/portfolio or particular building"**
   **Strictly round off all values to 0 decimal places, except for energy intensity queries.**
   **If the user query matches (or closely resembles) any of the verified queries, strictly use the verified query as a reference to formulate the response.**   
###Generate an SQL query based on the following verified queries;
verified_queries:
  - name: Peak Demand for user 
    question: When did I set my peak on date y? for user x
    sql: "WITH USER_BUILDINGS AS (
                    SELECT DISTINCT DB.ID, DB.NAME
                    FROM DIM_BUILDINGS AS DB
                    JOIN FACT_BUILDINGS AS FB ON DB.ID = FB.ID
                    JOIN DIM_BUILDING_USERS AS DBU ON DBU.BUILDING_ID = DB.ID
                    JOIN DIM_USERS AS DU ON DU.ID = DBU.USER_ID
                    WHERE FB.ACTIVE = TRUE 
                    AND DU.FIRST_NAME ILIKE 'x'
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
                WHERE DATE_TRUNC('DAY', 'y'::DATE) >= DATE_TRUNC('DAY', PBP.STARTS_ON)  
                AND DATE_TRUNC('DAY', 'y'::DATE) <= DATE_TRUNC('DAY', PBP.ENDS_ON)

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
                WHERE DATE_TRUNC('DAY', 'y'::DATE) >= DATE_TRUNC('DAY', GBP.STARTS_ON)  
                AND DATE_TRUNC('DAY', 'y'::DATE) <= DATE_TRUNC('DAY', GBP.ENDS_ON)

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
                WHERE DATE_TRUNC('DAY', 'y'::DATE) >= DATE_TRUNC('DAY', SBP.STARTS_ON)  
                AND DATE_TRUNC('DAY', 'y'::DATE) <= DATE_TRUNC('DAY', SBP.ENDS_ON);"

  - name: peak demand for user during X month
    question: What was the peak demand across power, gas and steam for buildings associated with user Scott during January 2024?
    sql: "WITH __fact_steam_billing_periods AS (
                SELECT
                    building_id,
                    starts_on,
                    ends_on,
                    measured_demand_peak_date,
                    measured_demand_peak
                FROM cortex_search.silver.fact_steam_billing_periods
                ), __fact_power_billing_periods AS (
                SELECT
                    building_id,
                    starts_on,
                    ends_on,
                    measured_demand_peak_date,
                    measured_demand_peak
                FROM cortex_search.silver.fact_power_billing_periods
                ), __fact_gas_billing_periods AS (
                SELECT
                    building_id,
                    starts_on,
                    ends_on,
                    measured_demand_peak_date,
                    measured_demand_peak
                FROM cortex_search.silver.fact_gas_billing_periods
                ), __dim_buildings AS (
                SELECT
                    id,
                    name
                FROM cortex_search.silver.dim_buildings
                ), __fact_buildings AS (
                SELECT
                    id,
                    active
                FROM cortex_search.silver.fact_buildings
                ), __dim_building_users AS (
                SELECT
                    building_id,
                    user_id
                FROM cortex_search.silver.dim_building_users
                ), __dim_users AS (
                SELECT
                    id,
                    first_name
                FROM cortex_search.silver.dim_users
                ), USER_BUILDINGS AS (
                SELECT DISTINCT
                    DB.ID,
                    DB.NAME
                FROM __dim_buildings AS DB
                JOIN __fact_buildings AS FB
                    ON DB.ID = FB.ID
                JOIN __dim_building_users AS DBU
                    ON DBU.BUILDING_ID = DB.ID
                JOIN __dim_users AS DU
                    ON DU.ID = DBU.USER_ID
                WHERE
                    FB.ACTIVE = TRUE AND DU.FIRST_NAME ILIKE 'scott'
                )
                SELECT
                UB.ID,
                UB.NAME,
                ROUND(PBP.MEASURED_DEMAND_PEAK) AS MEASURED_DEMAND_PEAK,
                PBP.MEASURED_DEMAND_PEAK_DATE,
                'POWERDEMANDSTATS' AS DEMANDTYPE,
                PBP.STARTS_ON,
                PBP.ENDS_ON
                FROM __fact_power_billing_periods AS PBP
                JOIN USER_BUILDINGS AS UB
                ON PBP.BUILDING_ID = UB.ID
                WHERE
                DATE_TRUNC('MONTH', PBP.STARTS_ON) = DATE_TRUNC('MONTH', TO_DATE('2024-01', 'yyyy-mm'))
                AND DATE_TRUNC('MONTH', PBP.ENDS_ON) = DATE_TRUNC('MONTH', TO_DATE('2024-01', 'yyyy-mm'))
                UNION ALL
                SELECT
                UB.ID,
                UB.NAME,
                ROUND(GBP.MEASURED_DEMAND_PEAK) AS MEASURED_DEMAND_PEAK,
                GBP.MEASURED_DEMAND_PEAK_DATE,
                'GASDEMANDSTATS' AS DEMANDTYPE,
                GBP.STARTS_ON,
                GBP.ENDS_ON
                FROM __fact_gas_billing_periods AS GBP
                JOIN USER_BUILDINGS AS UB
                ON GBP.BUILDING_ID = UB.ID
                WHERE
                DATE_TRUNC('MONTH', GBP.STARTS_ON) = DATE_TRUNC('MONTH', TO_DATE('2024-01', 'yyyy-mm'))
                AND DATE_TRUNC('MONTH', GBP.ENDS_ON) = DATE_TRUNC('MONTH', TO_DATE('2024-01', 'yyyy-mm'))
                UNION ALL
                SELECT
                UB.ID,
                UB.NAME,
                ROUND(SBP.MEASURED_DEMAND_PEAK) AS MEASURED_DEMAND_PEAK,
                SBP.MEASURED_DEMAND_PEAK_DATE,
                'STEAMDEMANDSTATS' AS DEMANDTYPE,
                SBP.STARTS_ON,
                SBP.ENDS_ON
                FROM __fact_steam_billing_periods AS SBP
                JOIN USER_BUILDINGS AS UB
                ON SBP.BUILDING_ID = UB.ID
                WHERE
                DATE_TRUNC('MONTH', SBP.STARTS_ON) = DATE_TRUNC('MONTH', TO_DATE('2024-01', 'yyyy-mm'))
                AND DATE_TRUNC('MONTH', SBP.ENDS_ON) = DATE_TRUNC('MONTH', TO_DATE('2024-01', 'yyyy-mm'))
                -- Generated by Cortex Analyst
                ;" 

  - name: peak demand for user scott for last week
    question: What was the peak demand for user scott for last week
    sql: "WITH __fact_steam_billing_periods AS (
                    SELECT
                        building_id,
                        starts_on,
                        ends_on,
                        measured_demand_peak_date,
                        measured_demand_peak
                    FROM cortex_search.silver.fact_steam_billing_periods
                ), __fact_power_billing_periods AS (
                    SELECT
                        building_id,
                        starts_on,
                        ends_on,
                        measured_demand_peak_date,
                        measured_demand_peak
                    FROM cortex_search.silver.fact_power_billing_periods
                ), __fact_gas_billing_periods AS (
                    SELECT
                        building_id,
                        starts_on,
                        ends_on,
                        measured_demand_peak_date,
                        measured_demand_peak
                    FROM cortex_search.silver.fact_gas_billing_periods
                ), __dim_buildings AS (
                    SELECT
                        id,
                        name
                    FROM cortex_search.silver.dim_buildings
                ), __fact_buildings AS (
                    SELECT
                        id
                    FROM cortex_search.silver.fact_buildings
                ), __dim_building_users AS (
                    SELECT
                        building_id,
                        user_id
                    FROM cortex_search.silver.dim_building_users
                ), __dim_users AS (
                    SELECT
                        id,
                        first_name
                    FROM cortex_search.silver.dim_users
                ), USER_BUILDINGS AS (
                    SELECT DISTINCT
                        DB.ID,
                        DB.NAME
                    FROM __dim_buildings AS DB
                    JOIN __fact_buildings AS FB
                        ON DB.ID = FB.ID
                    JOIN __dim_building_users AS DBU
                        ON DBU.BUILDING_ID = DB.ID
                    JOIN __dim_users AS DU
                        ON DU.ID = DBU.USER_ID
                    WHERE FB.ACTIVE = TRUE 
                    AND DU.FIRST_NAME ILIKE 'scott'
                )

                -- Get data for last month
                SELECT
                    UB.ID,
                    UB.NAME,
                    ROUND(PBP.MEASURED_DEMAND_PEAK) AS MEASURED_DEMAND_PEAK,
                    PBP.MEASURED_DEMAND_PEAK_DATE,
                    'POWERDEMANDSTATS' AS DEMANDTYPE,
                    PBP.STARTS_ON,
                    PBP.ENDS_ON
                FROM __fact_power_billing_periods AS PBP
                JOIN USER_BUILDINGS AS UB ON PBP.BUILDING_ID = UB.ID
                WHERE
                    PBP.STARTS_ON >= DATE_TRUNC('WEEK', CURRENT_DATE - INTERVAL '1 WEEK')
                    AND PBP.ENDS_ON <= DATE_TRUNC('WEEK', CURRENT_DATE) - INTERVAL '1 DAY'

                UNION ALL

                SELECT
                    UB.ID,
                    UB.NAME,
                    ROUND(GBP.MEASURED_DEMAND_PEAK) AS MEASURED_DEMAND_PEAK,
                    GBP.MEASURED_DEMAND_PEAK_DATE,
                    'GASDEMANDSTATS' AS DEMANDTYPE,
                    GBP.STARTS_ON,
                    GBP.ENDS_ON
                FROM __fact_gas_billing_periods AS GBP
                JOIN USER_BUILDINGS AS UB ON GBP.BUILDING_ID = UB.ID
                WHERE
                    GBP.STARTS_ON >= DATE_TRUNC('WEEK', CURRENT_DATE - INTERVAL '1 WEEK')
                    AND GBP.ENDS_ON <= DATE_TRUNC('WEEK', CURRENT_DATE) - INTERVAL '1 DAY'

                UNION ALL

                SELECT
                    UB.ID,
                    UB.NAME,
                    ROUND(SBP.MEASURED_DEMAND_PEAK) AS MEASURED_DEMAND_PEAK,
                    SBP.MEASURED_DEMAND_PEAK_DATE,
                    'STEAMDEMANDSTATS' AS DEMANDTYPE,
                    SBP.STARTS_ON,
                    SBP.ENDS_ON
                FROM __fact_steam_billing_periods AS SBP
                JOIN USER_BUILDINGS AS UB ON SBP.BUILDING_ID = UB.ID
                WHERE
                    SBP.STARTS_ON >= DATE_TRUNC('WEEK', CURRENT_DATE - INTERVAL '1 WEEK')
                    AND SBP.ENDS_ON <= DATE_TRUNC('WEEK', CURRENT_DATE) - INTERVAL '1 DAY'
                ;"

  - name: peak demand for user scott for last month 
    question: What was the peak demand across power, gas and steam for buildings associated with user Scott during last month?
    sql: "WITH __fact_steam_billing_periods AS (
            SELECT
                building_id,
                starts_on,
                ends_on,
                measured_demand_peak_date,
                measured_demand_peak
            FROM cortex_search.silver.fact_steam_billing_periods
        ), __fact_power_billing_periods AS (
            SELECT
                building_id,
                starts_on,
                ends_on,
                measured_demand_peak_date,
                measured_demand_peak
            FROM cortex_search.silver.fact_power_billing_periods
        ), __fact_gas_billing_periods AS (
            SELECT
                building_id,
                starts_on,
                ends_on,
                measured_demand_peak_date,
                measured_demand_peak
            FROM cortex_search.silver.fact_gas_billing_periods
        ), __dim_buildings AS (
            SELECT
                id,
                name
            FROM cortex_search.silver.dim_buildings
        ), __fact_buildings AS (
            SELECT
                id
            FROM cortex_search.silver.fact_buildings
        ), __dim_building_users AS (
            SELECT
                building_id,
                user_id
            FROM cortex_search.silver.dim_building_users
        ), __dim_users AS (
            SELECT
                id,
                first_name
            FROM cortex_search.silver.dim_users
        ), USER_BUILDINGS AS (
            SELECT DISTINCT
                DB.ID,
                DB.NAME
            FROM __dim_buildings AS DB
            JOIN __fact_buildings AS FB
                ON DB.ID = FB.ID
            JOIN __dim_building_users AS DBU
                ON DBU.BUILDING_ID = DB.ID
            JOIN __dim_users AS DU
                ON DU.ID = DBU.USER_ID
            WHERE FB.ACTIVE = TRUE 
            AND DU.FIRST_NAME ILIKE 'scott'
        )

        SELECT
            UB.ID,
            UB.NAME,
            ROUND(PBP.MEASURED_DEMAND_PEAK) AS MEASURED_DEMAND_PEAK,
            PBP.MEASURED_DEMAND_PEAK_DATE,
            'POWERDEMANDSTATS' AS DEMANDTYPE,
            PBP.STARTS_ON,
            PBP.ENDS_ON
        FROM __fact_power_billing_periods AS PBP
        JOIN USER_BUILDINGS AS UB ON PBP.BUILDING_ID = UB.ID
        WHERE
            PBP.STARTS_ON >= DATE_TRUNC('MONTH', CURRENT_DATE - INTERVAL '1 MONTH')
            AND PBP.ENDS_ON <= DATE_TRUNC('MONTH', CURRENT_DATE) - INTERVAL '1 DAY'

        UNION ALL

        SELECT
            UB.ID,
            UB.NAME,
            ROUND(GBP.MEASURED_DEMAND_PEAK) AS MEASURED_DEMAND_PEAK,
            GBP.MEASURED_DEMAND_PEAK_DATE,
            'GASDEMANDSTATS' AS DEMANDTYPE,
            GBP.STARTS_ON,
            GBP.ENDS_ON
        FROM __fact_gas_billing_periods AS GBP
        JOIN USER_BUILDINGS AS UB ON GBP.BUILDING_ID = UB.ID
        WHERE
            GBP.STARTS_ON >= DATE_TRUNC('MONTH', CURRENT_DATE - INTERVAL '1 MONTH')
            AND GBP.ENDS_ON <= DATE_TRUNC('MONTH', CURRENT_DATE) - INTERVAL '1 DAY'

        UNION ALL

        SELECT
            UB.ID,
            UB.NAME,
            ROUND(SBP.MEASURED_DEMAND_PEAK) AS MEASURED_DEMAND_PEAK,
            SBP.MEASURED_DEMAND_PEAK_DATE,
            'STEAMDEMANDSTATS' AS DEMANDTYPE,
            SBP.STARTS_ON,
            SBP.ENDS_ON
        FROM __fact_steam_billing_periods AS SBP
        JOIN USER_BUILDINGS AS UB ON SBP.BUILDING_ID = UB.ID
        WHERE
            SBP.STARTS_ON >= DATE_TRUNC('MONTH', CURRENT_DATE - INTERVAL '1 MONTH')
            AND SBP.ENDS_ON <= DATE_TRUNC('MONTH', CURRENT_DATE) - INTERVAL '1 DAY'
        ;"                 
            

  - name: peak demand for user scott for this month 
    question: What was the peak demand across power, gas and steam for buildings associated with user bryan during this month?
    sql: "WITH __fact_steam_billing_periods AS (
            SELECT
                building_id,
                starts_on,
                ends_on,
                measured_demand_peak_date,
                measured_demand_peak
            FROM cortex_search.silver.fact_steam_billing_periods
        ), __fact_power_billing_periods AS (
            SELECT
                building_id,
                starts_on,
                ends_on,
                measured_demand_peak_date,
                measured_demand_peak
            FROM cortex_search.silver.fact_power_billing_periods
        ), __fact_gas_billing_periods AS (
            SELECT
                building_id,
                starts_on,
                ends_on,
                measured_demand_peak_date,
                measured_demand_peak
            FROM cortex_search.silver.fact_gas_billing_periods
        ), __dim_buildings AS (
            SELECT
                id,
                name
            FROM cortex_search.silver.dim_buildings
        ), __fact_buildings AS (
            SELECT
                id
            FROM cortex_search.silver.fact_buildings
        ), __dim_building_users AS (
            SELECT
                building_id,
                user_id
            FROM cortex_search.silver.dim_building_users
        ), __dim_users AS (
            SELECT
                id,
                first_name
            FROM cortex_search.silver.dim_users
        ), USER_BUILDINGS AS (
            SELECT DISTINCT
                DB.ID,
                DB.NAME
            FROM __dim_buildings AS DB
            JOIN __fact_buildings AS FB
                ON DB.ID = FB.ID
            JOIN __dim_building_users AS DBU
                ON DBU.BUILDING_ID = DB.ID
            JOIN __dim_users AS DU
                ON DU.ID = DBU.USER_ID
           WHERE FB.ACTIVE = TRUE 
           AND  DU.FIRST_NAME ILIKE 'BRYAN'
        )

        -- Get data for last month
        SELECT
            UB.ID,
            UB.NAME,
            ROUND(PBP.MEASURED_DEMAND_PEAK) AS MEASURED_DEMAND_PEAK,
            PBP.MEASURED_DEMAND_PEAK_DATE,
            'POWERDEMANDSTATS' AS DEMANDTYPE,
            PBP.STARTS_ON,
            PBP.ENDS_ON
        FROM __fact_power_billing_periods AS PBP
        JOIN USER_BUILDINGS AS UB ON PBP.BUILDING_ID = UB.ID
        WHERE
            PBP.STARTS_ON >= DATE_TRUNC('MONTH', CURRENT_DATE)
            AND PBP.ENDS_ON <= DATE_TRUNC('MONTH', CURRENT_DATE) + INTERVAL '1 MONTH' - INTERVAL '1 DAY'

        UNION ALL

        SELECT
            UB.ID,
            UB.NAME,
            ROUND(GBP.MEASURED_DEMAND_PEAK) AS MEASURED_DEMAND_PEAK,
            GBP.MEASURED_DEMAND_PEAK_DATE,
            'GASDEMANDSTATS' AS DEMANDTYPE,
            GBP.STARTS_ON,
            GBP.ENDS_ON
        FROM __fact_gas_billing_periods AS GBP
        JOIN USER_BUILDINGS AS UB ON GBP.BUILDING_ID = UB.ID
        WHERE
            GBP.STARTS_ON >= DATE_TRUNC('MONTH', CURRENT_DATE)
            AND GBP.ENDS_ON <= DATE_TRUNC('MONTH', CURRENT_DATE) + INTERVAL '1 MONTH' - INTERVAL '1 DAY'

        UNION ALL

        SELECT
            UB.ID,
            UB.NAME,
            ROUND(SBP.MEASURED_DEMAND_PEAK) AS MEASURED_DEMAND_PEAK,
            SBP.MEASURED_DEMAND_PEAK_DATE,
            'STEAMDEMANDSTATS' AS DEMANDTYPE,
            SBP.STARTS_ON,
            SBP.ENDS_ON
        FROM __fact_steam_billing_periods AS SBP
        JOIN USER_BUILDINGS AS UB ON SBP.BUILDING_ID = UB.ID
        WHERE
            SBP.STARTS_ON >= DATE_TRUNC('MONTH', CURRENT_DATE)
            AND SBP.ENDS_ON <= DATE_TRUNC('MONTH', CURRENT_DATE) + INTERVAL '1 MONTH' - INTERVAL '1 DAY'
        ;"                 

  - name: peak demand for user scott for this month ###All buildings in specific portfolio
    question: What was the peak demand across power, gas and steam for all buildings associated with stahl portfolio,for user bryan during this month?
    sql: "SELECT 
            DB.ID,
            DB.NAME,
            MEASURED_DEMAND_PEAK, 
            MEASURED_DEMAND_PEAK_DATE, 
            'POWERDEMANDSTATS' AS DEMANDTYPE,
            starts_on,
            ends_on
            FROM
                FACT_POWER_BILLING_PERIODS AS PBP
            JOIN 
                FACT_BUILDINGS AS FB ON PBP.BUILDING_ID = FB.ID
            JOIN 
                DIM_BUILDINGS AS DB ON DB.ID = FB.ID
            JOIN 
                DIM_PORTFOLIO_BUILDINGS AS PB ON PB.BUILDING_ID = FB.ID
            JOIN 
                DIM_PORTFOLIOS AS DP ON DP.ID = PB.PORTFOLIO_ID
            JOIN 
                DIM_PORTFOLIO_USERS AS PU ON PU.PORTFOLIO_ID = DP.ID
            JOIN 
                DIM_USERS AS DU ON DU.ID = PU.USER_ID
            WHERE
            PBP.STARTS_ON >= DATE_TRUNC('MONTH', CURRENT_DATE)
            AND PBP.ENDS_ON <= DATE_TRUNC('MONTH', CURRENT_DATE) + INTERVAL '1 MONTH' - INTERVAL '1 DAY' and fb.active = true  AND DU.FIRST_NAME ILIKE 'bryan'
                AND DP.NAME ILIKE 'stahl' 
            UNION
            SELECT 
            DB.ID,
            DB.NAME,
            MEASURED_DEMAND_PEAK, 
            MEASURED_DEMAND_PEAK_DATE, 
            'GASDEMANDSTATS' AS DEMANDTYPE,
            starts_on,
            ends_on
            FROM
                FACT_GAS_BILLING_PERIODS AS GBP
            JOIN 
                FACT_BUILDINGS AS FB ON GBP.BUILDING_ID = FB.ID
            JOIN 
                DIM_BUILDINGS AS DB ON DB.ID = FB.ID
            JOIN 
                DIM_PORTFOLIO_BUILDINGS AS PB ON PB.BUILDING_ID = FB.ID
            JOIN 
                DIM_PORTFOLIOS AS DP ON DP.ID = PB.PORTFOLIO_ID
            JOIN 
                DIM_PORTFOLIO_USERS AS PU ON PU.PORTFOLIO_ID = DP.ID
            JOIN 
                DIM_USERS AS DU ON DU.ID = PU.USER_ID
            WHERE
            GBP.STARTS_ON >= DATE_TRUNC('MONTH', CURRENT_DATE)
            AND GBP.ENDS_ON <= DATE_TRUNC('MONTH', CURRENT_DATE) + INTERVAL '1 MONTH' - INTERVAL '1 DAY' and fb.active = true  AND DU.FIRST_NAME ILIKE 'bryan'
                AND DP.NAME ILIKE 'stahl' 
            UNION
            SELECT
            DB.ID,
            DB.NAME,
            MEASURED_DEMAND_PEAK, 
            MEASURED_DEMAND_PEAK_DATE, 
            'STEAMDEMANDSTATS' AS DEMANDTYPE,
            starts_on,
            ends_on
            FROM
                FACT_STEAM_BILLING_PERIODS AS SBP
            JOIN 
                FACT_BUILDINGS AS FB ON SBP.BUILDING_ID = FB.ID
            JOIN 
                DIM_BUILDINGS AS DB ON DB.ID = FB.ID
            JOIN 
                DIM_PORTFOLIO_BUILDINGS AS PB ON PB.BUILDING_ID = FB.ID
            JOIN 
                DIM_PORTFOLIOS AS DP ON DP.ID = PB.PORTFOLIO_ID
            JOIN 
                DIM_PORTFOLIO_USERS AS PU ON PU.PORTFOLIO_ID = DP.ID
            JOIN 
                DIM_USERS AS DU ON DU.ID = PU.USER_ID
            WHERE
            SBP.STARTS_ON >= DATE_TRUNC('MONTH', CURRENT_DATE)
            AND SBP.ENDS_ON <= DATE_TRUNC('MONTH', CURRENT_DATE) + INTERVAL '1 MONTH' - INTERVAL '1 DAY' and fb.active = true  AND DU.FIRST_NAME ILIKE 'bryan'
                AND DP.NAME ILIKE 'stahl';"                    
            """
