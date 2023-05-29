""""Load a class from a python file"""

import importlib
import os
import pathlib
import sys


def load_class(pyfile: str, class_name: str):
    """Load function_name from python file pyfile"""
    module_file = pathlib.Path(pyfile)
    if not module_file.is_file():
        raise FileNotFoundError(f"module {pyfile} does not appear to exist")

    module_dir = module_file.parent or pathlib.Path(os.getcwd())
    module_name = module_file.stem

    # store old sys.path and ensure module_dir at beginning of path
    syspath = sys.path
    sys.path = [str(module_dir)] + syspath
    module = importlib.import_module(module_name)

    try:
        class_ = getattr(module, class_name)
    except AttributeError as e:
        raise ValueError(f"'{class_name}' not found in module '{module_name}'") from e
    finally:
        # restore sys.path
        sys.path = syspath

    return class_
