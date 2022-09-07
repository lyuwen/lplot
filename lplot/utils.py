import os
from gettext import gettext as _
from argparse import (
    Action,
    _StoreConstAction,
    ArgumentTypeError,
    )
import yaml


__all__ = ["StoreYAMLAction", "StoreConfigAction"]


class StoreYAMLAction(Action):
    """ Read YAML file from CLI input.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        # Store yaml action
        data = self.load_yaml(parser, values)
        setattr(namespace, self.dest, data)


    def load_yaml(self, parser, values):
        """
        Load yaml from input.

        Parameters
        ----------
        parser : ArgumentParser
            An ArgumentParser object.
        values : Union[str, list, dict]
            A path to a yaml file, a yaml string or a list or dict type object.
        """
        if isinstance(values, str):
          if os.path.isfile(values) and os.path.exists(values):
            # Load the file
            with open(values, "r") as f:
              data = yaml.load(f.read(), Loader=yaml.SafeLoader)
          else:
            parser.error(_("File {} does not exists.".format(values)))
        elif isinstance(values, (list, dict)):
          data = values.copy()
        else:
          parser.error(_("Failed to parse yaml for {dest} from value {value}.".format(dest=self.dest, value=values)))
        return data


class StoreConfigAction(StoreYAMLAction):
    """
    Read configuration from CLI input.

    Load configuration for the argument parser from a yaml dictionary file.
    It can parse the arguments that are in the argument parser, using their respective
    actions, with the exception that all _StoreConstAction actions will store the value
    in the input dictionary (the type of that input should match the constant).
    The rest of the entries that are not part of the parser will be store in self.dest.

    This action aims to facilitate a yaml config file in the place of a long line of command
    line input.

    """

    def __call__(self, parser, namespace, values, option_string=None):
        yaml_data = self.load_yaml(parser, values)
        if isinstance(yaml_data, dict):
          for action in parser._actions:
            if action.dest in yaml_data:
              if isinstance(action, _StoreConstAction):
                if (action.type is not None and isinstance(yaml_data[action.dest], action.type))\
                    or isinstance(yaml_data[action.dest], type(action.const)):
                  setattr(namespace, action.dest, yaml_data.pop(action.dest))
                else:
                  type_name = action.type.__name__ if action.type is not None else type(action.const).__name__
                  parser.error(_("Invalid type for argument {dest}, expected {type}.".format(dest=action.dest, type=type_name)))
                  raise ArgumentTypeError("Invalid type for argument {dest}, expected {type}.".format(dest=action.dest, type=type_name))
              else:
                action(parser, namespace, yaml_data.pop(action.dest), option_string)
        else:
          parser.error(_("{}: Expected a dict type input.".format(self.dest)))
        setattr(namespace, self.dest, yaml_data)
