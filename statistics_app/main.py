import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn2_circles, venn3
import matplotlib.patches as mpatches
from scipy.stats import alpha
from pages import basic_terms, basic_definitions, conditional_probability, normal_distribution

# Set the password for the app
PASSWORD = "BGU123"

# Initialize session state variable for password attempts
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Function to display password input
def login():
    if st.session_state['authenticated']:
        return  # Return early if already authenticated

    # Create a text input for the password
    password = st.text_input("Enter password", type="password", key="password_input")

    # Check if the button is clicked
    if st.button("Submit"):
        # If the password is correct
        if password == PASSWORD:
            st.session_state['authenticated'] = True  # Successful login
            st.success("Correct Password! Please click the 'Submit' button again to login.")  # Optional success message
        elif password:  # Check only if the password is not empty
            st.error("Incorrect password")


if st.session_state['authenticated']:
    st.markdown("<h1 style='font-size: 52px; font-weight: bold; color: #139dd1;'>🔢 Statistical Visualizations</h1>", unsafe_allow_html=True)

    # Sidebar for navigation
    section = st.sidebar.radio("Select a Concept", ["Basic Terms", "Basic Definitions", "Conditional Probability",
                                                    "Normal Distribution"])

    # Visualize union an intersection concepts
    if section == "Basic Terms":
        basic_terms.app()

    elif section == "Basic Definitions":
        basic_definitions.app()

    # Visualize conditional probability
    elif section == "Conditional Probability":
        conditional_probability.app()

    # Visualize normal distribution
    elif section == "Normal Distribution":
        normal_distribution.app()


else:
    login()
    st.write("Please enter the password to access the app.")