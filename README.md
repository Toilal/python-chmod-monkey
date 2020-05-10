# python-chmod-monkey

[![PyPI](https://img.shields.io/pypi/v/chmod-monkey)](https://pypi.org/project/chmod-monkey/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/chmod-monkey)
![PyPI - License](https://img.shields.io/pypi/l/chmod-monkey)
[![Build Status](https://img.shields.io/travis/Toilal/python-chmod-monkey.svg)](https://travis-ci.org/Toilal/python-chmod-monkey)
[![Code coverage](https://img.shields.io/coveralls/github/Toilal/python-chmod-monkey)](https://coveralls.io/github/Toilal/python-chmod-monkey)

Add support for `os.chmod('script.sh', 'ug+x')` syntax style.

Almost any expression supported by [GNU Coreutils chmod](https://linux.die.net/man/1/chmod) should be supported by this module.

**`[ugoa]*([-+=]([rwx]*|[ugo]))+|[-+=][0-7]+`**

`Xst` flags are not supported though.

## Install

```
pip install chmod-monkey
```

## Usage

There are two ways to use `chmod-monkey`.

### Using os.chmod MonkeyPatch

```python
import os

import chmod_monkey
chmod_monkey.install()  # Install monkeypatch because we are evil !

os.chmod('script.sh', 'ug+x')  # Magic :)
```

### Using to_mode converter

```python
import os

from chmod_monkey import to_mode

os.chmod('script.sh', to_mode('ug+x'))  # For serious people.
```
