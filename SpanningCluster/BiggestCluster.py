from SpanningCluster import SpanningCluster
from time import time
import pandas as pd
import numpy as np
import os
from CommonFunctions import (create_probability_space, make_directories,
                             check_if_file_has_data, ask_to_replace_file)


def create_file_name(L, t, concatenate=False):
    name = f'Dist_L{L}T{t}'
    name += '_concatenated' if concatenate else ''
    return name + '.csv'


if __name__ == '__main__':
    t = 1000
    L_list = [10, 50, 100]
    percolation_p = 0.592746
    probability_space = create_probability_space(percolation_p)
    number_of_simulations = len(probability_space)
    cluster_p_space = np.zeros(number_of_simulations)
    cluster_time = np.zeros(number_of_simulations)
    concatenate_clusters = True

    results_path = 'results'
    make_directories([results_path])

    perform_simulation = []
    for L in L_list:
        file_name = create_file_name(L, t, concatenate=concatenate_clusters)
        is_simulation_done = check_if_file_has_data(file_name, sub_dir=results_path)
        ask_to_redo_simulation = False
        if is_simulation_done:
            ask_to_redo_simulation = ask_to_replace_file(file_name)
        if is_simulation_done is False or ask_to_redo_simulation:
            perform_simulation.append(True)
        else:
            perform_simulation.append(False)

    start_time = time()
    for L_index, L in enumerate(L_list):
        if perform_simulation[L_index]:
            spanning_cluster = SpanningCluster(L=L)
            print(f'{f" L = {L} ":-^50}')
            for index, probability in enumerate(probability_space):
                start_time_sim = time()
                spanning_cluster.change_probability(probability)
                spanning_cluster.t_spanning_cluster_trials(trials=t, update_clusters=concatenate_clusters)
                average_cluster = spanning_cluster.get_average_biggest_cluster()
                cluster_p_space[index] = average_cluster
                stop_time_sim = time()
                time_delta = round(stop_time_sim - start_time_sim, 3)
                cluster_time[index] = time_delta
                print(f'Average cluster: {average_cluster}, '
                      f'site probability: {round(probability, 4)}, '
                      f'time taken: {time_delta} seconds')
            file_title = os.path.join(results_path, create_file_name(L, t, concatenate=concatenate_clusters))
            data_to_save = pd.DataFrame()
            data_to_save['site_prob'] = probability_space.tolist()
            data_to_save['clus_size'] = cluster_p_space.tolist()
            data_to_save['clus_time'] = cluster_time.tolist()
            data_to_save.to_csv(file_title, sep=',', index=False)

    stop_time = time()
    print(f'Program took {round(stop_time - start_time, 3)} seconds')

