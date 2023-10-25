from ProbabilitySite import ProbabilitySite
from matplotlib import pyplot as plt
import numpy as np
from CommonFunctions import make_directories, check_if_file_exists
import os
from time import time


class SpanningCluster(ProbabilitySite):

    def __init__(self, L=100, p=0.5):
        super().__init__(L=L, p=p)
        self.k = 2
        self.Mk = {f'Mk{self.k}': f'{1}'}
        self.top_value = 0
        self.left_value = 0
        self.occupied_sites = None
        self.mc_steps = 0
        self.cluster_size_histogram = {}
        self.number_of_trials = 1
        self.trials_array = None
        self.clusters_concatenated = False

    def reset_simulation_params(self, initial_grid=None, reset_histogram=True):
        self.k = 2
        self.Mk = {f'Mk{self.k}': f'{1}'}
        self.set_initial_grid(initial_grid=initial_grid)
        self.top_value = 0
        self.left_value = 0
        self.mc_steps = 0
        if reset_histogram:
            self.reset_histogram()
        self.clusters_concatenated = False

    def reset_histogram(self):
        self.cluster_size_histogram = {}

    def set_top_left_site(self):
        initial_value_assigned = False
        for row, x in zip(self.grid, range(self.L)):
            for grid_value, y in zip(row, range(self.L)):
                if grid_value == 1:
                    self.grid[x][y] = 2
                    initial_value_assigned = True
                    break
            if initial_value_assigned:
                break

    def find_occupied_sites(self):
        self.occupied_sites = np.where(self.grid == 1)

    def check_top_value(self, x_pos, y_pos):
        if x_pos == 0:
            return 0
        else:
            return self.grid[x_pos - 1][y_pos]

    def check_left_value(self, x_pos, y_pos):
        if y_pos == 0:
            return 0
        else:
            return self.grid[x_pos][y_pos - 1]

    def cluster_size(self, cluster_number):
        if '-k' in self.Mk[f'Mk{cluster_number}']:
            return 0
        else:
            return int(self.Mk[f'Mk{cluster_number}'])

    def set_cluster_size(self, cluster_number, cluster_size, negative=False):
        self.Mk[f'Mk{cluster_number}'] = f'-k{cluster_size}' if negative else f'{cluster_size}'

    def increment_existing_cluster(self, x_pos, y_pos, k_value):
        self.grid[x_pos][y_pos] = k_value
        mk_value = self.cluster_size(k_value) + 1
        self.set_cluster_size(k_value, mk_value)

    def concatenate_clusters(self, bigger_k, smaller_k, update_clusters=False):
        bigger_mk = self.cluster_size(bigger_k)
        smaller_mk = self.cluster_size(smaller_k)
        cluster_sum = bigger_mk + smaller_mk + 1
        self.set_cluster_size(bigger_k, cluster_sum)
        self.set_cluster_size(smaller_k, bigger_k, negative=True)
        if update_clusters:
            self.clusters_concatenated = True
            self.grid[np.where(self.grid == smaller_k)] = bigger_k

    def hk_algorithm_step(self, x_pos, y_pos, update_clusters=False):
        self.top_value = self.check_top_value(x_pos, y_pos)
        self.left_value = self.check_left_value(x_pos, y_pos)
        self.mc_steps += 1
        if self.top_value == 0 and self.left_value == 0:
            self.k += 1
            self.grid[x_pos][y_pos] = self.k
            self.set_cluster_size(self.k, 1)
        elif self.top_value == self.left_value:
            self.increment_existing_cluster(x_pos, y_pos, self.top_value)
        elif self.top_value == 0 and self.left_value != 0:
            self.increment_existing_cluster(x_pos, y_pos, self.left_value)
        elif self.top_value != 0 and self.left_value == 0:
            self.increment_existing_cluster(x_pos, y_pos, self.top_value)
        elif self.top_value != self.left_value:
            if self.cluster_size(self.top_value) > self.cluster_size(self.left_value):
                self.grid[x_pos][y_pos] = self.top_value
                self.concatenate_clusters(self.top_value, self.left_value, update_clusters=update_clusters)
            else:
                self.grid[x_pos][y_pos] = self.left_value
                self.concatenate_clusters(self.left_value, self.top_value, update_clusters=update_clusters)

    def hk_algorithm(self, reset_grid=False, update_clusters=False, initial_grid=None, reset_histogram=True):
        if reset_grid:
            self.set_initial_grid(initial_grid=initial_grid)
            self.grid_thresholding()
            self.set_top_left_site()
            self.reset_simulation_params(reset_histogram=reset_histogram)
        self.find_occupied_sites()
        x_values = self.occupied_sites[0]
        y_values = self.occupied_sites[1]
        for x, y in zip(x_values, y_values):
            self.hk_algorithm_step(x, y, update_clusters=update_clusters)

    def find_biggest_cluster(self):
        biggest_cluster = 0
        for size in self.Mk.values():
            if '-' not in size:
                size = int(size)
                if size > biggest_cluster:
                    biggest_cluster = size
        return biggest_cluster

    def convert_cluster_to_histogram(self):
        for size in self.Mk.values():
            if '-' not in size:
                if size in self.cluster_size_histogram:
                    self.cluster_size_histogram[size] += 1
                else:
                    self.cluster_size_histogram[size] = 1

    def t_spanning_cluster_trials(self, trials=1, update_clusters=False):
        self.number_of_trials = trials
        self.trials_array = np.zeros(trials)
        for trial in range(trials):
            self.hk_algorithm(reset_grid=True, update_clusters=update_clusters)
            biggest_cluster = self.find_biggest_cluster()
            self.trials_array[trial] = biggest_cluster

    def t_histogram_trials(self, trials=1, update_clusters=False,
                           reset_histogram=True, normalize_histogram=False):
        self.number_of_trials = trials
        for trial in range(trials):
            self.hk_algorithm(reset_grid=True,
                              update_clusters=update_clusters,
                              reset_histogram=reset_histogram)
            self.convert_cluster_to_histogram()
        if normalize_histogram:
            self.cluster_size_histogram = {size: (quantity / trials)
                                           for size, quantity in self.cluster_size_histogram.items()}

    def get_histogram(self):
        return self.cluster_size_histogram

    def get_average_biggest_cluster(self):
        if self.trials_array is not None:
            avg_cluster = self.trials_array.mean()
            return avg_cluster
        else:
            return 0

    def count_all_clusters(self):
        return np.sum(np.array(list(self.cluster_size_histogram.values())))

    def map_random_values_to_clusters(self):
        grid = self.get_current_grid()
        unique_values = np.unique(grid)
        unique_values = unique_values[unique_values != 0]
        for value in unique_values:
            grid[grid == value] = np.random.randint(1000, 100000)
        return grid

    def visualize_clusters(self, ax=None):
        if ax:
            grid = self.map_random_values_to_clusters()
            different_clusters = self.count_all_clusters()
            biggest_cluster = self.find_biggest_cluster()
            title = (f'{different_clusters} different clusters'
                     f'{", concatenated" if self.clusters_concatenated else ""}\n'
                     f'biggest cluster: {biggest_cluster}, L = {self.L}, p = {self.p}')
            ax.imshow(grid, vmin=grid.min(), vmax=grid.max(),
                      cmap='gnuplot', interpolation='nearest')
            ax.set_title(title)
            ax.set(xticks=[], yticks=[])


if __name__ == '__main__':
    L = 500
    p = [0.4, 0.54, 0.56, 0.58, 0.6, 0.8]
    # p = [0.56]
    use_one_column = False
    concatenate = True

    spanning_cluster = SpanningCluster(L=L)
    initial_grid = spanning_cluster.get_initial_grid()
    if use_one_column:
        figure, axes = plt.subplots(len(p), 1, layout='constrained')
        figure.set_size_inches(4, 3 * len(p))
    else:
        graph_length = int(len(p) / 2)
        figure, axes = plt.subplots(graph_length, 2, layout='constrained')
        figure.set_size_inches(8, 3 * graph_length)
        axes = axes.ravel()
    axes = [axes] if len(p) == 1 else axes
    for index, probability in enumerate(p):
        start_time = time()
        spanning_cluster.change_probability(probability)
        spanning_cluster.hk_algorithm(reset_grid=True,
                                      initial_grid=initial_grid,
                                      update_clusters=concatenate)
        spanning_cluster.convert_cluster_to_histogram()
        spanning_cluster.visualize_clusters(ax=axes[index])
        stop_time = time()
        print(f'Visualization done for p = {probability}. '
              f'Time taken: {round(stop_time - start_time, 3)} seconds')

    image_path = 'images'
    make_directories([image_path])
    image_name = f'HKVisualizationL{L}p'
    for probability in p:
        image_name += f'-{probability}'
    image_name += '_concat' if concatenate else ''
    image_name += '_one_col' if use_one_column else '_two_col'
    image_name += '.png'

    path = os.path.join(image_path, image_name)
    if not check_if_file_exists(path):
        figure.savefig(path)
    plt.show()

