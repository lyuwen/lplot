import math


gcd = math.gcd


def factorial(x: int) -> int:
  """ Compute factorial of input x -> x!.
  """
  return x * factorial(x - 1) if x != 1 else 1
