import streamlit as st
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import math
import os
import random
import pandas as pd
from utils.helper_functions import setup_page, under_development_page


# --- Helper Functions ---

def reset_game():
    """Reset all game state variables."""
    st.session_state.game_history_money = []
    st.session_state.total_caught = 0
    st.session_state.round_count = 0


def simulate_money_drop(rate=5):
    """
    Simulate a Poisson process of money dropping.

    Args:
        rate (float): The rate parameter (lambda) for the Poisson distribution.
                     Represents the average number of bills dropped per minute.

    Returns:
        int: Number of bills dropped in one minute.
    """
    # מימוש פואסון עם numpy - אין צורך ב-scipy
    return np.random.poisson(rate)


def poisson_pmf(k, lam):
    """
    Calculate Poisson probability mass function.

    Args:
        k (int): The number of occurrences
        lam (float): The rate parameter (lambda)

    Returns:
        float: The probability of exactly k occurrences
    """
    # מימוש ידני של PMF של פואסון
    return (lam ** k) * (math.exp(-lam)) / math.factorial(k)


def display_money_emojis(num_bills):
    """
    Display money bills using emojis.

    Args:
        num_bills (int): The number of bills caught
    """
    emoji = "💵"

    # מגבילים את מספר האימוג'ים המוצגים כדי שהמסך לא יהיה עמוס מדי
    display_count = min(num_bills, 15)

    # מציגים את השטרות כאימוג'ים
    emoji_display = f"<h1 style='text-align: center;'>{emoji * display_count}</h1>"

    # אם יש יותר שטרות ממה שהחלטנו להציג, נוסיף הודעה
    if num_bills > display_count:
        emoji_display += f"<p style='text-align: center;'>+עוד {num_bills - display_count} שטרות</p>"

    st.markdown(emoji_display, unsafe_allow_html=True)

    # הצגת הסכום הכולל

    st.markdown(f"""
           <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center;'>
           <h3>זכית ב-{num_bills} שטרות!</h3>
            
            <h3>סך הכל: ₪{num_bills * 20}</h3>
           </div>
       """, unsafe_allow_html=True)
    return ""


def calculate_catches_distribution(history):
    """
    Calculate the distribution of caught bills.

    Args:
        history (list): List of dictionaries containing game history

    Returns:
        tuple: Lists of results and their counts
    """
    df = pd.DataFrame(history)
    result_counts = df['מספר שטרות'].value_counts().sort_index()
    return result_counts.index.tolist(), result_counts.values.tolist()


def calculate_success_stats(history):
    """
    Calculate statistics about catching money.

    Args:
        history (list): List of dictionaries containing game history

    Returns:
        dict: Dictionary with various statistics
    """
    if not history:
        return {
            'ממוצע': 0,
            'מקסימום': 0,
            'שונות': 0
        }

    df = pd.DataFrame(history)
    catches = df['מספר שטרות']

    mean_catches = catches.mean()
    max_catches = catches.max()
    variance = catches.var() if len(catches) > 1 else 0

    return {
        'ממוצע': round(mean_catches, 2),
        'מקסימום': max_catches,
        'שונות': round(variance, 2)
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

st.markdown('<div class="top-header"><h1>גשם של שטרות 💵</h1></div>', unsafe_allow_html=True)

# --- game explanation ---
st.markdown('<div class="section-header"><h2>🎮 המשחק</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
        <div class='game-explanation'>
        <h3>ברוכים הבאים למשחק גשם של שטרות!</h3>

        כאן תוכלו לתרגל וליישם את התפלגות פואסון והתפלגות מעריכית.

        <h4>חוקי המשחק:</h4>
        אתם נכנסים לתא מיוחד שבתקרה שלו נמצאת מכונה המפילה שטרות של 20 ש"ח.
        
        
        המכונה מפילה שטרות בקצב ממוצע של 5 שטרות בדקה.
        משך כל משחק הוא דקה אחת, והפרס שלכם הוא השטרות שנופלים בזמן המשחק.
        
        **חישבו:** כיצד התוחלת והשונות משתנים ככל שמספר המשחקים גדל?

        </div>
    """, unsafe_allow_html=True)

# --- game-zone ---
col1, col2 = st.columns([4, 1])

with col1:
    # Initialize session state for game history and score
    if 'game_history_money' not in st.session_state:
        st.session_state.game_history_money = []
    if 'total_caught' not in st.session_state:
        st.session_state.total_caught = 0
    if 'round_count' not in st.session_state:
        st.session_state.round_count = 0

    col_rounds_input, col_play, col_reset, col_space = st.columns([1, 1, 1, 1])

    with col_rounds_input:
        num_rounds = st.number_input(
            "מספר משחקים (1-50):",
            min_value=1,
            max_value=50,
            value=1,
            step=1
        )

    with col_play:
        play_button = st.button("התחלת המשחק")
    with col_reset:
        reset_button = st.button("משחק חדש")
        if reset_button:
            reset_game()

    if play_button:
        st.markdown('תוצאות המשחק האחרון:')
        for _ in range(num_rounds):
            st.session_state.round_count += 1
            num_bills = simulate_money_drop(rate=5)
            st.session_state.total_caught += num_bills

            # Add round to history
            st.session_state.game_history_money.append({
                'מספר משחק': st.session_state.round_count,
                'מספר שטרות': num_bills,
                'ערך כולל': num_bills * 20
            })

        # Display current game visualization and stats
        col_visual, col_stats, col_space = st.columns([2, 1, 1])

        with col_visual:
            # Show the money animation for the last game
            last_bills = st.session_state.game_history_money[-1]['מספר שטרות']
            st.markdown(display_money_emojis(last_bills), unsafe_allow_html=True)

        with col_stats:
            # Display catch statistics
            success_stats = calculate_success_stats(st.session_state.game_history_money)

            # Create statistics display
            st.markdown(f"""
                <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center;'>
                <h4>סטטיסטיקה מצטברת:</h4>
                    <div style='font-size: 1.2em; margin: 10px 0; color: black;'>
                        📊 ממוצע שטרות: {success_stats['ממוצע']}
                    </div>
                    <div style='font-size: 1.2em; margin: 10px 0; color: black;'>
                    📏 שונות:     {success_stats['שונות']}
                    </div>
                    <div style='font-size: 1.2em; margin: 10px 0; color: green;'>
                        💰 סך הכל: ₪{st.session_state.total_caught * 20}
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # Display distribution chart
        if st.session_state.game_history_money:
            #st.markdown("### התפלגות השטרות שנתפסו:")

            # Create distribution chart
            results, counts = calculate_catches_distribution(st.session_state.game_history_money)

            fig = go.Figure(data=[
                go.Bar(x=[str(x) for x in results], y=counts, name="מספר המשחקים")
            ])

            # Calculate Poisson expected distribution for comparison
            max_val = max(results) if results else 10
            x_values = list(range(max_val + 1))

            # Calculate expected frequencies based on Poisson with lambda=5 (מימוש ידני במקום scipy)
            expected_probs = [poisson_pmf(k, 5) for k in x_values]
            num_games = len(st.session_state.game_history_money)
            expected_counts = [prob * num_games for prob in expected_probs]

            # Add expected Poisson line
            fig.add_trace(
                go.Scatter(
                    x=[str(x) for x in x_values],
                    y=expected_counts,
                    mode='lines+markers',
                    name='התפלגות פואסון תיאורטית (λ=5)',
                    line=dict(color='red', width=2)
                )
            )

            fig.update_layout(
                xaxis_title="מספר שטרות",
                yaxis_title="מספר פעמים",
                title="                                                                                                                                                                                     התפלגות מספר השטרות בכל משחק",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                height=400,
                xaxis=dict(
                    dtick=1  # הגדר קפיצות של 1 בציר ה-X
                )
            )

            st.plotly_chart(fig, use_container_width=True)

# --- Theory Section ---
st.markdown('<div class="section-header"><h2>📚 רקע תיאורטי</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(r"""
        <div class='theory-section'>
        <h3>התפלגות פואסון 📊</h3>

        התפלגות פואסון מתארת את מספר האירועים שמתרחשים בפרק זמן קבוע, כאשר האירועים מתרחשים בקצב ממוצע קבוע וכל אירוע הוא בלתי תלוי באירועים האחרים.
        
        משתנה מקרי עם התפלגות פואסון מקבל ערכים לא שליליים ומציין את מספר האירועים ביחידת זמן מתוך זרם אירועים פואסוני עם קצב של $\lambda$ אירועים ליחידת זמן כלשהי.

        $Poisson(\lambda) \sim X $
        
        $\frac{^{\lambda -}\lambda ^{x}e}{!x} =$ $(x=P(X$
        
        $\lambda = E[X]$

        $\lambda = Var[X]$
        
        <h3>התפלגות מעריכית 📊</h3>

        התפלגות מעריכית מתארת מספר יחידות מידה בין שני מופעים פואסונים. 
        
        התפלגות זאת הינה בעלת תכונת חוסר זכרון ולכן, בהינתן מידע על העבר, משתנה מקרי מעריכי יתפלג כמו משתנה מקרי "חדש".
        
        $exp(\lambda) \sim X $
        
        $\frac{^{\lambda -}\lambda ^{x}e}{!x} =$ $(x\geq P(X$
        
        $    \begin{cases} x < 0 & 0 \\x \geq 0& e^{\lambda x -} + 1 - \end{cases} =$ $(x\geq P(X$
        
        $\frac{1}{\lambda} =$ $E[X]$

        $\frac{1}{^2{\lambda}} =$ $Var[X]$

        </div>
    """, unsafe_allow_html=True)

# --- Practice Section ---
st.markdown('<div class="section-header"><h2>✍️ בואו נתרגל!</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class='practice-section'>
        בדיוק כמו במשחק, המכונה מפילה שטרות בקצב ממוצע של 5 שטרות בדקה.

        * יש לקחת 4 ספרות לאחר הנקודה (בשבר עשרוני) בכל שלב בחישוב ולהזין את התשובה הסופית באחוזים בדיוק של 2 ספרות (%XX.xx).
        * לכל שאלה יש 10 ניסיונות.
        </div>
    """, unsafe_allow_html=True)

# Definition of correct answers
correct_answers_money = {
    "q1": 14.62,
    "q2": 12.46,
    "q3": 8.21,
    "q4":18.89
}

# Question 1
with col1:
    st.markdown("""
        <div class='question-box'>
        <h3>שאלה 1️⃣</h3>
        מה ההסתברות שמשתתף שנכנס לתא למשך דקה יתפוס 6 שטרות?
        </div>
    """, unsafe_allow_html=True)

    # Get the current attempt count from URL parameters
    q1_attempt_count = int(st.query_params.get("q1_attempts_money", "0"))

    # Use a form for question 1
    with st.form(key="question1_money_form"):
        q1_answer = st.number_input(
            "הכניסו את תשובתכם באחוזים:",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            key="q1_money_input"
        )

        # Submit button (disabled if max attempts reached)
        q1_submit = st.form_submit_button(
            "בדיקת תשובה",
            disabled=(q1_attempt_count >= 10 or st.query_params.get("q1_status_money") == "success")
        )

        # Process form submission inside the form
        if q1_submit:
            # Check if answer is correct
            is_correct = abs(q1_answer - correct_answers_money["q1"]) < 0.1

            if is_correct:
                st.query_params["q1_status_money"] = "success"
            else:
                # Increment attempt counter
                q1_attempt_count += 1

                # Update URL parameter
                st.query_params["q1_attempts_money"] = str(q1_attempt_count)

                if q1_attempt_count >= 10:
                    st.query_params["q1_status_money"] = "failed"
                else:
                    st.query_params["q1_status_money"] = "trying"

        # Check if we need to show a previous result
        if "q1_status_money" in st.query_params:
            status = st.query_params["q1_status_money"]
            if status == "success":
                st.success(
                    f"כל הכבוד! התשובה הנכונה היא {correct_answers_money['q1']}%.\n"
                    "\n"
                    "**הסבר:** זוהי שאלה על התפלגות פואסון.\n"
                    "אנחנו מחפשים את ההסתברות לתפוס בדיוק 6 שטרות במשך דקה.\n"
                    "\n"
                    "נגדיר את המשתנה המקרי X כמספר השטרות שנתפסים במשך דקה.\n"
                    "בהתחשב בכך שהשטרות נופלים בקצב קבוע וכל שטר נופל באופן בלתי תלוי באחרים, X מתפלג לפי התפלגות פואסון:\n"
                    "\n"
                    "X ~ Poisson(λ=5)\n"
                    "\n"
                    "נשתמש בנוסחה להתפלגות פואסון: P(X=x) = (λ^x * e^(-λ)) / (x!)\n"
                    "כאשר:\n"
                    "- λ = 5 \n"
                    "- x = 6 (מספר השטרות הרצוי)\n"
                    "\n"
                    "נציב בנוסחה ונקבל שההסתברות לתפוס בדיוק 6 שטרות במשך דקה הינה **14.62%**."
                )
            elif status == "failed":
                st.error(
                    f"כל הכבוד על הניסיון! בפעם הבאה תצליחו יותר.\n"
                    "\n"
                    f"התשובה הנכונה היא {correct_answers_money['q1']}%.\n"
                    "\n"
                    "**הסבר:** זוהי שאלה על התפלגות פואסון.\n"
                    "אנחנו מחפשים את ההסתברות לתפוס בדיוק 6 שטרות במשך דקה.\n"
                    "\n"
                    "נגדיר את המשתנה המקרי X כמספר השטרות שנתפסים במשך דקה.\n"
                    "בהתחשב בכך שהשטרות נופלים בקצב קבוע וכל שטר נופל באופן בלתי תלוי באחרים, X מתפלג לפי התפלגות פואסון:\n"
                    "\n"
                    "X ~ Poisson(λ=5)\n"
                    "\n"
                    "נשתמש בנוסחה להתפלגות פואסון: P(X=x) = (λ^x * e^(-λ)) / (x!)\n"
                    "כאשר:\n"
                    "- λ = 5 \n"
                    "- x = 6 (מספר השטרות הרצוי)\n"
                    "\n"
                    "נציב בנוסחה ונקבל שההסתברות לתפוס בדיוק 6 שטרות במשך דקה הינה **14.62%**."
                )
            elif status == "trying":
                current_attempts = int(st.query_params.get("q1_attempts_money", "0"))
                remaining = 10 - current_attempts
                st.error(f"לא מדויק. נסו שוב! נותרו {remaining} ניסיונות.")

# Question 2
with col1:
    st.markdown("""
        <div class='question-box'>
        <h3>שאלה 2️⃣</h3>
        מה ההסתברות שמשתתף שנכנס לתא למשך דקה יתפוס פחות מ-3 שטרות?
        </div>
    """, unsafe_allow_html=True)

    # Get the current attempt count from URL parameters
    q2_attempt_count = int(st.query_params.get("q2_attempts_money", "0"))

    # Use a form for question 2
    with st.form(key="question2_money_form"):
        q2_answer = st.number_input(
            "הכניסו את תשובתכם באחוזים:",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            key="q2_money_input"
        )

        # Submit button (disabled if max attempts reached)
        q2_submit = st.form_submit_button(
            "בדיקת תשובה",
            disabled=(q2_attempt_count >= 10 or st.query_params.get("q2_status_money") == "success")
        )

        # Process form submission inside the form
        if q2_submit:
            # Check if answer is correct
            is_correct = abs(q2_answer - correct_answers_money["q2"]) < 0.1

            if is_correct:
                st.query_params["q2_status_money"] = "success"
            else:
                # Increment attempt counter
                q2_attempt_count += 1

                # Update URL parameter
                st.query_params["q2_attempts_money"] = str(q2_attempt_count)

                if q2_attempt_count >= 10:
                    st.query_params["q2_status_money"] = "failed"
                else:
                    st.query_params["q2_status_money"] = "trying"

        # Check if we need to show a previous result
        if "q2_status_money" in st.query_params:
            status = st.query_params["q2_status_money"]
            if status == "success":
                st.success(
                    f"כל הכבוד! התשובה הנכונה היא {correct_answers_money['q2']}%.\n"
                    "\n"
                    "**הסבר:** זוהי שאלה על התפלגות פואסון מצטברת.\n"
                    "אנחנו מחפשים את ההסתברות לתפוס פחות מ-3 שטרות במשך דקה, כלומר 0, 1, או 2 שטרות.\n"
                    "\n"
                    "המשתנה המקרי X מתפלג לפי התפלגות פואסון:\n"
                    "X ~ Poisson(λ=5)\n"
                    "\n"
                    "ההסתברות לתפוס פחות מ-3 שטרות במשך דקה הינה:\n"
                    "P(X < 3) = P(X=0) + P(X=1) + P(X=2)\n"
                    "\n"
                    "נחשב כל אחת מההסתברויות בנפרד:\n"
                    "\n"
                    "P(X=0) = (5^0 * e^(-5)) / 0!\n"
                    "= 0.0067\n"
                    "\n"
                    "P(X=1) = (5^1 * e^(-5)) / 1!\n"
                    "= 0.0337\n"
                    "\n"
                    "P(X=2) = (5^2 * e^(-5)) / 2!\n"
                    "= 0.0842\n"
                    "\n"
                    "P(X < 3) = 0.0067 + 0.0337 + 0.0842 = 0.1246\n"
                    "\n"
                    "ההסתברות לתפוס פחות מ-3 שטרות היא 0.1246, או **12.46%**.\n"
                )
            elif status == "failed":
                st.error(
                    f"כל הכבוד על הניסיון! בפעם הבאה תצליחו יותר.\n"
                    "\n"
                    f"התשובה הנכונה היא {correct_answers_money['q2']}%.\n"
                    "\n"
                    "**הסבר:** זוהי שאלה על התפלגות פואסון מצטברת.\n"
                    "אנחנו מחפשים את ההסתברות לתפוס פחות מ-3 שטרות במשך דקה, כלומר 0, 1, או 2 שטרות.\n"
                    "\n"
                    "המשתנה המקרי X מתפלג לפי התפלגות פואסון:\n"
                    "X ~ Poisson(λ=5)\n"
                    "\n"
                    "ההסתברות לתפוס פחות מ-3 שטרות במשך דקה הינה:\n"
                    "P(X < 3) = P(X=0) + P(X=1) + P(X=2)\n"
                    "\n"
                    "נחשב כל אחת מההסתברויות בנפרד:\n"
                    "\n"
                    "P(X=0) = (5^0 * e^(-5)) / 0!\n"
                    "= 0.0067\n"
                    "\n"
                    "P(X=1) = (5^1 * e^(-5)) / 1!\n"
                    "= 0.0337\n"
                    "\n"
                    "P(X=2) = (5^2 * e^(-5)) / 2!\n"
                    "= 0.0842\n"
                    "\n"
                    "P(X < 3) = 0.0067 + 0.0337 + 0.0842 = 0.1246\n"
                    "\n"
                    "ההסתברות לתפוס פחות מ-3 שטרות היא 0.1246, או **12.46%**.\n"
                )
            elif status == "trying":
                current_attempts = int(st.query_params.get("q2_attempts_money", "0"))
                remaining = 10 - current_attempts
                st.error(f"לא מדויק. נסו שוב! נותרו {remaining} ניסיונות.")

# Question 3
with col1:
    st.markdown("""
        <div class='question-box'>
        <h3>שאלה 3️⃣</h3>
        מה ההסתברות שיחלפו יותר מ-30 שניות בין שטר אחד לבא אחריו?
        </div>
    """, unsafe_allow_html=True)

    # Get the current attempt count from URL parameters
    q3_attempt_count = int(st.query_params.get("q3_attempts_money", "0"))

    # Use a form for question 3
    with st.form(key="question3_money_form"):
        q3_answer = st.number_input(
            "הכניסו את תשובתכם באחוזים:",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            key="q3_money_input"
        )

        # Submit button (disabled if max attempts reached)
        q3_submit = st.form_submit_button(
            "בדיקת תשובה",
            disabled=(q3_attempt_count >= 10 or st.query_params.get("q3_status_money") == "success")
        )

        # Process form submission inside the form
        if q3_submit:
            # Check if answer is correct
            is_correct = abs(q3_answer - 8.21) < 0.1

            if is_correct:
                st.query_params["q3_status_money"] = "success"
            else:
                # Increment attempt counter
                q3_attempt_count += 1

                # Update URL parameter
                st.query_params["q3_attempts_money"] = str(q3_attempt_count)

                if q3_attempt_count >= 10:
                    st.query_params["q3_status_money"] = "failed"
                else:
                    st.query_params["q3_status_money"] = "trying"

        # Check if we need to show a previous result
        if "q3_status_money" in st.query_params:
            status = st.query_params["q3_status_money"]
            if status == "success":
                st.success(
                    f"כל הכבוד! התשובה הנכונה היא 8.21%.\n"
                    "\n"
                    "**הסבר:** זוהי שאלה על התפלגות מעריכית.\n"
                    "אנחנו מחפשים את ההסתברות שיחלפו יותר מ-30 שניות (0.5 דקות) בין שטר אחד לבא אחריו.\n"
                    "\n"
                    "נגדיר את המשתנה המקרי X כזמן ההמתנה בין שטר לשטר.\n"
                    "בהתחשב בכך שהשטרות נופלים בקצב של 5 בדקה בממוצע, X מתפלג לפי התפלגות מעריכית:\n"
                    "\n"
                    "X ~ Exp(λ=5)\n"
                    "\n"
                    "ההסתברות שיחלפו יותר מ-x=0.5 דקות היא:\n"
                    "\n"
                    "P(X > 0.5) = 1 - P(X <= 0.5) = 1-(1-e^(-λx)) = e^(-5 * 0.5) = 0.0821\n"
                    "\n"
                    "ולכן ההסתברות שיחלפו יותר מ-30 שניות בין שטר לשטר היא 0.0821, או **8.21%**."
                )
            elif status == "failed":
                st.error(
                    f"כל הכבוד על הניסיון! בפעם הבאה תצליחו יותר.\n"
                    "\n"
                    f"התשובה הנכונה היא 8.21%.\n"
                    "\n"
                    "**הסבר:** זוהי שאלה על התפלגות מעריכית.\n"
                    "אנחנו מחפשים את ההסתברות שיחלפו יותר מ-30 שניות (0.5 דקות) בין שטר אחד לבא אחריו.\n"
                    "\n"
                    "נגדיר את המשתנה המקרי X כזמן ההמתנה בין שטר לשטר.\n"
                    "בהתחשב בכך שהשטרות נופלים בקצב של 5 בדקה בממוצע, X מתפלג לפי התפלגות מעריכית:\n"
                    "\n"
                    "X ~ Exp(λ=5)\n"
                    "\n"
                    "ההסתברות שיחלפו יותר מ-x=0.5 דקות היא:\n"
                    "\n"
                    "P(X > 0.5) = 1 - P(X <= 0.5) = 1-(1-e^(-λx)) = e^(-5 * 0.5) = 0.0821\n"
                    "\n"
                    "ולכן ההסתברות שיחלפו יותר מ-30 שניות בין שטר לשטר היא 0.0821, או **8.21%**."
                )
            elif status == "trying":
                current_attempts = int(st.query_params.get("q3_attempts_money", "0"))
                remaining = 10 - current_attempts
                st.error(f"לא מדויק. נסו שוב! נותרו {remaining} ניסיונות.")

# Question 4
with col1:
    st.markdown("""
        <div class='question-box'>
        <h3>שאלה 4️⃣</h3>
        אם עברו כבר 15 שניות בלי שנפל שטר, מה ההסתברות שיחלפו לפחות עוד 20 שניות נוספות עד שיפול שטר?
        </div>
    """, unsafe_allow_html=True)

    # Get the current attempt count from URL parameters
    q4_attempt_count = int(st.query_params.get("q4_attempts_money", "0"))

    # Use a form for question 4
    with st.form(key="question4_money_form"):
        q4_answer = st.number_input(
            "הכניסו את תשובתכם באחוזים:",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            key="q4_money_input"
        )

        # Submit button (disabled if max attempts reached)
        q4_submit = st.form_submit_button(
            "בדיקת תשובה",
            disabled=(q4_attempt_count >= 10 or st.query_params.get("q4_status_money") == "success")
        )

        # Process form submission inside the form
        if q4_submit:
            # Check if answer is correct
            is_correct = abs(q4_answer - 18.89) < 0.1

            if is_correct:
                st.query_params["q4_status_money"] = "success"
            else:
                # Increment attempt counter
                q4_attempt_count += 1

                # Update URL parameter
                st.query_params["q4_attempts_money"] = str(q4_attempt_count)

                if q4_attempt_count >= 10:
                    st.query_params["q4_status_money"] = "failed"
                else:
                    st.query_params["q4_status_money"] = "trying"

        # Check if we need to show a previous result
        if "q4_status_money" in st.query_params:
            status = st.query_params["q4_status_money"]
            if status == "success":
                st.success(
                    f"כל הכבוד! התשובה הנכונה היא 18.89%.\n"
                    "\n"
                    "**הסבר:** שאלה זו מדגימה את תכונת חוסר הזיכרון של ההתפלגות המעריכית.\n"
                    "אנחנו מחפשים את ההסתברות שיחלפו לפחות עוד 20 שניות (1/3 דקה) מרגע נתון, בהינתן שכבר עברו 15 שניות.\n"
                    "\n"
                    "נגדיר את המשתנה המקרי X כזמן ההמתנה עד להפלת שטר.\n"
                    "בהתחשב בכך שהשטרות נופלים בקצב של 5 בדקה בממוצע, X מתפלג לפי התפלגות מעריכית:\n"
                    "\n"
                    "X ~ Exp(λ=5)\n"
                    "\n"
                    "לפי תכונת חוסר הזיכרון של ההתפלגות המעריכית:\n"
                    "P(X > t + s | X > t) = P(X > s)\n"
                    "\n"
                    "במקרה שלנו, אנו מחפשים:\n"
                    "P(X > 15s + 20s | X > 15s) = P(X > 20s)\n"
                    "\n"
                    "כלומר, ההסתברות שנצטרך להמתין לפחות עוד 20 שניות בהינתן שכבר המתנו 15 שניות זהה להסתברות להמתין 20 שניות מההתחלה.\n"
                    "\n"
                    "P(X > 20s) = 1-(1-e^(-λ * 20/60)) = e^(-5 * 1/3) = e^(-5/3) = 0.1889\n"
                    "\n"
                    "ולכן ההסתברות שיחלפו לפחות עוד 20 שניות עד שיפול השטר הבא היא 0.1889, או **18.89%**.\n"
                )
            elif status == "failed":
                st.error(
                    f"כל הכבוד על הניסיון! בפעם הבאה תצליחו יותר.\n"
                    "\n"
                    f"התשובה הנכונה היא 18.89%.\n"
                    "\n"
                    "**הסבר:** שאלה זו מדגימה את תכונת חוסר הזיכרון של ההתפלגות המעריכית.\n"
                    "אנחנו מחפשים את ההסתברות שיחלפו לפחות עוד 20 שניות (1/3 דקה) מרגע נתון, בהינתן שכבר עברו 15 שניות.\n"
                    "\n"
                    "נגדיר את המשתנה המקרי X כזמן ההמתנה עד להפלת שטר.\n"
                    "בהתחשב בכך שהשטרות נופלים בקצב של 5 בדקה בממוצע, X מתפלג לפי התפלגות מעריכית:\n"
                    "\n"
                    "X ~ Exp(λ=5)\n"
                    "\n"
                    "לפי תכונת חוסר הזיכרון של ההתפלגות המעריכית:\n"
                    "P(X > t + s | X > t) = P(X > s)\n"
                    "\n"
                    "במקרה שלנו, אנו מחפשים:\n"
                    "P(X > 15s + 20s | X > 15s) = P(X > 20s)\n"
                    "\n"
                    "כלומר, ההסתברות שנצטרך להמתין לפחות עוד 20 שניות בהינתן שכבר המתנו 15 שניות זהה להסתברות להמתין 20 שניות מההתחלה.\n"
                    "\n"
                    "P(X > 20s) = 1-(1-e^(-λ * 20/60)) = e^(-5 * 1/3) = e^(-5/3) = 0.1889\n"
                    "\n"
                    "ולכן ההסתברות שיחלפו לפחות עוד 20 שניות עד שיפול השטר הבא היא 0.1889, או **18.89%**.\n"
                )
            elif status == "trying":
                current_attempts = int(st.query_params.get("q4_attempts_money", "0"))
                remaining = 10 - current_attempts
                st.error(f"לא מדויק. נסו שוב! נותרו {remaining} ניסיונות.")