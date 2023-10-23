from BurningModel import BurningModel
from time import time
import pandas as pd
from CommonFunctions import *


if __name__ == '__main__':
    t = 100
    L_list = [100, 50, 10]
    percolation_p = 0.592746
    probability_space = create_probability_space(percolation_p)
    number_of_simulations = len(probability_space)
    percolation_p_space = np.zeros(number_of_simulations)
    percolation_time = np.zeros(number_of_simulations)

    results_path = 'results'
    make_directories([results_path])

    perform_simulation = []
    for L in L_list:
        file_name = f'Average_L{L}T{t}.csv'
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
            burning_model = BurningModel(L=L)
            print(f'{f" L = {L} ":-^50}')
            for index, probability in enumerate(probability_space):
                start_time_sim = time()
                burning_model.change_probability(probability)
                burning_model.t_percolation_trials(trials=t)
                percolation_probability = burning_model.get_percolation_probability()
                percolation_p_space[index] = percolation_probability
                stop_time_sim = time()
                time_delta = round(stop_time_sim - start_time_sim, 3)
                percolation_time[index] = time_delta
                print(f'Percolation probability: {percolation_probability}, '
                      f'site probability: {probability}, time taken: {time_delta}')
            file_title = os.path.join(results_path, f'Average_L{L}T{t}.csv')
            data_to_save = pd.DataFrame()
            data_to_save['site_prob'] = probability_space.tolist()
            data_to_save['perc_prob'] = percolation_p_space.tolist()
            data_to_save['perc_time'] = percolation_time.tolist()
            data_to_save.to_csv(file_title, sep=',', index=False)

    stop_time = time()
    print(f'Program took {round(stop_time - start_time, 3)} seconds')

    start_time = time()



