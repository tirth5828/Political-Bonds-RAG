from langchain.callbacks.base import BaseCallbackHandler


class SQLHandler(BaseCallbackHandler):
    def __init__(self):
        self.sql_result = []

    def on_agent_action(self, action, **kwargs):
        """Run on agent action. if the tool being used is sql_db_query,
         it means we're submitting the sql and we can 
         record it as the final sql"""

        if action.tool in ["sql_db_query_checker","sql_db_query"]:
            self.sql_result.append(action.tool_input)