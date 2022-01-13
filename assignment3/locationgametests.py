import unittest
from assignment3.locationgame import LocationGame

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
        self.assertEqual(sorted(g.find_Nash_profiles()), sorted([(0, 0), (1, 0)]), f"Unexpected result with the game\n{g}")

    def ne2(self):
        g = LocationGame(5)
        self.assertEqual(g.find_Nash_profiles(), [], f"Unexpected result with the game\n{g}")

    def ne3(self):
        g = LocationGame(6)
        self.assertEqual(sorted(g.find_Nash_profiles()), sorted([(2, 1), (3, 0), (3, 1)]), f"Unexpected result with the game\n{g}")


    # IESDS
    def iesds1(self):
        g = LocationGame(3)
        giesds = g.iesds()
        self.assertTrue(g.get_matrix() == LocationGame([[(1, 5), (0, 5)], [(0, 5), (0, 5)]]).get_matrix(), f"The original game should be left unchanged; now it is\n{g}.")
    def iesds2(self):
        g = LocationGame(5)
        giesds = g.iesds()
        self.assertTrue(giesds.get_matrix() == LocationGame([[(1, 5), (7, 5)]]).get_matrix(), f"Unexpected result with the game\n{g}\n")



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