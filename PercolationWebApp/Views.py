import streamlit as st

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


# def probability_site_description():

