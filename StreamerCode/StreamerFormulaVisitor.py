# Generated from C:/Users/tlarsen/Documents/AlteryxStreams/StreamerFormula\StreamerFormula.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .StreamerFormulaParser import StreamerFormulaParser
else:
    from StreamerFormulaParser import StreamerFormulaParser

# This class defines a complete generic visitor for a parse tree produced by StreamerFormulaParser.

class StreamerFormulaVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by StreamerFormulaParser#formula.
    def visitFormula(self, ctx:StreamerFormulaParser.FormulaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#add.
    def visitAdd(self, ctx:StreamerFormulaParser.AddContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#or.
    def visitOr(self, ctx:StreamerFormulaParser.OrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#in.
    def visitIn(self, ctx:StreamerFormulaParser.InContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#subtract.
    def visitSubtract(self, ctx:StreamerFormulaParser.SubtractContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#notEqual.
    def visitNotEqual(self, ctx:StreamerFormulaParser.NotEqualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#integer.
    def visitInteger(self, ctx:StreamerFormulaParser.IntegerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#parenthesis.
    def visitParenthesis(self, ctx:StreamerFormulaParser.ParenthesisContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#equal.
    def visitEqual(self, ctx:StreamerFormulaParser.EqualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#datetimeLiteral.
    def visitDatetimeLiteral(self, ctx:StreamerFormulaParser.DatetimeLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#func.
    def visitFunc(self, ctx:StreamerFormulaParser.FuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#field.
    def visitField(self, ctx:StreamerFormulaParser.FieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#stringLiteral.
    def visitStringLiteral(self, ctx:StreamerFormulaParser.StringLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#and.
    def visitAnd(self, ctx:StreamerFormulaParser.AndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#elseIf.
    def visitElseIf(self, ctx:StreamerFormulaParser.ElseIfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#lessThan.
    def visitLessThan(self, ctx:StreamerFormulaParser.LessThanContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#dateLiteral.
    def visitDateLiteral(self, ctx:StreamerFormulaParser.DateLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#divide.
    def visitDivide(self, ctx:StreamerFormulaParser.DivideContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#greaterEqual.
    def visitGreaterEqual(self, ctx:StreamerFormulaParser.GreaterEqualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#notIn.
    def visitNotIn(self, ctx:StreamerFormulaParser.NotInContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#lessEqual.
    def visitLessEqual(self, ctx:StreamerFormulaParser.LessEqualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#decimal.
    def visitDecimal(self, ctx:StreamerFormulaParser.DecimalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#multiply.
    def visitMultiply(self, ctx:StreamerFormulaParser.MultiplyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#if.
    def visitIf(self, ctx:StreamerFormulaParser.IfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#greaterThan.
    def visitGreaterThan(self, ctx:StreamerFormulaParser.GreaterThanContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#pow.
    def visitPow(self, ctx:StreamerFormulaParser.PowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#min.
    def visitMin(self, ctx:StreamerFormulaParser.MinContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#max.
    def visitMax(self, ctx:StreamerFormulaParser.MaxContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by StreamerFormulaParser#string.
    def visitString(self, ctx:StreamerFormulaParser.StringContext):
        return self.visitChildren(ctx)



del StreamerFormulaParser