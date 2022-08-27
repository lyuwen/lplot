from collections import OrderedDict


class PhysicalConstant:
  """ A *physical* constant in a given units

  This class will construct a given physical constant in different units.
  with provided data at construction.

  Parameters
  ----------
  data         : str
      Table of constant values data. (See below for format eamples.)
  name         : str, optional, default to None
      Name of the constant.
  default_unit : str, optional, default to None
      The default unit for the constant.
      If None, default to the first in the provided data.

  """


  def __init__(self, data, name=None, default_unit=None):
    self._name = name
    self._constant = self.data_parse(data)
    if default_unit is not None:
      if default_unit not in self._constant.keys():
        raise KeyError("Unit {unit} does not exist.".format(unit=default_unit))
      self._default_unit = default_unit
    else:
      self._default_unit = list(self._constant.keys())[0]


  def __call__(self, unit):
    if unit in self._constant:
      return self._constant[unit]
    else:
      raise KeyError("Unit {unit} does not exist.".format(unit=unit))

  def __repr__(self):
    if self._name is not None:
      return "<{}>".format(self._name)
    else:
      return super(self.__class__, self).__repr__()

  @property
  def existing_units(self):
    return list(self._constant.keys())

  @staticmethod
  def data_parse(data):
    if isinstance(data, str):
      udict = OrderedDict()
      for i in data.strip().splitlines():
        i1, c = i.split()
        udict[i1] = eval(c)
    elif isinstance(data, dict):
      udict = OrderedDict(data)
    return udict

  def __add__(self, other):
    return self._constant[self._default_unit] + other

  def __radd__(self, other):
    return self.__add__(other)

  def __sub__(self, other):
    return self._constant[self._default_unit] - other

  def __rsub__(self, other):
    return other - self._constant[self._default_unit]

  def __mul__(self, other):
    return self._constant[self._default_unit] * other

  def __rmul__(self, other):
    return self.__mul__(other)

  def __truediv__(self, other):
    return self._constant[self._default_unit] / other

  def __rtruediv__(self, other):
    return other / self._constant[self._default_unit]

  def __floordiv__(self, other):
    return self._constant[self._default_unit] // other

  def __rfloordiv__(self, other):
    return other // self._constant[self._default_unit]

  def __mod__(self, other):
    return self._constant[self._default_unit] % other

  def __rmod__(self, other):
    return other % self._constant[self._default_unit]

  def __pow__(self, other, modulo=None):
    if modulo is not None:
      return self._constant[self._default_unit] ** other % modulo
    else:
      return self._constant[self._default_unit] ** other

  def __neg__(self):
    return - self._constant[self._default_unit]

  def __pos__(self):
    return + self._constant[self._default_unit]

  def __abs__(self):
    return abs(self._constant[self._default_unit])

  def __float__(self):
    return float(self._constant[self._default_unit])

  def __int__(self):
    return int(self._constant[self._default_unit])

  def __complex__(self):
    return complex(self._constant[self._default_unit])

  def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
    newinputs = []
    for inp in inputs:
      if isinstance(inp, self.__class__):
        newinputs.append(inp._constant[inp._default_unit])
      else:
        newinputs.append(inp)
    return getattr(ufunc, method)(*newinputs, **kwargs)


hbar = PhysicalConstant(
    name="Reduced Planck constant",
    data="""
    J*sec       1.054571800*10**-34
    eV*sec      6.582*10**-16
    cm^-1*sec   5.3088*10**-12
    """,
    default_unit="J*sec"
    )

kB = PhysicalConstant(
    name="Boltzmann constant",
    data="""
    J*K^-1       1.38064852*10**-23
    eV*K^-1      8.6173303*10**-5
    cm^-1*K^-1   0.69503476
    """,
    default_unit="J*K^-1"
    )

AMU = PhysicalConstant(
    name="Atomic mass unit",
    data="""
    Kg 1.66053904020*10**-27
    g  1.66053904020*10**-24
    eV*s^2*A^-2  1.0364*10**-28
    """,
    default_unit="Kg")

THz = PhysicalConstant(
    name="Terahertz",
    data="Hz 10**12"
    )

eV = PhysicalConstant(
    name="Electronvolt",
    data="J 1.602176634*10**-19",
    )

Angstrom = PhysicalConstant(
    name="Angstrom",
    data="m 10**-10",
    )
