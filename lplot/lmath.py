import math


gcd = math.gcd


def factorial(x):
  return x * factorial(x - 1) if x != 1 else 1
