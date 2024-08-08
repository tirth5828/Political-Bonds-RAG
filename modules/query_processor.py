# modules/query_processor.py
from agent_toolkits.sql.base import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from modules.load_env import get_openai_key
import openai
from langchain_anthropic import ChatAnthropic
from modules.database import connect , get_description_of_all_tables
from modules.LLM import GPT4Module
from modules.SQLHandler import SQLHandler
from modules.prompt_creation import generate_sql_prompt



def create_agent(db_path , api_key):
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
    llm = ChatOpenAI(api_key=api_key,model="gpt-4", temperature=0)
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=False)
    return agent_executor

def translate_and_execute_query(agent_executor, user_query):
    handler = SQLHandler()
    response = agent_executor.invoke({"input": user_query},{'callbacks':[handler]})
    return response["output"] , handler.sql_result[-1]

def execute_sql_query(conn, sql_query):
    cursor = conn.cursor()
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    return rows

def format_response(rows):
    if not rows:
        return "No results found."
    
    return rows[0][0]


def process_without_agent(conn , user_query , api_key):
    
    # get database decsription
    description = get_description_of_all_tables(conn)
    
    
    prompt = generate_sql_prompt(description, user_query)
    
    
    # Generate SQL query through LLM
    llm = GPT4Module(api_key)
    sql_query = llm.execute_query(prompt)
    
    print(f"Translated SQL Query: {sql_query}")
    
    
    # verify if the query is valid
    if not sql_query:
        return "No valid SQL query could be generated."
    else:
        # trim the query between ``` and ``` to get the actual query
        sql_query = sql_query.split("```")[1]
    
    # Execute the SQL query
    rows = execute_sql_query(conn, sql_query)
    
    
    # Format the response
    formatted_response = format_response(rows)
    
    return formatted_response
    
    
    
    
    
    

