#!/usr/bin/env python3

'''An implementation of a generic matrix formalization of problems of
decisions under ignorance, ***that exploits the module decisionmatrix***.

interactive_choose_rule() is an interactive method to help the user decide
which rule to use among Maximin, Optimism-Pessimism, Minimax regret,
and Insufficient reason.

All these rules and others are implemented, to decide which actions
are best under them.

'''

from assignment2.decisionmatrix import DecisionMatrix
import numpy as np

rule_names = ["Maximin", "Optimism-Pessimism", "Minimax Regret", "Insufficient Reason"]


def interactive_choose_rule():
    ''' Help user to choose a decision rule among
        Maximin(Wald), Optimism-Pessimism(Hurwicz), MinimaxRegret(Savage), and Insufficient Reason(Laplace.)'''
    axiomsBool = valid_input("Which form of assistance in choosing a decision rule do you prefer? \n"
                             "0) Intuitive: goal oriented questions (0) \n"
                             "1) Formal: selection of Milner's principles (1) \n"
                             "Respond with the number of your choice.\n", [0, 1])
    if axiomsBool == 1:
        return axiom_based_choice()
    else:
        return intuitive_choice()


def intuitive_choice():
    result = ""
    print("\nYou have chosen the intuitive approach to selecting a decision rule. \n"
          "Please answer the following questions to generate a recommendation.\n")

    valueType = valid_input("Should the values of the outcomes be considered as:\n"
                            "Simple ranking between values (Ordinal) (0), \n"
                            "Numerical values (Interval) (1)\n", [0, 1])
    if valueType == 1:
        knowProbs = valid_input("Do you know the probability of states or an estimation of them?\n"
                            "No (0), Yes (1)\n", [0, 1])
        if knowProbs == 1:
            attitudelossI = valid_input("How do you feel about a loss considering this decision?\n"
                                       "Not so concerned (0),  Worried (1)\n", [0, 1])
            if attitudelossI == 0:
                attitudeRegret = valid_input("How important is the consideration of possible regret in this decision?\n"
                                                 "Not very (0),  Important (1)\n", [0, 1])
                if attitudeRegret == 1:
                    print("\nRecommendation:\nGiven your concerns you could use the {} rule to help you with your decision.".format("Minimax Regret"))
                else: # not so concerned about regret or loss
                    print("\nRecommendation:\nGiven your concerns you could use the {} rule to help you with your decision.".format("Optimism-Pessimism(alpha > 0.5) (more optimistic)"))
            else: #Worried if loss
                print("\nRecommendation:\nGiven your concerns you could use the {} rule to help you with your decision.".format("Optimism-Pessimism(alpha < 0.5) (more pessimistic)"))
        else: # Dont know the probs of the states
            print("\nRecommendation:\nGiven your concerns you could use the {} rule to help you with your decision.".format("Insufficient Reason"))
    else: # if values are to be considered as simple ranking
        attitudelossO = valid_input("How do you feel about a loss considering this decision?\n"
                                   "Not so concerned (0),  Worried (1)\n", [0, 1])
        if attitudelossO == 1: # Is more risk averse
            print("\nRecommendation:\nGiven your concerns you could use the {} rules to help you with your decision.".format("Maximin or Leximin"))
        else: # Is more of a gambler
            print("\nRecommendation:\nGiven your concerns you could use the {} rules to help you with your decision.".format("Maximax or Strongly Dominates"))


def axiom_based_choice():
    print("You have chosen to use Milner's principles to help you pick a decision rule. \n"
          "Please answer the following questions by responding with the number that signifies your choice.\n")

    irrelevant_a = valid_input("\nIrrelevant alternatives: \n"
                               "The ordering between old alternatives does not change if new alternatives are added to the decision problem. \n"
                               "No (0), Yes (1), Indifferent (2)", [0, 1, 2])
    col_lin = valid_input("\nColumn linearity: \n"
                          "The ordering of the alternatives does not change if a constant is added to a column. \n"
                          "No (0), Yes (1), Indifferent (2)", [0, 1, 2])
    col_dup = valid_input("\nColumn duplication: \n"
                          "The ordering of the alternatives does not change if an identical state (column) is added.\n"
                          "No (0), Yes (1), Indifferent (2)", [0, 1, 2])
    randomiz = valid_input("\nRandomization: \n"
                           "If two acts are equally valuable, then every randomization between the two acts is also equally valuable.\n"
                           "No (0), Yes (1), Indifferent (2)", [0, 1, 2])
    convex = valid_input("\nConvexity: \n"
                         "The set of optimal alternatives is convex; "
                         "if two actions are more valuable than a third one, then so is their randomization. \n"
                         "No (0), Yes (1), Indifferent (2)", [0, 1, 2])

    responses = [irrelevant_a, col_lin, col_dup, randomiz, convex]
    print("responses", responses)
    scores = get_scores(responses)
    print(scores)
    choiceIDs = [x for x, val in enumerate(scores) if val == np.max(scores)]
    names = [rule_names[id] for id in choiceIDs]
    print("Given your concerns you could use the following rule/s {}.".format(", ".join(names)))
    return


def valid_input(text, responsOptions):
    if type(text) == str:
        response = input(text)
        if response == '':
            print("\nYour response should not be empty. Please try again:")
            return valid_input(text, responsOptions)
        else:
            if int(response) in responsOptions:
                return int(response)
            else:
                print("\nYour response should be one of these values", responsOptions, "but your response was",
                      response,
                      "\nPlease try again:")
                return valid_input(text, responsOptions)

# axiom_based_choice()
def get_scores(responses):
    scores = [0, 0, 0, 0]

    rules = [[1, 0, 1, 0, 1],
             [1, 0, 1, 0, 0],
             [0, 1, 1, 0, 1],
             [1, 1, 0, 1, 1]]

    for rule in range(0, 4):
        for ax in range(0, 5):
            if responses[ax] == rules[rule][ax]:
                scores[rule] += 2
            elif responses[ax] == 2: # In case the user selected indifferent
                scores[rule] += 2
    return scores


# __________________________________________________________________________________________________
# __________________________________________________________________________________________________


class IgnoranceMatrix(DecisionMatrix):

    def add_randomized_action(self, actid_array, actid_probability):
        '''Intuition:   Chose an act with a probability distribution such as a coin toss etc.
                        May make sense when the decision is faced many times.
            Limitations: Randomizing actions doesn't make sense when you are likely to only face the decision once
                        But when facing decision many times, it maybe makes more sense to chose 1 action
                        and adjust behavior as one learns more about the relative frequencies of the states
            Function:   add a randomized action to the list of actions, with first available id,
                        and name rand(*actid_array*, *actid_probability*).
                        *actid_array* is a list of action id's,
                        and *actid_probability* is a distribution of probability over these actions id's.

        '''
        notRandActionsIds = [x for x, name in enumerate(self.action_names) if name[:4] != "rand"]
        correctNumActions = len(actid_array) == len(notRandActionsIds)
        matchingLength = len(actid_array) == len(actid_probability)
        probSumOne = np.sum(actid_probability) == 1
        positiveProbs = np.sum([x > 0 for x in actid_probability]) == len(actid_probability)

        if correctNumActions and matchingLength and probSumOne and positiveProbs:
            self.action_names.append("rand([" + "],[".join(
                [", ".join([str(id) for id in actid_array]), ", ".join([str(p) for p in actid_probability])]) + "])")
            outcome_array = []
            for i in range(0, self.n_states):
                statesum = 0
                for act in notRandActionsIds:
                    statesum += self.values[str(self.outcome_matrix[act][i])] * actid_probability[act]
                outcome_array.append(np.round(statesum, 2))
            self.outcome_matrix.append(outcome_array)

            self.num_actions()

            # add the randomized values to the value dictionary
            for out in outcome_array:
                self.values[str(out)] = out
        else:
            raise Exception(
                "The probabilities either don't sum up to 1 or the 2 provided arrays have a different length or don't correspond to the correct number of actions.")

    def weakly_dominates(self, aid1, aid2):
        '''return True if action aid1 weakly dominates action aid2,
           False otherwise.'''
        sameLenght = len(self.outcome_matrix[aid1]) == len(self.outcome_matrix[aid2])
        idsExist = 0 <= aid1 < self.n_actions and 0 <= aid2 < self.n_actions
        if sameLenght and idsExist and len(self.outcome_matrix[aid2]) > 0:
            weakDominance = True
            valAction1 = [self.values[str(out)] for out in self.outcome_matrix[aid1]]
            valAction2 = [self.values[str(out)] for out in self.outcome_matrix[aid2]]

            for val1, val2 in zip(valAction1, valAction2):
                weakDominance = weakDominance and val1 >= val2
            return weakDominance
        else:
            raise Exception("Unexpected result {} .".format(self.outcome_matrix))

    def strongly_dominates(self, aid1, aid2):
        """ Intuition:  Action a is at least as good as action b
                        and at least 1 state of action a strictly dominates the same state of action b
            Function :  return True if action aid1 strongly dominates action aid2,
                        False otherwise."""
        sameLenght = len(self.outcome_matrix[aid1]) == len(self.outcome_matrix[aid2])
        idsExist = 0 <= aid1 < self.n_actions and 0 <= aid2 < self.n_actions

        if sameLenght and idsExist and len(self.outcome_matrix[aid2]) > 0:
            dom = 0
            valAction1 = [self.values[str(out)] for out in self.outcome_matrix[aid1]]
            valAction2 = [self.values[str(out)] for out in self.outcome_matrix[aid2]]

            for val1, val2 in zip(valAction1, valAction2):
                if val1 > val2:
                    dom += 1
            return (dom > 0 and self.weakly_dominates(aid1, aid2))
        else:
            raise Exception("Unexpected result {} .".format(self.outcome_matrix))

    def dominance_bests(self):
        """Intuition: it doesn't make sense to chose acts that are strongly dominated by other acts
                      also better action is not influenced by state probabilities since we are
                      at least as well off as with alternative actions
            Limitation: This rule however can not distinguish between actions that don't dominate each other
                        To chose between the remaining actions you could use another decision rule.
            Function: return the list of actions id's that are best for dominance (non (strongly) dominated)."""
        try:
            dominated = []
            notdominated = []
            ids = np.arange(self.n_actions)
            for i in range(0, self.n_actions):
                for j in range(0, self.n_actions):
                    if i != j:
                        if not (self.strongly_dominates(i, j)):
                            notdominated.append(j)
                        else:
                            dominated.append(j)
            dom_best = set(notdominated).symmetric_difference(set(dominated))
            return list(dom_best)
        except:
            raise Exception("Unexpected result {} .".format(self.outcome_matrix))

    def maximin_bests(self):
        """Intuition:   For each action select the worst possible outcome value from all states
                        and then return the action that has the best worst case
                        This way you can minimize your losses but you may also not gain very much.
                        Sensible for risk-averse scenarios
            Limitation: Because comparison on ordinal scale if you can chose between a1: [1,2] and a2: [1, 100]
                        Minimax will return that it is indifferent between a1 and a2
            Function:   return the list of actions id's that are best for maximin."""
        maximinCol = []
        for i in range(0, len(self.outcome_matrix)):
            actionVals = [self.values[str(out)] for out in self.outcome_matrix[i]]
            maximinCol.append(np.min(actionVals))
        return [x for x, val in enumerate(maximinCol) if val == np.max(maximinCol)]

    def maximax_bests(self):
        """Intuition:   For each action select the best possible outcome value from all states
                        and then return the action that has the best best case
                        This way you can maximize your possible gains but you may also loose a lot."""
        maximaxCol = []
        for i in range(0, len(self.outcome_matrix)):
            actionVals = [self.values[str(out)] for out in self.outcome_matrix[i]]
            maximaxCol.append(np.max(actionVals))
        return [x for x, val in enumerate(maximaxCol) if val == np.max(maximaxCol)]

    def leximin_bests(self):
        """ Intuition:  if the worst outcomes are equal, compare 2nd worst, then 3rd worst and so on
                        until you can find an action that has a better xth worst case outcome.
            Limitation: Since comparison on ordinal scale choosing decisions such as
                        sacrificing 0.1 to gain 100 are not recommended with this method
                        Aka the difference between the values does not matter and for these 2 decision rules
                        it might make more sense to transform the outcomes into a simple ordinal scale (1,2,3,4...)
            Function:   return the list of actions id's that are best for leximin."""
        try:
            sortedValues = [sorted([self.values[str(out)] for out in self.outcome_matrix[i]]) for i in
                            np.arange(0, self.n_actions)]
            maxActions = np.arange(0, self.n_actions)
            for col in range(0, self.n_states):
                column = [row[col] for row in sortedValues]
                column = [elem - np.max(column) if x not in maxActions else elem for x, elem in enumerate(column)]
                if column.count(max(column)) == 1:
                    return [x for x, val in enumerate(column) if val == np.max(column)]
                else:
                    maxActions = [x for x, val in enumerate(column) if val == np.max(column)]
        except:
            raise Exception("Unexpected result {} .".format(self.outcome_matrix))

    def optimism_pessimism_bests(self, alpha):
        """Intuition:   Rather than being purely pessimistic(Maximin) or purely optimistic(Maximax)
                        Balance the level of optimisim and pessimism with an alpha (0-1)
                        - Requires value to be measured on an interval scale
            Limitations: Only the best and worst case values are considered,
                        disregarding all values of an action that lie in between these 2
                        If the ratio between numbers matters, O-P rule is not well suited
                        -> idea: adjust interval scale so that the ratio seems less important eg adding 10000
            Function:   return the list of actions id's that are best for
           *alpha*-optimism-pessimism."""
        if 0 <= alpha <= 1:
            opCol = []
            for i in range(0, len(self.outcome_matrix)):
                actionVals = [self.values[str(out)] for out in self.outcome_matrix[i]]
                np.min(actionVals)
                opBalance = alpha * np.max(actionVals) + (1 - alpha) * np.min(actionVals)
                opCol.append(np.round(opBalance, 2))
            return [x for x, val in enumerate(opCol) if val == np.max(opCol)]
        else:
            raise Exception("Unexpected result {} .".format(self.outcome_matrix))

    def get_regret_matrix(self):
        """Intuition:   Regret = best value of state - values of action,state for every action of this state
                        The closer to 0 the less regret you will feel.
           Function:    return the regret matrix"""
        try:
            regret_matrix = [[self.values[str(out)] for out in self.outcome_matrix[i]] for i in
                             np.arange(0, self.n_actions)]
            bestValuesPerS = []
            for col in range(0, self.n_states):
                column = [row[col] for row in regret_matrix]
                bestValuesPerS.append(np.max(column))
            return [list(np.subtract(bestValuesPerS, row)) for row in regret_matrix]
        except:
            raise Exception("Unexpected result {} .".format(self.outcome_matrix))

    def minimax_regret_bests(self):
        """Intuition:   Minimize the maximum amount of regret.
                        Maybe good when you know that you can afford to lose a little
                        Eg. like the decision of participating in cryptocurrencies when
                        they first started and the possible regret you might feel today of not having invested earlier.
            Limitation: When an action is added it can change the ordering between previously good actions
                        even if the added action is worse than the other actions.
                        Sensitive to how actions are defined or changed
                        (Disputed whether this sensitivity is problematic or not)
            Function:   return the list of actions id's that are best for minimax regret."""
        try:
            minimax = []
            regret_matrix = self.get_regret_matrix()
            for i in range(0, len(regret_matrix)):
                regrets = [row for row in regret_matrix[i]]
                minimax.append(np.max(regrets))
            return [x for x, val in enumerate(minimax) if val == np.min(minimax)]
        except:
            raise Exception("Unexpected result {} .".format(self.outcome_matrix))

    def insufficient_reason_bests(self):
        """Intuition:   Don't know probabilities of states? Assume all states are equiprobable.
                        Decision under Ignorance -> decision under risk
                        -> Maximise expected value
            Limitation: Very Sensitive to definition of states or changes thereof
                        Can you argue that you have found the one correct set of states?
            Function:   return the list of actions id's that are best for insufficient reason."""
        try:
            maxExpectationList = []
            probabilities = [np.round(1 / self.n_states, 2)] * self.n_states
            for row in self.outcome_matrix:
                row = [self.values[str(out)] for out in row]
                expectedValues = np.multiply(row, probabilities)
                maxExpectationList.append(np.max(np.round(expectedValues, 2)))
            ids = [x for x, val in enumerate(maxExpectationList) if val == np.max(maxExpectationList)]
            return ids
        except:
            raise Exception("Unexpected result {} .".format(self.outcome_matrix))


def main():
    def IDENTITY(x):
        return x

    m = IgnoranceMatrix([["boring", "great"], ["great", "annoying"]])
    m.assign_states_names(["not windy", "windy"])
    m.assign_actions_names(["fly kite", "play ping pong"])
    m.assign_values(lambda x: {"boring": 0, "great": 2, "annoying": -1}[x])
    print(m, '\n')
    print("REGRETS\n", m.get_regret_matrix())
    print("Dominance", m.dominance_bests())
    print("Maximin", m.maximin_bests())
    print("Leximin", m.leximin_bests())
    print("0.25-Optimism-Pessimism", m.optimism_pessimism_bests(0.25))
    print("0.8-Optimism-Pessimism", m.optimism_pessimism_bests(0.8))
    print("Insufficient reason", m.insufficient_reason_bests())
    print("Minimax regret", m.minimax_regret_bests())

    print("_________________________________________________________________________________________")
    print('\n\n')

    m = IgnoranceMatrix([[2, 1, 0], [0, 1, 3]])
    m.assign_states_names(["sunny", "cloudy", "rain"])
    m.assign_actions_names(["go out", "play videogames"])
    m.assign_values(IDENTITY)
    print(m, '\n')

    m.add_randomized_action([0, 1], [0.3, 0.7])
    print(m, '\n')

    m.add_randomized_action([1, 2], [0.5, 0.5])
    print(m, '\n')

    print("REGRETS\n", m.get_regret_matrix())
    print("Dominance", m.dominance_bests())
    print("Maximin", m.maximin_bests())
    print("Leximin", m.leximin_bests())
    print("0.25-Optimism-Pessimism", m.optimism_pessimism_bests(0.25))
    print("0.8-Optimism-Pessimism", m.optimism_pessimism_bests(0.8))
    print("Insufficient reason", m.insufficient_reason_bests())
    print("Minimax regret", m.minimax_regret_bests())

    print("_________________________________________________________________________________________")
    print('\n\n')

    m = IgnoranceMatrix([[2, 1, 0], [0, 1, 3], [-1, 3, 5], [1, 1, 1]])
    m.assign_values(IDENTITY)
    print(m)
    print("REGRETS\n", m.get_regret_matrix())
    print("Dominance", m.dominance_bests())
    print("Maximin", m.maximin_bests())
    print("Leximin", m.leximin_bests())
    print("0.25-Optimism-Pessimism", m.optimism_pessimism_bests(0.25))
    print("0.8-Optimism-Pessimism", m.optimism_pessimism_bests(0.8))
    print("Insufficient reason", m.insufficient_reason_bests())
    print("Minimax regret", m.minimax_regret_bests())

    print("_________________________________________________________________________________________")
    print('\n\n')

    m = IgnoranceMatrix([[2, 1, 0], [0, 1, 3], [0, 3, 5], [0, 3, 6]])
    m.assign_values(IDENTITY)
    print(m)
    print("REGRETS\n", m.get_regret_matrix())
    print("Dominance", m.dominance_bests())
    print("Maximin", m.maximin_bests())
    print("Leximin", m.leximin_bests())
    print("0.25-Optimism-Pessimism", m.optimism_pessimism_bests(0.25))
    print("0.8-Optimism-Pessimism", m.optimism_pessimism_bests(0.8))
    print("Insufficient reason", m.insufficient_reason_bests())
    print("Minimax regret", m.minimax_regret_bests())

    print("_________________________________________________________________________________________")
    print('\n\n')

    m = IgnoranceMatrix([[2, 1, 0], [0, 1, -1], [0, -1, 0], [0, 3, 6]])
    m.assign_values(IDENTITY)
    print(m)
    print("REGRETS\n", m.get_regret_matrix())
    print("Dominance", m.dominance_bests())
    print("Maximin", m.maximin_bests())
    print("Leximin", m.leximin_bests())
    print("0.25-Optimism-Pessimism", m.optimism_pessimism_bests(0.25))
    print("0.8-Optimism-Pessimism", m.optimism_pessimism_bests(0.8))
    print("Insufficient reason", m.insufficient_reason_bests())
    print("Minimax regret", m.minimax_regret_bests())


if __name__ == '__main__':
    main()
