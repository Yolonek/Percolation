# <center>Percolation</center>

GitHub Repository for full project can be found [here](https://github.com/Yolonek/Percolation).

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

# <center>Spanning Cluster</center>

Second part of the project is to count and label every different cluster that was created on the 2D grid. We treat adjacent sites as a cluster if black squares around it created a closed loop. The goal is to see, that for a mentioned before critical probability $p_c$ there is a high chance that we can find a large cluster that spans most of the grid.

To find all cluster we are going to use <i>Hoshen-Kopelman</i> algorithm. It's a method used primarly in computational studies to identify and label clusters often used in percolation theory. In short, here are some key steps of the algorithm:

<ul>
    <li>First we set the nearest top left available square on the grid. We iterate through each site to the right and then we do it again with another row till the end of the lattice</li>
    <li>If top and left neighbours are unoccupied (have value $0$) we have found a new cluster</li>
    <li>If top or left square is occupied we can assign current square to an existing cluster</li>
    <li>If top and left squares belong to two different clusters, we have found a site that joins them together. We have to assign one of them to another, but important part is to change only the label, not every site because it will increase the simulation time substantially (one graph will show how much of a difference can it make)</li>
</ul>

After we have labelled all clusters, we can easilly count them, find the biggest one and plot histograms - which is exactly what we will do in the following part of the project.

This `streamlit` app is a tutorial about my project and how to use its objects and how they work. To navigate go to the ***Contents*** page and read about each section.

Below are presented graphs for larger simulations.
