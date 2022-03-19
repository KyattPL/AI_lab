from copy import deepcopy
from random import random
from GA import GA

expected_solution = 4818
is_tournament = False

if __name__ == "__main__":
    ga = GA('easy', 9, 9, 2000, 3, 25, 0.5, 0.5)
    ga.generate_random_population()

    if is_tournament:
        best_result = ga.evaluate_population()
    else:
        best_result, ratings = ga.evaluate_population_roulette()
    
    while best_result > expected_solution:
        print(best_result)
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
            
            new_pop.append(child)
            new_ratings.append(child_rating)
        ga.population = new_pop
        ratings = new_ratings

    print(best_result)

# Sprawozdanie:
#   - tabele i wykresy dot. porównania:
#       * krzyżowanie (ON/OFF)
#       * mutacje (ON/OFF)
#       * rozmiar populacji (mało, ok, za dużo)
#       * liczba pokoleń