#!/usr/bin/env python3
import numpy as np
from prettytable import PrettyTable
from itertools import permutations, product
'''An implementation of generic 2-player strategic games.

'''


class StrategicGame:

    def __init__(self, matrix):
        """*matrix* is a two-dimensional array of pairs of numbers
           (primitive numerical types). It should be non-empty, and
           have at least row and one column. All subarrays of
           *matrix* should have the same length."""

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
        for rowID in range(0, self.n_action_rows):
            row = [self.row_action_names[rowID]]
            for colID in range(0, self.n_action_cols):
                isNE = (rowID,colID) in self.find_Nash_profiles()
                isDS = (rowID,colID) in self.find_dominant_strategy_profiles()
                if isNE or isDS:
                    row.append(str(self.matrix[rowID][colID]) + " *")
                else:
                    row.append(self.matrix[rowID][colID])
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

# ____________________________ Dominance functions _____________________________________________________

    def strictlydominates(self, a1, a2):
        if len(a1) == len(a2):
            #using the fact that True = 1 and if sum of True(1) = len(a1) then all elements are larger
            domCount = np.sum(np.greater(a1,a2))
            if len(a1) == domCount:
                return True
            else:
                return False
        else:
            raise Exception("The 2 actions you are comparing are of different lenghts.")

    def stronglydominates(self, a1, a2):
        if len(a1) == len(a2):
            strictdomCount = np.sum(np.greater(a1,a2))
            strongdomCount = np.sum(np.greater_equal(a1,a2))
            if len(a1) == strongdomCount and strictdomCount > 0:
                return True
            else:
                return False
        else:
            raise Exception("The 2 actions you are comparing are of different lenghts.")

    def find_strongly_dom_action(self, r_c=("R", "C")):
        matrix = np.array(self.matrix)
        dom_actions = []
        if r_c == "R":
            if self.n_action_rows == 1:
                dom_actions.append(0)
            else:
                for combo in permutations(np.arange(0, self.n_action_rows), 2):
                    if self.stronglydominates(matrix[combo[0],:,0], matrix[combo[1],:,0]):
                        dom_actions.append(combo[0])
        elif r_c == "C":
            if self.n_action_cols == 1:
                dom_actions.append(0)
            else:
                for combo in permutations(np.arange(0, self.n_action_cols), 2):
                    if self.stronglydominates(matrix[:,combo[0],1], matrix[:,combo[1],1]):
                        dom_actions.append(combo[0])
        else:
            raise Exception("You need to indicate either R or C to find strongly dominant actions for either rows or columns")
        return dom_actions

    def find_dominant_strategy_profiles(self):
        # returns a list of dominant profiles as a list of row action/ column action ID pairs
        # a profile is a dominant profile if every player's action is a (strongly) dominant strategy
        dom_rows = self.find_strongly_dom_action("R")
        dom_cols = self.find_strongly_dom_action("C")
        all_combinations = [list(zip(each_permutation, dom_rows)) for each_permutation in permutations(dom_rows, len(dom_cols))]
        domsp = [item for sublist in all_combinations for item in sublist]
        return domsp

# _______________ Code segments needed for showing remaining matrix after IESDS and IENBR ________________

    def remainingMatrix(self, remaining_rows, remaining_cols):
        matrix = []
        for rowID in remaining_rows:
            row = []
            for colID in remaining_cols:
                row.append(self.matrix[rowID][colID])
            matrix.append(row)
        return matrix

    def getRemainingNames(self, remaining, r_c=("R", "C")):
        names = []
        if r_c == "R":
            for id in remaining:
                names.append(self.row_action_names[id])
        else:
            for id in remaining:
                names.append(self.col_action_names[id])
        return names

# ___________________ Code segments for IESDS ___________________________________________________________

    def removeDominatedRowsCols(self, matrix, verbose=False):
        dominated_rows = []
        for row_combos in permutations(np.arange(0, matrix.shape[0]), 2):
            if self.strictlydominates(matrix[row_combos[0], :, 0], matrix[row_combos[1], :, 0]):
                if verbose:
                    print("Row", self.row_action_names[row_combos[1]],"is dominated by row", self.row_action_names[row_combos[0]] )
                dominated_rows.append(row_combos[1])

        dominated_rows = list(set(dominated_rows)) #don't remove rows more often that are dominated by more than one other action
        for row in sorted(dominated_rows, reverse=True):
            matrix = np.delete(matrix, row, axis=0)

        dominated_cols = []
        for col_combos in permutations(np.arange(0, matrix.shape[1]), 2):
            if self.strictlydominates(matrix[:,col_combos[0],1], matrix[:,col_combos[1],1]):
                if verbose:
                    print("Column", self.col_action_names[col_combos[1]],"is dominated by column", self.col_action_names[col_combos[0]] )
                dominated_cols.append(col_combos[1])

        dominated_cols = list(set(dominated_cols)) #don't remove columns more often that are dominated by more than one other action
        for col in sorted(dominated_cols, reverse=True):
            matrix = np.delete(matrix, col, axis=1)

        return (matrix, dominated_rows, dominated_cols)

    def iesds(self, verbose=False):
        '''Apply IESDS (Iteratrive Elimination) on the current StrategicGame and returns the resulting
        StrategicGame. Leaves the original StrategicGame unchanged.'''

        print("Each dominated row or column is only removed once \n "
              "no matter how many other actions it is dominated by.")

        tmp_matrix = np.array(self.matrix)
        tmp_result = self.removeDominatedRowsCols(tmp_matrix, verbose)
        tmp_matrix_new = tmp_result[0]
        dominated_rows = tmp_result[1]
        dominated_cols = tmp_result[2]

        while tmp_matrix.shape != tmp_matrix_new.shape:
            tmp_matrix = tmp_matrix_new
            tmp_result = self.removeDominatedRowsCols(tmp_matrix)
            tmp_matrix_new = tmp_result[0]
            dominated_rows = dominated_rows + tmp_result[1]
            dominated_cols = dominated_cols + tmp_result[2]

        remaining_rows = [elem for elem in np.arange(0,self.n_action_rows) if elem not in dominated_rows]
        remaining_cols = [elem for elem in np.arange(0,self.n_action_cols) if elem not in dominated_cols]

        resulting_matrix = self.remainingMatrix(remaining_rows,remaining_cols)
        iesds_matrix = StrategicGame(resulting_matrix)
        iesds_matrix.assign_row_actions_names(self.getRemainingNames(remaining_rows, "R"))
        iesds_matrix.assign_col_actions_names(self.getRemainingNames(remaining_cols, "C"))
        return iesds_matrix

# __________________________ Code segments for IENBR ____________________________________________________

    def bestResponseToAction(self, matrix, actionID, r_c=("R", "C")):
        if r_c == "R":
            # the opponent is Row and takes action with actionID so we check what Cols best response to this is
            best_response = max(matrix[actionID, :, 1])
            max_index = np.where(matrix[actionID, :, 1] == best_response)
        elif r_c == "C":
            # the opponent is Column and takes action with actionID so we check what Rows best response to this is
            best_response = max(matrix[:, actionID, 0])
            max_index = np.where(matrix[:, actionID, 0]== best_response)
        else:
            raise Exception("The input of the function must specify whether an action is assumed by R or by C.")
        return max_index

    def neverBestResponse(self, matrix, r_c=("R", "C")):
        best_response = []
        if r_c == "R":
            for row in range(0,matrix.shape[0]):
                best_response += self.bestResponseToAction(matrix, row, r_c="R")
            neverBest = [id for id in range(0, matrix.shape[0]) if id not in best_response]
        elif r_c == "C":
            for col in range(0, matrix.shape[1]):
                best_response += self.bestResponseToAction(matrix, col, r_c="C")
            neverBest = [id for id in range(0, matrix.shape[1]) if id not in best_response]
        else:
            raise Exception("The input of the function must specify whether an action is assumed by R or by C.")
        return neverBest

    def ienbr(self, verbose=False):
        # non-destructively and iteratively eliminates never best responses
        tmp_matrix = np.array(self.matrix)
        tmp_matrix_old = np.array([])

        removed_rows = []
        removed_cols = []
        while tmp_matrix.shape != tmp_matrix_old.shape:
            tmp_matrix_old = tmp_matrix

            neverbest_row = self.neverBestResponse(tmp_matrix_old, r_c="R")
            removed_rows += neverbest_row
            for id in sorted(neverbest_row, reverse=True):
                if verbose:
                    print("Removing row ", self.row_action_names[id], "because it is a never best response.")
                tmp_matrix = np.delete(tmp_matrix, id, axis=0)

            neverbest_col = self.neverBestResponse(tmp_matrix_old, r_c="C")
            removed_cols += neverbest_col
            for id in sorted(neverbest_col, reverse=True):
                if verbose:
                    print("Removing column ", self.col_action_names[id], "because it is a never best response.")
                tmp_matrix = np.delete(tmp_matrix, id, axis=1)

        remaining_rows = [elem for elem in np.arange(0,tmp_matrix.shape[0]) if elem not in list(set(removed_rows))]
        remaining_cols = [elem for elem in np.arange(0,tmp_matrix.shape[1]) if elem not in list(set(removed_cols))]

        resulting_matrix = self.remainingMatrix(remaining_rows ,remaining_cols)
        ienbr_matrix = StrategicGame(resulting_matrix)
        ienbr_matrix.assign_row_actions_names(self.getRemainingNames(remaining_rows, "R"))
        ienbr_matrix.assign_col_actions_names(self.getRemainingNames(remaining_cols, "C"))
        return ienbr_matrix

# ___________________ Nash Profiles _____________________________________________________________________
#     def best_responseTo(self, opponentAction, r_c=("R", "C")):
#         #if other player plays action a1 what is the best response?
#         matrix = np.array(self.matrix)
#         if r_c == "R":
#             best_response = np.where(matrix[opponentAction,:,1] == np.max(matrix[opponentAction,:,1]))[0][0]
#         elif r_c == "C":
#             #print(np.where(matrix[:,opponentAction,0] == np.max(matrix[:,opponentAction,0]))[0][0])
#             best_response = np.where(matrix[:,opponentAction,0] == np.max(matrix[:,opponentAction,0]))[0][0]
#         else:
#             raise Exception("Select whether the opponent is Row R or Column C.")
#         return best_response

    def is_nash_equilibrium(self, rowID, colID):
        matrix = np.array(self.matrix)
        rowBest = not(any(matrix[:,colID,0] > matrix[rowID,colID,0]))
        colBest = not(any(matrix[rowID,:,1] > matrix[rowID,colID,1]))

        return (rowBest and colBest)

    def find_Nash_profiles(self):
        '''return the list of Nash equilibria, as a list of row action /
           column action pairs (aidr, aidc).'''
        nash_idPairs = []

        all_combinations = list(list(zip(np.arange(0,self.n_action_rows), element)) for element
                                in product(np.arange(0,self.n_action_cols), repeat = self.n_action_rows))
        combos = list(set([item for sublist in all_combinations for item in sublist]))

        for combo in combos:
            if self.is_nash_equilibrium(combo[0], combo[1]):
                nash_idPairs.append((combo[0], combo[1]))
        return nash_idPairs

# ____________ MAIN with example class instantiations ___________________________________________________

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

    print("\n==========================================\n")

    m4 = StrategicGame([[(1, 4), (2, 4)],
                        [(1, 10), (4, 0)],
                        [(0, 10), (8, 11)]])

    print(m4)

    for m in [m0, m1, m2, m3, m4]:
        print("Nash equilibria:", m.find_Nash_profiles())

    # print("\n==========================================\n")
    #
    # m5 = StrategicGame([[(2,1), (0,0)],
    #                     [(0,1),(2,0)],
    #                     [(1,1),(1,2)]])
    # print(f"Before IENBR\n{m}")
    # print(f"After IENBR\n{m5.ienbr(verbose=True)}")
    # print(f"My game is still unchanged \n{m}")

    # print("\n==========================================\n")
    #
    # print("Strongly dominant Strategy profiles")
    # g = StrategicGame([[(1, 5)],
    #                    [(0, 5)]])
    # print(g)
    # print(g.find_dominant_strategy_profiles())

if __name__ == '__main__':
    main()
