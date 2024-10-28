import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn2_circles, venn3
import matplotlib.patches as mpatches
from scipy.stats import alpha


def app():
    st.write("# Basic Concepts of Probability")

    # Union and Intersection of Events Visualization
    st.write("## Union and Intersection of Events:")

    A = {1, 2, 3, 4}
    B = {3, 4, 5, 6}

    # User selects operation: Union or Intersection
    operation = st.radio("Choose an operation:", ("Union", "Intersection"))

    # Set up the Venn diagram
    fig, ax = plt.subplots()

    # Create the basic Venn diagram without coloring
    venn = venn2([A, B], set_labels=('A', 'B'))

    # Adding a black rectangle representing the sample space
    rect = mpatches.Rectangle((-0.74, -0.557), 1.47, 1.06, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(rect)

    # Adding Ω label at the bottom right
    ax.text(0.65, -0.48, r'$\Omega$', fontsize=30, ha='center', va='center')

    # Color the regions based on the operation
    if operation == "Union":
        # Color all areas for the union
        plt.title(r'$A \cup B$', fontsize=20, pad=0.1)
        venn.get_label_by_id('10').set_text('')  # Only A
        venn.get_label_by_id('01').set_text('')  # Only B
        venn.get_label_by_id('11').set_text('')  # A ∩ B
        venn.get_patch_by_id('10').set_color('#af8bce')  # Color only A
        venn.get_patch_by_id('01').set_color('#af8bce')  # Color only B
        venn.get_patch_by_id('11').set_color('#af8bce')  # Color A ∩ B
        venn.get_patch_by_id('10').set_edgecolor('#e2877f')  # Circle A outline color
        venn.get_patch_by_id('01').set_edgecolor('#7fb2e2')  # Circle B outline color
        venn.get_patch_by_id('10').set_linewidth(2)  # Circle A outline width
        venn.get_patch_by_id('01').set_linewidth(2)  # Circle B outline width
        venn.get_patch_by_id('10').set_alpha(0.7)
        venn.get_patch_by_id('01').set_alpha(0.7)
        venn.get_patch_by_id('11').set_alpha(0.7)
        st.write("**Union of A and B**: All elements from both events.")

    elif operation == "Intersection":
        # Color only the intersection for A ∩ B
        plt.title(r'$A \cap B$', fontsize=20, pad=0.1)
        venn.get_label_by_id('10').set_text('')  # Only A
        venn.get_label_by_id('01').set_text('')  # Only B
        venn.get_label_by_id('11').set_text('')  # A ∩ B
        venn.get_patch_by_id('10').set_color('white')  # Remove color for only A
        venn.get_patch_by_id('01').set_color('white')  # Remove color for only B
        venn.get_patch_by_id('11').set_color('#af8bce')  # Color only A ∩ B
        venn.get_patch_by_id('10').set_edgecolor('#e2877f')  # Circle A outline color
        venn.get_patch_by_id('01').set_edgecolor('#7fb2e2')  # Circle B outline color
        venn.get_patch_by_id('10').set_linewidth(2)  # Circle A outline width
        venn.get_patch_by_id('01').set_linewidth(2)  # Circle B outline width
        venn.get_patch_by_id('11').set_alpha(0.7)
        st.write("**Intersection of A and B**: Common elements between both events.")

    # Place the plot in the center column
    col1, col2, col3= st.columns([1, 3, 1])
    with col1:
        st.write("")  # Placeholder for the first column

    with col2:
        # Display the plot in the second column
        st.pyplot(fig)

    with col3:
        st.write("")  # Placeholder for the third column

    # Complementary Event Visualization
    st.write("## Complementary Event:")

    fig, ax = plt.subplots()

    # Adding a blank rectangle representing the sample space
    rect = mpatches.Rectangle((0, 0), 1, 1, linewidth=3, edgecolor='black', facecolor='#af8bce', alpha=0.7)
    ax.add_patch(rect)

    # Create a circle to represent event A
    circle = plt.Circle((0.5, 0.5), 0.3, color='white', ec='#e2877f', lw=2)  # White circle with blue edge
    ax.add_artist(circle)

    # Adding Ω and A lables
    ax.text(0.93, 0.07, r'$\Omega$', fontsize=26, ha='center', va='center')
    ax.text(0.5, 0.25, r'$A$', fontsize=14, ha='center', va='center')

    # Set limits and aspect
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal', adjustable='box')  # Maintain aspect ratio

    plt.title(r"Complement of Event A = $\overline{A}$")
    plt.axis('off')  # Hide the axes

    # Place the plot in the center column
    col1, col2, col3= st.columns([1, 3, 1])
    with col1:
        st.write("")  # Placeholder for the first column

    with col2:
        # Display the plot in the second column
        st.pyplot(fig)

    with col3:
        st.write("")  # Placeholder for the third column

    # The difference between events visualization
    st.write("## The difference between events:")

    # Create a figure
    fig, ax = plt.subplots()

    # Create a Venn diagram with event A colored and event B empty
    venn = venn2(subsets=(1, 1, 1), set_labels=('A', 'B'))

    # Adding a black rectangle representing the sample space
    rect = mpatches.Rectangle((-0.74, -0.557), 1.47, 1.06, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(rect)

    # Adding Ω label at the bottom right
    ax.text(0.65, -0.48, r'$\Omega$', fontsize=30, ha='center', va='center')

    # Customize the appearance
    venn.get_label_by_id('10').set_text('')  # Hide A label
    venn.get_label_by_id('01').set_text('')  # Hide B label
    venn.get_label_by_id('11').set_text('')  # Hide the label for A - B
    venn.get_patch_by_id('10').set_color('#af8bce')
    venn.get_patch_by_id('01').set_color('white') # Hide B circle
    venn.get_patch_by_id('11').set_color('white')  # Hide intersection
    venn.get_patch_by_id('10').set_edgecolor('#e2877f')  # Circle A outline color
    venn.get_patch_by_id('01').set_edgecolor('#7fb2e2')  # Circle B outline color
    venn.get_patch_by_id('10').set_linewidth(2)  # Circle A outline width
    venn.get_patch_by_id('01').set_linewidth(2)  # Circle B outline width
    venn.get_patch_by_id('11').set_linewidth(2)
    venn.get_patch_by_id('10').set_alpha(0.7)

    plt.title(r"A\B = $A \cap \overline{B}$", fontsize=18)
    plt.axis('off')  # Hide the axes

    # Place the plot in the center column
    col1, col2, col3= st.columns([1, 3, 1])
    with col1:
        st.write("")  # Placeholder for the first column

    with col2:
        # Display the plot in the second column
        st.pyplot(fig)

    with col3:
        st.write("")  # Placeholder for the third column

    # Foreign Events Visualization
    st.write("## Foreign Events:")

    # Create a figure
    fig, ax = plt.subplots()

    # Adding a blank rectangle representing the sample space
    rect = mpatches.Rectangle((0, 0), 1, 1, linewidth=3, edgecolor='black', facecolor='white')
    ax.add_patch(rect)

    # Create a circle for event A, colored blue
    circle_A = plt.Circle((0.28, 0.5), 0.21, color='#e2877f', alpha=0.7, label='A')  # Blue circle
    ax.add_artist(circle_A)

    # Create a circle for event B, colored green
    circle_B = plt.Circle((0.72, 0.5), 0.21, color='#7fb2e2', alpha=0.7, label='B')  # Green circle
    ax.add_artist(circle_B)

    # Adding Ω label at the bottom right
    ax.text(0.93, 0.07, r'$\Omega$', fontsize=26, ha='center', va='center')
    ax.text(0.28, 0.22, r'$A$', fontsize=14, ha='center', va='center')
    ax.text(0.71, 0.22, r'$B$', fontsize=14, ha='center', va='center')

    # Set limits and aspect
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal', adjustable='box')  # Maintain aspect ratio

    # Add titles and legends
    plt.title(r"$A \cap B = \emptyset$", fontsize=18)
    plt.axis('off')  # Hide the axes

    # Place the plot in the center column
    col1, col2, col3= st.columns([1, 3, 1])
    with col1:
        st.write("")  # Placeholder for the first column

    with col2:
        # Display the plot in the second column
        st.pyplot(fig)

    with col3:
        st.write("")  # Placeholder for the third column
