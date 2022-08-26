import argparse
import numpy as np
import matplotlib.pyplot as plt


class Backend:

  def __init__(self, display):
    self.display = display

  @property
  def display(self):
    return self._display

  @display.setter
  def display(self, display):
    self._display = display


class MPLBackend(Backend):

  def __init__(self, display):
    self.display = display
    import matplotlib.pyplot as plt
    self._plot_handle = plt
    self._features = {
      "plot": "plot",
      "scatter": "scatter",
      "histogram": "hist", 
      "pie": "pie",
      "bar": "bar",
      }

  @Backend.display.setter
  def display(self, display):
    self._display = display
    if not display:
      import matplotlib as mpl
      mpl.use("Agg")

  def __getattr__(self, attr):
    if attr not in self._features:
      raise AttributeError("Attribite: {attr} not defined.".format(attr=attr))
    return 0

  def plot(*args, **kwargs):
    self._plot_handle(*args, **kwargs)


backends = {
    "matplotlib": MPLBackend,
    }


class Plot:

  def __init__(
      self,
      backend="matplotlib",
      display=True,
      ):
    self._set_backend(backend=backend, display=display)

  def _set_backend(
      self,
      backend,
      display=True,
      ):
    if backend in backends:
      self._backend = backends[backend](display=display)
    elif callable(backend):
      self._backend = backend(display=display)



def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--file-mode", "--fs", "--fm", action="store_true", help="Treat each file as a dataset. Default is treating each column as a dataset.")
  parser.add_argument("--line-styles", "--ls", "-l", help="Line styles.")
  parser.add_argument("--symbol-styles", "--ss", "-s", help="Symbol styles.")
  parser.add_argument("--line-colors", "--color", "--lc", "-c", help="Line colors.")
  parser.add_argument("--symbol-colors", "--sc", help="Symbol colors.")
  parser.add_argument("--legend", "-g", help="Legends for datasets.")
  parser.add_argument("--xmin", help="Lower boundary of x value in the plot.")
  parser.add_argument("--xmax", help="Higher boundary of x value in the plot.")
  parser.add_argument("--ymin", help="Lower boundary of y value in the plot.")
  parser.add_argument("--ymax", help="Higher boundary of y value in the plot.")
  parser.add_argument("--fontsize", help="Fontsize.")
  parser.add_argument("--xticks", "--xt", help="Tick points for x axis.")
  parser.add_argument("--xticklabels", "--xlabels", "--xtl", help="Tick labels for x axis.")
  parser.add_argument("--yticks", "--yt", help="Tick points for y axis.")
  parser.add_argument("--yticklabels", "--ylabels", "--ytl", help="Tick labels for y axis.")
  parser.add_argument("--show", "-p", action="store_true", help="Show plot.")
  parser.add_argument("--save-fig", "-o", help="Save plot to file.")
  parser.add_argument("data", nargs="*", help="Data files.")

  args = parser.parse_args()

  for file in args.data:
    data = np.loadtxt(file)
    plt.plot(data[:, 0], data[:, 1:])

  plt.show()


if __name__ == '__main__':
  main()

