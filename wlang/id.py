from . import ast


class IdChecker (ast.AstVisitor):
    """IdChecker visitor"""

    def __init__(self, limit=13):
        super(IdChecker, self).__init__()
        self.idLimit = limit
        self.isViolator = False

    def get_isViolator(self):
        return self.isViolator
    
    def get_limit(self):
        return self.idLimit
    
    def set_isViolator(self, idLength):
        if (idLength == self.idLimit):
            self.isViolator = True

    def visit_StmtList(self, node, *args, **kwargs):
        if node.stmts is None or len(node.stmts) == 0:
            return

        for n in node.stmts:
            self.visit(n, *args, **kwargs)

    def visit_Stmt(self, node, *args, **kwargs):
        pass

    def visit_IntVar(self, node, *args, **kwargs):
        self.set_isViolator(len(node.name))

    def visit_Const(self, node, *args, **kwargs):
        pass

    def visit_AsgnStmt(self, node, *args, **kwargs):
        self.visit_Stmt(node, *args, **kwargs)
        self.visit(node.lhs, *args, **kwargs)
        self.visit(node.rhs, *args, **kwargs)

    def visit_IfStmt(self, node, *args, **kwargs):
        self.visit_Stmt(node, *args, **kwargs)
        self.visit(node.cond, *args, **kwargs)
        self.visit(node.then_stmt, *args, **kwargs)
        if node.has_else():
            self.visit(node.else_stmt, *args, **kwargs)

    def visit_WhileStmt(self, node, *args, **kwargs):
        self.visit_Stmt(node, *args, **kwargs)
        self.visit(node.cond, *args, **kwargs)
        self.visit(node.body, *args, **kwargs)

    def visit_AssertStmt(self, node, *args, **kwargs):
        self.visit_Stmt(node, *args, **kwargs)
        self.visit(node.cond, *args, **kwargs)

    def visit_AssumeStmt(self, node, *args, **kwargs):
        self.visit_Stmt(node, *args, **kwargs)
        self.visit(node.cond, *args, **kwargs)

    def visit_HavocStmt(self, node, *args, **kwargs):
        self.visit_Stmt(node, *args, **kwargs)
        for v in node.vars:
            self.visit(v, *args, **kwargs)

    def visit_Exp(self, node, *args, **kwargs):
        for a in node.args:
            self.visit(a, *args, **kwargs)


def main():
    import sys

    prg = ast.parse_file(sys.argv[1])
    id = IdChecker()
    id.visit(prg)
    print('idCheck: ', id.get_isViolator())


if __name__ == '__main__':
    import sys
    sys.exit(main())
