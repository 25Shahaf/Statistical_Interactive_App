import streamlit as st

"""
This module contains helper functions that are used across multiple pages.
"""

"""
Set up the page with custom CSS styles.
"""
def setup_page():
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
                color: black !important;
            }

            /* Style navigation links */
            .css-1n76uvr {
                font-family: 'Rubik', sans-serif;
                font-size: 1.1rem !important;
                color: black !important;
                padding: 0.8rem 0.5rem !important;
                border-radius: 8px;
                transition: all 0.2s ease;
            }

            /* Highlight active page */
            .css-1n76uvr[aria-selected="true"] {
                background-color: #d4ebf2 !important;
                color: black !important;
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
                color: black;
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
                    h1, h2, h3, h4, h5, h6 {
            color: black !important;
            }
            /* Adjust padding */
            .css-18e3th9 {padding: 6rem;
            } 
            .css-1y4p8pa {
            max-width: 100rem;
            }
            .section-header {
                background-color: #e0e5eb;
                color: black !important;
                padding: 0.1rem;
                border-radius: 10px;
                margin: 2rem 0 1rem 0;
            }
            .top-header {
                background-color: rgba(236, 249, 252, 0.8);
                color: black !important;
                padding: 0.1rem;
                border-radius: 10px;
                margin: 2rem 0 1rem 0;
                text-align: center;
            }
            .game-explanation {
                background-color: #eefafd;
                color: black !important;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1rem 0;
                border-right: 5px solid #83b0bb;
            }
            .game-explanation-header {
                background-color: #eefafd;
                color: black !important;
                padding: 0.3rem;
                border-radius: 10px;
                margin: 1rem 0;
            }
            .theory-section {
                background-color: #fdf5f8;
                color: black !important;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1rem 0;
                border-right: 5px solid #c8a2ae;
            }
            .practice-section {
                background-color: #ebfaf1;
                color: black !important;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1rem 0;
                border-right: 5px solid #83bb9a;
            }
            .question-box {
                background-color: white;
                color: black !important;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1rem 0;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                border: 1px solid #ddd;
            }
            .stButton>button {
                margin: 10px 0;
            }
            .custom-columns {
                display: flex;
                gap: 2rem;
            .custom-image {
                height: 150px; /* Set desired height */
                object-fit: cover; /* Ensures the image fits nicely */
            }
        </style>
    """, unsafe_allow_html=True)

def under_development_page():
    col1, col2 = st.columns([1, 4])

    with col1:
        st.markdown('<div class="section-header"><h2>🚧 בפיתוח</h2></div>', unsafe_allow_html=True)
        st.write("עמוד זה עדיין בפיתוח. בקרוב יהיה זמין!")