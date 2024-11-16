import streamlit as st
from funcs.llm import LLM
class ExtractInformation:
    def __init__(self,llm :LLM):
        self.llm = llm
        
    def CreatePage(self):
        st.header("Extract Information")
        if "query_template" in st.session_state and "data" in st.session_state:
            st.write("### Using Query Template:")
            st.code(st.session_state["query_template"])

            column_selection = st.session_state["column_selection"]
            entities_column = st.session_state["data"][column_selection]
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write("### Selected Entity Column:")
                st.dataframe(entities_column, use_container_width=True)
            
            with col2:
                start_button = st.button("Start Extraction", type="primary", use_container_width=True)

            results_container = st.empty()
                
            if start_button:
                with st.spinner("Extracting information..."):
                    progress_bar = st.progress(0)
                    progress_text = st.empty()
                    
                    try:
                        results = []
                        for i, selected_entity in enumerate(entities_column):
                            user_query = st.session_state["query_template"].replace("{entity}", str(selected_entity))
                            final_answer, search_results = self.llm.refine_answer_with_searches(selected_entity, user_query)
                            results.append({
                                "Entity": selected_entity,
                                "Extracted Information": final_answer,
                                "Search Results": search_results
                            })
                            
                            progress = (i + 1) / len(entities_column)
                            progress_bar.progress(progress)
                            progress_text.text(f"Processing {i+1}/{len(entities_column)} entities...")

                        st.session_state["results"] = results
                        
                        progress_bar.empty()
                        progress_text.empty()
                        st.success("Extraction completed successfully!")

                    except Exception as e:
                        st.error(f"An error occurred during extraction: {str(e)}")
                        st.session_state.pop("results", None)

            if "results" in st.session_state and st.session_state["results"]:
                with results_container:
                    results = st.session_state["results"]
                    
                    search_query = st.text_input("🔍 Search results", "")
                    
                    tab1, tab2 = st.tabs(["Compact View", "Detailed View"])
                    
                    with tab1:
                        found_results = False
                        for result in results:
                            if search_query.lower() in str(result["Entity"]).lower() or \
                            search_query.lower() in str(result["Extracted Information"]).lower():
                                found_results = True
                                with st.expander(f"📋 {result['Entity']}", expanded=False):
                                    st.markdown("#### Extracted Information")
                                    st.write(result["Extracted Information"])
                        
                        if not found_results and search_query:
                            st.info("No results found for your search.")
                    
                    with tab2:
                        found_results = False
                        for i, result in enumerate(results):
                            if search_query.lower() in str(result["Entity"]).lower() or \
                            search_query.lower() in str(result["Extracted Information"]).lower():
                                found_results = True
                                st.markdown(f"### Entity {i+1}: {result['Entity']}")
                                
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.markdown("#### 📝 Extracted Information")
                                    st.info(result["Extracted Information"])
                                
                                with col2:
                                    st.markdown("#### 🔍 Search Results")
                                    st.warning(result["Search Results"])
                                
                                st.divider()
                        
                        if not found_results and search_query:
                            st.info("No results found for your search.")
        else:
            st.warning("Please upload your data and define the query template.")