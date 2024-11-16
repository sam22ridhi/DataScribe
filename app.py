import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import streamlit as st
import warnings
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from funcs.llm import LLM
from views import home,upload_data,define_query,extract_information,view_and_download
from views.extract_information import ExtractInformation

warnings.filterwarnings("ignore", category=DeprecationWarning)


#environment
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
search = GoogleSerperAPIWrapper(serp_api_key=SERPER_API_KEY)
model = ChatGroq(model="llama-3.1-70b-versatile")


tools = [
            Tool(
                name="Web Search",
                func=search.run,
                description="Searches the web for information related to the query"
    )   
]

llm = LLM(tools,model,search)

st.set_page_config(page_title="DataScribe", page_icon=":notebook_with_decorative_cover:", layout="wide")
if "results" not in st.session_state:
    st.session_state["results"] = [] 
    
with st.sidebar:
    selected = option_menu(
        "DataScribe Menu",
        ["Home", "Upload Data", "Define Query", "Extract Information", "View & Download"],
        icons=["house", "cloud-upload", "gear", "search", "table"],
        menu_icon="cast",
        default_index=0
    )
if selected == "Home":
    home.CreatePage()

elif selected == "Upload Data":
    upload_data.CreatePage()
    
elif selected == "Define Query":
    define_query.CreatePage()
    
elif selected == "Extract Information":
    extract = ExtractInformation(llm)
    extract.CreatePage()
   
elif selected == "View & Download":
    view_and_download.CreatePage()

