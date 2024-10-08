from . import ast


class DepthChecker (ast.AstVisitor):
    """DepthChecker visitor"""

    def __init__(self, limit=4):
        super(DepthChecker, self).__init__()
        self.limit = limit
        self.depth = 0

    def get_isViolator(self):
        return self.depth > self.limit
    
    def get_limit(self):
        return self.limit

    def get_depth(self):
        return self.depth

    def visit_StmtList(self, node, *args, **kwargs):
        if node.stmts is None or len(node.stmts) == 0:
            return

        for n in node.stmts:
            self.visit(n, *args, **kwargs)

    def visit_Stmt(self, node, *args, **kwargs):
        pass

    def visit_IntVar(self, node, *args, **kwargs):
        pass

    def visit_Const(self, node, *args, **kwargs):
        pass

    def visit_AsgnStmt(self, node, *args, **kwargs):
        pass

    def visit_IfStmt(self, node, *args, **kwargs):
        self.visit(node.cond, *args, **kwargs)
        self.visit(node.then_stmt, *args, **kwargs)
        if node.has_else():
            self.visit(node.else_stmt, *args, **kwargs)
        self.depth = self.depth + 1

    def visit_WhileStmt(self, node, *args, **kwargs):
        self.visit(node.cond, *args, **kwargs)
        self.visit(node.body, *args, **kwargs)
        self.depth = self.depth + 5

    def visit_AssertStmt(self, node, *args, **kwargs):
        self.visit(node.cond, *args, **kwargs)

    def visit_AssumeStmt(self, node, *args, **kwargs):
        self.visit(node.cond, *args, **kwargs)

    def visit_HavocStmt(self, node, *args, **kwargs):
        for v in node.vars:
            self.visit(v, *args, **kwargs)

    def visit_Exp(self, node, *args, **kwargs):
        for a in node.args:
            self.visit(a, *args, **kwargs)


def main():
    import sys

    prg = ast.parse_file(sys.argv[1])
    id = DepthChecker()
    id.visit(prg)
    print('idCheck: ', id.get_isViolator())


if __name__ == '__main__':
    import sys
    sys.exit(main())
