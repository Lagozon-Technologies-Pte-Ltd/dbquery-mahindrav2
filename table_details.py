import pandas as pd
import os
import configure
from operator import itemgetter
from langchain.chains.openai_tools import create_extraction_chain_pydantic 
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI 
#from  langchain_openai.chat_models import with_structured_output

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
llm = ChatOpenAI(model=configure.selected_models, temperature=0)
from typing import List
# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

def get_table_details(selected_subject='Demo', table_name=None):
    # Build the path to the CSV file
    select_database_table_desc_csv = selected_subject + ".csv"
    path = f'table_files/{select_database_table_desc_csv}'
    
    try:
        table_description = pd.read_csv(path)
    except FileNotFoundError:
        return f"File not found: {path}"
    
    table_details = ""
    print("path for csv: ", path)

    # Check if 'data_type' column exists
    has_data_type = 'data_type' in table_description.columns

    # Filter for the requested table_name if provided
    if table_name:
        filtered = table_description[table_description['table_name'].str.lower() == table_name.lower()]
        if filtered.empty:
            return f"No details found for table: {table_name}"
        grouped = filtered.groupby(['table_name', 'table_description'])
    else:
        grouped = table_description.groupby(['table_name', 'table_description'])

    for (table, desc), group in grouped:
        table_details += f"Table Name: {table}\n"
        table_details += f"Table Description: {desc}\n"
        table_details += "Columns:\n"
        for i, row in group.iterrows():
            # Parse column_name&description
            if ':' in row['column_name&description']:
                col_name, col_desc = row['column_name&description'].split(':', 1)
                col_name = col_name.strip()
                col_desc = col_desc.strip()
            else:
                col_name = row['column_name&description'].strip()
                col_desc = ""
            # Add data type if present
            if has_data_type:
                data_type = row['data_type']
                table_details += f"  - {col_name} ({data_type}): {col_desc}\n"
            else:
                table_details += f"  - {col_name}: {col_desc}\n"
        table_details += "\n"

    if not table_details:
        table_details = "No tables found in the CSV."
    
    return table_details
class Table(BaseModel):
    """Table in SQL database."""

    name: str = Field(description="Name of table in SQL database.")

def get_tables(tables: List[Table]) -> List[str]:
    tables  = [table.name for table in tables]
    return tables


# table_names = "\n".join(db.get_usable_table_names())
# table_details = get_table_details()
# print("testinf details",table_details, type(table_details))
# table_details_prompt = f"""Return the names of ALL the SQL tables that MIGHT be relevant to the user question. \
#     The permissible tables names are listed below and must be strictly followed:

#     {table_details}

#     Remember to include ALL POTENTIALLY RELEVANT tables, even if you're not sure that they're needed."""
# table_details_set_prompt = os.getenv('TABLE_DETAILS_SET_PROMPT')
# table_details_prompt=table_details_set_prompt.format(table=table_details)
# # print("Table_details_prompt: ", table_details_prompt)
# table_chain = {"input": itemgetter("question")} | create_extraction_chain_pydantic(Table, llm, system_message=table_details_prompt) | get_tables
# mock_question_test = "How many product view by products in last week"
# table_chain_check = table_chain.invoke({"question":mock_question_test})
# print("test table chain  first mock_question  :" , mock_question_test ,"  Now tables selected:... ",table_chain_check)
