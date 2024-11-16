import streamlit as st

def CreatePage():
    st.header("Define Your Custom Query")

    if "data" not in st.session_state or st.session_state["data"] is None:
        st.warning("Please upload data first! Use the 'Upload Data' section to upload your data.")
    else:
        column = st.selectbox(
            "Select entity column", 
            st.session_state["data"].columns,
            help="Select the column that contains the entities for which you want to define queries."
        )
        
        st.markdown("""
        <style>
        div[data-baseweb="select"] div[data-id="select"] {{
            background-color: #f0f8ff;
        }}
        </style>
        """, unsafe_allow_html=True)

        st.subheader("Define Fields to Extract")
        num_fields = st.number_input(
            "Number of fields to extract", 
            min_value=1, 
            value=1, 
            step=1, 
            help="Specify how many fields you want to extract from each entity."
        )
        
        fields = []
        for i in range(num_fields):
            field = st.text_input(
                f"Field {i+1} name", 
                key=f"field_{i}",
                placeholder=f"Enter field name for {i+1}", 
                help="Name the field you want to extract from the entity."
            )
            if field:
                fields.append(field)

        if fields:
            st.subheader("Query Template")
            query_template = st.text_area(
                "Enter query template (Use '{entity}' to represent each entity)",
                value=f"Find the {', '.join(fields)} for {{entity}}",
                help="You can use {entity} as a placeholder to represent each entity in the query."
            )

            if "{entity}" in query_template:
                example_entity = str(st.session_state["data"][column].iloc[0])
                example_query = query_template.replace("{entity}", example_entity)
                st.write("### Example Query Preview")
                st.code(example_query)

            if st.button("Save Query Configuration"):
                if not fields:
                    st.error("Please define at least one field to extract.")
                elif not query_template:
                    st.error("Please enter a query template.")
                else:
                    st.session_state["column_selection"] = column
                    st.session_state["query_template"] = query_template
                    st.session_state["extraction_fields"] = fields
                    st.success("Query configuration saved successfully!")
