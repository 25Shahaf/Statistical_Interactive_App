import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn2_circles, venn3
import matplotlib.patches as mpatches
from scipy.stats import alpha


def app():
    st.write("# Basic Definitions of Probability")

    st.write(r"### $P(A \cap B) + P(A \cap \overline{B}) = P(A)$")
    # Set up the figure and axes
    fig, ax = plt.subplots(figsize=(10, 3))
    plt.axis('off')

    # First Venn diagram: P(A∩B)
    ax1 = plt.subplot(131)
    venn1 = venn2(subsets=(1, 1, 1), set_labels=('A', 'B'), ax=ax1)
    venn1.get_label_by_id('10').set_text('')  # Only A
    venn1.get_label_by_id('01').set_text('')  # Only B
    venn1.get_label_by_id('11').set_text('')  # A ∩ B
    venn1.get_patch_by_id('10').set_color('white')  # Color only A
    venn1.get_patch_by_id('01').set_color('white')  # Color only B
    venn1.get_patch_by_id('11').set_color('#af8bce')  # Color A ∩ B
    venn1.get_patch_by_id('10').set_edgecolor('#e2877f')  # Circle A outline color
    venn1.get_patch_by_id('01').set_edgecolor('#7fb2e2')  # Circle B outline color
    venn1.get_patch_by_id('10').set_linewidth(2)  # Circle A outline width
    venn1.get_patch_by_id('01').set_linewidth(2)  # Circle B outline width
    venn1.get_patch_by_id('11').set_alpha(0.7)

    # Second Venn diagram: P(A ∩ B')
    ax2 = plt.subplot(132)
    venn11 = venn2(subsets=(1, 1, 1), set_labels=('A', 'B'), ax=ax2)
    venn11.get_label_by_id('10').set_text('')  # Only A
    venn11.get_label_by_id('01').set_text('')  # Only B
    venn11.get_label_by_id('11').set_text('')  # A ∩ B
    venn11.get_patch_by_id('10').set_color('#af8bce')  # Color only A
    venn11.get_patch_by_id('01').set_color('white')  # Color only B
    venn11.get_patch_by_id('11').set_color('white')  # Color A ∩ B
    venn11.get_patch_by_id('10').set_edgecolor('#e2877f')  # Circle A outline color
    venn11.get_patch_by_id('01').set_edgecolor('#7fb2e2')  # Circle B outline color
    venn11.get_patch_by_id('10').set_linewidth(2)  # Circle A outline width
    venn11.get_patch_by_id('01').set_linewidth(2)  # Circle B outline width
    venn11.get_patch_by_id('10').set_alpha(0.7)

    # Third Venn diagram: P(A)
    ax3 = plt.subplot(133)
    venn111 = venn2(subsets=(1, 1, 1), set_labels=('A', 'B'), ax=ax3)
    venn111.get_label_by_id('10').set_text('')  # Only A
    venn111.get_label_by_id('01').set_text('')  # Only B
    venn111.get_label_by_id('11').set_text('')  # A ∩ B
    venn111.get_patch_by_id('10').set_color('#af8bce')  # Color only A
    venn111.get_patch_by_id('01').set_color('white')  # Color only B
    venn111.get_patch_by_id('11').set_color('#af8bce')  # Color A ∩ B
    venn111.get_patch_by_id('10').set_edgecolor('#e2877f')  # Circle A outline color
    venn111.get_patch_by_id('01').set_edgecolor('#7fb2e2')  # Circle B outline color
    venn111.get_patch_by_id('10').set_linewidth(2)  # Circle A outline width
    venn111.get_patch_by_id('01').set_linewidth(2)  # Circle B outline width
    venn111.get_patch_by_id('10').set_alpha(0.7)
    venn111.get_patch_by_id('11').set_alpha(0.7)

    # Adding '+' and '=' signs
    ax1.annotate('+', xy=(0.74, 0.0), fontsize=24, ha='left', va='center', color='black')
    ax2.annotate('=', xy=(0.74, 0.0), fontsize=24, ha='left', va='center', color='black')

    # Adjust layout
    plt.subplots_adjust(wspace=0.1)

    st.pyplot(fig)