from Views import *


def switch_site(site_name):
    if site_name == home_page_str:
        home_page()
    elif site_name == probability_site_1_1:
        probability_site_description()
    elif site_name == probability_site_1_2:
        probability_site_interaction()
    elif site_name == probability_site_1_3:
        probability_site_source_code()
    elif site_name == burning_model_2_1:
        burning_model_description()
    elif site_name == burning_model_2_2:
        pass
    elif site_name == burning_model_2_3:
        burning_model_source_code()
    elif site_name == spanning_cluster_3_1:
        pass
    elif site_name == spanning_cluster_3_2:
        pass
    elif site_name == spanning_cluster_3_3:
        spanning_cluster_source_code()


contents_str = 'Contents'
home_page_str = 'Home Page'

probability_site_1 = '1. Probability Site'
probability_site_1_1 = '1.1 Description'
probability_site_1_2 = '1.2 Interaction'
probability_site_1_3 = '1.3 Source Code'

burning_model_2 = '2. Burning Model'
burning_model_2_1 = '2.1 Description'
burning_model_2_2 = '2.2 Interaction'
burning_model_2_3 = '2.3 Source Code'

spanning_cluster_3 = '3. Spanning Cluster'
spanning_cluster_3_1 = '3.1 Description'
spanning_cluster_3_2 = '3.2 Interaction'
spanning_cluster_3_3 = '3.3 Source Code'

button_list = [home_page_str,
               probability_site_1_1, probability_site_1_2, probability_site_1_3,
               burning_model_2_1, burning_model_2_2, burning_model_2_3,
               spanning_cluster_3_1, spanning_cluster_3_2, spanning_cluster_3_3]

for button in button_list:
    st.session_state[button] = False

with st.sidebar:
    st.title(contents_str)
    if st.button(home_page_str):
        st.session_state[home_page_str] = True
    with st.expander(probability_site_1):
        for button in button_list[1:4]:
            if st.button(button):
                st.session_state[button] = True
    with st.expander(burning_model_2):
        for button in button_list[4:7]:
            if st.button(button):
                st.session_state[button] = True
    with st.expander(spanning_cluster_3):
        for button in button_list[7:]:
            if st.button(button):
                st.session_state[button] = True


some_button_clicked = False
for button in button_list:
    if st.session_state[button]:
        switch_site(button)
        some_button_clicked = True
if some_button_clicked is False:
    # home_page()
    switch_site(burning_model_2_1)


