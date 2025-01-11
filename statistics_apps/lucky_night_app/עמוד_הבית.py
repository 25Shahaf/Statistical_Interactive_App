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

    col1, col2, col3, col4 = st.columns([1, 2, 2, 1])

    with col2:

        st.markdown("""
        ערב טוב וברוכים הבאים,
        \n
         הגעתם בדיוק בזמן - זהו ליל המזל שלכם!
    
        לפניכם נפתחות דלתות קזינו ההסתברות, המקום היחיד בעולם שבו כולם מנצחים... בידע! 🎯✨
    
        ### 🎓 איך משחקים?
        * בחרו משחק מהתפריט בצד ימין
        * נסו את המזל שלכם במשחקים השונים
        * גלו את התיאוריה שמאחורי כל משחק
        * תרגלו עם שאלות אמיתיות
        * והכי חשוב - תהנו בדרך! 🎪
        """)
    with col3:
        image = Image.open("casino.png")
        new_width = int(image.width * 0.4)
        new_height = int(image.height * 0.4)
        image = image.resize((new_width, new_height))
        st.image(image)


if __name__ == "__main__":
    main()