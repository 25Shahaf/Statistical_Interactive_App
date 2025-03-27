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

st.markdown('<div class="top-header"><h1>קליעה למטרה 🎯</h1></div>', unsafe_allow_html=True)

# --- game explanation ---
st.markdown('<div class="section-header"><h2>🎮 המשחק</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
        <div class='game-explanation'>
        <h3>ברוכים הבאים למשחק קליעה למטרה!</h3>
    
        כאן תוכלו לתרגל וליישם הסתברות גיאומטרית והסתברות מותנית בעזרת זריקת חצים על לוח מטרה, כאשר הסיכוי לפגוע בכל אזור בלוח תלוי בגודלו ביחס לכל שטח הלוח.
    
        <h4>חוקי המשחק:</h4>
        לפניכם לוח מטרה עגול המחולק ל-3 אזורים: B, A ו-C בגדלים שונים.
        <ul>
        <li>הניקוד עבור כל פגיעה בלוח הינו בין 1-10 נקודות ומחושב על פי הנוסחה: score=10-(area percentage)/100 (הניקוד מעוגל כלפי מטה).</li>
        <li>למשל, פגיעה באזור ששטחו 70% תזכה ב-3 נקודות.</li>
        </ul>
        
        הרעיון הוא פשוט - ככל שהאזור קטן יותר, כך קשה יותר לפגוע בו, אבל הניקוד עליו גדול יותר!
        
        בסימולציה מטה, הכניסו ערכים שונים עבור גודל כל אזור על הלוח, זרקו חצים וראו את התוצאות המתקבלות.
        
        **חישבו:** באילו מגמות אתם יכולים להבחין כאשר אתם משנים את גדלי השטחים ומספר החצים?
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
        
        <h3>הסתברות מותנית 📊</h3>
        ההסתברות להתרחשות של מאורע מסויים בהינתן מידע על התרחשותם של מאורעות אחרים.
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
        
        * לכל שאלה יש 10 ניסיונות.
        </div>
    """, unsafe_allow_html=True)

with col2:
    radius_a_default, radius_b_default = calculate_radii_from_percentages(4.76, 24.99)
    fig_default = draw_target(radius_a_default, radius_b_default)
    st.pyplot(fig_default)

# Definition of correct answers
correct_answers = {
    "q1": 4.76,
    "q2": 42.55,
    "q3": 16.0,
    "q4": 5.76
}

# Question 1
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class='question-box'>
        <h3>שאלה 1️⃣</h3>
         מה ההסתברות לפגוע באזור A?
        </div>
    """, unsafe_allow_html=True)

    # Get the current attempt count from URL parameters
    q1_attempt_count = int(st.query_params.get("q1_attempts", "0"))

    # Use a form for question 1
    with st.form(key="question1_form"):
        q1_answer = st.number_input(
            "הכניסו את תשובתכם באחוזים:",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            key="q1_input"
        )

        # Submit button (disabled if max attempts reached)
        q1_submit = st.form_submit_button(
            "בדיקת תשובה",
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
                st.success(f"כל הכבוד! התשובה הנכונה היא {correct_answers['q1']}%. \n"
                           "\n"
                           f"**הסבר:** ההסתברות לפגיעה באזור A נקבעת על פי יחס השטחים בין אזור A לכל לוח המטרה.")
            elif status == "failed":
                st.error(f"כל הכבוד על הניסיון! בפעם הבאה תצליחו יותר. \n"
                         "\n"
                         f"התשובה הנכונה היא {correct_answers['q1']}%. \n"
                         "\n"
                         f"**הסבר:** ההסתברות לפגיעה באזור A נקבעת על פי יחס השטחים בין אזור A לכל לוח המטרה.")
            elif status == "trying":
                current_attempts = int(st.query_params.get("q1_attempts", "0"))
                remaining = 10 - current_attempts
                st.error(f"לא מדויק. נסו שוב! נותרו {remaining} ניסיונות.")

# Question 2
with col1:
    st.markdown("""
        <div class='question-box'>
        <h3>שאלה 2️⃣</h3>
        מקטינים את אזור C בחצי, כאשר החצי שהוקטן מתחלק באופן שווה בין אזור A לאזור B (השטח הכולל של לוח המטרה נשמר). מה ההסתברות לפגוע באזור B?
        </div>
    """, unsafe_allow_html=True)

    # Get the current attempt count from URL parameters
    q2_attempt_count = int(st.query_params.get("q2_attempts", "0"))

    # Use a form for question 2
    with st.form(key="question2_form"):
        q2_answer = st.number_input(
            "הכניסו את תשובתכם באחוזים:",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            key="q2_input"
        )

        # Submit button (disabled if max attempts reached)
        q2_submit = st.form_submit_button(
            "בדיקת תשובה",
            disabled=(q2_attempt_count >= 10 or st.query_params.get("q2_status") == "success")
        )

        # Process form submission inside the form
        if q2_submit:
            # Check if answer is correct
            is_correct = abs(q2_answer - correct_answers["q2"]) < 0.1

            if is_correct:
                st.query_params["q2_status"] = "success"
            else:
                # Increment attempt counter
                q2_attempt_count += 1

                # Update URL parameter
                st.query_params["q2_attempts"] = str(q2_attempt_count)

                if q2_attempt_count >= 10:
                    st.query_params["q2_status"] = "failed"
                else:
                    st.query_params["q2_status"] = "trying"

        # Check if we need to show a previous result
        if "q2_status" in st.query_params:
            status = st.query_params["q2_status"]
            if status == "success":
                st.success(f"כל הכבוד! התשובה הנכונה היא {correct_answers['q2']:.2f}%. \n"
                           f"\n"
                           f"**הסבר:** ההסתברות לפגיעה באזור B נקבעת על פי יחס השטחים בין אזור B לכל לוח המטרה. השטח של אזור B גדל ברבע מהשטח המקורי של אזור C. חלוקה בין השטח החדש של אזור B לשטח הכולל של לוח המטרה (שנשמר זהה) מניבה את התוצאה הנכונה.")
            elif status == "failed":
                st.error(f"כל הכבוד על הניסיון! בפעם הבאה תצליחו יותר. \n"
                         "\n"
                         f"התשובה הנכונה היא {correct_answers['q2']:.2f}%. \n"
                         "\n"
                         f"**הסבר:** ההסתברות לפגיעה באזור B נקבעת על פי יחס השטחים בין אזור B לכל לוח המטרה. השטח של אזור B גדל ברבע מהשטח המקורי של אזור C. חלוקה בין השטח החדש של אזור B לשטח הכולל של לוח המטרה (שנשמר זהה) מניבה את התוצאה הנכונה.")
            elif status == "trying":
                current_attempts = int(st.query_params.get("q2_attempts", "0"))
                remaining = 10 - current_attempts
                st.error(f"לא מדויק. נסו שוב! נותרו {remaining} ניסיונות.")

# Question 3
with col1:
    st.markdown("""
        <div class='question-box'>
        <h3>שאלה 3️⃣</h3>
        סטודנט מצטיין בזריקת חצים בטוח פוגע באזור A או B. מה הסיכוי שהוא יפגע באזור A?
        </div>
    """, unsafe_allow_html=True)

    # Get the current attempt count from URL parameters
    q3_attempt_count = int(st.query_params.get("q3_attempts", "0"))

    # Use a form for question 3
    with st.form(key="question3_form"):
        q3_answer = st.number_input(
            "הכניסו את תשובתכם באחוזים:",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            key="q3_input"
        )

        # Submit button (disabled if max attempts reached)
        q3_submit = st.form_submit_button(
            "בדיקת תשובה",
            disabled=(q3_attempt_count >= 10 or st.query_params.get("q3_status") == "success")
        )

        # Process form submission inside the form
        if q3_submit:
            # Check if answer is correct
            is_correct = abs(q3_answer - correct_answers["q3"]) < 0.1

            # Display result with special visualization for question 3
            if is_correct:
                st.query_params["q3_status"] = "success"
            else:
                # Increment attempt counter
                q3_attempt_count += 1

                # Update URL parameter
                st.query_params["q3_attempts"] = str(q3_attempt_count)

                if q3_attempt_count >= 10:
                    st.query_params["q3_status"] = "failed"
                else:
                    st.query_params["q3_status"] = "trying"

        if "q3_status" in st.query_params:
            status = st.query_params["q3_status"]
            if status == "success":
                col1_vis, col2_vis = st.columns(2)
                with col1_vis:
                    st.success(f"כל הכבוד! התשובה הנכונה היא {correct_answers['q3']:.0f}%. \n"
                               "\n"
                               f"**הסבר:** כאשר ידוע שהחץ פגע באזור A או B, מרחב המדגם מצטמצם לאזורים A ו-B בלבד ולכן ההסתברות לפגיעה באזור A משתנה. חלוקה בין שטח אזור A לסכום השטחים של אזור A ו-B (מרחב המדגם החדש) מניבה את התוצאה הנכונה.")

                with col2_vis:
                    radius_a_default, radius_b_default = calculate_radii_from_percentages(4.76, 24.99)
                    fig_reduced = draw_target(radius_a_default, radius_b_default, radius_c=radius_b_default)
                    st.pyplot(fig_reduced)
            elif status == "failed":
                col1_vis, col2_vis = st.columns(2)
                with col1_vis:
                    st.error(f"כל הכבוד על הניסיון! בפעם הבאה תצליחו יותר. \n"
                             "\n"
                             f"התשובה הנכונה היא {correct_answers['q3']:.0f}%. \n"
                             "\n"
                             f"**הסבר:** כאשר ידוע שהחץ פגע באזור A או B, מרחב המדגם מצטמצם לאזורים A ו-B בלבד ולכן ההסתברות לפגיעה באזור A משתנה. חלוקה בין שטח אזור A לסכום השטחים של אזור A ו-B (מרחב המדגם החדש) מניבה את התוצאה הנכונה.")

                with col2_vis:
                    radius_a_default, radius_b_default = calculate_radii_from_percentages(4.76, 24.99)
                    fig_reduced = draw_target(radius_a_default, radius_b_default, radius_c=radius_b_default)
                    st.pyplot(fig_reduced)
            elif status == "trying":
                current_attempts = int(st.query_params.get("q3_attempts", "0"))
                remaining = 10 - current_attempts
                st.error(f"לא מדויק. נסו שוב! נותרו {remaining} ניסיונות.")

# Question 4
with col1:
    st.markdown("""
        <div class='question-box'>
        <h3>שאלה 4️⃣</h3>
        כעת, מגבילים את אזור הפגיעה לכדי ריבוע החסום על ידי המעגל הגדול ביותר.
        \n
        מה ההסתברות לפגוע באזור A?
        </div>
    """, unsafe_allow_html=True)

    # Get the current attempt count from URL parameters
    q4_attempt_count = int(st.query_params.get("q4_attempts", "0"))

    # Use a form for question 4
    with st.form(key="question4_form"):
        q4_answer = st.number_input(
            "הכניסו את תשובתכם באחוזים:",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            key="q4_input"
        )

        # Submit button (disabled if max attempts reached)
        q4_submit = st.form_submit_button(
            "בדיקת תשובה",
            disabled=(q4_attempt_count >= 10 or st.query_params.get("q4_status") == "success")
        )

        # Process form submission inside the form
        if q4_submit:
            # Check if answer is correct
            is_correct = abs(q4_answer - correct_answers["q4"]) < 0.1

            # Display result with special visualization for question 4
            if is_correct:
                st.query_params["q4_status"] = "success"
            else:
                # Increment attempt counter
                q4_attempt_count += 1

                # Update URL parameter
                st.query_params["q4_attempts"] = str(q4_attempt_count)

                if q4_attempt_count >= 10:
                    st.query_params["q4_status"] = "failed"
                else:
                    st.query_params["q4_status"] = "trying"

        if "q4_status" in st.query_params:
            status = st.query_params["q4_status"]
            if status == "success":
                col1_vis, col2_vis = st.columns(2)
                with col1_vis:
                    st.success(f"כל הכבוד! התשובה הנכונה היא {correct_answers['q4']:.2f}%. \n"
                               "\n"
                               f"**הסבר:** כאשר הריבוע משיק למעגל החיצוני, צלע הריבוע שווה לרדיוס המעגל החיצוני כפול 2√. "
                               f"היחס בין שטח מעגל A לשטח הריבוע הוא ²(12/50). "
                               f"לכן ההסתברות לפגוע באזור A היא 5.76%.")

                with col2_vis:
                    radius_a_default, radius_b_default = calculate_radii_from_percentages(4.76, 24.99)
                    fig_reduced = draw_target(radius_a_default, radius_b_default, show_square=True)
                    st.pyplot(fig_reduced)
            elif status == "failed":
                col1_vis, col2_vis = st.columns(2)
                with col1_vis:
                    st.error(f"כל הכבוד על הניסיון! בפעם הבאה תצליחו יותר. \n"
                             "\n"
                             f"התשובה הנכונה היא {correct_answers['q4']:.2f}%. \n"
                             "\n"
                             f"**הסבר:** כאשר הריבוע משיק למעגל החיצוני, צלע הריבוע שווה לרדיוס המעגל החיצוני כפול 2√. "
                             f"היחס בין שטח מעגל A לשטח הריבוע הוא ²(12/50). "
                             f"לכן ההסתברות לפגוע באזור A היא 5.76%.")

                with col2_vis:
                    radius_a_default, radius_b_default = calculate_radii_from_percentages(4.76, 24.99)
                    fig_reduced = draw_target(radius_a_default, radius_b_default, show_square=True)
                    st.pyplot(fig_reduced)
            elif status == "trying":
                current_attempts = int(st.query_params.get("q4_attempts", "0"))
                remaining = 10 - current_attempts
                st.error(f"לא מדויק. נסו שוב! נותרו {remaining} ניסיונות.")