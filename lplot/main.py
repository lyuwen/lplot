import ast
import argparse
import numpy as np
import matplotlib.pyplot as plt

from lplot.safe_eval import safe_eval


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
    figure, ax = plt.subplots()
    self._plot_engine = plt
    self._plot_handle = ax
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
    return getattr(self._plot_handle, self._features[attr])


  def show(self):
    self._plot_engine.show()


  def savefig(self, *args, **kwargs):
    self._plot_engine.savefig(*args, **kwargs)


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


  def set_data(
      self,
      data,
      transform=None,
      ):
    pass


  def set_figure_properties(
      self,
      properties,
      ):
    pass


  def make_plot(
      self,
      show=True,
      output=None,
      ):
    pass



def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--file-mode", "--fs", "--fm", action="store_true", help="Treat each file as a dataset. Default is treating each column as a dataset.")
  parser.add_argument("--transform", "-t", help="Transform input dateset.")
  #
  group = parser.add_mutually_exclusive_group()#title='plot mode')
  #  group.add_argument("--mode", default="plot", choices=["plot", "scatter", "histogram", "pie", "bar"], help="Plot modes.")
  group.add_argument('--plot', action="store_const", const="plot", dest="mode", help='Plot lines')
  group.add_argument('--scatter', action="store_const", const="scatter", dest="mode", help='Scatter plot')
  group.add_argument('--histogram', action="store_const", const="histogram", dest="mode", help='Histogram plot')
  group.add_argument('--pie', action="store_const", const="pie", dest="mode", help='Pie plot')
  group.add_argument('--bar', action="store_const", const="bar", dest="mode", help='Bar plot')
  #
  parser.add_argument("--linestyle", "--ls", "-l", help="Line styles.")
  parser.add_argument("--marker", "-m", help="Marker styles.")
  parser.add_argument("--color", "--linecolor", "--lc", "-c", help="Line colors.")
  parser.add_argument("--linewidth", "--lw", help="Line colors.")
  parser.add_argument("--markercolor", "--mc", help="Symbol colors.")
  parser.add_argument("--markersize", "--ms", help="Symbol colors.")
  parser.add_argument("--legend", "-g", help="Legends for datasets.")
  parser.add_argument("--xmin", help="Lower boundary of x value in the plot.")
  parser.add_argument("--xmax", help="Higher boundary of x value in the plot.")
  parser.add_argument("--ymin", help="Lower boundary of y value in the plot.")
  parser.add_argument("--ymax", help="Higher boundary of y value in the plot.")
  parser.add_argument("--fontsize", help="Fontsize.")
  parser.add_argument("--xticks", "--xt", help="Tick points for x axis.")
  parser.add_argument("--xticklabels", "--xlabels", "--xtl", "--xl", help="Tick labels for x axis.")
  parser.add_argument("--yticks", "--yt", help="Tick points for y axis.")
  parser.add_argument("--yticklabels", "--ylabels", "--ytl", "--yl", help="Tick labels for y axis.")
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

