import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import matplotlib.patches as mpatches
from scipy.stats import alpha

def app():
    st.write("## Normal Distribution Histogram")

    mean = st.slider("Mean", -10.0, 10.0, 0.0)
    std_dev = st.slider("Standard Deviation", 0.1, 5.0, 1.0)

    data = np.random.normal(mean, std_dev, 1000)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(data, bins=30, color='#7fb2e2', edgecolor='black')
    # ax.set_title('Histogram of Normal Distribution')
    ax.set_xlabel('Value')
    ax.set_ylabel('Frequency')
    ax.set_xlim([-20, 30])
    ax.set_ylim([0, 105])

    # Place the plot in the center column
    col1, col2, col3 = st.columns([1, 5, 1])
    with col1:
        st.write("")  # Placeholder for the first column

    with col2:
        # Display the plot in the second column
        st.pyplot(fig)

    with col3:
        st.write("")  # Placeholder for the third column