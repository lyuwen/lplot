import pytest
import numpy as np

from lplot.safe_eval import safe_eval


def test_safety_check_bad():
  with pytest.raises(TypeError) as e_info:
    class BadArray(np.ndarray):

      def __add__(self, other):
        print("The __add__ operator is maliciously overridded in this BadArray class")
        new = BadArray(self.__array__().copy())
        new[:] = 420
        return new
    variables = {
        "x": BadArray(np.zeros((10, ))),
        }
    result = safe_eval("x + 10", locals=variables)


def test_safety_check_good():
  variables = {
      "x": np.zeros((10, ), dtype=int),
      }
  result = safe_eval("x + 10", locals=variables)
  assert np.array_equal(result, np.full((10, ), 10, dtype=int))
