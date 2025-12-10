import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import math
import os
from utils.helper_functions import setup_page

# --- Helper Functions ---


# --- Page Content ---
st.set_page_config(layout="wide")
setup_page()

# -- Sidebar --
current_dir = os.path.dirname(os.path.abspath(__file__))

logo_path = os.path.join(current_dir, 'bgu_logo.png')
st.sidebar.image(logo_path)
st.sidebar.markdown("""

        <div style="text-align: center;">
            <h3>תורת התנודות</h3>
            <h4>362.1.4791</h4>
        </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="top-header"><h1>🔎 The Galerkin method︎</h1></div>', unsafe_allow_html=True)

# --- background ---
st.markdown('<div class="section-header"><h2>💡 Theory background</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
        <div class='background'>

        Some general background about the topic. \n
        A link to a PDF file if needed.

        </div>
    """, unsafe_allow_html=True)

# --- Video Section ---
st.markdown('<div class="section-header"><h2>▶️ Video</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
video_url = 'https://www.youtube.com/watch?v=vLaFAKnaRJU&t=595s'

with col1:
    st.markdown(f"""
        <div class='video-section'>
        Here will be a video about the topic, either a link to YouTube or embedded here.\n
        For example:\n

        <iframe width="560" height="315" src="https://www.youtube.com/embed/vLaFAKnaRJU?si=ooRWYPxSeJHI7uXO" title="YouTube video player" 
        frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; 
        web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
        </div>
    """, unsafe_allow_html=True)

# --- Simulation Section ---
st.markdown('<div class="section-header"><h2>🕹️ Simulation</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
        <div class='simulation-section'>
            Here will be a simulation of the topic (python, matlab, something from the internet).
        </div>
    """, unsafe_allow_html=True)

# --- Practice Section ---
st.markdown('<div class="section-header"><h2>✍️ Lets prectice!</h2></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown(r"""
        <div class='practice-section'>
        <h4>Given:</h4>

        Here we can put some multiple-choice question about the topic so the students can practice.

        Currently there are 10 tries until the correct answer is presented.

        </div>
    """, unsafe_allow_html=True)

# Definition of correct answers
correct_answers = {
    "q1": 1,
    "q2": 1,
    "q3": 1,
    "q4": 1
}

# Question 1
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class='question-box'>
        <h3>Question 1️⃣</h3>
         What is the color of the sky? \n
         1- Green\n
         2- Blue\n
         3- Red\n
         4- Yellow\n
        </div>
    """, unsafe_allow_html=True)

    # Get the current attempt count from URL parameters
    q1_attempt_count = int(st.query_params.get("q1_attempts", "0"))

    # Use a form for question 1
    with st.form(key="question1_form"):
        q1_answer = st.number_input(
            "Type the number of the correct answer:",
            min_value=0.0,
            max_value=4.0,
            step=1.0,
            key="q1_input"
        )

        # Submit button (disabled if max attempts reached)
        q1_submit = st.form_submit_button(
            "check",
            disabled=(q1_attempt_count >= 10 or st.query_params.get("q1_status") == "success")
        )

        # Process form submission inside the form
        if q1_submit:
            # Check if answer is correct
            is_correct = abs(q1_answer - correct_answers["q1"]) < 0.1

            if is_correct:
                st.query_params["q1_status"] = "success"
            else:
                # Increment attempt counter
                q1_attempt_count += 1

                # Update URL parameter
                st.query_params["q1_attempts"] = str(q1_attempt_count)

                if q1_attempt_count >= 10:
                    st.query_params["q1_status"] = "failed"
                else:
                    st.query_params["q1_status"] = "trying"

        # Check if we need to show a previous result
        if "q1_status" in st.query_params:
            status = st.query_params["q1_status"]
            if status == "success":
                st.success(f"Good job! The correct answer is {correct_answers['q1']}. \n"
                           "\n"
                           f"**Explanation:** Bla Bla Bla.")
            elif status == "failed":
                st.error(f"Better luck next time. \n"
                         "\n"
                         f"The correct answer is {correct_answers['q1']}. \n"
                         "\n"
                         f"**Explanation:** Bla Bla Bla.")
            elif status == "trying":
                current_attempts = int(st.query_params.get("q1_attempts", "0"))
                remaining = 10 - current_attempts
                st.error(f"Try again! {remaining} attempts are left.")

