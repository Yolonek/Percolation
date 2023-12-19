import sys
sys.path.append('..')
from ProbabilitySite import ProbabilitySite
from matplotlib import pyplot as plt


def generate_probability_grid(L=10, p=0.5):
    return ProbabilitySite(L=L, p=p).get_initial_grid()


def plot_probability_grid(L=10, numeric=False):
    probability_site = ProbabilitySite(L=L)
    figure, axes = plt.subplots(1, 1, layout='constrained')
    axes.set_title(f'Probability grid generated for $L = {L}$')
    if numeric:
        probability_site.plot_grid_as_matrix(axes=axes)
    else:
        probability_site.plot_grid(initial=True, ax=axes, cmap_name='bone')
    return figure


def plot_threshold_grid(L=10, p=0.5, numeric=False, initial_grid=None):
    probability_site = ProbabilitySite(L=L, p=p, initial_grid=initial_grid)
    probability_site.grid_thresholding()
    figure, axes = plt.subplots(1, 1, layout='constrained')
    axes.set_title(f'Grid after thresholding for probability {p}')
    if numeric:
        probability_site.plot_grid_as_matrix(matrix=probability_site.get_current_grid(), axes=axes)
    else:
        probability_site.plot_grid(initial=False, ax=axes, cmap_name='bone')
    return figure


def plot_grid_comparison_after_threshold(L=10, p=0.5):
    probability_site = ProbabilitySite(L=L, p=p)
    probability_site.grid_thresholding()
    figure, axes = plt.subplots(1, 2, layout='constrained')
    figure.suptitle(f'Visual representation of ${L}' + r'\times' + f'{L}$ grid\n$p = {p}$')
    probability_site.plot_grid(initial=True, ax=axes[0], title='before thresholding', cmap_name='bone')
    probability_site.plot_grid(initial=False, ax=axes[1], title='after thresholding', cmap_name='bone')
    return figure


def compare_probability_site_for_different_p(L=10, probabilities=(0.2, 0.5, 0.8)):
    probability_site = ProbabilitySite(L=L)
    figure, axes = plt.subplots(2, 2, layout='constrained')
    axes = axes.ravel()
    figure.suptitle(f'Grid after thresholding for various probabilities')
    probability_site.plot_grid(initial=True, ax=axes[0], title='initial grid', cmap_name='bone')
    for index, probability in enumerate(probabilities):
        probability_site.change_probability(probability)
        probability_site.grid_thresholding()
        probability_site.plot_grid(initial=False, ax=axes[index + 1], title=f'$p = {probability}$')
    return figure
