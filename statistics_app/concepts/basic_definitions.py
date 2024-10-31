import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn2_circles, venn3
import matplotlib.patches as mpatches
from scipy.stats import alpha


def app():
    st.write("# Basic Definitions in Probability")

    st.write(r"### $P(A) = P(A \cap B) + P(A \cap \overline{B})$")
    # Set up the figure and axes
    fig, ax = plt.subplots(figsize=(10, 3))
    plt.axis('off')

    # First Venn diagram: P(A∩B)
    ax1 = plt.subplot(131)
    venn_1 = venn2(subsets=(1, 1, 1), set_labels=('A', 'B'), ax=ax1)
    venn_1.get_label_by_id('10').set_text('')  # Only A
    venn_1.get_label_by_id('01').set_text('')  # Only B
    venn_1.get_label_by_id('11').set_text('')  # A ∩ B
    venn_1.get_patch_by_id('10').set_color('white')  # Color only A
    venn_1.get_patch_by_id('01').set_color('white')  # Color only B
    venn_1.get_patch_by_id('11').set_color('#af8bce')  # Color A ∩ B
    venn_1.get_patch_by_id('10').set_edgecolor('#e2877f')  # Circle A outline color
    venn_1.get_patch_by_id('01').set_edgecolor('#7fb2e2')  # Circle B outline color
    venn_1.get_patch_by_id('10').set_linewidth(2)  # Circle A outline width
    venn_1.get_patch_by_id('01').set_linewidth(2)  # Circle B outline width
    venn_1.get_patch_by_id('11').set_alpha(0.7)

    # Second Venn diagram: P(A ∩ B')
    ax2 = plt.subplot(132)
    venn_2 = venn2(subsets=(1, 1, 1), set_labels=('A', 'B'), ax=ax2)
    venn_2.get_label_by_id('10').set_text('')  # Only A
    venn_2.get_label_by_id('01').set_text('')  # Only B
    venn_2.get_label_by_id('11').set_text('')  # A ∩ B
    venn_2.get_patch_by_id('10').set_color('#af8bce')  # Color only A
    venn_2.get_patch_by_id('01').set_color('white')  # Color only B
    venn_2.get_patch_by_id('11').set_color('white')  # Color A ∩ B
    venn_2.get_patch_by_id('10').set_edgecolor('#e2877f')  # Circle A outline color
    venn_2.get_patch_by_id('01').set_edgecolor('#7fb2e2')  # Circle B outline color
    venn_2.get_patch_by_id('10').set_linewidth(2)  # Circle A outline width
    venn_2.get_patch_by_id('01').set_linewidth(2)  # Circle B outline width
    venn_2.get_patch_by_id('10').set_alpha(0.7)

    # Third Venn diagram: P(A)
    ax3 = plt.subplot(133)
    venn_3 = venn2(subsets=(1, 1, 1), set_labels=('A', 'B'), ax=ax3)
    venn_3.get_label_by_id('10').set_text('')  # Only A
    venn_3.get_label_by_id('01').set_text('')  # Only B
    venn_3.get_label_by_id('11').set_text('')  # A ∩ B
    venn_3.get_patch_by_id('10').set_color('#af8bce')  # Color only A
    venn_3.get_patch_by_id('01').set_color('white')  # Color only B
    venn_3.get_patch_by_id('11').set_color('#af8bce')  # Color A ∩ B
    venn_3.get_patch_by_id('10').set_edgecolor('#e2877f')  # Circle A outline color
    venn_3.get_patch_by_id('01').set_edgecolor('#7fb2e2')  # Circle B outline color
    venn_3.get_patch_by_id('10').set_linewidth(2)  # Circle A outline width
    venn_3.get_patch_by_id('01').set_linewidth(2)  # Circle B outline width
    venn_3.get_patch_by_id('10').set_alpha(0.7)
    venn_3.get_patch_by_id('11').set_alpha(0.7)

    # Adding '+' and '=' signs
    ax1.annotate('+', xy=(0.74, 0.0), fontsize=24, ha='left', va='center', color='black')
    ax2.annotate('=', xy=(0.74, 0.0), fontsize=24, ha='left', va='center', color='black')

    # Adjust layout
    plt.subplots_adjust(wspace=0.1)

    st.pyplot(fig)

    st.write(r"### $P(A \cup B) = P(A) + P(B) - P(A \cap B)$")
    # Set up the figure and axes
    fig, ax = plt.subplots(figsize=(10, 3))
    plt.axis('off')

    # First Venn diagram: P(A)
    ax1 = plt.subplot(141)
    venn_1 = venn2(subsets=(1, 1, 1), set_labels=('A', 'B'), ax=ax1)
    venn_1.get_label_by_id('10').set_text('')  # Only A
    venn_1.get_label_by_id('01').set_text('')  # Only B
    venn_1.get_label_by_id('11').set_text('')  # A ∩ B
    venn_1.get_patch_by_id('10').set_color('#af8bce')  # Color only A
    venn_1.get_patch_by_id('01').set_color('white')  # Color only B
    venn_1.get_patch_by_id('11').set_color('#af8bce')  # Color A ∩ B
    venn_1.get_patch_by_id('10').set_edgecolor('#e2877f')  # Circle A outline color
    venn_1.get_patch_by_id('01').set_edgecolor('#7fb2e2')  # Circle B outline color
    venn_1.get_patch_by_id('10').set_linewidth(2)  # Circle A outline width
    venn_1.get_patch_by_id('01').set_linewidth(2)  # Circle B outline width
    venn_1.get_patch_by_id('11').set_alpha(0.7)
    venn_1.get_patch_by_id('10').set_alpha(0.7)

    # second Venn diagram: P(B)
    ax2 = plt.subplot(142)
    venn_2 = venn2(subsets=(1, 1, 1), set_labels=('A', 'B'), ax=ax2)
    venn_2.get_label_by_id('10').set_text('')  # Only A
    venn_2.get_label_by_id('01').set_text('')  # Only B
    venn_2.get_label_by_id('11').set_text('')  # A ∩ B
    venn_2.get_patch_by_id('10').set_color('white')  # Color only A
    venn_2.get_patch_by_id('01').set_color('#af8bce')  # Color only B
    venn_2.get_patch_by_id('11').set_color('#af8bce')  # Color A ∩ B
    venn_2.get_patch_by_id('10').set_edgecolor('#e2877f')  # Circle A outline color
    venn_2.get_patch_by_id('01').set_edgecolor('#7fb2e2')  # Circle B outline color
    venn_2.get_patch_by_id('10').set_linewidth(2)  # Circle A outline width
    venn_2.get_patch_by_id('01').set_linewidth(2)  # Circle B outline width
    venn_2.get_patch_by_id('01').set_alpha(0.7)
    venn_2.get_patch_by_id('11').set_alpha(0.7)

    # third Venn diagram: P(A ∩ B)
    ax3 = plt.subplot(143)
    venn_3 = venn2(subsets=(1, 1, 1), set_labels=('A', 'B'), ax=ax3)
    venn_3.get_label_by_id('10').set_text('')  # Only A
    venn_3.get_label_by_id('01').set_text('')  # Only B
    venn_3.get_label_by_id('11').set_text('')  # A ∩ B
    venn_3.get_patch_by_id('10').set_color('white')  # Color only A
    venn_3.get_patch_by_id('01').set_color('white')  # Color only B
    venn_3.get_patch_by_id('11').set_color('#af8bce')  # Color A ∩ B
    venn_3.get_patch_by_id('10').set_edgecolor('#e2877f')  # Circle A outline color
    venn_3.get_patch_by_id('01').set_edgecolor('#7fb2e2')  # Circle B outline color
    venn_3.get_patch_by_id('10').set_linewidth(2)  # Circle A outline width
    venn_3.get_patch_by_id('01').set_linewidth(2)  # Circle B outline width
    venn_3.get_patch_by_id('11').set_alpha(0.7)

    # Forth Venn diagram: P(A ∪ B)
    ax4 = plt.subplot(144)
    venn_4 = venn2(subsets=(1, 1, 1), set_labels=('A', 'B'), ax=ax4)
    venn_4.get_label_by_id('10').set_text('')  # Only A
    venn_4.get_label_by_id('01').set_text('')  # Only B
    venn_4.get_label_by_id('11').set_text('')  # A ∩ B
    venn_4.get_patch_by_id('10').set_color('#af8bce')  # Color only A
    venn_4.get_patch_by_id('01').set_color('#af8bce')  # Color only B
    venn_4.get_patch_by_id('11').set_color('#af8bce')  # Color A ∩ B
    venn_4.get_patch_by_id('10').set_edgecolor('#e2877f')  # Circle A outline color
    venn_4.get_patch_by_id('01').set_edgecolor('#7fb2e2')  # Circle B outline color
    venn_4.get_patch_by_id('10').set_linewidth(2)  # Circle A outline width
    venn_4.get_patch_by_id('01').set_linewidth(2)  # Circle B outline width
    venn_4.get_patch_by_id('10').set_alpha(0.7)
    venn_4.get_patch_by_id('11').set_alpha(0.7)
    venn_4.get_patch_by_id('01').set_alpha(0.7)


    # Adding '+' and '=' signs
    ax1.annotate('+', xy=(0.74, 0.0), fontsize=24, ha='left', va='center', color='black')
    ax2.annotate('—', xy=(0.68, 0.0), fontsize=24, ha='left', va='center', color='black')
    ax3.annotate('=', xy=(0.74, 0.0), fontsize=24, ha='left', va='center', color='black')

    # Adjust layout
    plt.subplots_adjust(wspace=0.1)

    st.pyplot(fig)

    st.write(r"### $P(A \cup B \cup C) = P(A) + P(B) + P(C) - P(A \cap B) - P(A \cap C) - P(B \cap C) + P(A \cap B \cap C)$")
    # Set up the figure and axes
    fig, ax = plt.subplots(figsize=(10, 3))
    plt.axis('off')

    # First Venn diagram: P(A)
    ax1 = plt.subplot(241)
    venn_1 = venn3(subsets=(1, 1, 1, 1, 1, 1, 1), set_labels=('A', 'B', 'C'), ax=ax1)
    venn_1.get_label_by_id('100').set_text('')  # Only A
    venn_1.get_label_by_id('010').set_text('')  # Only B
    venn_1.get_label_by_id('001').set_text('')  # Only C
    venn_1.get_label_by_id('110').set_text('')  # A ∩ B
    venn_1.get_label_by_id('101').set_text('')  # A ∩ C
    venn_1.get_label_by_id('011').set_text('')  # B ∩ C
    venn_1.get_label_by_id('111').set_text('')  # A ∩ B ∩ C
    venn_1.get_patch_by_id('100').set_color('#af8bce')  # Color only A
    venn_1.get_patch_by_id('010').set_color('white')  # Color only B
    venn_1.get_patch_by_id('001').set_color('white')  # Color only C
    venn_1.get_patch_by_id('110').set_color('#af8bce')  # Color A ∩ B
    venn_1.get_patch_by_id('101').set_color('#af8bce')  # Color A ∩ C
    venn_1.get_patch_by_id('011').set_color('white')  # Color B ∩ C
    venn_1.get_patch_by_id('111').set_color('#af8bce')  # Color A ∩ B ∩ C
    venn_1.get_patch_by_id('100').set_edgecolor('#e2877f')  # Circle A outline color
    venn_1.get_patch_by_id('010').set_edgecolor('#7fb2e2')  # Circle B outline color
    venn_1.get_patch_by_id('001').set_edgecolor('#6bca93')  # Circle C outline color
    venn_1.get_patch_by_id('100').set_linewidth(2)  # Circle A outline width
    venn_1.get_patch_by_id('010').set_linewidth(2)  # Circle B outline width
    venn_1.get_patch_by_id('001').set_linewidth(2)  # Circle C outline width
    venn_1.get_patch_by_id('100').set_alpha(0.7)
    venn_1.get_patch_by_id('110').set_alpha(0.7)
    venn_1.get_patch_by_id('101').set_alpha(0.7)
    venn_1.get_patch_by_id('111').set_alpha(0.7)

    # Second Venn diagram: P(B)
    ax2 = plt.subplot(242)
    venn_2 = venn3(subsets=(1, 1, 1, 1, 1, 1, 1), set_labels=('A', 'B', 'C'), ax=ax2)
    venn_2.get_label_by_id('100').set_text('')  # Only A
    venn_2.get_label_by_id('010').set_text('')  # Only B
    venn_2.get_label_by_id('001').set_text('')  # Only C
    venn_2.get_label_by_id('110').set_text('')  # A ∩ B
    venn_2.get_label_by_id('101').set_text('')  # A ∩ C
    venn_2.get_label_by_id('011').set_text('')  # B ∩ C
    venn_2.get_label_by_id('111').set_text('')  # A ∩ B ∩ C
    venn_2.get_patch_by_id('100').set_color('white')  # Color only A
    venn_2.get_patch_by_id('010').set_color('#af8bce')  # Color only B
    venn_2.get_patch_by_id('001').set_color('white')  # Color only C
    venn_2.get_patch_by_id('110').set_color('#af8bce')  # Color A ∩ B
    venn_2.get_patch_by_id('101').set_color('white')  # Color A ∩ C
    venn_2.get_patch_by_id('011').set_color('#af8bce')  # Color B ∩ C
    venn_2.get_patch_by_id('111').set_color('#af8bce')  # Color A ∩ B ∩ C
    venn_2.get_patch_by_id('100').set_edgecolor('#e2877f')  # Circle A outline color
    venn_2.get_patch_by_id('010').set_edgecolor('#7fb2e2')  # Circle B outline color
    venn_2.get_patch_by_id('001').set_edgecolor('#6bca93')  # Circle C outline color
    venn_2.get_patch_by_id('010').set_linewidth(2)  # Circle B outline width
    venn_2.get_patch_by_id('011').set_linewidth(2)  # Circle B outline width
    venn_2.get_patch_by_id('110').set_alpha(0.7)
    venn_2.get_patch_by_id('011').set_alpha(0.7)
    venn_2.get_patch_by_id('010').set_alpha(0.7)
    venn_2.get_patch_by_id('111').set_alpha(0.7)

    # Third Venn diagram: P(C)
    ax3 = plt.subplot(243)
    venn_3 = venn3(subsets=(1, 1, 1, 1, 1, 1, 1), set_labels=('A', 'B', 'C'), ax=ax3)
    venn_3.get_label_by_id('100').set_text('')  # Only A
    venn_3.get_label_by_id('010').set_text('')  # Only B
    venn_3.get_label_by_id('001').set_text('')  # Only C
    venn_3.get_label_by_id('110').set_text('')  # A ∩ B
    venn_3.get_label_by_id('101').set_text('')  # A ∩ C
    venn_3.get_label_by_id('011').set_text('')  # B ∩ C
    venn_3.get_label_by_id('111').set_text('')  # A ∩ B ∩ C
    venn_3.get_patch_by_id('100').set_color('white')  # Color only A
    venn_3.get_patch_by_id('010').set_color('white')  # Color only B
    venn_3.get_patch_by_id('001').set_color('#af8bce')  # Color only C
    venn_3.get_patch_by_id('110').set_color('white')  # Color A ∩ B
    venn_3.get_patch_by_id('101').set_color('#af8bce')  # Color A ∩ C
    venn_3.get_patch_by_id('011').set_color('#af8bce')  # Color B ∩ C
    venn_3.get_patch_by_id('111').set_color('#af8bce')  # Color A ∩ B ∩ C
    venn_3.get_patch_by_id('100').set_edgecolor('#e2877f')  # Circle A outline color
    venn_3.get_patch_by_id('010').set_edgecolor('#7fb2e2')  # Circle B outline color
    venn_3.get_patch_by_id('001').set_edgecolor('#6bca93')  # Circle C outline color
    venn_3.get_patch_by_id('001').set_linewidth(2)  # Circle C outline width
    venn_3.get_patch_by_id('101').set_linewidth(2)  # Circle C outline width
    venn_3.get_patch_by_id('011').set_alpha(0.7)
    venn_3.get_patch_by_id('101').set_alpha(0.7)
    venn_3.get_patch_by_id('001').set_alpha(0.7)
    venn_3.get_patch_by_id('111').set_alpha(0.7)

    # Fourth Venn diagram: P(A ∩ B)
    ax4 = plt.subplot(244)
    venn_4 = venn3(subsets=(1, 1, 1, 1, 1, 1, 1), set_labels=('A', 'B', 'C'), ax=ax4)
    venn_4.get_label_by_id('100').set_text('')  # Only A
    venn_4.get_label_by_id('010').set_text('')  # Only B
    venn_4.get_label_by_id('001').set_text('')  # Only C
    venn_4.get_label_by_id('110').set_text('')  # A ∩ B
    venn_4.get_label_by_id('101').set_text('')  # A ∩ C
    venn_4.get_label_by_id('011').set_text('')  # B ∩ C
    venn_4.get_label_by_id('111').set_text('')  # A ∩ B ∩ C
    venn_4.get_patch_by_id('100').set_color('white')  # Color only A
    venn_4.get_patch_by_id('010').set_color('white')  # Color only B
    venn_4.get_patch_by_id('001').set_color('white')  # Color only C
    venn_4.get_patch_by_id('110').set_color('#af8bce')  # Color A ∩ B
    venn_4.get_patch_by_id('101').set_color('white')  # Color A ∩ C
    venn_4.get_patch_by_id('011').set_color('white')  # Color B ∩ C
    venn_4.get_patch_by_id('111').set_color('#af8bce')  # Color A ∩ B ∩ C
    venn_4.get_patch_by_id('100').set_edgecolor('#e2877f')  # Circle A outline color
    venn_4.get_patch_by_id('010').set_edgecolor('#7fb2e2')  # Circle B outline color
    venn_4.get_patch_by_id('001').set_edgecolor('#6bca93')  # Circle C outline color
    venn_4.get_patch_by_id('100').set_linewidth(2)  # Circle A outline width
    venn_4.get_patch_by_id('010').set_linewidth(2)  # Circle B outline width
    venn_4.get_patch_by_id('110').set_alpha(0.7)
    venn_4.get_patch_by_id('111').set_alpha(0.7)

    # Fifth Venn diagram: P(A ∩ C)
    ax5 = plt.subplot(245)
    venn_5 = venn3(subsets=(1, 1, 1, 1, 1, 1, 1), set_labels=('A', 'B', 'C'), ax=ax5)
    venn_5.get_label_by_id('100').set_text('')  # Only A
    venn_5.get_label_by_id('010').set_text('')  # Only B
    venn_5.get_label_by_id('001').set_text('')  # Only C
    venn_5.get_label_by_id('110').set_text('')  # A ∩ B
    venn_5.get_label_by_id('101').set_text('')  # A ∩ C
    venn_5.get_label_by_id('011').set_text('')  # B ∩ C
    venn_5.get_label_by_id('111').set_text('')  # A ∩ B ∩ C
    venn_5.get_patch_by_id('100').set_color('white')  # Color only A
    venn_5.get_patch_by_id('010').set_color('white')  # Color only B
    venn_5.get_patch_by_id('001').set_color('white')  # Color only C
    venn_5.get_patch_by_id('110').set_color('white')  # Color A ∩ B
    venn_5.get_patch_by_id('101').set_color('#af8bce')  # Color A ∩ C
    venn_5.get_patch_by_id('011').set_color('white')  # Color B ∩ C
    venn_5.get_patch_by_id('111').set_color('#af8bce')  # Color A ∩ B ∩ C
    venn_5.get_patch_by_id('100').set_edgecolor('#e2877f')  # Circle A outline color
    venn_5.get_patch_by_id('010').set_edgecolor('#7fb2e2')  # Circle B outline color
    venn_5.get_patch_by_id('001').set_edgecolor('#6bca93')  # Circle C outline color
    venn_5.get_patch_by_id('100').set_linewidth(2)  # Circle A outline width
    venn_5.get_patch_by_id('001').set_linewidth(2)  # Circle C outline width
    venn_5.get_patch_by_id('101').set_alpha(0.7)
    venn_5.get_patch_by_id('111').set_alpha(0.7)

    # Sixth Venn diagram: P(B ∩ C)
    ax6 = plt.subplot(246)
    venn_6 = venn3(subsets=(1, 1, 1, 1, 1, 1, 1), set_labels=('A', 'B', 'C'), ax=ax6)
    venn_6.get_label_by_id('100').set_text('')  # Only A
    venn_6.get_label_by_id('010').set_text('')  # Only B
    venn_6.get_label_by_id('001').set_text('')  # Only C
    venn_6.get_label_by_id('110').set_text('')  # A ∩ B
    venn_6.get_label_by_id('101').set_text('')  # A ∩ C
    venn_6.get_label_by_id('011').set_text('')  # B ∩ C
    venn_6.get_label_by_id('111').set_text('')  # A ∩ B ∩ C
    venn_6.get_patch_by_id('100').set_color('white')  # Color only A
    venn_6.get_patch_by_id('010').set_color('white')  # Color only B
    venn_6.get_patch_by_id('001').set_color('white')  # Color only C
    venn_6.get_patch_by_id('110').set_color('white')  # Color A ∩ B
    venn_6.get_patch_by_id('101').set_color('white')  # Color A ∩ C
    venn_6.get_patch_by_id('011').set_color('#af8bce')  # Color B ∩ C
    venn_6.get_patch_by_id('111').set_color('#af8bce')  # Color A ∩ B ∩ C
    venn_6.get_patch_by_id('100').set_edgecolor('#e2877f')  # Circle A outline color
    venn_6.get_patch_by_id('010').set_edgecolor('#7fb2e2')  # Circle B outline color
    venn_6.get_patch_by_id('001').set_edgecolor('#6bca93')  # Circle C outline color
    venn_6.get_patch_by_id('010').set_linewidth(2)  # Circle B outline width
    venn_6.get_patch_by_id('001').set_linewidth(2)  # Circle C outline width
    venn_6.get_patch_by_id('011').set_alpha(0.7)
    venn_6.get_patch_by_id('111').set_alpha(0.7)

    # Seventh Venn diagram: P(A ∩ B ∩ C)
    ax7 = plt.subplot(247)
    venn_7 = venn3(subsets=(1, 1, 1, 1, 1, 1, 1), set_labels=('A', 'B', 'C'), ax=ax7)
    venn_7.get_label_by_id('100').set_text('')  # Only A
    venn_7.get_label_by_id('010').set_text('')  # Only B
    venn_7.get_label_by_id('001').set_text('')  # Only C
    venn_7.get_label_by_id('110').set_text('')  # A ∩ B
    venn_7.get_label_by_id('101').set_text('')  # A ∩ C
    venn_7.get_label_by_id('011').set_text('')  # B ∩ C
    venn_7.get_label_by_id('111').set_text('')  # A ∩ B ∩ C
    venn_7.get_patch_by_id('100').set_color('white')  # Color only A
    venn_7.get_patch_by_id('010').set_color('white')  # Color only B
    venn_7.get_patch_by_id('001').set_color('white')  # Color only C
    venn_7.get_patch_by_id('110').set_color('white')  # Color A ∩ B
    venn_7.get_patch_by_id('101').set_color('white')  # Color A ∩ C
    venn_7.get_patch_by_id('011').set_color('white')  # Color B ∩ C
    venn_7.get_patch_by_id('111').set_color('#af8bce')  # Color A ∩ B ∩ C
    venn_7.get_patch_by_id('100').set_edgecolor('#e2877f')  # Circle A outline color
    venn_7.get_patch_by_id('010').set_edgecolor('#7fb2e2')  # Circle B outline color
    venn_7.get_patch_by_id('001').set_edgecolor('#6bca93')  # Circle C outline color
    venn_7.get_patch_by_id('100').set_linewidth(2)  # Circle A outline width
    venn_7.get_patch_by_id('010').set_linewidth(2)  # Circle B outline width
    venn_7.get_patch_by_id('001').set_linewidth(2)  # Circle C outline width
    venn_7.get_patch_by_id('111').set_alpha(0.7)

    # Eighth Venn diagram: P(A ∪ B ∪ C)
    ax8 = plt.subplot(248)
    venn_8 = venn3(subsets=(1, 1, 1, 1, 1, 1, 1), set_labels=('A', 'B', 'C'), ax=ax8)
    venn_8.get_label_by_id('100').set_text('')  # Only A
    venn_8.get_label_by_id('010').set_text('')  # Only B
    venn_8.get_label_by_id('001').set_text('')  # Only C
    venn_8.get_label_by_id('110').set_text('')  # A ∩ B
    venn_8.get_label_by_id('101').set_text('')  # A ∩ C
    venn_8.get_label_by_id('011').set_text('')  # B ∩ C
    venn_8.get_label_by_id('111').set_text('')  # A ∩ B ∩ C
    venn_8.get_patch_by_id('100').set_color('#af8bce')  # Color only A
    venn_8.get_patch_by_id('010').set_color('#af8bce')  # Color only B
    venn_8.get_patch_by_id('001').set_color('#af8bce')  # Color only C
    venn_8.get_patch_by_id('110').set_color('#af8bce')  # Color A ∩ B
    venn_8.get_patch_by_id('101').set_color('#af8bce')  # Color A ∩ C
    venn_8.get_patch_by_id('011').set_color('#af8bce')  # Color B ∩ C
    venn_8.get_patch_by_id('111').set_color('#af8bce')  # Color A ∩ B ∩ C
    venn_8.get_patch_by_id('100').set_edgecolor('#e2877f')  # Circle A outline color
    venn_8.get_patch_by_id('010').set_edgecolor('#7fb2e2')  # Circle B outline color
    venn_8.get_patch_by_id('001').set_edgecolor('#6bca93')  # Circle C outline color
    venn_8.get_patch_by_id('100').set_linewidth(2)  # Circle A outline width
    venn_8.get_patch_by_id('010').set_linewidth(2)  # Circle B outline width
    venn_8.get_patch_by_id('001').set_linewidth(2)  # Circle C outline width
    venn_8.get_patch_by_id('110').set_alpha(0.7)
    venn_8.get_patch_by_id('101').set_alpha(0.7)
    venn_8.get_patch_by_id('001').set_alpha(0.7)
    venn_8.get_patch_by_id('111').set_alpha(0.7)
    venn_8.get_patch_by_id('100').set_alpha(0.7)
    venn_8.get_patch_by_id('010').set_alpha(0.7)
    venn_8.get_patch_by_id('011').set_alpha(0.7)

    # Adding '+' and '=' signs
    ax2.annotate('+', xy=(-0.7, 0.0), fontsize=24, ha='right', va='center', color='black')
    ax3.annotate('+', xy=(-0.7, 0.0), fontsize=24, ha='right', va='center', color='black')
    ax4.annotate('—', xy=(-0.7, 0.0), fontsize=24, ha='right', va='center', color='black')
    ax5.annotate('—', xy=(-0.7, 0.0), fontsize=24, ha='right', va='center', color='black')
    ax6.annotate('—', xy=(-0.7, 0.0), fontsize=24, ha='right', va='center', color='black')
    ax7.annotate('+', xy=(-0.7, 0.0), fontsize=24, ha='right', va='center', color='black')
    ax8.annotate('=', xy=(-0.7, 0.0), fontsize=24, ha='right', va='center', color='black')

    # Adjust layout
    plt.subplots_adjust(wspace=0.1)

    st.pyplot(fig)

