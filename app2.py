import os
import time
from urllib.parse import quote_plus
from dotenv import load_dotenv
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import streamlit as st

load_dotenv()

# Initialize the database
def init_database(host, user, port, database, password):
    password_encoded = quote_plus(password)
    db = SQLDatabase.from_uri(
        f"mysql+mysqlconnector://{user}:{password_encoded}@{host}:{port}/{database}"
    )
    return db

def get_sql_chain(db):
    groq_api_key = os.environ.get("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")

    template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the things in the database.
    Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.

    <SCHEMA>{schema}</SCHEMA>

    Conversation History: {chat_history}

    Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.

    Question: {question}
    SQL Query:
    """
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="mixtral-8x7b-32768")

    def get_schema(_):
        return db.get_table_info()

    return (
            RunnablePassthrough.assign(schema=get_schema)
            | prompt
            | llm
            | StrOutputParser()
    )

def get_response(question: str, db: SQLDatabase, chat_history: list):
    groq_api_key = os.environ.get("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")

    sql_chain = get_sql_chain(db)
    template = """
    You are a helpful assistant. You are interacting with a user who is asking you questions about the things in the database. You will have access to
    the table schema below, question: {question} and SQL query that would answer the user's question. Your job is to write a natural language response based on the SQL response {sql_response}.
    Take the conversation history into account.

    <SCHEMA>{schema}</SCHEMA>

    Conversation History: {chat_history}
    """

    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="mixtral-8x7b-32768")

    chain = (
            RunnablePassthrough.assign(query=sql_chain).assign(
                schema=lambda _: db.get_table_info(),
                sql_response=lambda vars: db.run(vars["query"]),
            )
            | prompt
            | llm
            | StrOutputParser()
    )

    return chain.invoke(
        {
            "question": question,
            "chat_history": chat_history,
        }
    )

# Set up the Streamlit app
st.set_page_config(
    page_title="Chat with MySQL",
    page_icon=":speech_balloon:",
)

st.title("Chat with MySQL")

# Set up the sidebar with settings and connect button
with st.sidebar:
    st.subheader("Settings")
    st.write("This is a simple application using MySQL & Streamlit.")

    host = st.text_input("Host", value="localhost", key="host")
    user = st.text_input("User", value="root", key="user")
    port = st.text_input("Port", value="3306", key="port")
    database = st.text_input("Database", value="jobs_in_data", key="database")
    password = st.text_input("Password", type="password", key="password")

    if st.button("Connect"):
        if not all([host, user, port, database, password]):
            st.warning("Please fill in all fields.")
        else:
            try:
                with st.spinner("Connecting..."):
                    db = init_database(host, user, port, database, password)
                    st.session_state["db"] = db
                    st.success("Connected to MySQL!")
            except Exception as e:
                st.error(f"Error: {e}")

# Chat interface
if "db" in st.session_state:
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [
            AIMessage(content="Hello, I'm your SQL AI Assistant. How can I help you?")
        ]

    for message in st.session_state["chat_history"]:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.markdown(message.content)
        else:
            with st.chat_message("Human"):
                st.markdown(message.content)

    user_input = st.chat_input(
        placeholder="Ask a query about Jobs in Data...", key="query"
    )

    if user_input:
        try:
            st.session_state.chat_history.append(HumanMessage(content=user_input))

            with st.chat_message("Human"):
                st.markdown(user_input)

            with st.chat_message("AI"):
                response = get_response(user_input, st.session_state.db, st.session_state.chat_history)
                message_placeholder = st.empty()
                full_response = ""

                for chunk in response:
                    full_response += chunk
                    time.sleep(0.001)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)
            st.session_state.chat_history.append(AIMessage(content=response))

        except Exception as e:
            st.warning(
                "Please input a valid SQL query according to the database schema."
            )
