import sys
sys.path.append('..')
from ProbabilitySite import ProbabilitySite
from BurningModel.BurningModel import BurningModel
from matplotlib import pyplot as plt
import numpy as np


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


def plot_grid_comparison_after_threshold(L=10, p=0.5, numeric=False, vertical=False, initial_grid=None):
    probability_site = ProbabilitySite(L=L, p=p, initial_grid=initial_grid)
    probability_site.grid_thresholding()
    if vertical:
        figure, axes = plt.subplots(2, 1, layout='constrained', figsize=(6, 10))
    else:
        figure, axes = plt.subplots(1, 2, layout='constrained')
    figure.suptitle(f'Visual representation of ${L}' + r'\times' + f'{L}$ grid\n$p = {p}$')
    if numeric:
        probability_site.plot_grid_as_matrix(matrix=probability_site.get_initial_grid(), axes=axes[0],
                                             title='before thresholding')
        probability_site.plot_grid_as_matrix(matrix=probability_site.get_current_grid(), axes=axes[1],
                                             title='after thresholding')
    else:
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


def burning_model_grid(L=10, p=0.5, numeric=False, initial_grid=None):
    burning_model = BurningModel(L=L, p=p, initial_grid=initial_grid)
    burning_model.burning_model()
    figure, axes = plt.subplots(1, 1, layout='constrained')
    if numeric:
        burning_model.plot_grid_as_matrix(matrix=burning_model.get_current_grid(), axes=axes)
    else:
        burning_model.plot_percolation(ax=axes, add_title=False)
    axes.set_title(f'Percolation for $L = {L}$ and $p = {p}$')
    return figure


def burning_model_three_stages(L=10, p=0.5, number_of_steps=30):
    burning_model = BurningModel(L=L, p=p)
    burning_model.grid_thresholding()
    figure, axes = plt.subplots(1, 3, layout='constrained')

    burning_model.set_top_row_to_initial_value()
    burning_model.plot_percolation(ax=axes[0])
    axes[0].set_title(f'Initial phase\nTop row set on fire')

    for _ in range(number_of_steps):
        burning_model.another_burning_step()
    burning_model.plot_percolation(ax=axes[1])
    axes[1].set_title(f'Grid after {number_of_steps} steps')

    burning_model.burning_model(reset_grid=True, initial_grid=burning_model.get_initial_grid())
    burning_model.plot_percolation(ax=axes[2])
    axes[2].set_title(f'Grid after percolation')
    return figure


def burning_model_compare_probability(L=50, p=(0.5, 0.6, 0.7)):
    figure, axes = plt.subplots(1, len(p), layout='constrained')
    probability_grid = BurningModel(L=L)
    initial_grid = probability_grid.get_initial_grid()
    for index, probability in enumerate(p):
        probability_grid.change_probability(probability)
        probability_grid.burning_model(reset_grid=True, initial_grid=initial_grid)
        probability_grid.plot_percolation(ax=axes[index])
        axes[index].title.set_size(8)
    return figure


def burning_model_percolation_plot(L=50, trials=100):
    percolation_probability = 0.592
    burning_model_mean = BurningModel(L=L)
    probability_space = np.linspace(0.45, 0.8, 15)
    percolation_space = np.zeros(len(probability_space))
    for index, probability in enumerate(probability_space):
        burning_model_mean.change_probability(probability)
        burning_model_mean.t_percolation_trials(trials=trials)
        percolation_space[index] = burning_model_mean.get_percolation_probability()
    figure, axes = plt.subplots(1, 1, layout='constrained')
    axes.plot(probability_space, percolation_space, color='black', label=f'L={L}')
    axes.axvline(x=percolation_probability,
                 color='blue',
                 linestyle='--',
                 label=f'$p_c$ = {percolation_probability}')
    axes.grid()
    axes.legend(loc='upper left')
    axes.set_title(f'Percolation probability based on {trials} number of trials')
    axes.set(xlabel='site probability', ylabel='percolation probability')
    return figure


def burning_model_percolation_interaction(L=50, p=0.5, step=2, numeric=False, initial_grid=None):
    model = BurningModel(L=L, p=p, initial_grid=initial_grid)
    model.grid_thresholding()
    model.set_top_row_to_initial_value()
    for _ in range(step - 2):
        model.another_burning_step()
    figure, axes = plt.subplots(1, 1, layout='constrained')
    if numeric:
        title = (f'{"Percolation reached" if model.check_if_percolation_threshold_reached() else "No percolation"}. '
                 f'$L = {model.L}$\n Longest path: {model.step} steps, $p = {model.p}$')
        model.plot_grid_as_matrix(matrix=model.get_current_grid(), axes=axes, title=title)
    else:
        model.plot_percolation(ax=axes)
    return figure
