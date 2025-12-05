# CortexAI

## Description
CortexAI is an AI-powered chatbot built with Streamlit that generates SQL queries based on user input and provides structured summaries of building and portfolio data from a Snowflake database. The chatbot classifies queries into predefined cases, retrieves relevant data, and presents insights interactively.


## Visuals
(Screenshots or GIFs demonstrating the application in action can be added here.)

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.11.11
- Snowflake Database
- Streamlit

### Steps to Install
1. Clone the repository:
   ```bash
   git clone https://gitlab.com/cortex-ai/cortex_ai.git
   cd cortex_ai
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the `.env` file with Snowflake credentials (details below).
4. Run the application:
   ```bash
   streamlit run cortexai_streamlit.py
   ```

## Configuration

### `.env` File Setup
- Stores Snowflake credentials (to be created by the user).
The application requires Snowflake connection details provided in a `.env` file. The file should contain:
```plaintext
HOST=<Snowflake Host URL>
DATABASE=<Database Name>
SCHEMA=<Schema Name>
STAGE=<Stage Name>
FILE=<YAML Configuration File Name>
USER=<Snowflake Username>
PASSWORD=<Snowflake Password>
ACCOUNT=<Snowflake Account Identifier>
PORT=<Port Number>
WAREHOUSE=<Warehouse Name>
ROLE=<User Role>
```

### YAML Configuration File
The latest YAML file for data processing is:
```
semantic_file.yaml
```
This file is stored in the **SILVER schema** under **STAGES** in the **CortexAI Snowflake Database**.
Ensure that the `.env` file references the latest YAML file version.
This file defines metadata and structural information required for processing queries.

## Usage
1. Start the Streamlit app.
2. Enter a natural language query related to buildings or portfolios.
3. The chatbot classifies the query, generates SQL, and fetches data.
4. The results are displayed interactively with charts and tables.

## Project Structure

### Main File
- **`cortexai_streamlit.py`**: Primary Streamlit application file.

### SQL Query Modules (`prompts/`)
- `building.py` - Queries for buildings.
- `portfolio.py` - Queries for portfolios.
- `dailystat.py` - Queries for daily statistics.
- `measurement.py` - Queries for the latest sensor data.
- `demand.py` - Queries for peak demand.
- `improvements.py` - Queries for operational improvements.
- `query.py` - Classifies user queries.

### Summary Modules (`summary/`)
- `summary_case0.py` - General case.
- `summary_case1.py` - Multi-year analysis.
- `summary_case2.py` - Year-over-year comparison.
- `summary_case3.py` - Best/worst performer analysis.
- `summary_case4.py` - Single-year analysis.
- `summary_case5.py` - Multi-building/portfolio comparison year-over-year.
- `summary_case6.py` - Energy intensity analysis.
- `summary_case7.py` - Peak demand analysis.
- `improvements.py` - Operational improvement suggestions.
- `summary_classification.py` - Classifies summary cases.
- `default_summary.py` - Default summary handling.
