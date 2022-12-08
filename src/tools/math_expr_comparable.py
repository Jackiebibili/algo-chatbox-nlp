import functools
from sympy import limit, oo, Symbol
from sympy.core.basic import Basic
from latex2sympy2 import latex2sympy

ASC = 1
DESC = -1

# compare the growth rate of two Big-O or univariate math expressions
class ComparableMathExpr:
   def __init__(self, latex_expr_str: str):
    self.latex_expr_str = latex_expr_str
    self.prepare_expr(latex_expr_str)

   def prepare_expr(self, latex_expr_str: str):
      try:
         latex_sym = self.convert_str_expr_to_sympy(latex_expr_str)
         symbol = self.get_math_symbols(latex_sym)
         self.check_positivity(latex_sym, symbol)
         self.latex_sym = latex_sym
         self.symbol = symbol
      except MathExprBaseException as ex:
         raise ex
      except Exception as ex:
         raise MathExprBaseException(f"Latex expression {latex_expr_str} is malformed")

   def __str__(self):
      return self.latex_expr_str

   @classmethod
   def check_positivity(cls, expr: Basic, sym):
      if sym is None:
         # for constant functions, use a dummy variable for the limit
         sym = Symbol('n')
      res = limit(expr, sym, oo)
      if res < 0:  # type: ignore
         raise MathExprNegativeException()

   @classmethod
   def check_univariate(cls, symbols_set: set[Basic]):
      try:
         val = len(symbols_set) > 1
         if val: raise MathExprUnivariateException()
         return True
      except Exception as ex:
         raise ex

   @classmethod
   def convert_str_expr_to_sympy(cls, expr: str):
      res = latex2sympy(expr)
      return res

   @classmethod
   def get_math_symbols(cls, expr: Basic):
      symbols = expr.free_symbols
      cls.check_univariate(symbols)
      return iter(symbols).__next__() if len(symbols) > 0 else None


def growth_rate_compare_to(expr1: ComparableMathExpr, expr2: ComparableMathExpr):
   # for constant functions, use a dummy variable for the limit
   if expr1.symbol is None and expr2.symbol is None:
      expr1.symbol = Symbol('n')
      expr2.symbol = Symbol('n')
   elif expr1.symbol is None:
      expr1.symbol = expr2.symbol
   elif expr2.symbol is None:
      expr2.symbol = expr1.symbol

   # check the two expressions to have the same symbol (e.g. n)
   if expr1.symbol != expr2.symbol:
      raise MathExprSymbolException()
   
   try:
      comp_expr = expr1.latex_sym / expr2.latex_sym  # type: ignore
      comp_res = limit(comp_expr, expr1.symbol, oo)

      if comp_res == oo:
         return 1
      elif comp_res == 0:
         return -1
      else:
         # a constant, e.g. one function can be written as a constant times the other function
         return 0
   except Exception as ex:
      raise MathExprBaseException(f"Cannot compare expressions {str(expr1)} and {str(expr2)}")


def get_comparison_sign(out: int):
   if out > 0:
      return ">"
   elif out < 0:
      return "<"
   else:
      return "=="


def get_ordered_functions_growth_rate(exprs: list[str], order=ASC):
   def print_comparison_result(acc: list[str], cur: ComparableMathExpr, other: ComparableMathExpr):
      acc.append(" ".join([
         str(cur),
         get_comparison_sign(growth_rate_compare_to(cur, other)),
         str(other)
         ]))
      return acc

   fns = map(lambda x: ComparableMathExpr(x), exprs)
   try:
      fns = sorted(fns, key=functools.cmp_to_key(growth_rate_compare_to), reverse=order==DESC)
   except MathExprBaseException as ex:
      raise ex
   except Exception as ex:
      raise MathExprBaseException(f"Cannot compare given expressions. Error: {str(ex)}")
   
   # print results
   # results = []
   # for idx in range(len(fns) - 1):
   #    print_comparison_result(results, fns[idx], fns[idx + 1])
   # return results
   return list(map(lambda x: str(x), fns))


# custom exception classes
class MathExprBaseException(Exception):
   def __init__(self, msg: str):
      super().__init__(msg)

class MathExprNegativeException(MathExprBaseException):
   def __init__(self):
      super().__init__("Expression cannot be negative")

class MathExprUnivariateException(MathExprBaseException):
   def __init__(self):
      super().__init__("Expression must be univariate in order to compare.")

class MathExprSymbolException(MathExprBaseException):
   def __init__(self):
      super().__init__("Variable in the expressions must be the same symbol")



# test
# print(get_ordered_functions_growth_rate([
#    '0','2','3'
# ]))
# print(get_ordered_functions_growth_rate([
#    '100n^2', "3n^3", "3n", "1"
# ]))
# print(get_ordered_functions_growth_rate([
#    'n!', "n^n", "2^n", "\\log_2n"
# ]))
