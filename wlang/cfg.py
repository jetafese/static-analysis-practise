from enum import Enum
from functools import reduce

from . import ast


class Types(Enum):
    TOP = 1
    EVEN = 2
    ODD = 3
    ZERO = 4
    BOTTOM = 5

class Domain (object):
    """A domain for analyzing While programs that
    Keeps track of all variables defined up to the statement,
    and where they are on the lattice.

            T
        /   |    |
       e    o    0 
       |    |    /
           _|_
    """

    def __init__(self, evens=None, odds=None, zeros=None, tops=None, bottoms=None):
        # even variables
        if evens is None or len(evens) == 0:
            self._evens = set()
        else:
            self._evens = set(evens)

        # odd variables
        if odds is None or len(odds) == 0:
            self._odds = set()
        else:
            self._odds = set(odds)

        # zero variables
        if zeros is None or len(zeros) == 0:
            self._zeros = set()
        else:
            self._zeros = set(zeros)

        # top variables
        if tops is None or len(tops) == 0:
            self._tops = set()
        else:
            self._tops = set(tops)

        # bottom variables
        if bottoms is None or len(bottoms) == 0:
            self._bottoms = set()
        else:
            self._bottoms = set(bottoms)

    def get_evens(self):
        return self._evens

    def get_odds(self):
        return self._odds

    def get_zeros(self):
        return self._zeros

    def get_tops(self):
        return self._tops

    def get_bottoms(self):
        return self._bottoms

    def set_domain(self, other):
        self._evens = other.get_evens()
        self._zeros = other.get_zeros()
        self._odds = other.get_odds()
        self._tops = other.get_tops()
        self._bottoms = other.get_bottoms()

    def checkEquals(self, other):
        print(len(self._evens.difference(other._evens)), len(other._evens.difference(self._evens)))
        if len(self._evens.difference(other._evens)) > 0 or len(other._evens.difference(self._evens)) > 0:
            return False
        print(len(self._odds.difference(other._odds)), len(other._odds.difference(self._odds)))
        if len(self._odds.difference(other._odds)) > 0 or len(other._odds.difference(self._odds)) > 0:
            return False
        print(len(self._zeros.difference(other._zeros)), len(other._zeros.difference(self._zeros)))
        if len(self._zeros.difference(other._zeros)) > 0 or len(other._zeros.difference(self._zeros)) > 0:
            return False
        print(len(other._tops.difference(other._tops)), len(other._tops.difference(self._tops)))
        if len(self._tops.difference(other._tops)) > 0 or len(other._tops.difference(self._tops)) > 0:
            return False
        print(len(self._bottoms.difference(other._bottoms)), len(other._bottoms.difference(self._bottoms)))
        if len(self._bottoms.difference(other._bottoms)) > 0 or len(other._bottoms.difference(self._bottoms)) > 0:
            return False
        return True

    def get_type(self, var):
        if var in self._evens:
            return Types.EVEN
        if var in self._odds:
            return Types.ODD
        if var in self._zeros:
            return Types.ZERO
        if var in self._tops:
            return Types.TOP
        if var in self._bottoms:
            return Types.BOTTOM
        assert False

    def join(self, fact):
        """Joins a given domain fact into this one"""
        if self.checkEquals(fact):
            return
        # join verdicts
        self._evens = self._evens.union(fact._evens)
        self._odds = self._odds.union(fact._odds)
        self._zeros = self._zeros.union(fact._zeros)
        self._tops = self._tops.union(fact._tops)
        self._bottoms = self._bottoms.union(fact._bottoms)
        # merge verdicts
        tempBottom = self._bottoms
        for val in tempBottom:
            self.mark_bottom(val)
        tempTops = self._tops
        for val in tempTops:
            self.mark_top(val)
        # handle evens
        tempEvens = self._evens
        tempEvensFork = self.fork()
        for val in tempEvens:
            if val in tempEvensFork.get_odds() or val in tempEvensFork.get_zeros():
                tempEvensFork.mark_top(val)
                print(val)
        self.set_domain(tempEvensFork)
        # handle odds
        tempOdds = self._odds
        tempOddsFork = self.fork()
        for val in tempOdds:
            if val in tempOddsFork.get_odds() or val in tempOddsFork.get_zeros():
                tempOddsFork.mark_top(val)
                print(val)
        self.set_domain(tempOddsFork)
        # handle zeros
        tempZeros = self._zeros
        tempZerosFork = self.fork()
        for val in tempZeros:
            if val in tempZerosFork.get_odds() or val in tempZerosFork.get_zeros():
                tempZerosFork.mark_top(val)
                print(val)
        self.set_domain(tempZerosFork)
        
    def fork(self):
        """Splits the current domain into two"""
        return Domain(self._evens, self._odds, self._zeros, self._tops, self._bottoms)

    def removeEven(self, var):
        if var in self._evens:
            self._evens.remove(var)

    def removeOdd(self, var):
        if var in self._odds:
            self._odds.remove(var)

    def removeZero(self, var):
        if var in self._zeros:
            self._zeros.remove(var)

    def removeTop(self, var):
        if var in self._tops:
            self._tops.remove(var)

    def mark_zero(self, var):
        self.removeEven(var)
        self.removeOdd(var)
        self.removeTop(var)
        self._zeros.add(var)

    def mark_even(self, var):
        self.removeOdd(var)
        self.removeZero(var)
        self.removeTop(var)
        self._evens.add(var)

    def mark_odd(self, var):
        self.removeZero(var)
        self.removeEven(var)
        self.removeTop(var)
        self._odds.add(var)

    def mark_top(self, var):
        self.removeZero(var)
        self.removeEven(var)
        self.removeOdd(var)
        self._tops.add(var)

    def mark_bottom(self, var):
        self.removeZero(var)
        self.removeEven(var)
        self.removeOdd(var)
        self.removeTop(var)
        self._bottoms.add(var)


class CFGAnalysis (ast.AstVisitor):
    """Computes cfg for program"""

    def __init__(self):
        super(CFGAnalysis, self).__init__()
        self._dom = Domain()

    def analyze(self, filename):
        node = ast.parse_file(filename)
        self._dom = self.visit(node, dom=Domain())

    def get_evens(self):
        return self._dom.get_evens()

    def get_odds(self):
        return self._dom.get_odds()

    def get_zeros(self):
        return self._dom.get_zeros()

    def get_tops(self):
        return self._dom.get_tops()

    def get_bottoms(self):
        return self._dom.get_bottoms()
    
    def get_add(self, lhs, rhs, dom):
        tlhs = lhs
        trhs = rhs
        if not isinstance(lhs, Types):
            tlhs = dom.get_type(lhs)
        if not isinstance(rhs, Types):
            trhs = dom.get_type(rhs)
        if tlhs == Types.BOTTOM or trhs == Types.BOTTOM:
            return Types.BOTTOM
        if tlhs == Types.TOP or trhs == Types.TOP:
            return Types.TOP
        if tlhs == Types.ZERO:
            return trhs
        if trhs == Types.ZERO:
            return tlhs
        if tlhs == Types.EVEN:
            if trhs == Types.ODD:
                return Types.ODD
            return Types.EVEN
        if tlhs == Types.ODD:
            if trhs == Types.ODD:
                return Types.EVEN
            return Types.ODD

        return Types.TOP

    def get_mult(self, lhs, rhs, dom):
        tlhs = lhs
        trhs = rhs
        if not isinstance(lhs, Types):
            tlhs = dom.get_type(lhs)
        if not isinstance(rhs, Types):
            trhs = dom.get_type(rhs)
        if tlhs == Types.BOTTOM or trhs == Types.BOTTOM:
            return Types.BOTTOM
        if tlhs == Types.ZERO or trhs == Types.ZERO:
            return Types.ZERO
        if tlhs == Types.EVEN or trhs == Types.EVEN:
            return Types.EVEN
        if tlhs == Types.ODD and trhs == Types.ODD:
            return Types.ODD

        return Types.TOP

    def get_sub(self, lhs, rhs, dom):
        tlhs = lhs
        trhs = rhs
        if not isinstance(lhs, Types):
            tlhs = dom.get_type(lhs)
        if not isinstance(rhs, Types):
            trhs = dom.get_type(rhs)
        if tlhs == Types.BOTTOM or trhs == Types.BOTTOM:
            return Types.BOTTOM
        if tlhs == Types.TOP or trhs == Types.TOP:
            return Types.TOP
        if tlhs == Types.ZERO:
            return trhs
        if trhs == Types.ZERO:
            return tlhs
        if tlhs == Types.EVEN and trhs == Types.ODD:
            return Types.ODD
        if tlhs == Types.ODD and trhs == Types.EVEN:
            return Types.ODD

        return Types.TOP

    def get_div(self, lhs, rhs, dom):
        tlhs = lhs
        trhs = rhs
        if not isinstance(lhs, Types):
            tlhs = dom.get_type(lhs)
        if not isinstance(rhs, Types):
            trhs = dom.get_type(rhs)
        if tlhs == Types.BOTTOM or trhs == Types.BOTTOM:
            return Types.BOTTOM
        if trhs == Types.ZERO:
            return Types.BOTTOM
        if tlhs == Types.ZERO:
            return Types.ZERO

        return Types.TOP


    def visit_StmtList(self, node, *args, **kwargs):
        print("statements:")
        for n in node.stmts:
            df = self.visit(n)
        return df

    def visit_StmtList(self, node, *args, **kwargs):
        dom = kwargs['dom']
        if node.stmts is None:
            return dom
        for n in node.stmts:
            dom = self.visit(n, dom=dom)
        return dom

    def visit_AsgnStmt(self, node, *args, **kwargs):
        print("assng: ", node.lhs, " ", node.rhs)
        dom = kwargs['dom']
        res = self.visit(node.rhs, dom=dom)
        print(res)
        if res == Types.EVEN:
            dom.mark_even(node.lhs)
        elif res == Types.ODD:
            dom.mark_odd(node.lhs)
        elif res == Types.ZERO:
            dom.mark_zero(node.lhs)
        elif res == Types.TOP:
            dom.mark_top(node.lhs)
        else:
            dom.mark_bottom(node.lhs)
        print(dom.get_type(node.lhs))
        return dom

    def visit_AExp(self, node, *args, **kwargs):
        print("aexp: ")
        kids = [self.visit(a, *args, **kwargs) for a in node.args]
        dom = kwargs['dom']

        fn = None
        if node.op == "+":
            fn = lambda x, y: self.get_add(x, y, dom)
        elif node.op == "-":
            fn = lambda x, y: self.get_sub(x, y, dom)
        elif node.op == "*":
            fn = lambda x, y: self.get_mult(x, y, dom)
        elif node.op == "/":
            fn = lambda x, y: self.get_div(x, y, dom)

        assert fn is not None
        return reduce(fn, kids)

    def visit_IntVar(self, node, *args, **kwargs):
        print("int var: ", node.name)
        dom = kwargs['dom']
        return dom.get_type(node)

    def visit_Const(self, node, *args, **kwargs):
        print("const: ", node.val)
        if node.val == 0:
            return Types.ZERO
        if node.val % 2 == 0:
            return Types.EVEN
        return Types.ODD

    def visit_HavocStmt(self, node, *args, **kwargs):
        dom = kwargs['dom']
        for v in node.vars:
            dom.mark_top(v)
        return dom

    def visit_Stmt(self, node, *args, **kwargs):
        print("stmt")
        return kwargs['dom']
    
    def visit_IfStmt(self, node, *args, **kwargs):
        print("ifstmt")
        dom = kwargs['dom']
        # self.visit(node.cond)
        dom_then = dom.fork()
        dom_then = self.visit(node.then_stmt, dom=dom_then)
        dom.join(dom_then)
        print("done then")
        dom_else = dom.fork()
        if node.has_else():
            dom_else = self.visit(node.else_stmt, dom=dom_else)
            print("done else")
        dom.join(dom_else)
        return dom

    def visit_AssertStmt(self, node, *args, **kwargs):
        print("assert")
        return kwargs['dom']

    def visit_AssumeStmt(self, node, *args, **kwargs):
        print("assume")
        return kwargs['dom']

    def visit_WhileStmt(self, node, *args, **kwargs):
        print("whilestmt")
        return kwargs['dom']

def main():
    import sys

    prg = ast.parse_file('wlang/prog1.prg')
    cfg = CFGAnalysis()
    cfg.analyze(prg)


if __name__ == '__main__':
    import sys
    sys.exit(main())
