import datetime
import unittest
from formula_visitor import calculate, FormulaVisitor, MissingFieldException


class FormulaVisitorTests(unittest.TestCase):
    def test_basic_expressions(self):
        self.assertEqual(6, calculate('4 + 2'))
        self.assertEqual(4, calculate('6 - 2'))
        self.assertEqual(4, calculate('6-2'))
        self.assertEqual(-4, calculate('-4'))
        self.assertEqual(8, calculate('4 * 2'))
        self.assertEqual(4, calculate('8 / 2'))
        self.assertEqual(True, calculate('2 = 2'))
        self.assertEqual(True, calculate('3 > 2'))
        self.assertEqual(True, calculate('3 >= 2'))
        self.assertEqual(True, calculate('2 < 3'))
        self.assertEqual(True, calculate('2 <= 3'))
        self.assertEqual(True, calculate('2 != 3'))
        self.assertEqual(True, calculate('1 = 1 AND 2 = 2'))
        self.assertEqual(True, calculate('1 = 1 && 2 = 2'))
        self.assertEqual(True, calculate('2 = 2 OR 3 = 2'))
        self.assertEqual(True, calculate('2 = 2 || 3 = 2'))
        self.assertEqual(12, calculate('2 * 3 + 6'))
        self.assertEqual(18, calculate('2 * (3 + 6)'))
        self.assertEqual(True, calculate('0 IN (0,2,3,4,5)'))
        self.assertEqual(False, calculate('0 IN (1,2,3,4,5)'))
        self.assertEqual(True, calculate('0 NOT IN (1,2,3,4,5)'))
        self.assertEqual(False, calculate('0 NOT IN (0,2,3,4,5)'))
        self.assertEqual(0, calculate('IF 0=0 THEN 0 ELSE 1 ENDIF'))
        self.assertEqual(0, calculate('IF 0=1 THEN 1 ELSE 0 ENDIF'))
        self.assertEqual('ABC', calculate('"ABC"'))
        self.assertEqual('ABC', calculate("'ABC'"))
        self.assertEqual(123.2, calculate("123.2"))
        self.assertEqual(datetime.datetime(2020, 1, 31), calculate("'2020-01-31'"))
        self.assertEqual(datetime.datetime(2020, 1, 31, 3, 4, 5), calculate("'2020-01-31 03:04:05'"))
        self.assertEqual(1, calculate('IF 0=1 THEN 0 ELSEIF 0=0 THEN 1 ELSE 2 ENDIF'))
        self.assertEqual(0, calculate('IF 0=0 THEN 0 ELSEIF 0=0 THEN 1 ELSE 2 ENDIF'))
        self.assertEqual(2, calculate('IF 0=1 THEN 0 ELSEIF 0=1 THEN 1 ELSE 2 ENDIF'))
        self.assertEqual(2, calculate('IF 0=1 THEN 0 ELSEIF 0=1 THEN 1 ELSEIF 0=0 THEN 2 ELSE 3 ENDIF'))
        self.assertEqual(8, calculate('POW(2,3)'))
        self.assertEqual(0, calculate('Min(4,8,2,4,6,0,3)'))
        self.assertEqual(8, calculate('Max(4,8,2,4,6,0,3)'))
        self.assertRaises(Exception, lambda: calculate('2 * (1 + 3'))
        self.assertEqual("ab", calculate("'a' + 'b'"))
        self.assertEqual("", calculate("''"))
        self.assertIsInstance(calculate("''"), str)

    def test_field_expressions(self):
        fields = {
            'field1': lambda: 10,
            'field2': lambda: 'a',
            'field3': lambda: 'b'
        }
        expression = '[field1]'
        self.assertEqual(10, calculate('[field1]', fields))
        self.assertEqual('ab', calculate('[field2] + [field3]', fields))

    def test_field_expressions_invalid_syntax(self):
        fields = {
            'Field1': lambda: 10
        }
        expression = '[Field1] * (2 + [Field1]'
        with self.assertRaises(Exception) as ex:
            FormulaVisitor(expression=expression, fields=fields)
            print(ex)

    def test_missing_field(self):
        fields = {
            'field1': lambda: 10
        }
        expression = '[field2]'
        visitor = FormulaVisitor(expression=expression, fields=fields)
        with self.assertRaises(MissingFieldException) as ex:
            visitor.calculate()
            print(ex)


if __name__ == '__main__':
    unittest.main()
