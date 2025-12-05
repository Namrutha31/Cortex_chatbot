prompt_measurement = """
 ###Instruction:
 In interpreation of question, do not change any words or context, or do not assume to add anything.
   **Do not alter the meaning or context in your interpretation of question, if the user question is related to (best/worst,poor/best performance, ineffective, inefficiency) do not interpret only negative values, include all values along with all savings columns, do not reside on 1 or 2 columns; keep it exactly as it is.**
   **Strictly round off all values to 0 decimal places, except for energy intensity queries.**    
    **Time Zone**:
        - Strictly add time_zone column, for all queries related to table FACT_SENSOR_LATEST_MEASUREMENTS    
   **If the user query matches (or closely resembles) any of the verified queries, strictly use the verified query as a reference to formulate the response.**   
###Generate an SQL query based on the following verified queries;
verified_queries:
  - name: Building Latest measurement of sensor x and building y for user z 
    question: What are the latest sensor measurements for X for Y?

    sql: "SELECT
          fslm.id,
          fslm.BUILDING_ID, 
          fslm.BUILDING_SENSOR_NAME, 
          fslm.BUILDING_SENSOR_MOST_RECENT_MEASURED_AT, 
          fslm.BUILDING_SENSOR_MEASUREMENT_TYPE, 
          fslm.MEASURED_AT, 
          ROUND(fslm.MEASUREMENT) AS MEASUREMENT, 
          fslm.DISPLAY_MEASUREMENT_UNIT, fslm.time_zone
      FROM FACT_SENSOR_LATEST_MEASUREMENTS AS fslm
      JOIN FACT_BUILDINGS AS fb ON fb.id = fslm.BUILDING_ID
      JOIN DIM_BUILDINGS AS db ON db.id = fb.id
      JOIN DIM_BUILDING_USERS AS dbu ON dbu.BUILDING_ID = db.id
      JOIN DIM_USERS AS du ON du.id = dbu.USER_ID
      where du.first_name ilike 'z' and fslm.building_sensor_name ilike 'x' and db.name ilike 'y';"
 
"""