import datetime

from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from StreamerFormulaParser import StreamerFormulaParser
from StreamerFormulaLexer import StreamerFormulaLexer
from typing import Callable, Dict


class MissingFieldException(Exception):
    def __init__(self, missing_field: str):
        self.MissingField = missing_field

    def __str__(self):
        return "Missing field {field}".format(field=self.MissingField)


def calculate(expression: str, fields=None):
    if fields is None:
        fields = {}
    visitor = FormulaVisitor(expression, fields)
    return visitor.calculate()


class FormulaErrorListener(ErrorListener):

    def __init__(self):
        super(FormulaErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception("{line}:{col} {msg}".format(line=line, col=column, msg=msg))


class FormulaVisitor(ParseTreeVisitor):
    def __init__(self, expression: str, fields: Dict[str, Callable]):
        self.Expression = expression
        self.Fields = fields
        lexer = StreamerFormulaLexer(InputStream(expression))
        lexer.addErrorListener(FormulaErrorListener())
        stream = CommonTokenStream(lexer)
        parser = StreamerFormulaParser(stream)
        parser.addErrorListener(FormulaErrorListener())
        self._tree = parser.formula()

    def _left_right_check(self, ctx, operator):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        return operator(left, right)

    def calculate(self):
        return self.visit(self._tree)

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

    def visitField(self, ctx: StreamerFormulaParser.FieldContext):
        field_name = ctx.getText()[1:-1]
        value_getter = self.Fields.get(field_name)
        if value_getter is None:
            raise MissingFieldException(missing_field=field_name)
        return value_getter()

    def visitStringLiteral(self, ctx: StreamerFormulaParser.StringLiteralContext):
        return ctx.getText()[1:-1]

    def visitAnd(self, ctx: StreamerFormulaParser.AndContext):
        return self._left_right_check(ctx, lambda l, r: l and r)

    def visitElseIf(self, ctx: StreamerFormulaParser.ElseIfContext):
        condition = self.visit(ctx.expr(0))
        if condition:
            return self.visit(ctx.expr(1))

        elseifs = (len(ctx.expr())-3) / 2
        elseif = 0
        while elseif < elseifs:
            start_index = (elseif * 2) + 2
            condition = self.visit(ctx.expr(start_index))
            if condition:
                return self.visit(ctx.expr(start_index + 1))
            elseif += 1

        else_expr = len(ctx.expr())-1
        return self.visit(ctx.expr(else_expr))

    def visitLessThan(self, ctx: StreamerFormulaParser.LessThanContext):
        return self._left_right_check(ctx, lambda l, r: l < r)

    def visitDateLiteral(self, ctx: StreamerFormulaParser.DateLiteralContext):
        return datetime.datetime.strptime(ctx.getText()[1:-1], "%Y-%m-%d")

    def visitDatetimeLiteral(self, ctx: StreamerFormulaParser.DatetimeLiteralContext):
        return datetime.datetime.strptime(ctx.getText()[1:-1], "%Y-%m-%d %H:%M:%S")

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
        return float(ctx.getText())

    def visitMultiply(self, ctx: StreamerFormulaParser.MultiplyContext):
        return self._left_right_check(ctx, lambda l, r: l * r)

    def visitIf(self, ctx: StreamerFormulaParser.IfContext):
        condition = self.visit(ctx.expr(0))
        if condition:
            return self.visit(ctx.expr(1))
        else:
            return self.visit(ctx.expr(2))

    def visitGreaterThan(self, ctx: StreamerFormulaParser.GreaterThanContext):
        return self._left_right_check(ctx, lambda l, r: l > r)

    def visitPow(self, ctx: StreamerFormulaParser.PowContext):
        return pow(self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

    def visitMin(self, ctx: StreamerFormulaParser.MinContext):
        min_value = self.visit(ctx.expr(0))
        index = 1
        while index < len(ctx.expr()):
            compare_to = self.visit(ctx.expr(index))
            if compare_to < min_value:
                min_value = compare_to
            index += 1
        return min_value

    def visitMax(self, ctx: StreamerFormulaParser.MaxContext):
        max_value = self.visit(ctx.expr(0))
        index = 1
        while index < len(ctx.expr()):
            compare_to = self.visit(ctx.expr(index))
            if compare_to > max_value:
                max_value = compare_to
            index += 1
        return max_value
