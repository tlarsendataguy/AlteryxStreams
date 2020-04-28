# Generated from C:/Users/tlarsen/Documents/AlteryxStreams/StreamerFormula\StreamerFormula.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .StreamerFormulaParser import StreamerFormulaParser
else:
    from StreamerFormulaParser import StreamerFormulaParser

# This class defines a complete listener for a parse tree produced by StreamerFormulaParser.
class StreamerFormulaListener(ParseTreeListener):

    # Enter a parse tree produced by StreamerFormulaParser#formula.
    def enterFormula(self, ctx:StreamerFormulaParser.FormulaContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#formula.
    def exitFormula(self, ctx:StreamerFormulaParser.FormulaContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#add.
    def enterAdd(self, ctx:StreamerFormulaParser.AddContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#add.
    def exitAdd(self, ctx:StreamerFormulaParser.AddContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#or.
    def enterOr(self, ctx:StreamerFormulaParser.OrContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#or.
    def exitOr(self, ctx:StreamerFormulaParser.OrContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#in.
    def enterIn(self, ctx:StreamerFormulaParser.InContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#in.
    def exitIn(self, ctx:StreamerFormulaParser.InContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#subtract.
    def enterSubtract(self, ctx:StreamerFormulaParser.SubtractContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#subtract.
    def exitSubtract(self, ctx:StreamerFormulaParser.SubtractContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#notEqual.
    def enterNotEqual(self, ctx:StreamerFormulaParser.NotEqualContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#notEqual.
    def exitNotEqual(self, ctx:StreamerFormulaParser.NotEqualContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#integer.
    def enterInteger(self, ctx:StreamerFormulaParser.IntegerContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#integer.
    def exitInteger(self, ctx:StreamerFormulaParser.IntegerContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#parenthesis.
    def enterParenthesis(self, ctx:StreamerFormulaParser.ParenthesisContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#parenthesis.
    def exitParenthesis(self, ctx:StreamerFormulaParser.ParenthesisContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#equal.
    def enterEqual(self, ctx:StreamerFormulaParser.EqualContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#equal.
    def exitEqual(self, ctx:StreamerFormulaParser.EqualContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#func.
    def enterFunc(self, ctx:StreamerFormulaParser.FuncContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#func.
    def exitFunc(self, ctx:StreamerFormulaParser.FuncContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#field.
    def enterField(self, ctx:StreamerFormulaParser.FieldContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#field.
    def exitField(self, ctx:StreamerFormulaParser.FieldContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#stringLiteral.
    def enterStringLiteral(self, ctx:StreamerFormulaParser.StringLiteralContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#stringLiteral.
    def exitStringLiteral(self, ctx:StreamerFormulaParser.StringLiteralContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#and.
    def enterAnd(self, ctx:StreamerFormulaParser.AndContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#and.
    def exitAnd(self, ctx:StreamerFormulaParser.AndContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#elseIf.
    def enterElseIf(self, ctx:StreamerFormulaParser.ElseIfContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#elseIf.
    def exitElseIf(self, ctx:StreamerFormulaParser.ElseIfContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#lessThan.
    def enterLessThan(self, ctx:StreamerFormulaParser.LessThanContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#lessThan.
    def exitLessThan(self, ctx:StreamerFormulaParser.LessThanContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#dateLiteral.
    def enterDateLiteral(self, ctx:StreamerFormulaParser.DateLiteralContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#dateLiteral.
    def exitDateLiteral(self, ctx:StreamerFormulaParser.DateLiteralContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#divide.
    def enterDivide(self, ctx:StreamerFormulaParser.DivideContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#divide.
    def exitDivide(self, ctx:StreamerFormulaParser.DivideContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#greaterEqual.
    def enterGreaterEqual(self, ctx:StreamerFormulaParser.GreaterEqualContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#greaterEqual.
    def exitGreaterEqual(self, ctx:StreamerFormulaParser.GreaterEqualContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#notIn.
    def enterNotIn(self, ctx:StreamerFormulaParser.NotInContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#notIn.
    def exitNotIn(self, ctx:StreamerFormulaParser.NotInContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#lessEqual.
    def enterLessEqual(self, ctx:StreamerFormulaParser.LessEqualContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#lessEqual.
    def exitLessEqual(self, ctx:StreamerFormulaParser.LessEqualContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#decimal.
    def enterDecimal(self, ctx:StreamerFormulaParser.DecimalContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#decimal.
    def exitDecimal(self, ctx:StreamerFormulaParser.DecimalContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#multiply.
    def enterMultiply(self, ctx:StreamerFormulaParser.MultiplyContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#multiply.
    def exitMultiply(self, ctx:StreamerFormulaParser.MultiplyContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#if.
    def enterIf(self, ctx:StreamerFormulaParser.IfContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#if.
    def exitIf(self, ctx:StreamerFormulaParser.IfContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#greaterThan.
    def enterGreaterThan(self, ctx:StreamerFormulaParser.GreaterThanContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#greaterThan.
    def exitGreaterThan(self, ctx:StreamerFormulaParser.GreaterThanContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#pow.
    def enterPow(self, ctx:StreamerFormulaParser.PowContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#pow.
    def exitPow(self, ctx:StreamerFormulaParser.PowContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#min.
    def enterMin(self, ctx:StreamerFormulaParser.MinContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#min.
    def exitMin(self, ctx:StreamerFormulaParser.MinContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#max.
    def enterMax(self, ctx:StreamerFormulaParser.MaxContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#max.
    def exitMax(self, ctx:StreamerFormulaParser.MaxContext):
        pass


    # Enter a parse tree produced by StreamerFormulaParser#string.
    def enterString(self, ctx:StreamerFormulaParser.StringContext):
        pass

    # Exit a parse tree produced by StreamerFormulaParser#string.
    def exitString(self, ctx:StreamerFormulaParser.StringContext):
        pass



del StreamerFormulaParser