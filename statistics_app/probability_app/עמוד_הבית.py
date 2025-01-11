import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import math
import time
import pandas as pd
import seaborn as sns

from utils.helper_functions import setup_page









def main():
    setup_page()

    st.title(" 🎲 ליל המזל הגדול! 🎲")

    st.markdown("""

    ערב טוב וברוכים הבאים,
     הגעתם בדיוק בזמן - זהו ליל המזל שלכם!

    לפניכם נפתחות דלתות קזינו ההסתברות, המקום היחיד בעולם שבו כולם מנצחים... בידע! 🎯✨

    ### 🎓 איך משחקים?
    * בחרו משחק מהתפריט בצד ימין
    * נסו את המזל שלכם במשחקים השונים
    * גלו את התיאוריה שמאחורי כל משחק
    * תרגלו עם שאלות אמיתיות
    * והכי חשוב - תהנו בדרך! 🎪
    """)


if __name__ == "__main__":
    main()