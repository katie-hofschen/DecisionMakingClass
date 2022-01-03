#!/usr/bin/env python3

'''Test units for the module decisionignorance dedicated to the
formalization of problems decisions under ignorance and finding
actions under a variety of decision rules.

These tests units focus on some corner cases of matrix creations, and
then on the actual correctness of the implementations of the decision
rules.

'''

from assignment2.decisionignorance import IgnoranceMatrix
import unittest

TESTS_TYPES = ['mc', 'ara', 'wd', 'sd', 'db', 'mb', 'lb', 'opb', 'mr', 'ir']
UP_BOUND = 100  # max number of tests of one type


def IDENTITY(x):
    return x


class DecisionIgnoranceTestCase(unittest.TestCase):
    def setUp(self):
        pass

    # MATRIX CREATION
    def mc1(self):
        with self.assertRaises(Exception):
            m = IgnoranceMatrix([[1, 3], ['h', 3], [1, 1, 1]])

    # ADD RANDOMIZED ACTION
    def ara1(self):
        m = IgnoranceMatrix([[2, 1, 0], [2, 1, 3]])
        with self.assertRaises(Exception):
            m.add_randomized_action([0, 1], [-0.5, 1.5])

    # WEAKLY DOMINATES
    def wd1(self):
        m = IgnoranceMatrix([[2, 1, 0], [2, 1, 3]])
        m.assign_values(IDENTITY)
        self.assertTrue(m.weakly_dominates(1, 0), "Unexpected result [[2, 1, 0], [2, 1, 3]].")

    # STRONGLY DOMINATES
    def sd1(self):
        m = IgnoranceMatrix([[2, 1, 0], [2, 1, 3]])
        m.assign_values(IDENTITY)
        self.assertTrue(m.strongly_dominates(1, 0), "Unexpected result [[2, 1, 0], [2, 1, 3]].")

    # DOMINANCE BESTS
    def db1(self):
        m = IgnoranceMatrix([[2, 1, 1], [0, 1, 3], [1, 1, 1]])
        m.assign_values(IDENTITY)
        self.assertEqual(m.dominance_bests(), sorted([0, 1]), "Unexpected result [[2, 1, 1], [0, 1, 3], [1, 1, 1]].")

    # MAXIMIN BESTS
    def mb1(self):
        m = IgnoranceMatrix([[0, 5], [0, 5]])
        m.assign_values(IDENTITY)
        self.assertEqual(sorted(m.maximin_bests()), sorted([0, 1]), "Unexpected result [[0, 5], [0, 5]].")

    # LEXIMIN BESTS
    def lb1(self):
        m = IgnoranceMatrix([[0, 5], [0, 4]])
        m.assign_values(IDENTITY)
        self.assertEqual(sorted(m.leximin_bests()), sorted([0]), "Unexpected result [[0, 5], [0, 4]].")

    # OPTIMISM PESSIMISM BESTS
    def opb1(self):
        m = IgnoranceMatrix([[0, 5], [0, 5]])
        m.assign_values(IDENTITY)
        self.assertEqual(sorted(m.optimism_pessimism_bests(0.9)), sorted([0, 1]), "Unexpected result [[0, 5], [0, 5]].")

    # REGRET MATRIX AND MINIMAX REGRET BESTS
    def mr1(self):
        m = IgnoranceMatrix([[1, 1, 1, 8], [2, 1, 7, 8], [0, 3, 0, 9]])
        m.assign_values(IDENTITY)
        self.assertEqual(sorted(m.minimax_regret_bests()), sorted([1]), "Unexpected result [[1, 1, 1, 8], [2, 1, 7, 8], [0, 3, 0, 9]].")

    # INSUFFICIENT REASON BESTS
    def ir1(self):
        m = IgnoranceMatrix([[0, 5], [0, 5]])
        m.assign_values(IDENTITY)
        self.assertEqual(sorted(m.insufficient_reason_bests()), sorted([0, 1]), "Unexpected result [[0, 5], [0, 5]].")


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for t in TESTS_TYPES:
        for i in range(1, UP_BOUND):
            try:
                suite.addTest(DecisionIgnoranceTestCase(f'{t}{i}'))
            except ValueError:
                break

    runner = unittest.TextTestRunner()
    runner.run(suite)
