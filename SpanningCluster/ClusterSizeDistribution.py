from SpanningCluster import SpanningCluster
from time import time
from CommonFunctions import (make_directories, check_if_file_has_data,
                             ask_to_replace_file, save_json_file)


def get_file_name(L, t, normalized=False):
    name = f'Dist_L{L}T{t}'
    name += '_normalized' if normalized else ''
    return name + '.json'


if __name__ == '__main__':
    L_list = [10, 50, 100]
    t = 10000
    percolation_p = 0.592
    probability_for_histogram = [0.2, 0.3, 0.3, 0.5, percolation_p, 0.6, 0.7, 0.8]
    cluster_histogram_dict = {}
    normalize = False

    results_path = 'results'
    make_directories([results_path])

    perform_simulation = []
    for L in L_list:
        file_name = get_file_name(L, t, normalized=normalize)
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
            for index, probability in enumerate(probability_for_histogram):
                start_time_sim = time()
                spanning_cluster.change_probability(probability)
                spanning_cluster.t_histogram_trials(trials=t,
                                                    reset_histogram=False,
                                                    normalize_histogram=normalize)
                stop_time_sim = time()
                time_delta = round(stop_time_sim - start_time_sim, 3)
                cluster_histogram_dict[probability] = {'hist': spanning_cluster.get_histogram(),
                                                       'time': time_delta}
                print(f'Generated histogram for site probability {probability}, '
                      f'time taken: {time_delta} seconds')
                spanning_cluster.reset_histogram()
            save_json_file(cluster_histogram_dict,
                           get_file_name(L, t, normalized=normalize),
                           sub_dir=results_path)

    stop_time = time()
    print(f'Program took {round(stop_time - start_time, 3)} seconds')

