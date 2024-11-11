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
        self.assertEqual(set([ast.IntVar('y'), ast.IntVar('c'), ast.IntVar('r'), ast.IntVar('x')]), cfgCheck.get_tops())

    def test_prog_2(self):
        cfgCheck = cfg.CFGAnalysis()
        cfgCheck.analyze('wlang/prog2.prg')
        self.assertEqual(len(cfgCheck.get_zeros()), 0)
        self.assertEqual(len(cfgCheck.get_odds()), 0)
        self.assertEqual(len(cfgCheck.get_bottoms()), 0)
        self.assertEqual(set([ast.IntVar('c'), ast.IntVar('r'), ast.IntVar('x'), ast.IntVar('abcdefghijklm')]), cfgCheck.get_tops())
        self.assertEqual(set([ast.IntVar('y')]), cfgCheck.get_evens())

    def test_prog_3(self):
        cfgCheck = cfg.CFGAnalysis()
        cfgCheck.analyze('wlang/prog3.prg')
        self.assertEqual(len(cfgCheck.get_zeros()), 0)
        self.assertEqual(len(cfgCheck.get_odds()), 0)
        self.assertEqual(len(cfgCheck.get_evens()), 0)
        self.assertEqual(len(cfgCheck.get_bottoms()), 0)
        self.assertEqual(set([ast.IntVar('x')]), cfgCheck.get_tops())

    def test_prog_4(self):
        cfgCheck = cfg.CFGAnalysis()
        cfgCheck.analyze('wlang/prog4.prg')
        self.assertEqual(len(cfgCheck.get_zeros()), 0)
        self.assertEqual(len(cfgCheck.get_odds()), 0)
        self.assertEqual(len(cfgCheck.get_evens()), 0)
        self.assertEqual(len(cfgCheck.get_bottoms()), 0)
        self.assertEqual(set([ast.IntVar('x')]), cfgCheck.get_tops())

    def test_prog_5(self):
        cfgCheck = cfg.CFGAnalysis()
        cfgCheck.analyze('wlang/prog5.prg')
        self.assertEqual(len(cfgCheck.get_zeros()), 0)
        self.assertEqual(len(cfgCheck.get_odds()), 0)
        self.assertEqual(len(cfgCheck.get_evens()), 0)
        self.assertEqual(len(cfgCheck.get_bottoms()), 0)
        self.assertEqual(set([ast.IntVar('x')]), cfgCheck.get_tops())

    def test_prog_6(self):
        cfgCheck = cfg.CFGAnalysis()
        cfgCheck.analyze('wlang/prog6.prg')
        self.assertEqual(len(cfgCheck.get_zeros()), 0)
        self.assertEqual(len(cfgCheck.get_odds()), 0)
        self.assertEqual(set([ast.IntVar('a'), ast.IntVar('b')]), cfgCheck.get_evens())
        self.assertEqual(set([ast.IntVar('c'), ast.IntVar('d')]), cfgCheck.get_tops())

    def test_prog_7(self):
        cfgCheck = cfg.CFGAnalysis()
        cfgCheck.analyze('wlang/prog7.prg')
        self.assertEqual(len(cfgCheck.get_zeros()), 0)
        self.assertEqual(len(cfgCheck.get_odds()), 0)
        self.assertEqual(set([ast.IntVar('a'), ast.IntVar('b'), ast.IntVar('d')]), cfgCheck.get_evens())
        self.assertEqual(set([ast.IntVar('c')]), cfgCheck.get_tops())
        self.assertEqual(set([ast.IntVar('e')]), cfgCheck.get_bottoms())
