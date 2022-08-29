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


  @property
  def n_items(self):
    return len(self.items)


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


if __name__ == "__main__":
  cw = mpl_colorwheel

  counter = 0
  for color in cw:
    if counter > 15:
      break
    print(counter, color, cw._index)
    counter += 1
