import streamlit as st
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

    #st.title(" 🎲 ליל המזל הגדול! 🎲")
    st.markdown('<div class="top-header"><h1>🎲 ליל המזל הגדול! 🎲</h1></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        st.image('home_page.png', use_container_width=True)



if __name__ == "__main__":
    main()