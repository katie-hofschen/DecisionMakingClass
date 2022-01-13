#!/usr/bin/env python3

'''Test units for the module strategicgame.

'''

from assignment3.strategicgame import StrategicGame
import unittest


TESTS_TYPES = ['mc', 'ne', 'ds', 'iesds', 'ienbr']
UP_BOUND = 100  # max number of tests of one type


class StrategicGameTestCase(unittest.TestCase):
    def setUp(self):
        pass

    # MATRIX CREATION
    def mc7(self):
        with self.assertRaises(Exception):
            g = StrategicGame([[(1, 3), (1, 3)],
                               [(8, 3), (8, 3)],
                               [(2, list(0, 4)), (1, 4)]])
    def mc10(self):
        with self.assertRaises(Exception):
            g = StrategicGame([(1, -10), (9, 1)])

    # DOMINANT STRATEGIES
    def ds1(self):
        g = StrategicGame([[(0, 5)],
                           [(0, 5)]])
        self.assertEqual(sorted(g.find_dominant_strategy_profiles()), sorted([]), f"Unexpected result with the game\n{g}")
    def ds2(self):
        g = StrategicGame([[(1, 5)],
                           [(0, 5)]])
        self.assertEqual(sorted(g.find_dominant_strategy_profiles()), sorted([(0, 0)]), f"Unexpected result with the game\n{g}")

    # NASH EQULIBRIA
    def ne1(self):
        g = StrategicGame([[(0, 5)],
                           [(0, 5)]])
        self.assertEqual(sorted(g.find_Nash_profiles()), sorted([(0, 0), (1, 0)]), f"Unexpected result with the game\n{g}")
    def ne2(self):
        g = StrategicGame([[(0, 0), (0, 1)],
                           [(-1, 1), (1, 0)]])
        self.assertEqual(g.find_Nash_profiles(), [], f"Unexpected result with the game\n{g}")
    def ne3(self):
        g = StrategicGame([[(0, 2), (1, 0)],
                           [(1, 1), (0, 1)],
                           [(1, 1), (1, 1)],
                           [(2, 1), (1, 1)]])
        self.assertEqual(sorted(g.find_Nash_profiles()), sorted([(2, 1), (3, 0), (3, 1)]), f"Unexpected result with the game\n{g}")


    # IESDS
    def iesds1(self):
        g = StrategicGame([[(1, 5), (0, 5)],
                           [(0, 5), (0, 5)]])
        giesds = g.iesds()
        self.assertTrue(g.get_matrix() == StrategicGame([[(1, 5), (0, 5)], [(0, 5), (0, 5)]]).get_matrix(), f"The original game should be left unchanged; now it is\n{g}.")
    def iesds2(self):
        g = StrategicGame([[(1, 5), (7, 5)],
                           [(0, 5), (0, 5)]])
        giesds = g.iesds()
        self.assertTrue(giesds.get_matrix() == StrategicGame([[(1, 5), (7, 5)]]).get_matrix(), f"Unexpected result with the game\n{g}\n")

    # IENBR
    def ienbr1(self):
        g = StrategicGame([[(2, 1), (0, 0)],
                           [(0, 1), (2, 0)],
                           [(1, 1), (1, 2)]])
        gienbr = g.ienbr()
        self.assertTrue(g.get_matrix() == StrategicGame([[(2, 1), (0, 0)], [(0, 1), (2, 0)], [(1, 1), (1, 2)]]).get_matrix(), f"The original game should be left unchanged; now it is\n{g}.")

    def ienbr2(self):
        g = StrategicGame([[(2, 1), (0, 0)],
                           [(0, 1), (2, 0)],
                           [(1, 1), (1, 2)]])
        gienbr = g.ienbr()
        self.assertTrue(gienbr.get_matrix() == StrategicGame([[(2, 1)]]).get_matrix(), f"Unexpected result with the game\n{g}\n")


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for t in TESTS_TYPES:
        for i in range(1, UP_BOUND):
            try:
                suite.addTest(StrategicGameTestCase(f'{t}{i}'))
            except ValueError:
                break
    runner = unittest.TextTestRunner()
    runner.run(suite)
