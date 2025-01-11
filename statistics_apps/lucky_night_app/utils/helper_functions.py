import streamlit as st

"""
This module contains helper functions that are used across multiple pages.
"""

"""
Set up the page with custom CSS styles.
"""
def setup_page():
    # Add RTL support
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;600&display=swap');

            .stApp {
                direction: rtl;
            }

            /* Style the sidebar */
            section[data-testid="stSidebar"] {
                background-color: #f0f8ff;  /* תכלת בהיר */
            }

            /* Style sidebar content */
            section[data-testid="stSidebar"] .css-1d391kg {
                padding-top: 2rem;
            }

            /* Style navigation links */
            .css-1n76uvr {
                font-family: 'Rubik', sans-serif;
                font-size: 1.1rem !important;
                padding: 0.8rem 0.5rem !important;
                border-radius: 8px;
                transition: all 0.2s ease;
            }

            /* Highlight active page */
            .css-1n76uvr[aria-selected="true"] {
                background-color: #d4ebf2 !important;
                border-left: 4px solid #2e86c1;
                font-weight: 500;
            }

            /* Hover effect on navigation links */
            .css-1n76uvr:hover {
                background-color: #e1f1f7 !important;
            }

            /* Style sidebar header */
            section[data-testid="stSidebar"] .css-6qob1r {
                font-family: 'Rubik', sans-serif;
                font-size: 1.3rem;
                font-weight: 600;
                color: #2c3e50;
                padding: 1rem 0.5rem;
                border-bottom: 2px solid #bde0ec;
                margin-bottom: 1rem;
            }

            /* Add some space between icon and text */
            .css-1n76uvr span {
                margin-right: 8px;
            }

            /* Style main content */
            .main > div {
                padding-right: 80px;
                padding-left: 20px;
            }
        </style>
    """, unsafe_allow_html=True)

def under_development_page():
    st.title("🚧 בפיתוח")
    st.write("עמוד זה עדיין בפיתוח. בקרוב יהיה זמין!")