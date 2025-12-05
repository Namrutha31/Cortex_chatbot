prompt_building = """
###Instructions:
In interpreation of question, do not change any words or context, or do not assume to add anything.
    **Preserve Context and Meaning in your interpretation question:**
        - Interpret the user query exactly as stated without altering its meaning or context.
        - **Strictly do not restrict the data by using the LIMIT function in any query; retrieve all available data for all queries.**
        - For queries related to performance metrics (e.g., best, worst, poor performance, inefficiency, ineffective), include all relevant values mentioned below. Do not focus solely on negative or positive values. Ensure the query is answered comprehensively without limiting responses to one or two columns.
    **Maintain Time Period Formatting:**
        - Retain the time period format as mentioned in the query (e.g., if "last month" is used, do not change it to "December 2024").
        - **Strictly ensure that only for queries like "Compare with some time period", then the last year's date is included. If the user requests for compare data for a specific period (X), the SQL query must include both the requested period (X) and the previous year's corresponding period (X-1) to allow comparison. This rule must be enforced for all compare queries without exception. Check the verified queries below for reference.**
        - **Do not generate a previous year query for rank-based (best vs. worst) queries; include only the user-specified query.**
        - If no verified query exists for a similar time period, use logical reasoning to provide the appropriate range or default.
    **For Queries without mentioning time period:** 
        - If the query does not specify a time period, it should default to type = "BuildingSummaryMetricsYearToDate".
    **For Queries asked for current year:** 
        **If the query is asked for year, then it should take, type = "BuildingSummaryMetricsYearToDate" and date ="current_date -2"**
    **Building-Related Queries:**
        - For queries involving buildings, first refer to the list of verified queries. Use verified queries as a reference to ensure consistency and accuracy.
        - Include all default columns mentioned in the below, regardless of whether the focus is on best, worst, or other performance metrics.
        - RANK based on only  "electric_consumption_total_savings_percent" column, strictly do not choose any other columns.
        - **STRICTLY use below rank verified queries for rank based questions.**
        - **Strictly retrieve all buildings with electric_rank in the SQL query for both best and worst building queries. Do not generate SQL query to return only one best and worst building.**
    **Follow Verified Queries for Similar Questions:**
        - If the user query matches or closely resembles a verified query, use the verified query as a template for crafting the response.
        - Ensure all mentioned columns and metrics in the query are addressed comprehensively.
    **Default Columns for Unmatched Queries:**
        - If the user query does not match any verified queries (e.g., "best" or "worst"), use the following columns from the fact_building_summary_metrics table:
           building_id, building_name,date,days_included,electric_consumption_total_savings_kwh,electric_consumption_total_actual_kwh,electric_consumption_total_baseline_kwh,steam_consumption_total_savings_mlbs,steam_consumption_total_actual_mlbs,steam_consumption_total_baseline_mlbs,gas_consumption_total_savings_therms,gas_consumption_total_actual_therms,gas_consumption_total_baseline_therms,total_carbon_savings_tons_co2,electric_consumption_total_savings_percent,steam_consumption_total_savings_percent,gas_consumption_total_savings_percent,hdd_days,cdd_days,occupancy,total_sqft,START_TIME_LATE_START_PERCENT,START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,START_TIME_EARLY_START_PERCENT,((START_TIME_LATE_START_PERCENT*days_included)/100) AS START_TIME_LATE_START_DAYS,((START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,((START_TIME_EARLY_START_PERCENT*days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded
    **Handling Dates:**
        - When generating or referencing dates, use the dates mentioned in verified queries as a baseline.
        - **Since the data is cumulative, for any period-based queries,Strictly use the last date of the specified period. For example, if the query is for last year, use the last date of that year (e.g., 31/12/2024).**
        - If no verified query is applicable, provide logical date ranges based on the context of the question.
    **Strictly round off all values to 0 decimal places, except for energy intensity queries.**
    **Answer Construction:**
        - Use data directly retrieved from the fact_building_summary_metrics table to craft the response.
        - Ensure all responses are concise, accurate, and address the full scope of the user query.
###Generate an SQL query based on the following verified queries;
**verified_queries:**
verified_queries:
  - name: Building Performance without mentioning date 
    question: How did x's buildings perform?
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded
        FROM fact_building_summary_metrics AS bm
                  JOIN dim_buildings AS db ON bm.building_id = db.id
                  join fact_buildings as fb on db.id = fb.id
                  and fb.active = true
                  join dim_building_users  bu on db.id = bu.building_id
                  join dim_users as du on du.id = bu.user_id  
                  where bm.type = 'BuildingSummaryMetricsYearToDate' and(bm.date = CURRENT_DATE - 2) and du.first_name ilike 'x' order by bm.building_id;"

  - name: Building Performance for current year 
    question: How did x's buildings perform in 2025?
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded
        FROM fact_building_summary_metrics AS bm
                  JOIN dim_buildings AS db ON bm.building_id = db.id
                  join fact_buildings as fb on db.id = fb.id
                  and fb.active = true
                  join dim_building_users  bu on db.id = bu.building_id
                  join dim_users as du on du.id = bu.user_id  
                  where bm.type = 'BuildingSummaryMetricsYearToDate' and(bm.date = CURRENT_DATE - 2) and du.first_name ilike 'x' order by bm.building_id;"
                  
                                 
  - name: Compare Building Performance without mentioning date 
    question: Compare x's buildings perform?
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded
        FROM fact_building_summary_metrics AS bm
                  JOIN dim_buildings AS db ON bm.building_id = db.id
                  join fact_buildings as fb on db.id = fb.id
                  and fb.active = true
                  join dim_building_users  bu on db.id = bu.building_id
                  join dim_users as du on du.id = bu.user_id  
                  where bm.type = 'BuildingSummaryMetricsYearToDate' and(bm.date = CURRENT_DATE - 2 OR bm.date = DATEADD(YEAR, -1, CURRENT_DATE - 2)) and du.first_name ilike 'x' order by bm.building_id;"       

  - name: Building Performance for last year
    question: How did x's buildings perform in the last year?
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded
        FROM fact_building_summary_metrics AS bm
                  JOIN dim_buildings AS db ON bm.building_id = db.id
                  join fact_buildings as fb on db.id = fb.id
                  and fb.active = true
                  join dim_building_users  bu on db.id = bu.building_id
                  join dim_users as du on du.id = bu.user_id  
                  where (bm.type = 'BuildingSummaryMetricsYearToDate' and(MONTH(bm.date) = 12
        AND DAY(bm.date) = 31 and( year(bm.date)= year(current_date)-1 ))) and du.first_name ilike 'x' order by bm.building_id;"

  - name: Compare Building Performance for last year
    question: Compare x's buildings perform in the last year for user y?
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded
        FROM fact_building_summary_metrics AS bm
                  JOIN dim_buildings AS db ON bm.building_id = db.id
                  join fact_buildings as fb on db.id = fb.id
                  and fb.active = true
                  join dim_building_users  bu on db.id = bu.building_id
                  join dim_users as du on du.id = bu.user_id  
                  where (bm.type = 'BuildingSummaryMetricsYearToDate' and(MONTH(bm.date) = 12
        AND DAY(bm.date) = 31 and( year(bm.date)= year(current_date)-1  or year(bm.date)= year(current_date)-2))) and du.first_name ilike 'y' and db.name ilike 'x' order by bm.building_id;"

      
  - name: Building Performance for specific year: (Evaluates building performance within a single specified year)
    question: How did x's buildings perform in the y year?
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded
        FROM fact_building_summary_metrics AS bm
                  JOIN dim_buildings AS db ON bm.building_id = db.id
                  join fact_buildings as fb on db.id = fb.id
                  and fb.active = true
                  join dim_building_users  bu on db.id = bu.building_id
                  join dim_users as du on du.id = bu.user_id  
                  where bm.type = 'BuildingSummaryMetricsYearToDate' and(MONTH(bm.date) = 12
        AND DAY(bm.date) = 31 and( year(bm.date)= y)) and du.first_name ilike 'x' order by bm.building_id;" 
 
  - name: Building Performance for specific quarter: (Evaluates building performance within a single specified quarter)
    question: How did x's buildings perform in the yth quarter of z year?
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded
        FROM fact_building_summary_metrics AS bm
                  JOIN dim_buildings AS db ON bm.building_id = db.id
                  join fact_buildings as fb on db.id = fb.id
                  and fb.active = true
                  join dim_building_users  bu on db.id = bu.building_id
                  join dim_users as du on du.id = bu.user_id   where bm.type = 'BuildingSummaryMetricsFullQuarter' 
            AND (QUARTER(bm.date) = y and year(bm.date) = z )and du.first_name ilike 'x' order by bm.building_id;" 

  - name: Building Performance for specific month: (Evaluates building performance within a single specified month)
    question: How did x's buildings perform in the yth month of z year?
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded
        FROM fact_building_summary_metrics AS bm
                  JOIN dim_buildings AS db ON bm.building_id = db.id
                  join fact_buildings as fb on db.id = fb.id
                  and fb.active = true
                  join dim_building_users  bu on db.id = bu.building_id
                  join dim_users as du on du.id = bu.user_id  where bm.type = 'BuildingSummaryMetricsFullMonth' and (MONTH(bm.date) = y and year(bm.date)='z')
       and  du.first_name ilike 'x' order by bm.building_id;"  
        
  - name: Compare Building Performance for Given Year vs. the Present Year:(Compares performance between a specific mentioned year and the current year.)
    question: How did building x perform compared to/with z year?  or how building x performance for user x with/to z?
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded
      FROM fact_building_summary_metrics AS bm
                  JOIN dim_buildings AS db ON bm.building_id = db.id
                  join fact_buildings as fb on db.id = fb.id
                  and fb.active = true
                  join dim_building_users  bu on db.id = bu.building_id
                  join dim_users as du on du.id = bu.user_id  
      WHERE bm.type = 'BuildingSummaryMetricsYearToDate'
      AND (bm.date = CURRENT_DATE - 2 OR bm.date = DATEADD(YEAR, z - EXTRACT(YEAR FROM CURRENT_DATE), CURRENT_DATE - 2))
      AND du.first_name ILIKE 'x' 
      ORDER BY bm.building_id;" 

  - name: Compare Building Performance for Given Year vs. the Present Year:(Compares performance between a specific mentioned year and the current year.)
    question: Compare x's building perform with/to y year?
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded
      FROM fact_building_summary_metrics AS bm
                  JOIN dim_buildings AS db ON bm.building_id = db.id
                  join fact_buildings as fb on db.id = fb.id
                  and fb.active = true
                  join dim_building_users  bu on db.id = bu.building_id
                  join dim_users as du on du.id = bu.user_id  
      WHERE bm.type = 'BuildingSummaryMetricsYearToDate'
      AND (bm.date = CURRENT_DATE - 2 OR bm.date = DATEADD(YEAR, y - EXTRACT(YEAR FROM CURRENT_DATE), CURRENT_DATE - 2))
      AND du.first_name ILIKE 'x' 
      ORDER BY bm.building_id;"
           

  - name: Building Performance for past/last 30 rolling days
    question: How did X's buildings perform in the past 30 rolling days?
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded
        FROM fact_building_summary_metrics AS bm
                  JOIN dim_buildings AS db ON bm.building_id = db.id
                  join fact_buildings as fb on db.id = fb.id
                  and fb.active = true
                  join dim_building_users  bu on db.id = bu.building_id
                  join dim_users as du on du.id = bu.user_id  
                  where bm.type = 'BuildingSummaryMetricsPastThirtyRollingDays' and(bm.date = CURRENT_DATE - 2) and du.first_name ilike 'x' order by bm.building_id;"


  - name: Compare Building Performance for past/last 30 rolling days
    question: Compare x's buildings perform in the past 30 rolling days for user y?
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded
        FROM fact_building_summary_metrics AS bm
                  JOIN dim_buildings AS db ON bm.building_id = db.id
                  join fact_buildings as fb on db.id = fb.id
                  and fb.active = true
                  join dim_building_users  bu on db.id = bu.building_id
                  join dim_users as du on du.id = bu.user_id  
                  where bm.type = 'BuildingSummaryMetricsPastThirtyRollingDays' and(bm.date = CURRENT_DATE - 2 OR bm.date = DATEADD(YEAR, -1, CURRENT_DATE - 2)) and du.first_name ilike 'y' and db.name ilike 'x' order by bm.building_id;"

  - name: Building Performance for past/last full month
    question: How did X's buildings perform in the last or last full month?
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded
        FROM fact_building_summary_metrics AS bm
                  JOIN dim_buildings AS db ON bm.building_id = db.id
                  join fact_buildings as fb on db.id = fb.id
                  and fb.active = true
                  join dim_building_users  bu on db.id = bu.building_id
                  join dim_users as du on du.id = bu.user_id  
                  where (bm.type = 'BuildingSummaryMetricsFullMonth'
                  and ( bm.date = DATEADD(DAY, -1, DATE_TRUNC('MONTH', CURRENT_DATE)) )) and du.first_name ilike 'x' order by bm.building_id;"

  - name: Compare Building Performance for past/last full month
    question: Compare x's buildings perform in the last or last full month?my nameis y
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded
         FROM fact_building_summary_metrics AS bm
                  JOIN dim_buildings AS db ON bm.building_id = db.id
                  join fact_buildings as fb on db.id = fb.id
                  and fb.active = true
                  join dim_building_users  bu on db.id = bu.building_id
                  join dim_users as du on du.id = bu.user_id  
                  where (bm.type = 'BuildingSummaryMetricsFullMonth'
                  and ( bm.date = DATEADD(DAY, -1, DATE_TRUNC('MONTH', CURRENT_DATE)) OR bm.date
            = DATEADD(DAY, -1, DATEADD(YEAR, -1, DATE_TRUNC('MONTH', CURRENT_DATE)))
            )) and du.first_name ilike 'y' and db.name ilike 'x' order by bm.building_id;"    

  - name: Building Performance for rolling or current year
    question: How did X's buildings perform in the rolling or current year?
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded
        FROM fact_building_summary_metrics AS bm
                  JOIN dim_buildings AS db ON bm.building_id = db.id
                  join fact_buildings as fb on db.id = fb.id
                  and fb.active = true
                  join dim_building_users  bu on db.id = bu.building_id
                  join dim_users as du on du.id = bu.user_id  
                  where bm.type = 'BuildingSummaryMetricsPastRollingYear' and(bm.date = CURRENT_DATE - 2 ) and db.name ilike 'x' order by bm.building_id;"

  - name: Compare Building Performance for rolling or current year
    question: Compare x's buildings perform in the rolling or current year?
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded
        FROM fact_building_summary_metrics AS bm
                  JOIN dim_buildings AS db ON bm.building_id = db.id
                  join fact_buildings as fb on db.id = fb.id
                  and fb.active = true
                  join dim_building_users  bu on db.id = bu.building_id
                  join dim_users as du on du.id = bu.user_id  
                  where bm.type = 'BuildingSummaryMetricsPastRollingYear' and(bm.date = CURRENT_DATE - 2 OR bm.date = DATEADD(YEAR, -1, CURRENT_DATE - 2)) and du.first_name ilike 'y' and db.name ilike 'x' order by bm.building_id;"      

  - name: Building Performance for till the date or year to date
    question: How did X's buildings perform in the till current date this year?
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded
        FROM fact_building_summary_metrics AS bm
                  JOIN dim_buildings AS db ON bm.building_id = db.id
                  join fact_buildings as fb on db.id = fb.id
                  and fb.active = true
                  join dim_building_users  bu on db.id = bu.building_id
                  join dim_users as du on du.id = bu.user_id  
                  where bm.type = 'BuildingSummaryMetricsYearToDate' and(bm.date = CURRENT_DATE - 2) and db.name ilike 'x' order by bm.building_id;"
       
  - name: Building Performance for last quarter
    question: How did X's buildings perform in the last/full quarter?
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded
        FROM fact_building_summary_metrics AS bm
                  JOIN dim_buildings AS db ON bm.building_id = db.id
                  join fact_buildings as fb on db.id = fb.id
                  and fb.active = true
                  join dim_building_users  bu on db.id = bu.building_id
                  join dim_users as du on du.id = bu.user_id  
                  where bm.type = 'BuildingSummaryMetricsFullQuarter' 
                  AND (
      bm.date = DATEADD(DAY, -1, DATE_TRUNC('QUARTER', CURRENT_DATE()))
      )  
                      and du.first_name ilike 'x' order by bm.building_id;"

  - name: Compare Building Performance for last quarter
    question: Compare x's buildings perform in the last/full quarter for user y?
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded
        FROM fact_building_summary_metrics AS bm
                  JOIN dim_buildings AS db ON bm.building_id = db.id
                  join fact_buildings as fb on db.id = fb.id
                  and fb.active = true
                  join dim_building_users  bu on db.id = bu.building_id
                  join dim_users as du on du.id = bu.user_id  
                  where bm.type = 'BuildingSummaryMetricsFullQuarter' 
                  AND (
      BM.DATE =  DATEADD(DAY, -1, DATE_TRUNC(YEAR, DATEADD(QUARTER, -1, CURRENT_DATE()))) OR bm.date = DATEADD(DAY, -1, DATE_TRUNC('QUARTER', CURRENT_DATE()))
      ) 
                      and du.first_name ilike 'y' and db.name ilike 'x' order by bm.building_id;"                        
       
  - name: ###Compare 2 or more Building Performance for specific period
    question: Compare x and y buildings performonce in the last/full quarter?
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded
        FROM fact_building_summary_metrics AS bm
                  JOIN dim_buildings AS db ON bm.building_id = db.id
                  join fact_buildings as fb on db.id = fb.id
                  and fb.active = true
                  join dim_building_users  bu on db.id = bu.building_id
                  join dim_users as du on du.id = bu.user_id  
                  where bm.type = 'BuildingSummaryMetricsFullQuarter' 
                  AND (
      BM.DATE =  DATEADD(DAY, -1, DATE_TRUNC(YEAR, DATEADD(QUARTER, -1, CURRENT_DATE()))) OR bm.date = DATEADD(DAY, -1, DATE_TRUNC('QUARTER', CURRENT_DATE()))
      ) 
                      and db.name IN ('x', 'y') order by bm.building_id;" 
                            
  - name: Building Performance for since it was included or since installing cortex
    question: How did building y carried out since it was included or since installing cortex? for user X
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded
        FROM fact_building_summary_metrics AS bm
                  JOIN dim_buildings AS db ON bm.building_id = db.id
                  join fact_buildings as fb on db.id = fb.id
                  and fb.active = true
                  join dim_building_users  bu on db.id = bu.building_id
                  join dim_users as du on du.id = bu.user_id  
                  WHERE (bm.type = 'BuildingSummaryMetricsYearToDate' and (
                  (MONTH(bm.date) = 12
                  AND DAY(bm.date) = 31) or bm.date = current_date-2))
                  and du.first_name ilike 'x' order by bm.building_id;"

  - name: Building Performance to provide best and worst building
    question:compare all buildings performance of user x and give best and worst building for last quarter
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded,
        RANK() OVER (PARTITION BY YEAR(date)  ORDER BY electric_consumption_total_savings_percent DESC NULLS LAST) AS electric_rank,
        FROM fact_building_summary_metrics AS bm
                  JOIN dim_buildings AS db ON bm.building_id = db.id
                  join fact_buildings as fb on db.id = fb.id
                  and fb.active = true
                  join dim_building_users  bu on db.id = bu.building_id
                  join dim_users as du on du.id = bu.user_id  
                  where bm.type = 'BuildingSummaryMetricsFullQuarter' 
                  AND (
      bm.date = DATEADD(DAY, -1, DATE_TRUNC('QUARTER', CURRENT_DATE()))
      )  
                      and du.first_name ilike 'x' order by bm.building_id;"

  - name: Building Performance to provide best and worst building 
    question:Which building performed well compared to other buildings for the associated user x over last quarter?
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded,
        RANK() OVER (PARTITION BY YEAR(date)  ORDER BY electric_consumption_total_savings_percent DESC NULLS LAST) AS electric_rank,
          FROM fact_building_summary_metrics AS bm
                  JOIN dim_buildings AS db ON bm.building_id = db.id
                  join fact_buildings as fb on db.id = fb.id
                  and fb.active = true
                  join dim_building_users  bu on db.id = bu.building_id
                  join dim_users as du on du.id = bu.user_id  
                  where bm.type = 'BuildingSummaryMetricsFullQuarter' 
                  AND (
      bm.date = DATEADD(DAY, -1, DATE_TRUNC('QUARTER', CURRENT_DATE()))
      )  
                      and du.first_name ilike 'x' order by bm.building_id;" 

  - name: Building Performance in specific Portfolio
    question:how my buildings in x porfolio working this year?  my name is y
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded   
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
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded
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
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded
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
    sql: "SELECT bm.building_id,db.name AS building_name,DATEADD(DAY,-(bm.days_included),bm.date) AS from_date,bm.date AS end_date,bm.days_included,ROUND(bm.electric_consumption_total_savings_kwh) AS electric_consumption_total_savings_kwh,ROUND(bm.electric_consumption_total_actual_kwh) AS electric_consumption_total_actual_kwh,ROUND(electric_consumption_total_baseline_kwh) AS electric_consumption_total_baseline_kwh,ROUND(bm.steam_consumption_total_savings_mlbs) AS steam_consumption_total_savings_mlbs,ROUND(bm.steam_consumption_total_actual_mlbs) AS steam_consumption_total_actual_mlbs,ROUND(bm.steam_consumption_total_baseline_mlbs) AS steam_consumption_total_baseline_mlbs,ROUND(bm.gas_consumption_total_savings_therms) AS gas_consumption_total_savings_therms,ROUND(bm.gas_consumption_total_actual_therms) AS gas_consumption_total_actual_therms,ROUND(bm.gas_consumption_total_baseline_therms) AS gas_consumption_total_baseline_therms,ROUND(bm.total_carbon_savings_tons_co2) AS total_carbon_savings_tons_co2,ROUND(bm.electric_consumption_total_savings_percent) AS electric_consumption_total_savings_percent,ROUND(bm.steam_consumption_total_savings_percent) AS steam_consumption_total_savings_percent,ROUND(bm.gas_consumption_total_savings_percent) AS gas_consumption_total_savings_percent,ROUND(bm.hdd_days) AS hdd_days,ROUND(bm.cdd_days) AS cdd_days,ROUND(bm.occupancy) AS occupancy,ROUND(fb.total_sqft) AS total_sqft,ROUND(bm.START_TIME_LATE_START_PERCENT) AS START_TIME_LATE_START_PERCENT,ROUND(bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT) AS START_TIME_FOLLOWED_RECOMMENDATION_PERCENT,ROUND(bm.START_TIME_EARLY_START_PERCENT) AS START_TIME_EARLY_START_PERCENT,ROUND((bm.START_TIME_LATE_START_PERCENT*bm.days_included)/100) AS START_TIME_LATE_START_DAYS,ROUND((bm.START_TIME_FOLLOWED_RECOMMENDATION_PERCENT*bm.days_included)/100) AS START_TIME_FOLLOWED_RECOMMENDATION_DAYS,ROUND((bm.START_TIME_EARLY_START_PERCENT*bm.days_included)/100) AS START_TIME_EARLY_START_DAYS,CASE WHEN days_included<(MAX(bm.days_included) OVER ())/2 THEN TRUE ELSE FALSE END AS excluded
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
     
  - name: Energy intesity of building
    question:Calculate the energy intensity of building x in last year
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
        where db.name ilike 'x' and (bm.type = 'BuildingSummaryMetricsYearToDate' and(MONTH(bm.date) = 12
        AND DAY(bm.date) = 31 and( year(bm.date)= year(current_date)-1 )))
        GROUP BY
          bm.building_id,
          dp.name,
          db.name,
          bm.type,
          bm.date;" 
                
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
    question:Calculate the energy intensity for all buildings in x's portfolio 
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
            bm.date = CURRENT_DATE - 2
          )
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