class CostFlow:
    """
    Class that concatenates costs and material flows between machines.
    The result is a list (index indicates source machine number) of lists
    (that contain destination machines with given costs and material flows).

    Fields:
        data (list[list[list[3]]]): 3-element list represents (destination, cost, flow),
            outer list represents all of the destinations, most outer list represents all source machines
    """

    def __init__(self, costs: list, flows: list, NO_MACHINES: int) -> None:
        """
        Args:
            costs (list[dict]): list of costs between src and dest machines
            flows (list[dict]): list of material flows between src and dest machines
            NO_MACHINES (int): number of machines
        """
        self.data = []
        for i in range(NO_MACHINES - 1):
            self.data.append([])

        for i in range(len(costs)):
            self.data[costs[i]['source']].append(
                [costs[i]['dest'], costs[i]['cost'], flows[i]['amount']])
