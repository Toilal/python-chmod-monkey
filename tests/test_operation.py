import os
import sys

import pytest

from chmod_monkey.operation import Operation

oct_offset = 1 if sys.version_info.major < 3 else 2


@pytest.mark.parametrize('operation,expected', [
    (Operation(source='a', operator='+', target='x'), '775'),
    (Operation(source='a', operator='-', target='x'), '664'),
    (Operation(source='a', operator='-', target='w'), '444'),
    (Operation(source='a', operator='-', target='r'), '220'),
    (Operation(source='a', operator='-', target='rw'), '' if sys.version_info.major < 3 else '0'),
    (Operation(source='go', operator='-', target='rwx'), '600'),
    (Operation(source='u', operator='-', target='w'), '464'),
])
def test_simple_flags_operation(tmpdir, operation, expected):
    filepath = os.path.join(str(tmpdir), "test")
    open(filepath, 'w').close()

    os.chmod(filepath, 0o664)
    bitfields = operation.to_mode(filepath)
    assert oct(bitfields)[oct_offset:] in expected


@pytest.mark.parametrize('operation,expected', [
    (Operation(source='o', operator='+', target='u'), '666')
])
def test_simple_copy_operation(tmpdir, operation, expected):
    filepath = os.path.join(str(tmpdir), "test")
    open(filepath, 'w').close()

    os.chmod(filepath, 0o664)
    bitfields = operation.to_mode(filepath)
    assert oct(bitfields)[oct_offset:] == expected


@pytest.mark.parametrize('operation,expected', [
    (Operation(operator='+', target=int('111', 8)), '775'),
    (Operation(operator='-', target=int('111', 8)), '664'),
    (Operation(operator='-', target=int('222', 8)), '444'),
    (Operation(operator='-', target=int('444', 8)), '220'),
    (Operation(operator='-', target=int('666', 8)), '' if sys.version_info.major < 3 else '0'),
    (Operation(operator='-', target=int('066', 8)), '600'),
    (Operation(operator='-', target=int('200', 8)), '464'),
])
def test_simple_bits_operation(tmpdir, operation, expected):
    filepath = os.path.join(str(tmpdir), "test")
    open(filepath, 'w').close()

    os.chmod(filepath, 0o664)
    bitfields = operation.to_mode(filepath)
    assert oct(bitfields)[oct_offset:] == expected
