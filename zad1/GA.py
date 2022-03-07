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
            int: Sum of the ratings of the individuals
        """
        sum_of_pop = 0

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

            print(individual_rating)
            sum_of_pop += individual_rating

    def evaluate_individual(ind: Individual) -> int:
        """_summary_

        Args:
            ind (Individual): _description_

        Returns:
            int: _description_
        """
        pass
