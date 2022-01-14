import numpy as np
from assignment3.strategicgame import StrategicGame

class CournotDuopolyGame(StrategicGame):
    def __init__(self, prod_poss1, prod_poss2, c1, c2, price_fun):
        """"
        * c1 and c2 are unit costs for each firm eg c1 = c2 = 30
        * prod_fun is the product demand price function with 2 parameters
          that stand for the quantities produced by each firm eg. lambda x,y: 150 - x - y
        * the profit of one firm producing q and with unit cost c is q(P-c)
        * prod_poss1 and prod_poss2 are possible production amounts,
          e.g. range(0,100) or [i /25 for in in range(38*25, 42*25)]
        """

        self.prod_poss1 = prod_poss1
        self.prod_poss2 = prod_poss2

        self.cost1 = c1
        self.cost2 = c2

        self.price_fun = price_fun  #price_fun(x, y)

        self.matrix = self.create_matrix()
        super().__init__(self.matrix)

    def create_matrix(self):
        utility_firm1 = self.create_half_matrix(1)
        utility_firm2 = self.create_half_matrix(2)
        matrix = [[(a,b) for a,b in zip(row1, row2)] for row1, row2 in zip(utility_firm1,utility_firm2)]
        return matrix

    def create_half_matrix(self, firm=(1,2)):
        #function, shape, *, dtype=<class 'float'>, like=None, **kwargs
        lower_bound1 = self.prod_poss1[0]
        upper_bound1 = self.prod_poss1[-1] + 1
        lower_bound2 = self.prod_poss2[0]
        upper_bound2 = self.prod_poss2[-1] + 1

        if firm in [1,2]:
            matrix_one = np.fromfunction(
                lambda i, j: self.calculate_profit(i+lower_bound1, j+lower_bound2, firm),
                shape=(upper_bound1-lower_bound1, upper_bound2-lower_bound2))
        else:
            raise Exception("You must select either firm 1 or firm 2.")
        return matrix_one

    def calculate_profit(self, n_prod1, n_prod2, firm=(1,2)):
        if firm == 1 :
            profit = n_prod1 * (self.price_fun(n_prod1, n_prod2) - self.cost1)
        elif firm == 2:
            profit = n_prod2 * (self.price_fun(n_prod1, n_prod2) - self.cost2)
        else:
            raise Exception("You must select either firm 1 or firm 2.")
        return np.around(profit, 1)

    def maintain_equilibrium(self):
        pass

def main():

    cdg = CournotDuopolyGame(range(0, 5), range(0, 4), 15, 40, lambda x, y: 100 - (x + y) ** (1/2))
    print(cdg)
    print("Nash equilibria and unit price:",
          [((q1, q2), cdg.price_fun(q1, q2)) for (q1, q2) in cdg.find_Nash_profiles()])
    print(f"After IESDS\n{cdg.iesds()}")


if __name__ == '__main__':
    main()