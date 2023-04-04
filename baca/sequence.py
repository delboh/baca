"""
Sequence.
"""
import collections
import copy
import itertools

import abjad


def accumulate(sequence, operands=None, count=None):
    r"""
    Accumulates ``operands`` calls against sequence to identity.

    ..  container:: example

        Accumulates identity operator:

        >>> collection_1 = abjad.PitchClassSegment([0, 1, 2, 3])
        >>> collection_2 = abjad.PitchClassSegment([4, 5])
        >>> sequence = [collection_1, collection_2]
        >>> for item in baca.sequence.accumulate(sequence):
        ...     item
        ...
        [PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])]

    ..  container:: example

        Accumulates alpha:

        >>> collection_1 = abjad.PitchClassSegment([0, 1, 2, 3])
        >>> collection_2 = abjad.PitchClassSegment([4, 5])
        >>> sequence = [collection_1, collection_2]
        >>> for item in baca.sequence.accumulate(
        ...     sequence, [lambda _: baca.pcollections.alpha(_)]
        ... ):
        ...     item
        ...
        [PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])]
        [PitchClassSegment([1, 0, 3, 2]), PitchClassSegment([5, 4])]

    ..  container:: example

        Accumulates transposition:

        >>> collection_1 = abjad.PitchClassSegment([0, 1, 2, 3])
        >>> collection_2 = abjad.PitchClassSegment([4, 5])

        >>> sequence = [collection_1, collection_2]
        >>> for item in baca.sequence.accumulate(sequence, [lambda _: _.transpose(n=3)]):
        ...     item
        ...
        [PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])]
        [PitchClassSegment([3, 4, 5, 6]), PitchClassSegment([7, 8])]
        [PitchClassSegment([6, 7, 8, 9]), PitchClassSegment([10, 11])]
        [PitchClassSegment([9, 10, 11, 0]), PitchClassSegment([1, 2])]

    ..  container:: example

        Accumulates alpha followed by transposition:

        >>> collection_1 = abjad.PitchClassSegment([0, 1, 2, 3])
        >>> collection_2 = abjad.PitchClassSegment([4, 5])

        >>> sequence = [collection_1, collection_2]
        >>> for item in baca.sequence.accumulate(
        ...     sequence,
        ...     [lambda _: baca.pcollections.alpha(_), lambda _: _.transpose(n=3)]
        ... ):
        ...     item
        ...
        [PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])]
        [PitchClassSegment([1, 0, 3, 2]), PitchClassSegment([5, 4])]
        [PitchClassSegment([4, 3, 6, 5]), PitchClassSegment([8, 7])]
        [PitchClassSegment([5, 2, 7, 4]), PitchClassSegment([9, 6])]
        [PitchClassSegment([8, 5, 10, 7]), PitchClassSegment([0, 9])]
        [PitchClassSegment([9, 4, 11, 6]), PitchClassSegment([1, 8])]
        [PitchClassSegment([0, 7, 2, 9]), PitchClassSegment([4, 11])]
        [PitchClassSegment([1, 6, 3, 8]), PitchClassSegment([5, 10])]
        [PitchClassSegment([4, 9, 6, 11]), PitchClassSegment([8, 1])]
        [PitchClassSegment([5, 8, 7, 10]), PitchClassSegment([9, 0])]
        [PitchClassSegment([8, 11, 10, 1]), PitchClassSegment([0, 3])]
        [PitchClassSegment([9, 10, 11, 0]), PitchClassSegment([1, 2])]

    ..  container:: example

        Accumulates permutation:

        >>> collection_1 = abjad.PitchClassSegment([0, 1, 2, 3])
        >>> collection_2 = abjad.PitchClassSegment([4, 5])

        >>> row = abjad.TwelveToneRow([10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])
        >>> sequence = [collection_1, collection_2]
        >>> for item in baca.sequence.accumulate(sequence, [lambda _: row(_)]):
        ...     item
        ...
        [PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])]
        [PitchClassSegment([10, 0, 2, 6]), PitchClassSegment([8, 7])]
        [PitchClassSegment([4, 10, 2, 5]), PitchClassSegment([1, 3])]
        [PitchClassSegment([8, 4, 2, 7]), PitchClassSegment([0, 6])]
        [PitchClassSegment([1, 8, 2, 3]), PitchClassSegment([10, 5])]
        [PitchClassSegment([0, 1, 2, 6]), PitchClassSegment([4, 7])]
        [PitchClassSegment([10, 0, 2, 5]), PitchClassSegment([8, 3])]
        [PitchClassSegment([4, 10, 2, 7]), PitchClassSegment([1, 6])]
        [PitchClassSegment([8, 4, 2, 3]), PitchClassSegment([0, 5])]
        [PitchClassSegment([1, 8, 2, 6]), PitchClassSegment([10, 7])]
        [PitchClassSegment([0, 1, 2, 5]), PitchClassSegment([4, 3])]
        [PitchClassSegment([10, 0, 2, 7]), PitchClassSegment([8, 6])]
        [PitchClassSegment([4, 10, 2, 3]), PitchClassSegment([1, 5])]
        [PitchClassSegment([8, 4, 2, 6]), PitchClassSegment([0, 7])]
        [PitchClassSegment([1, 8, 2, 5]), PitchClassSegment([10, 3])]
        [PitchClassSegment([0, 1, 2, 7]), PitchClassSegment([4, 6])]
        [PitchClassSegment([10, 0, 2, 3]), PitchClassSegment([8, 5])]
        [PitchClassSegment([4, 10, 2, 6]), PitchClassSegment([1, 7])]
        [PitchClassSegment([8, 4, 2, 5]), PitchClassSegment([0, 3])]
        [PitchClassSegment([1, 8, 2, 7]), PitchClassSegment([10, 6])]

    ..  container:: example

        Accumulates permutation followed by transposition:

        >>> collection_1 = abjad.PitchClassSegment([0, 1, 2, 3])
        >>> collection_2 = abjad.PitchClassSegment([4, 5])

        >>> row = abjad.TwelveToneRow([10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])
        >>> sequence = [collection_1, collection_2]
        >>> for item in baca.sequence.accumulate(
        ...     sequence, [lambda _: row(_), lambda _: _.transpose(n=3)],
        ... ):
        ...     item
        ...
        [PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])]
        [PitchClassSegment([10, 0, 2, 6]), PitchClassSegment([8, 7])]
        [PitchClassSegment([1, 3, 5, 9]), PitchClassSegment([11, 10])]
        [PitchClassSegment([0, 6, 7, 9]), PitchClassSegment([11, 4])]
        [PitchClassSegment([3, 9, 10, 0]), PitchClassSegment([2, 7])]
        [PitchClassSegment([6, 9, 4, 10]), PitchClassSegment([2, 3])]
        [PitchClassSegment([9, 0, 7, 1]), PitchClassSegment([5, 6])]
        [PitchClassSegment([9, 10, 3, 0]), PitchClassSegment([7, 5])]
        [PitchClassSegment([0, 1, 6, 3]), PitchClassSegment([10, 8])]
        [PitchClassSegment([10, 0, 5, 6]), PitchClassSegment([4, 1])]
        [PitchClassSegment([1, 3, 8, 9]), PitchClassSegment([7, 4])]
        [PitchClassSegment([0, 6, 1, 9]), PitchClassSegment([3, 8])]
        [PitchClassSegment([3, 9, 4, 0]), PitchClassSegment([6, 11])]
        [PitchClassSegment([6, 9, 8, 10]), PitchClassSegment([5, 11])]
        [PitchClassSegment([9, 0, 11, 1]), PitchClassSegment([8, 2])]
        [PitchClassSegment([9, 10, 11, 0]), PitchClassSegment([1, 2])]

    Returns sequence of accumulated sequences.

    Returns sequence of length ``count`` + 1 with integer ``count``.

    Returns sequence of orbit length with ``count`` set to identity.
    """
    if count is None:
        count = abjad.EXACT
    operands = operands or [lambda _: _]
    if not isinstance(operands, list):
        operands = [operands]
    items = [sequence]
    if count == abjad.EXACT:
        for i in range(1000):
            sequence = items[-1]
            for operand in operands:
                sequence = type(sequence)([operand(_) for _ in sequence])
                items.append(sequence)
            if sequence == items[0]:
                items.pop(-1)
                break
        else:
            message = "1000 iterations without identity:"
            message += f" {items[0]!r} to {items[-1]!r}."
            raise Exception(message)
    else:
        for i in range(count - 1):
            sequence = items[-1]
            for operand in operands:
                sequence = type(sequence)([operand(_) for _ in sequence])
                items.append(sequence)
    return type(sequence)(items)


def boustrophedon(sequence, count=2):
    r"""
    Iterates sequence boustrophedon.

    ..  container:: example

        Iterates atoms boustrophedon:

        >>> sequence = [1, 2, 3, 4, 5]

        >>> baca.sequence.boustrophedon(sequence, count=0)
        []

        >>> baca.sequence.boustrophedon(sequence, count=1)
        [1, 2, 3, 4, 5]

        >>> baca.sequence.boustrophedon(sequence, count=2)
        [1, 2, 3, 4, 5, 4, 3, 2, 1]

        >>> baca.sequence.boustrophedon(sequence, count=3)
        [1, 2, 3, 4, 5, 4, 3, 2, 1, 2, 3, 4, 5]

    ..  container:: example

        Iterates collections boustrophedon:

        >>> collections = [
        ...     abjad.PitchClassSegment([1, 2, 3]),
        ...     abjad.PitchClassSegment([4, 5, 6]),
        ... ]
        >>> sequence = collections

        >>> baca.sequence.boustrophedon(sequence, count=0)
        []

        >>> for collection in baca.sequence.boustrophedon(sequence, count=1):
        ...     collection
        ...
        PitchClassSegment([1, 2, 3])
        PitchClassSegment([4, 5, 6])

        >>> for collection in baca.sequence.boustrophedon(sequence, count=2):
        ...     collection
        ...
        PitchClassSegment([1, 2, 3])
        PitchClassSegment([4, 5, 6])
        PitchClassSegment([5, 4])
        PitchClassSegment([3, 2, 1])

        >>> for collection in baca.sequence.boustrophedon(sequence, count=3):
        ...     collection
        ...
        PitchClassSegment([1, 2, 3])
        PitchClassSegment([4, 5, 6])
        PitchClassSegment([5, 4])
        PitchClassSegment([3, 2, 1])
        PitchClassSegment([2, 3])
        PitchClassSegment([4, 5, 6])

    ..  container:: example

        Iterates mixed items boustrophedon:

        >>> collection = abjad.PitchClassSegment([1, 2, 3])
        >>> sequence = [collection, 4, 5]
        >>> for item in baca.sequence.boustrophedon(sequence, count=3):
        ...     item
        ...
        PitchClassSegment([1, 2, 3])
        4
        5
        4
        PitchClassSegment([3, 2, 1])
        PitchClassSegment([2, 3])
        4
        5

    Returns new sequence.
    """
    result = []
    for i in range(count):
        if i == 0:
            for item in sequence:
                result.append(copy.copy(item))
        elif i % 2 == 0:
            if isinstance(sequence[0], collections.abc.Iterable):
                result.append(sequence[0][1:])
            else:
                pass
            for item in sequence[1:]:
                result.append(copy.copy(item))
        else:
            if isinstance(sequence[-1], collections.abc.Iterable):
                item = type(sequence[-1])(list(reversed(sequence[-1]))[1:])
                result.append(item)
            else:
                pass
            for item in reversed(sequence[:-1]):
                if isinstance(item, collections.abc.Iterable):
                    item = type(item)(list(reversed(item)))
                    result.append(item)
                else:
                    result.append(item)
    return type(sequence)(result)


def degree_of_rotational_symmetry(sequence):
    """
    Gets degree of rotational symmetry.

    ..  container:: example

        >>> baca.sequence.degree_of_rotational_symmetry([1, 1, 1, 1, 1, 1])
        6

        >>> baca.sequence.degree_of_rotational_symmetry([1, 2, 1, 2, 1, 2])
        3

        >>> baca.sequence.degree_of_rotational_symmetry([1, 2, 3, 1, 2, 3])
        2

        >>> baca.sequence.degree_of_rotational_symmetry([1, 2, 3, 4, 5, 6])
        1

        >>> baca.sequence.degree_of_rotational_symmetry([])
        1

    Returns positive integer.
    """
    degree_of_rotational_symmetry = 0
    for index in range(len(sequence)):
        rotation = sequence[index:] + sequence[:index]
        if rotation == sequence:
            degree_of_rotational_symmetry += 1
    degree_of_rotational_symmetry = degree_of_rotational_symmetry or 1
    return degree_of_rotational_symmetry


def group_by_sign(sequence, sign=(-1, 0, 1)):
    r"""
    Groups sequence by sign of items.

    >>> sequence = [0, 0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

    ..  container:: example

        >>> for item in baca.sequence.group_by_sign(sequence):
        ...     item
        ...
        [0, 0]
        [-1, -1]
        [2, 3]
        [-5]
        [1, 2, 5]
        [-5, -6]

    ..  container:: example

        >>> for item in baca.sequence.group_by_sign(sequence, [-1]):
        ...     item
        ...
        [0]
        [0]
        [-1, -1]
        [2]
        [3]
        [-5]
        [1]
        [2]
        [5]
        [-5, -6]

    ..  container:: example

        >>> for item in baca.sequence.group_by_sign(sequence, [0]):
        ...     item
        ...
        [0, 0]
        [-1]
        [-1]
        [2]
        [3]
        [-5]
        [1]
        [2]
        [5]
        [-5]
        [-6]

    ..  container:: example

        >>> for item in baca.sequence.group_by_sign(sequence, [1]):
        ...     item
        ...
        [0]
        [0]
        [-1]
        [-1]
        [2, 3]
        [-5]
        [1, 2, 5]
        [-5]
        [-6]

    ..  container:: example

        >>> for item in baca.sequence.group_by_sign(sequence, [-1, 0]):
        ...     item
        ...
        [0, 0]
        [-1, -1]
        [2]
        [3]
        [-5]
        [1]
        [2]
        [5]
        [-5, -6]

    ..  container:: example

        >>> for item in baca.sequence.group_by_sign(sequence, [-1, 1]):
        ...     item
        ...
        [0]
        [0]
        [-1, -1]
        [2, 3]
        [-5]
        [1, 2, 5]
        [-5, -6]

    ..  container:: example

        >>> for item in baca.sequence.group_by_sign(sequence, [0, 1]):
        ...     item
        ...
        [0, 0]
        [-1]
        [-1]
        [2, 3]
        [-5]
        [1, 2, 5]
        [-5]
        [-6]

    ..  container:: example

        >>> for item in baca.sequence.group_by_sign(sequence, [-1, 0, 1]):
        ...     item
        ...
        [0, 0]
        [-1, -1]
        [2, 3]
        [-5]
        [1, 2, 5]
        [-5, -6]

    Groups negative elements when ``-1`` in ``sign``.

    Groups zero-valued elements When ``0`` in ``sign``.

    Groups positive elements when ``1`` in ``sign``.

    Returns nested sequence.
    """
    items = []
    pairs = itertools.groupby(sequence, abjad.math.sign)
    for current_sign, group in pairs:
        if current_sign in sign:
            items.append(type(sequence)(group))
        else:
            for item in group:
                items.append(type(sequence)([item]))
    return type(sequence)(items)


def helianthate(sequence, n=0, m=0):
    r"""
    Helianthates sequence.

    ..  container:: example

        Helianthates list of lists:

        >>> sequence = [[1, 2, 3], [4, 5], [6, 7, 8]]
        >>> sequence = baca.sequence.helianthate(sequence, n=-1, m=1)
        >>> for item in sequence:
        ...     item
        ...
        [1, 2, 3]
        [4, 5]
        [6, 7, 8]
        [5, 4]
        [8, 6, 7]
        [3, 1, 2]
        [7, 8, 6]
        [2, 3, 1]
        [4, 5]
        [1, 2, 3]
        [5, 4]
        [6, 7, 8]
        [4, 5]
        [8, 6, 7]
        [3, 1, 2]
        [7, 8, 6]
        [2, 3, 1]
        [5, 4]

    ..  container:: example

        Helianthates list of collections:

        >>> J = abjad.PitchClassSegment(items=[0, 2, 4])
        >>> K = abjad.PitchClassSegment(items=[5, 6])
        >>> L = abjad.PitchClassSegment(items=[7, 9, 11])
        >>> sequence = [J, K, L]
        >>> sequence = baca.sequence.helianthate(sequence, n=-1, m=1)
        >>> for collection in sequence:
        ...     collection
        ...
        PitchClassSegment([0, 2, 4])
        PitchClassSegment([5, 6])
        PitchClassSegment([7, 9, 11])
        PitchClassSegment([6, 5])
        PitchClassSegment([11, 7, 9])
        PitchClassSegment([4, 0, 2])
        PitchClassSegment([9, 11, 7])
        PitchClassSegment([2, 4, 0])
        PitchClassSegment([5, 6])
        PitchClassSegment([0, 2, 4])
        PitchClassSegment([6, 5])
        PitchClassSegment([7, 9, 11])
        PitchClassSegment([5, 6])
        PitchClassSegment([11, 7, 9])
        PitchClassSegment([4, 0, 2])
        PitchClassSegment([9, 11, 7])
        PitchClassSegment([2, 4, 0])
        PitchClassSegment([6, 5])

    ..  container:: example

        Trivial helianthation:

        >>> items = [[1, 2, 3], [4, 5], [6, 7, 8]]
        >>> sequence = items
        >>> baca.sequence.helianthate(sequence)
        [[1, 2, 3], [4, 5], [6, 7, 8]]

    """
    start = list(sequence[:])
    result = list(sequence[:])
    assert isinstance(n, int), repr(n)
    assert isinstance(m, int), repr(m)
    original_n = n
    original_m = m

    def _generalized_rotate(argument, n=0):
        if hasattr(argument, "rotate"):
            return abjad.sequence.rotate(argument, n=n)
        argument_type = type(argument)
        argument = abjad.sequence.rotate(argument, n=n)
        argument = argument_type(argument)
        return argument

    i = 0
    while True:
        inner = [_generalized_rotate(_, m) for _ in sequence]
        candidate = _generalized_rotate(inner, n)
        if candidate == start:
            break
        result.extend(candidate)
        n += original_n
        m += original_m
        i += 1
        if i == 1000:
            message = "1000 iterations without identity."
            raise Exception(message)
    return type(sequence)(result)


def period_of_rotation(sequence):
    """
    Gets period of rotation of ``sequence``.

    ..  container:: example

        >>> baca.sequence.period_of_rotation([1, 2, 3, 4, 5, 6])
        6

        >>> baca.sequence.period_of_rotation([1, 2, 3, 1, 2, 3])
        3

        >>> baca.sequence.period_of_rotation([1, 2, 1, 2, 1, 2])
        2

        >>> baca.sequence.period_of_rotation([1, 1, 1, 1, 1, 1])
        1

        >>> baca.sequence.period_of_rotation([])
        0

    Defined equal to length of sequence divided by degree of rotational symmetry of
    sequence.

    Returns positive integer.
    """
    return len(sequence) // degree_of_rotational_symmetry(sequence)


def quarters(durations: list[abjad.Duration]) -> list[list[abjad.Duration]]:
    r"""
    Splits ``durations`` into quarters.

    ..  container:: example

        >>> durations = abjad.durations([(2, 4), (6, 4)])
        >>> for list_ in baca.sequence.quarters(durations): list_
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]

    """
    assert isinstance(durations, list), repr(durations)
    assert all(isinstance(_, abjad.Duration) for _ in durations), repr(durations)
    weights = abjad.durations([(1, 4)])
    lists = abjad.sequence.split(durations, weights, cyclic=True, overhang=True)
    assert isinstance(lists, list)
    for list_ in lists:
        assert all(isinstance(_, abjad.Duration) for _ in list_), repr(lists)
    return lists


def repeat_by(sequence, counts=None, cyclic=None):
    r"""
    Repeat sequence elements at ``counts``.

    ..  container:: example

        With no counts:

        ..  container:: example

            >>> baca.sequence.repeat_by([[1, 2, 3], 4, [5, 6]])
            [[1, 2, 3], 4, [5, 6]]

    ..  container:: example

        With acyclic counts:

        >>> sequence = [[1, 2, 3], 4, [5, 6]]

        ..  container:: example

            >>> baca.sequence.repeat_by(sequence, [0])
            [4, [5, 6]]

            >>> baca.sequence.repeat_by(sequence, [1])
            [[1, 2, 3], 4, [5, 6]]

            >>> baca.sequence.repeat_by(sequence, [2])
            [[1, 2, 3], [1, 2, 3], 4, [5, 6]]

            >>> baca.sequence.repeat_by(sequence, [3])
            [[1, 2, 3], [1, 2, 3], [1, 2, 3], 4, [5, 6]]

        ..  container:: example

            >>> baca.sequence.repeat_by(sequence, [1, 0])
            [[1, 2, 3], [5, 6]]

            >>> baca.sequence.repeat_by(sequence, [1, 1])
            [[1, 2, 3], 4, [5, 6]]

            >>> baca.sequence.repeat_by(sequence, [1, 2])
            [[1, 2, 3], 4, 4, [5, 6]]

            >>> baca.sequence.repeat_by(sequence, [1, 3])
            [[1, 2, 3], 4, 4, 4, [5, 6]]

        ..  container:: example

            >>> baca.sequence.repeat_by(sequence, [1, 1, 0])
            [[1, 2, 3], 4]

            >>> baca.sequence.repeat_by(sequence, [1, 1, 1])
            [[1, 2, 3], 4, [5, 6]]

            >>> baca.sequence.repeat_by(sequence, [1, 1, 2])
            [[1, 2, 3], 4, [5, 6], [5, 6]]

            >>> baca.sequence.repeat_by(sequence, [1, 1, 3])
            [[1, 2, 3], 4, [5, 6], [5, 6], [5, 6]]

    ..  container:: example

        With cyclic counts:

        ..  container:: example

            >>> baca.sequence.repeat_by(sequence, [0], cyclic=True)
            []

            >>> baca.sequence.repeat_by(sequence, [1], cyclic=True)
            [[1, 2, 3], 4, [5, 6]]

            >>> baca.sequence.repeat_by(sequence, [2], cyclic=True)
            [[1, 2, 3], [1, 2, 3], 4, 4, [5, 6], [5, 6]]

            >>> baca.sequence.repeat_by(sequence, [3], cyclic=True)
            [[1, 2, 3], [1, 2, 3], [1, 2, 3], 4, 4, 4, [5, 6], [5, 6], [5, 6]]

        ..  container:: example

            >>> baca.sequence.repeat_by(sequence, [2, 0], cyclic=True)
            [[1, 2, 3], [1, 2, 3], [5, 6], [5, 6]]

            >>> baca.sequence.repeat_by(sequence, [2, 1], cyclic=True)
            [[1, 2, 3], [1, 2, 3], 4, [5, 6], [5, 6]]

            >>> baca.sequence.repeat_by(sequence, [2, 2], cyclic=True)
            [[1, 2, 3], [1, 2, 3], 4, 4, [5, 6], [5, 6]]

            >>> baca.sequence.repeat_by(sequence, [2, 3], cyclic=True)
            [[1, 2, 3], [1, 2, 3], 4, 4, 4, [5, 6], [5, 6]]

    Raises exception on negative counts.

    Returns new sequence.
    """
    if counts is None:
        return type(sequence)(sequence)
    counts = counts or [1]
    assert isinstance(counts, collections.abc.Iterable)
    if cyclic is True:
        counts = abjad.CyclicTuple(counts)
    items = []
    for i, item in enumerate(sequence):
        try:
            count = counts[i]
        except IndexError:
            count = 1
        items.extend(count * [item])
    return type(sequence)(items)
