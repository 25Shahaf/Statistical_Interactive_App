import streamlit as st
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import math
import os
import random
import pandas as pd
from utils.helper_functions import setup_page, under_development_page


# --- Helper Functions ---

def reset_game():
    """Reset all game state variables."""
    st.session_state.game_history = []
    st.session_state.score = 0
    st.session_state.flip_count = 0


def flip_coin():
    """
    Simulate a coin flip.
    Returns: str - "עץ" or "פלי"
    """
    return random.choice(["עץ", "פלי"])  # Return string directly instead of 0/1

def create_coin_svg(result):
    """
    Create an SVG representation of a coin with the given result.
    Args:
        result (str): The result of the coin flip ("עץ" or "פלי")
    Returns:
        str: SVG markup for the coin
    """
    text = result  # Use the result string directly since it's already "עץ" or "פלי"
    return f'''
    <svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <radialGradient id="coinGradient" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
                <stop offset="0%" style="stop-color:#FFD700"/>
                <stop offset="100%" style="stop-color:#B8860B"/>
            </radialGradient>
        </defs>
        <circle cx="100" cy="100" r="90" fill="url(#coinGradient)" 
                stroke="#8B4513" stroke-width="5"/>
        <text x="100" y="115" font-family="Arial" font-size="40" 
              text-anchor="middle" fill="#8B4513" font-weight="bold">
            {text}
        </text>
    </svg>
    '''


def calculate_flip_distribution(history):
    """
    Calculate the distribution of coin flip results.
    Args:
        history (list): List of dictionaries containing flip history
    Returns:
        tuple: Lists of results and their counts
    """
    df = pd.DataFrame(history)
    result_counts = df['תוצאה'].value_counts()
    return result_counts.index.tolist(), result_counts.values.tolist()


def calculate_success_rate(history):
    """
    Calculate the success rate of coin flips.
    Args:
        history (list): List of dictionaries containing flip history
    Returns:
        dict: Success and failure percentages
    """
    if not history:
        return {'הצלחה': 0, 'כישלון': 0}

    df = pd.DataFrame(history)
    total_flips = len(df)
    successes = len(df[df['תוצאה'] == 'עץ'])

    success_rate = (successes / total_flips) * 100
    failure_rate = 100 - success_rate

    return {
        'הצלחה': round(success_rate, 1),
        'כישלון': round(failure_rate, 1)
    }

# --- Page Content ---
st.set_page_config(layout="wide")
setup_page()

# -- Sidebar --
current_dir = os.path.dirname(os.path.abspath(__file__))

logo_path = os.path.join(current_dir, 'bgu_logo.png')
st.sidebar.image(logo_path)
st.sidebar.markdown("""

        <div style="text-align: center;">
            <h3>שיטות סטטיסטיות בהנדסה</h3>
            <h4>362.1.3071</h4>
        </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="top-header"><h1>מטבע הזהב 🪙</h1></div>', unsafe_allow_html=True)

# --- game explanation ---
st.markdown('<div class="section-header"><h2>🎮 המשחק</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
        <div class='game-explanation'>
        <h3>ברוכים הבאים למשחק מטבע הזהב!</h3>

        כאן תוכלו לתרגל וליישם התפלגות ברנולי, התפלגות בינומית, התפלגות גיאומטרית והתפלגות בינומית שלילית.

        <h4>חוקי המשחק:</h4>
        ברשותכם מטבע סטנדרטי עם שני צדדים - עץ ופלי.
        הטילו את המטבע ובדקו מה יצא.

        רק תוצאה של "עץ" מזכה בנקודה.

        </div>
    """, unsafe_allow_html=True)

# --- game-zone ---
col1, col2 = st.columns([4, 1])

with col1:
    # Initialize session state for game history and score
    if 'game_history' not in st.session_state:
        st.session_state.game_history = []
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'flip_count' not in st.session_state:
        st.session_state.flip_count = 0

    # Create two columns for the buttons
    col_flip, col_reset, col_space = st.columns([1, 1, 2])

    with col_flip:
        flip_button= st.button("הטלת מטבע")
    with col_reset:
        reset_button = st.button("משחק חדש")
        if reset_button:
            reset_game()

    if flip_button:
        st.session_state.flip_count += 1
        coin = flip_coin()
        is_lucky = coin == "עץ"  # Compare with string instead of number

        if is_lucky:
            st.session_state.score += 1

        # Add flip to history
        st.session_state.game_history.append({
            'מספר הטלה': st.session_state.flip_count,
            'תוצאה': coin  # Use coin directly since it's already the correct string
        })

        # Display current flip with coin visualization
        col_coin, col_score, col_space = st.columns([1, 1, 1])
        with col_coin:
            st.markdown(create_coin_svg(coin), unsafe_allow_html=True)

        # Display score
        st.markdown(f"ניקוד מצטבר: {st.session_state.score}")

        with col_score:
            success_data = calculate_success_rate(st.session_state.game_history)

            # Create success rate display
            st.markdown(f"""
                <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center;'>
                <h4>אחוזי הצלחה מצטברים:</h4>
                    <div style='font-size: 1.2em; margin: 10px 0; color: black;'>
                        🏅 הצלחה: {success_data['הצלחה']}%
                    </div>
                    <div style='font-size: 1.2em; margin: 10px 0; color: black;'>
                        ❌ כישלון: {success_data['כישלון']}%
                    </div>
                    <div style='font-size: 0.9em; color: #666; margin-top: 10px;'>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # Display flip distribution chart
        if st.session_state.game_history:
            # Create two columns for the charts
            col_hist, col_space = st.columns([1,2])

            # Display flip distribution chart
            with col_hist:
                st.markdown("התפלגות התוצאות:")
                result, counts = calculate_flip_distribution(st.session_state.game_history)

                fig = go.Figure(data=[
                    go.Bar(x=[str(x) for x in result], y=counts)
                ])

                fig.update_layout(
                    xaxis_title="תוצאה",
                    yaxis_title="מספר הופעות",
                    showlegend=False,
                    height=500,
                    yaxis=dict(
                        dtick=1  # Set y-axis tick interval to 1
                    ),
                    xaxis=dict(
                        dtick=1  # Set x-axis tick interval to 1
                    )
                )

                st.plotly_chart(fig, use_container_width=True)


# --- Theory Section ---
st.markdown('<div class="section-header"><h2>📚 רקע תיאורטי</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
        <div class='theory-section'>
        <h3>התפלגות ברנולי 📊</h3>
        
        הסבר על התפלגות ברנולי.
        
        <h3>התפלגות בינומית 📊</h3>
        
        הסבר על התפלגות בינומית.
        
        <h3>התפלגות בינומית שלילית 📊</h3>
        
        הסבר על התפלגות בינומית שלילית.
        
        <h3>התפלגות גיאומטרית 📊</h3>
        
        הסבר על התפלגות גיאומטרית.

        </div>
    """, unsafe_allow_html=True)

# --- Practice Section ---
st.markdown('<div class="section-header"><h2>✍️ בואו נתרגל!</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(r"""
        <div class='practice-section'>
        בדיוק כמו במשחק, נתון מטבע סטנדרטי עם שני צדדים - עץ ופלי.

        * יש לקחת 2 ספרות לאחר הנקודה (באחוזים) בכל שלב בחישוב ולהזין את התשובה גם כן בדיוק של 2 ספרות.
        </div>
    """, unsafe_allow_html=True)

    # Question 1
    st.markdown("""
        <div class='question-box'>
        <h3>שאלה 1️⃣</h3>
         מה ההסתברות לזכות בנקודה בדיוק פעמיים מתוך 5 הטלות?
        </div>
    """, unsafe_allow_html=True)

    user_answer1 = st.number_input(
        "הכניסו את תשובתכם באחוזים:",
        min_value=0.0,
        max_value=100.0,
        step=0.1,
        key="q1"
    )

    if st.button("בדיקת תשובה", key="check1"):
        correct_answer = 31.25
        if user_answer1 == correct_answer:
            st.success(
                f"כל הכבוד! התשובה הנכונה היא {correct_answer}%.\n"
                "\n"
                "**הסבר:** זוהי שאלה על התפלגות בינומית.\n"
                "אנחנו מחפשים את ההסתברות לקבל בדיוק 2 הצלחות מתוך 5 ניסיונות.\n"
                "\n"
                "נשתמש בנוסחה: P(X=k) = C(n,k) * p^k * (1-p)^(n-k)\n"
                "כאשר:\n"
                "- n = 5 (מספר ההטלות)\n"
                "- k = 2 (מספר ההצלחות הרצוי)\n"
                "- p = 0.5 (הסתברות להצלחה בהטלה בודדת)\n"
                "\n"
                "P(X=2) = C(5,2) * (0.5)^2 * (0.5)^3\n"
                "= 10 * 0.25 * 0.125\n"
                "= 0.3125 = 31.25%\n"
            )
        else:
            st.error("לא מדויק. נסו שוב!")

    # Question 2
    st.markdown("""
        <div class='question-box'>
        <h3>שאלה 2️⃣</h3>
        מה ההסתברות שתזכו ב-5 נקודות לפחות כאשר תטילו את המטבע 7 פעמים?
        </div>
    """, unsafe_allow_html=True)

    user_answer = st.number_input(
        "הכניסו את תשובתכם באחוזים:",
        min_value=0.0,
        max_value=100.0,
        step=0.1,
        key="q2"
    )

    if st.button("בדיקת תשובה", key="check2"):
        correct_answer = 7.03
        if user_answer == correct_answer:
            st.success(
                f"כל הכבוד! התשובה הנכונה היא {correct_answer}%.\n"
                "\n"
                "**הסבר:** זוהי שאלה על התפלגות בינומית מצטברת.\n"
                "אנחנו מחפשים את ההסתברות לקבל 5 או יותר הצלחות מתוך 7 ניסיונות.\n"
                "\n"
                "P(X≥5) = P(X=5) + P(X=6) + P(X=7)\n"
                "כאשר:\n"
                "- n = 7 (מספר ההטלות)\n"
                "- p = 0.5 (הסתברות להצלחה בהטלה בודדת)\n"
                "\n"
                "\nP(X=5) = C(7,5) * (0.5)^5 * (0.5)^2 = 5.47%\n"
                "\nP(X=6) = C(7,6) * (0.5)^6 * (0.5)^1 = 0.78%\n"
                "\nP(X=7) = C(7,7) * (0.5)^7 * (0.5)^0 = 0.78%\n"
                "\n"
                "סכום כל ההסתברויות = 7.03%\n"
            )
        else:
            st.error("לא מדויק. נסו שוב!")

    # Question 3
    st.markdown("""
        <div class='question-box'>
        <h3>שאלה 3️⃣</h3>
        כעת קיבלתם מטבע לא הוגן שמציג עץ רק ב-30% מהפעמים.
        מה ההסתברות שתקבלו 5 נקודות אם תטילו את המטבע לכל היותר 8 פעמים?
        </div>
    """, unsafe_allow_html=True)

    user_answer = st.number_input(
        "הכניסו את תשובתכם באחוזים:",
        min_value=0.0,
        max_value=100.0,
        step=0.1,
        key="q3"
    )

    if st.button("בדיקת תשובה", key="check3"):
        correct_answer = 5.62
        if abs(user_answer - correct_answer) < 0.01:
            st.success(
                f"כל הכבוד! התשובה הנכונה היא {correct_answer}%.\n"
                "\n"
                "**הסבר:** זוהי שאלה על התפלגות בינומית שלילית.\n"
                "אנחנו מחפשים את ההסתברות לקבל בדיוק 5 הצלחות תוך 8 ניסיונות או פחות.\n"
                "\n"
                "נחשב את ההסתברות לקבל 5 הצלחות בכל אחד מהניסיונות מ-5 עד 8:\n"
                "P(X=5) + P(X=6) + P(X=7) + P(X=8)\n"
                "\n"
                "כאשר:\n"
                "- r = 5 (מספר ההצלחות הרצוי)\n"
                "- p = 0.3 (הסתברות להצלחה)\n"
                "\n"
                "חישוב מדויק נותן:\n"
                "0.0562 = 5.62%\n"
            )
        else:
            st.error("לא מדויק. נסו שוב!")

    # Question 4
    st.markdown("""
        <div class='question-box'>
        <h3>שאלה 4️⃣</h3>
        מטילים את אותו מטבע לא הוגן 15 פעמים.
        מה הסיכוי שתקבלו בין 10 ל-12 נקודות?
        </div>
    """, unsafe_allow_html=True)

    user_answer = st.number_input(
        "הכניסו את תשובתכם באחוזים:",
        min_value=0.0,
        max_value=100.0,
        step=0.1,
        key="q4"
    )

    if st.button("בדיקת תשובה", key="check4"):
        correct_answer = 15.33
        if abs(user_answer - correct_answer) < 0.01:
            st.success(
                f"כל הכבוד! התשובה הנכונה היא {correct_answer}%.\n"
                "\n"
                "**הסבר:** זוהי שאלה על התפלגות בינומית.\n"
                "אנחנו מחפשים את ההסתברות לקבל בין 10 ל-12 הצלחות (כולל) מתוך 15 ניסיונות.\n"
                "\n"
                "P(10≤X≤12) = P(X=10) + P(X=11) + P(X=12)\n"
                "כאשר:\n"
                "- n = 15 (מספר ההטלות)\n"
                "- p = 0.3 (הסתברות להצלחה)\n"
                "\n"
                "P(X=10) = C(15,10) * (0.3)^10 * (0.7)^5 = 0.0775\n"
                "P(X=11) = C(15,11) * (0.3)^11 * (0.7)^4 = 0.0504\n"
                "P(X=12) = C(15,12) * (0.3)^12 * (0.7)^3 = 0.0254\n"
                "\n"
                "סכום ההסתברויות = 0.1533 = 15.33%\n"
            )
        else:
            st.error("לא מדויק. נסו שוב!")

    # Question 5
    st.markdown("""
         <div class='question-box'>
         <h3>שאלה 5️⃣</h3>
         נחזור למטבע ההוגן.
         מה ההסתברות שתצטרכו בדיוק 6 הטלות כדי לקבל 3 נקודות?
         </div>
     """, unsafe_allow_html=True)

    user_answer = st.number_input(
        "הכניסו את תשובתכם באחוזים:",
        min_value=0.0,
        max_value=100.0,
        step=0.1,
        key="q5"
    )

    if st.button("בדיקת תשובה", key="check5"):
        correct_answer = 15.63
        if abs(user_answer - correct_answer) < 0.01:
            st.success(
                f"כל הכבוד! התשובה הנכונה היא {correct_answer}%.\n"
                "\n"
                "**הסבר:** זוהי שאלה על התפלגות בינומית שלילית (או התפלגות פסקל).\n"
                "אנחנו מחפשים את ההסתברות לקבל את ההצלחה השלישית בדיוק בניסיון השישי.\n"
                "\n"
                "נשתמש בנוסחה: P(X=n) = C(n-1,r-1) * p^r * (1-p)^(n-r)\n"
                "כאשר:\n"
                "- n = 6 (מספר הניסיון הספציפי)\n"
                "- r = 3 (מספר ההצלחות הרצוי)\n"
                "- p = 0.5 (הסתברות להצלחה)\n"
                "\n"
                "P(X=6) = C(5,2) * (0.5)^3 * (0.5)^3\n"
                "= 10 * 0.125 * 0.125\n"
                "= 0.15625 = 15.63%\n"
            )
        else:
            st.error("לא מדויק. נסו שוב!")