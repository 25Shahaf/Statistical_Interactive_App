import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import matplotlib.patches as mpatches
from scipy.stats import alpha

def app():
    st.write("## Conditional Probability")

    # Display explanation for conditional probability
    st.markdown("""### Conditional Probability Formula:""")
    st.latex(r"P(A | B) = \frac{P(A \cap B)}{P(B)}")

    # Define the probabilities with sliders
    p_A = 0.5
    p_B = 0.6
    p_A_given_B = p_A * p_B

    # Set up the Venn diagram
    fig1, ax1 = plt.subplots()

    venn1 = venn2(subsets=(p_A, p_B, p_A_given_B), set_labels=('A', 'B'))

    # Highlight the intersection P(A ∩ B) (joint probability)
    venn1.get_label_by_id('11').set_text(f'P(A ∩ B)')
    venn1.get_patch_by_id('11').set_color('#af8bce')  # Purple color for intersection
    venn1.get_label_by_id('11').set_fontsize(10)
    venn1.get_patch_by_id('11').set_alpha(0.7)

    # Highlight the whole region of B for conditional probability
    venn1.get_label_by_id('01').set_text(f'P(B)')
    venn1.get_patch_by_id('01').set_color('#7fb2e2')  # Blue color for B
    venn1.get_label_by_id('01').set_fontsize(10)
    venn1.get_patch_by_id('01').set_alpha(0.5)

    # Highlight the whole region of A
    venn1.get_label_by_id('10').set_text(f'P(A)')
    venn1.get_patch_by_id('10').set_color('#e2877f')  # Red color for A
    venn1.get_label_by_id('10').set_fontsize(10)
    venn1.get_patch_by_id('10').set_alpha(0.5)

    # Adding a black rectangle representing the sample space
    rect = mpatches.Rectangle((-0.75, -0.55), 1.5, 1.06, linewidth=2, edgecolor='black', facecolor='none')
    ax1.add_patch(rect)

    # Adding Ω label at the bottom right
    ax1.text(0.65, -0.48, r'$\Omega$', fontsize=30, ha='center', va='center')

    # Create the second Venn diagram in a new figure
    fig2, ax2 = plt.subplots()

    # Create a single Venn diagram for only B
    venn11 = venn2(subsets=(p_A, p_B, p_A_given_B), ax=ax2, set_labels=('', ''))

    # Setting the properties for the circle
    venn11.get_patch_by_id('01').set_color('#7fb2e2')  # Blue color for B
    venn11.get_patch_by_id('11').set_color('#af8bce')  # Purple color for intersection
    venn11.get_patch_by_id('10').set_color('white')  # Remove color for only A
    venn11.get_label_by_id('01').set_text(r'P(B)')  # Label for B
    venn11.get_label_by_id('11').set_text(r'P(A ∩ B)')  # Intersection label
    venn11.get_label_by_id('10').set_text('')  # Remove label for only A

    # Adding a black circle around the second Venn diagram
    circle = plt.Circle((0.22, 0.004), 0.45, color='black', fill=False, linewidth=2)
    ax2.add_artist(circle)

    # Adding a right arrow on the left side of the diagram
    arrow = plt.Arrow(-0.7, 0, 0.4, 0, width=0.1, color='black')
    ax2.add_patch(arrow)

    # Adding Ω label inside the B area
    ax2.text(0.35, -0.3, r'$\Omega$', fontsize=30, ha='center', va='center')

    # Placing the plots side by side
    col1, col2 = st.columns([1, 1])
    with col1:
        st.pyplot(fig1)

    with col2:
        st.pyplot(fig2)

    # Display explanation for conditional probability

    st.markdown(f"""
            ### For example, given:
            - **P(A)**: {p_A:.2f}
            - **P(B)**: {p_B:.2f}
            - **P(A ∩ B)**: {p_A_given_B:.2f}
            """)

    st.markdown("""### The Calculated Conditional Probability:""")

    st.latex(rf"P(A | B) = \frac{{{p_A_given_B:.2f}}}{{{p_B:.2f}}} = {p_A_given_B / p_B if p_B > 0 else 'undefined'}")