from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import os
from CommonFunctions import make_directories, check_if_file_exists
from BiggestCluster import create_file_name


if __name__ == '__main__':
    L = 100
    t = 500

    results_path = 'results'
    image_path = 'images'

    dataframes = {}
    for concat in [False, True]:
        file_name = create_file_name(L, t, concatenate=concat)
        file_path = os.path.join(results_path, file_name)
        try:
            dataframes[concat] = pd.read_csv(file_path, sep=',')
        except FileNotFoundError:
            print(f'File {file_name} does not exist!')

    colors = ['darkgreen', 'blue']
    figure, axes = plt.subplots(1, 1, layout='constrained')
    for index, (concat, dataframe) in enumerate(dataframes.items()):
        total_time = round(dataframe['clus_time'].sum())
        if concat:
            label = f'clusters concatenated, time = {total_time} s'
        else:
            label = f'clusters not concatenated, time = {total_time} s'
        axes.plot(dataframe['site_prob'], dataframe['clus_time'],
                  color=colors[index], label=label)

    speed_up = round((dataframes[True]['clus_time'].sum() / dataframes[False]['clus_time'].sum()) * 100) - 100

    axes.set_title(f'Difference between concatenated and not concatenated clusters for HK algorithm\n'
                   f'Speed up: {speed_up} %, $L = {L}$, $trials = {t}$')
    axes.set(xlabel='site probability', ylabel='simulation time')
    axes.grid()
    axes.legend(loc='lower right')
    figure.set_size_inches(10, 8)

    make_directories([image_path])
    image_name = f'TimeComparisonGraphT{t}L{L}.png'

    path = os.path.join(image_path, image_name)
    if not check_if_file_exists(path):
        figure.savefig(path)
    plt.show()

