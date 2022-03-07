from random import randint


class Individual:
    """
    Class representing an individual in the population.

    Fields:
        no_machines (int): Number of available machines to place
        no_tiles (int): Number of available tiles/spots for the machine to be placed at
        genotype (list[int]): List containing positions of the machines in order (index is the
            machine number, value at that index is the tile on which that machine stands)
    """

    def __init__(self, NO_MACHINES: int, NO_TILES: int) -> None:
        """
        Args:
            NO_MACHINES (int): Number of machines to be placed in a factory
            NO_TILES (int): Number of available tiles/spots for machines to be placed at
        """
        self.no_machines = NO_MACHINES
        self.no_tiles = NO_TILES
        self.genotype = []

        for i in range(NO_MACHINES):
            self.genotype.append(None)

    def randomize(self) -> None:
        """
        Randomly places machines on tiles. Modifies self.genotype.
        """
        available_spots = []
        machines_assigned = 0

        for i in range(self.no_tiles):
            available_spots.append(i)

        while machines_assigned != self.no_machines:
            randomized = randint(0, len(available_spots) - 1)
            spot = available_spots.pop(randomized)
            self.genotype[machines_assigned] = spot
            machines_assigned += 1
