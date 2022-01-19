#!/usr/bin/env python3

'''Test units for the module strategicgame.

'''

from assignment3.strategicgame import StrategicGame
import unittest


TESTS_TYPES = ['mc', 'ne', 'ds',
               #'nbr',
               'iesds', 'ienbr']
UP_BOUND = 100  # max number of tests of one type


class StrategicGameTestCase(unittest.TestCase):
    def setUp(self):
        pass

    # MATRIX CREATION
    def mc1(self):
        with self.assertRaises(Exception):
            g = StrategicGame([])
    def mc2(self):
        with self.assertRaises(Exception):
            g = StrategicGame([[], []])
    def mc3(self):
        with self.assertRaises(Exception):
            g = StrategicGame([[1, 2, 3], [1, 2, 4]])
    def mc4(self):
        with self.assertRaises(Exception):
            g = StrategicGame([[(1, 3), (1, 2), (3, 3), (1, 0)],
                               [(1, 0), (3, 3), (1, 1)]])
    def mc5(self):
        with self.assertRaises(Exception):
            g = StrategicGame([[(1, 1), (3, 3)],
                               [(1, 1), (3, 3)],
                               [(1, 1), (1, 1), (1, 1)]])
    def mc6(self):
        with self.assertRaises(Exception):
            g = StrategicGame([[(1, 1), (3, 3)],
                               [('h', 0), (3, 3)],
                               [(1, 1), (0, 9)]])
    def mc7(self):
        with self.assertRaises(Exception):
            g = StrategicGame([[(1, 3), (1, 3)],
                               [(8, 3), (8, 3)],
                               [(2, list(0, 4)), (1, 4)]])
    def mc8(self):
        with self.assertRaises(Exception):
            g = StrategicGame([[(1, 3)], [('a', 3)]])
    def mc9(self):
        with self.assertRaises(Exception):
            g = StrategicGame([(1, -10)])
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
    def ds3(self):
        g = StrategicGame([[(0, 2), (1, 0)],
                           [(1, 1), (0, 1)],
                           [(1, 1), (1, 1)],
                           [(2, 1), (1, 1)]])
        self.assertEqual(sorted(g.find_dominant_strategy_profiles()), sorted([(3, 0)]), f"Unexpected result with the game\n{g}")
    def ds4(self):
        g = StrategicGame([[(0, 2), (1, 2)],
                           [(1, 1), (0, 1)],
                           [(1, 1), (1, 1)],
                           [(2, 1), (1, 1)]])
        self.assertEqual(sorted(g.find_dominant_strategy_profiles()), sorted([]), f"Unexpected result with the game\n{g}")
    def ds5(self):
        g = StrategicGame([[(1, 2)],
                           [(0, 1)],
                           [(2, 1)],
                           [(1, 1)]])
        self.assertEqual(sorted(g.find_dominant_strategy_profiles()), sorted([(2, 0)]), f"Unexpected result with the game\n{g}")
    def ds6(self):
        g = StrategicGame([[(0, 2), (2, 2)]])
        self.assertEqual(sorted(g.find_dominant_strategy_profiles()), sorted([]), f"Unexpected result with the game\n{g}")
    def ds7(self):
        g = StrategicGame([[(0, 2), (2, 3)]])
        self.assertEqual(sorted(g.find_dominant_strategy_profiles()), sorted([(0, 1)]), f"Unexpected result with the game\n{g}")
    def ds8(self):
        g = StrategicGame([[(-1, -1), (-3, 0)], [(0, -3), (-2, -2)]])
        self.assertEqual(sorted(g.find_dominant_strategy_profiles()), sorted([(1, 1)]), f"Unexpected result with the game\n{g}")
    def ds9(self):
        g = StrategicGame([[(1, 1), (1, 0)], [(0, 1), (0, 0)]])
        self.assertEqual(sorted(g.find_dominant_strategy_profiles()), sorted([(0, 0)]), f"Unexpected result with the game\n{g}")
    def ds10(self):
        g = StrategicGame([[(0, 0), (0, 0)], [(0, 0), (0, 0)]])
        self.assertEqual(sorted(g.find_dominant_strategy_profiles()), sorted([]), f"Unexpected result with the game\n{g}")


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
    def ne4(self):
        g = StrategicGame([[(-5, -5), (-100, -100), (-1, -20)],
                           [(-100, -100), (0, 0), (0, -20)],
                           [(-20, -1), (-20, 0), (-20, -20)]])
        self.assertEqual(sorted(g.find_Nash_profiles()), sorted([(0, 0), (1, 1)]), f"Unexpected result with the game\n{g}")
    def ne5(self):
        g = StrategicGame([[(1, 1), (1, 1)],
                           [(1, 1), (1, 1)]])
        self.assertEqual(sorted(g.find_Nash_profiles()), sorted([(0, 0), (0, 1), (1, 0), (1, 1)]), f"Unexpected result with the game\n{g}")
    def ne6(self):
        g = StrategicGame([[(1, 1), (1, 2)],
                           [(1, 1), (1, 1)]])
        self.assertEqual(sorted(g.find_Nash_profiles()), sorted([(0, 1), (1, 0), (1, 1)]), f"Unexpected result with the game\n{g}")
    def ne7(self):
        g = StrategicGame([[(1, 1), (1, 1)],
                           [(1, -2), (1, 1)]])
        self.assertEqual(sorted(g.find_Nash_profiles()), sorted([(0, 0), (0, 1), (1, 1)]), f"Unexpected result with the game\n{g}")
    def ne8(self):
        g = StrategicGame([[(1, 1), (1, -3)],
                           [(1, -2), (1, 1)]])
        self.assertEqual(sorted(g.find_Nash_profiles()), sorted([(0, 0), (1, 1)]), f"Unexpected result with the game\n{g}")
    def ne9(self):
        g = StrategicGame([[(1, 1), (1, -3)],
                           [(1, -2), (1, 1)],
                           [(-1, -2), (0, 0)]])
        self.assertEqual(sorted(g.find_Nash_profiles()), sorted([(0, 0), (1, 1)]), f"Unexpected result with the game\n{g}")
    def ne10(self):
        g = StrategicGame([[(1, -10)]])
        self.assertEqual(sorted(g.find_Nash_profiles()), sorted([(0, 0)]), f"Unexpected result with the game\n{g}")
    def ne11(self):
        g = StrategicGame([[(-10, -10)]])
        self.assertEqual(sorted(g.find_Nash_profiles()), sorted([(0, 0)]), f"Unexpected result with the game\n{g}")
    def ne12(self):
        g = StrategicGame([
            [(1, 2), (2, 2)],
            [(0, 2), (4, 2)]])
        self.assertEqual(sorted(g.find_Nash_profiles()), sorted([(0, 0), (1, 1)]), f"Unexpected result with the game\n{g}")
    def ne13(self):
        g = StrategicGame([
            [(1, 2), (2, 2)],
            [(1, 2), (4, 2)]])
        self.assertEqual(sorted(g.find_Nash_profiles()), sorted([(0, 0), (1, 0), (1, 1)]), f"Unexpected result with the game\n{g}")
    def ne14(self):
        g = StrategicGame([
            [(1, 3), (2, 2)],
            [(1, 1), (4, 2)]])
        self.assertEqual(sorted(g.find_Nash_profiles()), sorted([(0, 0), (1, 1)]), f"Unexpected result with the game\n{g}")

    # NBR
    def nbr1(self):
        g = StrategicGame([[(1, 5), (0, 5)],
                           [(0, 5), (-1, 5)]])
        self.assertTrue(g.is_never_best_row_response(1), f"")
    def nbr2(self):
        g = StrategicGame([[(2, 1), (0, 0)],
                           [(0, 1), (2, 0)],
                           [(1, 1), (1, 2)]])
        self.assertTrue(g.is_never_best_row_response(2), f"")
    def nbr3(self):
        g = StrategicGame([[(2, 1), (0, 0)],
                           [(0, 1), (2, 0)],
                           [(1, 1), (1, 2)]])
        self.assertFalse(g.is_never_best_row_response(0), f"")
    def nbr4(self):
        g = StrategicGame([[(2, 1), (0, 0)],
                           [(0, 1), (1, 0)]])
        self.assertTrue(g.is_never_best_col_response(1), f"")
    def nbr5(self):
        g = StrategicGame([[(1, 2), (1, 0), (1, 1)],
                           [(0, 0), (0, 2), (2, 1)]])
        self.assertTrue(g.is_never_best_col_response(2), f"")
    def nbr6(self):
        g = StrategicGame([[(1, 2), (1, 0), (1, 1)],
                           [(0, 0), (0, 2), (2, 1)]])
        self.assertFalse(g.is_never_best_col_response(0), f"")

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
    def iesds3(self):
        g = StrategicGame([[(1, 5), (0, 6)],
                           [(0, 6), (0, 5)]])
        giesds = g.iesds()
        self.assertTrue(g.get_matrix() == StrategicGame([[(1, 5), (0, 6)], [(0, 6), (0, 5)]]).get_matrix(), f"The original game should be left unchanged; now it is\n{g}.")
    def iesds4(self):
        g = StrategicGame([[(1, 5), (0, 6)],
                           [(0, 6), (-1, 5)]])
        giesds = g.iesds()
        self.assertTrue(giesds.get_matrix() == StrategicGame([[(0, 6)]]).get_matrix(), f"Unexpected result with the game\n{g}\n")
    def iesds5(self):
        g = StrategicGame([
            [(0, 0), (1, 1), (2, 3)],
            [(1, -1), (2, 0), (-1, -2)],
            [(0, 1), (1, 1), (5, 2)]])
        giesds = g.iesds()
        self.assertTrue(giesds.get_matrix() == StrategicGame([[(0, 0), (1, 1), (2, 3)], [(1, -1), (2, 0), (-1, -2)], [(0, 1), (1, 1), (5, 2)]]).get_matrix(), f"Unexpected result with the game\n{g}\n")
    def iesds6(self):
        g = StrategicGame([
            [(1, 2), (2, 2)],
            [(0, 2), (4, 2)]])
        giesds = g.iesds()
        self.assertTrue(giesds.get_matrix() == StrategicGame([[(1, 2), (2, 2)], [(0, 2), (4, 2)]]).get_matrix(), f"Unexpected result with the game\n{g}")
    def iesds7(self):
        g = StrategicGame([
            [(1, 2), (2, 2)],
            [(2, 2), (4, 2)]])
        giesds = g.iesds()
        self.assertTrue(giesds.get_matrix() == StrategicGame([[(2, 2), (4, 2)]]).get_matrix(), f"Unexpected result with the game\n{g}\n")
    def iesds8(self):
        g = StrategicGame([
            [(1, 3), (2, 2)],
            [(2, 1), (4, 2)]])
        giesds = g.iesds()
        self.assertTrue(giesds.get_matrix() == StrategicGame([[(4, 2)]]).get_matrix(), f"Unexpected result with the game\n{g}\n")
    def iesds9(self):
        g = StrategicGame([[(1, 7), (-2, 6)],
                           [(-10, 5), (0, 5)]])
        giesds = g.iesds()
        self.assertTrue(giesds.get_matrix() == StrategicGame([[(1, 7), (-2, 6)], [(-10, 5), (0, 5)]]).get_matrix(), f"Unexpected result with the game\n{g}")
    def iesds10(self):
        g = StrategicGame([[(1, 7), (-2, 2)],
                           [(-10, 5), (0, 4)]])
        giesds = g.iesds()
        self.assertTrue(giesds.get_matrix() == StrategicGame([[(1, 7)]]).get_matrix(), f"Unexpected result with the game\n{g}")

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
    def ienbr3(self):
        g = StrategicGame([[(1, 2), (1, 0), (1, 1)],
                           [(0, 0), (0, 2), (2, 1)]])
        self.assertTrue(g.get_matrix() == StrategicGame([[(1, 2), (1, 0), (1, 1)], [(0, 0), (0, 2), (2, 1)]]).get_matrix(), f"The original game should be left unchanged; now it is\n{g}.")
    def ienbr4(self):
        g = StrategicGame([[(1, 2), (1, 0), (1, 1)],
                           [(0, 0), (0, 2), (2, 1)]])
        gienbr = g.ienbr()
        self.assertTrue(gienbr.get_matrix() == StrategicGame([[(1, 2)]]).get_matrix(), f"Unexpected result with the game\n{g}\n")
    def ienbr5(self):
        g = StrategicGame([[(1, 2), (1, 0)],
                           [(0, 0), (1, 1)],
                           [(0, 2), (2, 1)]])
        gienbr = g.ienbr()
        self.assertTrue(gienbr.get_matrix() == StrategicGame([[(1, 2)]]).get_matrix(), f"Unexpected result with the game\n{g}\n")
    def ienbr6(self):
        g = StrategicGame([[(1, 2), (1, 0)],
                           [(0, 0), (1, 1)],
                           [(0, 2), (2, 1)]])
        gienbr = g.ienbr()
        self.assertTrue(gienbr.get_matrix() == StrategicGame([[(1, 2)]]).get_matrix(), f"Unexpected result with the game\n{g}\n")
    def ienbr7(self):
        g = StrategicGame([[(1, 2), (0, 0), (0, 2)],
                           [(1, 0), (1, 1), (2, 1)]])
        gienbr = g.ienbr()
        self.assertTrue(gienbr.get_matrix() == g.get_matrix(), f"Unexpected result with the game\n{g}\n")
    def ienbr8(self):
        g = StrategicGame([[(2, 1), (0, 0), (2, 0)],
                           [(0, 1), (1, 1), (1, 2)]])
        gienbr = g.ienbr()
        self.assertTrue(gienbr.get_matrix() == StrategicGame([[(2 ,1)]]).get_matrix(), f"Unexpected result with the game\n{g}\n")


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