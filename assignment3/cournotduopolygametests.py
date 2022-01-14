import unittest
from assignment3.cournot_duopoly_game import CournotDuopolyGame
from assignment3.strategicgame import StrategicGame

TESTS_TYPES = ['mc','iesds']

class CournotDuopolyTestCase(unittest.TestCase):
    # MATRIX CREATION
    def mc1(self):
        g = CournotDuopolyGame(range(0, 4), range(0, 4), 10, 20, lambda x, y: 100 - (x + y) ** (1/2))
        self.assertEqual(g.get_matrix(), [[(0.0, 0.0), (0.0, 79.0), (0.0, 157.2), (0.0, 234.8)],
                                          [(89.0, 0.0), (88.6, 78.6), (88.3, 156.5), (88.0, 234.0)],
                                          [(177.2, 0.0), (176.5, 78.3), (176.0, 156.0), (175.5, 233.3)],
                                          [(264.8, 0.0), (264.0, 78.0), (263.3, 155.5), (262.7, 232.7)]], f"Unexpected result with the game\n{g}")

    # IESDS
    def iesds1(self):
        g = CournotDuopolyGame(range(0, 4), range(0, 4), 10, 20, lambda x, y: 100 - (x + y) ** (1/2))
        giesds = g.iesds()
        self.assertTrue(giesds.get_matrix() == StrategicGame([[(262.7, 232.7)]]).get_matrix(), f"The original game should be left unchanged; now it is\n{g}.")


if __name__ == '__main__':
    suite = unittest.TestSuite()
    for t in TESTS_TYPES:
        for i in range(1, 20):
            try:
                suite.addTest(CournotDuopolyTestCase(f'{t}{i}'))
            except ValueError:
                break
    runner = unittest.TextTestRunner()
    runner.run(suite)