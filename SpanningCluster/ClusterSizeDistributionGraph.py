from matplotlib import pyplot as plt
import numpy as np
import os
import sys
from CommonFunctions import make_directories, check_if_file_exists, read_json_file
from ClusterSizeDistribution import get_file_name


if __name__ == '__main__':
    L = 100
    t = 1000
    percolation_p = 0.592
    normalize = False

    results_path = 'results'
    image_path = 'images'

    json_data = {}
    file_name = get_file_name(L, t, normalized=normalize)
    try:
        json_data = read_json_file(file_name, sub_dir=results_path)
    except FileNotFoundError:
        print(f'File {file_name} does not exist!')
        sys.exit()

    colors = ['red', 'darkgreen', 'blue', 'purple', 'orange']
    figure, axes = plt.subplots(3, 1, layout='constrained')
    first_graph_index = 0
    third_graph_index = 0
    for probability, data in json_data.items():
        simulation_time = data['time']
        histogram = data['hist']
        cluster_size_space = np.array(list(map(int, histogram.keys())))
        cluster_number_space = np.array(list(histogram.values()))
        if float(probability) < percolation_p:
            axes[0].scatter(cluster_size_space, cluster_number_space,
                            label=f'p = {probability}, time = {simulation_time} s',
                            color=colors[first_graph_index],
                            alpha=0.6)
            first_graph_index += 1
        elif float(probability) > percolation_p:
            axes[2].scatter(cluster_size_space, cluster_number_space,
                            label=f'p = {probability}, time = {simulation_time} s',
                            color=colors[third_graph_index],
                            alpha=0.2,
                            s=10)
            third_graph_index += 1
        else:
            axes[1].scatter(cluster_size_space, cluster_number_space,
                            label=f'p = {probability}, time = {simulation_time} s',
                            color='black',
                            alpha=0.35,
                            s=20)

    if L >= 50:
        axes[2].set(xlim=[0, 500])

    axes[0].set_title(f'Cluster size distribution, L = {L}, T = {t}'
                      f'{", normalized" if normalize else ""}\n$p < p_c$')
    axes[0].set(xlabel='cluster size', ylabel='number of occurrences', yscale='log')
    axes[1].set_title(f'$p = p_c$')
    axes[1].set(xlabel='cluster size', ylabel='number of occurrences', yscale='log', xscale='log')
    axes[2].set_title(f'$p > p_c$')
    axes[2].set(xlabel='cluster size', ylabel='number of occurrences', yscale='log')
    for index in range(3):
        axes[index].grid()
        axes[index].legend(loc='upper right')
    figure.set_size_inches(5, 10)

    make_directories([image_path])
    image_name = (f'ClusterSizeDistributionGraphT{t}L{L}'
                  f'{"_normalized" if normalize else ""}.png')

    path = os.path.join(image_path, image_name)
    if not check_if_file_exists(path):
        figure.savefig(path)
    plt.show()





