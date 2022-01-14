import unittest
from assignment3.locationgame import LocationGame
from assignment3.strategicgame import StrategicGame

TESTS_TYPES = ['mc', 'ne', 'iesds']

class LocationGameTestCase(unittest.TestCase):
    # MATRIX CREATION
    def mc1(self):
        with self.assertRaises(Exception):
            g = LocationGame(0)

    def mc2(self):
        with self.assertRaises(Exception):
            g = LocationGame(1.5)

    # NASH EQULIBRIA
    def ne1(self):
        g = LocationGame(3)
        self.assertEqual(sorted(g.find_Nash_profiles()), sorted([(1, 1)]), f"Unexpected result with the game\n{g}")

    def ne2(self):
        g = LocationGame(5)
        self.assertEqual(g.find_Nash_profiles(), sorted([(2, 2)]), f"Unexpected result with the game\n{g}")

    def ne3(self):
        g = LocationGame(4)
        # the nash equilibrium should always be the central entries of the matrix
        # depending on whether it is an uneven or even number of locations that means either 1 or 4 cells
        self.assertEqual(sorted(g.find_Nash_profiles()), sorted([(1, 2), (2, 1), (2, 2), (1, 1)]), f"Unexpected result with the game\n{g}")


    # IESDS
    def iesds1(self):
        g = LocationGame(3)
        giesds = g.iesds()
        self.assertTrue(g.get_matrix() == LocationGame(3).get_matrix(), f"The original game should be left unchanged; now it is\n{g}.")

    def iesds2(self):
        g = LocationGame(5)
        giesds = g.iesds()
        self.assertTrue(giesds.get_matrix() == StrategicGame([[(2.0, 3.0)],[(2.0, 3.0)]]).get_matrix(), f"Unexpected result with the game\n{g}\n")



if __name__ == '__main__':
    suite = unittest.TestSuite()
    for t in TESTS_TYPES:
        for i in range(1, 20):
            try:
                suite.addTest(LocationGameTestCase(f'{t}{i}'))
            except ValueError:
                break
    runner = unittest.TextTestRunner()
    runner.run(suite)