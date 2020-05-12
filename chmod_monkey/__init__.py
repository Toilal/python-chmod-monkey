"""
Add support for `os.chmod('script.sh', 'ug+x')` syntax style.
"""

import os
from contextlib import contextmanager

from .parser import parse

_default_chmod = None  # pylint:disable=invalid-name


def to_mode(filepath, mode_str, return_old_mode=False):
    """
    Convert a string based mode to a bitmask mode ready to give to os.chmod.
    :param filepath:
    :param mode_str:
    :param return_old_mode:
    :return:
    """
    mode = None
    old_mode = None
    for parsed in parse(mode_str):
        mode = parsed.to_mode(filepath, mode, return_old_mode=return_old_mode and old_mode is None)
        if isinstance(mode, tuple):
            mode, old_mode = mode
    if return_old_mode:
        return mode, old_mode
    return mode


@contextmanager
def tmp_chmod(filepath, mode_str):
    """
    Temporary change file mode in a context manager.
    :param filepath:
    :param mode_str:
    """

    new_mode, old_mode = to_mode(filepath, mode_str, return_old_mode=True)
    os.chmod(filepath, new_mode)
    try:
        yield new_mode
    finally:
        os.chmod(filepath, old_mode)


def install():
    """
    Monkeypatch os.chmod to support string input.
    """
    global _default_chmod  # pylint:disable=global-statement,invalid-name
    if _default_chmod is None:
        _default_chmod = os.chmod

        def chmod_monkey(*args, **kwargs):
            """
            os.chmod MonkeyPatch decorator function. Invoke to_mode if mode argument is not an int.
            """
            if len(args) > 0:  # pylint:disable=len-as-condition
                path = args[0]
            else:
                path = kwargs.get('path')

            if len(args) > 1:
                mode = args[1]
            else:
                mode = kwargs.get('mode')

            if path is not None and not isinstance(mode, int):
                mode = to_mode(path, mode)
                if len(args) > 1:
                    args_list = list(args)
                    args_list[1] = mode
                    args = tuple(args_list)
                else:
                    kwargs['mode'] = mode
            return _default_chmod(*args, **kwargs)

        os.chmod = chmod_monkey
