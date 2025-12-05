query_prompt = f"""
Classify the following user input into one of these three categories: dailystat, portfolio, building, measurement, demand, improvements.
### Instructions:
1. Understand the full context of the user input before classifying it. Do not classify based on isolated keywords.
2. Follow a strict classification approach based on the relationships between portfolios, buildings, and daily statistics.
3. Ensure correct classification by considering the scope:
    - Users are connected to multiple portfolios.
    - A portfolio contains multiple buildings.
    - Each building has its own daily statistics.
4. If the users question refers to the performance of a **building** or **portfolio** for the full duration of one of these [RollingYear,FullQuarter,NinetyRollingDays,ThirtyRollingDays,FullMonth,YearToDate] cumulative periods, classify it as `building` or `portfolio`. 
5. If the users question focuses on a specific day, or a non-cumulative breakdown within a cumulative period, classify it as `dailystat`.
6. If the users question refers to the performance of all or single building in specific portfolio, then strictly choose **building**.
### Classification Criteria:
- **Dailystat**:
    Classify as dailystat if the input refers to:
        - Daily operational or statistical data of buildings.
        - A comparison of building statistics on a single specific date (e.g., today, yesterday, or a given date).
        - Any request focusing on the daily performance of buildings.
        - If the query asks for insights **within** a cumulative period.
        - If the time period mentioned in the question is **less than one month** (e.g., weekly, daily), always classify as `dailystat`.
    Examples:
        - "Show todays building stats."
        - "Compare yesterdays stats with todays."
        - "What were the daily readings for Building X on Jan 5?"
        - "Identify the days when it was high/low?" 
        - "Peak consumption"
        - "What was my buildings highest energy consumption day in last month?"

- **Portfolio**:
    Classify as portfolio if the input refers to:
        - The performance of a portfolio as a whole over a specific time period (not just daily stats).
        - A comparison of portfolios (e.g., "how are we performing compared to others?").
        - Any reference to portfolio metrics, trends, or evaluations.
        - For cumulative performance of a portfolio over an entire cumulative period. 
    Examples:
        - "How is my portfolio performing this month?"
        - "Compare our portfolio against similar ones."
        - "What are the portfolio-level efficiency trends for the last quarter?"

- **Building**:
    Classify as building if the input refers to:
        - The performance of a specific building or multiple buildings within a single portfolio over a specific period (not daily stats).
        - Any request for building-related metrics (not daily operations).
        - If the users question refers to the performance of all or single building in specific portfolio, then strictly choose **building**.
        - Comparison of buildings within a portfolio.
        - For cumulative performance of a building over an entire cumulative period. 
    Examples:
        - "How did Building X perform this quarter?"
        - "Compare all buildings in Portfolio A for the last month."
        - "Which buildings had the worst efficiency last week?"
        - "compare all buildings in X portfolio for 2023 vs 2024"
        - "how did buildings in X portfolio performed compare to 2024"

- **Measurement**:
    Classify as measurement if the input refers to:
        - The latest or sensor measurement of a specific building within a single portfolio over a specific period.
        - Any request for building-related to sensors. 
    Examples:
        - "What are the latest sensor measurements for X for Y?" 

- **Demand**:
    Classify as demand if the input refers to:
        - The demand, peak demand, max demand of a specific building within a single portfolio over a specific period.
        - Any request for building-related to demand. 
    Examples:
        - "When did I set my peak on date y? for user x"        
- **Improvements**:
    Classify as improvements if the input refers to:
        - If user asks for, where he need to improve
        - Any request for building-related for improvements. 
    Examples:
        - **"Which building should I focus on for improvements?"**
        - **"Where could we be operating better?"**      


### Expected Output:
Only return one of these category names: dailystat, portfolio, building, measurement, demand or improvements. No explanations or additional text.
"""
