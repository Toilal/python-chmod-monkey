import os
import stat
import sys

import pytest

from chmod_monkey import to_mode, install

oct_offset = 1 if sys.version_info.major < 3 else 2


@pytest.mark.parametrize('mode,expected', [
    ('+x', '775'),
])
def test_to_mode(tmpdir, mode, expected):
    filepath = os.path.join(str(tmpdir), "test")
    open(filepath, 'w').close()

    os.chmod(filepath, 0o664)
    assert oct(to_mode(filepath, mode))[oct_offset:] == expected


@pytest.mark.parametrize('mode,expected', [
    ('+x', int('775', 8)),
])
def test_install_args(tmpdir, mode, expected):
    filepath = os.path.join(str(tmpdir), "test")
    open(filepath, 'w').close()

    os.chmod(filepath, 0o664)

    install()
    os.chmod(filepath, "+x")
    stat.S_IMODE(os.lstat(filepath).st_mode) == expected


@pytest.mark.skipif(sys.version_info.major < 3, reason="requires python3 or higher")
@pytest.mark.parametrize('mode,expected', [
    ('+x', int('775', 8)),
])
def test_install_kwargs(tmpdir, mode, expected):
    filepath = os.path.join(str(tmpdir), "test")
    open(filepath, 'w').close()

    os.chmod(filepath, 0o664)

    install()
    os.chmod(mode="+x", path=filepath)
    stat.S_IMODE(os.lstat(filepath).st_mode) == expected