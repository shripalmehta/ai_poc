# import sqlite3
import io, sys, os, textwrap, re
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_together import ChatTogether

from dotenv import load_dotenv
load_dotenv()


from user_py_prompt import prompt as custom_prompt

# Initialize Groq LLM
llm = ChatTogether(model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free")


db_path = "./data/file_out.csv"  # Ensure this path is correct

# Python code from user query using LLM
def get_pycode_from_query(user_query):
    """Generate Python code for user query and execute it

    Args:
        user_query: user's input query

    Return:
        Python code to extract insights from database, if appropriate, or a response if no code is required.
        response: str
    """

    # Define the custom prompt
    prompt_template = PromptTemplate(
        input_variables=["user_query"],
        template=custom_prompt,
    )

    # creating llm chain
    py_chain = prompt_template | llm | StrOutputParser()

    # Generate Python code using LLM
    py_code = py_chain.invoke({"user_query": user_query})

    # If LLM determines no SQL is needed, return response
    if "invalid" in py_code:
        return "Response: Invalid input, please retry."


    # Remove leading whitespace from the generated code
    cleaned_py_code = re.sub(r"^```.*?\n|\n```$", "", py_code.strip(), flags=re.MULTILINE)

    print(" -------- -------- -------- ")
    print(cleaned_py_code)
    print(" -------- -------- -------- ")

    try:
        # Capture the standard output
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        # Execute the generated Python code
        exec(cleaned_py_code, {}, {})

        # Get the printed output
        output = sys.stdout.getvalue().strip()

        # Restore the standard output
        sys.stdout = old_stdout

        print(output)
        return output if output else "No output generated."

    except Exception as e:
        sys.stdout = old_stdout # Restore standard output in case of an error
        print("Inside exception")
        # print("*********** output ***********")
        # print(str(output))
        print("*********** old_stdout ***********")
        print(str(old_stdout))

        print(f"Error: {str(e)}")
        return f"Error: {str(e)}"


# Example usage
if __name__ == "__main__":
    # user_query = "what is the sale of 15th sept 2020?"
    # result = get_pycode_from_query(user_query)
    # print("============")
    # print(result)
    while True:
        user_query = input("Enter your query (or type 'exit' to quit): ")
        if user_query.lower() == "exit":
            break
        result = get_pycode_from_query(user_query)
        print("------------")
        print(result)
        print("------------")
