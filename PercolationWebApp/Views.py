import streamlit as st
from Backend import *


def home_page():
    image_list = [
        '../images/ProbabilitySiteL30p-0.3-0.5-0.7.png',
        '../images/ProbabilitySiteL300p-0.3-0.5-0.7.png',
        '../BurningModel/images/PercolationGraphL10p-0.5-0.6-0.7.png',
        '../BurningModel/images/PercolationGraphL300p-0.5-0.6-0.7.png',
        '../BurningModel/images/PercolationPlotT10000L-100-50-10.png',
        '../SpanningCluster/images/HKVisualizationL30p-0.4-0.54-0.56-0.58-0.6-0.8_concat_two_col.png',
        '../SpanningCluster/images/HKVisualizationL200p-0.4-0.54-0.56-0.58-0.6-0.8_concat_two_col.png',
        '../SpanningCluster/images/AverageClusterGraphT10000L-10-50-100.png',
        '../SpanningCluster/images/TimeComparisonGraphT10000L50.png',
        '../SpanningCluster/images/TimeComparisonGraphT10000L100.png',
        '../SpanningCluster/images/ClusterSizeDistributionGraphT10000L10.png',
        '../SpanningCluster/images/ClusterSizeDistributionGraphT10000L50.png',
        '../SpanningCluster/images/ClusterSizeDistributionGraphT10000L100.png'
    ]
    with open('./Markdowns/HomePagePart1.md', 'r') as file:
        text_to_display = file.read()
    st.markdown(text_to_display, unsafe_allow_html=True)
    for image in image_list:
        st.image(image)


def probability_site_description():
    st.markdown('### <center>ProbabilitySite Object Description</center>', unsafe_allow_html=True)
    st.markdown('We begin with importing all necessary modules, '
                'and `ProbabilitySite` object, which contains the 2D grid')
    st.code('from ProbabilitySite import ProbabilitySite \n'
            'from matplotlib import pyplot as plt\n'
            'import numpy as np')
    st.markdown('The most important parameter to pass into the constructor is system size **L**. '
                'Additionally we can pass probability **p** of site occupation, '
                'but it is going to be changed many times during the simulation. '
                'To generate grid, it uses `numpy.random` module. '
                'Here is a line from `ProbabilitySite` responsible for this operation:')
    st.code('self.initial_grid = np.random.random((self.L, self.L))')
    st.markdown("Now we build the `ProbabilitySite` object and see its features.")
    st.code("L = 10\n"
            "probability_site = ProbabilitySite(L=L)\n"
            "figure, axes = plt.subplots(1, 1, layout='constrained')\n"
            "axes.set_title(f'Probability grid generated for $L = {L}$')\n"
            "probability_site.plot_grid_as_matrix(axes=axes)")
    st.pyplot(plot_probability_grid(numeric=True))
    st.markdown('Now we can pass site probability. Each site above $1 - p$ is going to be occupied, '
                'marked as $1$ and the rest of them will be $0$.')
    st.code("probability = 0.6\n"
            "probability_site.change_probability(probability)\n"
            "probability_site.grid_thresholding()\n"
            "figure2, axes2 = plt.subplots(1, 1, layout='constrained')\n"
            "axes2.set_title(f'Grid after thresholding')\n"
            "probability_site.plot_grid_as_matrix(matrix=probability_site.get_current_grid(), axes=axes2)")
    st.pyplot(plot_threshold_grid(p=0.6, numeric=True))
    st.markdown('Line responsible for grid thresholding is written below:')
    st.code("self.grid = np.where(self.initial_grid < 1 - self.p, 0, 1).astype(int)")
    st.markdown('We can see the grid visualizations for larger ***L***:')
    st.code("L = 50\n"
            "probability = 0.6\n"
            "probability_site = ProbabilitySite(L=L, p=probability)\n"
            "probability_site.grid_thresholding()\n"
            "figure3, axes3 = plt.subplots(2, 1, layout='constrained')\n" +
            r"figure3.suptitle(f'Visual representation of ${L}' + r'\times' + f'{L}$ grid\n$p = {probability}$')" +
            "\nprobability_site.plot_grid(initial=True, ax=axes3[0], title='before thresholding', cmap_name='bone')\n"
            "probability_site.plot_grid(initial=False, ax=axes3[1], title='after thresholding', cmap_name='bone')")
    st.pyplot(plot_grid_comparison_after_threshold(L=50, p=0.6, numeric=False))
    st.markdown('We can also see how the grid looks for different values of ***p***:')
    st.code("figure4, axes4 = plt.subplots(2, 2, layout='constrained')\n"
            "axes4 = axes4.ravel()\n"
            "probabilities = [0.2, 0.5, 0.8]\n"
            "figure4.suptitle(f'Grid after thresholding for various probabilities')\n"
            "probability_site.plot_grid(initial=True, ax=axes4[0], title='initial grid', cmap_name='bone')\n"
            "for index, probability in enumerate(probabilities):\n"
            "   probability_site.change_probability(probability)\n"
            "   probability_site.grid_thresholding()\n"
            "   probability_site.plot_grid(initial=False, ax=axes4[index + 1], title=f'$p = {probability}$')")
    st.pyplot(compare_probability_site_for_different_p(L=50))
    st.markdown('You can tweak with parameters interactively in section `1.2 Interaction`.')


def probability_site_interaction():
    st.markdown('### <center>ProbabilitySite Object Interaction</center>', unsafe_allow_html=True)
    st.markdown('In this section you can tweak with different parameters to see how it affects the 2D random grid.'
                'Plots are the same as the ones shown in section `1.1 Description`.')

    imshow_tab, numeric_tab, comparison_tab = st.tabs(['Image', 'Numeric', 'Comparison'])
    with imshow_tab:
        L_im = 50
        if 'initial_L_im_ps' not in st.session_state:
            st.session_state.initial_L_im_ps = L_im
        if 'initial_grid_im_ps' not in st.session_state:
            st.session_state.initial_grid_im_ps = generate_probability_grid(L=L_im)
        L_im = st.number_input('System size', min_value=10, max_value=500, value=L_im, step=10, key='size1_im')
        if st.session_state.initial_L_im_ps != L_im:
            st.session_state.initial_L_im_ps = L_im
            st.session_state.initial_grid_im_ps = generate_probability_grid(L=L_im)
        st.pyplot(plot_probability_grid(L=L_im, numeric=False))
    with numeric_tab:
        L_num = 10
        if 'initial_L_num_ps' not in st.session_state:
            st.session_state.initial_L_num_ps = L_num
        if 'initial_grid_num_ps' not in st.session_state:
            st.session_state.initial_grid_num_ps = generate_probability_grid(L=L_num)
        L_num = st.number_input('System size', min_value=2, max_value=14, value=10, step=2, key='size1_num')
        if st.session_state.initial_L_num_ps != L_num:
            st.session_state.initial_L_num_ps = L_num
            st.session_state.initial_grid_num_ps = generate_probability_grid(L=L_num)
        st.pyplot(plot_probability_grid(L=L_num, numeric=True))
    with comparison_tab:
        L_com_num = 10
        L_com_im = 50
        if 'initial_L_com_num_ps' not in st.session_state:
            st.session_state.initial_L_com_num_ps = L_com_num
        if 'initial_grid_com_num_ps' not in st.session_state:
            st.session_state.initial_grid_com_num_ps = generate_probability_grid(L=L_com_num)
        if 'initial_L_com_im_ps' not in st.session_state:
            st.session_state.initial_L_com_im_ps = L_com_im
        if 'initial_grid_com_im_ps' not in st.session_state:
            st.session_state.initial_grid_com_im_ps = generate_probability_grid(L=L_com_im)
        is_numeric = st.checkbox('Numeric', value=False, key='is_num1_ps')
        size_col_num, size_col_im, prob_col = st.columns(3)
        L_com_num = size_col_num.number_input('System size (numeric)', min_value=2, max_value=14,
                                              value=10, step=2, key='size1_num_com')
        L_com_im = size_col_im.number_input('System size (image)', min_value=10, max_value=500,
                                            value=L_im, step=10, key='size1_im_com')
        probability_com = prob_col.slider('Probability', min_value=0., max_value=1.,
                                          value=0.5, step=0.01, key='prob1_num_com')
        if st.session_state.initial_L_com_num_ps != L_com_num:
            st.session_state.initial_L_com_num_ps = L_com_num
            st.session_state.initial_grid_com_num_ps = generate_probability_grid(L=L_com_num)
        if st.session_state.initial_L_com_im_ps != L_com_im:
            st.session_state.initial_L_com_im_ps = L_com_im
            st.session_state.initial_grid_com_im_ps = generate_probability_grid(L=L_com_im)
        if is_numeric:
            st.pyplot(plot_grid_comparison_after_threshold(L=L_com_num,
                                                           p=probability_com,
                                                           initial_grid=st.session_state.initial_grid_com_num_ps,
                                                           vertical=True,
                                                           numeric=True))
        else:
            st.pyplot(plot_grid_comparison_after_threshold(L=L_com_im,
                                                           p=probability_com,
                                                           initial_grid=st.session_state.initial_grid_com_im_ps,
                                                           vertical=False,
                                                           numeric=False))
    st.markdown('To see whole `ProbabilitySite` object check section `1.3 Source Code`')


def probability_site_source_code():
    with open('../ProbabilitySite.py', 'r') as file:
        source_code = file.read()
    source_code = source_code.split('\n\n\n')
    imports = source_code[0].split('\n')
    imports.pop(1)
    source_code[0] = '\n'.join(imports)
    source_code = '\n\n\n'.join(source_code[0:2])
    st.code(source_code)


def burning_model_description():
    st.markdown('### <center>BurningModel Object Description</center>', unsafe_allow_html=True)
    st.markdown('In this section we take introduced before `ProbabilitySite` object '
                'and inherit from it to get the grid with occupied and unoccupied sites. '
                'We begin with importing all necessary modules.')
    st.code("from BurningModel import BurningModel\n"
            "from matplotlib import pyplot as plt\n"
            "import numpy as np")
    st.markdown("First we create the `BurningModel object. Let's see, "
                "how the whole percolation process affects our grid numerically:")
    st.code("L = 10\n"
            "p = 0.6\n"
            "burning_model = BurningModel(L=L, p=p)\n"
            "burning_model.burning_model()\n"
            "figure1, axes1 = plt.subplots(1, 1, layout='constrained')\n"
            "burning_model.plot_grid_as_matrix(matrix=burning_model.get_current_grid(), axes=axes1)\n"
            "axes1.set_title(f'Percolation for $L = {L}$ and $p = {p}$')")
    st.pyplot(burning_model_grid(L=10, p=0.6, numeric=True))
    st.markdown("We can see that after each step to occupy neighbours the number increases "
                "and it gets as far as it can. Thanks to that we can easilly extract the number of steps "
                "for percolation and if it reached the end of the grid. "
                "Let's see now how the grid looks after initialization, "
                "a couple of steps and at the end of the process.")
    st.code("L = 50\n"
            "p = 0.65\n"
            "figure2, axes2 = plt.subplots(1, 3, layout='constrained')\n"
            "burning_model = BurningModel(L=L, p=p)\n"
            "burning_model.grid_thresholding()\n\n"
            "# first graph\n"
            "burning_model.set_top_row_to_initial_value()\n"
            "burning_model.plot_percolation(ax=axes2[0])\n"
            "axes2[0].set_title(f'Initial phase\nTop row set on fire')\n\n"
            "# second graph\n"
            "number_of_steps = 30\n"
            "for _ in range(number_of_steps):\n"
            "   burning_model.another_burning_step()\n"
            "burning_model.plot_percolation(ax=axes2[1])\n"
            "axes2[1].set_title(f'Grid after {number_of_steps} steps')\n\n"
            "# third graph\n"
            "burning_model.burning_model(reset_grid=True, initial_grid=burning_model.get_initial_grid())\n"
            "burning_model.plot_percolation(ax=axes2[2])\n"
            "axes2[2].set_title(f'Grid after percolation')")
    st.pyplot(burning_model_three_stages(L=50, p=0.65, number_of_steps=30))
    st.markdown("Let's see some examples for different probabilities for larger ***L***")
    for L in [50, 100, 200]:
        st.pyplot(burning_model_compare_probability(L=L))
    st.markdown("By repeating the same process many times wee can estimate "
                "the percolation probability and plot it on a graph.")
    st.code("def plot_percolation_probability(L=10, t=15):\n"
            "   percolation_probability = 0.592\n"
            "   burning_model_mean = BurningModel(L=L)\n"
            "   probability_space = np.linspace(0.45, 0.8, 15)\n"
            "   percolation_space = np.zeros(len(probability_space))\n"
            "   for index, probability in enumerate(probability_space):\n"
            "       burning_model_mean.change_probability(probability)\n"
            "       burning_model_mean.t_percolation_trials(trials=t)\n"
            "       percolation_space[index] = burning_model_mean.get_percolation_probability()\n\n"
            "   figure, axes = plt.subplots(1, 1, layout='constrained')\n"
            "   axes.plot(probability_space, percolation_space, color='black')\n"
            "             axes.axvline(x=percolation_probability, \n"
            "             color='blue', \n"
            "             linestyle='--', \n"
            "             label=f'$p_c$ = {percolation_probability}')\n"
            "   axes.grid()\n"
            "   axes.legend(loc='upper left')\n"
            "   axes.set_title(f'Percolation probability based on {t} number of trials')\n"
            "   axes.set(xlabel='site probability', ylabel='percolation probability')")
    st.code("plot_percolation_probability(L=20, t=20)")
    st.pyplot(burning_model_percolation_plot(L=20, trials=200))
    st.markdown('Graph generated for larger parameters is located below. '
                'We can see that for larger ***L*** line gets steeper. '
                'Theoretically for $L = \infty$ it is a vertical line.')
    st.image('../BurningModel/images/PercolationPlotT10000L-100-50-10.png')
    st.markdown('For interactive plots check section `2.2 Interaction`.')


def burning_model_interaction():
    st.markdown('### <center>BurningModel Object Interaction</center>', unsafe_allow_html=True)
    st.markdown('In this section you see how percolation process works based on given probability. '
                'Plots are the same as the ones shown in section `2.1 Description`.')

    imshow_tab, numeric_tab, plot_tab = st.tabs(['Image', 'Numeric', 'Plot'])
    with imshow_tab:
        L_im = 50
        if 'initial_L_im_bm' not in st.session_state:
            st.session_state.initial_L_im_bm = L_im
        if 'initial_grid_im_bm' not in st.session_state:
            st.session_state.initial_grid_im_bm = generate_probability_grid(L=L_im)
        size_col_im, prob_col_im, step_col_im = st.columns(3)
        L_im = size_col_im.number_input('System size', min_value=10, max_value=500, value=L_im, step=10, key='size1_im')
        probability_im = prob_col_im.slider('Probability', min_value=0., max_value=1.,
                                            value=0.5, step=0.01, key='prob1_im_bm')
        step_im = step_col_im.slider('Step', min_value=2, max_value=600, value=2, step=1, key='step1_im')
        if st.session_state.initial_L_im_bm != L_im:
            st.session_state.initial_L_im_bm = L_im
            st.session_state.initial_grid_im_bm = generate_probability_grid(L=L_im)
        st.pyplot(burning_model_percolation_interaction(L=L_im,
                                                        p=probability_im,
                                                        step=step_im,
                                                        initial_grid=st.session_state.initial_grid_im_bm))
    with numeric_tab:
        L_num = 10
        if 'initial_L_num_bm' not in st.session_state:
            st.session_state.initial_L_num_bm = L_num
        if 'initial_grid_num_bm' not in st.session_state:
            st.session_state.initial_grid_num_bm = generate_probability_grid(L=L_num)
        size_col_num, prob_col_num, step_col_num = st.columns(3)
        L_num = size_col_num.number_input('System size', min_value=2, max_value=14,
                                          value=L_num, step=1, key='size1_num')
        probability_num = prob_col_num.slider('Probability', min_value=0., max_value=1.,
                                              value=0.5, step=0.01, key='prob1_num')
        step_num = step_col_num.slider('Step', min_value=2, max_value=80, value=2, step=1, key='step1_num')
        if st.session_state.initial_L_num_bm != L_num:
            st.session_state.initial_L_num_bm = L_num
            st.session_state.initial_grid_num_bm = generate_probability_grid(L=L_num)
        st.pyplot(burning_model_percolation_interaction(L=L_num,
                                                        p=probability_num,
                                                        step=step_num,
                                                        initial_grid=st.session_state.initial_grid_num_bm,
                                                        numeric=True))
    with plot_tab:
        size_col_plot, t_col_plot = st.columns(2)
        L_plot = size_col_plot.number_input('System size', min_value=2, max_value=100,
                                            value=L_num, step=2, key='size1_plot')
        t_plot = t_col_plot.slider('Number of trials', min_value=10, max_value=200,
                                   value=50, step=10, key='trials1_plot')
        st.markdown('Warning. Simulation takes some time for larger parameters.')
        st.pyplot(burning_model_percolation_plot(L=L_plot, trials=t_plot))


def burning_model_source_code():
    with open('../BurningModel/BurningModel.py', 'r') as file:
        source_code = file.read()
    source_code = source_code.split('\n\n\n')
    imports = source_code[0].split('\n')
    imports.pop(3)
    source_code[0] = '\n'.join(imports)
    source_code = '\n\n\n'.join(source_code[0:2])
    st.code(source_code)


def spanning_cluster_description():
    st.markdown('### <center>SpanningCluster Object Description</center>', unsafe_allow_html=True)
    st.markdown('In this section we take introduced before `ProbabilitySite` object '
                'and inherit from it to get the grid with occupied and unoccupied sites. '
                'We begin with importing all necessary modules.')
    st.code("from SpanningCluster import SpanningCluster\n"
            "from matplotlib import pyplot as plt\n"
            "import numpy as np")
    st.markdown('First of all, we can set labeling all squares with reverse updates or without them. '
                'The advantege of reverse updates is that it allows to make much better looking visualizations, '
                'but it slows down the simulation. Below we define both approaches.')
    st.code("L = 20\n"
            "p = 0.54\n"
            "spanning_cluster = SpanningCluster(L=L, p=p)\n"
            "initial_grid = spanning_cluster.get_initial_grid()\n"
            "spanning_cluster.hk_algorithm(reset_grid=True, update_clusters=False, initial_grid=initial_grid)\n"
            "cluster_1 = spanning_cluster.get_current_grid()\n"
            "spanning_cluster.hk_algorithm(reset_grid=True, update_clusters=True, initial_grid=initial_grid)\n"
            "cluster_2 = spanning_cluster.get_current_grid()")
    st.code("figure1, axes1 = plt.subplots(2, 1, layout='constrained')\n"
            "spanning_cluster.plot_grid_as_matrix(matrix=cluster_1, axes=axes1[0])\n" +
            r"axes1[0].set_title(f'$L = {L}$\nClustering without concatenating')" +
            "\nspanning_cluster.plot_grid_as_matrix(matrix=cluster_2, axes=axes1[1])\n"
            "axes1[1].set_title('Clustering with concatenating')")
    st.pyplot(spanning_cluster_concat_comparison_numeric(L=15, p=0.54))
    st.markdown("The main difference we can notice is that on the first graph we can see "
                "two distinct numbers next to each other, while on the second one that's not the case, "
                "because every adjacent cluster was relabelled.")
    st.markdown("Now let's see how we store calculated values after HK algorithm and compare it to the grid.")
    st.code("L = 10\n"
            "panning_cluster = SpanningCluster(L=L, p=p)\n"
            "spanning_cluster.hk_algorithm(reset_grid=True, update_clusters=False)\n"
            "for key, value in spanning_cluster.get_container().items():\n"
            "   print(f'{key}: {value}')\n"
            "figure2, axes2 = plt.subplots(1, 1, layout='constrained')\n"
            "spanning_cluster.plot_grid_as_matrix(matrix=spanning_cluster.get_current_grid(), axes=axes2)")
    st.code("spanning_cluster.convert_cluster_to_histogram()\n"
            "print(spanning_cluster.get_histogram(sort=True))")
    bin_column, plot_column = st.columns([1, 3])
    fig, container, histogram = spanning_cluster_clustering_plot(L=10,
                                                                 p=0.54,
                                                                 numeric=True,
                                                                 return_bins=True,
                                                                 update_clusters=False)
    with bin_column:
        st.write('Container:')
        st.write(container)
        st.write('Histogram:')
        st.write(histogram)
    with plot_column:
        fig.set_size_inches(4, 5)
        st.pyplot(fig)
    st.markdown("By checking values in the container we can deduce exactly which clusters where joined to another one. "
                "They are marked as $-k_i$. We can also convert acquired container into histogram.")
    st.markdown("And now let's see the histogram for a bigger grid:")
    large_histogram = spanning_cluster_generate_histogram(L=50, p=0.54)
    st.write(large_histogram)
    st.markdown("Now we can visualize what exactly happens after HK algorithm to 2D grid. "
                "Let's see first the difference between concatenated and not concatenated graphs.")
    st.code("spanning_cluster = SpanningCluster(L=30)\n"
            "initial_grid = spanning_cluster.get_initial_grid()\n"
            "probabilities = [0.5, 0.6, 0.7]")
    st.code("figure3, axes3 = plt.subplots(len(probabilities), 2, layout='constrained')\n"
            "for x, probability in enumerate(probabilities):\n"
            "   for y, bool_value in enumerate([False, True]):\n"
            "       spanning_cluster.change_probability(probability)\n"
            "       spanning_cluster.hk_algorithm(reset_grid=True, update_clusters=bool_value, "
            "initial_grid=initial_grid)\n"
            "       spanning_cluster.visualize_clusters(ax=axes3[x][y], add_title=False)\n" +
            r"figure3.suptitle(f'Visualized grid. Left side is not concatenated, right side is.\n'" + "\n" +
            r"                 f'Probabilities: {" + "','" + ".join(list(map(str, probabilities)))}')")
    L_1 = 50
    initial_grid = generate_probability_grid(L=L_1)
    fig1 = spanning_cluster_concat_comparison_image(L=L_1, p=0.5, initial_grid=initial_grid)
    fig1.suptitle(f'Visualized grid. Left side is not concatenated, right side is.\n'
                  f'Probabilities: {[0.5, 0.6, 0.7]}')
    st.pyplot(fig1)
    st.pyplot(spanning_cluster_concat_comparison_image(L=L_1, p=0.6, initial_grid=initial_grid))
    st.pyplot(spanning_cluster_concat_comparison_image(L=L_1, p=0.7, initial_grid=initial_grid))
    st.markdown("We can see that we have different colors next to each other in graphs on the left. "
                "This happens because they are labelled with different number "
                "and information about them being concatenated is hidden in the container. "
                "On the right side we have better visualizations with each cluster "
                "separated by a black color, but it takes additional computational time.")
    st.markdown("Below we can see how much of a difference concatenating clusters can make.")
    st.image('../SpanningCluster/images/TimeComparisonGraphT10000L100.png')
    st.markdown("Let's see how clustering looks for larger system size:")
    st.pyplot(visualize_clustered_grid(L=200, p=0.54, concatenated=True))
    st.markdown("Now based on many repetitions we can estimate the size of the biggest cluster for each probability, "
                "the same way as we calculated percolation probability in previous part of the project.")
    st.markdown(calculate_average_biggest_cluster(L=100, p=0.54, trials=100))
    st.markdown("Below we can see graphs for larger parameters:")
    st.image('../SpanningCluster/images/AverageClusterGraphT10000L-10-50-100.png')
    st.markdown("And last but not least we can create a histogram over many repetitions for given probability.")
    st.pyplot(spanning_cluster_average_cluster_size(L=50, p=0.7, trials=500))
    st.markdown("And below we can see a graph calculated for larger ***L*** and many trials.")
    st.image('../SpanningCluster/images/ClusterSizeDistributionGraphT10000L100.png')
    st.markdown("And some other generated graphics:")
    st.image('../SpanningCluster/images/HKVisualizationL500p-0.4-0.54-0.56-0.58-0.6-0.8_concat_two_col.png')
    st.image('../SpanningCluster/images/ClusterSizeDistributionGraphT10000L10.png')
    st.markdown('For interactive plots check section `3.2 Interaction`.')


def spanning_cluster_interaction():
    st.markdown('### <center>SpanningCluster Object Interaction</center>', unsafe_allow_html=True)
    st.markdown('In this section you see how site occupation probability affects clustering on the grid. '
                'Plots are the same as the ones shown in section `3.1 Description`.')
    st.markdown("Grid stays the same until ***L*** is changed but colors for clusters "
                "are chosen randomly while rendering. That's why graphs appear to be different. "
                "Cluster's shape stays the same.")
    imshow_tab, numeric_tab, plot_tab, histogram_tab = st.tabs(['Image', 'Numeric', 'Plot', 'Histogram'])
    with imshow_tab:
        L_im = 50
        if 'initial_L_im_sp' not in st.session_state:
            st.session_state.initial_L_im_sp = L_im
        if 'initial_grid_im_sp' not in st.session_state:
            st.session_state.initial_grid_im_sp = generate_probability_grid(L=L_im)
        is_concat_im = st.checkbox('Sites relabelled', value=True, key='concat1_im')
        size_col_im, prob_col_im = st.columns(2)
        L_im = size_col_im.number_input('System size', min_value=10, max_value=500, value=L_im, step=10, key='size1_im')
        probability_im = prob_col_im.slider('Probability', min_value=0., max_value=1.,
                                            value=0.5, step=0.01, key='prob1_im')
        if st.session_state.initial_L_im_sp != L_im:
            st.session_state.initial_L_im_sp = L_im
            st.session_state.initial_grid_im_sp = generate_probability_grid(L=L_im)
        st.pyplot(visualize_clustered_grid(L=L_im,
                                           p=probability_im,
                                           concatenated=is_concat_im,
                                           initial_grid=st.session_state.initial_grid_im_sp))
    with numeric_tab:
        L_num = 10
        if 'initial_L_num_sp' not in st.session_state:
            st.session_state.initial_L_num_sp = L_num
        if 'initial_grid_num_sp' not in st.session_state:
            st.session_state.initial_grid_num_sp = generate_probability_grid(L=L_num)
        is_concat_num = st.checkbox('Sites relabelled', value=True, key='concat1_num')
        size_col_num, prob_col_num = st.columns(2)
        L_num = size_col_num.number_input('System size', min_value=2, max_value=14,
                                          value=L_num, step=1, key='size1_num')
        probability_num = prob_col_num.slider('Probability', min_value=0., max_value=1.,
                                              value=0.5, step=0.01, key='prob1_num')
        if st.session_state.initial_L_num_sp != L_num:
            st.session_state.initial_L_num_sp = L_num
            st.session_state.initial_grid_num_sp = generate_probability_grid(L=L_num)
        st.pyplot(visualize_clustered_grid(L=L_num,
                                           p=probability_num,
                                           concatenated=is_concat_num,
                                           initial_grid=st.session_state.initial_grid_num_sp,
                                           numeric=True))
    with plot_tab:
        size_col_plot, t_col_plot = st.columns(2)
        L_plot = size_col_plot.number_input('System size', min_value=2, max_value=100,
                                            value=L_num, step=2, key='size1_plot')
        t_plot = t_col_plot.slider('Number of trials', min_value=10, max_value=200,
                                   value=50, step=10, key='trials1_plot')
        st.pyplot(spanning_cluster_biggest_cluster_plot(L=L_plot, trials=t_plot))
        st.markdown('Warning. Simulation takes some time for larger parameters.')
    with histogram_tab:
        size_col_hist, prob_col_hist, t_col_hist = st.columns(3)
        L_hist = size_col_hist.number_input('System size', min_value=2, max_value=100,
                                            value=L_num, step=2, key='size1_hist')
        probability_hist = prob_col_hist.slider('Probability', min_value=0., max_value=1.,
                                                value=0.5, step=0.01, key='prob1_hist')
        t_hist = t_col_hist.slider('Number of trials', min_value=10, max_value=200,
                                   value=50, step=10, key='trials1_hist')
        st.pyplot(spanning_cluster_average_cluster_size(L=L_hist, p=probability_hist, trials=t_hist))
        st.markdown('Warning. Simulation takes some time for larger parameters.')


def spanning_cluster_source_code():
    with open('../SpanningCluster/SpanningCluster.py', 'r') as file:
        source_code = file.read()
    source_code = source_code.split('\n\n\n')
    imports = source_code[0].split('\n')
    imports.pop(3)
    source_code[0] = '\n'.join(imports)
    source_code = '\n\n\n'.join(source_code[0:2])
    st.code(source_code)

