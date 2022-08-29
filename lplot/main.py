import ast
import argparse
import numpy as np
import matplotlib.pyplot as plt

from lplot.safe_eval import safe_exec


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
      title=None,
      backend="matplotlib",
      display=True,
      ):
    self._title = title
    self._X = []
    self._Y = []
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


  def add_data(
      self,
      data,
      transform=None,
      file_mode=False,
      ):
    if isinstance(data, str):
      data = np.loadtxt(data)
    if not isinstance(data, np.ndarray):
      raise TypeError("Input data is expected to be a str to a datafile or a numpy array.")
    if len(data.shape) == 1:
      data = np.array([np.arange(len(data)), data]).T
    if len(data.shape) != 2:
      raise ValueError("Input data is expected to be either 1 or 2 dimentional.")
    x = data[:, 0]
    y = data[:, 1:]
    if transform is not None:
      data = {"x": x, "y": y}
      safe_exec(transform, locals=data)
      x = data["x"]
      y = data["y"]
    if file_mode:
      # Treat the entire file as a single dataset.
      sekf._X.append(x)
      sekf._Y.append(y)
    else:
      # Treat each column of the file as separate dataset.
      for i in range(y.shape[1]):
        self._X.append(x)
        self._Y.append(y[:, i])


  def set_transform(
      self,
      transform,
      ):
    data = {"x": self._X, "y": self._Y}
    print(transform, data)
    safe_exec(transform, locals=data)
    self._X = data["x"]
    self._Y = data["y"]


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
  parser.add_argument("--title", "-T", help="Title of the plot.")
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

  print(args)

  plot = Plot(title=args.title)

  for file_transform in args.data:
    file_transform = file_transform.split(":")
    file = file_transform.pop(0)
    transform = None
    if file_transform:
      transform = file_transform.pop(0)
    plot.add_data(
        data=file,
        transform=transform,
        file_mode=args.file_mode,
        )
  print(f"{plot._X=}")
  print(f"{plot._Y=}")
  if args.transform:
    plot.set_transform(args.transform)
  print(f"{plot._X=}")
  print(f"{plot._Y=}")
  #
  #  plt.show()


if __name__ == '__main__':
  main()

