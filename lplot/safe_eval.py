import ast
import numpy as np
from numbers import Number
from typing import Union

import lplot.lmath as lmath
import lplot.unit_conversion as unit_conversion
import lplot.physical_constant as constant


def safe_eval(node_or_string: Union[str, ast.AST], locals: dict={}):
  """ Safely evaluate expression with some supported functions and local variables.

  Adapted from Python's built in ast.literal_eval function, this function provides more
  numerical flexibility with safety remaining the highest priority.

  Parameters
  ----------
  node_or_string : str or ast.AST
      The expression to evaluate.
  locals : dict
      Only generic number types, numpy number types, and numpy.ndarray are supported as local variables.
  """
  if type(locals) != dict:
    raise TypeError("Input variables 'locals' is not a dict type.")
  locals = dict(locals)
  valid_numpy_functions = [
      "sum", "sin", "cos", "tan", "arcsin", "arccos", "arctan",
      "log", "exp", "abs", "max", "min", "argmin", "argmax",
      "dot", "pi",
      ]
  valid_math_functions = [
      "gcd", "factorial",
      ]
  valid_unit_conversion_functions = [
      "energy", "mass", "pressure", "length",
      ]
  valid_constant_functions = [
      "hbar", "kB", "AMU", "THz", "eV", "Angstrom",
      ]
  if isinstance(node_or_string, str):
    node_or_string = ast.parse(node_or_string, mode='eval')
  def _raise_malformed_node(node):
    raise ValueError(f'malformed node or string: {node!r}')
  def _convert_num(node):
    if isinstance(node, ast.Call):
      return _convert_call(node)
    if not isinstance(node, ast.Constant) or type(node.value) not in (int, float, complex):
      _raise_malformed_node(node)
    return node.value
  def _convert_signed_num(node):
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
      operand = _convert_num(node.operand)
      if isinstance(node.op, ast.UAdd):
        return + operand
      else:
        return - operand
    return _convert_num(node)
  def _convert_call(node):
    if not hasattr(node.func, "id"):
      raise NameError("Syntax '{module}.{name}' not supported.".format(module=node.func.value.id, name=node.func.attr))
    args = []
    if hasattr(node, "args"):
      args = [_convert(arg) for arg in node.args]
    keywords = {}
    if hasattr(node, "keywordss"):
      keywords = {keyword.arg:_convert(keyword.value) for keyword in node.keywords}
    if node.func.id in valid_numpy_functions:
      return getattr(np, node.func.id)(*args, **keywords)
    if node.func.id in valid_math_functions:
      return getattr(lmath, node.func.id)(*args, **keywords)
    if node.func.id in valid_unit_conversion_functions:
      return getattr(unit_conversion, node.func.id)(*args, **keywords)
    if node.func.id in valid_constant_functions:
      return getattr(constant, node.func.id)(*args, **keywords)
  def _convert(node):
    if isinstance(node_or_string, ast.Expression):
      node = getattr(node, "body", node)
    if isinstance(node, ast.Name):
      if node.id in locals:
        if isinstance(locals[node.id], (Number, np.number, np.ndarray)):
          return locals[node.id]
      else:
        raise NameError("name \'{name}\' is not defined.".format(name=node.id))
    elif isinstance(node, ast.Call):
      return _convert_call(node)
    else:
      if isinstance(node, ast.Constant):
        return node.value
      elif isinstance(node, ast.Tuple):
        return tuple(map(_convert, node.elts))
      elif isinstance(node, ast.List):
        return list(map(_convert, node.elts))
      elif isinstance(node, ast.Set):
        return set(map(_convert, node.elts))
      elif isinstance(node, ast.Dict):
        if len(node.keys) != len(node.values):
          _raise_malformed_node(node)
        return dict(zip(map(_convert, node.keys),
          map(_convert, node.values)))
      elif isinstance(node, ast.BinOp):
        left = _convert_signed_num(node.left)
        right = _convert_signed_num(node.right)
        if isinstance(node.op, (ast.Add, ast.Sub)):
          if isinstance(left, (int, float)) and isinstance(right, complex):
              if isinstance(node.op, ast.Add):
                return left + right
              else:
                return left - right
        elif isinstance(node.op, (ast.Mult)):
          return left * right
        elif isinstance(node.op, (ast.Div)):
          return left / right
        elif isinstance(node.op, (ast.FloorDiv)):
          return left // right
        elif isinstance(node.op, (ast.Mod)):
          return left % right
      return _convert_signed_num(node)
  return _convert(node_or_string)


def main():
  print("test")
  exp = "length('inch', 'cm')"
  print(safe_eval(exp))


if __name__ == '__main__':
  main()

