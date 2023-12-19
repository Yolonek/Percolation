import streamlit as st
from Backend import *

IMAGE_LIST = [
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


def home_page():
    with open('./Markdowns/HomePagePart1.md', 'r') as file:
        text_to_display = file.read()
    st.empty()
    st.markdown(text_to_display, unsafe_allow_html=True)
    for image in IMAGE_LIST:
        st.image(image)


def probability_site_description():
    st.markdown('### <center>ProbabilitySite Object Description</center>', unsafe_allow_html=True)
    st.markdown('We begin with importing all necessary modules, '
                'and `ProbabilitySite` object, which contains the 2D grid')
    st.code('from ProbabilitySite import ProbabilitySite \n'
            'from matplotlib import pyplot as plt')
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
    st.pyplot(plot_numeric_probability_grid())
    st.markdown('Now we can pass site probability. Each site above $1 - p$ is going to be occupied, '
                'marked as $1$ and the rest of them will be $0$.')
    st.code("probability = 0.6\n"
            "probability_site.change_probability(probability)\n"
            "probability_site.grid_thresholding()\n"
            "figure2, axes2 = plt.subplots(1, 1, layout='constrained')\n"
            "axes2.set_title(f'Grid after thresholding')\n"
            "probability_site.plot_grid_as_matrix(matrix=probability_site.get_current_grid(), axes=axes2)")
    st.pyplot(plot_threshold_grid(p=0.6))
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
    st.pyplot(plot_grid_comparison_after_threshold(L=50, p=0.6))
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
    st.markdown('You can tweak with parameters interactively in section `1.2`.')

