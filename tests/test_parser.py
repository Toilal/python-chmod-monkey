import pytest

from chmod_monkey.operation import Operation
from chmod_monkey.parser import parse


class TestParse(object):
    @pytest.mark.parametrize('input', ['', 'x', 'u+664', 'u+rw6', '644+u', '+111-111'])
    def test_errors(self, input):
        with pytest.raises(ValueError):
            parse(input)

    @pytest.mark.parametrize('input,expected', [
        ('+x', [Operation(source='a', operator='+', target='x')]),
        ('+rw', [
            Operation(source='a', operator='+', target='rw')
        ]),
        ('-x', [Operation(source='a', operator='-', target='x')]),
        ('-rw', [Operation(source='a', operator='-', target='rw')]),
        ('+r-w', [
            Operation(source='a', operator='+', target='r'),
            Operation(source='a', operator='-', target='w')
        ]),
        ('ugo+r-w', [
            Operation(source='ugo', operator='+', target='r'),
            Operation(source='ugo', operator='-', target='w')
        ])
    ])
    def test_letters_expected(self, input, expected):
        assert parse(input) == expected

    @pytest.mark.parametrize('input,expected', [
        ('644', [Operation(operator='=', target=int('644', 8))]),
        ('+111', [Operation(operator='+', target=int('111', 8))]),
        ('-222', [Operation(operator='-', target=int('222', 8))]),
    ])
    def test_bits_expected(self, input, expected):
        assert parse(input) == expected
