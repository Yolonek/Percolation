# <center>Percolation</center>

Percolation is a theory studying the behavior of connected clusters in a random system. It provides insight into a wide range of phenomena, like physics, mathematics and recently epidemiology.

The basic idea is to generate a grid of square sites, where each one of them can be occupied or not with a certain probability $p$. If many sites are occupied next to each other, they form a cluster. With increasing site occupation probability theese clusters grow larger. At a certain critical probability $p_c$ the cluster spans the entire system. We call this probability the <i>percolation threshold.</i> Mathematically, for infinite 2D system this percolation is equal:

### <center>$$p_c \approx 0.592756$$</center>

In this project we're going to use Monte Carlo techniques to analyze phase transitions and clustering at various site occupation probabilities.

# <center>Burning Model</center>

The Burning Algorithm is a type of percolation process. It provides a simulation of dynamic spread of some phenomenon across a network lattice. It uses an analogy of forest fire, where we initiate one grid as a tree and we simulate how far the fire is able to spread.

<ul>
    <li>We initiate by setting on fire top row of a grid</li>
    <li>In each step we try to set on fire adjacent sites that are occupied</li>
    <li>We keep going until the fire stops or it gets to the last row of a grid</li>
</ul>

If fire reaches the last row it means that percolation happened. Let's implement it in a code.

This `streamlit` app is a tutorial about my project and how to use its objects and how they work. To navigate go to the ***Contents*** page and read about each section.

Below are presented graphs for larger simulations.
