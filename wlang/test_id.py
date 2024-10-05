import unittest

from . import ast, id


class TestId(unittest.TestCase):
    def test_safe_assign(self):
        prg1 = "xdfd := 10; print_state"
        ast1 = ast.parse_string(prg1)
        idcheck = id.IdChecker()
        idcheck.visit(ast1)
        self.assertFalse(idcheck.get_isViolator())

    def test_unsafe_assign(self):
        prg1 = "xyzdefghijklm := 10; print_state"
        ast1 = ast.parse_string(prg1)
        idcheck = id.IdChecker()
        idcheck.visit(ast1)
        self.assertTrue(idcheck.get_isViolator())

    def test_safe_havoc(self):
        ast1 = ast.parse_file('wlang/prog1.prg')
        idcheck = id.IdChecker()
        idcheck.visit(ast1)
        self.assertFalse(idcheck.get_isViolator())

    def test_unsafe_havoc(self):
        ast1 = ast.parse_file('wlang/prog2.prg')
        idcheck = id.IdChecker()
        idcheck.visit(ast1)
        self.assertTrue(idcheck.get_isViolator())
