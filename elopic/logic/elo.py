from __future__ import division
import math


class EloRating:

    def __init__(self, k_function=lambda x: 32, advantage_factor=400.0):
        self.k = k_function
        self.af = advantage_factor

    def calculate_new_rating(self, rating_1, rating_2, outcome):
        """Calculates new elo ratings, given two original ratings and an outcome.

        See https://metinmediamath.wordpress.com/2013/11/27/how-to-calculate-the-elo-rating-including-example/
        for a detailed explanation of the algorithm.

        :param rating_1: original rating of "player" one
        :param rating_2: original rating of "player" two
        :param outcome: 1 if "player" one wins, 0 if "player" two wins, 0.5 for a draw
        :return: new_rating_1, new_rating_2
        """
        r1 = self._transormed_rating(rating_1)
        r2 = self._transormed_rating(rating_2)

        e1 = self._expected_score(r1, r2)
        e2 = self._expected_score(r2, r1)

        u1 = self._updated_elo_rating(rating_1, e1, outcome)
        u2 = self._updated_elo_rating(rating_2, e2, 1 - outcome)

        return round(u1), round(u2)

    def _transormed_rating(self, score):
        return math.pow(10, score / self.af)

    def _expected_score(self, own_tr, other_tr):
        return own_tr / (own_tr + other_tr)

    def _updated_elo_rating(self, original_rating, expected_score, outcome):
        return original_rating + self.k(original_rating) * (outcome - expected_score)
