import streamlit as st
def CreatePage():
    st.markdown("""
        <h1 style="text-align:center; color:#4CAF50; font-size: 40px;">🚀 Welcome to DataScribe</h1>
        <p style="text-align:center; font-size: 18px; color:#333;">An AI-powered information extraction tool to streamline data retrieval and analysis.</p>
    """, unsafe_allow_html=True)

    st.markdown("""---""")

    def feature_card(title, description, icon, page):
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"<div style='font-size: 40px; text-align:center;'>{icon}</div>", unsafe_allow_html=True)
        with col2:
            if st.button(f"{title}", key=title, help=description):
                st.session_state.selected_page = page
            st.markdown(f"<p style='font-size: 14px; color:#555;'>{description}</p>", unsafe_allow_html=True)
            
    col1, col2 = st.columns([1, 1])

    with col1:
        feature_card(
            title="Upload Data",
            description="Upload data from CSV or Google Sheets to get started with your extraction.",
            icon="📄",
            page="Upload Data"
        )

    with col2:
        feature_card(
            title="Define Custom Queries",
            description="Set custom search queries for each entity in your dataset for specific information retrieval.",
            icon="🔍",
            page="Define Query"
        )

    col1, col2 = st.columns([1, 1])

    with col1:
        feature_card(
            title="Run Automated Searches",
            description="Execute automated web searches and extract relevant information using an AI-powered agent.",
            icon="🤖",
            page="Extract Information"
        )

    with col2:
        feature_card(
            title="View & Download Results",
            description="View extracted data in a structured format and download as a CSV or update Google Sheets.",
            icon="📊",
            page="View & Download"
        )
    return True
