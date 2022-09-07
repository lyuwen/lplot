import glob
import argparse
import numpy as np
from typing import Union
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod, abstractproperty

from lplot.safe_eval import safe_exec
from lplot.wheels import Wheel, mpl_colorwheel, wheel_of_markers, wheel_of_linestyles, wheel_of_none


class Backend(ABC):
  """ Abstract class for the plotting backend.
  """

  @abstractmethod
  def __init__(self, display, dim):
    self.display = display

  @property
  def display(self):
    return self._display

  @display.setter
  def display(self, display):
    self._display = display

  @abstractmethod
  def show(self):
    """ Show the plot.
    """
    return NotImplemented


  @abstractmethod
  def savefig(self, *args, **kwargs):
    """ Save the plot into a file.
    """
    return NotImplemented


class MPLBackend(Backend):
  """ Matplotlib plotting backend.

  Parameters
  ----------
  display: bool
      Whether the image will be displayed. Different MPL backend will be chosen
      depending on this option.
  dim: Union[tuple[float, float], str], default to (6.4, 4.8)
      Dimension of the figure.
  """

  def __init__(self, display: bool, dim: Union[tuple[float, float], str]=(6.4, 4.8)):
    self.display = display
    import matplotlib.pyplot as plt
    if isinstance(dim, str):
      x, y = dim.split("x")
      dim = (float(x), float(y))
    figure, ax = plt.subplots(figsize=dim)
    self._plot_engine = plt
    self._plot_handle = ax
    self._features = {
      "plot": "plot",
      "scatter": "scatter",
      "histogram": "hist", 
      "pie": "pie",
      "bar": "bar",
      }


  def get_default_fontsize(self) -> Union[float, str]:
    """ Get default font size from the plotting backend.
    """
    return self._plot_engine.rcParams["axes.titlesize"]


  @Backend.display.setter
  def display(self, display: bool):
    self._display = display
    if not display:
      import matplotlib as mpl
      mpl.use("Agg")


  def __getattr__(self, attr: str) -> callable:
    if attr not in self._features:
      raise AttributeError("Attribite: {attr} not defined.".format(attr=attr))
    return getattr(self._plot_handle, self._features[attr])


  def configure_plot(self, configs: dict):
    """
    Configure the plot.

    Parameters
    ----------
    configs: dict
        Configurations to apply to the plot.
    """
    ax = self._plot_handle
    ax.set_title(configs.get("title", None), fontsize=configs["fontsize"])
    ax.set_xlim(
        configs.get("xmin", None),
        configs.get("xmax", None),
        )
    ax.set_ylim(
        configs.get("ymin", None),
        configs.get("ymax", None),
        )
    ax.set_xlabel(configs.get("xlabel", None), fontsize=configs["fontsize"])
    ax.set_ylabel(configs.get("ylabel", None), fontsize=configs["fontsize"])
    if "xticks" in configs:
      ax.set_xticks([float(i) for i in configs.get("xticks")])
      if "xticklabels" in configs:
        ax.set_xticklabels(configs.get("xticklabels"), fontsize=configs["fontsize"])
    if "yticks" in configs:
      ax.set_yticks([float(i) for i in configs.get("yticks")])
      if "yticklabels" in configs:
        ax.set_yticklabels(configs.get("yticklabels"), fontsize=configs["fontsize"])
    if configs.get("has_legend", False):
      #  ax.legend()
      #remove duplicates
      handles, labels = ax.get_legend_handles_labels()
      newLabels, newHandles = [], []
      for handle, label in zip(handles, labels):
        if label not in newLabels:
          newLabels.append(label)
          newHandles.append(handle)
      ax.legend(newHandles, newLabels)


  def show(self):
    """ Show the plot.
    """
    self._plot_engine.show()


  def savefig(self, *args, **kwargs):
    """ Save the plot into a file.
    """
    self._plot_engine.savefig(*args, **kwargs)


backends = {
    "matplotlib": MPLBackend,
    }


class Plot:
  """
  Plot object

  Parameters
  ----------
  title: str
      Title of the plot.
  """


  _valid_keys = ["linestyle", "marker", "color", "linewidth", "markercolor", "markersize",
      "legend", "xmin", "xmax", "ymin", "ymax", "fontsize", "xticks", "xticklabels",
      "yticks", "yticklabels", "xlabel", "ylabel"
      ]
  _item_specific_keys = ["linestyle", "marker", "color", "markercolor", "legend", ]
  _item_specific_keys_allow_fail = ["legend", ]


  def __init__(
      self,
      title: str=None,
      ):
    self._title = title
    self._X = []
    self._Y = []
    self._datalabel = []
    self._figure_properties = {}


  def add_data(
      self,
      data: Union[str, np.ndarray],
      data_range: Union[str, slice, list],
      transform: str=None,
      file_mode: bool=False,
      ):
    """
    Add new dateset,

    Parameters
    ----------
    data: Union[str, np.ndarray]
        Dataset of path to the dataset file.
    data_range: Union[str, slice, list]
        Columns of the data to use.
    transform: str, default to None
        Transformation to operate on the dataset.
    file_mode: bool, default toFalse
        Whether the whole file is treated as a single dataset.
    """
    if isinstance(data, str):
      filename = data
      data = np.loadtxt(data)
    else:
      filename = "Dataset({n})".format(n=len(self._X))
    if not isinstance(data, np.ndarray):
      raise TypeError("Input data is expected to be a str to a datafile or a numpy array.")
    if len(data.shape) == 1:
      data = np.array([np.arange(len(data)), data]).T
    if len(data.shape) != 2:
      raise ValueError("Input data is expected to be either 1 or 2 dimentional.")
    x = data[:, 0]
    y = data[:, 1:]
    if data_range is not None:
      delimiter = ".."
      if isinstance(data_range, str):
        data_range_str = data_range
        data_range = []
        for i in data_range_str.split(","):
          if i.find(delimiter) > -1:
            slice_spec = i.split(delimiter)
            start = int(slice_spec.pop(0).strip() or 0)
            stop = int(slice_spec.pop(0).strip() or y.shape[1])
            step = 1
            if slice_spec:
              step = int(slice_spec.pop(0).strip() or 1)
            for ii in range(start, stop, step):
              data_range.append(ii)
          else:
            data_range.append(int(i))
      elif not isinstance(data_range, (list, slice)):
        raise TypeError("Input data_range is expected to be a str, list or slice.")
      y = y[:, data_range]
    if transform is not None:
      data = {"x": x, "y": y}
      safe_exec(transform, locals=data)
      x = data["x"]
      y = data["y"]
    if file_mode:
      # Treat the entire file as a single dataset.
      self._X.append(x)
      self._Y.append(y)
      self._datalabel.append(filename)
    else:
      # Treat each column of the file as separate dataset.
      for i in range(y.shape[1]):
        self._X.append(x)
        self._Y.append(y[:, i])
        self._datalabel.append("{} {}".format(filename, i))


  def set_transform(
      self,
      transform: str,
      ):
    """
    Perform tranformation operation on the dataset.

    Parameters
    ----------
    transform: str, default to None
        Transformation to operate on the dataset.
    """
    data = {"x": self._X, "y": self._Y}
    safe_exec(transform, locals=data)
    self._X = data["x"]
    self._Y = data["y"]


  def set_figure_property(
      self,
      key: str,
      value: Union[str, int, float],
      ):
    """
    Update a single figure property.

    Parameters
    ----------
    key: str
        Name of the figure property.
    value: Union[str, int, float]
        Value of the figure property.
    """
    if key in self._valid_keys:
      self._figure_properties[key] = value


  def set_figure_properties(
      self,
      properties: dict,
      ):
    """
    Update a bunch of figure properties.

    Parameters
    ----------
    properties: dict
        A dictionary of figure properties.
    """
    properties = properties.copy()
    for key in self._valid_keys:
      if key in properties:
        self._figure_properties.update({key: properties.pop(key)})
        if key in self._item_specific_keys:
          self._check_item_specific_key(key)


  def _check_item_specific_key(self, key: str):
    """
    Check whether the item specific key has the correct length.

    Parameters
    ----------
    key: str
        Name of the figure property.
    """
    if key in self._item_specific_keys:
      if isinstance(self._figure_properties[key], str):
        self._figure_properties[key] = self._figure_properties[key].split(",")
      if len(self._figure_properties[key]) == 1:
        if self._figure_properties[key][0] == "auto":
          self._figure_properties[key] = "auto"
        else:
          self._figure_properties[key] = self._figure_properties[key] * self.n_datasets
      elif (len(self._figure_properties[key]) != self.n_datasets) and (key not in self._item_specific_keys_allow_fail):
        raise ValueError("Length of property configs for '{key}' does not match length of datasets.".format(key=key))


  @property
  def n_datasets(self) -> int:
    """ Number of datasets.

    Returns
    -------
    n_datasets: int
    """
    return len(self._X)


  def make_plot(
      self,
      mode: str="plot",
      backend: str="matplotlib",
      show: bool=True,
      output: str=None,
      ):
    """
    Create the plot

    Parameters
    ----------
    mode: str, default to "plot"
        Mode of the plot.
    backend: str, default to "matplotlib"
        The plotting engine to actually draw the figure.
    show: bool, default to True
        Whether to show the figure.
    output: str, default to None
        Path to the output file for the figure to save into,
        if None, the figure won't be saved.
    """
    if backend in backends:
      backend = backends[backend](display=show)
    elif callable(backend):
      backend = backend(display=display)
    if len(self._Y) != self.n_datasets:
      raise ValueError("Length of X and Y does not match.")
    #
    if "color" in self._figure_properties:
      color = iter(self._figure_properties["color"])
    else:
      color = mpl_colorwheel
    if "linestyle" in self._figure_properties:
      linestyle = iter(self._figure_properties["linestyle"])
    else:
      linestyle = Wheel(["-"])
      #  linestyle = wheel_of_linestyles
    if "marker" in self._figure_properties:
      marker = iter(self._figure_properties["marker"])
    else:
      marker = wheel_of_none
    if "markercolor" in self._figure_properties:
      markercolor = iter(self._figure_properties["markercolor"])
    else:
      markercolor = wheel_of_none
    if "legend" in self._figure_properties:
      if self._figure_properties["legend"] == "auto":
        legend = iter(self._datalabel)
      else:
        if len(self._figure_properties["legend"]) != self.n_datasets:
          raise ValueError("Length of legend does not match the number of datasets.")
        legend = iter(self._figure_properties["legend"])
      has_legend = True
    else:
      legend = wheel_of_none
      has_legend = False
    #
    for i in range(self.n_datasets):
      getattr(backend, mode)(
          self._X[i], self._Y[i],
          linestyle=next(linestyle),
          marker=next(marker),
          color=next(color),
          markerfacecolor=next(markercolor),
          label=next(legend),
          )

    properties = self._figure_properties.copy()
    for key in self._item_specific_keys:
      properties.pop(key, None)
    properties["title"] = self._title
    properties.setdefault("fontsize", backend.get_default_fontsize())
    properties.setdefault("has_legend", has_legend)
    backend.configure_plot(properties)
    if output:
      backend.savefig(output)
    if show:
      backend.show()



def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--file-mode", "--fs", "--fm", action="store_true", help="Treat each file as a dataset. Default is treating each column as a dataset.")
  parser.add_argument("--title", "-T", help="Title of the plot.")
  parser.add_argument("--transform", "-t", help="Transform input dateset.")
  #
  group = parser.add_mutually_exclusive_group()#title='plot mode')
  group.add_argument("--mode", default="plot", choices=["plot"], help="Plot modes.")
  #  group.add_argument("--mode", default="plot", choices=["plot", "scatter", "histogram", "pie", "bar"], help="Plot modes.")
  #  group.add_argument('--plot', action="store_const", const="plot", dest="mode", help='Plot lines')
  #  group.add_argument('--scatter', action="store_const", const="scatter", dest="mode", help='Scatter plot')
  #  group.add_argument('--histogram', action="store_const", const="histogram", dest="mode", help='Histogram plot')
  #  group.add_argument('--pie', action="store_const", const="pie", dest="mode", help='Pie plot')
  #  group.add_argument('--bar', action="store_const", const="bar", dest="mode", help='Bar plot')
  # Plot configs
  parser.add_argument("--dim", default="6.4x4.8", help="Plot dimension.")
  parser.add_argument("--linestyle", "--ls", "-l", help="Line styles.")
  parser.add_argument("--marker", "-m", help="Marker styles.")
  parser.add_argument("--color", "--linecolor", "--lc", "-c", help="Line colors.")
  parser.add_argument("--linewidth", "--lw", help="Line colors.")
  parser.add_argument("--markercolor", "--mc", help="Symbol colors.")
  parser.add_argument("--markersize", "--ms", type=float, help="Symbol colors.")
  parser.add_argument("--legend", "-g", nargs="?", const="auto", help="Legends for datasets.")
  parser.add_argument("--auto-legend", "-G", dest="legend", action="store_const", const="auto", help="Automatic legends for datasets.")
  parser.add_argument("--xmin", type=int, help="Lower boundary of x value in the plot.")
  parser.add_argument("--xmax", type=int, help="Higher boundary of x value in the plot.")
  parser.add_argument("--ymin", type=int, help="Lower boundary of y value in the plot.")
  parser.add_argument("--ymax", type=int, help="Higher boundary of y value in the plot.")
  parser.add_argument("--fontsize", type=float, help="Fontsize.")
  parser.add_argument("--xticks", "--xt", help="Tick points for x axis.")
  parser.add_argument("--xticklabels", "--xtl", help="Tick labels for x axis.")
  parser.add_argument("--yticks", "--yt", help="Tick points for y axis.")
  parser.add_argument("--yticklabels", "--ytl", help="Tick labels for y axis.")
  parser.add_argument("--xlabel", "--xl", help="Label for x axis.")
  parser.add_argument("--ylabel", "--yl", help="Label for y axis.")
  #
  parser.add_argument("--show", "-p", action="store_true", help="Show plot.")
  parser.add_argument("--output", "--savefig", "-o", help="Save plot to file.")
  parser.add_argument("data", nargs="*", help="Data files. With the format <path to file>:<columns>:<transformation>, " \
      "one can select columns of the data files and apply transformation immediately")

  try:
    import argcomplete
    argcomplete.autocomplete(parser)
  except ImportError:
    pass

  args = parser.parse_args()

  plot = Plot(title=args.title)

  for file_range_transform in args.data:
    file_range_transform = file_range_transform.split(":")
    file = file_range_transform.pop(0)
    data_range = None
    transform = None
    if file_range_transform:
      data_range = file_range_transform.pop(0).strip() or None
    if file_range_transform:
      transform = file_range_transform.pop(0).strip()
    for f in glob.glob(file):
      plot.add_data(
          data=f,
          data_range=data_range,
          transform=transform,
          file_mode=args.file_mode,
          )
  if args.transform:
    plot.set_transform(args.transform)
  #
  figure_properties = {key:getattr(args, key) for key in plot._valid_keys if getattr(args, key, None) is not None}
  plot.set_figure_properties(figure_properties)
  #
  plot.make_plot(
      mode=args.mode,
      show=args.show,
      output=args.output,
      )


if __name__ == '__main__':
  main()

