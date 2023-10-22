import numpy as np
from CommonFunctions import make_directories, check_if_file_exists
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os


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

    def plot_grid_as_matrix(self, matrix=None, axes=None):
        if axes:
            axes.axis('off')
            matrix = np.round(np.array(matrix if matrix else self.initial_grid), 4)

            try:
                cell_height = 1 / matrix.shape[0]
                cell_width = 1 / matrix.shape[1]
            except IndexError:
                matrix = matrix[:, None]
                cell_height = 1 / matrix.shape[0]
                cell_width = 1 / matrix.shape[1]

            table = axes.table(cellText=matrix, loc='center', cellLoc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(9)

            for cell in table._cells.values():
                cell.set_edgecolor('none')
                cell.set_linewidth(0)
                cell.set_height(cell_height)
                cell.set_width(cell_width)

    def plot_grid2(self, initial=True, ax=None, title='', cmap_name='gray'):
        if ax:
            grid = self.initial_grid if initial else self.grid
            ax.imshow(grid, cmap=cmap_name,
                      vmin=0, vmax=1, interpolation='nearest')
            if title:
                ax.set_title(title)


if __name__ == '__main__':
    L = 100
    p = [0.3, 0.5, 0.7]

    figure, axes = plt.subplots(len(p), 2, layout='constrained')
    probability_grid = ProbabilitySite(L=L)
    for index, probability in enumerate(p):
        probability_grid.change_probability(probability)
        probability_grid.grid_thresholding()
        title = f'$p = {probability}$'
        probability_grid.plot_grid2(initial=True, ax=axes[index][0],
                                    title=title, cmap_name='bone')
        probability_grid.plot_grid2(initial=False, ax=axes[index][1],
                                    title=title, cmap_name='bone')
        axes[index][0].axis('off')
        axes[index][1].axis('off')

    figure.suptitle('Probability grid before and after thresholding for various $p$\n'
                    'for the same probability grid')
    figure.set_size_inches(5, 2.2 * len(p))
    plt.show()

    image_path = 'images'
    make_directories([image_path])
    image_name = f'ProbabilitySiteL{L}p'
    for probability in p:
        image_name += f'-{probability}'
    image_name += '.png'

    path = os.path.join(image_path, image_name)
    if not check_if_file_exists(path):
        figure.savefig(path)



