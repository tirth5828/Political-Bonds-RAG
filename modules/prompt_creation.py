# modules/prompt_creation.py
def generate_sql_prompt(description, user_query):
    """
    Generate a prompt for creating a SQL query from a natural language description.

    Parameters:
    description (str): A description of the database schema.
    user_query (str): The user's natural language query.

    Returns:
    str: A formatted prompt for generating a SQL query.
    """
    prompt = "Generate SQL query based on the user's natural language input.\n"
    prompt += f"Database Description:\n{description}\n\n"
    prompt += f"User Query: '{user_query}'\n"
    prompt += "DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.)\n"
    prompt += "SQL Query:"
    
    return prompt