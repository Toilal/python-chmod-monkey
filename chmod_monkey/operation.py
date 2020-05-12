"""
Operation
"""

import os
import stat

BITS = "0123456789"
FLAGS = "rwxXst"
COPY = "ugo"

_BIT_MAPPING = {
    "a": {
        "r": stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH,
        "w": stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH,
        "x": stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    },
    "u": {
        "r": stat.S_IRUSR,
        "w": stat.S_IWUSR,
        "x": stat.S_IXUSR
    },
    "g": {
        "r": stat.S_IRGRP,
        "w": stat.S_IWGRP,
        "x": stat.S_IXGRP
    },
    "o": {
        "r": stat.S_IROTH,
        "w": stat.S_IWOTH,
        "x": stat.S_IXOTH
    }
}


class Operation(object):
    """
    An operation to perform on file permissions.
    """

    def __init__(self, source=None, operator=None, target=None):
        self.source = source
        self.operator = operator
        self.target = target

    @property
    def target_mode(self):
        """
        Retrieve target mode from target
        """
        if isinstance(self.target, int):
            return TARGET_MODE_BITS
        if self.target is not None and self.target:
            if self.target[0] in BITS:
                return TARGET_MODE_BITS
            if self.target[0] in FLAGS:
                return TARGET_MODE_FLAGS
            if self.target[0] in COPY:
                return TARGET_MODE_COPY
        return None

    def to_mode(self, filepath=None, mode=None, return_old_mode=False):
        """
        Converts the operation to mode ready to apply with os.chmod
        :param filepath: actual filepath. Used to get actual mode if not given.
        :param mode: actual mode.
        :param return_old_mode: If true, return will be a tuple (new_mode, old_mode)
        """
        if self.operator != '=':
            if mode is None:
                if not filepath:
                    raise ValueError(
                        "filepath or mode parameter must be defined for \"%s\" operator" % (self.operator,))
                mode = stat.S_IMODE(os.lstat(filepath).st_mode)
        else:
            mode = 0

        if self.target_mode == TARGET_MODE_FLAGS:
            new_mode = self._flags_to_mode(mode)
        elif self.target_mode == TARGET_MODE_COPY:
            new_mode = self._copy_to_mode(mode)
        elif self.target_mode == TARGET_MODE_BITS:
            new_mode = self._bits_to_mode(mode)
        else:
            raise ValueError("Target mode value is invalid (%i)" % (self.target_mode,))

        return new_mode if not return_old_mode else (new_mode, mode)

    def _flags_to_mode(self, mode):
        for source in self.source:
            for target in self.target:
                bit = _BIT_MAPPING[source][target]
                if self.operator == '-':
                    mode = mode & ~ bit
                else:
                    mode = mode | bit
        return mode

    def _copy_to_mode(self, mode):
        for source in self.source:
            for target in self.target:
                flags = ''
                for flag in 'rwx':
                    try:
                        target_bit = _BIT_MAPPING[target][flag]
                        if bool(mode & target_bit):
                            flags += flag
                    except KeyError:
                        continue
                for flag in flags:
                    bit = _BIT_MAPPING[source][flag]
                    if self.operator == '-':
                        mode = mode & ~ bit
                    else:
                        mode = mode | bit
        return mode

    def _bits_to_mode(self, mode):
        if self.operator == '-':
            return mode & ~ self.target  # pylint:disable=invalid-unary-operand-type
        return mode | self.target

    def clone(self):
        """
        Clone the operation
        """
        return Operation(source=self.source, operator=self.operator, target=self.target)

    def __repr__(self):
        return ''.join([x for x in (self.source, self.operator, self.target) if x is not None])

    def __hash__(self):
        return hash(self.source) + hash(self.operator) + hash(self.target)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and \
               self.source == other.source and \
               self.operator == other.operator and \
               self.target == other.target


TARGET_MODE_COPY = 2
TARGET_MODE_FLAGS = 1
TARGET_MODE_BITS = 0
