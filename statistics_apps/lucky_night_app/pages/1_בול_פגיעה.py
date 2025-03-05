import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import math
import os
from utils.helper_functions import setup_page

# --- Helper Functions ---
def calculate_radii_from_percentages(percent_a, percent_b):
    radius_a = math.sqrt(percent_a / 100)
    radius_b = math.sqrt((percent_a + percent_b) / 100)
    return radius_a, radius_b

def calculate_score(area_percent):
    return max(1, int(10 - (area_percent / 10)))

def draw_target(radius_a, radius_b, radius_c=1, throws=None, figsize=(2, 2), show_square=False):
    fig, ax = plt.subplots(figsize=figsize)

    circle_c = Circle((0, 0), radius_c, color='lightgray', alpha=0.8)
    circle_b = Circle((0, 0), radius_b, color='lightblue', alpha=0.8)
    circle_a = Circle((0, 0), radius_a, color='pink', alpha=0.8)

    ax.add_patch(circle_c)
    ax.add_patch(circle_b)
    ax.add_patch(circle_a)

    plt.text(0, 0, 'A', horizontalalignment='center', verticalalignment='center')
    plt.text(radius_a + (radius_b - radius_a) / 2, 0, 'B', horizontalalignment='center')
    plt.text(radius_b + (radius_c - radius_b) / 2, 0, 'C', horizontalalignment='center')

    if show_square:
        side = radius_c * np.sqrt(2)
        half_side = side / 2
        square = plt.Rectangle((-half_side, -half_side), side, side,
                             fill=False, color='red', linestyle='--')
        ax.add_patch(square)

    if throws is not None:
        for x, y in throws:
            ax.plot(x, y, 'k.', markersize=2)

    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.axis('equal')
    ax.grid(False)
    ax.axis('off')

    fig.patch.set_facecolor('none')  # Make the background transparent
    fig.patch.set_edgecolor('none')  # Remove the edge color

    return fig


def simulate_throws(n_throws, radius_a, radius_b):
    throws = []
    hits = {'A': 0, 'B': 0, 'C': 0}

    for _ in range(n_throws):
        angle = np.random.uniform(0, 2 * np.pi)
        r = np.sqrt(np.random.uniform(0, 1))
        x = r * np.cos(angle)
        y = r * np.sin(angle)
        throws.append((x, y))

        distance = np.sqrt(x ** 2 + y ** 2)
        if distance <= radius_a:
            hits['A'] += 1
        elif distance <= radius_b:
            hits['B'] += 1
        else:
            hits['C'] += 1

    return throws, hits


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

st.markdown('<div class="top-header"><h1>בול פגיעה 🎯</h1></div>', unsafe_allow_html=True)

# --- game explanation ---
st.markdown('<div class="section-header"><h2>🎮 המשחק</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
        <div class='game-explanation'>
        <h3>ברוכים הבאים למשחק בול פגיעה!</h3>
    
        כאן תוכלו לתרגל וליישם הסתברות גיאומטרית והסתברות מותנית בעזרת זריקת חצים על לוח מטרה.
        
        הסיכוי לפגוע בכל אזור בלוח תלוי בגודלו ביחס לכל הלוח.
    
        <h4>חוקי המשחק:</h4>
        לפניכם לוח מטרה עגול המחולק ל-3 אזורים: B, A ו-C.
        <ul>
        <li>הניקוד לכל אזור מחושב אוטומטית לפי גודל האזור, כך שהוא השלמה ל-10 ביחס לאחוז השטח.</li>
        <li>למשל, אזור ששטחו 70% יזכה ב-3 נקודות.</li>
        </ul>
        
        הרעיון הוא פשוט - ככל שהאזור קטן יותר, כך קשה יותר לפגוע בו, אבל הפרס גדול יותר!
        
        הכניסו ערכים שונים עבור גודל כל אזור על הלוח וזרקו חצים כדי לראות את התוצאות.
        
        **חשבו:** מה קורה לתוצאות הזריקות ככל שמספר הזריקות עולה?
        </div>
    """, unsafe_allow_html=True)

with col2:
    radius_a, radius_b = calculate_radii_from_percentages(15, 40)
    fig = draw_target(radius_a, radius_b)
    st.pyplot(fig)


# --- game-zone ---
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<div class="game-explanation-header"><h3>הכניסו גודל באחוזים לכל אזור:</h3></div>',
                unsafe_allow_html=True)
    percent_a = st.number_input("גודל אזור A:", 0, 100, 15)
    percent_b = st.number_input("גודל אזור B:", 0, 100, 35)
    percent_c = st.number_input("גודל אזור C:", 0, 100, 50)


    total_percent = percent_a + percent_b + percent_c
    if total_percent != 100:
        st.error("סך כל האחוזים חייב להיות 100!")

    n_throws = st.number_input("מספר זריקות (1-1500)", 1, 1500, 1)
    if total_percent == 100:
        if st.button("זרקו חצים"):
            radius_a, radius_b = calculate_radii_from_percentages(percent_a, percent_b)
            throws, hits = simulate_throws(n_throws, radius_a, radius_b)
            fig = draw_target(radius_a, radius_b, throws=throws)
            with col2:
                st.text('\n')
                st.text('\n')
                st.pyplot(fig)

            #  Presenting the results
            st.markdown('<div class="game-explanation-header"><h3>תוצאות הזריקות:</h3></div>', unsafe_allow_html=True)
            score_a = calculate_score(percent_a)
            score_b = calculate_score(percent_b)
            score_c = calculate_score(percent_c)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("אזור A", f"{hits['A'] / n_throws * 100:.1f}%")
                st.markdown(f"**ניקוד:** {score_a} נקודות")
            with col2:
                st.metric("אזור B", f"{hits['B'] / n_throws * 100:.1f}%")
                st.markdown(f"**ניקוד:** {score_b} נקודות")
            with col3:
                st.metric("אזור C", f"{hits['C'] / n_throws * 100:.1f}%")
                st.markdown(f"**ניקוד:** {score_c} נקודות")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**סך כל הנקודות מאזור A:**")
                st.markdown(f"{hits['A'] * score_a}")
            with col2:
                st.markdown("**סך כל הנקודות מאזור B:**")
                st.markdown(f"{hits['B'] * score_b}")
            with col3:
                st.markdown("**סך כל הנקודות מאזור C:**")
                st.markdown(f"{hits['C'] * score_c}")

            st.markdown(f"**סך הנקודות הכולל:** {(hits['A'] * score_a + hits['B'] * score_b + hits['C'] * score_c)}")


# --- Theory Section ---
st.markdown('<div class="section-header"><h2>📚 רקע תיאורטי</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
        <div class='theory-section'>
        <h3>הסתברות גיאומטרית 📐</h3>
    
        הסתברות גיאומטרית היא דרך לחשב הסתברות עבור מאורעות רציפים.
    
        ההסתברות שיתקיים מאורע מסויים היא:
    
        $\large \\frac{שטח \, המאורע}{שטח \, מרחב \, המדגם} = (מאורע)P$
        
        <h3>הסתברות מותנית ❗</h3>
        אם אנו יודעים שמאורע מסויים התרחש, מרחב המדגם משתנה וכך גם ההסתברות של שאר המאורעות להתרחש.
        \n
        ההסתברות במקרה זה מחושבת על פי Bayes:
        <br><br>
        
        $\large \\frac{P(A \cap B)}{P(B)} = P(A|B)$
        </div>
    """, unsafe_allow_html=True)

# --- Practice Section ---
st.markdown('<div class="section-header"><h2>✍️ בואו נתרגל!</h2></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown(r"""
        <div class='practice-section'>
        <h4>נתונים:</h4>
        הרדיוס של כל אחד מהעיגולים על לוח המטרה:
        
        $ [cm] 12 = R(A)$
        
        $ [cm] 30 = R(B)$
        
        $ [cm] 55 = R(C)$
        
        * את התשובות יש להזין באחוזים בדיוק של 2 ספרות אחרי הנקודה (%XX.xx).
        </div>
    """, unsafe_allow_html=True)

with col2:
    radius_a_default, radius_b_default = calculate_radii_from_percentages(4.76, 24.99)
    fig_default = draw_target(radius_a_default, radius_b_default)
    st.pyplot(fig_default)

col1, col2 = st.columns(2)

with col1:
    # Qurstion 1
    st.markdown("""
        <div class='question-box'>
        <h3>שאלה 1️⃣</h3>
         מה ההסתברות לפגוע באזור A?
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
        correct_answer = 4.76
        if user_answer1 == correct_answer:
            st.success(f"כל הכבוד! התשובה הנכונה היא {correct_answer}%. \n"
                       "\n"
                       f"**הסבר:** ההסתברות לפגיעה באזור A נקבעת על פי יחס השטחים בין אזור A לכל לוח המטרה.")
        else:
            st.error("לא מדויק. נסו שוב!")

    # Question 2
    st.markdown("""
        <div class='question-box'>
        <h3>שאלה 2️⃣</h3>
        מקטינים את אזור C בחצי, כאשר החצי שהוקטן מתחלק באופן שווה בין אזור A לאזור B (השטח הכולל של לוח המטרה נשמר). מה ההסתברות לפגוע באזור B?
        </div>
    """, unsafe_allow_html=True)

    user_answer2 = st.number_input(
        "הכניסו את תשובתכם באחוזים:",
        min_value=0.0,
        max_value=100.0,
        step=0.1,
        key="q2"
    )

    if st.button("בדיקת תשובה", key="check2"):
        correct_answer = 42.55
        if user_answer2 == correct_answer:
            st.success(f"כל הכבוד! התשובה הנכונה היא {correct_answer:.1f}%. \n"
                       f"\n"
                       f"**הסבר:** ההסתברות לפגיעה באזור B נקבעת על פי יחס השטחים בין אזור B לכל לוח המטרה. השטח של אזור B גדל ברבע מהשטח המקורי של אזור C. חלוקה בין השטח החדש של אזור B לשטח הכולל של לוח המטרה (שנשמר זהה) מניבה את התוצאה הנכונה.")
        else:
            st.error("לא מדויק. נסו שוב!")

    # Question 3
    st.markdown("""
        <div class='question-box'>
        <h3>שאלה 3️⃣</h3>
        סטודנט מצטיין בזריקת חצים בטוח פוגע באזור A או B. מה הסיכוי שהוא יפגע באזור A?
        </div>
    """, unsafe_allow_html=True)

    user_answer3 = st.number_input(
        "הכניסו את תשובתכם באחוזים:",
        min_value=0.0,
        max_value=100.0,
        step=0.1,
        key="q3"
    )

    if st.button("בדיקת תשובה", key="check3"):
        correct_answer = 16
        if user_answer3 == correct_answer:
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"כל הכבוד! התשובה הנכונה היא {correct_answer:.0f}%. \n"
                           "\n"
                           f"**הסבר:** כאשר ידוע שהחץ פגע באזור A או B, מרחב המדגם מצטמצם לאזורים A ו-B בלבד ולכן ההסתברות לפגיעה באזור A משתנה. חלוקה בין שטח אזור A לסכום השטחים של אזור A ו-B (מרחב המדגם החדש) מניבה את התוצאה הנכונה.")
            with col2:
                with col2:
                    radius_a_default, radius_b_default = calculate_radii_from_percentages(4.76, 24.99)
                    fig_reduced = draw_target(radius_a_default, radius_b_default, radius_c=radius_b_default)
                    st.pyplot(fig_reduced)
        else:
            st.error("לא מדויק. נסו שוב!")

    # Question 4
    st.markdown("""
        <div class='question-box'>
        <h3>שאלה 4️⃣</h3>
        כעת, מגבילים את אזור הפגיעה לכדי ריבוע שכל קודקודיו משיקים למעגל חיצוני.
        \n
        מה ההסתברות לפגוע באזור A?
        </div>
    """, unsafe_allow_html=True)

    user_answer4 = st.number_input(
        "הכניסו את תשובתכם באחוזים:",
        min_value=0.0,
        max_value=100.0,
        step=0.1,
        key="q4"
    )

    if st.button("בדיקת תשובה", key="check4"):
        correct_answer = 5.76  # (12/50)^2 * 100
        if abs(user_answer4 - correct_answer) < 0.1:
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"כל הכבוד! התשובה הנכונה היא {correct_answer:.2f}%. \n"
                           "\n"
                           f"**הסבר:** כאשר הריבוע משיק למעגל החיצוני, צלע הריבוע שווה לרדיוס המעגל החיצוני כפול √2. "
                           f"היחס בין שטח מעגל A לשטח הריבוע הוא (12/50)². "
                           f"לכן ההסתברות לפגוע באזור A היא 5.76%.")
            with col2:
                radius_a_default, radius_b_default = calculate_radii_from_percentages(4.76, 24.99)
                fig_reduced = draw_target(radius_a_default, radius_b_default, show_square=True)
                st.pyplot(fig_reduced)
        else:
            st.error("לא מדויק. נסו שוב!")