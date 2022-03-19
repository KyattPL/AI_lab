from random import seed
from GA import GA


def test_randomizing_of_population(ga_obj: GA):
    ga_obj.generate_random_population()
    
    for pop in ga_obj.population:
        print(pop.genotype)
    print()


def test_evaluation(ga_obj: GA):
    ratings = []

    for ind in ga_obj.population:
        ratings.append(ga_obj.evaluate_individual(ind))

    print(ratings)


def test_tournament(ga_obj: GA):
    ind = ga_obj.select_individual_tournament()
    print(ind.genotype)


def test_tournament_picks_best():
    ga = GA('easy', 9, 9, 5, 3, 5, 0.5, 0.5)
    seed(101)
    test_randomizing_of_population(ga)
    seed(101)
    test_randomizing_of_population(ga)
    test_evaluation(ga)
    test_tournament(ga) # Czy wybiera o najmniejszej wartości


def test_tournament_chooses_random():
    ga = GA('easy', 9, 9, 5, 3, 2, 0.5, 0.5)
    seed(105)
    test_randomizing_of_population(ga)
    test_evaluation(ga)
    seed()
    test_tournament(ga)


def test_roulette_chooses_random():
    ga = GA('easy', 9, 9, 5, 3, 5, 0.5, 0.5)
    seed(107)
    test_randomizing_of_population(ga)
    _,ratings = ga.evaluate_population_roulette()
    test_evaluation(ga)
    seed()
    ind = ga.select_individual_roulette(ratings)
    print(ind.genotype)


def test_random_crossover():
    ga = GA('easy', 9, 9, 5, 3, 2, 0.5, 0.5)
    seed(110)
    test_randomizing_of_population(ga)
    test_evaluation(ga)
    seed()
    parent_1 = ga.select_individual_tournament()
    parent_2 = ga.select_individual_tournament()
    child = ga.crossover(parent_1, parent_2)
    print(parent_1.genotype)
    print(parent_2.genotype)
    print(child.genotype)


def test_random_mutation():
    ga = GA('easy', 9, 9, 5, 3, 2, 0.5, 0.5)
    seed(112)
    test_randomizing_of_population(ga)
    test_evaluation(ga)
    ind = ga.population[0]
    seed()
    mutated = ga.mutation(ind)
    print(ind.genotype)
    print(mutated.genotype)

if __name__ == "__main__":
    #test_tournament_picks_best()
    #test_tournament_chooses_random()
    #test_roulette_chooses_random()
    #test_random_crossover()
    test_random_mutation()