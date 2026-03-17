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
    st.session_state.game_history_coin = []
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

        כאן תוכלו לתרגל וליישם מספר סוגי התפלגויות: ברנולי, בינומית, גיאומטרית ובינומית שלילית.

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
    if 'game_history_coin' not in st.session_state:
        st.session_state.game_history_coin = []
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'flip_count' not in st.session_state:
        st.session_state.flip_count = 0

    col_flips_input, col_flip, col_reset, col_space = st.columns([1, 1, 1, 1])

    with col_flips_input:
        num_flips = st.number_input(
            "מספר הטלות (1-100):",
            min_value=1,
            max_value=100,
            value=1,
            step=1
        )

    with col_flip:
        flip_button = st.button("הטלת המטבעות")
    with col_reset:
        reset_button = st.button("משחק חדש")
        if reset_button:
            reset_game()

    if flip_button:
        st.markdown('ההטלה האחרונה:')
        for _ in range(num_flips):
            st.session_state.flip_count += 1
            coin = flip_coin()
            is_lucky = coin == "עץ"  # Compare with string instead of number

            if is_lucky:
                st.session_state.score += 1

            # Add flip to history
            st.session_state.game_history_coin.append({
                'מספר הטלה': st.session_state.flip_count,
                'תוצאה': coin  # Use coin directly since it's already the correct string
            })

        # Display current flip with coin visualization (showing only the last flip)
        col_coin, col_score, col_space = st.columns([1, 1, 1])
        with col_coin:
            st.markdown(create_coin_svg(coin), unsafe_allow_html=True)

            # Display success rate stats
            success_data = calculate_success_rate(st.session_state.game_history_coin)

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

        with col_score:
            # Display flip distribution chart
            if st.session_state.game_history_coin:
                # Create two columns for the charts
                # st.markdown("התפלגות התוצאות:")
                result, counts = calculate_flip_distribution(st.session_state.game_history_coin)

                fig = go.Figure(data=[
                    go.Bar(x=[str(x) for x in result], y=counts)
                ])

                fig.update_layout(
                    xaxis_title="תוצאה",
                    yaxis_title="מספר הופעות",
                    title="                                                    :התפלגות התוצאות",
                    showlegend=False,
                    height=500,
                    yaxis=dict(
                        dtick=50  # Set y-axis tick interval to 1
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
        
        התפלגות של משתנה מקרי X אשר מקבל 1 עבור הצלחה ו-0 עבור כישלון.
        
        $Ber(q) \sim X$
        
        $q-1=$ $(0=P(x$ $\,$ ,  $q=$ $(1=P(x$
        
        $q=$ $E[X]$
        
        $(q-1)q=$ $Var[X]$
                
        <h3>התפלגות בינומית 📊</h3>
        
        מספר הצלחות ב-n ניסויי ברנולי בלתי תלויים.
        
        $B(n, q) \sim X$
        
        $^{n-x}(q-1)^{x}q\\binom{n}{x}=$ $(x=P(X$
        
        $nq=$ $E[X]$
        
        $(q-1)nq=$ $Var[X]$

        
        <h3>התפלגות בינומית שלילית 📊</h3>
        
        מספר הניסויים עד להצלחה ה-m.
        
        $NB(m, q) \sim X$
        
        $^{x-m}(q-1)^{m}q\\binom{1-x}{1-m}=$ $(x=P(X$
        
        $\\frac{m}{q} =$ $E[X]$
        
        $\\frac{m(1-q)}{^{2}q} =$ $Var[X]$
        
        <h3>התפלגות גיאומטרית 📊</h3>
        
        מקרה פרטי של התפלגות בינומית שלילית - מספר ניסויי ברנולי עד להצלחה ראשונה.
        
        מאופיינת בתכונת חוסר זכרון, היסטוריית ההתפלגות לא משפיעה על ההסתברות.
        
        $G(q) \sim X$
        
        $^{1-k}(q-1)q =$ $(k=P(X$
        
        $^{k}(q-1)-1 =$ $(k\geq P(X$
        
        $\\frac{1}{q} =$ $E[X]$
        
        $\\frac{q+1-}{^{2}q} =$ $Var[X]$
        

        </div>
    """, unsafe_allow_html=True)

# --- Practice Section ---
st.markdown('<div class="section-header"><h2>✍️ בואו נתרגל!</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(r"""
        <div class='practice-section'>
        בדיוק כמו במשחק, נתון מטבע סטנדרטי עם שני צדדים - עץ ופלי. תוצאה של "עץ" מזכה בנקודה.

        * יש לקחת 4 ספרות לאחר הנקודה (בשבר עשרוני) בכל שלב בחישוב ולהזין את התשובה הסופית באחוזים בדיוק של 2 ספרות (%XX.xx).
        * לכל שאלה יש 10 ניסיונות.
        </div>
    """, unsafe_allow_html=True)

# Definition of correct answers
correct_answers_coin = {
    "q1": 31.25,
    "q2": 22.66,
    "q3": 2.92,
    "q4": 0.37,
    "q5": 6.25
}

# Question 1
with col1:
    st.markdown("""
        <div class='question-box'>
        <h3>שאלה 1️⃣</h3>
         מה ההסתברות לזכות בנקודה בדיוק פעמיים מתוך 5 הטלות?
        </div>
    """, unsafe_allow_html=True)

    # Get the current attempt count from URL parameters
    q1_attempt_count = int(st.query_params.get("q1_attempts_coin", "0"))

    # Use a form for question 1
    with st.form(key="question1_coin_form"):
        q1_answer = st.number_input(
            "הכניסו את תשובתכם באחוזים:",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            key="q1_coin_input"
        )

        # Submit button (disabled if max attempts reached)
        q1_submit = st.form_submit_button(
            "בדיקת תשובה",
            disabled=(q1_attempt_count >= 10 or st.query_params.get("q1_status_coin") == "success")
        )

        # Process form submission inside the form
        if q1_submit:
            # Check if answer is correct
            is_correct = abs(q1_answer - correct_answers_coin["q1"]) < 0.1

            if is_correct:
                st.query_params["q1_status_coin"] = "success"
            else:
                # Increment attempt counter
                q1_attempt_count += 1

                # Update URL parameter
                st.query_params["q1_attempts_coin"] = str(q1_attempt_count)

                if q1_attempt_count >= 10:
                    st.query_params["q1_status_coin"] = "failed"
                else:
                    st.query_params["q1_status_coin"] = "trying"

        # Check if we need to show a previous result
        if "q1_status_coin" in st.query_params:
            status = st.query_params["q1_status_coin"]
            if status == "success":
                st.success(
                    f"כל הכבוד! התשובה הנכונה היא {correct_answers_coin['q1']}%.\n"
                    "\n"
                    "**הסבר:** זוהי שאלה על התפלגות בינומית.\n"
                    "אנחנו מחפשים את ההסתברות לקבל בדיוק 2 הצלחות מתוך 5 ניסיונות.\n"
                    "\n"
                    "נגדיר את המשתנה המקרי X כמספר ההצלחות (מספר הפעמים שיתקבל 'עץ') מתוך 5 ניסיונות.\n"
                    "בהתחשב בכך שההטלות בלתי תלויות, X מתפלג לפי התפלגות בינומית:\n"
                    "\n"
                    "X ~ B(5, 0.5)\n"
                    "\n"
                    "כלומר, מספר ההצלחות מתוך 5 ניסיונות, כאשר ההסתברות להצלחה בהטלה בודדת היא 0.5.\n"
                    "\n"
                    "נשתמש בנוסחה להתפלגות בינומית: P(X=k) = C(n,k) * p^k * (1-p)^(n-k)\n"
                    "כאשר:\n"
                    "- n = 5 (מספר ההטלות)\n"
                    "- k = 2 (מספר ההצלחות הרצוי)\n"
                    "- p = 0.5 (הסתברות להצלחה בהטלה בודדת)\n"
                    "\n"
                    "P(X=2) = C(5,2) * (0.5)^2 * (0.5)^3\n"
                    "= 10 * 0.25 * 0.125\n"
                    "= 0.3125 = 31.25%\n"
                )
            elif status == "failed":
                st.error(
                    f"כל הכבוד על הניסיון! בפעם הבאה תצליחו יותר.\n"
                    "\n"
                    f"התשובה הנכונה היא {correct_answers_coin['q1']}%.\n"
                    "\n"
                    "**הסבר:** זוהי שאלה על התפלגות בינומית.\n"
                    "אנחנו מחפשים את ההסתברות לקבל בדיוק 2 הצלחות מתוך 5 ניסיונות.\n"
                    "\n"
                    "נגדיר את המשתנה המקרי X כמספר ההצלחות (מספר הפעמים שיתקבל 'עץ') מתוך 5 ניסיונות.\n"
                    "בהתחשב בכך שההטלות בלתי תלויות, X מתפלג לפי התפלגות בינומית:\n"
                    "\n"
                    "X ~ B(5, 0.5)\n"
                    "\n"
                    "כלומר, מספר ההצלחות מתוך 5 ניסיונות, כאשר ההסתברות להצלחה בהטלה בודדת היא 0.5.\n"
                    "\n"
                    "נשתמש בנוסחה להתפלגות בינומית: P(X=k) = C(n,k) * p^k * (1-p)^(n-k)\n"
                    "כאשר:\n"
                    "- n = 5 (מספר ההטלות)\n"
                    "- k = 2 (מספר ההצלחות הרצוי)\n"
                    "- p = 0.5 (הסתברות להצלחה בהטלה בודדת)\n"
                    "\n"
                    "P(X=2) = C(5,2) * (0.5)^2 * (0.5)^3\n"
                    "= 10 * 0.25 * 0.125\n"
                    "= 0.3125 = 31.25%\n"
                )
            elif status == "trying":
                current_attempts = int(st.query_params.get("q1_attempts_coin", "0"))
                remaining = 10 - current_attempts
                st.error(f"לא מדויק. נסו שוב! נותרו {remaining} ניסיונות.")

# Question 2
with col1:
    st.markdown("""
        <div class='question-box'>
        <h3>שאלה 2️⃣</h3>
        מה ההסתברות שתזכו ב-5 נקודות לפחות כאשר תטילו את המטבע 7 פעמים?
        </div>
    """, unsafe_allow_html=True)

    # Get the current attempt count from URL parameters
    q2_attempt_count = int(st.query_params.get("q2_attempts_coin", "0"))

    # Use a form for question 2
    with st.form(key="question2_coin_form"):
        q2_answer = st.number_input(
            "הכניסו את תשובתכם באחוזים:",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            key="q2_coin_input"
        )

        # Submit button (disabled if max attempts reached)
        q2_submit = st.form_submit_button(
            "בדיקת תשובה",
            disabled=(q2_attempt_count >= 10 or st.query_params.get("q2_status_coin") == "success")
        )

        # Process form submission inside the form
        if q2_submit:
            # Check if answer is correct
            is_correct = abs(q2_answer - correct_answers_coin["q2"]) < 0.1

            if is_correct:
                st.query_params["q2_status_coin"] = "success"
            else:
                # Increment attempt counter
                q2_attempt_count += 1

                # Update URL parameter
                st.query_params["q2_attempts_coin"] = str(q2_attempt_count)

                if q2_attempt_count >= 10:
                    st.query_params["q2_status_coin"] = "failed"
                else:
                    st.query_params["q2_status_coin"] = "trying"

        # Check if we need to show a previous result
        if "q2_status_coin" in st.query_params:
            status = st.query_params["q2_status_coin"]
            if status == "success":
                st.success(
                    f"כל הכבוד! התשובה הנכונה היא {correct_answers_coin['q2']}%.\n"
                    "\n"
                    "**הסבר:** זוהי שאלה על התפלגות בינומית מצטברת.\n"
                    "אנחנו מחפשים את ההסתברות לקבל 5 או יותר הצלחות מתוך 7 ניסיונות.\n"
                    "\n"
                    "המשתנה המקרי X מתפלג לפי התפלגות בינומית:\n"
                    "X ~ B(7, 0.5)\n"
                    "\n"
                    "ההסתברות לקבל לפחות 5 נקודות מתוך 7 הטלות הינה:"
                    "\n"
                    "\n"
                    "P(X≥5) = P(X=5) + P(X=6) + P(X=7)\n"
                    " ,כאשר:\n"
                    "- n = 7 (מספר ההטלות)\n"
                    "- p = 0.5 (הסתברות להצלחה בהטלה בודדת)\n"
                    "\n"
                    "P(X=5) = C(7,5) * (0.5)^5 * (0.5)^2 = 0.1641"
                    "\n\n"
                    "P(X=6) = C(7,6) * (0.5)^6 * (0.5)^1 = 0.0547"
                    "\n\n"
                    "P(X=7) = C(7,7) * (0.5)^7 * (0.5)^0 = 0.0078"
                    "\n\n"
                    "סכום כל ההסתברויות: P(X ≥ 5) = 0.1641 + 0.0547 + 0.0078 = 0.2266\n"
                    "\n"
                    "ההסתברות לזכות ב-5 נקודות לפחות היא 0.2266, או **22.66%**."
                )
            elif status == "failed":
                st.error(
                    f"כל הכבוד על הניסיון! בפעם הבאה תצליחו יותר.\n"
                    "\n"
                    f"התשובה הנכונה היא {correct_answers_coin['q2']}%.\n"
                    "\n"
                    "**הסבר:** זוהי שאלה על התפלגות בינומית מצטברת.\n"
                    "אנחנו מחפשים את ההסתברות לקבל 5 או יותר הצלחות מתוך 7 ניסיונות.\n"
                    "\n"
                    "המשתנה המקרי X מתפלג לפי התפלגות בינומית:\n"
                    "X ~ B(7, 0.5)\n"
                    "\n"
                    "ההסתברות לקבל לפחות 5 נקודות מתוך 7 הטלות הינה:"
                    "\n"
                    "\n"
                    "P(X≥5) = P(X=5) + P(X=6) + P(X=7)\n"
                    " ,כאשר:\n"
                    "- n = 7 (מספר ההטלות)\n"
                    "- p = 0.5 (הסתברות להצלחה בהטלה בודדת)\n"
                    "\n"
                    "P(X=5) = C(7,5) * (0.5)^5 * (0.5)^2 = 0.1641"
                    "\n\n"
                    "P(X=6) = C(7,6) * (0.5)^6 * (0.5)^1 = 0.0547"
                    "\n\n"
                    "P(X=7) = C(7,7) * (0.5)^7 * (0.5)^0 = 0.0078"
                    "\n\n"
                    "סכום כל ההסתברויות: P(X ≥ 5) = 0.1641 + 0.0547 + 0.0078 = 0.2266\n"
                    "\n"
                    "ההסתברות לזכות ב-5 נקודות לפחות היא 0.2266, או **22.66%**."
                )
            elif status == "trying":
                current_attempts = int(st.query_params.get("q2_attempts_coin", "0"))
                remaining = 10 - current_attempts
                st.error(f"לא מדויק. נסו שוב! נותרו {remaining} ניסיונות.")

# Question 3
with col1:
    st.markdown("""
        <div class='question-box'>
        <h3>שאלה 3️⃣</h3>
        כעת קיבלתם מטבע לא הוגן שמציג עץ רק ב-30% מהפעמים.
        מה ההסתברות שתצטרכו בדיוק 8 הטלות כדי לקבל 5 נקודות?
        </div>
    """, unsafe_allow_html=True)

    # Get the current attempt count from URL parameters
    q3_attempt_count = int(st.query_params.get("q3_attempts_coin", "0"))

    # Use a form for question 3
    with st.form(key="question3_coin_form"):
        q3_answer = st.number_input(
            "הכניסו את תשובתכם באחוזים:",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            key="q3_coin_input"
        )

        # Submit button (disabled if max attempts reached)
        q3_submit = st.form_submit_button(
            "בדיקת תשובה",
            disabled=(q3_attempt_count >= 10 or st.query_params.get("q3_status_coin") == "success")
        )

        # Process form submission inside the form
        if q3_submit:
            # Check if answer is correct
            is_correct = abs(q3_answer - correct_answers_coin["q3"]) < 0.1

            if is_correct:
                st.query_params["q3_status_coin"] = "success"
            else:
                # Increment attempt counter
                q3_attempt_count += 1

                # Update URL parameter
                st.query_params["q3_attempts_coin"] = str(q3_attempt_count)

                if q3_attempt_count >= 10:
                    st.query_params["q3_status_coin"] = "failed"
                else:
                    st.query_params["q3_status_coin"] = "trying"

        # Check if we need to show a previous result
        if "q3_status_coin" in st.query_params:
            status = st.query_params["q3_status_coin"]
            if status == "success":
                st.success(
                    f"כל הכבוד! התשובה הנכונה היא {correct_answers_coin['q3']}%.\n"
                    "\n"
                    "**הסבר:** זוהי שאלה על התפלגות בינומית שלילית.\n"
                    "אנחנו מחפשים את ההסתברות שיידרשו בדיוק 8 ניסיונות כדי לקבל בדיוק 5 הצלחות (5 נקודות).\n"
                    "\n"
                    "המשתנה המקרי X מתפלג לפי התפלגות בינומית שלילית עם פרמטרים:\n"
                    "X ~ NB(5, 0.3)\n"
                    "כאשר n = 8 (מספר הניסיונות הכוללים) ו- p = 0.3 (הסתברות להצלחה).\n"
                    "\n"
                    "נחשב את ההסתברות לקבל בדיוק 5 הצלחות מתוך 8 ניסיונות:\n"
                    "\n"
                    "P(X = 8) = C(8 - 1, 5 - 1) * (0.3)^5 * (0.7)^3 = 0.0292\n"
                    "\n"
                    "ההסתברות שיידרשו בדיוק 8 ניסיונות כדי לקבל 5 נקודות היא 0.0292, או **2.92%**."
                )
            elif status == "failed":
                st.error(
                    f"כל הכבוד על הניסיון! בפעם הבאה תצליחו יותר.\n"
                    "\n"
                    f"התשובה הנכונה היא {correct_answers_coin['q3']}%.\n"
                    "\n"
                    "**הסבר:** זוהי שאלה על התפלגות בינומית שלילית.\n"
                    "אנחנו מחפשים את ההסתברות שיידרשו בדיוק 8 ניסיונות כדי לקבל בדיוק 5 הצלחות (5 נקודות).\n"
                    "\n"
                    "המשתנה המקרי X מתפלג לפי התפלגות בינומית שלילית עם פרמטרים:\n"
                    "X ~ NB(5, 0.3)\n"
                    "כאשר n = 8 (מספר הניסיונות הכוללים) ו- p = 0.3 (הסתברות להצלחה).\n"
                    "\n"
                    "נחשב את ההסתברות לקבל בדיוק 5 הצלחות מתוך 8 ניסיונות:\n"
                    "\n"
                    "P(X = 8) = C(8 - 1, 5 - 1) * (0.3)^5 * (0.7)^3 = 0.0292\n"
                    "\n"
                    "ההסתברות שיידרשו בדיוק 8 ניסיונות כדי לקבל 5 נקודות היא 0.0292, או **2.92%**."
                )
            elif status == "trying":
                current_attempts = int(st.query_params.get("q3_attempts_coin", "0"))
                remaining = 10 - current_attempts
                st.error(f"לא מדויק. נסו שוב! נותרו {remaining} ניסיונות.")

# Question 4
with col1:
    st.markdown("""
        <div class='question-box'>
        <h3>שאלה 4️⃣</h3>
        מטילים את אותו מטבע לא הוגן 15 פעמים.
        מה הסיכוי שתקבלו בין 10 ל-12 נקודות?
        </div>
    """, unsafe_allow_html=True)

    # Get the current attempt count from URL parameters
    q4_attempt_count = int(st.query_params.get("q4_attempts_coin", "0"))

    # Use a form for question 4
    with st.form(key="question4_coin_form"):
        q4_answer = st.number_input(
            "הכניסו את תשובתכם באחוזים:",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            key="q4_coin_input"
        )

        # Submit button (disabled if max attempts reached)
        q4_submit = st.form_submit_button(
            "בדיקת תשובה",
            disabled=(q4_attempt_count >= 10 or st.query_params.get("q4_status_coin") == "success")
        )

        # Process form submission inside the form
        if q4_submit:
            # Check if answer is correct
            is_correct = abs(q4_answer - correct_answers_coin["q4"]) < 0.1

            if is_correct:
                st.query_params["q4_status_coin"] = "success"
            else:
                # Increment attempt counter
                q4_attempt_count += 1

                # Update URL parameter
                st.query_params["q4_attempts_coin"] = str(q4_attempt_count)

                if q4_attempt_count >= 10:
                    st.query_params["q4_status_coin"] = "failed"
                else:
                    st.query_params["q4_status_coin"] = "trying"

        # Check if we need to show a previous result
        if "q4_status_coin" in st.query_params:
            status = st.query_params["q4_status_coin"]
            if status == "success":
                st.success(
                    f"כל הכבוד! התשובה הנכונה היא {correct_answers_coin['q4']}%.\n"
                    "\n"
                    "**הסבר:** זוהי שאלה על התפלגות בינומית.\n"
                    "אנחנו מחפשים את ההסתברות לקבל בין 10 ל-12 הצלחות מתוך 15 ניסיונות.\n"
                    "\n"
                    "המשתנה המקרי X מתפלג לפי התפלגות בינומית עם פרמטרים:\n"
                    "X ~ B(15, 0.3)\n"
                    "כאשר n = 15 (מספר ההטלות) ו- p = 0.3 (הסתברות להצלחה).\n"
                    "\n"
                    "נחשב את ההסתברויות עבור 10, 11 ו-12 הצלחות:\n"
                    "\n"
                    "P(X=10) = C(15, 10) * (0.3)^10 * (0.7)^5 = 0.0030\n"
                    "\n"
                    "P(X=11) = C(15, 11) * (0.3)^11 * (0.7)^4 = 0.0006\n"
                    "\n"
                    "P(X=12) = C(15, 12) * (0.3)^12 * (0.7)^3 = 0.0001\n"
                    "\n"
                    "הסכום הכולל: P(10 ≤ X ≤ 12) = 0.0030 + 0.0006 + 0.0001 = 0.0037\n"
                    "\n"
                    "ההסתברות לקבל בין 10 ל-12 נקודות היא 0.0037, או **0.37%**."
                )
            elif status == "failed":
                st.error(
                    f"כל הכבוד על הניסיון! בפעם הבאה תצליחו יותר.\n"
                    "\n"
                    f"התשובה הנכונה היא {correct_answers_coin['q4']}%.\n"
                    "\n"
                    "**הסבר:** זוהי שאלה על התפלגות בינומית.\n"
                    "אנחנו מחפשים את ההסתברות לקבל בין 10 ל-12 הצלחות מתוך 15 ניסיונות.\n"
                    "\n"
                    "המשתנה המקרי X מתפלג לפי התפלגות בינומית עם פרמטרים:\n"
                    "X ~ B(15, 0.3)\n"
                    "כאשר n = 15 (מספר ההטלות) ו- p = 0.3 (הסתברות להצלחה).\n"
                    "\n"
                    "נחשב את ההסתברויות עבור 10, 11 ו-12 הצלחות:\n"
                    "\n"
                    "P(X=10) = C(15, 10) * (0.3)^10 * (0.7)^5 = 0.0030\n"
                    "\n"
                    "P(X=11) = C(15, 11) * (0.3)^11 * (0.7)^4 = 0.0006\n"
                    "\n"
                    "P(X=12) = C(15, 12) * (0.3)^12 * (0.7)^3 = 0.0001\n"
                    "\n"
                    "הסכום הכולל: P(10 ≤ X ≤ 12) = 0.0030 + 0.0006 + 0.0001 = 0.0037\n"
                    "\n"
                    "ההסתברות לקבל בין 10 ל-12 נקודות היא 0.0037, או **0.37%**."
                )
            elif status == "trying":
                current_attempts = int(st.query_params.get("q4_attempts_coin", "0"))
                remaining = 10 - current_attempts
                st.error(f"לא מדויק. נסו שוב! נותרו {remaining} ניסיונות.")

# Question 5
with col1:
    st.markdown("""
        <div class='question-box'>
        <h3>שאלה 5️⃣</h3>
        נחזור למטבע ההוגן.
        מה ההסתברות שתצליחו לזכות בנקודה רק אחרי 4 הטלות?
        </div>
    """, unsafe_allow_html=True)

    # Get the current attempt count from URL parameters
    q5_attempt_count = int(st.query_params.get("q5_attempts_coin", "0"))

    # Use a form for question 5
    with st.form(key="question5_coin_form"):
        q5_answer = st.number_input(
            "הכניסו את תשובתכם באחוזים:",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            key="q5_coin_input"
        )

        # Submit button (disabled if max attempts reached)
        q5_submit = st.form_submit_button(
            "בדיקת תשובה",
            disabled=(q5_attempt_count >= 10 or st.query_params.get("q5_status_coin") == "success")
        )

        # Process form submission inside the form
        if q5_submit:
            # Check if answer is correct
            is_correct = abs(q5_answer - correct_answers_coin["q5"]) < 0.1

            if is_correct:
                st.query_params["q5_status_coin"] = "success"
            else:
                # Increment attempt counter
                q5_attempt_count += 1

                # Update URL parameter
                st.query_params["q5_attempts_coin"] = str(q5_attempt_count)

                if q5_attempt_count >= 10:
                    st.query_params["q5_status_coin"] = "failed"
                else:
                    st.query_params["q5_status_coin"] = "trying"

        # Check if we need to show a previous result
        if "q5_status_coin" in st.query_params:
            status = st.query_params["q5_status_coin"]
            if status == "success":
                st.success(
                    f"כל הכבוד! התשובה הנכונה היא {correct_answers_coin['q5']}%.\n"
                    "\n"
                    "**הסבר:** זוהי שאלה על הסתברות גיאומטרית.\n"
                    "ההסתברות הגיאומטרית עוסקת במצבים שבהם אנחנו רוצים לדעת מה ההסתברות לקבל את ההצלחה הראשונה בהטלה ה-k.\n"
                    "\n"
                    "במקרה שלנו, אנחנו מחפשים את ההסתברות שההצלחה הראשונה (כלומר, 'עץ') תקרה בהטלה ה-4.\n"
                    "\n"
                    "הנוסחה להסתברות גיאומטרית היא:\n"
                    "P(X = k) = (1 - p)^(k-1) * p\n"
                    "כאשר:\n"
                    "- p = 0.5 (ההסתברות להצלחה בהטלה)\n"
                    "- k = 4 (ההטלה הראשונה בה נקבל 'עץ')\n"
                    "\n"
                    "נחשב את ההסתברות:\n"
                    "P(X = 4) = (1 - 0.5)^(4-1) * 0.5 = (0.5)^3 * 0.5 = 0.0625\n"
                    "\n"
                    "ההסתברות לקבל 'עץ' לראשונה בהטלה ה-4 היא 0.0625, או **6.25%**."
                )
            elif status == "failed":
                st.error(
                    f"כל הכבוד על הניסיון! בפעם הבאה תצליחו יותר.\n"
                    "\n"
                    f"התשובה הנכונה היא {correct_answers_coin['q5']}%.\n"
                    "\n"
                    "**הסבר:** זוהי שאלה על הסתברות גיאומטרית.\n"
                    "ההסתברות הגיאומטרית עוסקת במצבים שבהם אנחנו רוצים לדעת מה ההסתברות לקבל את ההצלחה הראשונה בהטלה ה-k.\n"
                    "\n"
                    "במקרה שלנו, אנחנו מחפשים את ההסתברות שההצלחה הראשונה (כלומר, 'עץ') תקרה בהטלה ה-4.\n"
                    "\n"
                    "הנוסחה להסתברות גיאומטרית היא:\n"
                    "P(X = k) = (1 - p)^(k-1) * p\n"
                    "כאשר:\n"
                    "- p = 0.5 (ההסתברות להצלחה בהטלה)\n"
                    "- k = 4 (ההטלה הראשונה בה נקבל 'עץ')\n"
                    "\n"
                    "נחשב את ההסתברות:\n"
                    "P(X = 4) = (1 - 0.5)^(4-1) * 0.5 = (0.5)^3 * 0.5 = 0.0625\n"
                    "\n"
                    "ההסתברות לקבל 'עץ' לראשונה בהטלה ה-4 היא 0.0625, או **6.25%**."
                )
            elif status == "trying":
                current_attempts = int(st.query_params.get("q5_attempts_coin", "0"))
                remaining = 10 - current_attempts
                st.error(f"לא מדויק. נסו שוב! נותרו {remaining} ניסיונות.")