# -*- coding: utf-8 -*-
import abjad
import math


def is_dotted_integer(argument):
    '''Is true when `argument` is equivalent to a positive integer and
    can be written with zero or more dots. Otherwise false.

    ..  container:: example

        ::

            >>> for argument in range(16):
            ...     print('%s\t%s' % (argument, baca.tools.is_dotted_integer(argument)))
            ... 
            0         False
            1         False
            2         False
            3         True
            4         False
            5         False
            6         True
            7         True
            8         False
            9         False
            10        False
            11        False
            12        True
            13        False
            14        True
            15        True

    Returns true or false.

    Integer `n` qualifies as dotted when ``abs(n)`` is of the form
    ``2**j * (2**k - 1)`` with integers ``0 <= j``, ``2 < k``.
    '''
    if argument == 0:
        return False
    non_two_product = 1
    non_two_factors = [
        _ for _ in abjad.mathtools.factors(argument) if not _ == 2
        ]
    for non_two_factor in non_two_factors:
        non_two_product *= non_two_factor
    x = math.log(abs(non_two_product) + 1, 2)
    result = 1 < abs(non_two_product) and int(x) == x
    return result
