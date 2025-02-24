import io, sys, os, textwrap, re

import sqlite3
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_together import ChatTogether

from user_sql_prompt import prompt as custom_prompt

from dotenv import load_dotenv
load_dotenv()


# Initialize Groq LLM
llm = ChatTogether(model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free")


# SQLite Database Connection
db_path = "./data/database.db"  # Ensure this path is correct
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


def get_sql_data(user_query):
    """Generate SQL from user query and execute it

    Args:
        user_query: user's input query

    Return:
        The output of the SQL query or a response if no SQL is needed.
        response: str
    """

    # Define the custom prompt
    prompt_template = PromptTemplate(
        input_variables=["user_query"],
        template=custom_prompt,
    )

    # Create an LLM chain
    # sql_chain = ({
    #     llm=llm | prompt=prompt_template}
    #     )

    # sql_chain = (
    #     {"question": RunnablePassthrough()}
    #     | custom_prompt
    #     | llm
    #     | StrOutputParser()
    # )

    # creating llm chain
    sql_chain = prompt_template | llm | StrOutputParser()

    # Generate SQL using LLM
    response = sql_chain.invoke({"user_query": user_query})

    # If LLM determines no SQL is needed, return response
    if "No SQL needed" in response or not response.lower().startswith("select"):
        return f"Response: {response}"

    try:
        # Execute SQL query
        cursor.execute(response)
        rows = cursor.fetchall()
        print(response)
        print("------------")
        print(rows)

        if rows:
            return rows
        else:
            return "No records found."
    except sqlite3.Error as e:
        print("Inside exception")
        return f"SQL Error: {str(e)}"


# Example usage
if __name__ == "__main__":
    while True:
        user_query = input("Enter your query (or type 'exit' to quit): ")
        if user_query.lower() == "exit":
            break
        result = get_sql_data(user_query)
        print("------------")
        print(result)
        print("------------")

# Close the database connection when done
conn.close()
