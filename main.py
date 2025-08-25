import os
import asyncio
import streamlit as st
# from firecrawl import FirecrawlApp
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import serpapi
import sys
from dotenv import load_dotenv

# Load environment variables from .env file``
load_dotenv()

# --- Streamlit UI Setup ---
st.set_page_config(
    page_title="Task 1: Web Search Agent | Task 2: Asynchronous Programming",
    layout="wide",
)

st.title("Web Search Agent")
st.write(
    """
    This web search agent performs two key tasks:
    
    1.  *TASK 1: Web Search and Summarization*: It uses a web search API to find relevant information and then leverages a large language model to provide a concise, well-structured summary.
    2.  *TASK 2: Asynchronous Programming*: It uses asynchronous calls to ensure the agent remains responsive and doesn't block while waiting for the LLM's response.
    """
)
# API Key Management
try:
    # Use st.secrets to retrieve keys in a deployed Streamlit app.
    # It also works locally if you set up the secrets.toml file.
    serpapi_api_key = st.secrets["api_keys"]["SERPAPI_API_KEY"]
    gemini_api_key = st.secrets["api_keys"]["GOOGLE_API_KEY"]

    if not all([serpapi_api_key, gemini_api_key]):
        st.error("API keys are not configured. Please ensure your keys are set as secrets in the Streamlit Cloud dashboard.")
        st.stop()
    
    # Optional: Set as environment variables for downstream libraries
    os.environ["SERPAPI_API_KEY"] = serpapi_api_key
    os.environ["GOOGLE_API_KEY"] = gemini_api_key
except KeyError:
    st.error("API keys are not configured. Please ensure your keys are set as environment variables in the streamlit dashboard secrets file.")
    st.stop()

# Initialize chat history in Streamlit's session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Main Agent Pipeline (Modified for Streamlit) ---
async def run_pipeline(user_prompt: str):
    with st.spinner("1. Searching the web with SerpAPI..."):
        serpapi_client = serpapi.Client(api_key=os.environ["SERPAPI_API_KEY"])
        try:
            data = serpapi_client.search(
                q=user_prompt,
                engine="google",
                hl="en",
                gl="us",
                num=5
            )
            items = data.get("organic_results", [])[:5]
            context = [
                {"title": item.get("title"),
                 "snippet": item.get("snippet"),
                 "link": item.get("link")}
                for item in items
            ]
        except Exception as e:
            st.error(f"SerpAPI Error: {e}")
            return "Sorry, I encountered an error during the search."

    with st.spinner("2. Summarizing with Gemini..."):
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are an expert researcher. Provide an in-depth, well-structured answer to the user's prompt only by using the context provided."),
            ("user", "The user searched for {prompt} and these are the search results: {context}. Provide a meaningful output using your knowledge and the context in a well-structured format. Use bullet points, tabular outputs, and other structures wherever needed.")
        ])

        output_parser = StrOutputParser()
        chain = prompt_template | llm | output_parser

        final_answer = await chain.ainvoke({
            "context": context,
            "prompt": user_prompt
        })
    
    return final_answer

# Main chat input and response logic
if prompt := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = asyncio.run(run_pipeline(prompt))
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content":response})