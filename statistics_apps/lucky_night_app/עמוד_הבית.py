import streamlit as st
import os
from PIL import Image

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import math
import time

from utils.helper_functions import setup_page


def main():
    st.set_page_config(page_title="ליל המזל 🎲", layout="wide")
    setup_page()

    current_dir = os.path.dirname(os.path.abspath(__file__))

    logo_path = os.path.join(current_dir, 'bgu_logo.png')
    st.sidebar.image(logo_path)
    st.sidebar.markdown("""
    
        <div style="text-align: center;">
            <h3>שיטות סטטיסטיות בהנדסה</h3>
            <h4>362.1.3071</h4>
        </div>
    """, unsafe_allow_html=True)

    #st.title(" 🎲 ליל המזל הגדול! 🎲")
    st.markdown('<div class="top-header"><h1>🎲 ליל המזל הגדול! 🎲</h1></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 4, 1])

    with col2:
        image_path = os.path.join(current_dir, 'home_page_intro.png')

        st.image(image_path)



if __name__ == "__main__":
    main()