prompt_improvements = """
 ###Instruction:
 In interpreation of question, do not change any words or context, or do not assume to add anything.
   **If the user query matches (or closely resembles) any of the verified queries, strictly use the verified query as a reference to formulate the response.**
   **Conditions to Trigger Analysis**:
        If the input contains phrases such as:
        - 'where to improve'
        - 'give suggestion to reduce consumption'
        - 'where are we operating better'
    **Time to mention:**
        If user did not mention any time period,
        - strictly use "date BETWEEN (CURRENT_DATE - 15) AND CURRENT_DATE
    **Data to Analyze**:
        1. From the `fact_daily_building_stats` table, retrieve and analyze **the columns mentioned in verified query**.
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
  - name: Building improvemts for user z ###Specific Building
    question: Where should I focus on for improvements? or where could we operating better? in x Building for z user.
    sql: "SELECT
            db.id AS building_id,
            db.name AS building_name,
            CAST(MAX(bs.operation_start_time) AS DATE) AS end_date,
            CAST(MIN(bs.operation_start_time) AS DATE) AS start_date,
            CAST(MAX(bs.OPERATION_START_TIME) AS TIME) AS OPERATION_START_TIME,
            CAST(MAX(bs.OPERATION_TURN_OFF_TIME) AS TIME) AS OPERATION_TURN_OFF_TIME,
            CAST(MAX(bs.RECOMMENDED_OPERATION_START_TIME ) AS TIME) AS RECOMMENDED_OPERATION_START_TIME,
            CAST(MAX(bs.LEASE_OBLIGATIONS_START_AT ) AS TIME) AS LEASE_OBLIGATIONS_START_AT,
            CAST(MAX(bs.LEASE_OBLIGATIONS_END_AT) AS TIME) AS LEASE_OBLIGATIONS_END_AT,
            CAST(MAx(bs.STOPPED_SATISFYING_LEASE_OBLIGATIONS_AT ) AS TIME) AS STOPPED_SATISFYING_LEASE_OBLIGATIONS_AT,
            CAST(MAX(bs.SATISFIED_LEASE_OBLIGATIONS_AT) AS TIME) AS SATISFIED_LEASE_OBLIGATIONS_AT,
            ROUND(AVG(bs.start_time_difference_in_minutes)) AS start_time_difference_in_minutes,
            ROUND(AVG(bs.time_in_bounds)) AS time_in_bounds,
            ROUND(AVG(bs.rt)) AS avg_rt,
            ROUND(AVG(bs.startup_minutes_from_lease_start)) AS startup_minutes_from_lease_start,
            ROUND(AVG(bs.excess_run_time)) AS excess_run_time,
            LISTAGG(alerts, ',') WITHIN GROUP (ORDER BY alerts) AS alerts,bs.time_zone
            FROM
            fact_building_daily_stats AS bs
            JOIN
            dim_buildings AS db ON bs.building_id = db.id
            JOIN
            dim_building_users AS bu ON bu.building_id = db.id
            JOIN
            dim_users AS du ON du.id = bu.user_id
            WHERE
            bs.date BETWEEN (CURRENT_DATE - 16) AND (CURRENT_DATE-1)
            AND du.first_name ILIKE 'scott' and db.name ilike '277 park'
            AND bs.operation_start_time IS NOT NULL
            AND bs.excluded_from_calculations = false
            GROUP BY
            db.id,
            db.name,
            wl.time_zone
            ORDER BY
            db.id;"
  - name: Building improvemts for user z ###Specific user
    question: Which building should I focus on for improvements? or where could we operating better? for user y.
    sql: "SELECT
            db.id AS building_id,
            db.name AS building_name,
            CAST(MAX(bs.operation_start_time) AS DATE) AS end_date,
            CAST(MIN(bs.operation_start_time) AS DATE) AS start_date,
            CAST(MAX(bs.OPERATION_START_TIME) AS TIME) AS OPERATION_START_TIME,
            CAST(MAX(bs.OPERATION_TURN_OFF_TIME) AS TIME) AS OPERATION_TURN_OFF_TIME,
            CAST(MAX(bs.RECOMMENDED_OPERATION_START_TIME ) AS TIME) AS RECOMMENDED_OPERATION_START_TIME,
            CAST(MAX(bs.LEASE_OBLIGATIONS_START_AT ) AS TIME) AS LEASE_OBLIGATIONS_START_AT,
            CAST(MAX(bs.LEASE_OBLIGATIONS_END_AT) AS TIME) AS LEASE_OBLIGATIONS_END_AT,
            CAST(MAx(bs.STOPPED_SATISFYING_LEASE_OBLIGATIONS_AT ) AS TIME) AS STOPPED_SATISFYING_LEASE_OBLIGATIONS_AT,
            CAST(MAX(bs.SATISFIED_LEASE_OBLIGATIONS_AT) AS TIME) AS SATISFIED_LEASE_OBLIGATIONS_AT,
            ROUND(AVG(bs.start_time_difference_in_minutes)) AS start_time_difference_in_minutes,
            ROUND(AVG(bs.time_in_bounds)) AS time_in_bounds,
            ROUND(AVG(bs.rt)) AS avg_rt,
            ROUND(AVG(bs.startup_minutes_from_lease_start)) AS startup_minutes_from_lease_start,
            ROUND(AVG(bs.excess_run_time)) AS excess_run_time,
            LISTAGG(alerts, ',') WITHIN GROUP (ORDER BY alerts) AS alerts,bs.time_zone  
            FROM
                fact_building_daily_stats AS bs
            JOIN
                dim_buildings AS db ON bs.building_id = db.id
            JOIN
                dim_building_users AS bu ON bu.building_id = db.id
            JOIN
                dim_users AS du ON du.id = bu.user_id
            WHERE
            bs.date BETWEEN (CURRENT_DATE - 16) AND (CURRENT_DATE - 1)
            AND du.first_name ILIKE 'y'
            AND bs.operation_start_time IS NOT NULL
            AND bs.excluded_from_calculations = false
            GROUP BY
                db.id,
                db.name
            ORDER BY
                db.id;"

  - name: Building improvemts for user z ###Specific portfolio
    question: Which building should I focus on for improvements? or where could we operating better? in portfolio y.
    sql: "WITH __fact_building_daily_stats AS (
            SELECT
                excluded_from_calculations,
                building_id,
                alerts,
                time_zone,
                date,
                operation_start_time,
                operation_turn_off_time,
                recommended_operation_start_time,
                satisfied_lease_obligations_at,
                stopped_satisfying_lease_obligations_at,
                lease_obligations_start_at,
                lease_obligations_end_at,
                start_time_difference_in_minutes,
                time_in_bounds,
                rt,
                startup_minutes_from_lease_start,
                excess_run_time
            FROM cortex_search.silver.fact_building_daily_stats
            ), __dim_buildings AS (
            SELECT
                id,
                name
            FROM cortex_search.silver.dim_buildings
            ), __dim_portfolio_buildings AS (
            SELECT
                building_id,
                portfolio_id
            FROM cortex_search.silver.dim_portfolio_buildings
            ), __dim_portfolios AS (
            SELECT
                name,
                id
            FROM cortex_search.silver.dim_portfolios
            )
            SELECT
            db.id AS building_id,
            db.name AS building_name,
            CAST(MAX(bs.operation_start_time) AS DATE) AS end_date,
            CAST(MIN(bs.operation_start_time) AS DATE) AS start_date,
            CAST(MAX(bs.OPERATION_START_TIME) AS TIME) AS OPERATION_START_TIME,
            CAST(MAX(bs.OPERATION_TURN_OFF_TIME) AS TIME) AS OPERATION_TURN_OFF_TIME,
            CAST(MAX(bs.RECOMMENDED_OPERATION_START_TIME) AS TIME) AS RECOMMENDED_OPERATION_START_TIME,
            CAST(MAX(bs.LEASE_OBLIGATIONS_START_AT) AS TIME) AS LEASE_OBLIGATIONS_START_AT,
            CAST(MAX(bs.LEASE_OBLIGATIONS_END_AT) AS TIME) AS LEASE_OBLIGATIONS_END_AT,
            CAST(MAX(bs.STOPPED_SATISFYING_LEASE_OBLIGATIONS_AT) AS TIME) AS STOPPED_SATISFYING_LEASE_OBLIGATIONS_AT,
            CAST(MAX(bs.SATISFIED_LEASE_OBLIGATIONS_AT) AS TIME) AS SATISFIED_LEASE_OBLIGATIONS_AT,
            ROUND(AVG(bs.start_time_difference_in_minutes)) AS start_time_difference_in_minutes,
            ROUND(AVG(bs.time_in_bounds)) AS time_in_bounds,
            ROUND(AVG(bs.rt)) AS avg_rt,
            ROUND(AVG(bs.startup_minutes_from_lease_start)) AS startup_minutes_from_lease_start,
            ROUND(AVG(bs.excess_run_time)) AS excess_run_time,
            LISTAGG(bs.alerts, ',') WITHIN GROUP (ORDER BY
                bs.alerts) AS alerts,
            bs.time_zone
            FROM __fact_building_daily_stats AS bs
            INNER JOIN __dim_buildings AS db
            ON bs.building_id = db.id
            INNER JOIN __dim_portfolio_buildings AS pb
            ON db.id = pb.building_id
            INNER JOIN __dim_portfolios AS p
            ON pb.portfolio_id = p.id
            WHERE
            bs.date BETWEEN (
                CURRENT_DATE - 15
            ) AND CURRENT_DATE
            AND p.name ilike 'y'
            AND NOT bs.operation_start_time IS NULL
            AND bs.excluded_from_calculations = FALSE
            GROUP BY
            db.id,
            db.name,
            bs.time_zone
            ORDER BY
            db.id
            -- Generated by Cortex Analyst
            ;"          
            """