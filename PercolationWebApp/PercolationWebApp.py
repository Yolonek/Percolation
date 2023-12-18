import streamlit as st
from Views import home_page


def probability_site_window():
    st.empty()
    st.title('Probability Site')


contents_str = 'Contents'
home_page_str = 'Home Page'

probability_site_1 = '1. Probability Site'
probability_site_1_1 = '1.1 Description'
probability_site_1_2 = '1.2 Source Code'

burning_model_2 = '2. Burning Model'
burning_model_2_1 = '2.1 Description'
burning_model_2_2 = '2.2 Source Code'

spanning_cluster_3 = '3. Spanning Cluster'
spanning_cluster_3_1 = '3.1 Description'
spanning_cluster_3_2 = '3.2 Source Code'

button_list = [home_page_str,
               probability_site_1_1, probability_site_1_2,
               burning_model_2_1, burning_model_2_2,
               spanning_cluster_3_1, spanning_cluster_3_2]

for button in button_list:
    st.session_state[button] = False

with st.sidebar:
    st.title(contents_str)
    if st.button(home_page_str):
        st.session_state[home_page_str] = True
    with st.expander(probability_site_1):
        for button in [probability_site_1_1, probability_site_1_2]:
            if st.button(button):
                st.session_state[button] = True
    with st.expander(burning_model_2):
        for button in [burning_model_2_1, burning_model_2_2]:
            if st.button(button):
                st.session_state[button] = True
    with st.expander(spanning_cluster_3):
        for button in [spanning_cluster_3_1, spanning_cluster_3_2]:
            if st.button(button):
                st.session_state[button] = True


some_button_clicked = False
for button in button_list:
    if st.session_state[button]:
        st.empty()
        st.write(f'this is {button}')
        some_button_clicked = True
if some_button_clicked is False:
    home_page()


