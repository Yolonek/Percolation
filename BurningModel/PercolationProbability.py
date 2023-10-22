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