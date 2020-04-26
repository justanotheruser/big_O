"""Data generators for big_O module."""

import random
import string


def n_(n):
    """ Return N. """
    return n


def range_n(n, start=0):
    """ Return constructor for the sequence [start, start+1, ..., start+N-1]. """
    def make_single():
        return list(range(start, start + n))
    return make_single


def integers(n, min_, max_):
    """ Return constructor for sequence of N random integers between min_ and max_ (included).
    """
    def make_single():
        return [random.randint(min_, max_) for _ in range(n)]
    return make_single


def large_integers(n):
    """ Return constructor for sequence of N large random integers. """
    def make_single():
        return [random.randint(-50, 50) * 1000000 + random.randint(0, 10000)
                for _ in range(n)]
    return make_single


def strings(n, chars=string.ascii_letters):
    """ Return constructor for random string of N characters, sampled at random from `chars`.
    """
    def make_single():
        return ''.join([random.choice(chars) for i in xrange(n)])
    return make_single


def datagen(single_data_maker, n_cases):
    data_cases = [single_data_maker() for _ in range(n_cases)]
    while True:
        for data in data_cases:
            yield data
