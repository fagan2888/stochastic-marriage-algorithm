
import unittest

from random import randint, sample

from prefs import Preferences
from rankings import Rankings
from pairing import Pairing
from algorithm import stochastic_marriage
from rogues import Rogues

class PreferenceTests(unittest.TestCase):
    def test_prefs(self):
        p = Preferences([1, 2, 3, 4, 5])
        self.assertTrue(p.prefers(1, 2))
        self.assertFalse(p.prefers(2, 1))
        self.assertTrue(p.prefers(2, 5))
        self.assertTrue(p.prefers(2, 3))
        self.assertTrue(p.prefers(1, 5))
        self.assertFalse(p.prefers(5, 1))
        self.assertFalse(p.prefers(5, 5))
        self.assertFalse(p.prefers(5, 10))
        self.assertEqual([1,2,3,4,5], list(p))
    def test_pref_rankings(self):
        total = list(range(0,1000))
        for _ in range(1000):
            samp = sample(total, randint(20, 700))
            self.assertEqual(samp, list(Preferences(samp)))
    def test_all_preferred_to(self):
        p = Preferences([1, 2, 3, 4, 5])
        self.assertEqual({1,2,3}, set(p.all_preferred_to(4)))
        self.assertEqual({1,2,3,4}, set(p.all_preferred_to(5)))
        self.assertEqual(set(), set(p.all_preferred_to(1)))
        self.assertEqual(set(), set(p.all_preferred_to(6)))
    def test_string_keys(self):
        p = Preferences(('A', 'B'))
        self.assertTrue(p.prefers('A', 'B'))
        self.assertFalse(p.prefers('B', 'A'))
        self.assertEqual({'A'}, set(p.all_preferred_to('B')))

class StochasticInput(unittest.TestCase):
    def test_rankings(self):
        rank = Rankings({1:['A', 'B'], 2:['A', 'B'], 'A':[2, 1], 'B':[2, 1]})
        self.assertTrue(rank.prefers(1, 'A', 'B'))
        self.assertTrue(rank.prefers(2, 'A', 'B'))
        self.assertTrue(rank.prefers('A', 2, 1))
        self.assertFalse(rank.prefers('A', 1, 2))
        self.assertFalse(rank.prefers('A', 1, 1))
        self.assertFalse(rank.prefers('A', 1, 3))
    def test_all_preferred(self):
        rank = Rankings({1:['A', 'B'], 2:['A', 'B'], 'A':[2, 1], 'B':[2, 1]})
        self.assertEqual(set(), set(rank.all_preferred(1, 'A')))
        self.assertEqual(set(), set(rank.all_preferred(2, 'A')))
        self.assertEqual({'A'}, set(rank.all_preferred(1, 'B')))
        self.assertEqual({2}, set(rank.all_preferred('B', 1)))
        self.assertEqual({2}, set(rank.all_preferred('A', 1)))

class PairingTest(unittest.TestCase):
    def test_pairing_people(self):
        init = Pairing((1, 'B'), (2, 'A'), (3, 'C'))
        self.assertEqual({1, 'B', 2, 'A', 3, 'C'}, set(init.people))

class RoguesTest(unittest.TestCase):
    def test_rogues(self):
        rank = Rankings({
                1 : ['A', 'B'],
                2 : ['B', 'A'],
                'A' : [1, 2],
                'B' : [2, 1]
            })
        init = Pairing((1, 'B'), (2, 'A'))
        r = Rogues(init, rank)
        self.assertEqual(2, len(r))
        self.assertEqual({(2, 'B'), (1, 'A')}, {r.select(), r.select()})
        
class AlgorithmTests(unittest.TestCase):
    def test_stability_of_output(self):
        rank = Rankings({
                1 : ['A', 'B'],
                2 : ['B', 'A'],
                'A' : [1, 2],
                'B' : [2, 1]
            })
        init = Pairing((1, 'B'), (2, 'A'))
        self.assertEqual(Pairing((1, 'A'), (2, 'B')), stochastic_marriage(rank, init))

unittest.main()