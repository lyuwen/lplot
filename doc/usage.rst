Usage
=====

.. code-block:: bash

    usage: lplot [-h] [--file-mode] [--title TITLE] [--transform TRANSFORM]
                 [--plot | --scatter | --histogram | --pie | --bar] [--dim DIM]
                 [--linestyle LINESTYLE] [--marker MARKER] [--color COLOR]
                 [--linewidth LINEWIDTH] [--markercolor MARKERCOLOR]
                 [--markersize MARKERSIZE] [--legend LEGEND] [--xmin XMIN]
                 [--xmax XMAX] [--ymin YMIN] [--ymax YMAX] [--fontsize FONTSIZE]
                 [--xticks XTICKS] [--xticklabels XTICKLABELS] [--yticks YTICKS]
                 [--yticklabels YTICKLABELS] [--xlabel XLABEL] [--ylabel YLABEL]
                 [--show] [--output OUTPUT]
                 [data ...]

    positional arguments:
      data                  Data files.

    optional arguments:
      -h, --help            show this help message and exit
      --file-mode, --fs, --fm
                            Treat each file as a dataset. Default is treating each
                            column as a dataset.
      --title TITLE, -T TITLE
                            Title of the plot.
      --transform TRANSFORM, -t TRANSFORM
                            Transform input dateset.
      --plot                Plot lines
      --scatter             Scatter plot
      --histogram           Histogram plot
      --pie                 Pie plot
      --bar                 Bar plot
      --dim DIM             Plot dimension.
      --linestyle LINESTYLE, --ls LINESTYLE, -l LINESTYLE
                            Line styles.
      --marker MARKER, -m MARKER
                            Marker styles.
      --color COLOR, --linecolor COLOR, --lc COLOR, -c COLOR
                            Line colors.
      --linewidth LINEWIDTH, --lw LINEWIDTH
                            Line colors.
      --markercolor MARKERCOLOR, --mc MARKERCOLOR
                            Symbol colors.
      --markersize MARKERSIZE, --ms MARKERSIZE
                            Symbol colors.
      --legend LEGEND, -g LEGEND
                            Legends for datasets.
      --xmin XMIN           Lower boundary of x value in the plot.
      --xmax XMAX           Higher boundary of x value in the plot.
      --ymin YMIN           Lower boundary of y value in the plot.
      --ymax YMAX           Higher boundary of y value in the plot.
      --fontsize FONTSIZE   Fontsize.
      --xticks XTICKS, --xt XTICKS
                            Tick points for x axis.
      --xticklabels XTICKLABELS, --xtl XTICKLABELS
                            Tick labels for x axis.
      --yticks YTICKS, --yt YTICKS
                            Tick points for y axis.
      --yticklabels YTICKLABELS, --ytl YTICKLABELS
                            Tick labels for y axis.
      --xlabel XLABEL, --xl XLABEL
                            Label for x axis.
      --ylabel YLABEL, --yl YLABEL
                            Label for y axis.
      --show, -p            Show plot.
      --output OUTPUT, --savefig OUTPUT, -o OUTPUT
                            Save plot to file.


Tranform
--------

The tranformation of dataset can be applied as the dataset is being passed in or after all dataset have been loaded.
The operation allows a list of basic mathematical operations and physical constants only on the dataset, for security reasons.
The list of allowed operations include::

      sum, sin, cos, tan, arcsin, arccos, arctan, log, exp, abs,
      max, min, argmin, argmax, dot, pi, gcd, factorial

Some unit conversions has been built in too::

      energy, mass, pressure, length

As well as a selection of physical constants in various units::

      hbar, kB, AMU, THz, eV, Angstrom

The operation string is in the form a simple Python statement, with only the dataset variables ``x`` and ``y`` accessible along with basic
arithmetic operations and the above functions. Anything else won't be allowed.


Example
-------
.. code-block:: bash

    lplot --fs "dataset.txt:x=x+1" --title test \
        --transform "y[0]=sin(x[0]**2)" \
        --xl "X" --yl "\$\\x^2\$" \
        --show -o figure.pdf
