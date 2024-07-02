from langchain_openai import ChatOpenAI
from modules.load_env import get_openai_key
import openai
from openai import OpenAI


api_key = get_openai_key()


class GPT4Module:
    def __init__(self):
        # new

        self.client = OpenAI(
            api_key=api_key,  
            )
        
        

    def execute_query(self, prompt, model="gpt-4", max_tokens=500):
        """
        Execute a query using GPT-4.
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that is assisting a user with generating a SQL query based on their natural language input.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            return str(e)