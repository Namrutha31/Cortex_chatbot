# Imports essential libraries:
# streamlit: For building a web-based UI.
# pandas: For data manipulation and analysis.
# requests: For making API calls.
# snowflake.connector: For connecting to a Snowflake database.
# json: For handling JSON data.
# typing: Provides type hints for better code clarity (Any, Dict, Optional).
import streamlit as st
import pandas as pd
import requests
import snowflake.connector
import json
from typing import Any, Dict, Optional
# Imports prompt templates from different modules to generate sql query:
# building: sql prompts related to building queries
# portfolio: sql prompts related to portfolio queries
# dailystat: sql prompts related to dailystat queries
# measurement: sql prompts related to latest measurement queries
# demand: sql prompts related to peak demand queries
# improvements: sql prompts related to improvements queries
# query: prompts to classify user_input into different cases
from prompts.building import prompt_building
from prompts.portfolio import prompt_portfolio
from prompts.dailystat import prompt_dailystat
from prompts.measurement import prompt_measurement
from prompts.demand import prompt_demand
from prompts.improvements import prompt_improvements
from prompts.query import query_prompt
# Imports configuration settings:
# contains API keys, database credentials, and other environment variables.
from config import settings
# Imports various summary-related prompts:
# Each summary_caseX module contains predefined prompts for different scenarios.
# prompt_classify classify user input into different summary cases.
from summary.summary_case0 import case0_prompt
from summary.summary_case1 import case1_prompt 
from summary.summary_case2 import case2_prompt
from summary.summary_case3 import case3_prompt
from summary.summary_case4 import case4_prompt
from summary.summary_case5 import case5_prompt
from summary.summary_case6 import case6_prompt
from summary.summary_case7 import case7_prompt
from summary.improvements import improvements_prompt
from summary.summary_classification import prompt_classify
from summary.default_summary import sum_llm
# Imports altair:
# A visualization library for creating interactive charts in Streamlit.
import altair as alt


# Establishes a Snowflake connection in Streamlit's session state to avoid redundant logins.
if "CONN" not in st.session_state:
    st.session_state.CONN = None

if st.session_state.CONN is None:
    st.session_state.CONN = snowflake.connector.connect(
        user=settings.user,
        password=settings.password,
        account=settings.account,
        host=settings.HOST,
        port=settings.port,
        warehouse=settings.warehouse,
        role=settings.role,
    )



def execute_with_retries(func, prompt, retries=3):
    """Executes a function with retries, retrying up to 'retries' times before raising an exception on failure."""
    attempt = 0
    while attempt < retries:
        try:
            return func(prompt)
        except Exception as e:
            attempt += 1
            if attempt == retries:
                raise Exception(f"All {retries} attempts failed.") from e
def is_verified_query_matched(prompt: str) -> bool:
    """
    Checks if a user query matches a verified query in the semantic model.
    Returns True if the query is verified, otherwise False.
    """
    test_request_body = {
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
        "semantic_model_file": f"@{settings.DATABASE}.{settings.SCHEMA}.{settings.STAGE}/{settings.FILE}",
    }
    try:
        response = requests.post(
            url=f"https://{settings.HOST}/api/v2/cortex/analyst/message",
            json=test_request_body,
            headers={
                "Authorization": f'Snowflake Token="{st.session_state.CONN.rest.token}"',
                "Content-Type": "application/json",
            },
        )

        if response.status_code == 200:
            
            response_data = response.json()

            for content in response_data.get("message", {}).get("content", []):
                if content.get("type") == "sql":
                    
                    confidence_data = content.get("confidence", {})
                    if confidence_data.get("verified_query_used") is not None:
                        
                        return True
            return False
        else:
            raise Exception(f"API Error: Status code {response.status_code}, Response: {response.text}")

    except Exception as e:
        print(f"Error in is_verified_query_matched: {e}")


def send_message(prompt: str) -> Dict[str, Any]:
    """Calls the REST API and returns the response."""
    
    dynamic_prompt = get_dynamic_prompt(prompt)
    complete_prompt = f"""###USER QUERY:"{prompt}"\n\n{dynamic_prompt}"""

    request_body = {
        "messages": [{"role": "user", "content": [{"type": "text", "text": complete_prompt}]}],
        "semantic_model_file": f"@{settings.DATABASE}.{settings.SCHEMA}.{settings.STAGE}/{settings.FILE}",
    }
    
    resp = requests.post(
        url=f"https://{settings.HOST}/api/v2/cortex/analyst/message",
        json=request_body,
        headers={
            "Authorization": f'Snowflake Token="{st.session_state.CONN.rest.token}"',
            "Content-Type": "application/json",
        },
    )
    request_id = resp.headers.get("X-Snowflake-Request-Id")
    if resp.status_code < 400:
        return {**resp.json(), "request_id": request_id}  
    else:
        st.session_state.messages.pop()
        raise Exception(
            f"Failed request (id: {request_id}) with status {resp.status_code}: {resp.text}"
        )
def classify_input_with_conditions(user_input: str) -> str:
    """Classifies user input into categories using an LLM, guided by conditions."""
    sanitized_input = user_input.replace("'", "''")
    prompt = query_prompt
    sql_query = f"""
        SELECT SNOWFLAKE.CORTEX.COMPLETE(
            'mistral-large2',
            [
                {{
                    'role': 'system',
                    'content': '{prompt}'
                }},
                {{
                    'role': 'user',
                    'content': '### User Input:{sanitized_input}'
                }}
            ],
            {{'temperature': 0.4, 'max_tokens': 1000}}
        ) AS category
    """

    

    try:
        classification_result = pd.read_sql(sql_query, st.session_state.CONN)
        category = classification_result.iat[0, 0].strip().lower()
        response_json = json.loads(category)
        messages_content = response_json.get("choices", [{}])[0].get("messages", "").strip()              
        return messages_content
    except Exception as e:
        st.error(f"Error classifying user input: {e}")
        return "portfolio"

def get_dynamic_prompt(user_input: str) -> str:
    """Get the appropriate prompt based on LLM classification of user input."""
    category = classify_input_with_conditions(user_input)
    if category == "dailystat":
        return prompt_dailystat
    elif category == "portfolio":
        return prompt_portfolio
    elif category == "building":
        return prompt_building
    elif category == "measurement":
        return prompt_measurement
    elif category == "demand":
        return prompt_demand
    elif category == "improvements":
        return prompt_improvements
    else:
        return prompt_portfolio

def classify_summary_with_conditions(user_input,data):
    """Classifies user input and data into different summary cases using an LLM, guided by conditions."""
    sanitized_input = user_input.replace("'", "''")
    prompt = prompt_classify
    sql_query = f"""
        SELECT SNOWFLAKE.CORTEX.COMPLETE(
            'mistral-large2',
            [
                {{
                    'role': 'system',
                    'content': '{prompt}'
                }},
                {{
                    'role': 'user',
                    'content': '### User Input:{sanitized_input}
                                ### Data:{data}'
                }}
            ],
            {{'temperature': 0.4, 'max_tokens': 1000}}
        ) AS category
    """

    

    try:
        classification_result = pd.read_sql(sql_query, st.session_state.CONN)
        category = classification_result.iat[0, 0].strip().lower()
        response_json = json.loads(category)
        messages_content = response_json.get("choices", [{}])[0].get("messages", "").strip()               
        return messages_content
    except Exception as e:
        st.error(f"Error classifying user input: {e}")
    return "default"

def get_dynamic_summary_prompt(category):
    """Get the appropriate summary prompt based on LLM classification of user input."""
    category = category
    if category == "case0":
        return case0_prompt
    if category == "case1":
        return case1_prompt
    elif category == "case2":
        return case2_prompt
    elif category == "case3":
        return case3_prompt
    elif category == "case4":
        return case4_prompt
    elif category == "case5":
        return case5_prompt
    elif category == "case6":
        return case6_prompt
    elif category == "case7":
        return case7_prompt    
    elif category == "improvements":
        return improvements_prompt
    elif category == "default":
        return sum_llm
    
def generate_data_summary(user_input: str, sql_api: str) -> str:
    """Generates a summarized response from SQL query results by sanitizing input, executing the query, classifying the data, formatting the summary prompt, and parsing the final response.  """
    sanitized_input = user_input.replace("'", "''").strip()
    query = f"""
        SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))::STRING as Output 
        FROM ({sql_api})
    """
    data = pd.read_sql(query, st.session_state.CONN)
    data = data.iat[0, 0]
    data= data.replace("'","")
    category = classify_summary_with_conditions(user_input,data)
    sum_final = get_dynamic_summary_prompt(category)
    sql_sum= sum_final.format(sanitized_input=sanitized_input,data=data)
    try:
        DataSummary = pd.read_sql(sql_sum, st.session_state.CONN)
        response = DataSummary.iat[0, 0]
        response_json = json.loads(response)
        summary = response_json.get("choices", [{}])[0].get("messages", "").strip()
        summary= summary.replace("$", "\$")
        return summary
    except Exception as e:
        st.error(f"Error generating data summary: {e}")
        return ""

        
def display_content(
    content: list,
    request_id: str = None,
    message_index: Optional[int] = None,
    user_input: str = None
) -> None:
    """Displays content (text, suggestions, SQL query, results, or summary) with interactive elements, executes SQL queries, handles errors, and renders data in tables or charts, while also providing options to display request ID and summaries.
"""
    message_index = message_index or len(st.session_state.messages)
    if request_id:
        with st.expander("Request ID", expanded=False):
            st.markdown(request_id)
    
    for item in content:
        if item["type"] == "text":
            st.markdown(item["text"], unsafe_allow_html=True)
        elif item["type"] == "suggestions":
            with st.expander("Suggestions", expanded=True):
                for suggestion_index, suggestion in enumerate(item["suggestions"]):
                    if st.button(suggestion, key=f"{message_index}_{suggestion_index}"):
                        st.session_state.active_suggestion = suggestion
        elif item["type"] == "sql":
            with st.expander("SQL Query", expanded=False):
                st.code(item["statement"], language="sql")
            with st.expander("Results", expanded=True):
                sql_api = item["statement"].replace(";", "")
                data_tab, chart_tab = st.tabs(["Data 📄", "Chart 📈"])
                try:
                    df = pd.read_sql(sql_api, st.session_state.CONN)
                    if not df.empty:
                            if not any(c["type"] == "summary" for c in content):
                                summary = generate_data_summary(user_input, sql_api)
                                content.append({"type": "summary", "text": summary})
                            with data_tab:
                                st.dataframe(df)
                            with chart_tab:
                                display_charts_tab(user_input, df, message_index)
                    else:
                        st.warning("No data found for the query.")
                except Exception as e:
                    st.error(f"Error running SQL query: {e}")
        elif item["type"] == "summary":
            with st.expander("Summary", expanded=True):
                st.write(item["text"], unsafe_allow_html=True)

            message = st.session_state.messages[message_index] if message_index < len(st.session_state.messages) else {}
            summary = item["text"]

def process_message(user_input: str) -> None:
    """Processes user input by appending it to session messages, displaying it in the chat, executing response generation with retries, and displaying the assistant's response content.
"""
    st.session_state.messages.append(
        {"role": "user", "content": [{"type": "text", "text": user_input}]}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            response = execute_with_retries(send_message, prompt=user_input)
            request_id = response.get("request_id", "Unknown")
            content = response.get("message", {}).get("content", [])

            st.session_state.messages.append(
                {"role": "analyst", "content": content, "request_id": request_id}
            )
            display_content(content=content, request_id=request_id, user_input=user_input)


def create_chart(data: pd.DataFrame, x_col: str, measures: list, multiple_years: bool, is_single_entity: bool) -> alt.Chart:
    """Helper function to create bar charts with consistent styling"""
    if data is None or measures is None or len(measures) == 0:
        st.error("No valid data or measures provided for chart creation.")
        return None  # Early return if data or measures are invalid

    try:
        if is_single_entity:
            # For single portfolio/building: one chart with all measures
            plot_data = pd.melt(
                data,
                id_vars=[x_col],
                value_vars=measures,
                var_name='Measure',
                value_name='Value'
            )
            
            # Create chart with x_col as x-axis and all measures
            chart = alt.Chart(plot_data).encode(
                x=alt.X(f'{x_col}:N', title=x_col.replace('_', ' ').title()),
                y=alt.Y('Value:Q', 
                       title='Measure Values',
                       scale=alt.Scale(zero=True)),
                color=alt.Color('Measure:N', 
                              title='Measures',
                              legend=alt.Legend(orient='top')),
                tooltip=[
                    alt.Tooltip(x_col, title=x_col.replace('_', ' ').title()),
                    alt.Tooltip('Measure:N', title='Measure'),
                    alt.Tooltip('Value:Q', title='Value', format=',.2f')
                ]
            ).mark_bar()
            
            title = f"Measures Comparison for {data[x_col].iloc[0]}"
            
        else:
            # For multiple portfolios/buildings
            if multiple_years:
                # Multiple measures, multiple years case
                plot_data = pd.melt(
                    data,
                    id_vars=[x_col, 'YEAR'],  # Include YEAR for multiple years
                    value_vars=measures,
                    var_name='Measure',
                    value_name='Value'
                )
                
                chart = alt.Chart(plot_data).encode(
                    x=alt.X(f'{x_col}:N', 
                           title=x_col.replace('_', ' ').title(),
                           axis=alt.Axis(
                               labelAngle=45,
                               labelLimit=200,
                               labelOverlap=False
                           )),
                    y=alt.Y('Value:Q', 
                           title='Measure Values',
                           scale=alt.Scale(zero=True)),
                    color=alt.Color('Measure:N', 
                                  title='Measures',
                                  legend=alt.Legend(orient='top')),
                    column=alt.Column('YEAR:N', title='Year'),  # Create separate charts for each year
                    tooltip=[
                        alt.Tooltip(x_col, title=x_col.replace('_', ' ').title()),
                        alt.Tooltip('Measure:N', title='Measure'),
                        alt.Tooltip('Value:Q', title='Value', format=',.2f')
                    ]
                ).mark_bar()
                
                title = f"Measures Comparison by {x_col.replace('_', ' ').title()} Across Years"
            else:
                # Multiple measures, single year case
                plot_data = pd.melt(
                    data,
                    id_vars=[x_col],
                    value_vars=measures,
                    var_name='Measure',
                    value_name='Value'
                )
                
                chart = alt.Chart(plot_data).encode(
                    x=alt.X(f'{x_col}:N', 
                           title=x_col.replace('_', ' ').title(),
                           axis=alt.Axis(
                               labelAngle=45,
                               labelLimit=200,
                               labelOverlap=False
                           )),
                    y=alt.Y('Value:Q', 
                           title='Measure Values',
                           scale=alt.Scale(zero=True)),
                    color=alt.Color('Measure:N', 
                                  title='Measures',
                                  legend=alt.Legend(orient='top')),
                    tooltip=[
                        alt.Tooltip(x_col, title=x_col.replace('_', ' ').title()),
                        alt.Tooltip('Measure:N', title='Measure'),
                        alt.Tooltip('Value:Q', title='Value', format=',.2f')
                    ]
                ).mark_bar()
                
                title = f"Measures Comparison by {x_col.replace('_', ' ').title()}"

        # Add chart styling with increased width
        width = 800
        
        styled_chart = chart.properties(
            width=width,
            height=400,
            title=alt.TitleParams(
                text=title,
                fontSize=16,
                anchor='middle'
            )
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        ).configure_title(
            fontSize=16,
            anchor='middle'
        )
        
        # Add zoom and pan interactions
        styled_chart = styled_chart.configure_view(
            continuousWidth=width,
            continuousHeight=400,
        ).interactive()
            
        return styled_chart
        
    except Exception as e:
        st.error(f"Error in create_chart: {str(e)}")
        return None

def display_charts_tab(user_input: str, df: pd.DataFrame, message_index: int) -> None:
    try:
        """Generates interactive charts for metrics from a given DataFrame, including options to select and compare different measures, handle multiple years, and display relevant visualizations.
"""
        if len(df.columns) < 2:
            st.write("At least 2 columns are required")
            return
            
        # Clean column names and convert to uppercase
        df.columns = df.columns.str.upper().str.strip()
        
        # Extract year from DATE column
        if 'END_DATE' in df.columns:
            df['END_DATE'] = pd.to_datetime(df['END_DATE'])
            df['YEAR'] = df['END_DATE'].dt.year
            df = df.dropna(subset=['END_DATE'])
        else:
            st.warning("No DATE column found in the data")
            return
        
        # Separate kWh measures from other measures
        kwh_columns = [col for col in df.columns 
                      if col.endswith('_TOTAL_SAVINGS_KWH') and not df[col].isnull().all()]
        
        other_columns = [col for col in df.columns 
                        if any(col.endswith(suffix) for suffix in 
                            ('_SAVINGS_DOLLARS', '_SAVINGS_TONS_CO2', '_SAVINGS_THERMS', '_SAVINGS_MLBS')) 
                        and not df[col].isnull().all()]
        
        if not kwh_columns and not other_columns:
            st.warning("No valid measure columns found")
            return
        
        # Create multiselect for non-KWh measures
        measures = st.multiselect(
            "Select measures to compare",
            options=other_columns,
            default=other_columns[:3] if len(other_columns) >= 3 else other_columns,
            key=f"measures_select_{message_index}"
        )
        
        x_col = 'PORTFOLIO_NAME' if 'PORTFOLIO_NAME' in df.columns else 'BUILDING_NAME'
        is_single_entity = len(df[x_col].unique()) == 1
        unique_years = df['YEAR'].nunique()
        
        # First display kWh charts
        if kwh_columns:
            st.markdown("### Energy Savings (kWh)")
            # Prepare data for kWh measures
            plot_data_kwh = df[[x_col, 'YEAR'] + kwh_columns].copy()
            plot_data_kwh = plot_data_kwh.groupby([x_col, 'YEAR'])[kwh_columns].mean().reset_index()
            
            if not plot_data_kwh.empty:
                # Melt the kWh data for charting
                plot_data_kwh_melted = pd.melt(
                    plot_data_kwh,
                    id_vars=[x_col, 'YEAR'],
                    value_vars=kwh_columns,
                    var_name='Measure',
                    value_name='Measure_Value'
                )
                
                # Create a single chart for kWh measures
                chart_kwh = alt.Chart(plot_data_kwh_melted).encode(
                    x=alt.X(f'{x_col}:N', 
                           title=x_col.replace('_', ' ').title(),
                           axis=alt.Axis(
                               labelAngle=45,
                               labelLimit=200,
                               labelOverlap=False
                           )),
                    y=alt.Y('Measure_Value:Q', 
                           title='Measure Values',
                           scale=alt.Scale(zero=True)),
                    color=alt.Color('YEAR:N',  # Color by year
                                  title='Year',
                                  legend=alt.Legend(orient='top')),
                    tooltip=[
                        alt.Tooltip(x_col, title=x_col.replace('_', ' ').title()),
                        alt.Tooltip('YEAR:N', title='Year'),
                        alt.Tooltip('Measure:N', title='Measure'),
                        alt.Tooltip('Measure_Value:Q', title='Value', format=',.2f')
                    ]
                ).mark_bar().encode(
                    xOffset='YEAR:N'  # Use xOffset to separate bars for each year
                )
                
                title_kwh = f"Energy Savings (kWh) Comparison by {x_col.replace('_', ' ').title()}"
                
                # Add chart styling
                styled_chart_kwh = chart_kwh.properties(
                    title=title_kwh
                ).configure_axis(
                    labelFontSize=12,
                    titleFontSize=14
                ).configure_title(
                    fontSize=16,
                    anchor='middle'
                )
                
                with st.container():
                    st.altair_chart(styled_chart_kwh, use_container_width=True)
                st.markdown("---")
        
        # Then display other measures
        if measures:
            st.markdown("### Other Metrics")
            plot_data = df[[x_col] + measures + ['YEAR']].copy()
            plot_data = plot_data.groupby([x_col, 'YEAR'])[measures].mean().reset_index()
            
            if not plot_data.empty:
                # Check if multiple years are present
                if unique_years > 1:
                    # Multiple measures, multiple years case
                    for measure in measures:
                        measure_data = pd.melt(
                            df,
                            id_vars=[x_col, 'YEAR'],  # Include YEAR for multiple years
                            value_vars=measure,
                            var_name='Measure',
                            value_name='Measure_Value'
                        )
                        
                        chart = alt.Chart(measure_data).encode(
                            x=alt.X(f'{x_col}:N', 
                                   title=x_col.replace('_', ' ').title(),
                                   axis=alt.Axis(
                                       labelAngle=45,
                                       labelLimit=200,
                                       labelOverlap=False
                                   )),
                            y=alt.Y('Measure_Value:Q', 
                                   title='Measure Values',
                                   scale=alt.Scale(zero=True)),
                            color=alt.Color('YEAR:N',  # Color by year
                                          title='Year',
                                          legend=alt.Legend(orient='top')),
                            tooltip=[
                                alt.Tooltip(x_col, title=x_col.replace('_', ' ').title()),
                                alt.Tooltip('YEAR:N', title='Year'),
                                alt.Tooltip('Measure:N', title='Measure'),
                                alt.Tooltip('Measure_Value:Q', title='Value', format=',.2f')
                            ]
                        ).mark_bar().encode(
                            xOffset='YEAR:N'  # Use xOffset to separate bars for each year
                        )
                        
                        title = f"{measure} Comparison by {x_col.replace('_', ' ').title()} Across Years"
                        styled_chart = chart.properties(
                            title=title
                        ).configure_axis(
                            labelFontSize=12,
                            titleFontSize=14
                        ).configure_title(
                            fontSize=16,
                            anchor='middle'
                        )
                        
                        with st.container():
                            st.altair_chart(styled_chart, use_container_width=True)
                else:  # Single year case
                    plot_data = pd.melt(
                        df,
                        id_vars=[x_col],
                        value_vars=measures,
                        var_name='Measure',
                        value_name='Measure_Value'  # Change 'Value' to 'Measure_Value' to avoid conflict
                    )
                    
                    chart = alt.Chart(plot_data).encode(
                        x=alt.X(f'{x_col}:N', 
                               title=x_col.replace('_', ' ').title(),
                               axis=alt.Axis(
                                   labelAngle=45,
                                   labelLimit=200,
                                   labelOverlap=False
                               )),
                        y=alt.Y('Measure_Value:Q', 
                               title='Measure Values',
                               scale=alt.Scale(zero=True)),
                        color=alt.Color('Measure:N',  # Color by measure
                                      title='Measure',
                                      legend=alt.Legend(orient='top')),
                        tooltip=[
                            alt.Tooltip(x_col, title=x_col.replace('_', ' ').title()),
                            alt.Tooltip('Measure:N', title='Measure'),
                            alt.Tooltip('Measure_Value:Q', title='Value', format=',.2f')
                        ]
                    ).mark_bar().encode(
                        xOffset='Measure:N'  # Use xOffset as measures when no year data
                    )
                    
                    title = f"Measures Comparison by {x_col.replace('_', ' ').title()}"
                    styled_chart = chart.properties(
                        title=title
                    ).configure_axis(
                        labelFontSize=12,
                        titleFontSize=14
                    ).configure_title(
                        fontSize=16,
                        anchor='middle'
                    )
                    
                    with st.container():
                        st.altair_chart(styled_chart, use_container_width=True)
            else:
                st.warning("No data available for the selected measures.")
                    
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        st.write("DataFrame columns:", df.columns.tolist())

st.title("Cortex Analyst")
st.markdown(f"Semantic Model: `{settings.FILE}`")

if st.button("Reset conversation") or "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.suggestions = []
    st.session_state.active_suggestion = None

for message_index,message in enumerate(st.session_state.messages):
    chat_role = "assistant" if message["role"] == "analyst" else "user"
    with st.chat_message(chat_role):
        display_content(
            content=message["content"],
            request_id=message.get("request_id"),
            message_index=message_index,
        )
if user_input := st.chat_input("What is your question?"):
    process_message(user_input=user_input)

if st.session_state.active_suggestion:
    process_message(user_input=st.session_state.active_suggestion)
    st.session_state.active_suggestion = None