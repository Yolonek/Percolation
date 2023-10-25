from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import os
from CommonFunctions import make_directories, check_if_file_exists


if __name__ == '__main__':
    L_list = [10, 50, 100]
    t = 500
    percolation_p = 0.592

    results_path = 'results'
    image_path = 'images'

    dataframe_list = []

    for L in L_list:
        file_name = f'Dist_L{L}T{t}.csv'
        file_path = os.path.join(results_path, file_name)
        try:
            cluster_dataframe = pd.read_csv(file_path, sep=',')
            dataframe_list.append(cluster_dataframe)
        except FileNotFoundError:
            print(f'File {file_name} does not exist!')

    colors = ['red', 'darkgreen', 'blue']
    figure, axes = plt.subplots(int(len(L_list) / 2) + 1, 2, layout='constrained')
    axes = axes.ravel()
    for index, (dataframe, L) in enumerate(zip(dataframe_list, L_list)):
        total_time = round(np.sum(dataframe['clus_time']))
        axes[index].plot(dataframe['site_prob'], dataframe['clus_size'],
                         label=f'L = {L}, time = {total_time} s', color=colors[index])
        axes[index].axvline(x=percolation_p, color='black',
                            linestyle='--', label=f'$p_c$ = {percolation_p}')
        axes[index].set(xlabel='site probability', ylabel='cluster size')
        axes[index].legend(loc='upper left')
        axes[index].grid()
        axes[3].plot(dataframe['site_prob'], dataframe['clus_time'],
                     label=f'L = {L}, time = {total_time} s', color=colors[index])
    axes[3].axvline(x=percolation_p, color='black',
                    linestyle='--', label=f'$p_c$ = {percolation_p}')
    axes[3].legend(loc='upper left')
    axes[3].grid()
    axes[3].set(xlabel='site probability', ylabel='time [s]')
    figure.suptitle(f'Average cluster size for t = {t} with simulation time')
    figure.set_size_inches(10, 8)

    make_directories([image_path])
    image_name = f'AverageClusterGraphT{t}L'
    for L in L_list:
        image_name += f'-{L}'
    image_name += '.png'

    path = os.path.join(image_path, image_name)
    if not check_if_file_exists(path):
        figure.savefig(path)
    plt.show()
