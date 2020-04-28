import unittest
from formula_visitor import FormulaVisitor


class FormulaVisitorTests(unittest.TestCase):
    def test_basic_expressions(self):
        fields = {}
        visitor = FormulaVisitor(fields)
        self.assertEqual(6, visitor.calculate('4 + 2'))
        self.assertEqual(4, visitor.calculate('6 - 2'))
        self.assertEqual(8, visitor.calculate('4 * 2'))
        self.assertEqual(4, visitor.calculate('8 / 2'))
        self.assertEqual(True, visitor.calculate('2 = 2'))
        self.assertEqual(True, visitor.calculate('3 > 2'))
        self.assertEqual(True, visitor.calculate('3 >= 2'))
        self.assertEqual(True, visitor.calculate('2 < 3'))
        self.assertEqual(True, visitor.calculate('2 <= 3'))
        self.assertEqual(True, visitor.calculate('2 != 3'))
        self.assertEqual(True, visitor.calculate('1 = 1 AND 2 = 2'))
        self.assertEqual(True, visitor.calculate('1 = 1 && 2 = 2'))
        self.assertEqual(True, visitor.calculate('2 = 2 OR 3 = 2'))
        self.assertEqual(True, visitor.calculate('2 = 2 || 3 = 2'))
        self.assertEqual(12, visitor.calculate('2 * 3 + 6'))
        self.assertEqual(18, visitor.calculate('2 * (3 + 6)'))
        self.assertEqual(True, visitor.calculate('0 IN (0,2,3,4,5)'))
        self.assertEqual(False, visitor.calculate('0 IN (1,2,3,4,5)'))
        self.assertEqual(True, visitor.calculate('0 NOT IN (1,2,3,4,5)'))
        self.assertEqual(False, visitor.calculate('0 NOT IN (0,2,3,4,5)'))


if __name__ == '__main__':
    unittest.main()
