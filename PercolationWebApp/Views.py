import streamlit as st
from Backend import *
import pandas as pd


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

    numeric_tab, imshow_tab = st.tabs(['Numeric', 'Image'])
    with numeric_tab:
        if 'figure_1' not in st.session_state:
            st.session_state.figure_1 = None
        if 'initial_L_1' not in st.session_state:
            st.session_state.initial_L_1 = None
        L_1_num = numeric_tab.number_input('System size', min_value=2, max_value=14, value=10, step=2, key='size1_num')
        if st.session_state.initial_L_1 != L_1_num:
            st.session_state.initial_L_1 = L_1_num
            st.session_state.figure_1 = plot_probability_grid(L=L_1_num, numeric=True)
        st.pyplot(st.session_state.figure_1)

        prob_col_num, l_col_num = st.columns(2)
        probability_num = prob_col_num.slider('Probability', min_value=0., max_value=1.,
                                              value=0.5, step=0.01, key='prob1_num')

        L_num = 10
        if 'initial_L_2' not in st.session_state:
            st.session_state.initial_L_2 = L_num
        if 'initial_grid_2' not in st.session_state:
            st.session_state.initial_grid_2 = generate_probability_grid(L=L_num, p=probability_num)
        L_num = l_col_num.number_input('System size', min_value=2, max_value=20, value=L_num, key='size2_num')
        if st.session_state.initial_L_2 != L_num:
            st.session_state.initial_L_2 = L_num
            st.session_state.initial_grid_2 = generate_probability_grid(L=L_num, p=probability_num)
        st.pyplot(plot_grid_comparison_after_threshold(L=st.session_state.initial_L_2,
                                                       p=probability_num,
                                                       initial_grid=st.session_state.initial_grid_2,
                                                       numeric=True,
                                                       vertical=True))

    with imshow_tab:
        if 'figure_3' not in st.session_state:
            st.session_state.figure_3 = None
        if 'initial_L_3' not in st.session_state:
            st.session_state.initial_L_3 = None
        L_1_im = imshow_tab.number_input('System size', min_value=10, max_value=500, value=50, step=10, key='size1_im')
        if st.session_state.initial_L_3 != L_1_im:
            st.session_state.initial_L_3 = L_1_im
            st.session_state.figure_3 = plot_probability_grid(L=L_1_im, numeric=False)
        st.pyplot(st.session_state.figure_3)

        prob_col_im, l_col_im = st.columns(2)
        probability_im = prob_col_im.slider('Probability', min_value=0., max_value=1.,
                                            value=0.5, step=0.01, key='prob1_im')

        L_im = 50
        if 'initial_L_4' not in st.session_state:
            st.session_state.initial_L_4 = L_im
        if 'initial_grid_4' not in st.session_state:
            st.session_state.initial_grid_4 = generate_probability_grid(L=L_im, p=probability_im)
        L_im = l_col_im.number_input('System size', min_value=10, max_value=500, value=50, step=10, key='size2_im')
        if st.session_state.initial_L_4 != L_im:
            st.session_state.initial_L_4 = L_im
            st.session_state.initial_grid_4 = generate_probability_grid(L=L_im, p=probability_im)
        st.pyplot(plot_grid_comparison_after_threshold(L=st.session_state.initial_L_4,
                                                       p=probability_im,
                                                       initial_grid=st.session_state.initial_grid_4,
                                                       numeric=False,
                                                       vertical=False))
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




def burning_model_source_code():
    with open('../BurningModel/BurningModel.py', 'r') as file:
        source_code = file.read()
    source_code = source_code.split('\n\n\n')
    imports = source_code[0].split('\n')
    imports.pop(3)
    source_code[0] = '\n'.join(imports)
    source_code = '\n\n\n'.join(source_code[0:2])
    st.code(source_code)


def spanning_cluster_source_code():
    with open('../SpanningCluster/SpanningCluster.py', 'r') as file:
        source_code = file.read()
    source_code = source_code.split('\n\n\n')
    imports = source_code[0].split('\n')
    imports.pop(3)
    source_code[0] = '\n'.join(imports)
    source_code = '\n\n\n'.join(source_code[0:2])
    st.code(source_code)

