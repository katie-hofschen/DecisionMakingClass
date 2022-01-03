#!/usr/bin/env python3

"""Test units for the module decisionmatrix. """

from assignment2.decisionmatrix import DecisionMatrix
import unittest
from math import fsum

TESTS_TYPES = ['mc', 'na', 'pa', 'aa', 'ev', 'pir', 'mos']
UP_BOUND = 100  # max number of tests of one type


def IDENTITY(x):
    return x


class DecisionMatrixTestCase(unittest.TestCase):
    def setUp(self):
        pass

    # MATRIX CREATION
    def mc1(self):
        with self.assertRaises(Exception):
            m = DecisionMatrix([])

    def mc2(self):
        with self.assertRaises(Exception):
            m = DecisionMatrix([[], []])

    def mc3(self):
        with self.assertRaises(Exception):
            m = DecisionMatrix([["a", "b", 3], []])

    def mc4(self):
        with self.assertRaises(Exception):
            m = DecisionMatrix([[]])

    # NAMES ASSIGNMENT AND GET FROM NAMES
    def na1(self):
        with self.assertRaises(Exception):
            m = DecisionMatrix([[1, 2, 3]])
            m.assign_actions_names([2])

    def na2(self):
        with self.assertRaises(Exception):
            m = DecisionMatrix([[1, 3]])
            m.assign_states_names(["1", 2])

    def na3(self):
        with self.assertRaises(Exception):
            m = DecisionMatrix([[1, 3]])
            m.assign_states_names(["a", "a"])

    def na4(self):
        m = DecisionMatrix([[1], [2], [3]])
        m.assign_actions_names(["a", "b", "c"])
        self.assertEqual(m.get_action_from_name("a"), 0)
        self.assertEqual(m.get_action_from_name("b"), 1)
        self.assertEqual(m.get_action_from_name("c"), 2)

    # PROBABILITIES ASSIGNMENTS
    def pa1(self):
        with self.assertRaises(Exception):
            m = DecisionMatrix([[0, 1], [0, 1]])
            m.assign_states_probabilities([0.5, 0.48])

    def pa2(self):
        with self.assertRaises(Exception):
            m = DecisionMatrix([[0, 1], [0, 1]])
            m.assign_states_probabilities([0.5, 0.25, 0.25])

    # ADD ACTION
    def aa1(self):
        with self.assertRaises(Exception):
            m = DecisionMatrix([[1, 2, 3]])
            m.add_action([1, 2], "new")

    # add tests

    # EXPECTED VALUE
    def ev1(self):
        m = DecisionMatrix([[0, 2]])
        m.assign_actions_names(["0"])
        m.assign_values(IDENTITY)
        self.assertEqual(round(m.expected_value_of_action("0"), 2), 1.0)

    def ev2(self):
        m = DecisionMatrix([[0, 2], [1, 3]])
        m.assign_actions_names(["0", "1"])
        m.assign_values(IDENTITY)
        self.assertEqual(round(m.expected_value_of_action("0"), 2), 1.0)
        self.assertEqual(round(m.expected_value_of_action("1"), 2), 2.0)

    # PRINCIPLE OF INSUFFICIENT REASON
    def pir1(self):
        m = DecisionMatrix([[0, 2]])
        m.assign_states_probabilities([1/8, 7/8])
        m.principle_of_insufficient_reason()
        self.assertEqual(m.state_probability(1), 0.5)

    # MERGER OF STATES
    def mos1(self):
        m = DecisionMatrix([[2, 2, 3], [2, 2, 1], [2, 2, 3]])
        m.merger_of_states()
        with self.assertRaises(Exception):
            m.outcome(0, 2)

    def mos2(self):
        m = DecisionMatrix([[2, 2, 3], [2, 2, 1], [2, 2, 3]])
        exp_values1 = [m.expected_value(i) for i in range(m.num_actions())]
        m.merger_of_states()
        exp_values2 = [m.expected_value(i) for i in range(m.num_actions())]
        self.assertEqual(exp_values1, exp_values2)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    for t in TESTS_TYPES:
        for i in range(1, UP_BOUND):
            try:
                suite.addTest(DecisionMatrixTestCase(f'{t}{i}'))
            except ValueError:
                break

    runner = unittest.TextTestRunner()
    runner.run(suite)
