import unittest

from . import ast, depth


class TestId(unittest.TestCase):
    def test_safe_0(self):
        prg1 = "xdfd := 10; print_state"
        ast1 = ast.parse_string(prg1)
        depthcheck = depth.DepthChecker()
        depthcheck.visit(ast1)
        self.assertFalse(depthcheck.get_isViolator())
        self.assertEquals(depthcheck.get_depth(), 0)

    def test_safe_1_1(self):
        prg1 = "havoc y; x := 1; if y > 10 then { x := x + 1 }"
        ast1 = ast.parse_string(prg1)
        depthcheck = depth.DepthChecker()
        depthcheck.visit(ast1)
        self.assertFalse(depthcheck.get_isViolator())
        self.assertEquals(depthcheck.get_depth(), 1)

    def test_safe_1_2(self):
        prg1 = "havoc y; x := 1; if y > 10 then x := x + 1 else x := x - 1"
        ast1 = ast.parse_string(prg1)
        depthcheck = depth.DepthChecker()
        depthcheck.visit(ast1)
        self.assertFalse(depthcheck.get_isViolator())
        self.assertEquals(depthcheck.get_depth(), 1)

    def test_unsafe_havoc(self):
        ast1 = ast.parse_file('wlang/prog1.prg')
        depthcheck = depth.DepthChecker()
        depthcheck.visit(ast1)
        self.assertTrue(depthcheck.get_isViolator())

    def test_safe_havoc(self):
        ast1 = ast.parse_file('wlang/prog2.prg')
        depthcheck = depth.DepthChecker()
        depthcheck.visit(ast1)
        self.assertFalse(depthcheck.get_isViolator())
        self.assertEquals(depthcheck.get_depth(), 4)

    def test_safe_cascade(self):
        ast1 = ast.parse_file('wlang/prog3.prg')
        depthcheck = depth.DepthChecker()
        depthcheck.visit(ast1)
        self.assertFalse(depthcheck.get_isViolator())
        self.assertEquals(depthcheck.get_depth(), 4)


    def test_unsafe_cascade(self):
        ast1 = ast.parse_file('wlang/prog4.prg')
        depthcheck = depth.DepthChecker()
        depthcheck.visit(ast1)
        self.assertTrue(depthcheck.get_isViolator())
        self.assertEquals(depthcheck.get_depth(), 5)

    def test_safe_cascade_2(self):
        ast1 = ast.parse_file('wlang/prog5.prg')
        depthcheck = depth.DepthChecker()
        depthcheck.visit(ast1)
        self.assertFalse(depthcheck.get_isViolator())
        self.assertEquals(depthcheck.get_depth(), 1)