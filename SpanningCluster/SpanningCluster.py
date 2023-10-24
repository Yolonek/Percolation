from ProbabilitySite import ProbabilitySite
from matplotlib import pyplot as plt
import numpy as np


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

    def reset_simulation(self, initial_grid=None):
        self.k = 2
        self.Mk = {f'Mk{self.k}': f'{1}'}
        self.set_initial_grid(initial_grid=initial_grid)

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

    def concatenate_clusters(self, bigger_k, smaller_k):
        bigger_mk = self.cluster_size(bigger_k)
        smaller_mk = self.cluster_size(smaller_k)
        cluster_sum = bigger_mk + smaller_mk + 1
        self.set_cluster_size(bigger_k, cluster_sum)
        self.set_cluster_size(smaller_k, bigger_k, negative=True)
        # self.grid[np.where(self.grid == smaller_k)] = bigger_k

    def hk_algorithm_step(self, x_pos, y_pos):
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
                self.concatenate_clusters(self.top_value, self.left_value)
            else:
                self.grid[x_pos][y_pos] = self.left_value
                self.concatenate_clusters(self.left_value, self.top_value)

    def hk_algorithm(self, reset_grid=False, count_histogram=False):
        if reset_grid:
            self.set_initial_grid()
            self.grid_thresholding()
            self.set_top_left_site()
        self.find_occupied_sites()
        x_values = self.occupied_sites[0]
        y_values = self.occupied_sites[1]
        for x, y in zip(x_values, y_values):
            self.hk_algorithm_step(x, y)

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

    def t_spanning_cluster_trials(self, trials=1):
        self.number_of_trials = trials
        self.trials_array = np.zeros(trials)
        for trial in range(trials):
            self.hk_algorithm(reset_grid=True)
            biggest_cluster = self.find_biggest_cluster()
            self.trials_array[trial] = biggest_cluster
            self.convert_cluster_to_histogram()
            self.reset_simulation()

    def get_histogram(self):
        return self.cluster_size_histogram

    def get_average_biggest_cluster(self):
        if self.trials_array is not None:
            avg_cluster = self.trials_array.mean()
            return avg_cluster
        else:
            return 0


if __name__ == '__main__':
    L = 10
    p = 0.50
    cluster = SpanningCluster(L=L, p=p)
    cluster.grid_thresholding()
    print(cluster.grid)
    cluster.set_top_left_site()
    print(cluster.grid)
    cluster.hk_algorithm()
    print(cluster.grid)
    print(cluster.Mk)
    print(cluster.find_biggest_cluster())
    cluster.convert_cluster_to_histogram()
    print(cluster.cluster_size_histogram)
    cluster.reset_simulation()
    cluster.grid_thresholding()
    cluster.set_top_left_site()
    cluster.hk_algorithm()
    cluster.convert_cluster_to_histogram()
    print(cluster.cluster_size_histogram)



