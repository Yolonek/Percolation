import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


class ProbabilitySite(object):

    def __init__(self, L=100, p=0.5, initial_grid=None):
        self.L = L
        self.p = p
        self.initial_grid = None
        self.grid = None
        self.step = 0
        self.set_initial_grid(initial_grid=initial_grid)

    def set_initial_grid(self, initial_grid=None):
        if initial_grid is None:
            self.initial_grid = np.random.random((self.L, self.L))
        else:
            self.initial_grid = initial_grid

    def get_initial_grid(self):
        return self.initial_grid

    def change_probability(self, probability):
        self.p = probability

    def change_grid_size(self, new_size):
        self.L = new_size
        self.set_initial_grid()

    def grid_thresholding(self):
        self.grid = np.where(self.initial_grid < 1 - self.p, 0, 1)
        self.grid = self.grid.astype(int)
        self.step = 1

    def plot_grid(self, save='', colormap=(), grid_threshold=0, initial=True):
        if initial:
            min_val, max_val = 0, 1
        else:
            min_val, max_val = np.min(self.grid), np.max(self.grid)
        grid = self.initial_grid if initial else self.grid
        if colormap:
            colors = colormap[0]
            quality = colormap[1]
            cmap = LinearSegmentedColormap.from_list('', colors, N=quality)
        else:
            cmap = 'Greys'
        if grid_threshold:
            grid[grid >= grid_threshold] = grid_threshold
        figure = plt.imshow(grid, cmap=cmap, vmin=min_val, vmax=max_val,
                            interpolation='nearest')
        if save:
            pass
        return figure


if __name__ == '__main__':
    L = 100
    p = 0.5
    probability_grid = ProbabilitySite(L=L, p=p)
    colors = [(0, 0, 0), (1, 1, 1)]
    bitmap = 2
    print(probability_grid.initial_grid)
    fig1 = probability_grid.plot_grid()
    plt.show()
    probability_grid.grid_thresholding()
    fig2 = probability_grid.plot_grid(initial=False, colormap=(colors, bitmap))
    plt.show()

