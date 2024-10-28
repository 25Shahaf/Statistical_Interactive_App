import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn2_circles, venn3
import matplotlib.patches as mpatches
from scipy.stats import alpha

# Set the password for the app
PASSWORD = "BGU123"

# Initialize session state variable for password attempts
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Function to display password input
def login():
    if st.session_state['authenticated']:
        return  # Return early if already authenticated

    # Create a text input for the password
    password = st.text_input("Enter password", type="password", key="password_input")

    # Check if the button is clicked
    if st.button("Submit"):
        # If the password is correct
        if password == PASSWORD:
            st.session_state['authenticated'] = True  # Successful login
            st.success("Correct Password! Please click the 'Submit' button again to login.")  # Optional success message
        elif password:  # Check only if the password is not empty
            st.error("Incorrect password")


if st.session_state['authenticated']:
    st.title("Statistical Visualizations")

    # Sidebar for navigation
    section = st.sidebar.radio("Select a Concept", ["Basic Concepts", "Conditional Probability",
                                                    "Normal Distribution"])

    # Visualize union an intersection concepts
    if section == "Basic Concepts":
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

    # Visualize a normal distribution
    if section == "Normal Distribution":
        st.write("## Normal Distribution Histogram")

        mean = st.slider("Mean", -10.0, 10.0, 0.0)
        std_dev = st.slider("Standard Deviation", 0.1, 5.0, 1.0)

        data = np.random.normal(mean, std_dev, 1000)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(data, bins=30, color='#7fb2e2', edgecolor='black')
        #ax.set_title('Histogram of Normal Distribution')
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')
        ax.set_xlim([-20, 30])
        ax.set_ylim([0, 105])

        # Place the plot in the center column
        col1, col2, col3= st.columns([1, 5, 1])
        with col1:
            st.write("")  # Placeholder for the first column

        with col2:
            # Display the plot in the second column
            st.pyplot(fig)

        with col3:
            st.write("")  # Placeholder for the third column


    # Visualize conditional probability
    if section == "Conditional Probability":
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
        venn2 = venn2(subsets=(p_A, p_B, p_A_given_B), ax=ax2, set_labels=('', ''))

        # Setting the properties for the circle
        venn2.get_patch_by_id('01').set_color('#7fb2e2')  # Blue color for B
        venn2.get_patch_by_id('11').set_color('#af8bce')  # Purple color for intersection
        venn2.get_patch_by_id('10').set_color('white')  # Remove color for only A
        venn2.get_label_by_id('01').set_text(r'P(B)')  # Label for B
        venn2.get_label_by_id('11').set_text(r'P(A ∩ B)')  # Intersection label
        venn2.get_label_by_id('10').set_text('')  # Remove label for only A

        # Adding a black circle around the second Venn diagram
        circle = plt.Circle((0.22, 0.004), 0.45, color='black', fill=False, linewidth=2)
        ax2.add_artist(circle)

        # Adding a right arrow on the left side of the diagram
        arrow = plt.Arrow(-0.7, 0, 0.4, 0, width=0.1, color='black')
        ax2.add_patch(arrow)

        # Adding Ω label inside the B area
        ax2.text(0.35, -0.3, r'$\Omega$', fontsize=30, ha='center', va='center')

        # Placing the plots side by side
        col1, col2= st.columns([1, 1])
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

else:
    login()
    st.write("Please enter the password to access the app.")