import matplotlib as mpl


class ColorWheel:
  """
  A Color Wheel

  An iterator of a list of colors.

  Parameters
  ----------
  colors  :  list of str
      List of colors in the color wheel.
  loop    :  bool, optional, default to True
      Whether to loop around and start from the beginning of the list,
      when the color wheel reaches the end.
  """


  def __init__(self, colors, loop=True):
    self.colors = list(colors)
    self._loop = loop
    self.initialize()


  def initialize(self):
    self._color_index = -1


  @property
  def colors(self):
    return self._colors


  @colors.setter
  def colors(self, colors):
    if not all([isinstance(color, str) for color in colors]):
      raise TypeError("Input colors is not a list of strings.")
    self._colors = colors


  @property
  def n_colors(self):
    return len(self.colors)


  @property
  def current_color(self):
    return self.colors[self._color_index]


  def next(self):
    self._color_index += 1
    if (self._color_index >= self.n_colors):
      if not self._loop:
        raise StopIteration("Reached the end of the color wheel.")
      self._color_index = self._color_index % self.n_colors
    return self.current_color


  def __next__(self):
    return self.next()


  def __iter__(self):
    self.initialize()
    return self


mpl_colorwheel = ColorWheel(mpl.rc_params()["axes.prop_cycle"].by_key()["color"])


if __name__ == "__main__":
  cw = mpl_colorwheel

  counter = 0
  for color in cw:
    if counter > 15:
      break
    print(counter, color, cw._color_index)
    counter += 1
