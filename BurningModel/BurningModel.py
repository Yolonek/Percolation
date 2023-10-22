from ProbabilitySite import ProbabilitySite
import numpy as np
import os
import pandas as pd
from time import time
from CommonFunctions import make_directories, check_if_file_exists
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

    def plot_percolation(self, ax=None, cmap=()):
        if ax:
            cmap = cmap if cmap else ([(0, 0, 0), (0, 1, 0), (1, 0, 0)], 3)
            grid = self.grid
            grid[grid >= 2] = 2
            colors, quality = cmap
            cmap = LinearSegmentedColormap.from_list('', colors, N=quality)
            title = (f'{"Percolation reached" if self.check_if_percolation_threshold_reached() else "No percolation"}.'
                     f'$L = {self.L}$\n Longest path: {self.step} steps, $p = {self.p}$')
            ax.imshow(grid, cmap=cmap, interpolation='nearest')
            ax.set_title(title)
            ax.axis('off')


if __name__ == '__main__':
    L = 500
    p = [0.5, 0.6, 0.7]

    figure, axes = plt.subplots(len(p), 1, layout='constrained')
    probability_grid = BurningModel(L=L)
    for index, probability in enumerate(p):
        probability_grid.change_probability(probability)
        probability_grid.burning_model(reset_grid=True)
        probability_grid.plot_percolation(ax=axes[index])
    figure.set_size_inches(4, 3 * len(p))
    plt.show()

    image_path = 'images'
    make_directories([image_path])
    image_name = f'PercolationGraphL{L}p'
    for probability in p:
        image_name += f'-{probability}'
    image_name += '.png'

    path = os.path.join(image_path, image_name)
    if not check_if_file_exists(path):
        figure.savefig(path)




