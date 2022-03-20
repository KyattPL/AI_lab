import numpy as np
import multiprocessing
import matplotlib.pyplot as plt
from copy import deepcopy
from random import random
from typing import Tuple
from GA import GA

num_of_runs = 10
num_of_generations = 100
is_tournament = True

no_progress_for = 100
is_end_cond_dynamic = False


def ga_single_run() -> Tuple[list[int], list[int]]:
    # hard - 9119
    ga = GA('hard', 24, 30, 500, 6, 25, 0.15, 0.75)
    ga.generate_random_population()
    curr_generation = 0
    generations_wo_progress = 0
    worst_result = 0

    best_each_generation = []
    worst_each_generation = []

    if is_tournament:
        best_result = ga.evaluate_population()
    else:
        best_result, ratings = ga.evaluate_population_roulette()

    if is_end_cond_dynamic:
        def condition(): return no_progress_for > generations_wo_progress
    else:
        def condition(): return num_of_generations > curr_generation

    while condition():
        # print(best_result)
        new_pop = []
        new_ratings = []

        while len(new_pop) < len(ga.population):

            if is_tournament:
                first_parent = ga.select_individual_tournament()
                second_parent = ga.select_individual_tournament()
            else:
                first_parent = ga.select_individual_roulette(ratings)
                second_parent = ga.select_individual_roulette(ratings)

            if (random() < ga.PROB_CROSSOVER):
                child = ga.crossover(first_parent, second_parent)
            else:
                child = deepcopy(first_parent)

            child = ga.mutation(child)
            child_rating = ga.evaluate_individual(child)

            if child_rating < best_result:
                best_result = child_rating
                generations_wo_progress = -1

            if child_rating > worst_result:
                worst_result = child_rating

            new_pop.append(child)
            new_ratings.append(child_rating)
        ga.population = new_pop
        ratings = new_ratings
        curr_generation += 1
        generations_wo_progress += 1
        best_each_generation.append(best_result)
        worst_each_generation.append(worst_result)

    return best_each_generation, worst_each_generation


def single_process(i, queue):
    print(i)
    best_each_generation, worst_each_generation = ga_single_run()
    queue.put((best_each_generation, worst_each_generation))


if __name__ == "__main__":

    best_all_generations = []
    worst_all_generations = []

    q = multiprocessing.Queue()
    processes = []

    for i in range(num_of_runs):
        task = multiprocessing.Process(target=single_process, args=([i, q]))
        task.start()
        processes.append(task)

    for p in processes:
        p.join()
        single_best, single_worst = q.get()
        best_all_generations.append(single_best)
        worst_all_generations.append(single_worst)

    bests = []
    avgs = []
    worsts = []
    for i in range(num_of_generations):
        avg = 0
        best = float("inf")
        worst = 0
        for j in range(num_of_runs):
            if best_all_generations[j][i] > worst:
                worst = best_all_generations[j][i]
            if best_all_generations[j][i] < best:
                best = best_all_generations[j][i]

            avg += best_all_generations[j][i]
        bests.append(best)
        avgs.append(avg / num_of_runs)
        worsts.append(worst)

    fig, ax = plt.subplots()
    plt.plot(np.arange(num_of_generations), bests, label="best")
    plt.plot(np.arange(num_of_generations), avgs, label="avg")
    plt.plot(np.arange(num_of_generations), worsts, label="worsts")
    plt.legend(["best", "avg", "worst"], loc="upper right")
    plt.show()

    # Sprawozdanie:
    #   - tabele i wykresy dot. porównania:
    #       * krzyżowanie (ON/OFF)
    #       * mutacje (ON/OFF)
    #       * rozmiar populacji (mało, ok, za dużo)
    #       * liczba pokoleń

    # [[5000, 5000, 4900, 4850, 4850], [5000, 5000, 4900, 4850, 4850], ...]
