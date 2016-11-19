from elopic.logic.elo import EloRating

import unittest


class TestLogic(unittest.TestCase):
    """Test cases for the Logic package."""

    def test_elo_rating(self):
        """
        Test case for calculating new elo ratings after a "match".
        """
        elo = EloRating()
        elo1, elo2 = elo.calculate_new_rating(2400, 2000, 1)
        self.assertEqual(elo1, 2403)
        self.assertEqual(elo2, 1997)

        elo1, elo2 = elo.calculate_new_rating(2400, 2000, 0)
        self.assertEqual(elo1, 2371)
        self.assertEqual(elo2, 2029)


if __name__ == '__main__':
    unittest.main()
