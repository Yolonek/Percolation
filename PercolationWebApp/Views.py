import streamlit as st


def home_page():
    text_to_display = r"""# <center>Percolation</center>

Percolation is a theory studying the behavior of connected clusters in a random system. It provides insight into a wide range of phenomena, like physics, mathematics and recently epidemiology.

The basic idea is to generate a grid of square sites, where each one of them can be occupied or not with a certain probability $p$. If many sites are occupied next to each other, they form a cluster. With increasing site occupation probability theese clusters grow larger. At a certain critical probability $p_c$ the cluster spans the entire system. We call this probability the <i>percolation threshold.</i> Mathematically, for infinite 2D system this percolation is equal:

### <center>$$p_c \approx 0.592756$$</center>

In this project we're going to use Monte Carlo techniques to analize phase transistions and clustering at various site occupation probabilities."""
    st.empty()
    st.markdown(text_to_display, unsafe_allow_html=True)