import json


class DataReader:
    """
    Class that is used to read appropriate JSON files (containing costs and material flows
    data between machines).
    """

    def __init__(self, filenames="easy") -> None:
        """
        Args:
            filenames (str, optional): Front part of the filename that is followed by '_cost.json' and '_flow.json'.
                Defaults to "easy".
        """
        self.filenames = filenames

    def read_cost(self) -> list:
        """Reads costs between machines from JSON file

        Returns:
            list: list containing dictionaries {src, dest, cost}
        """
        with open(f'{self.filenames}_cost.json', "r") as file:
            data = json.load(file)

        return data

    def read_flow(self) -> list:
        """Reads material flows between machines from JSON file

        Returns:
            list: list containing dictionaries {src, dest, amount}
        """
        with open(f'{self.filenames}_flow.json', "r") as file:
            data = json.load(file)

        return data
