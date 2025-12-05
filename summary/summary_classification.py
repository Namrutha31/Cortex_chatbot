prompt_classify= f"""
Classify the following user input into one of these three categories: improvements, case0,case1, case2, case3, case4,case5,case6,case7.
### Instructions:
1. Strictly classify based on the below ### Data and ### User Input. 
2. Understand the full context of the user input before classifying it. Do not classify based on isolated keywords.
3. Follow a strict classification approach based on the relationships between improvements,case0,case1,case2,case3,case4,case5,case6,case7.
4. Ensure correct classification by considering the below criteria:

### Classification Criteria:

- **improvements**: 
    Classify as improvements if the input refers to:
        - asks for building improvements, with having only worst word.
    Examples:
        - **"Which building should I focus on for improvements?"**
        - **"Where could we be operating better?"** 
-**case0**:
    Classify as case0 if the input refers to:
        - If the user query does not match any predefined cases but still requires a relevant response based on available data.
        - If the query is for users,portfolios,buildings or anyother ata which doesnot have the columns or conditions to satisfy.
        - Use this case if the query does not match any of the other cases but still requires a response based on available data. 
    Examples:
        - "Give me an overview of energy consumption trends."  
        - "Summarize key insights from my portfolio." 
        - **"How many buildings are in the Nuveen portfolio?"**
        - **"List all users managing portfolios in the system."**
        - **"What is the total energy consumption of all buildings?"**
        - **"How has carbon emissions changed in the last five years?"** 
        - **"How are the recommendations folllowed by Wendi Gibb portfolio."**
- **case1**:
    Classify as case1 if the input refers to:
        - If the query includes building/portfolio performance from "since installation," "since installing Cortex," "from installing," or similar phrases.
        - Data have multiple years on same portolio or building with the metrics.
        - The query looks for **year-wise trends** since the system was installed. 
        - If the data consits of multiple years more than 2 years.
    Examples:
        - **"How has consumption changed since installing Cortex in portfolio?"**
        - **"Since installation, what are the year-wise trends in building?"**
        - **"How is my portfolio Station Place working since its included, I am Chris"**
- **case2**:
    Classify as case2 if the input refers to:
        - Year-to-Year Comparison; If the query includes "compare to x year" and multiple years are present.
        - Only if the data has Single Portfolio or Building in the data with two years data for performance.
        - If two portfolios or buildings with two years then use this with comparison of the building among the years.
        - Used when the user asks for a direct comparison between two specific years for performance.
    Examples:
        - **"Compare consumption in  portfolio for last year."**
        - **"How did the building perform last year compared to the x year?"**
        - **"How did my portfolio X perform compared to last year?"**
- **case3**:
    Classify as case3 if the input refers to:
        - Multiple Portfolios or Buildings with Single Year in the data for performance
        - Strictly choose this category, when the query is related to **best and worst words.**
        - If the query requests performance comparisons across multiple portfolios or buildings **for a single year**
        - If multiple buildings/portfolios are present in the dataset with a single date, trigger this case.
        - Use this case for queries like **"Best and Worst Performers"**, **"Which performed better"**, **"Performance ranking of buildings/portfolios"**.
    Examples:
        - **"Which buildings performed best in the portfolio x for user ?"**
        - **"Which building in stahl portfolio performed the best"**
        - **"Rank the top 5 portfolios based on carbon emissions for this year."**
        - **"Which portfolio had the best and worst performance in last month for user X."**
        - **"Rank the top 5 buildings based on carbon emissions."**
        - **"How did all buildings in the X portfolio perform last quarter for user Y?"**
- **case4**:
    Classify as case4 if the input refers to:
        - Single Year Summary with Single Portfolio/Building in the data retrived for performance  
        - If the query asks for **performance of a single portfolio or building for one year**. 
        - If the query asks any details of performance related to steam,gas,electricity,operations,emissions for**single portfolio or building in data**.
    Examples:
        - **"How did the portfolio perform last month for user Alejandro"**
        - **"How did my portfolio X perform last year?**
        - **"How did the portfolio(s) perform in the last year for user Wendi gibb?"**
- **case5**:
    Classify as case5 if the input refers to:
        - Multiple Portfolios or Buildings performance comparision Over Two Years for performance
        - If the query asks for **a comparison of multiple portfolios/buildings across two years, quarters, or months**.
        - **"Compare all buildings performance for last year/quarter/month"**
        - **"Compare the buildings in X portfolio for last year/quarter/month"**
        - **"Compare last year vs previous year, last quarter vs previous quarter, last month vs previous month"**
        - **"Performance change from last year/quarter/month"**.
    Examples:
        - **"Compare all buildings in the Rockpoint portfolio performance between 2024 and 2023 for user Chris."**
        - **"Compare all portfolios performance for user mike in last quarter"**
- **case6**: 
    Classify as case6 if the input refers to:
        - Energy Intensity
        - If the query asks for energy intensity calculations.
    Examples:
        - **"What is the energy intensity of buildings in the Rockpoint portfolio for 2024?"**
        - **"How does the energy intensity of the building 277 Park compare over the past three years?"**
        - **Which buildings have the highest energy intensity? in stahl portfolio**
- **case7**: 
    Classify as case7 if the input refers to:
        - Peak demand
        - If the query asks for demand peak calculations.
    Examples:
        - **"When did I set my highest peak in 2024?"**
        - **"What day did I set my peak in each month in 2024?"**  
        - **"What is power/steam/gas peak demand(s) for user x"**
    
    
### Expected Output:
Only return one of these category names: improvements,case0,case1,case2,case3,case4,case5,case6,case7. No explanations or additional text.
"""
