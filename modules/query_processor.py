# modules/query_processor.py
# from langchain_community.agent_toolkits.sql.base import create_sql_agent
from agent_toolkits.sql.base import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from modules.load_env import get_openai_key
import openai
from langchain_anthropic import ChatAnthropic




api_key = get_openai_key()

def create_agent(db_path):
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
    llm = ChatOpenAI(api_key=api_key,model="gpt-4", temperature=0)
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=False)
    return agent_executor


def translate_and_execute_query(agent_executor, user_query):
    response = agent_executor.invoke({"input": user_query})
    print(response)
    return response["output"]

def execute_sql_query(conn, sql_query):
    cursor = conn.cursor()
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    return rows

def format_response(rows):
    return [dict(row) for row in rows]

