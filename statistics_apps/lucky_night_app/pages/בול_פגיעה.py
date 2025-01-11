import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import math

# --- עיצוב ותמיכה ב-RTL ---
st.markdown("""
    <style>
        :root {
            --background-color: #ffffff !important; /* Bright background */
            --text-color: #000000 !important;      /* Dark text */
            --primary-color: #1a73e8 !important;  /* Bright primary */
        }
        .stApp {
            direction: rtl;
        }
        .css-1y4p8pa {
            max-width: 100rem;
        }
        .section-header {
            background-color: #e0e5eb;
            padding: 0.1rem;
            border-radius: 10px;
            margin: 2rem 0 1rem 0;
        }
        .game-explanation {
            background-color: #eefafd;
            text-color: #000000 !important;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            border-right: 5px solid #83b0bb;
        }
        .game-explanation-header {
            background-color: #eefafd;
            padding: 0.3rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        .theory-section {
            background-color: #fdf5f8;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            border-right: 5px solid #c8a2ae;
        }
        .practice-section {
            background-color: #ebfaf1;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            border-right: 5px solid #83bb9a;
        }
        .question-box {
            background-color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            border: 1px solid #ddd;
        }
        .stButton>button {
            margin: 10px 0;
        }
        .custom-columns {
            display: flex;
            gap: 2rem;
        }

    </style>
""", unsafe_allow_html=True)


# --- Helper Functions ---
def calculate_radii_from_percentages(percent_a, percent_b):
    radius_a = math.sqrt(percent_a / 100)
    radius_b = math.sqrt((percent_a + percent_b) / 100)
    return radius_a, radius_b


def draw_target(radius_a, radius_b, radius_c=1, throws=None, figsize=(2.5, 2.5)):  # הקטנת גודל המטרה
    fig, ax = plt.subplots(figsize=figsize)

    circle_c = Circle((0, 0), radius_c, color='lightgray', alpha=0.3)
    circle_b = Circle((0, 0), radius_b, color='lightblue', alpha=0.3)
    circle_a = Circle((0, 0), radius_a, color='pink', alpha=0.3)

    ax.add_patch(circle_c)
    ax.add_patch(circle_b)
    ax.add_patch(circle_a)

    plt.text(0, 0, 'A', horizontalalignment='center', verticalalignment='center')
    plt.text(radius_a + (radius_b - radius_a) / 2, 0, 'B', horizontalalignment='center')
    plt.text(radius_b + (radius_c - radius_b) / 2, 0, 'C', horizontalalignment='center')

    if throws is not None:
        for x, y in throws:
            ax.plot(x, y, 'k.', markersize=2)

    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.axis('equal')
    ax.grid(False)
    ax.axis('off')

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


# --- Page Contenct ---
st.title("🎯 בול פגיעה")

# --- game explanation ---
st.markdown('<div class="section-header"><h2>🎮 הסבר המשחק</h2></div>', unsafe_allow_html=True)

st.markdown("""
    <div class='game-explanation'>
    <h3>ברוכים הבאים למשחק בול פגיעה! 🎯</h3>

    כאן תוכלו לתרגל וליישם הסתברות גיאומטרית והסתברות מותנית בעזרת זריקת חצים על לוח מטרה.

    <h4>חוקי המשחק:</h4>
    לפניכם לוח מטרה עגול המחולק ל-3 אזורים: B, A ו-C.
    <ul>
    <li>פגיעה באזור A מזכה ב-20 נקודות</li>
    <li>פגיעה באזור B מזכה ב-10 נקודות</li>
    <li>פגיעה באזור C לא מזכה בנקודות</li>
    </ul>
    
    הרעיון הוא פשוט - ככל שהאזור קטן יותר, כך קשה יותר לפגוע בו, אבל הפרס גדול יותר!
    
    הכניסו ערכים שונים עבור גודל כל אזור על הלוח וזרקו חצים כדי לראות את התוצאות.
    
    **חשבו:** מה קורה לתוצאות הזריקות ככל שמספר הזריקות עולה?
    </div>
""", unsafe_allow_html=True)

# --- game-zone ---
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<div class="game-explanation-header"><h3>הכניסו גודל באחוזים לכל אזור:</h3></div>',
                unsafe_allow_html=True)
    percent_a = st.number_input("גודל אזור A:", 0, 100, 25)
    percent_b = st.number_input("גודל אזור B:", 0, 100, 40)
    percent_c = st.number_input("גודל אזור C:", 0, 100, 35)


    total_percent = percent_a + percent_b + percent_c
    if total_percent != 100:
        st.error("סך כל האחוזים חייב להיות 100!")

    n_throws = st.number_input("מספר זריקות (1-1500)", 1, 1500, 1)
    if total_percent == 100:
        radius_a, radius_b = calculate_radii_from_percentages(percent_a, percent_b)
        fig = draw_target(radius_a, radius_b)
        with col2:
            st.pyplot(fig)
        if st.button("זרקו חצים"):
            radius_a, radius_b = calculate_radii_from_percentages(percent_a, percent_b)
            throws, hits = simulate_throws(n_throws, radius_a, radius_b)
            fig = draw_target(radius_a, radius_b, throws=throws)
            with col2:
                st.text('\n')
                st.text('\n')
                st.text('\n')
                st.text('\n')
                st.text('\n')
                st.pyplot(fig)

            #  Presenting the results
            st.markdown('<div class="game-explanation-header"><h3>תוצאות הזריקות:</h3></div>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("אזור A", f"{hits['A'] / n_throws * 100:.1f}%")
                st.markdown("**סך כל הנקודות מאזור A:**")
                st.markdown(f"{hits['A'] * 20}")
                st.markdown(f"**סך הנקודות הכולל:** {(hits['A']*20 + hits['B']*10)}")
            with col2:
                st.metric("אזור B", f"{hits['B'] / n_throws * 100:.1f}%")
                st.markdown("**סך כל הנקודות מאזור B:**")
                st.markdown(f"{hits['B'] * 10}")
            with col3:
                st.metric("אזור C", f"{hits['C'] / n_throws * 100:.1f}%")

#with col2:
    #if total_percent == 100:
        #radius_a, radius_b = calculate_radii_from_percentages(percent_a, percent_b)
        #fig = draw_target(radius_a, radius_b)
        #st.pyplot(fig)

# --- Theory Section ---
st.markdown('<div class="section-header"><h2>📚 רקע תיאורטי</h2></div>', unsafe_allow_html=True)

st.markdown("""
    <div class='theory-section'>
    <h3>הסתברות גיאומטרית 📐</h3>

    הסתברות גיאומטרית היא דרך לחשב הסתברות עבור מאורעות רציפים.

    ההסתברות שיתקיים מאורע מסויים היא:

    $\large \\frac{שטח \, המאורע}{שטח \, מרחב \, המדגם} = (מאורע)P$
    
    <h3>הסתברות מותנית ❗</h3>
    אם אנו יודעים שמאורע מסויים התרחש, מרחב המדגם משתנה וכך גם ההסתברות של שאר המאורעות להתרחש.
    ההסתברות במקרה זה מחושבת על פי Bayes:
    <br><br>
    
    $\large \\frac{P(A \cap B)}{P(B)} = P(A|B)$
    </div>
""", unsafe_allow_html=True)

# --- Practice Section ---
st.markdown('<div class="section-header"><h2>✍️ בואו נתרגל!</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(r"""
        <div class='practice-section'>
        <h4>נתונים:</h4>
        הרדיוס של כל אחד מהעיגולים על לוח המטרה:
        
        $ [cm] 10 = R(A)$
        
        $ [cm] 17 = R(B)$
        
        $ [cm] 55 = R(C)$
        
        * את התשובות יש להזין בדיוק של 2 ספרות אחרי הנקודה.
        </div>
    """, unsafe_allow_html=True)

with col2:
    radius_a_default, radius_b_default = calculate_radii_from_percentages(4.76, 24.99)
    fig_default = draw_target(radius_a_default, radius_b_default)
    st.pyplot(fig_default)

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

if st.button("בדוק תשובה", key="check1"):
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

if st.button("בדוק תשובה", key="check2"):
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

if st.button("בדוק תשובה", key="check3"):
    correct_answer = 16
    if user_answer3 == correct_answer:
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"כל הכבוד! התשובה הנכונה היא {correct_answer:.1f}%. \n"
                       "\n"
                       f"**הסבר:** כאשר ידוע שהחץ פגע באזור A או B, מרחב המדגם מצטמצם לאזורים A ו-B בלבד ולכן ההסתברות לפגיעה באזור A משתנה. חלוקה בין שטח אזור A לסכום השטחים של אזור A ו-B (מרחב המדגם החדש) מניבה את התוצאה הנכונה.")
        with col2:
            with col2:
                radius_a_default, radius_b_default = calculate_radii_from_percentages(4.76, 24.99)
                fig_reduced = draw_target(radius_a_default, radius_b_default, radius_c=radius_b_default)
                st.pyplot(fig_reduced)
    else:
        st.error("לא מדויק. נסו שוב!")