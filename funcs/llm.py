import streamlit as st
import time
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
import re
import requests

class LLM:
    def __init__(self, tools, model, search):
        self.tools = tools
        self.model = model
        self.search = search
        self.agent = initialize_agent(
            self.tools,
            self.model,
            agent_type=AgentType.SELF_ASK_WITH_SEARCH,
            verbose=True,
            max_iterations=5,
            #memory=ConversationBufferWindowMemory(k=5, return_messages=True)
        )
        
        # Define extraction templates for different query types
        self.extraction_templates = {
            "ceo": {
                "pattern": r"(?i)(?:ceo|chief executive officer)[:\s]*([A-Za-z\s]+)",
                "clean": lambda x: x.strip().lower().title()
            },
            "email": {
                "pattern": r"[\w\.-]+@[\w\.-]+\.\w+",
                "clean": lambda x: x.strip().lower()
            },
            "phone": {
                "pattern": r"[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4}",
                "clean": lambda x: re.sub(r'[\s\.-]', '', x)
            }
        }

    def perform_web_search(self, query, max_retries=3, delay=2, timeout=10):
        retries = 0
        while retries < max_retries:
            try:
                search_results = self.search.run(query, timeout=timeout)
                return search_results
            except requests.exceptions.Timeout:
                retries += 1
                st.warning(f"Web search timed out. Retrying ({retries}/{max_retries})...")
                time.sleep(delay)
            except Exception as e:
                retries += 1
                st.warning(f"Web search failed. Retrying ({retries}/{max_retries})... Error: {e}")
                time.sleep(delay)
        st.error(f"Failed to perform web search after {max_retries} retries.")
        return "NaN"

    def extract_specific_information(self, text, query_type):
        """
        Extract specific information based on query type using predefined patterns
        """
        if query_type not in self.extraction_templates:
            return None
            
        template = self.extraction_templates[query_type]
        matches = re.findall(template["pattern"], text)
        
        if matches:
            # Apply cleaning function and return first match
            return template["clean"](matches[0])
        return None

    def get_llm_response(self, entity, query_type, web_results):
        """
        Enhanced extraction with specific formatting and cleaning
        """
        prompt = PromptTemplate(
            template="""
            Context: Find exactly {query_type} for {entity}.
            Web Results: {web_results}
            
            Rules:
            1. Return ONLY the {query_type} value
            2. Do not include any explanatory text
            3. If multiple values found, return the most recent/relevant one
            4. If no valid value found, return "NaN"
            
            Format your response as a single line with only the requested information.
            """,
            input_variables=["query_type", "entity", "web_results"]
        )

        try:
            # Get raw response from agent
            response = self.agent.invoke(
                prompt.format(
                    query_type=query_type,
                    entity=entity,
                    web_results=web_results
                ),
                handle_parsing_errors=True
            )
            
            raw_response = response.get("output", "").strip()
            
            # Try to extract specific information using patterns
            extracted_info = self.extract_specific_information(raw_response, query_type)
            
            if extracted_info:
                return extracted_info
            
            # If pattern matching fails, clean up the raw response
            cleaned_response = re.sub(r'(?i).*?(?:is|as|the|named|called|:|\->)\s*', '', raw_response)
            cleaned_response = re.sub(r'\s+', ' ', cleaned_response).strip()
            
            return cleaned_response if cleaned_response else "NaN"
            
        except Exception as e:
            return "NaN"

    def refine_answer_with_searches(self, entity, query_type, max_retries=3):
        """
        Improved search refinement with type-specific handling
        """
        search_query = f"What is the {query_type} of {entity}?"
        search_results = self.perform_web_search(search_query)
        extracted_answer = self.get_llm_response(entity, query_type, search_results)

        # If first attempt fails, try alternative search patterns
        if extracted_answer == "NaN" and max_retries > 1:
            alternative_queries = [
                f"{entity} {query_type} information",
                f"{entity} current {query_type}",
                f"Who is {entity}'s {query_type}"
            ]
            
            for query in alternative_queries:
                search_results = self.perform_web_search(query)
                extracted_answer = self.get_llm_response(entity, query_type, search_results)
                if extracted_answer != "NaN":
                    break

        return extracted_answer, search_results
