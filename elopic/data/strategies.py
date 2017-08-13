"""
Defines strategies for selecting random pictures from the database.
Each strategy is a function taking two parameters:
`entries`: A list of dicts (i.e. DB entries)
`count`: the number of entries that shall be returned
"""
import random
from operator import itemgetter


def fully_random(entries, count):
    """Choose completely at random from all entries"""
    return random.sample(entries, count)


def one_random_rest_least_seen(entries, count):
    """
    The first returned entry is completely random, any further entries
    are chosen in order of `seen_count` starting with the lowest.
    """
    the_random_one = random.choice(entries)
    if count > 1:
        entries.remove(the_random_one)
        least_seen = sorted(entries, key=itemgetter('seen_count'))[:count-1]
        least_seen.append(the_random_one)
        return least_seen
    else:
        return the_random_one
