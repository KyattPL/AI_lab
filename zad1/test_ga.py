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


if __name__ == "__main__":
    ga = GA('easy', 9, 9, 5, 3, 5, 0.5, 0.5)
    seed(101)
    test_randomizing_of_population(ga)
    seed(101)
    test_randomizing_of_population(ga)
    test_evaluation(ga)
    test_tournament(ga) # Czy wybiera o najmniejszej wartości

    # - nwm jak pokazać że ruletka dobre prawdopodobieństwa daje bez ingerowania w kod
    # - trzeba zrobić scenariusz pokazujący losowanie w turnieju (najlepiej z 5 razy)
    # - można zrobić seed() co weźmie aktualny czas i zrobić z tego scenariusz
    #   że populacja stała a turniej i ruletka losujo
    # - tak samo z seed() można dla stałej populacji pokazać losowy crossover i mutacje