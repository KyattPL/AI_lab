from copy import deepcopy
from random import randint, random
from math import ceil
from types import new_class
from typing import Tuple
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

    def __init__(self, dataset, NO_MACHINES=9, NO_TILES=9, POP_SIZE=2000,
                 WIDTH=3, SELECT_N=25, PROB_MUTATION=0.5, PROB_CROSSOVER=0.5) -> None:
        """
        Reads the data from JSON files, generates a single CostFlow object.
        """
        reader = DataReader(filenames=dataset)
        costs = reader.read_cost()
        flows = reader.read_flow()

        self.NO_MACHINES = NO_MACHINES
        self.NO_TILES = NO_TILES
        self.POP_SIZE = POP_SIZE
        self.WIDTH = WIDTH
        self.SELECT_N = SELECT_N
        self.PROB_MUTATION = PROB_MUTATION
        self.PROB_CROSSOVER = PROB_CROSSOVER

        self.machines = CostFlow(costs, flows, NO_MACHINES)
        self.population = []

    def generate_random_population(self) -> None:
        """
        Generates the whole population. Each individual randomly places machines.
        """
        self.population: list[Individual] = []
        for i in range(self.POP_SIZE):
            ind = Individual(self.NO_MACHINES, self.NO_TILES)
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
            for src_machine in range(len(self.machines.connections)):
                for dst_machine in self.machines.connections[src_machine]:
                    src_spot = ind.genotype[src_machine]
                    dst_spot = ind.genotype[dst_machine]

                    diff_x = abs((src_spot % self.WIDTH) -
                                 (dst_spot % self.WIDTH))
                    diff_y = abs(dst_spot // self.WIDTH -
                                 src_spot // self.WIDTH)

                    manhattan = diff_x + diff_y

                    connection = {}
                    for conn in self.machines.data[src_machine]:
                        if conn['dest'] == dst_machine:
                            connection = conn

                    individual_rating += manhattan * \
                        connection['cost'] * connection['flow']

            if individual_rating < best_rating:
                best_rating = individual_rating

        return best_rating

    def evaluate_population_roulette(self) -> Tuple[int, list[int]]:
        ratings = []
        best_rating = float("inf")

        for ind in self.population:
            individual_rating = 0
            for src_machine in range(len(self.machines.connections)):
                for dst_machine in self.machines.connections[src_machine]:
                    src_spot = ind.genotype[src_machine]
                    dst_spot = ind.genotype[dst_machine]

                    diff_x = abs((src_spot % self.WIDTH) -
                                 (dst_spot % self.WIDTH))
                    diff_y = abs(dst_spot // self.WIDTH -
                                 src_spot // self.WIDTH)

                    manhattan = diff_x + diff_y

                    connection = {}
                    for conn in self.machines.data[src_machine]:
                        if conn['dest'] == dst_machine:
                            connection = conn

                    individual_rating += manhattan * \
                        connection['cost'] * connection['flow']

            if individual_rating < best_rating:
                best_rating = individual_rating

            ratings.append(individual_rating)

        return best_rating, ratings

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

        for src_machine in range(len(self.machines.connections)):
            for dst_machine in self.machines.connections[src_machine]:
                src_spot = ind.genotype[src_machine]
                dst_spot = ind.genotype[dst_machine]
                diff_x = abs((src_spot % self.WIDTH) - (dst_spot % self.WIDTH))
                diff_y = abs(dst_spot // self.WIDTH - src_spot // self.WIDTH)
                manhattan = diff_x + diff_y

                connection = {}
                for conn in self.machines.data[src_machine]:
                    if conn['dest'] == dst_machine:
                        connection = conn

                individual_rating += manhattan * \
                    connection['cost'] * connection['flow']

        return individual_rating

    def select_individual_tournament(self) -> Individual:
        randomized_individuals = []

        while len(randomized_individuals) != self.SELECT_N:
            random_index = randint(0, self.POP_SIZE - 1)
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

    def select_individual_roulette(self, ratings: list[int]) -> Individual:
        sum_of_ratings = 0

        for rating in ratings:
            sum_of_ratings += rating

        probabilities = []
        sum_of_probs = 0

        for rating in ratings:
            probabilities.append(
                sum_of_probs + (sum_of_ratings / rating)**7)
            sum_of_probs += (sum_of_ratings / rating)**7

        random_num = randint(0, ceil(sum_of_probs))
        index_of_individual = 0

        for prob in probabilities:
            if random_num < prob:
                break
            else:
                index_of_individual += 1

        if index_of_individual == self.POP_SIZE:
            index_of_individual -= 1

        return self.population[index_of_individual]

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
        random_machine_no = randint(0, self.NO_MACHINES - 1)
        second_gene = second_parent.genotype[random_machine_no]
        new_genotype = deepcopy(first_parent.genotype)

        if second_gene in new_genotype:
            machine_occupying_place = new_genotype.index(second_gene)
            random_machine_spot = new_genotype[random_machine_no]
            new_genotype[random_machine_no] = second_gene
            new_genotype[machine_occupying_place] = random_machine_spot
        else:
            new_genotype[random_machine_no] = second_gene

        return Individual(self.NO_MACHINES, self.NO_TILES, new_genotype)

    def mutation(self, ind: Individual) -> Individual:
        new_individual = deepcopy(ind)
        for machine in range(self.NO_MACHINES):
            randomized = random()
            if randomized < self.PROB_MUTATION:
                temp = new_individual.genotype[machine]
                new_individual.genotype[machine] = new_individual.genotype[(
                    machine + 1) % self.NO_MACHINES]
                new_individual.genotype[(machine + 1) %
                                        self.NO_MACHINES] = temp

        return new_individual
