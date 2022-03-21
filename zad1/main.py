import numpy as np
import multiprocessing
import matplotlib.pyplot as plt
from copy import deepcopy
from random import random
from typing import Tuple
from GA import GA
from Individual import Individual

num_of_runs = 10
num_of_generations = 500  # 500
is_tournament = True

no_progress_for = 100
is_end_cond_dynamic = False

dataset = 'hard'  # 'easy'
no_machines = 24  # 9
no_tiles = 30  # 9
num_of_pop = 500  # 10
width = 6  # 3
select_n = 50  # 3
mut_prob = 0.18  # 0.1
cross_prob = 0.7  # 0.6


def random_run():
    ga = GA(dataset, no_machines, no_tiles, num_of_pop,
            width, select_n, mut_prob, cross_prob)
    best_score = float("inf")
    worst_score = 0
    avg_rnd = 0
    std_rnd = []
    for i in range(num_of_runs * num_of_generations * num_of_pop):
        new_ind = Individual(no_machines, no_tiles)
        new_ind.randomize()
        rating = ga.evaluate_individual(new_ind)
        if rating < best_score:
            best_score = rating
        elif rating > worst_score:
            worst_score = rating

        avg_rnd += rating
        std_rnd.append(rating)
    avg_rnd /= num_of_runs * num_of_generations * num_of_pop
    std_rnd = np.std(std_rnd)
    print("\nRANDOM RUN:")
    print(f"best: {best_score}")
    print(f"worst: {worst_score}")
    print(f"avg: {avg_rnd}")
    print(f"std: {std_rnd}")


def ga_single_run() -> Tuple[list[int], list[int]]:
    # hard - 9119
    # ga = GA('hard', 24, 30, 500, 6, 25, 0.15, 0.75)
    ga = GA(dataset, no_machines, no_tiles, num_of_pop,
            width, select_n, mut_prob, cross_prob)
    #ga = GA('flat', 12, 12, 10, 12, 3, 0.5, 0.9)
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
        worst_result = 0
        best_result = float("inf")

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
        single_best, single_worst = q.get()
        best_all_generations.append(single_best)
        worst_all_generations.append(single_worst)

    for p in processes:
        p.join()

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

    best_of_runs = float("inf")
    worst_of_runs = 0
    avg_of_runs = 0
    std_of_runs = []

    for i in range(num_of_runs):
        if best_all_generations[i][-1] < best_of_runs:
            best_of_runs = best_all_generations[i][-1]

        if best_all_generations[i][-1] > worst_of_runs:
            worst_of_runs = best_all_generations[i][-1]

        avg_of_runs += best_all_generations[i][-1]
        std_of_runs.append(best_all_generations[i][-1])

    avg_of_runs /= num_of_runs
    std_of_runs = np.std(std_of_runs)
    print(f"best: {best_of_runs}")
    print(f"worst: {worst_of_runs}")
    print(f"avg: {avg_of_runs}")
    print(f"std: {std_of_runs}")

    random_run()

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
