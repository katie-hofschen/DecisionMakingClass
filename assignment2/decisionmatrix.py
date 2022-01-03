#!/usr/bin/env python3

import numpy as np
from prettytable import PrettyTable
import pandas as pd
from itertools import combinations

'''An implementation of a generic matrix formalization.
What does it take to programmatically represent a decision matrix, and
how to programmatically extract information?
'''


class DecisionMatrix:

    def __init__(self, outcomesmatrix):

        self.isValid = self.isValidMatrix(outcomesmatrix)

        self.outcome_matrix = [[]]
        self.validateInput(outcomesmatrix)

        self.n_actions = 0
        self.n_states = 0

        self.num_actions()
        self.num_states()
        # Actions are identified with an integer id, starting from 0. States, too.
        # ^ Using position in array for this
        # By default, the names of actions and states are their id.
        self.action_names = [str(x) for x in range(0, self.n_actions)]
        self.state_names = [str(x) for x in range(0, self.n_states)]

        # By default, the states are equiprobable.
        self.state_probabilities = self.principle_of_insufficient_reason()

        # By default, all the outcomes have value 0.
        self.values = {}
        self.init_values()

    def init_values(self):
        for out in set([out for sub in self.outcome_matrix for out in sub]):
            self.values[str(out)] = 0

    def validateInput(self, inputMatrix):
        # Verify that it is a 2-D list. Also verifies that there is at least 1 outcome -> 1 action and 1 state
        # All sub-arrays of *outcomes-matrix* should have the same length.
        # because np.shape returns (length,) if the subarrays have different length this also automatically
        # filters out irregular lengths
        inputShape = np.shape(inputMatrix)
        twoDinput = len(inputShape) == 2
        if twoDinput:
            nonEmpty = inputShape[1] >= 1
            if nonEmpty:
                self.outcome_matrix = inputMatrix
        else:
            raise Exception("The outcome matrix you have provided has the wrong input. It should "
                       "contain at least 1 entry corresponding to the outcome of 1 action and 1 state. "
                       "Furthermore all subarrays should have the same length.")

    def isValidMatrix(self, inputMatrix):
        inputShape = np.shape(inputMatrix)
        twoDinput = len(inputShape) == 2
        if twoDinput:
            nonEmpty = inputShape[1] > 0
            return nonEmpty and twoDinput

    def __str__(self):
        # do something here; e.g., you can use prettytable module. Or
        # keep it simple for now.
        displayMatrix = PrettyTable()
        # displayMatrix.field_names = ["acts id", "act/states"] + self.state_names
        # displayMatrix.add_rows(row)
        if self.isValid:
            if self.n_states == 1 :
                row = np.concatenate([["acts id", "acts/states"] + [self.state_names[0] + " (" + str(1) + ")"]])
                displayMatrix.field_names = row
            else:
                row = np.concatenate([["acts id", "acts/states"] + [name + " (" + str(prob) + ")" for name, prob in zip(self.state_names, self.state_probabilities)]])
                displayMatrix.field_names = row
            for i in range(0, self.n_actions):
                stateOuts = []
                actions = [i, self.action_names[i]]
                for j in range(0, self.n_states):
                    stateOuts += [str(self.outcome_matrix[i][j]) + " (" + str(self.values[str(self.outcome_matrix[i][j])]) + ")"]
                row = np.concatenate([actions + stateOuts ])
                displayMatrix.add_row(row)
            return str(displayMatrix)
        else:
            raise Exception("Error: Please provide the correct input to obtain a decision matrix.")

    def expected_value_bests(self):
        '''return the list of actions id's that maximize
        the expected value.'''
        expectationList = []
        for i in range(0, self.n_actions):
            expectationList.append(self.expected_value(i))
        return [x for x,val in enumerate(expectationList) if val == np.max(expectationList)]


    def num_actions(self):
        """Returns the number of actions."""
        if len(self.outcome_matrix) > 0:
            self.n_actions = len(self.outcome_matrix)
            return self.n_actions
        else:
            raise Exception("Unable to assign number of actions.")

    def num_states(self):
        """Returns the number of states."""
        if len(self.outcome_matrix[0]) > 0:
            self.n_states = len(self.outcome_matrix[0])
            return self.n_states
        else:
            raise Exception("Unable to assign number of states")

    def assign_actions_names(self, name_array):
        """*name_array* is an array of strings of characters, as many as there
        are actions in the matrix. They must be unique."""
        isString = set([type(name) for name in name_array]).pop() == str
        if len(name_array) == len(np.unique(name_array)) and isString:
            if self.n_actions == len(name_array):
                self.action_names = name_array
            else:
                raise Exception("You did not provide exactly ", self.n_actions, " action names.")
        else:
            raise Exception("The action names were not unique or not provided as strings, please try again.")

    def assign_states_names(self, name_array):
        """*name_array* is an array of strings of characters, as many as there
        are states in the matrix. They must be unique.
        """
        isStringList = [type(name) == str for name in name_array]
        isString = np.sum([type(name) == str for name in name_array]) == len(name_array)
        if len(name_array) == len(np.unique(name_array)) and isString and self.n_states == len(name_array):
                self.state_names = name_array
        else:
            raise Exception("You did not provide exactly ", self.n_states, " state names. ",
                            "The State names were not unique or not provided as strings, please try again.")

    def assign_states_probabilities(self, prob_array):
        """*prob_array* is an array of floats between 0 and 1, as many as
        there are states in the matrix. They sum up to 1. """
        if len(prob_array) == self.n_states:
            if np.sum(prob_array) == 1:
                self.state_probabilities = prob_array
            else:
                raise Exception("The probabilities do not add up to 1. The probabilities remain at the default.")
        else:
            raise Exception("You did not provide exactly ", self.n_states, " state probabilities. "
                                                                 "The probabilities remain at the default.")

    def action_name(self, action):
        """get human readable action name from action identifier *action*"""
        if action <= self.n_actions and type(action) == int:
            return self.action_names[action]
        else:
            raise Exception("The action id must lie between 0 and ", self.n_actions - 1)

    def state_name(self, state):
        """get human readable state name from state identifier *state* """
        if state <= self.n_states and type(state) == int:
            return self.state_names[state]
        else:
            raise Exception("The state id must lie between 0 and ", self.n_states - 1)

    def state_probability(self, state):
        """get state probability from state identifier *state*"""
        if state <= len(self.state_probabilities) and type(state) == int:
            return self.state_probabilities[state]
        else:
            raise Exception("The state id must lie between 0 and ", self.n_states - 1)

    def add_action(self, outcomes_array, action_name):
        """add an action to the list of actions, with first available id, and
        name *action_name*. *outcomes_array* is a list of outcomes, as
        many as there are states, and *action_name* is a string of
        characters. """
        if len(outcomes_array) == self.n_states and type(action_name) == str:
            self.action_names.append(action_name)
            self.outcome_matrix.append(outcomes_array)
            self.num_actions()
        else:
            raise Exception("The outcome array you would like to add must have ", self.n_states, " elements. ",
                  "And the action name must be provided as a string of characters. Please try again.")

    def outcome(self, action, state):
        """get the outcome of action with identifier *action* and state with
        identifier *state* """
        if state <= self.n_states and action <= self.n_actions and type(state) == int and type(action) == int:
            return self.outcome_matrix[action][state]
        else:
            raise Exception("The indices you have provided are likely out of bounds.")

    def get_action_from_name(self, action_name):
        """get action id from its name *action_name*"""
        if action_name in self.action_names:
            action_id = [i for i,x in enumerate(self.action_names) if x == action_name][0]
            return action_id
        else:
            raise Exception("The provided action name doesn't seem to exist. These are all action names ", self.action_names)

    def get_state_from_name(self, state_name):
        """get state identifier from its name *state_name*"""
        if state_name in self.state_names:
            return [i for i, x in enumerate(self.state_names) if x == state_name][0]
        else:
            raise Exception("The provided state name doesn't seem to exist. These are all state names ", self.state_names)

    def print_howtoget(self, outcome):
        """print the actions names that can yield *outcome* name, and in which states"""
        if outcome in set([out for sub in self.outcome_matrix for out in sub]):
            indices = [(i, row.index(outcome)) for i, row in enumerate(self.outcome_matrix) if outcome in row][0]
            print("Outcome: ", outcome, "\nAction name: ", self.action_names[indices[0]], "\nState name:", self.state_names[indices[1]], "\n")
        else:
            raise Exception("The outcome you have entered may not be in the outcome matrix. Here are all possible outcomes: ", self.outcome_matrix)

    def assign_values(self, fvalue):
        """assign numerical values to outcomes names, as specified in
        the function *fvalue* from nominal outcomes to numerical values.
         m.assign_values(value_fun({"$0": 0, "$10K": 10000, "$5000": 5000, "$6000": 6000}))"""
        try:
            for out in set([out for sub in self.outcome_matrix for out in sub]):
                self.values[str(out)] = fvalue(out)
        except:
            raise Exception("The input of this function is expected as a Lambda function. Also verify that you have named the outcomes correctly.")

    def outcome_value(self, action, state):
        """get the value of the outcome of action with identifier *action* done state with identifier *state*"""
        try:
            return self.values[self.outcome_matrix[action][state]]
        except:
            raise Exception("The action and state id need to be provided as numbers between 0 and ", self.n_actions, "/ ", self.n_states, " respectively.")

    def expected_value(self, action):
        """the expected value of the action identified by *action* """
        if action <= self.n_actions and type(action) == int:
            valuesPerAction = [self.values[str(out)] for out in self.outcome_matrix[action]]
            expectedValue = [a * b for a,b in zip(valuesPerAction, self.state_probabilities)]
            return sum(expectedValue)
        else:
            raise Exception("The action id needs to be provided as numbers between 0 and ", self.n_actions, ".")

    def expected_value_of_action(self, action_name):
        """the expected value of the action name *action_name* """
        return self.expected_value(self.get_action_from_name(action_name))

    def principle_of_insufficient_reason(self):
        """assign equal probabilies to all states"""
        if self.n_states > 0:
            self.state_probabilities = [np.around((1 / self.n_states), 2)] * self.n_states
            return self.state_probabilities
        else:
            raise Exception("Error: Division by 0")

    def tuple_intersection(self, m_list):
        s = m_list
        for i, tup1 in enumerate(m_list) :
            for j, tup2 in enumerate(m_list[i+1:], i+1):
                if tup1 & tup2:
                    s[i]=tup1.union(m_list.pop(j))
                    return self.tuple_intersection(m_list)
        return m_list

    def merger_of_states(self):
        """merge all states that yield exactly the same outcomes for every
        action. The probabilities of the merger is the sum of the
        merged states. The name of the merger of {s1, s2, ...} is "s1,
        s2, ..."

        """
        #self.updateMatrix()
        #using pandas dataframe to find same columns
        matrix_df = pd.DataFrame(self.outcome_matrix)
        sameTuples = [(i,j) for i,j in combinations(matrix_df, 2) if matrix_df[i].equals(matrix_df[j])]
        s = [set(tup) for tup in sameTuples if tup]
        intersection = self.tuple_intersection(s)

        duplicateColumns = [list(set) for set in intersection]
        colToRemove = sorted([id for sub in duplicateColumns for id in sub[1:]], reverse=True)

        # Removing the duplicate columns from highest to lowest to avoid index problems.
        for colID in colToRemove:
            self.outcome_matrix = np.delete(self.outcome_matrix, colID, axis=1)

        for sub in duplicateColumns:
            newStateName = ", ".join([self.state_names[id] for id in sub])
            newProb = np.round(np.sum([self.state_probabilities[id] for id in sub]),2)
            self.state_names[sub[0]] = newStateName
            self.state_probabilities[sub[0]] = newProb

        for id in colToRemove:
            self.state_names.pop(id)
            self.state_probabilities.pop(id)

        self.num_states()

def main():
    def value_fun(value_dict):
        return lambda x: value_dict[x]

    # m = DecisionMatrix([[1,2],[2,3,4]])
    # print(m, '\n')

    m = DecisionMatrix([["no house and $100,000", "house and $0"],
                        ["no house and $100", "house and $100"]])
    m.assign_actions_names(["insurance", "no insurance"])
    m.assign_states_names(["fire", "no fire"])
    m.assign_states_probabilities([0.1, 0.9])
    print(m, '\n')
    m.print_howtoget("house and $100")
    m.assign_values(value_fun({"no house and $100,000": 1,
                               "house and $0": 4,
                               "no house and $100": -100,
                               "house and $100": 10}))
    print("The expected value of taking insurance is {}."
          .format(m.expected_value_of_action("insurance")))
    print("The expected value of not taking insurance is {}."
          .format(m.expected_value_of_action("no insurance")))

    print('\n\n')
    print("____________________________________________________________")
    print('\n\n')

    m = DecisionMatrix([
        ["$0", "$10K", "$10K"],
        ["$5000", "$6000", "$6000"]])
    m.assign_states_names(["P", "LA", "NY"])
    m.assign_actions_names(["Stay", "Go to Paris"])
    m.assign_values(value_fun({"$0": 0, "$10K": 10000,
                               "$5000": 5000, "$6000": 6000}))
    print("Merger of states, and principle of insufficient reason")
    m.merger_of_states()
    m.principle_of_insufficient_reason()
    print(m, '\n')
    print("The expected value of staying is {}."
          .format(m.expected_value_of_action("Stay")))
    print("The expected value of going to Paris is {}."
          .format(m.expected_value_of_action("Go to Paris")))
    print("The best expected value is for actions with ids {}."
          .format(m.expected_value_bests()))

    print('\n\n')
    print("____________________________________________________________")
    print('\n\n')

    m = DecisionMatrix([
        ["$0", "$10K", "$10K"],
        ["$5000", "$6000", "$6000"]])
    m.assign_states_names(["P", "LA", "NY"])
    m.assign_actions_names(["Stay", "Go to Paris"])
    m.assign_values(value_fun({"$0": 0, "$10K": 10000,
                               "$5000": 5000, "$6000": 6000}))
    print("Principle of insufficient reason, and merger of states")
    m.principle_of_insufficient_reason()
    m.merger_of_states()
    print(m, '\n')
    print("The expected value of staying is {}."
          .format(m.expected_value_of_action("Stay")))
    print("The expected value of going to Paris is {}."
          .format(m.expected_value_of_action("Go to Paris")))
    print("The best expected value is for actions with ids {}."
          .format(m.expected_value_bests()))

    print('\n\n')
    print("____________________________________________________________")
    print('\n\n')

    m = DecisionMatrix([
        ['$0', '$10K', '$10K', '$10K', '$0', '$3'],
        ['$5000', '$6000', '$6000', '$6000', '$5000', '$4']])
    m.assign_states_names(['P', 'LA', 'NY', 'Test', "test2", "Ano"])
    m.assign_states_probabilities([0.1, 0.1, 0.2, 0.3, 0.1, 0.2])
    m.assign_actions_names(["Stay", "Go to Paris"])
    m.assign_values(value_fun({"$0": 0, "$10K": 10000, '$3':3, '$4':4,
                               "$5000": 5000, "$6000": 6000}))
    print("Principle of insufficient reason, and merger of states")
    m.principle_of_insufficient_reason()
    m.merger_of_states()
    print(m, '\n')
    print("The expected value of staying is {}."
          .format(m.expected_value_of_action("Stay")))
    print("The expected value of going to Paris is {}."
          .format(m.expected_value_of_action("Go to Paris")))
    print("The best expected value is for actions with ids {}."
          .format(m.expected_value_bests()))

    print('\n\n')



if __name__ == '__main__':
    main()
