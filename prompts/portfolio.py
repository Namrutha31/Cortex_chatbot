prompt_portfolio = """
 ###Instruction:
 In interpreation of question, do not change any words or context, or do not assume to add anything.
   **Do not alter the meaning or context in your interpretation of question, if the user question is related to (best/worst,poor/best performance, ineffective, inefficiency) do not interpret only negative values, include all values along with all savings columns, do not reside on 1 or 2 columns; keep it exactly as it is.**
   **If any time peroid comes; do not change the format in your interpretation(for ex. in query if mentioned last month, keep last month in your interpretation, do not change to December 2024 )**
   **Strictly ensure that only for queries like "Compare with some time period", then the last year's date is included. If the user requests for compare data for a specific period (X), the SQL query must include both the requested period (X) and the previous year's corresponding period (X-1) to allow comparison. This rule must be enforced for all compare queries without exception. Check the verified queries below for reference.**
   **Strictly round off all values to 0 decimal places, except for energy intensity queries.**
   **For any portfolios-related question, first check the list of verified queries. For all types of questions (best, worst, performance, efficiency, inefficiency), ensure you include all the columns mentioned below.**
   **RANK based on only  "electric_consumption_total_savings_percent" column, strictly do not choose any other columns and STRICTLY use below rank verified queries for rank based questions.**
   **Strictly retrieve all portfolios with electric_rank in the SQL query for both best and worst portfolio queries. Do not generate SQL query to return only one best and worst portfolio.**
   **If the user query matches (or closely resembles) any of the verified queries, use the verified query as a reference to formulate the response.**
   **Since the data is cumulative, for any period-based queries,Strictly use the last date of the specified period. For example, if the query is for last year, use the last date of that year (e.g., 31/12/2024).**
   **If the query does not specify a time period, it should default to type = "PortfolioSummaryMetricsYearToDate".**
   **If the query is asked for year, then it should take, type = "PortfolioSummaryMetricsYearToDate" and date ="current_date -2"**
   **If the user query does not match any verified queries(like best or worst), use the following columns from the fact_portfolio_metrics table:
      portfolio_id, portfolio_name,date,days_included,electric_consumption_total_savings_kwh,electric_consumption_total_actual_kwh,electric_consumption_total_baseline_kwh,steam_consumption_total_savings_mlbs,steam_consumption_total_actual_mlbs,steam_consumption_total_baseline_mlbs,gas_consumption_total_savings_therms,gas_consumption_total_actual_therms,gas_consumption_total_baseline_therms,total_carbon_savings_tons_co2,electric_consumption_total_savings_percent,steam_consumption_total_savings_percent,gas_consumption_total_savings_percent,START_TIME_LATE_START_PERCENT,START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,START_TIME_EARLY_START_PERCENT,
   - When generating dates, use the dates mentioned in the verified query as a reference.
   - If no reference exists, provide a range or default based on the question.
   - Use the data retrieved from the fact_portfolio_metrics table to directly respond to the user query.
   - Ensure all answers are concise and to the point.
###Generate an SQL query based on the following verified queries;
verified_queries:
  - name: Portfolio Performance without mentioning date 
    question: How did x's portfolios perform?
    sql: "SELECT pm.portfolio_id,p.name AS portfolio_name,DATEADD(DAY,-(pm.days_included),pm.date) AS from_date,pm.date AS end_date,pm.days_included,ROUND(pm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(pm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(pm.electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(pm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(pm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(pm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(pm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(pm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(pm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(pm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(pm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(pm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(pm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(pm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(pm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND(((pm.START_TIME_LATE_START_PERCENT*pm.days_included)/100)) AS START_TIME_LATE_START_DAYS,ROUND(((pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*pm.days_included)/100)) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((pm.START_TIME_EARLY_START_PERCENT*pm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(pm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded,
        from fact_portfolio_metrics as pm join dim_portfolios
      as p on pm.portfolio_id = p.id join dim_portfolio_users pu on pu.portfolio_id
      = p.id join dim_users u on u.id = pu.user_id where (pm.type = 'PortfolioSummaryMetricsYearToDate'
      and ( pm.date = current_date -2)) and u.first_name ilike 'x' order by pm.portfolio_id;"

  - name: Portfolio Performance for current year 
    question: How did x's portfolios perform in 2025?
    sql: "SELECT pm.portfolio_id,p.name AS portfolio_name,DATEADD(DAY,-(pm.days_included),pm.date) AS from_date,pm.date AS end_date,pm.days_included,ROUND(pm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(pm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(pm.electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(pm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(pm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(pm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(pm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(pm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(pm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(pm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(pm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(pm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(pm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(pm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(pm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND(((pm.START_TIME_LATE_START_PERCENT*pm.days_included)/100)) AS START_TIME_LATE_START_DAYS,ROUND(((pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*pm.days_included)/100)) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((pm.START_TIME_EARLY_START_PERCENT*pm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(pm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded,
        from fact_portfolio_metrics as pm join dim_portfolios
      as p on pm.portfolio_id = p.id join dim_portfolio_users pu on pu.portfolio_id
      = p.id join dim_users u on u.id = pu.user_id where (pm.type = 'PortfolioSummaryMetricsYearToDate'
      and ( pm.date = current_date -2)) and u.first_name ilike 'x' order by pm.portfolio_id;"      

  - name: Compare Portfolio Performance without mentioning date 
    question: Compare x's portfolios perform?
    sql: "SELECT pm.portfolio_id,p.name AS portfolio_name,DATEADD(DAY,-(pm.days_included),pm.date) AS from_date,pm.date AS end_date,pm.days_included,ROUND(pm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(pm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(pm.electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(pm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(pm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(pm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(pm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(pm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(pm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(pm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(pm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(pm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(pm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(pm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(pm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND(((pm.START_TIME_LATE_START_PERCENT*pm.days_included)/100)) AS START_TIME_LATE_START_DAYS,ROUND(((pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*pm.days_included)/100)) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((pm.START_TIME_EARLY_START_PERCENT*pm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(pm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded ,
        from fact_portfolio_metrics as pm join dim_portfolios
      as p on pm.portfolio_id = p.id join dim_portfolio_users pu on pu.portfolio_id
      = p.id join dim_users u on u.id = pu.user_id where (pm.type = 'PortfolioSummaryMetricsYearToDate'
      and ( pm.date = current_date -2 OR pm.date = DATEADD(YEAR, -1, current_date
       -2))) and u.first_name ilike 'x' order by pm.portfolio_id;"       

  - name: Portfolio Performance for last year
    question: How did x's portfolios perform in the last year?
    sql: "SELECT pm.portfolio_id,p.name AS portfolio_name,DATEADD(DAY,-(pm.days_included),pm.date) AS from_date,pm.date AS end_date,pm.days_included,ROUND(pm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(pm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(pm.electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(pm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(pm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(pm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(pm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(pm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(pm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(pm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(pm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(pm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(pm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(pm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(pm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND(((pm.START_TIME_LATE_START_PERCENT*pm.days_included)/100)) AS START_TIME_LATE_START_DAYS,ROUND(((pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*pm.days_included)/100)) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((pm.START_TIME_EARLY_START_PERCENT*pm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(pm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded ,
        from fact_portfolio_metrics as pm join dim_portfolios
      as p on pm.portfolio_id = p.id join dim_portfolio_users pu on pu.portfolio_id
      = p.id join dim_users u on u.id = pu.user_id where (pm.type = 'PortfolioSummaryMetricsYearToDate'and(MONTH(pm.date) = 12
  AND DAY(pm.date) = 31 and( year(pm.date)= year(current_date)-1 ))
      ) and  u.first_name ilike 'x' order by pm.portfolio_id;"

  - name: Compare Portfolio Performance for last year
    question: Compare x's portfolios perform in the last year?
    sql: "SELECT pm.portfolio_id,p.name AS portfolio_name,DATEADD(DAY,-(pm.days_included),pm.date) AS from_date,pm.date AS end_date,pm.days_included,ROUND(pm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(pm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(pm.electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(pm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(pm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(pm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(pm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(pm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(pm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(pm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(pm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(pm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(pm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(pm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(pm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND(((pm.START_TIME_LATE_START_PERCENT*pm.days_included)/100)) AS START_TIME_LATE_START_DAYS,ROUND(((pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*pm.days_included)/100)) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((pm.START_TIME_EARLY_START_PERCENT*pm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(pm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded ,
        from fact_portfolio_metrics as pm join dim_portfolios
      as p on pm.portfolio_id = p.id join dim_portfolio_users pu on pu.portfolio_id
      = p.id join dim_users u on u.id = pu.user_id where (pm.type = 'PortfolioSummaryMetricsYearToDate'and(MONTH(pm.date) = 12
  AND DAY(pm.date) = 31 and( year(pm.date)= year(current_date)-1  or year(pm.date)= year(current_date)-2))
      ) and  u.first_name ilike 'x' order by pm.portfolio_id;"

  - name: Compare Portfolio Performance for Given Year vs. the Present Year:(Compares performance between a specific mentioned year and the current year.)
    question: How did portfolio x perform compared to/with z year? or how portfolio x performance for user x with/to z?
    sql: "SELECT pm.portfolio_id,p.name AS portfolio_name,DATEADD(DAY,-(pm.days_included),pm.date) AS from_date,pm.date AS end_date,pm.days_included,ROUND(pm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(pm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(pm.electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(pm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(pm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(pm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(pm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(pm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(pm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(pm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(pm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(pm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(pm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(pm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(pm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND(((pm.START_TIME_LATE_START_PERCENT*pm.days_included)/100)) AS START_TIME_LATE_START_DAYS,ROUND(((pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*pm.days_included)/100)) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((pm.START_TIME_EARLY_START_PERCENT*pm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(pm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded ,
      FROM fact_portfolio_metrics AS pm 
      JOIN dim_portfolios AS p ON pm.portfolio_id = p.id 
      JOIN dim_portfolio_users pu ON pu.portfolio_id = p.id 
      JOIN dim_users u ON u.id = pu.user_id 
      WHERE pm.type = 'PortfolioSummaryMetricsYearToDate'
      AND (pm.date = CURRENT_DATE - 2 OR pm.date = DATEADD(YEAR, z - EXTRACT(YEAR FROM CURRENT_DATE), CURRENT_DATE - 2))
      AND u.first_name ILIKE 'x' 
      ORDER BY pm.portfolio_id;" 

  - name: Compare Portfolio Performance for Given Year vs. the Present Year:(Compares performance between a specific mentioned year and the current year.)
    question: Compare x's portfolios perform with/to y year?
    sql: "SELECT pm.portfolio_id,p.name AS portfolio_name,DATEADD(DAY,-(pm.days_included),pm.date) AS from_date,pm.date AS end_date,pm.days_included,ROUND(pm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(pm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(pm.electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(pm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(pm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(pm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(pm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(pm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(pm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(pm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(pm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(pm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(pm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(pm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(pm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND(((pm.START_TIME_LATE_START_PERCENT*pm.days_included)/100)) AS START_TIME_LATE_START_DAYS,ROUND(((pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*pm.days_included)/100)) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((pm.START_TIME_EARLY_START_PERCENT*pm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(pm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded ,
      FROM fact_portfolio_metrics AS pm 
      JOIN dim_portfolios AS p ON pm.portfolio_id = p.id 
      JOIN dim_portfolio_users pu ON pu.portfolio_id = p.id 
      JOIN dim_users u ON u.id = pu.user_id 
      WHERE pm.type = 'PortfolioSummaryMetricsYearToDate'
      AND (pm.date = CURRENT_DATE - 2 OR pm.date = DATEADD(YEAR, y - EXTRACT(YEAR FROM CURRENT_DATE), CURRENT_DATE - 2))
      AND u.first_name ILIKE 'x' 
      ORDER BY pm.portfolio_id;"
            
  - name: Portfolio Performance for specific year: (Evaluates portfolio performance within a single specified year)
    question: How did x's portfolios perform in the y year?
    sql: "SELECT pm.portfolio_id,p.name AS portfolio_name,DATEADD(DAY,-(pm.days_included),pm.date) AS from_date,pm.date AS end_date,pm.days_included,ROUND(pm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(pm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(pm.electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(pm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(pm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(pm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(pm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(pm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(pm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(pm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(pm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(pm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(pm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(pm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(pm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND(((pm.START_TIME_LATE_START_PERCENT*pm.days_included)/100)) AS START_TIME_LATE_START_DAYS,ROUND(((pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*pm.days_included)/100)) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((pm.START_TIME_EARLY_START_PERCENT*pm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(pm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded ,
        from fact_portfolio_metrics as pm join dim_portfolios
      as p on pm.portfolio_id = p.id join dim_portfolio_users pu on pu.portfolio_id
      = p.id join dim_users u on u.id = pu.user_id where (pm.type = 'PortfolioSummaryMetricsYearToDate'and(MONTH(pm.date) = 12
      AND DAY(pm.date) = 31 and( year(pm.date)= y ))
      ) and  u.first_name ilike 'x' order by pm.portfolio_id;" 

  - name: Portfolio Performance for specific quarter: (Evaluates portfolio performance within a single specified quarter)
    question: How did x's portfolios perform in the yth quarter of z year?
    sql: "SELECT pm.portfolio_id,p.name AS portfolio_name,DATEADD(DAY,-(pm.days_included),pm.date) AS from_date,pm.date AS end_date,pm.days_included,ROUND(pm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(pm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(pm.electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(pm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(pm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(pm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(pm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(pm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(pm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(pm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(pm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(pm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(pm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(pm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(pm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND(((pm.START_TIME_LATE_START_PERCENT*pm.days_included)/100)) AS START_TIME_LATE_START_DAYS,ROUND(((pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*pm.days_included)/100)) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((pm.START_TIME_EARLY_START_PERCENT*pm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(pm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded ,
        from fact_portfolio_metrics as pm join dim_portfolios
      as p on pm.portfolio_id = p.id join dim_portfolio_users pu on pu.portfolio_id
      = p.id join dim_users u on u.id = pu.user_id where pm.type = 'PortfolioSummaryMetricsFullQuarter' 
            AND (QUARTER(pm.date) = y and year(pm.date) = z )and u.first_name ilike 'x' order by pm.portfolio_id;" 

  - name: Portfolio Performance for specific month: (Evaluates portfolio performance within a single specified month)
    question: How did x's portfolios perform in the yth month of z year?
    sql: "SELECT pm.portfolio_id,p.name AS portfolio_name,DATEADD(DAY,-(pm.days_included),pm.date) AS from_date,pm.date AS end_date,pm.days_included,ROUND(pm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(pm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(pm.electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(pm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(pm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(pm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(pm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(pm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(pm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(pm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(pm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(pm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(pm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(pm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(pm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND(((pm.START_TIME_LATE_START_PERCENT*pm.days_included)/100)) AS START_TIME_LATE_START_DAYS,ROUND(((pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*pm.days_included)/100)) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((pm.START_TIME_EARLY_START_PERCENT*pm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(pm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded ,
        from fact_portfolio_metrics as pm join dim_portfolios
        as p on pm.portfolio_id = p.id join dim_portfolio_users pu on pu.portfolio_id
        = p.id join dim_users u on u.id = pu.user_id where pm.type = 'PortfolioSummaryMetricsFullMonth' and (MONTH(pm.date) = y and year(pm.date)='z')
       and  u.first_name ilike 'x' order by pm.portfolio_id;"                              

  - name: Portfolio Performance for past/last 30 rolling days
    question: How did X's portfolios perform in the past 30 rolling days?
    sql: "SELECT pm.portfolio_id,p.name AS portfolio_name,DATEADD(DAY,-(pm.days_included),pm.date) AS from_date,pm.date AS end_date,pm.days_included,ROUND(pm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(pm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(pm.electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(pm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(pm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(pm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(pm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(pm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(pm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(pm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(pm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(pm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(pm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(pm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(pm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND(((pm.START_TIME_LATE_START_PERCENT*pm.days_included)/100)) AS START_TIME_LATE_START_DAYS,ROUND(((pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*pm.days_included)/100)) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((pm.START_TIME_EARLY_START_PERCENT*pm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(pm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded ,
        from fact_portfolio_metrics as pm join dim_portfolios
      as p on pm.portfolio_id = p.id join dim_portfolio_users pu on pu.portfolio_id
      = p.id join dim_users u on u.id = pu.user_id where (pm.type = 'PortfolioSummaryMetricsPastThirtyRollingDays'
      and ( pm.date = current_date -2 )) and u.first_name ilike 'x' order by pm.portfolio_id;"

  - name: Compare Portfolio Performance for past/last 30 rolling days
    question: Compare x's portfolios perform in the past 30 rolling days?
    sql: "SELECT pm.portfolio_id,p.name AS portfolio_name,DATEADD(DAY,-(pm.days_included),pm.date) AS from_date,pm.date AS end_date,pm.days_included,ROUND(pm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(pm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(pm.electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(pm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(pm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(pm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(pm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(pm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(pm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(pm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(pm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(pm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(pm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(pm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(pm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND(((pm.START_TIME_LATE_START_PERCENT*pm.days_included)/100)) AS START_TIME_LATE_START_DAYS,ROUND(((pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*pm.days_included)/100)) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((pm.START_TIME_EARLY_START_PERCENT*pm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(pm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded ,
        from fact_portfolio_metrics as pm join dim_portfolios
      as p on pm.portfolio_id = p.id join dim_portfolio_users pu on pu.portfolio_id
      = p.id join dim_users u on u.id = pu.user_id where (pm.type = 'PortfolioSummaryMetricsPastThirtyRollingDays'
      and ( pm.date = current_date -2 OR pm.date = DATEADD(YEAR, -1, current_date
       -2))) and u.first_name ilike 'x' order by pm.portfolio_id;"

  - name: Portfolio Performance for past/last full month
    question: How did X's portfolios perform in the last or last full month?
    sql: "SELECT pm.portfolio_id,p.name AS portfolio_name,DATEADD(DAY,-(pm.days_included),pm.date) AS from_date,pm.date AS end_date,pm.days_included,ROUND(pm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(pm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(pm.electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(pm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(pm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(pm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(pm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(pm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(pm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(pm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(pm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(pm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(pm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(pm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(pm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND(((pm.START_TIME_LATE_START_PERCENT*pm.days_included)/100)) AS START_TIME_LATE_START_DAYS,ROUND(((pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*pm.days_included)/100)) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((pm.START_TIME_EARLY_START_PERCENT*pm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(pm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded ,
        from fact_portfolio_metrics as pm join dim_portfolios
      as p on pm.portfolio_id = p.id join dim_portfolio_users pu on pu.portfolio_id
      = p.id join dim_users u on u.id = pu.user_id where (pm.type = 'PortfolioSummaryMetricsFullMonth'
       and ( pm.date =DATEADD(DAY, -1, DATE_TRUNC('MONTH', CURRENT_DATE))
      )) and  u.first_name ilike 'x' order by pm.portfolio_id;"

  - name: Compare Portfolio Performance for past/last full month
    question: Compare x's portfolios perform in the last or last full month?
    sql: "SELECT pm.portfolio_id,p.name AS portfolio_name,DATEADD(DAY,-(pm.days_included),pm.date) AS from_date,pm.date AS end_date,pm.days_included,ROUND(pm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(pm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(pm.electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(pm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(pm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(pm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(pm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(pm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(pm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(pm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(pm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(pm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(pm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(pm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(pm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND(((pm.START_TIME_LATE_START_PERCENT*pm.days_included)/100)) AS START_TIME_LATE_START_DAYS,ROUND(((pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*pm.days_included)/100)) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((pm.START_TIME_EARLY_START_PERCENT*pm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(pm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded ,
        from fact_portfolio_metrics as pm join dim_portfolios
      as p on pm.portfolio_id = p.id join dim_portfolio_users pu on pu.portfolio_id
      = p.id join dim_users u on u.id = pu.user_id where (pm.type = 'PortfolioSummaryMetricsFullMonth'
       and  ( pm.date = DATEADD(DAY, -1, DATE_TRUNC('MONTH', CURRENT_DATE)) OR pm.date
            = DATEADD(DAY, -1, DATEADD(YEAR, -1, DATE_TRUNC('MONTH', CURRENT_DATE)))
            )) and  u.first_name ilike 'x' order by pm.portfolio_id;"      

  - name: Portfolio Performance for rolling or current year
    question: How did X's portfolios perform in the rolling or current year?
    sql: "SELECT pm.portfolio_id,p.name AS portfolio_name,DATEADD(DAY,-(pm.days_included),pm.date) AS from_date,pm.date AS end_date,pm.days_included,ROUND(pm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(pm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(pm.electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(pm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(pm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(pm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(pm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(pm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(pm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(pm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(pm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(pm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(pm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(pm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(pm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND(((pm.START_TIME_LATE_START_PERCENT*pm.days_included)/100)) AS START_TIME_LATE_START_DAYS,ROUND(((pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*pm.days_included)/100)) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((pm.START_TIME_EARLY_START_PERCENT*pm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(pm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded ,
        from fact_portfolio_metrics as pm join dim_portfolios
      as p on pm.portfolio_id = p.id join dim_portfolio_users pu on pu.portfolio_id
      = p.id join dim_users u on u.id = pu.user_id where (pm.type = 'PortfolioSummaryMetricsPastRollingYear'
      and ( pm.date = current_date -2 )) and u.first_name ilike 'x' order by pm.portfolio_id;"

  - name: Compare Portfolio Performance for rolling or current year
    question: Compare x's portfolios perform in the rolling or current year?
    sql: "SELECT pm.portfolio_id,p.name AS portfolio_name,DATEADD(DAY,-(pm.days_included),pm.date) AS from_date,pm.date AS end_date,pm.days_included,ROUND(pm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(pm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(pm.electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(pm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(pm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(pm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(pm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(pm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(pm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(pm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(pm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(pm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(pm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(pm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(pm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND(((pm.START_TIME_LATE_START_PERCENT*pm.days_included)/100)) AS START_TIME_LATE_START_DAYS,ROUND(((pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*pm.days_included)/100)) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((pm.START_TIME_EARLY_START_PERCENT*pm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(pm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded ,
        from fact_portfolio_metrics as pm join dim_portfolios
      as p on pm.portfolio_id = p.id join dim_portfolio_users pu on pu.portfolio_id
      = p.id join dim_users u on u.id = pu.user_id where (pm.type = 'PortfolioSummaryMetricsPastRollingYear'
      and ( pm.date = current_date -2 OR pm.date = DATEADD(YEAR, -1, current_date
       -2))) and u.first_name ilike 'x' order by pm.portfolio_id;"       


  - name: Portfolio Performance for till the date or year to date
    question: How did X's portfolios perform in the till current date this year?
    sql: "SELECT pm.portfolio_id,p.name AS portfolio_name,DATEADD(DAY,-(pm.days_included),pm.date) AS from_date,pm.date AS end_date,pm.days_included,ROUND(pm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(pm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(pm.electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(pm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(pm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(pm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(pm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(pm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(pm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(pm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(pm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(pm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(pm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(pm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(pm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND(((pm.START_TIME_LATE_START_PERCENT*pm.days_included)/100)) AS START_TIME_LATE_START_DAYS,ROUND(((pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*pm.days_included)/100)) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((pm.START_TIME_EARLY_START_PERCENT*pm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(pm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded ,
        from fact_portfolio_metrics as pm join dim_portfolios
      as p on pm.portfolio_id = p.id join dim_portfolio_users pu on pu.portfolio_id
      = p.id join dim_users u on u.id = pu.user_id where (pm.type = 'PortfolioSummaryMetricsYearToDate'
      and ( pm.date = current_date -2 )) and u.first_name ilike 'x' order by pm.portfolio_id;"
       
  - name: Portfolio Performance for last quarter
    question: How did X's portfolios perform in the last/full quarter?
    sql: "SELECT pm.portfolio_id,p.name AS portfolio_name,DATEADD(DAY,-(pm.days_included),pm.date) AS from_date,pm.date AS end_date,pm.days_included,ROUND(pm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(pm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(pm.electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(pm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(pm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(pm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(pm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(pm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(pm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(pm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(pm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(pm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(pm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(pm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(pm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND(((pm.START_TIME_LATE_START_PERCENT*pm.days_included)/100)) AS START_TIME_LATE_START_DAYS,ROUND(((pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*pm.days_included)/100)) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((pm.START_TIME_EARLY_START_PERCENT*pm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(pm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded ,
        from fact_portfolio_metrics as pm join dim_portfolios
      as p on pm.portfolio_id = p.id join dim_portfolio_users pu on pu.portfolio_id
      = p.id join dim_users u on u.id = pu.user_id where pm.type = 'PortfolioSummaryMetricsFullQuarter' 
            AND (
                pm.date = DATEADD(DAY, -1, DATE_TRUNC('QUARTER', CURRENT_DATE())) 
            ) 
                and u.first_name ilike 'x' order by pm.portfolio_id;" 

  - name: Compare Portfolio Performance for last quarter
    question: Compare x's portfolios perform in the last/full quarter?
    sql: "SELECT pm.portfolio_id,p.name AS portfolio_name,DATEADD(DAY,-(pm.days_included),pm.date) AS from_date,pm.date AS end_date,pm.days_included,ROUND(pm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(pm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(pm.electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(pm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(pm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(pm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(pm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(pm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(pm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(pm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(pm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(pm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(pm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(pm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(pm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND(((pm.START_TIME_LATE_START_PERCENT*pm.days_included)/100)) AS START_TIME_LATE_START_DAYS,ROUND(((pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*pm.days_included)/100)) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((pm.START_TIME_EARLY_START_PERCENT*pm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(pm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded ,
        from fact_portfolio_metrics as pm join dim_portfolios
      as p on pm.portfolio_id = p.id join dim_portfolio_users pu on pu.portfolio_id
      = p.id join dim_users u on u.id = pu.user_id where pm.type = 'PortfolioSummaryMetricsFullQuarter' 
            AND (
        PM.DATE =  DATEADD(DAY, -1, DATE_TRUNC(YEAR, DATEADD(QUARTER, -1, CURRENT_DATE()))) OR pm.date = DATEADD(DAY, -1, DATE_TRUNC('QUARTER', CURRENT_DATE()))
        ) 
                and u.first_name ilike 'x' order by pm.portfolio_id;"                       
       
  - name: Compare 2 or more portfolio performance for specific period
    question: Compare portfolio x and y performance in the last/full quarter?
    sql: "SELECT pm.portfolio_id,p.name AS portfolio_name,DATEADD(DAY,-(pm.days_included),pm.date) AS from_date,pm.date AS end_date,pm.days_included,ROUND(pm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(pm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(pm.electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(pm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(pm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(pm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(pm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(pm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(pm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(pm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(pm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(pm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(pm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(pm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(pm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND(((pm.START_TIME_LATE_START_PERCENT*pm.days_included)/100)) AS START_TIME_LATE_START_DAYS,ROUND(((pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*pm.days_included)/100)) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((pm.START_TIME_EARLY_START_PERCENT*pm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(pm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded ,
        from fact_portfolio_metrics as pm join dim_portfolios
      as p on pm.portfolio_id = p.id join dim_portfolio_users pu on pu.portfolio_id
      = p.id join dim_users u on u.id = pu.user_id where pm.type = 'PortfolioSummaryMetricsFullQuarter' 
            AND (
        PM.DATE =  DATEADD(DAY, -1, DATE_TRUNC(YEAR, DATEADD(QUARTER, -1, CURRENT_DATE()))) OR pm.date = DATEADD(DAY, -1, DATE_TRUNC('QUARTER', CURRENT_DATE()))
        ) 
                and (p.name ilike 'x' or p.name ilike 'y') order by pm.portfolio_id;" 
                       
  - name: Portfolio Performance for since it was included or since installing cortex
    question: How did portfolio y carried out since it was included or since installing cortex? for user X
    sql: "SELECT pm.portfolio_id,p.name AS portfolio_name,DATEADD(DAY,-(pm.days_included),pm.date) AS from_date,pm.date AS end_date,pm.days_included,ROUND(pm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(pm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(pm.electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(pm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(pm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(pm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(pm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(pm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(pm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(pm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(pm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(pm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(pm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(pm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(pm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND(((pm.START_TIME_LATE_START_PERCENT*pm.days_included)/100)) AS START_TIME_LATE_START_DAYS,ROUND(((pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*pm.days_included)/100)) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((pm.START_TIME_EARLY_START_PERCENT*pm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(pm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded ,
        from fact_portfolio_metrics as pm join dim_portfolios
      as p on pm.portfolio_id = p.id join dim_portfolio_users pu on pu.portfolio_id
      = p.id join dim_users u on u.id = pu.user_id where pm.type = 'PortfolioSummaryMetricsYearToDate' 
            AND ((MONTH(pm.date) = 12
        AND DAY(pm.date) = 31) or pm.date = current_date-2)
                and u.first_name ilike 'x' and p.name ilike 'y' order by pm.portfolio_id;" 
  - name: Compare X number of portfolios performance 
    question: Compare any x portfolios of user Brayan for last quarter
    sql: "WITH portfolio_ids AS (
            SELECT dp.id 
            FROM dim_portfolios dp
            JOIN dim_portfolio_users pu ON dp.id = pu.portfolio_id
            JOIN dim_users du ON du.id = pu.user_id
            WHERE du.first_name ILIKE 'mike' 
            LIMIT 5
          )
          SELECT
            pm.portfolio_id,
            p.name AS portfolio_name,
            pm.date,
            pm.days_included,
            pm.electric_consumption_total_savings_kwh,
            pm.electric_consumption_total_actual_kwh,
            pm.electric_consumption_total_baseline_kwh,
            pm.steam_consumption_total_savings_mlbs,
            pm.steam_consumption_total_actual_mlbs,
            pm.steam_consumption_total_baseline_mlbs,
            pm.gas_consumption_total_savings_therms,
            pm.gas_consumption_total_actual_therms,
            pm.gas_consumption_total_baseline_therms,
            pm.total_carbon_savings_tons_co2,
            pm.start_time_late_start_percent,
            pm.start_time_followed_recommendation_percent,
            pm.start_time_early_start_percent,
            CASE 
                WHEN pm.days_included < (
                    SELECT MAX(days_included) / 2 
                    FROM fact_portfolio_metrics 
                    WHERE type = 'PortfolioSummaryMetricsFullQuarter'
                )
                THEN TRUE 
                ELSE FALSE 
            END AS excluded
          FROM fact_portfolio_metrics pm
          JOIN dim_portfolios p ON pm.portfolio_id = p.id
          WHERE 
            pm.type = 'PortfolioSummaryMetricsFullQuarter'
            AND pm.date IN (
                DATEADD(DAY, -1, DATE_TRUNC('QUARTER', CURRENT_DATE)), 
                DATEADD(YEAR, -1, DATEADD(DAY, -1, DATE_TRUNC('QUARTER', CURRENT_DATE)))
            )
            AND pm.portfolio_id IN (SELECT id FROM portfolio_ids);"   
            
  - name: Portfolio Performance to provide best and worst portfolio
    question:compare all portfolios performance of user x and give best and worst portfolio for last month
    sql: "SELECT pm.portfolio_id,p.name AS portfolio_name,DATEADD(DAY,-(pm.days_included),pm.date) AS from_date,pm.date AS end_date,pm.days_included,ROUND(pm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(pm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(pm.electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(pm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(pm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(pm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(pm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(pm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(pm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(pm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(pm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(pm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(pm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(pm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(pm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND(((pm.START_TIME_LATE_START_PERCENT*pm.days_included)/100)) AS START_TIME_LATE_START_DAYS,ROUND(((pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*pm.days_included)/100)) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((pm.START_TIME_EARLY_START_PERCENT*pm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(pm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded ,
          DENSE_RANK() OVER (PARTITION BY YEAR(date)  ORDER BY pm.electric_consumption_total_savings_percent DESC NULLS LAST) AS electric_rank,
        FROM  fact_portfolio_metrics AS pm
        JOIN dim_portfolios AS p
            ON pm.portfolio_id = p.id
        JOIN dim_portfolio_users AS pu
            ON pu.portfolio_id = p.id
        JOIN dim_users AS u
            ON u.id = pu.user_id
        WHERE
            pm.type = 'PortfolioSummaryMetricsFullMonth'
            AND (pm.date = DATEADD(DAY, -1, DATE_TRUNC('MONTH', CURRENT_DATE)))
            AND u.first_name ILIKE 'x'  order by portfolio_id" 

  - name: Portfolio Performance to provide best and worst portfolio 
    question:Which portfolio performed well compared to other portfolios for the associated user x over last quarter?
    sql: "SELECT pm.portfolio_id,p.name AS portfolio_name,DATEADD(DAY,-(pm.days_included),pm.date) AS from_date,pm.date AS end_date,pm.days_included,ROUND(pm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(pm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(pm.electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(pm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(pm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(pm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(pm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(pm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(pm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(pm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(pm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(pm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(pm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(pm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(pm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND(((pm.START_TIME_LATE_START_PERCENT*pm.days_included)/100)) AS START_TIME_LATE_START_DAYS,ROUND(((pm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*pm.days_included)/100)) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((pm.START_TIME_EARLY_START_PERCENT*pm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(pm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded ,
          DENSE_RANK() OVER (PARTITION BY YEAR(date)  ORDER BY pm.electric_consumption_total_savings_percent DESC NULLS LAST) AS electric_rank,
          FROM  fact_portfolio_metrics AS pm
          JOIN dim_portfolios AS p
              ON pm.portfolio_id = p.id
          JOIN dim_portfolio_users AS pu
              ON pu.portfolio_id = p.id
          JOIN dim_users AS u
              ON u.id = pu.user_id
          where (pm.type = 'PortfolioSummaryMetricsFullMonth'
        and ( pm.date = DATEADD(DAY, -1, DATE_TRUNC('QUARTER', CURRENT_DATE()))
        ))
              AND u.first_name ILIKE 'x';"  

  - name: Building Performance in specific Portfolio
    question:how my buildings in x porfolio working this year?  my name is y
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded,   
        FROM fact_building_summary_metrics AS bm
     JOIN dim_buildings as db on db.id = bm.building_id
     join fact_buildings as fb on db.id = fb.id
     and fb.active = true
     JOIN dim_portfolio_buildings as pb on pb.building_id = db.id 
     JOIN dim_portfolios as dp on dp.id = pb.portfolio_id
     join dim_portfolio_users as pu on pu.portfolio_id = dp.id
     join dim_users as du on du.id = pu.user_id
     where du.first_name ilike 'y' and  dp.name ilike 'x' AND (bm.DATE = CURRENT_DATE -2) AND bm.type = 'BuildingSummaryMetricsYearToDate';"       
             

  - name: Buildings Performance in specific Portfolio
    question:how my buildings in x porfolio working last month?  my name is y
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded,
      FROM fact_building_summary_metrics AS bm
     JOIN dim_buildings as db on db.id = bm.building_id
     join fact_buildings as fb on db.id = fb.id
     and fb.active = true
     JOIN dim_portfolio_buildings as pb on pb.building_id = db.id 
     JOIN dim_portfolios as dp on dp.id = pb.portfolio_id
     join dim_portfolio_users as pu on pu.portfolio_id = dp.id
     join dim_users as du on du.id = pu.user_id
          where du.first_name ilike 'y' and  dp.name ilike 'x' AND (bm.type = 'BuildingSummaryMetricsFullMonth'
                  and ( bm.date = DATEADD(DAY, -1, DATE_TRUNC('MONTH', CURRENT_DATE)) ));"

  - name: Compare specific building Performance in specific Portfolio in specific year for specific user
    question:compare my g building in x porfolio performed on y year?  my name is z
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded,
      FROM fact_building_summary_metrics AS bm
     JOIN dim_buildings as db on db.id = bm.building_id
     join fact_buildings as fb on db.id = fb.id
     and fb.active = true
     JOIN dim_portfolio_buildings as pb on pb.building_id = db.id 
     JOIN dim_portfolios as dp on dp.id = pb.portfolio_id
     join dim_portfolio_users as pu on pu.portfolio_id = dp.id
     join dim_users as du on du.id = pu.user_id
                  where bm.type = 'BuildingSummaryMetricsYearToDate' and(MONTH(bm.date) = 12
        AND DAY(bm.date) = 31 and( year(bm.date)= y  or year(bm.date)= y-1)) and du.first_name ilike 'z' and dp.name ilike 'x' and db.name ilike 'g' order by bm.building_id;"                    

  - name: Specific building Performance in specific Portfolio in specific year for specific user
    question:how my g building in x porfolio performed on y year?  my name is z
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded, 
      FROM fact_building_summary_metrics AS bm
     JOIN dim_buildings as db on db.id = bm.building_id
     join fact_buildings as fb on db.id = fb.id
     and fb.active = true
     JOIN dim_portfolio_buildings as pb on pb.building_id = db.id 
     JOIN dim_portfolios as dp on dp.id = pb.portfolio_id
     join dim_portfolio_users as pu on pu.portfolio_id = dp.id
     join dim_users as du on du.id = pu.user_id
                  where bm.type = 'BuildingSummaryMetricsYearToDate' and(MONTH(bm.date) = 12
        AND DAY(bm.date) = 31 and( year(bm.date)= y)) and du.first_name ilike 'z' and dp.name ilike 'x' and db.name ilike 'g' order by bm.building_id;"         

  - name: Energy intesity of buildings in specific portfolio
    question:Calculate the energy intensity for all buildings in x's portfolio over the entire available time period
    sql: "SELECT
          dp.name AS portfolio_name,
          db.name AS building_name,
          SUM(bm.electric_consumption_total_actual_kwh) / MAX(fb.total_sqft) AS electric_energy_intensity_kw,
          SUM(bm.steam_consumption_total_actual_mlbs) / MAX(fb.total_sqft) AS steam_energy_intensity_mlbs,
          SUM(bm.gas_consumption_total_actual_therms) / MAX(fb.total_sqft) AS gas_energy_intensity_therms,
          bm.days_included,
          bm.date
        FROM
          fact_building_summary_metrics AS bm
          JOIN dim_buildings AS db ON db.id = bm.building_id
          JOIN fact_buildings AS fb ON db.id = fb.id
          JOIN dim_portfolio_buildings AS pb ON pb.building_id = db.id
          JOIN dim_portfolios AS dp ON dp.id = pb.portfolio_id  
        WHERE
          dp.name ILIKE 'x'
          AND bm.type = 'BuildingSummaryMetricsYearToDate'
          AND (
            (
              MONTH (bm.date) = 12
              AND DAY (bm.date) = 31
            )
            OR bm.date = CURRENT_DATE - 2
          )
        GROUP BY
          bm.building_id,
          dp.name,
          db.name,
          bm.type,
          bm.date;" 

  - name: Energy intesity of buildings in specific portfolio
    question:Calculate the energy intensity for all buildings in x's portfolio last year
    sql: "SELECT
          dp.name AS portfolio_name,
          db.name AS building_name,
          SUM(bm.electric_consumption_total_actual_kwh) / MAX(fb.total_sqft) AS electric_energy_intensity_kw,
          SUM(bm.steam_consumption_total_actual_mlbs) / MAX(fb.total_sqft) AS steam_energy_intensity_mlbs,
          SUM(bm.gas_consumption_total_actual_therms) / MAX(fb.total_sqft) AS gas_energy_intensity_therms,
          bm.days_included,
          bm.date
        FROM
          fact_building_summary_metrics AS bm
          JOIN dim_buildings AS db ON db.id = bm.building_id
          JOIN fact_buildings AS fb ON db.id = fb.id
          JOIN dim_portfolio_buildings AS pb ON pb.building_id = db.id
          JOIN dim_portfolios AS dp ON dp.id = pb.portfolio_id  
        WHERE
          dp.name ILIKE 'x' and
          (bm.type = 'BuildingSummaryMetricsYearToDate' and(MONTH(bm.date) = 12
        AND DAY(bm.date) = 31 and( year(bm.date)= year(current_date)-1 )))
        GROUP BY
          bm.building_id,
          dp.name,
          db.name,
          bm.type,
          bm.date;" 

  - name: Energy Usage of buildings; (About dataset:measurement_types(SteamMeasurement,GasMeasurement,ChilledWaterDemandMeasurement,PowerMeasurement[electric]))
    question:Which day last month did I use the most energy for building y? or provide me when i used most energy in last month for building y 
    sql: "WITH RankedConsumption AS (
        SELECT
          measurement_type,
          building_id,
          consumption_total_actual,
          date,
          db.name,
          ROW_NUMBER() OVER (
            PARTITION BY measurement_type
            ORDER BY
              consumption_total_actual DESC
          ) AS rn
        FROM
          fact_building_daily_consuption 
          join fact_buildings as fb on building_id = fb.id
          join dim_buildings as db on building_id = db.id
        WHERE
          date BETWEEN '2025-02-01'
          AND '2025-02-28' and db.name ilike 'y'
      )
      SELECT
      name,
        measurement_type,
        building_id,
        consumption_total_actual AS max_consumption,
        date
      FROM
        RankedConsumption
      WHERE
        rn = 1
      ORDER BY
        measurement_type;"          
     """