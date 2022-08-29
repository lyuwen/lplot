import ast
import numpy as np
from numbers import Number
from typing import Union

import lplot.lmath as lmath
import lplot.unit_conversion as unit_conversion
import lplot.physical_constant as constant


def _safety_check(locals: dict):
  """
  Safty check for input local variables.

  The implementation of ``safe_eval`` was potentially dangerous where the variable
  passed in is derived from the above types but with the operators overridded
  with malicious code. This ``_safety_check`` function negate the danger by explicitly
  check the types of each variable against the built-in number types and numpy number
  tyoes..
  """
  allowed_data_type = [int, float, complex, #np.int, np.float, np.complex, # These are deprecated
      np.int8, np.int16, np.int32, np.int64,
      np.float16, np.float32, np.float64, np.float128,
      np.complex64, np.complex128, np.complex256,
      ]
  if type(locals) != dict:
    raise TypeError("Input variables 'locals' is not a dict type.")
  for key, value in locals.items():
    if not ((type(value) in allowed_data_type) \
        or \
        ((type(value) == np.ndarray) and value.dtype.type in allowed_data_type)):
      raise TypeError("Type of input local variables '{name}' is not supported".format(name=key))



def safe_eval(node_or_string: Union[str, ast.AST], locals: dict={}):
  """
  Safely evaluate expression with some supported functions and local variables.

  Adapted from Python's built in ast.literal_eval function, this function provides more
  numerical flexibility while trying to be as safe as possible.

  Parameters
  ----------
  node_or_string : str or ast.AST
      The expression to evaluate.
  locals : dict
      Only generic number types, numpy number types, and numpy.ndarray are supported as local variables.
  """
  _safety_check(locals)
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
        left = _convert(node.left)
        right = _convert(node.right)
        if isinstance(node.op, (ast.Add, ast.Sub)):
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


def eval_slice(slice, locals: dict={}):
  if isinstance(slice, ast.Constant):
    return safe_eval(slice, locals=locals)
  elif isinstance(slice, ast.Slice):
    return slice(
        safe_eval(slice.lower, locals=locals),
        safe_eval(slice.upper, locals=locals),
        safe_eval(slice.step,  locals=locals),
        )
  elif isinstance(slice, ast.List):
    return [safe_eval(elt, locals=locals) for elt in slice.elts]
  elif isinstance(slice, ast.Tuple):
    return tuple([safe_eval(elt, locals=locals) for elt in slice.elts])
  else:
    raise TypeError("Unsupported slice type for '{slice}'.".format(slice=slice))


def safe_assign(target: Union[str, ast.AST], value: any, locals: dict={}):
  if isinstance(target, str):
    target = ast.parse(target, mode='exec')
  if isinstance(target, ast.Expression):
    target = target.body
  if isinstance(target, ast.Name):
    locals[target.id] = value
  elif isinstance(target, ast.Attribute):
    setattr(locals[target.value.id], target.attr, value)
  elif isinstance(target, ast.Subscript):
    slice = eval_slice(target.slice, locals=locals)
    locals[target.id][slice] = value
  else:
    raise TypeError("Unsupported target type for '{target!s}'.".format(target=target))


def safe_exec(node: Union[str, ast.AST], locals: dict={}):
  #  exec(node, locals)
  #  return
  if isinstance(node, str):
    node = ast.parse(node, mode='exec')
  if isinstance(node.body, list):
    for n in node.body:
      if isinstance(n, ast.Assign):
        targets = n.targets
        value = safe_eval(n.value, locals=locals)
        if isinstance(value, (tuple, list)) and len(value) == len(targets):
          for i in range(len(targets)):
            safe_assign(targets[i], value[i], locals=locals)
        elif len(targets) == 1:
          safe_assign(targets[0], value, locals=locals)
        else:
          raise ValueError("Mismatch between number of targets and number of values in the expression.")
      elif isinstance(n, ast.AugAssign):
        target = safe_eval(n.target, locals=locals)
        value = safe_eval(n.value, locals=locals)
        if isinstance(n.op, ast.Add):
          target += value
        elif isinstance(n.op, ast.Sub):
          target -= value
        elif isinstance(n.op, (ast.Mult)):
          target *= value
        elif isinstance(n.op, (ast.Div)):
          target /= value
        elif isinstance(n.op, (ast.FloorDiv)):
          target //= value
        elif isinstance(n.op, (ast.Mod)):
          target %= value
      else:
        raise RuntimeError("Expression not supported.")


def main():
  print("test")
  exp = "x + 3"
  array = np.zeros((6, ), dtype=int)
  print(safe_eval(exp, locals={"x": array}))


if __name__ == '__main__':
  main()

