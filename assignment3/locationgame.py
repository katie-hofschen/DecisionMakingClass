import numpy as np
from itertools import permutations, product
from assignment3.strategicgame import StrategicGame

class LocationGame(StrategicGame):

    def __init__(self, n):
        """" For every number n, LocationGame(n) builds
        a two-player discrete location game along "Main Street"
        with n locations.
        """
        self.n_locations = n
        self.matrix = self.createMatrix()
        super().__init__(self.matrix)

    def createMatrix(self):
        # very inefficient for larger number of locations

        if self.n_locations <= 0 or type(self.n_locations) != int:
            raise Exception("There must be at least 1 Location and the number of locations must be an integer.")
        else:
            matrix = np.zeros((self.n_locations, self.n_locations), dtype=tuple)

            for combo in permutations(np.arange(0, self.n_locations)):
                diff = np.absolute(combo[0] - combo[1])
                if combo[0] < combo[1]:
                    row = (combo[0] + 1) + ((diff-1)/2)
                    col = (self.n_locations - combo[1]) + ((diff-1)/2)
                    matrix[combo[0], combo[1]] = tuple((row,col))
                else:
                    col = (combo[1] + 1) + ((diff-1)/2)
                    row = (self.n_locations - combo[0]) + ((diff-1)/2)
                    matrix[combo[0], combo[1]] = tuple((row,col))

            # Diagonal from top left to bottom right  Fill both diagonals with equal utilities
            for x in range(self.n_locations ):
                for y in range(self.n_locations):
                    if x+y == self.n_locations-1:
                        matrix[y,x] = tuple([(self.n_locations/2.0), (self.n_locations/2.0)])
                    if x-y == 0:
                        matrix[y,x] = tuple([(self.n_locations/2.0), (self.n_locations/2.0)])
            return matrix.tolist()


def main():
    lg1 = LocationGame(7)
    print(lg1.iesds(verbose=True))
    # print("\n==========================================\n")
    # print(f"Location Game with 5 locations\n{lg1}")
    # print(f"After IESDS \n{lg1.iesds(verbose=True)}")

    # lg2 = LocationGame(3)
    # print("\n==========================================\n")
    # print(f"Location Game with 3 locations\n{lg2}")
    # print(f"Nash profiles \n{lg2.find_Nash_profiles()}")
    # print(f"Nash profiles \n{lg2.iesds(verbose=True)}")

    # lg3 = LocationGame(28)
    # print("\n==========================================\n")
    # print(f"Before IESDS\n{lg3}")
    # print(f"After IESDS\n{lg3.iesds(verbose=True)}")
    #
    # lg4 = LocationGame(187)
    # print("\n==========================================\n")
    # print(f"Before IESDS\n{lg4}")
    # print(f"Nash profiles\n{lg4.find_Nash_profiles()}")


if __name__ == '__main__':
    main()