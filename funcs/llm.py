import streamlit as st
import time
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
import re
class LLM:
    def __init__(self,tools,model,search):
        
        self.tools=tools
        self.model=model
        self.search=search
        self.agent = initialize_agent(
                    self.tools,
                    self.model,
                    agent_type=AgentType.SELF_ASK_WITH_SEARCH,
                    verbose=True,
                    memory=ConversationBufferWindowMemory(k=5, return_messages=True))
    
         
    def perform_web_search(self,query, max_retries=3, delay=2):
        retries = 0
        while retries < max_retries:
            try:
                search_results = self.search.run(query)
                return search_results
            except Exception as e:
                retries += 1
                st.warning(f"Web search failed for query '{query}'. Retrying ({retries}/{max_retries})...")
                time.sleep(delay)
        st.error(f"Failed to perform web search for query '{query}' after {max_retries} retries.")
        return "NaN"


    # Function to get LLM response for dynamic queries

    def get_llm_response(self,entity, query, web_results):
        prompt = f"""
        Extract relevant {query} (e.g., email, phone number) from the following web results for the entity: {entity}.
        Web Results: {web_results}
        """

        human_message_content = f"""
        Entity: {entity}
        Query: {query}
        Web Results: {web_results}
        """
        system_message_content = """
        You are a helpful assistant designed to answer questions by extracting information from the web and external sources. Your goal is to provide the most relevant, concise, and accurate response to user queries.
        """


        try:
            response = self.agent.invoke([system_message_content, human_message_content], handle_parsing_errors=True)
            extracted_info = response.get("output", "Information not available").strip()

            # Clean up irrelevant parts of the response
            cleaned_info = re.sub(r"(Thought:|Action:)[^A-Za-z0-9]*", "", extracted_info).strip()
            return cleaned_info
        except Exception as e:
            return "NaN"
        
    # Retry logic for multiple web searches if necessary
    def refine_answer_with_searches(self,entity, query, max_retries=3):
        search_results = self.perform_web_search(query.format(entity=entity))
        extracted_answer = self.get_llm_response(entity, query, search_results)

        if len(extracted_answer.split()) <= 2 or "not available" in extracted_answer.lower():
            search_results = self.perform_web_search(query.format(entity=entity))
            extracted_answer = self.get_llm_response(entity, query, search_results)

        return extracted_answer, search_results