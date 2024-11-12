import unittest

from . import ast, cfg


class TestCFG(unittest.TestCase):
    def test_prog_1(self):
        cfgCheck = cfg.CFGAnalysis()
        cfgCheck.analyze('wlang/prog1.prg')
        self.assertEqual(len(cfgCheck.get_zeros()), 0)
        self.assertEqual(len(cfgCheck.get_odds()), 0)
        self.assertEqual(len(cfgCheck.get_bottoms()), 0)
        self.assertEqual(len(cfgCheck.get_evens()), 0)
        self.assertEqual(set(['y','c', 'r', 'x']), cfgCheck.get_tops())

    def test_prog_2(self):
        cfgCheck = cfg.CFGAnalysis()
        cfgCheck.analyze('wlang/prog2.prg')
        self.assertEqual(len(cfgCheck.get_zeros()), 0)
        self.assertEqual(len(cfgCheck.get_odds()), 0)
        self.assertEqual(len(cfgCheck.get_bottoms()), 0)
        self.assertEqual(set(['c', 'r', 'x', 'abcdefghijklm']), cfgCheck.get_tops())
        self.assertEqual(set(['y']), cfgCheck.get_evens())

    def test_prog_3(self):
        cfgCheck = cfg.CFGAnalysis()
        cfgCheck.analyze('wlang/prog3.prg')
        self.assertEqual(len(cfgCheck.get_zeros()), 0)
        self.assertEqual(len(cfgCheck.get_odds()), 0)
        self.assertEqual(len(cfgCheck.get_evens()), 0)
        self.assertEqual(len(cfgCheck.get_bottoms()), 0)
        self.assertEqual(set(['x']), cfgCheck.get_tops())

    def test_prog_4(self):
        cfgCheck = cfg.CFGAnalysis()
        cfgCheck.analyze('wlang/prog4.prg')
        self.assertEqual(len(cfgCheck.get_zeros()), 0)
        self.assertEqual(len(cfgCheck.get_odds()), 0)
        self.assertEqual(len(cfgCheck.get_evens()), 0)
        self.assertEqual(len(cfgCheck.get_bottoms()), 0)
        self.assertEqual(set(['x']), cfgCheck.get_tops())

    def test_prog_5(self):
        cfgCheck = cfg.CFGAnalysis()
        cfgCheck.analyze('wlang/prog5.prg')
        self.assertEqual(len(cfgCheck.get_zeros()), 0)
        self.assertEqual(len(cfgCheck.get_odds()), 0)
        self.assertEqual(len(cfgCheck.get_evens()), 0)
        self.assertEqual(len(cfgCheck.get_bottoms()), 0)
        self.assertEqual(set(['x']), cfgCheck.get_tops())

    def test_prog_6(self):
        cfgCheck = cfg.CFGAnalysis()
        cfgCheck.analyze('wlang/prog6.prg')
        self.assertEqual(len(cfgCheck.get_zeros()), 0)
        self.assertEqual(len(cfgCheck.get_odds()), 0)
        self.assertEqual(set(['a', 'b']), cfgCheck.get_evens())
        self.assertEqual(set(['c', 'd']), cfgCheck.get_tops())

    def test_prog_7(self):
        cfgCheck = cfg.CFGAnalysis()
        cfgCheck.analyze('wlang/prog7.prg')
        self.assertEqual(len(cfgCheck.get_zeros()), 0)
        self.assertEqual(len(cfgCheck.get_odds()), 0)
        self.assertEqual(set(['a', 'b', 'd']), cfgCheck.get_evens())
        self.assertEqual(set(['c']), cfgCheck.get_tops())
        self.assertEqual(set(['e']), cfgCheck.get_bottoms())
