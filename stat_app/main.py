import streamlit as st
import pandas as pd
import numpy as np

st.write("hello world")

df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

df

st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))

st.write("This is a dynamic table:")
dataframe1 = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe1.style.highlight_max(axis=0))

st.write("This is a static table:")
dataframe2 = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))
st.table(dataframe2)

st.write("This is a line chart:")
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)

st.write("This is a widget:")
x = st.slider('x')
st.write(x, 'squared is', x * x)

st.write("This is a checkbox example:")
if st.checkbox('Show dataframe'):
    chart_data2 = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    chart_data2

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)



"""
# Visualize the chain rule
if section == "Chain Rule":
    st.title("Chain Rule of Probability for Three Events")

    # Explanation of Chain Rule
    st.write(\"""
    The chain rule of probability for three events \(A\), \(B\), and \(C\) states that:\\
    \\
    $$ P(A \cap B \cap C) = P(A) \cdot P(B | A) \cdot P(C | A \cap B) $$

    This means that the probability of all three events happening is the product of:
    1. The probability of \(A\),
    2. The conditional probability of \(B\) given \(A\),
    3. The conditional probability of \(C\) given both \(A\) and \(B\).
    \""")

    # Sliders for user input on probabilities
    p_A = 0.6
    p_B_given_A = 0.7
    p_C_given_AB = 0.8

    # Calculating the chain rule
    p_ABC = p_A * p_B_given_A * p_C_given_AB

    # Display the result
    st.write(f"Using the chain rule of probability, we get:")
    st.latex(f"P(A \\cap B \\cap C) = {p_A} \\times {p_B_given_A} \\times {p_C_given_AB} = {p_ABC:.3f}")

    # Create the Venn diagram for A, B, C
    fig, ax = plt.subplots()

    venn = venn3(subsets=(p_A,
                          p_B_given_A * (1 - p_A),
                          p_A * p_B_given_A,
                          (1 - p_B_given_A) * (1 - p_A),
                          p_A * (1 - p_B_given_A),
                          p_B_given_A * p_A * (1 - p_C_given_AB),
                          p_ABC),
                 set_labels=('A', 'B', 'C'))

    # Customize the text for the areas
    venn.get_label_by_id('100').set_text(f'P(A): {p_A:.2f}')
    venn.get_label_by_id('010').set_text(f'P(B | A): {p_B_given_A:.2f}')
    venn.get_label_by_id('001').set_text(f'P(C | A ∩ B): {p_C_given_AB:.2f}')
    venn.get_label_by_id('111').set_text(f'P(A ∩ B ∩ C): {p_ABC:.2f}')

    # Hide the labels for P(A ∩ B), P(B ∩ C), and P(A ∩ C)
    if venn.get_label_by_id('110'):
        venn.get_label_by_id('110').set_text('')
    if venn.get_label_by_id('101'):
        venn.get_label_by_id('101').set_text('')
    if venn.get_label_by_id('011'):
        venn.get_label_by_id('011').set_text('')

    # Set text size smaller
    for label in ['100', '010', '001', '111']:
        if venn.get_label_by_id(label):
            venn.get_label_by_id(label).set_fontsize(8)

    # Add legend for clarity
    legend_patches = [
        mpatches.Patch(color=venn.get_patch_by_id('100').get_facecolor(), label="A"),
        mpatches.Patch(color=venn.get_patch_by_id('010').get_facecolor(), label="B"),
        mpatches.Patch(color=venn.get_patch_by_id('001').get_facecolor(), label="C")
    ]
    ax.legend(handles=legend_patches, loc='upper right', title="Events")

    # Display the diagram
    st.pyplot(fig)
"""