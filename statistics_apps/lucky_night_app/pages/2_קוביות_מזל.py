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
def roll_dice():
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    return dice1, dice2

def is_lucky_sum(sum_dice):
    return sum_dice in [6, 9]

def get_all_dice_combinations():
    combinations = []
    for i in range(1, 7):
        for j in range(1, 7):
            combinations.append((i, j))
    return combinations


def create_dice_svg(number):
    """Create SVG representation of a die with given number."""
    dot_positions = {
        1: [(50, 50)],
        2: [(25, 25), (75, 75)],
        3: [(25, 25), (50, 50), (75, 75)],
        4: [(25, 25), (25, 75), (75, 25), (75, 75)],
        5: [(25, 25), (25, 75), (50, 50), (75, 25), (75, 75)],
        6: [(25, 25), (25, 50), (25, 75), (75, 25), (75, 50), (75, 75)]
    }

    svg = f'''
    <svg width="100" height="100" viewBox="0 0 100 100">
        <rect x="5" y="5" width="90" height="90" rx="10" fill="white" stroke="black" stroke-width="2"/>
    '''

    for x, y in dot_positions[number]:
        svg += f'<circle cx="{x}" cy="{y}" r="8" fill="black"/>'

    svg += '</svg>'
    return svg

def reset_game():
    st.session_state.game_history = []
    st.session_state.score = 0
    st.session_state.roll_count = 0

def calculate_roll_distribution(history):
    sums = list(range(2, 13))
    counts = [0] * 11  # 11 possible sums (2-12)

    if history:
        for roll in history:
            idx = roll['סכום'] - 2  # Convert sum to index (2->0, 3->1, etc)
            counts[idx] += 1

    return sums, counts

def calculate_success_rate(history):
    if not history:
        return {"הצלחה": 0, "כישלון": 0}

    total_rolls = len(history)
    success_count = sum(1 for roll in history if roll['מספר מזל'] == 'כן')

    success_rate = (success_count / total_rolls) * 100
    failure_rate = 100 - success_rate

    return {
        "הצלחה": round(success_rate, 1),
        "כישלון": round(failure_rate, 1)
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

st.markdown('<div class="top-header"><h1>קוביות מזל 🎲</h1></div>', unsafe_allow_html=True)

# --- game explanation ---
st.markdown('<div class="section-header"><h2>🎮 המשחק</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
        <div class='game-explanation'>
        <h3>ברוכים הבאים למשחק קוביות מזל!</h3>

        כאן תוכלו לתרגל וליישם קומבינטוריקה (ועוד קצת) בעזרת הטלת קוביות.

        <h4>חוקי המשחק:</h4>
        ברשותכם 2 קוביות סטנדרטיות עם 6 פאות ממוספרות.
        הטילו את 2 הקוביות וסכמו את הספרות שהתקבלו.
        
        אם הסכום שהתקבל הינו אחד ממספרי המזל 6 או 9, תזכו בנקודה.
        
        </div>
    """, unsafe_allow_html=True)

# --- game-zone ---
col1, col2 = st.columns([4, 1])

with col1:
    #st.markdown('<div class="section-header"><h3>🎲 אזור המשחק</h3></div>', unsafe_allow_html=True)

    # Initialize session state for game history and score
    if 'game_history' not in st.session_state:
        st.session_state.game_history = []
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'roll_count' not in st.session_state:
        st.session_state.roll_count = 0

    # Create two columns for the buttons
    # Create columns for input and buttons
    col_rolls_input, col_roll, col_reset, col_space = st.columns([1, 1, 1, 1])

    with col_rolls_input:
        num_rolls = st.number_input(
            "מספר הטלות (1-100):",
            min_value=1,
            max_value=100,
            value=1,
            step=1
        )

    with col_roll:
        roll_button = st.button("הטלת קוביות")
    with col_reset:
        reset_button = st.button("משחק חדש")
        if reset_button:
            reset_game()

    st.markdown('ההטלה האחרונה:')
    if roll_button:
        for _ in range(num_rolls):
            st.session_state.roll_count += 1
            dice1, dice2 = roll_dice()
            sum_dice = dice1 + dice2
            is_lucky = is_lucky_sum(sum_dice)

            if is_lucky:
                st.session_state.score += 1

            # Add roll to history
            st.session_state.game_history.append({
                'מספר הטלה': st.session_state.roll_count,
                'קובייה 1': dice1,
                'קובייה 2': dice2,
                'סכום': sum_dice,
                'מספר מזל': "כן" if is_lucky else "לא"
            })

        # Display last roll with dice visualization (showing only the last roll)
        col_dice1, col_dice2, col_result = st.columns([1, 1, 2])
        with col_dice1:
            st.markdown('קובייה 1️⃣', unsafe_allow_html=True)
            st.markdown(create_dice_svg(dice1), unsafe_allow_html=True)
        with col_dice2:
            st.markdown("קובייה 2️⃣")
            st.markdown(create_dice_svg(dice2), unsafe_allow_html=True)

        with col_result:
            st.markdown(f"""
                <div style='background-color: {'#d4edda' if is_lucky else '#f8d7da'}; 
                          padding: 20px; 
                          border-radius: 10px; 
                          margin-top: 20px;
                          opacity: 0.8;
                          color: black;
                          text-align: center;
                          font-size: 1.2em;'>
                <h4>תוצאת ההטלה האחרונה:</h4>
                סכום: {sum_dice}<br>
                {" 🎉 מספר מזל! " if is_lucky else " לא מספר מזל... "}
                </div>
            """, unsafe_allow_html=True)

        # Display score
        st.markdown(f"ניקוד מצטבר: {st.session_state.score}")

        # Display roll distribution chart
        if st.session_state.game_history:
            # Create two columns for the charts
            col_hist, col_pie = st.columns(2)

            # Display roll distribution chart
            with col_hist:
                #st.markdown("התפלגות התוצאות:")
                sums, counts = calculate_roll_distribution(st.session_state.game_history)

                fig = go.Figure(data=[
                    go.Bar(x=[str(x) for x in sums], y=counts)
                ])

                fig.update_layout(
                    xaxis_title="סכום",
                    yaxis_title="מספר הופעות",
                    title="                                                                           :התפלגות התוצאות",
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

            with col_pie:
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

                # Display history table with colored rows
                if st.session_state.game_history:
                    st.markdown("\n")
                    st.markdown("10 הטלות אחרונות")

                    # Get last 10 rolls (reversed to show newest first)
                    last_10_rolls = list(reversed(st.session_state.game_history[-10:]))

                    # Create DataFrame with right-to-left column order
                    df = pd.DataFrame(last_10_rolls, index=None)
                    columns = ['מספר מזל', 'סכום', 'קובייה 2', 'קובייה 1', 'מספר הטלה']
                    df = df[columns]


                    # Style the DataFrame
                    def highlight_lucky(row):
                        is_lucky = row['מספר מזל'] == 'כן'
                        return [
                            'background-color: rgba(212, 237, 218, 0.5)' if is_lucky else 'background-color: rgba(248, 215, 218, 0.5)'] * len(
                            row)


                    styled_df = df.style.apply(highlight_lucky, axis=1).set_table_attributes('style="direction: rtl"')

                    # Display DataFrame without index
                    st.dataframe(
                        styled_df,
                        use_container_width=True,
                        hide_index=True
                    )

# --- Theory Section ---
st.markdown('<div class="section-header"><h2>📚 רקע תיאורטי</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
        <div class='theory-section'>
        <h3>קומבינטוריקה 🔢</h3>
        
        אנו עוסקים בקורס ב-3 סוגי בעיות קומבינטוריות:
        
        1. **חליפות עם החזרה** (Permutations with Repetition):
          - סדר הפריטים חשוב ומותרת חזרה על פריטים
          - נוסחה: $^{k}n$
        
        2. **חליפות ללא החזרה** (Permutations without Repetition):
          - סדר הפריטים חשוב ואין חזרה על פריטים
          - נוסחה: $ \\frac{!n}{!(n-k)} = P(n,k)$
        
        3. **צירופים ללא החזרה** (Combinations without Repetition):
          - הסדר אינו חשוב ואין חזרה על פריטים
          - נוסחה: $\\frac{!n}{!k!(n-k)} = \\binom{n}{k} = C(n,k)$

          כאשר עבור כל המקרים:
        - $n$: מספר הפריטים הכולל (האוכלוסיה)
        - $k$: מספר הפריטים הנבחרים (או השלבים)
        </div>
    """, unsafe_allow_html=True)

# --- Practice Section ---
st.markdown('<div class="section-header"><h2>✍️ בואו נתרגל!</h2></div>', unsafe_allow_html=True)


col1, col2 = st.columns(2)

with col1:
    st.markdown(r"""
        <div class='practice-section'>
        בדיוק כמו במשחק, נתונות 2 קוביות סטנדרטיות עם 6 פאות.

        מספרי המזל הם 6 ו-9.

        * תשובות באחוזים יש להזין בדיוק של 2 ספרות אחרי הנקודה (%XX.xx).
        </div>
    """, unsafe_allow_html=True)

    # Question 1
    st.markdown("""
        <div class='question-box'>
        <h3>שאלה 1️⃣</h3>
         כמה צמדים שונים קיימים כאשר מטילים 2 קוביות?
         \n
         הסדר אינו חשוב.
        </div>
    """, unsafe_allow_html=True)

    user_answer1 = st.number_input(
        "הכניסו את תשובתכם:",
        min_value=0.0,
        max_value=100.0,
        step=0.1,
        key="q1"
    )

    if st.button("בדיקת תשובה", key="check1"):
        correct_answer = 21
        if user_answer1 == correct_answer:
            st.success(f"כל הכבוד! התשובה הנכונה היא {correct_answer}. \n"
                       "\n"
                       "**הסבר:** כשהסדר לא חשוב, אנחנו משתמשים בנוסחת הצירופים (combinations):\n\n"
                       "* זוגות זהים (1,1), (2,2) וכו׳: 6 אפשרויות.\n"
                       "* זוגות שונים: המספרים שונים זה מזה, ולכן זה בעצם בחירת 2 מספרים מתוך 6, כשהסדר לא חשוב.\n"
                       "* נשתמש בנוסחה: $15 = \\frac{6 \\cdot 5}{2 \\cdot 1} = \\frac{!6}{!2!(6-2)} = \\binom{6}{2} $ \n"
                       "* סה\"כ: 6 + 15 = 21 צמדים שונים"
                       )
        else:
            st.error("לא מדויק. נסו שוב!")

    # Question 2
    st.markdown("""
        <div class='question-box'>
        <h3>שאלה 2️⃣</h3>
        כמה אופציות אפשריות לקבלת מספר המזל 9 בסכום הקוביות?
        </div>
    """, unsafe_allow_html=True)

    user_answer = st.number_input(
        "הכניסו את תשובתכם:",
        min_value=0.0,
        max_value=100.0,
        step=0.1,
        key="q2"
    )

    if st.button("בדיקת תשובה", key="check2"):
        correct_answer = 4
        if user_answer == correct_answer:
            st.success(f"כל הכבוד! התשובה הנכונה היא {correct_answer}. \n"
                       "\n"
                       "**הסבר:** במקרה הזה החישוב פשוט, אבל נחשב באמצעות תמורות (permutations) לשם התרגול:\n\n"
                       "* ראשית, נמצא את כל הזוגות השונים שסכומם 9: (3,6), (4,5)\n"
                       "* עבור כל זוג, נחשב את מספר התמורות האפשריות כשהסדר כן חשוב.\n"
                       "* הנוסחה לתמורה של 2 איברים היא: \n"
                       "$2 = \\frac{2 \\cdot 1}{1}  = \\frac{!2}{!0} = \\frac{!2}{!(2-2)}= N$\n"
                       "* לכן:\n"
                       "  * עבור הזוג (3,6): 2 תמורות - (3,6), (6,3)\n"
                       "  * עבור הזוג (4,5): 2 תמורות - (4,5), (5,4)\n"
                       "* סה״כ: 2 זוגות × 2 תמורות = 4 אפשרויות"
                       )
        else:
            st.error("לא מדויק. נסו שוב!")

    # Question 3
    st.markdown("""
        <div class='question-box'>
        <h3>שאלה 3️⃣</h3>
        מה ההסתברות לקבל מספר מזל כלשהו?
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
        correct_answer = 25  # (9/36) * 100
        if abs(user_answer - correct_answer) < 0.01:
            st.success(
                f"כל הכבוד! התשובה הנכונה היא {correct_answer:.0f}%.\n"
                "\n"
                "**הסבר:** נחשב את ההסתברות לקבל סכום של 6 או 9:\n"
                "\n"
                "* מספר האפשרויות לקבלת סכום 6:\n"
                "  * זוגות שונים: (1,5), (2,4), (4,2), (5,1) - כל אחד נספר בנפרד כי הקוביות שונות\n"
                "  * זוג זהה: (3,3) - נספר פעם אחת כי אותו מספר בשתי הקוביות\n"
                "  * סה\"כ 5 אפשרויות\n"
                "* מספר האפשרויות לקבלת סכום 9: (3,6), (4,5), (5,4), (6,3) = 4 אפשרויות\n"
                "* סך כל האפשרויות בהטלת 2 קוביות: 6 × 6 = 36 אפשרויות\n"
                "* לכן ההסתברות היא: $25\\% = 0.25 = \\frac{9}{36} = \\frac{5+4}{36}$"
            )
        else:
            st.error("לא מדויק. נסו שוב!")

    # Question 4
    st.markdown("""
        <div class='question-box'>
        <h3>שאלה 4️⃣</h3>
        לאחר מספר סיבובי משחקים, התחלתם לחשוד שאחת מהקוביות היא מזויפת אבל אתם לא בטוחים איזו מהן.
        \n
        כדי לבדוק את ההשערה שלכם, החלטתם לתעד 24 הטלות של קוביות 2 ו-1 בנפרד.
         \n
         בהסתמך על ההטלות שתעדתם בלבד ומוצגות מטה, איזו קוביה ייתכן שהינה מזוייפת?
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        | הטלה | קובייה 1 | קובייה 2 |
        |:---:|:---:|:---:|
        | 1 | 3 | 6 |
        | 2 | 5 | 4 |
        | 3 | 6 | 6 |
        | 4 | 2 | 3 |
        | 5 | 1 | 5 |
        | 6 | 4 | 6 |
        | 7 | 3 | 2 |
        | 8 | 5 | 5 |
        | 9 | 2 | 6 |
        | 10 | 6 | 1 |
        | 11 | 1 | 5 |
        | 12 | 4 | 6 |
        """)

    with col2:
        st.markdown("""
        | הטלה | קובייה 1 | קובייה 2 |
        |:---:|:---:|:---:|
        | 13 | 2 | 4 |
        | 14 | 5 | 6 |
        | 15 | 3 | 3 |
        | 16 | 6 | 5 |
        | 17 | 4 | 6 |
        | 18 | 1 | 2 |
        | 19 | 3 | 5 |
        | 20 | 5 | 6 |
        | 21 | 2 | 1 |
        | 22 | 6 | 5 |
        | 23 | 4 | 6 |
        | 24 | 1 | 4 |
        """)

    user_answer4 = st.number_input(
        "הכניסו את מספר הקוביה שייתכן כי היא מזוייפת:",
        min_value=0.0,
        max_value=100.0,
        step=0.1,
        key="q4"
    )

    if st.button("בדיקת תשובה", key="check4"):
        correct_answer = 2
        if user_answer4 == correct_answer:
            st.success(f"כל הכבוד! התשובה הנכונה היא {correct_answer:.0f}%. \n"
                       "\n"
                       "**הסבר:**\n"
                        "\n"
                        "נבדוק את התדירות היחסית של כל מספר בכל קובייה:\n"
                        "\n"
                        "**קובייה 1:**\n"
                        "* מספר 1: 4/24 = 16.7%\n"
                        "* מספר 2: 4/24 = 16.7%\n"
                        "* מספר 3: 4/24 = 16.7%\n"
                        "* מספר 4: 4/24 = 16.7%\n"
                        "* מספר 5: 4/24 = 16.7%\n"
                        "* מספר 6: 4/24 = 16.7%\n"
                        "\n"
                        "התפלגות התוצאות בקובייה 1 אחידה ותואמת את ההסתברות התיאורטית של 1/6 = 16.7% לכל מספר.\n"
                        "\n"
                        "**קובייה 2:**\n"
                        "* מספר 1: 2/24 = 8.3%\n"
                        "* מספר 2: 2/24 = 8.3%\n"
                        "* מספר 3: 2/24 = 8.3%\n"
                        "* מספר 4: 3/24 = 12.5%\n"
                        "* מספר 5: 6/24 = 25%\n"
                        "* מספר 6: 9/24 = 37.5%\n"
                        "\n"
                        "התפלגות התוצאות בקובייה 2 מראה העדפה למספרים 5 ו-6 (במיוחד ל-6), ותדירות נמוכה יותר למספרים 1-4.\n"
                        "זוהי סטייה מההסתברות התיאורטית של קובייה הוגנת (1/6 = 16.7% לכל מספר), ולכן ייתכן כי קוביה 2 מזוייפת."
                       "\n"
                       "יחד עם זאת, יש לשים לב כי לא באמת נוכל לקבוע זאת בוודאות וזוהי רק השערה שמסתמכת על 20 הטלות בלבד."
                    )
        else:
            st.error("לא מדויק. נסו שוב!")

    # Question 5
    st.markdown("""
        <div class='question-box'>
        <h3>שאלה 5️⃣</h3>
        נתון כי הקוביה שחשדתם שהינה מזוייפת בשאלה הקודמת אכן מזוייפת, ותוצאות ההטלה שלה מתפלגות בהתאם למה שקיבלתם בשאלה הקודמת.
        \n
        מה ההסתברות לקבל סכום של מספר מזל כאשר מטילים 2 קוביות מזוייפות כאלה?
        \n
        כדי להגיע לתשובה, יש לבצע את כל החישובים באחוזים בדיוק של 2 ספרות אחרי הנקודה.
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
        correct_answer = 19.43
        if abs(user_answer - correct_answer) == 0:
            st.success(f"כל הכבוד! התשובה הנכונה היא {correct_answer}%."
            "\n"
            "\n"
            "**הסבר:**"
            "\n"
            "נחשב לפי התדירויות היחסיות שחישבנו בשאלה הקודמת:" 
            "\n"
            "* עבור סכום 6:" 
            "\n"
            "  * תוצאה (1,5): P(1 בקובייה 1) × P(5 בקובייה 2) = 8.33% ×  25.00% = 2.08% \n"
            "  *  תוצאה (2,4): P(2 בקובייה 1) × P(4 בקובייה 2) = 8.33% × 12.50% = 1.04% \n"
            "  *  תוצאה (3,3): P(3 בקובייה 1) × P(3 בקובייה 2) = 8.33% × 8.33% = 0.69% \n"
            "  *  תוצאה (4,2): P(4 בקובייה 1) × P(2 בקובייה 2) = 12.50% × 8.33% = 1.04% \n"
            "  *  תוצאה (5,1): P(5 בקובייה 1) × P(1 בקובייה 2) = 25.00% × 8.33% = 2.08% \n"
            "\n"
            "  סכום ההסתברויות עבור סכום 6:" 
            "\n"
            "  2.08% + 1.04% + 0.69% + 1.04% + 2.08% = 6.93% \n"
            "\n"
            "* עבור סכום 9:" 
            "\n"
            "  *  תוצאה (3,6): P(3 בקובייה 1) × P(6 בקובייה 2) = 8.33% × 37.50% = 3.12% \n"
            "  *  תוצאה (4,5): P(4 בקובייה 1) × P(5 בקובייה 2) = 12.50% × 25.00% = 3.13% \n"
            "  *  תוצאה (5,4): P(5 בקובייה 1) × P(4 בקובייה 2) = 25.00% × 12.50% = 3.13% \n"
            "  *  תוצאה (6,3): P(6 בקובייה 1) × P(3 בקובייה 2) = 37.50% × 8.33% = 3.12% \n"
            "\n"
            "  סכום ההסתברויות עבור סכום 9:" 
            "  3.12% + 3.13% + 3.13% + 3.12% = 12.50% \n"
            "\n"
            "סכום כל ההסתברויות: 6.93% + 12.50% = 19.43% \n"
                       )
        else:
            st.error("לא מדויק. נסו שוב!")