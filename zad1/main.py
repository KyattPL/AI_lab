from copy import deepcopy
from random import random
from GA import GA

expected_solution = 4818

if __name__ == "__main__":
    ga = GA()
    ga.generate_random_population()
    best_result = ga.evaluate_population()
    while best_result > expected_solution:
        print(best_result)
        new_pop = []
        while len(new_pop) < len(ga.population):
            first_parent = ga.select_individual()
            second_parent = ga.select_individual()
            if (random() < ga.PROB_CROSSOVER):
                child = ga.crossover(first_parent, second_parent)
            else:
                child = deepcopy(first_parent)
            child = ga.mutation(child)
            child_rating = ga.evaluate_individual(child)
            if child_rating < best_result:
                best_result = child_rating
            new_pop.append(child)
        ga.population = new_pop
    print(best_result)
