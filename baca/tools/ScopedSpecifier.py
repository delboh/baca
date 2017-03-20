# -*- coding: utf-8 -*-
import abjad
import baca


class ScopedSpecifier(abjad.abctools.AbjadObject):
    r'''Scoped specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Makes scoped pitch specifier:

        ::

            >>> specifier = baca.tools.ScopedSpecifier(
            ...     ('Violin Music Voice', (1, 4)),
            ...     baca.tools.ScorePitchCommand(
            ...         source=[7, 1, 3, 4, 5, 11],
            ...         ),
            ...     )

        ::

            >>> f(specifier)
            baca.tools.ScopedSpecifier(
                scope=baca.tools.SimpleScope(
                    voice_name='Violin Music Voice',
                    stages=(1, 4),
                    ),
                specifier=baca.tools.ScorePitchCommand(
                    source=datastructuretools.CyclicTuple(
                        [
                            pitchtools.NamedPitch("g'"),
                            pitchtools.NamedPitch("cs'"),
                            pitchtools.NamedPitch("ef'"),
                            pitchtools.NamedPitch("e'"),
                            pitchtools.NamedPitch("f'"),
                            pitchtools.NamedPitch("b'"),
                            ]
                        ),
                    ),
                )


    ..  container:: example

        Makes pitch specifier with compound scope:

        ::

            >>> specifier = baca.tools.ScopedSpecifier(
            ...     baca.tools.CompoundScope([
            ...         baca.tools.SimpleScope('Violin Music Voice', (1, 4)),
            ...         baca.tools.SimpleScope('Violin Music Voice', (8, 12)),
            ...         ]),
            ...     baca.tools.ScorePitchCommand(
            ...         source=[7, 1, 3, 4, 5, 11],
            ...         ),
            ...     )

        ::

            >>> f(specifier)
            baca.tools.ScopedSpecifier(
                scope=baca.tools.CompoundScope(
                    simple_scopes=(
                        baca.tools.SimpleScope(
                            voice_name='Violin Music Voice',
                            stages=(1, 4),
                            ),
                        baca.tools.SimpleScope(
                            voice_name='Violin Music Voice',
                            stages=(8, 12),
                            ),
                        ),
                    ),
                specifier=baca.tools.ScorePitchCommand(
                    source=datastructuretools.CyclicTuple(
                        [
                            pitchtools.NamedPitch("g'"),
                            pitchtools.NamedPitch("cs'"),
                            pitchtools.NamedPitch("ef'"),
                            pitchtools.NamedPitch("e'"),
                            pitchtools.NamedPitch("f'"),
                            pitchtools.NamedPitch("b'"),
                            ]
                        ),
                    ),
                )


    ..  container:: example

        Makes scoped displacement specifier:

        ::

            >>> specifier = baca.tools.ScopedSpecifier(
            ...     ('Violin Music Voice', (1, 4)),
            ...     baca.tools.OctaveDisplacementCommand(
            ...         displacements=[0, 0, 0, 0, 1, 1, 1, 1],
            ...         ),
            ...     )

        ::

            >>> f(specifier)
            baca.tools.ScopedSpecifier(
                scope=baca.tools.SimpleScope(
                    voice_name='Violin Music Voice',
                    stages=(1, 4),
                    ),
                specifier=baca.tools.OctaveDisplacementCommand(
                    displacements=datastructuretools.CyclicTuple(
                        [0, 0, 0, 0, 1, 1, 1, 1]
                        ),
                    ),
                )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Segments'

    __slots__ = (
        '_scope',
        '_specifier',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, scope=None, specifier=None):
        if isinstance(scope, tuple):
            scope = baca.tools.SimpleScope(*scope)
        prototype = (baca.tools.SimpleScope, baca.tools.CompoundScope)
        if scope is not None:
            assert isinstance(scope, prototype), repr(scope)
        self._scope = scope
        assert not isinstance(specifier, (tuple, list)), repr(specifier)
        self._specifier = specifier

    ### PUBLIC PROPERTIES ###

    @property
    def scope(self):
        r'''Gets scope.

        ..  container:: example

            Gets scope:

            ::

                >>> specifier = baca.tools.ScopedSpecifier(
                ...     ('Violin Music Voice', (1, 4)),
                ...     baca.tools.ScorePitchCommand(
                ...         source=[7, 1, 3, 4, 5, 11],
                ...         ),
                ...     )

            ::

                >>> f(specifier.scope)
                baca.tools.SimpleScope(
                    voice_name='Violin Music Voice',
                    stages=(1, 4),
                    )

        Defaults to none.

        Set to scope or none.

        Returns scope or none.
        '''
        return self._scope

    @property
    def specifier(self):
        r'''Gets specifier.

        ..  container:: example

            Gets specifier:

            ::

                >>> specifier = baca.tools.ScopedSpecifier(
                ...     ('Violin Music Voice', (1, 4)),
                ...     baca.tools.ScorePitchCommand(
                ...         source=[7, 1, 3, 4, 5, 11],
                ...         ),
                ...     )

            ::

                >>> f(specifier.specifier)
                baca.tools.ScorePitchCommand(
                    source=datastructuretools.CyclicTuple(
                        [
                            pitchtools.NamedPitch("g'"),
                            pitchtools.NamedPitch("cs'"),
                            pitchtools.NamedPitch("ef'"),
                            pitchtools.NamedPitch("e'"),
                            pitchtools.NamedPitch("f'"),
                            pitchtools.NamedPitch("b'"),
                            ]
                        ),
                    )

        Defaults to none.

        Set to specifier or none.

        Returns specifier or none.
        '''
        return self._specifier
