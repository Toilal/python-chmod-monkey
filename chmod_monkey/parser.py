"""
Parser
"""

from chmod_monkey.operation import Operation, TARGET_MODE_BITS, TARGET_MODE_FLAGS, TARGET_MODE_COPY, \
    BITS, FLAGS, COPY


def parse(mode):
    """
    Parse chmod string to a list of operations
    :param mode: A string matching GNU Coreutils chmod argument "[ugoa]*([-+=]([rwxXst]*|[ugo]))+|[-+=][0-7]+"
    :return: A list of operations to perform
    """
    operations = []

    operation = Operation()
    for _, char in enumerate(mode):
        if char in 'ugoa':
            _parse_source(char, mode, operation)
            continue

        if char in '-+=':
            operation = _parse_operator(char, mode, operation, operations)
            continue

        if char in BITS:
            _parse_bits(char, mode, operation)
            continue

        if not operation.source:
            operation.source = 'a'

        if not operation.operator:
            raise ValueError("Invalid string mode given: " + mode)

        if char in FLAGS:
            _parse_flags(char, mode, operation)
            continue

        if char in COPY:
            _parse_copy(char, mode, operation)
            continue

        raise ValueError("Invalid string mode given: " + mode)

    if not operation.target:
        raise ValueError("Invalid string mode given: " + mode)

    if operation.target_mode != TARGET_MODE_BITS and not operation.operator:
        raise ValueError("Invalid string mode given: " + mode)

    operations.append(operation)

    for operation in operations:
        if operation.target_mode == TARGET_MODE_BITS:
            operation.target = int(str(operation.target), 8)  # to octal integer

    return operations


def _parse_copy(char, mode, operation):
    if operation.target_mode and operation.target_mode != TARGET_MODE_COPY:
        raise ValueError("Invalid string mode given: " + mode)
    operation.target = operation.target + char if operation.target else char


def _parse_flags(char, mode, operation):
    if operation.target_mode and operation.target_mode != TARGET_MODE_FLAGS:
        raise ValueError("Invalid string mode given: " + mode)
    operation.target = operation.target + char if operation.target else char


def _parse_bits(char, mode, operation):
    if operation.source:
        raise ValueError("Invalid string mode given: " + mode)
    if operation.target_mode and operation.target_mode != TARGET_MODE_BITS:
        raise ValueError("Invalid string mode given: " + mode)
    operation.target = operation.target + char if operation.target else char
    if not operation.operator:
        operation.operator = '='


def _parse_operator(char, mode, operation, operations):
    if operation.target or operation.operator:
        if operation.target_mode == TARGET_MODE_BITS:
            raise ValueError("Invalid string mode given: " + mode)
        operations.append(operation)
        operation = Operation(source=operation.source, operator=char)
    else:
        operation.operator = char
    return operation


def _parse_source(char, mode, operation):
    if operation.operator:
        raise ValueError("Invalid string mode given: " + mode)
    operation.source = operation.source + char if operation.source else char
