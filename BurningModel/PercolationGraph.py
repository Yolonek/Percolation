from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import os
from CommonFunctions import make_directories, check_if_file_exists


if __name__ == '__main__':
    L_list = [100, 50, 10]
    t = 10000
    percolation_p = 0.592

    results_path = 'results'
    images_path = 'images'

    dataframe_list = []

    for L in L_list:
        file_name = f'Average_L{L}T{t}.csv'
        file_path = os.path.join(results_path, file_name)
        try:
            percolation_dataframe = pd.read_csv(file_path, sep=',')
            dataframe_list.append(percolation_dataframe)
        except FileNotFoundError:
            print(f'File {file_name} does not exist!')

    colors = ['red', 'darkgreen', 'blue']
    figure, axes = plt.subplots(2, 1, layout='constrained')
    for index, (dataframe, L) in enumerate(zip(dataframe_list, L_list)):
        axes[0].plot(dataframe['site_prob'], dataframe['perc_prob'],
                     label=f'L = {L}', color=colors[index])
        total_time = int(np.sum(dataframe['perc_time']))
        axes[1].plot(dataframe['site_prob'], dataframe['perc_time'],
                     label=f'L = {L}, time = {total_time} s', color=colors[index])
    for index in range(2):
        axes[index].axvline(x=percolation_p, color='black', linestyle='--', label=f'$p_c$ = {percolation_p}')
        axes[index].legend(loc='upper left')
        axes[index].grid()
    axes[0].set(xlabel='site probability', ylabel='percolation probability')
    axes[1].set(xlabel='site probability', ylabel='time [s]', yscale='log')
    axes[0].set_title('Percolation probability dependence for each site probability')
    axes[1].set_title(f'Time taken for each probability. Each value calculated for mean t = {t}')
    figure.set_size_inches(8, 10)

    make_directories([images_path])
    image_name = f'PercolationPlotT{t}L'
    for L in L_list:
        image_name += f'-{L}'
    image_name += '.png'

    path = os.path.join(images_path, image_name)
    if not check_if_file_exists(path):
        figure.savefig(path)
    plt.show()
