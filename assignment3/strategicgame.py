#!/usr/bin/env python3
import numpy as np
from prettytable import PrettyTable
from itertools import permutations
'''An implementation of generic 2-player strategic games.

'''


class StrategicGame:

    def __init__(self, matrix):
        '''*matrix* is a two-dimensional array of pairs of numbers
           (primitive numerical types). It should be non-empty, and
           have at least row and one column. All subarrays of
           *matrix* should have the same length.

        '''
        self.matrix = [[]]
        self.validate_matrix(matrix)

        self.n_action_rows = len(self.matrix)
        self.n_action_cols = len(self.matrix[0])

        self.row_action_names = [str(elem) for elem in np.arange(0, self.n_action_rows)]
        self.col_action_names = [str(elem) for elem in np.arange(0, self.n_action_cols)]



    def validate_matrix(self, matrix):
        mat = np.array(matrix)
        shape = mat.shape
        if shape[0] > 0:
            if shape[1] > 0:
                subarray_lengths = [len(elem) for elem in matrix]
                if subarray_lengths.count(subarray_lengths[0]) == len(subarray_lengths):
                    if np.sum([type(tup) == tuple for elem in matrix for tup in elem]) == (shape[0] * shape[1]):
                        self.matrix = matrix
                    else:
                        raise Exception("Not all elements of the provided matrix are tuples.")
                else:
                    raise Exception("Not all subarrays have the same length.")
            else:
                raise Exception("The provided Matrix is 1-dimensional.")
        else:
            raise Exception("The provided matrix is empty.")

    def get_matrix(self):
        return self.matrix

    def __str__(self):
        displayMatrix = PrettyTable()
        first_row = [""] + self.col_action_names
        displayMatrix.field_names = first_row
        for row in range(0, self.n_action_rows):
            row = [self.row_action_names[row]] + self.matrix[row]
            displayMatrix.add_row(row)
        return str(displayMatrix)

    def assign_row_actions_names(self, name_array):
        '''*name_array* is an array of strings of characters, as many as there
        are row actions in the matrix.
        '''
        if len(name_array) == self.n_action_rows:
            self.row_action_names = name_array
        else:
            raise Exception("You did not provide the correct number of action names.")

    def assign_col_actions_names(self, name_array):
        '''*name_array* is an array of strings of characters, as many as there
        are column actions in the matrix.
        '''
        if len(name_array) == self.n_action_cols:
            self.col_action_names = name_array
        else:
            raise Exception("You did not provide the correct number of action names.")

    def strictlydominates(self, a1, a2):
        if len(a1) == len(a2):
            domCount = np.sum([elemA1 > elemA2 for elemA1, elemA2 in zip(a1,a2)])
            if len(a1) == domCount:
                return True
            else:
                return False
        else:
            raise Exception("The 2 actions you are comparing are of different lenghts.")

    def get_dominatedActions(self, playerMat):
        dominated = []
        for combo in permutations(np.arange(0, self.n_action_rows), 2):
            if self.strictlydominates(playerMat[combo[0]], playerMat[combo[1]]):
                dominated.append(combo[1])
                #print(dominated)
        return dominated

    def get_remaining(self, playerUtil):
        actionsToEliminate = self.get_dominatedActions(playerUtil)
        remaining = [elem for elem in np.arange(0,self.n_action_rows) if elem not in actionsToEliminate]
        return remaining

    def iesds(self, verbose=False):
        '''Apply IESDS (Iteratrive Elimination) on the current StrategicGame and returns the resulting
        StrategicGame. Leaves the original StrategicGame unchanged.'''
        displayMatrix = PrettyTable()

        rowPlayerUtil = [[tup[0] for tup in row] for row in self.matrix]
        remaining_rows = self.get_remaining(rowPlayerUtil)
        remaining_matrix = [self.matrix[rowID] for rowID in remaining_rows]

        colPlayerUtil = np.array([[tup[1] for tup in row] for row in remaining_matrix]).T.tolist()
        remaining_cols = self.get_remaining(colPlayerUtil)

        first_row = [""] + [self.col_action_names[id] for id in remaining_cols]
        displayMatrix.field_names = first_row
        for rowID in remaining_rows:
            row = [self.row_action_names[rowID]]
            for colID in remaining_cols:
                row.append(self.matrix[rowID][colID])
            displayMatrix.add_row(row)
        return str(displayMatrix)

    def find_Nash_profiles(self):
        '''return the list of Nash equilibria, as a list of row action /
           column action pairs (aidr, aidc).'''
        pass


def main():
    m0 = StrategicGame([[(10, 10), (0, 12)], [(12, 0), (1, 1)]])
    m0.assign_row_actions_names(["high", "low"])
    m0.assign_col_actions_names(["high", "low"])

    m1 = StrategicGame([[(0, 0), (1, 1), (2, 3)],
                        [(1, -1), (-1, 0), (-1, -2)],
                        [(0, 1), (1, 1), (5, 2)]])

    m2 = StrategicGame([[(3, 0), (4, 1), (2, 3)],
                        [(1, -1), (3, 0), (-1, -2)],
                        [(2, 1), (2, 1), (1, 2)]])

    for m in [m0, m1, m2]:
        print("\n==========================================\n")
        print(f"Before IESDS\n{m}")
        print(f"After IESDS\n{m.iesds(verbose=True)}")
        print(f"My game is still unchanged \n{m}")

    m3 = StrategicGame([[(0, 0), (-1, 1), (1, -1)],
                        [(1, -1), (0, 0), (-1, 1)],
                        [(-1, 1), (1, -1), (0, 0)]])
    m3.assign_row_actions_names(["rock", "paper", "scissors"])
    m3.assign_col_actions_names(["rock", "paper", "scissors"])

    m4 = StrategicGame([[(1, 4), (2, 4)],
                        [(1, 10), (4, 0)],
                        [(0, 10), (8, 11)]])
    for m in [m0, m1, m2, m3, m4]:
        print("Nash equilibria:", m.find_Nash_profiles())


    # pass


if __name__ == '__main__':
    main()
