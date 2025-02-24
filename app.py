import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_together import ChatTogether
from langchain_voyageai import VoyageAIEmbeddings
# from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnablePassthrough

from py_code_gen import get_pycode_from_query
from sql_query_gen import get_sql_data

load_dotenv()


query = "what is the sale of 15th septemeber 2020?"

llm = ChatTogether(model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free")
embeddings = VoyageAIEmbeddings(model="voyage-3")
# vector_store = Chroma(embedding_function=embeddings)

llm_prompt = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use maximum 3 sentences and keep it concise.
Question: {question}
Context: {context}
Answer:
"""

prompt = PromptTemplate(
    input_variables=["user_query", "context"],
    template=llm_prompt,
)
# retriever = vector_store.as_retriever()

# output retriever

# context = get_sql_data(user_query=query)
context = get_pycode_from_query(user_query=query)

chain = RunnablePassthrough() | {"context": context} | prompt | llm | StrOutputParser()

response = chain.invoke({"question": query})
print(response)
