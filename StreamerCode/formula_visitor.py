from antlr4 import *
from StreamerFormulaParser import StreamerFormulaParser
from StreamerFormulaLexer import StreamerFormulaLexer
from typing import Callable, Dict


class FormulaVisitor(ParseTreeVisitor):
    def __init__(self, fields: Dict[str, Callable]):
        self.Fields = fields

    def _left_right_check(self, ctx, operator):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        return operator(left, right)

    def calculate(self, expression: str):
        lexer = StreamerFormulaLexer(InputStream(expression))
        stream = CommonTokenStream(lexer)
        parser = StreamerFormulaParser(stream)
        tree = parser.formula()
        return self.visit(tree)

    def visitFormula(self, ctx: StreamerFormulaParser.FormulaContext):
        return self.visitChildren(ctx)

    def visitAdd(self, ctx: StreamerFormulaParser.AddContext):
        return self._left_right_check(ctx, lambda l, r: l + r)

    def visitOr(self, ctx: StreamerFormulaParser.OrContext):
        return self._left_right_check(ctx, lambda l, r: l or r)

    def visitIn(self, ctx: StreamerFormulaParser.InContext):
        value = self.visit(ctx.expr(0))
        compare_to = 1
        while compare_to < len(ctx.expr()):
            if value == self.visit(ctx.expr(compare_to)):
                return True
            compare_to += 1
        return False

    def visitSubtract(self, ctx: StreamerFormulaParser.SubtractContext):
        return self._left_right_check(ctx, lambda l, r: l - r)

    def visitNotEqual(self, ctx: StreamerFormulaParser.NotEqualContext):
        return self._left_right_check(ctx, lambda l, r: l != r)

    def visitInteger(self, ctx: StreamerFormulaParser.IntegerContext):
        return int(ctx.getText())

    def visitParenthesis(self, ctx: StreamerFormulaParser.ParenthesisContext):
        return self.visit(ctx.expr())

    def visitEqual(self, ctx: StreamerFormulaParser.EqualContext):
        return self._left_right_check(ctx, lambda l, r: l == r)

    def visitFunc(self, ctx: StreamerFormulaParser.FuncContext):
        return self.visitChildren(ctx)

    def visitField(self, ctx: StreamerFormulaParser.FieldContext):
        return self.visitChildren(ctx)

    def visitStringLiteral(self, ctx: StreamerFormulaParser.StringLiteralContext):
        return self.visitChildren(ctx)

    def visitAnd(self, ctx: StreamerFormulaParser.AndContext):
        return self._left_right_check(ctx, lambda l, r: l and r)

    def visitElseIf(self, ctx: StreamerFormulaParser.ElseIfContext):
        return self.visitChildren(ctx)

    def visitLessThan(self, ctx: StreamerFormulaParser.LessThanContext):
        return self._left_right_check(ctx, lambda l, r: l < r)

    def visitDateLiteral(self, ctx: StreamerFormulaParser.DateLiteralContext):
        return self.visitChildren(ctx)

    def visitDivide(self, ctx: StreamerFormulaParser.DivideContext):
        return self._left_right_check(ctx, lambda l, r: l / r)

    def visitGreaterEqual(self, ctx: StreamerFormulaParser.GreaterEqualContext):
        return self._left_right_check(ctx, lambda l, r: l >= r)

    def visitNotIn(self, ctx: StreamerFormulaParser.NotInContext):
        value = self.visit(ctx.expr(0))
        compare_to = 1
        while compare_to < len(ctx.expr()):
            if value == self.visit(ctx.expr(compare_to)):
                return False
            compare_to += 1
        return True

    def visitLessEqual(self, ctx: StreamerFormulaParser.LessEqualContext):
        return self._left_right_check(ctx, lambda l, r: l <= r)

    def visitDecimal(self, ctx: StreamerFormulaParser.DecimalContext):
        return self.visitChildren(ctx)

    def visitMultiply(self, ctx: StreamerFormulaParser.MultiplyContext):
        return self._left_right_check(ctx, lambda l, r: l * r)

    def visitIf(self, ctx: StreamerFormulaParser.IfContext):
        return self.visitChildren(ctx)

    def visitGreaterThan(self, ctx: StreamerFormulaParser.GreaterThanContext):
        return self._left_right_check(ctx, lambda l, r: l > r)

    def visitPow(self, ctx: StreamerFormulaParser.PowContext):
        return self.visitChildren(ctx)

    def visitMin(self, ctx: StreamerFormulaParser.MinContext):
        return self.visitChildren(ctx)

    def visitMax(self, ctx: StreamerFormulaParser.MaxContext):
        return self.visitChildren(ctx)

    def visitString(self, ctx: StreamerFormulaParser.StringContext):
        return self.visitChildren(ctx)
