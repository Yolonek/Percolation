from ProbabilitySite import ProbabilitySite
import numpy as np
import pandas as pd
from time import time
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


class BurningModel(ProbabilitySite):

    def __init__(self, L=100, p=0.5, initial_grid=None):
        super().__init__(L=L, p=p, initial_grid=initial_grid)
        self.directions = ['N', 'E', 'W', 'S']
        self.grid_changed = True
        self.number_of_trials = 1
        self.trials_array = None

    def set_top_row_to_initial_value(self):
        if self.grid is not None:
            self.grid[0, :][self.grid[0, :] == 1] = 2
            self.step = 2

    def another_burning_step(self):
        burning_progress = np.where(self.grid == self.step)
        self.step += 1
        x_index = burning_progress[0]
        y_index = burning_progress[1]
        self.grid_changed = False
        for x, y in zip(x_index, y_index):
            for direction in self.directions:
                self.burning_step(x, y, direction)

    def burning_step(self, x_pos, y_pos, direction):
        if direction == 'N' and 0 <= x_pos - 1 < self.L and self.grid[x_pos - 1][y_pos] == 1:
            self.grid[x_pos - 1][y_pos] = self.step
            self.grid_changed = True
        if direction == 'S' and 0 <= x_pos + 1 < self.L and self.grid[x_pos + 1][y_pos] == 1:
            self.grid[x_pos + 1][y_pos] = self.step
            self.grid_changed = True
        if direction == 'W' and 0 <= y_pos - 1 < self.L and self.grid[x_pos][y_pos - 1] == 1:
            self.grid[x_pos][y_pos - 1] = self.step
            self.grid_changed = True
        if direction == 'E' and 0 <= y_pos + 1 < self.L and self.grid[x_pos][y_pos + 1] == 1:
            self.grid[x_pos][y_pos + 1] = self.step
            self.grid_changed = True

    def check_if_percolation_threshold_reached(self):
        if self.step in self.grid[-1, :]:
            return True
        else:
            return False

    def burning_model(self, reset_grid=False, break_at_percolation=True):
        if reset_grid:
            self.set_initial_grid()
            self.grid_thresholding()
            self.set_top_row_to_initial_value()
        while True:
            self.another_burning_step()
            if self.check_if_percolation_threshold_reached() and break_at_percolation:
                break
            if self.grid_changed is False:
                break

    def plot_percolation_grid(self, grid_threshold=0):
        colors = [(0, 0, 0), (0, 1, 0), (1, 0, 0)]
        figure = self.plot_grid(grid_threshold=grid_threshold,
                                colormap=(colors, 3))
        return figure

    def t_percolation_trials(self, trials=1):
        self.number_of_trials = trials
        self.trials_array = np.zeros(trials)
        for trial in range(trials):
            self.burning_model(reset_grid=True, break_at_percolation=True)
            if self.grid_changed:
                self.trials_array[trial] = 1

    def get_percolation_probability(self):
        if self.trials_array is not None:
            percolation_probability = self.trials_array.mean()
            return percolation_probability
        else:
            return 0


if __name__ == '__main__':
    start_time = time()

    L = 100
    # p = 0.1
    t = 10000
    probability_space = np.arange(0.01, 0.99, 0.01)
    num_of_perc = len(probability_space)
    perc_prob_space = np.zeros(num_of_perc)

    burn = BurningModel(L=L)
    for probability, index in zip(probability_space, range(num_of_perc)):
        print(probability)
        burn.change_probability(probability)
        burn.t_percolation_trials(trials=t)
        perc_probability = burn.get_percolation_probability()
        perc_prob_space[index] = perc_probability

    print(probability_space)
    print(perc_prob_space)

    file_title = f'Ave_L{L}T{t}.csv'
    data_to_save = pd.DataFrame()
    data_to_save['site_prob'] = probability_space.tolist()
    data_to_save['perc_prob'] = perc_prob_space.tolist()
    data_to_save.to_csv(file_title, sep=',', index=False)

    stop_time = time()
    print(f'Program took {round(stop_time - start_time, 3)} seconds')
