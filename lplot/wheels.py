import matplotlib as mpl


class Wheel:
  """
  A Wheel

  An iterator of a list of items.

  Parameters
  ----------
  items   :  list of str
      List of items in the wheel.
  loop    :  bool, optional, default to True
      Whether to loop around and start from the beginning of the list,
      when the wheel reaches the end.
  """


  def __init__(self, items, loop=True):
    self.items = list(items)
    self._loop = loop
    self.initialize()


  def initialize(self):
    self._index = -1


  @property
  def items(self):
    return self._items


  @items.setter
  def items(self, items):
    if not all([isinstance(item, str) or item is None for item in items]):
      raise TypeError("Input items is not a list of strings.")
    self._items = items


  def __len__(self):
    return len(self.items)


  @property
  def n_items(self):
    return len(self)


  @property
  def current_item(self):
    return self.items[self._index]


  def next(self):
    self._index += 1
    if (self._index >= self.n_items):
      if not self._loop:
        raise StopIteration("Reached the end of the wheel.")
      self._index = self._index % self.n_items
    return self.current_item


  def __next__(self):
    return self.next()


  def __iter__(self):
    self.initialize()
    return self


mpl_colorwheel = Wheel(mpl.rc_params()["axes.prop_cycle"].by_key()["color"])
wheel_of_linestyles = Wheel(['-', '--', '-.', ':'])
wheel_of_markers = Wheel(['o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X'])
wheel_of_none = Wheel([None])

colorwheel = Wheel(["#3A81A2", "#B3E467", "#D3453A", "#62D7E1", "#5252B9", "#E9B7E3", "#B427B7", "#50E316", "#346A34", "#11E38C", "#FF0087", "#E7AD79"])


if __name__ == "__main__":
  import matplotlib.pyplot as plt
  for i, c in enumerate(colorwheel.items):
    plt.bar(i, 12, width=1, color=c)
  plt.show()
  #  cw = mpl_colorwheel
  #
  #  counter = 0
  #  for color in cw:
  #    if counter > 15:
  #      break
  #    print(counter, color, cw._index)
  #    counter += 1
