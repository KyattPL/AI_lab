from copy import deepcopy
from random import randint, random
from DataReader import DataReader
from CostFlow import CostFlow
from Individual import Individual


class GA:
    """
    Class that represents a genetic algorithm to solve the FLC problem. Acts as an interface.

    Consts:
        NO_MACHINES (int): Number of machines to be placed
        NO_TILES (int): Number of available tiles/spots for the machines to be placed at
        POP_SIZE (int): Number of individuals in the whole population
        WIDTH (int): With addition of NO_TILES basically defines the grid format (has to be rectangular)

    Fields:
        population (list[Individual]): List of individuals in the current population
        machines (CostFlow): CostFlow object that provides data of cost/material flow values between
            every pair of machines
    """

    NO_MACHINES = 9
    NO_TILES = 9
    POP_SIZE = 10_000
    WIDTH = 3
    SELECT_N = 20
    PROB_MUTATION = 0.1
    PROB_CROSSOVER = 0.1

    def __init__(self) -> None:
        """
        Reads the data from JSON files, generates a single CostFlow object.
        """
        reader = DataReader()
        costs = reader.read_cost()
        flows = reader.read_flow()
        self.machines = CostFlow(costs, flows, GA.NO_MACHINES)
        self.population = []

    def generate_random_population(self) -> None:
        """
        Generates the whole population. Each individual randomly places machines.
        """
        self.population: list[Individual] = []
        for i in range(GA.POP_SIZE):
            ind = Individual(GA.NO_MACHINES, GA.NO_TILES)
            ind.randomize()
            self.population.append(ind)

    def evaluate_population(self) -> int:
        """
        Evaluates the whole population in terms of the cost + distance + material flow
        between each machine for every individual.

        Returns:
            int: best individual rating
        """
        best_rating = float("inf")

        for ind in self.population:
            individual_rating = 0
            for src_machine in range(GA.NO_MACHINES - 1):
                for dst_machine in range(src_machine + 1, GA.NO_MACHINES):
                    src_spot = ind.genotype[src_machine]
                    dst_spot = ind.genotype[dst_machine]

                    diff_x = abs((src_spot % GA.WIDTH) - (dst_spot % GA.WIDTH))
                    diff_y = abs(dst_spot // GA.WIDTH - src_spot // GA.WIDTH)

                    manhattan = diff_x + diff_y
                    dict_index = dst_machine - src_machine - 1

                    individual_rating += manhattan * \
                        self.machines.data[src_machine][dict_index][1] * \
                        self.machines.data[src_machine][dict_index][2]

            if individual_rating < best_rating:
                best_rating = individual_rating

        return best_rating

    def evaluate_individual(self, ind: Individual) -> int:
        """
        Evaluates the single individual in terms of the cost + distance + material flow
        between each machine for that individual.

        Args:
            ind (Individual): individual to calculate rating for

        Returns:
            int: rating for the given individual
        """
        individual_rating = 0
        for src_machine in range(GA.NO_MACHINES - 1):
            for dst_machine in range(src_machine + 1, GA.NO_MACHINES):
                src_spot = ind.genotype[src_machine]
                dst_spot = ind.genotype[dst_machine]

                diff_x = abs((src_spot % GA.WIDTH) - (dst_spot % GA.WIDTH))
                diff_y = abs(dst_spot // GA.WIDTH - src_spot // GA.WIDTH)

                manhattan = diff_x + diff_y
                dict_index = dst_machine - src_machine - 1

                individual_rating += manhattan * \
                    self.machines.data[src_machine][dict_index][1] * \
                    self.machines.data[src_machine][dict_index][2]

        return individual_rating

    def select_individual(self) -> Individual:
        randomized_individuals = []

        while len(randomized_individuals) != GA.SELECT_N:
            random_index = randint(0, GA.POP_SIZE - 1)
            random_individual = self.population[random_index]
            if random_individual not in randomized_individuals:
                randomized_individuals.append(random_individual)

        best_individual = None
        best_score = float("inf")

        for ind in randomized_individuals:
            temp_score = self.evaluate_individual(ind)
            if temp_score < best_score:
                best_score = temp_score
                best_individual = ind

        return best_individual

    def crossover(self, first_parent: Individual, second_parent: Individual) -> Individual:
        """
        Since genotype are the positions of the machines (where index is the machine number),
        when placing a machine on another position there is a chance that this position has been
        already taken. In that case instead of moving one machine I switch the placement of both
        machines (so there won't be any duplicates possible).

        Args:
            first_parent (Individual): _description_
            second_parent (Individual): _description_

        Returns:
            Individual: _description_
        """
        random_machine_no = randint(0, GA.NO_MACHINES - 1)
        second_gene = second_parent.genotype[random_machine_no]
        new_genotype = deepcopy(first_parent.genotype)

        if second_gene in new_genotype:
            machine_occupying_place = new_genotype.index(second_gene)
            random_machine_spot = new_genotype[random_machine_no]
            new_genotype[random_machine_no] = second_gene
            new_genotype[machine_occupying_place] = random_machine_spot
        else:
            new_genotype[random_machine_no] = second_gene

        return Individual(GA.NO_MACHINES, GA.NO_TILES, new_genotype)

    def mutation(self, ind: Individual) -> Individual:
        new_individual = deepcopy(ind)
        for machine in range(GA.NO_MACHINES):
            randomized = random()
            if randomized < GA.PROB_MUTATION:
                mutated_gene = (
                    new_individual.genotype[machine] + 1) % GA.NO_TILES
                if mutated_gene not in new_individual.genotype:
                    new_individual.genotype[machine] = mutated_gene

        return new_individual
