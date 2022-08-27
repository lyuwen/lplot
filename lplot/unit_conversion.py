class UnitConversion:
  """Find unit conversion coefficients

  This class construct a graph of different units and find a path within
  the graph the calculate unit conversion coefficients.

  Parameters
  ----------
  data   :   str
      Table of unit conversion data. (See below for format eamples.)
  """


  def __init__(self, data):
    self.pair, self.neighbor = self.data_parse(data)


  def __call__(self, v1, v2):
    if v1 == v2:
      return 1.0
    elif (v1, v2) in self.pair:
      return self.pair[(v1, v2)]
    else:
      path = self.find_path(self.neighbor, v1, v2)
      if path is None:
        raise ValueError("Failed to find the path between {v1} and {v2}".format(v1=v1, v2=v2))
      conversion = 1.0
      for n1, n2 in zip(path[:-1], path[1:]):
        conversion *= self.pair[(n1, n2)]
      return conversion


  @staticmethod
  def data_parse(data):
    pair={}
    neighbor = {}
    for i in data.strip().splitlines():
      i1,i2,c=i.split()
      pair[(i1,i2)]=eval(c)
      pair[(i2,i1)]=1/eval(c)
      neighbor.setdefault(i1, []).append(i2)
      neighbor.setdefault(i2, []).append(i1)
    return pair, neighbor


  @classmethod
  def find_path(cls, graph, start, end, path=[]):
    path = path + [start]
    if start == end:
      return path
    if start not in graph:
      return None
    for node in graph[start]:
      if node not in path:
        newpath = cls.find_path(graph, node, end, path)
        if newpath:
          return newpath
    return None


  def __contains__(self, item):
    return item in self.neighbor


energy = UnitConversion(data="""\
  eV   meV   1000.
  eV   THz    241.79893
  eV   cm-1  8065.54429
  Ry   eV    13.6056980659
  """)


mass = UnitConversion(data="""\
  kg    eV*sec^2/A^2   6.2415*10**-2
  amu   kg             1.66054*10**-27
  amu   eV*sec^2/A^2   1.66054*10**-27*6.2415*10**-2
  """)


pressure = UnitConversion(data="""\
  eV/A^3     GPa   160.21766208
  Ha/Bohr^3  GPa   29421.02648438959
  GPa        kbar  10.
  Gbar       GPa   100000.
  Mbar       GPa   100.
  kbar       GPa   0.1
  atm        bat   1.01325
  atm        GPa   0.000101325
  pascal     GPa   1.0E-09
  TPa        GPa   1000.
  TPa        Mbar  10.
  dyne/cm^2  GPa   1.0E-10
  """)

length = UnitConversion(data="""\
  inch        cm  2.54
  mile        km  1.6
  km          m   1000.
  m           cm  100.
  m           mm  1000.
  m           nm  10**9
  hbarG/c^3   m   1.616252*10**-35
  e^2/me/c^2  m   2.81794*10**-15
  Angstrom    m   10**-10
  ly          m   9.4605*10**15
  Bohr        Angstrom 0.529177
  """)
