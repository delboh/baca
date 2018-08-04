import abjad
import collections
import copy
import math
import typing
from abjadext import rmakers
from . import classes
from . import commands
from . import pitchcommands
from . import pitchclasses
from . import rhythmcommands
from . import scoping
from . import spannercommands
from . import typings


### CLASSES ###

class AcciaccaturaSpecifier(abjad.AbjadObject):
    r"""
    Acciaccatura specifier.

    >>> from abjadext import rmakers

    ..  container:: example

        Default acciaccatura specifier:

        >>> rhythm_maker = baca.PitchFirstRhythmMaker(
        ...     acciaccatura_specifiers=[
        ...         baca.AcciaccaturaSpecifier()
        ...         ],
        ...     talea=rmakers.Talea(
        ...         counts=[1],
        ...         denominator=8,
        ...         ),
        ...     )

        >>> collections = [
        ...     [0],
        ...     [2, 10],
        ...     [18, 16, 15],
        ...     [20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ...     [20, 19, 9, 0, 2, 10],
        ...     ]
        >>> selections, state_manifest = rhythm_maker(collections)
        >>> lilypond_file = rhythm_maker.show(selections)
        >>> score = lilypond_file[abjad.Score]
        >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
        >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            {
                {   % measure
                    \time 3/4
                    \scaleDurations #'(1 . 1) {
                        c'8
                    }
                    \scaleDurations #'(1 . 1) {
                        \acciaccatura {
                            d'16
                        }
                        bf'8
                    }
                    \scaleDurations #'(1 . 1) {
                        \acciaccatura {
                            fs''16
                            [                                                                        %! ACC_1
                            e''16
                            ]                                                                        %! ACC_1
                        }
                        ef''8
                    }
                    \scaleDurations #'(1 . 1) {
                        \acciaccatura {
                            af''16
                            [                                                                        %! ACC_1
                            g''16
                            a'16
                            ]                                                                        %! ACC_1
                        }
                        c'8
                    }
                    \scaleDurations #'(1 . 1) {
                        \acciaccatura {
                            d'16
                            [                                                                        %! ACC_1
                            bf'16
                            fs''16
                            e''16
                            ]                                                                        %! ACC_1
                        }
                        ef''8
                    }
                    \scaleDurations #'(1 . 1) {
                        \acciaccatura {
                            af''16
                            [                                                                        %! ACC_1
                            g''16
                            a'16
                            c'16
                            d'16
                            ]                                                                        %! ACC_1
                        }
                        bf'8
                    }
                }   % measure
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_durations',
        '_lmr_specifier',
        '_pattern',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        durations=None,
        lmr_specifier=None,
        pattern=None,
        ):
        if durations is not None:
            assert isinstance(durations, list), repr(durations)
            durations = [abjad.Duration(_) for _ in durations]
        self._durations = durations
        if lmr_specifier is not None:
            prototype = LMRSpecifier
            assert isinstance(lmr_specifier, prototype)
        self._lmr_specifier = lmr_specifier
        if pattern is not None:
            assert isinstance(pattern, abjad.Pattern), repr(pattern)
        self._pattern = pattern

    ### SPECIAL METHODS ###

    def __call__(self, collection=None):
        """
        Calls acciaccatura specifier on ``collection``.

        Returns acciaccatura container together with new collection.
        """
        prototype = (list, abjad.Segment)
        assert isinstance(collection, prototype), repr(collection)
        lmr_specifier = self._get_lmr_specifier()
        segment_parts = lmr_specifier(collection)
        segment_parts = [_ for _ in segment_parts if _]
        collection = [_[-1] for _ in segment_parts]
        durations = self._get_durations()
        acciaccatura_containers = []
        maker = abjad.LeafMaker()
        for segment_part in segment_parts:
            if len(segment_part) <= 1:
                acciaccatura_containers.append(None)
                continue
            grace_token = list(segment_part[:-1])
            grace_leaves = maker(grace_token, durations)
            acciaccatura_container = abjad.AcciaccaturaContainer(grace_leaves)
            if 1 < len(acciaccatura_container):
                abjad.attach(
                    abjad.Beam(),
                    acciaccatura_container[:],
                    tag='ACC_1',
                    )
            acciaccatura_containers.append(acciaccatura_container)
        assert len(acciaccatura_containers) == len(collection)
        return acciaccatura_containers, collection

    ### PRIVATE METHODS ###

    def _get_durations(self):
        return self.durations or [abjad.Duration(1, 16)]

    def _get_lmr_specifier(self):
        if self.lmr_specifier is not None:
            return self.lmr_specifier
        return LMRSpecifier()

    def _get_pattern(self):
        return self.pattern or abjad.index_all()

    ### PUBLIC PROPERTIES ###

    @property
    def durations(self):
        r"""
        Gets durations.

        ..  container:: example

            Sixteenth-note acciaccaturas by default:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     acciaccatura_specifiers=[
            ...         baca.AcciaccaturaSpecifier()
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=8,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state_manifest = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/4
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''16
                                [                                                                        %! ACC_1
                                e''16
                                ]                                                                        %! ACC_1
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! ACC_1
                                g''16
                                a'16
                                ]                                                                        %! ACC_1
                            }
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                                [                                                                        %! ACC_1
                                bf'16
                                fs''16
                                e''16
                                ]                                                                        %! ACC_1
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! ACC_1
                                g''16
                                a'16
                                c'16
                                d'16
                                ]                                                                        %! ACC_1
                            }
                            bf'8
                        }
                    }   % measure
                }

        ..  container:: example

            Eighth-note acciaccaturas:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     acciaccatura_specifiers=[
            ...         baca.AcciaccaturaSpecifier(
            ...             durations=[(1, 8)],
            ...             ),
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=8,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state_manifest = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/4
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'8
                            }
                            bf'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''8
                                [                                                                        %! ACC_1
                                e''8
                                ]                                                                        %! ACC_1
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''8
                                [                                                                        %! ACC_1
                                g''8
                                a'8
                                ]                                                                        %! ACC_1
                            }
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'8
                                [                                                                        %! ACC_1
                                bf'8
                                fs''8
                                e''8
                                ]                                                                        %! ACC_1
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''8
                                [                                                                        %! ACC_1
                                g''8
                                a'8
                                c'8
                                d'8
                                ]                                                                        %! ACC_1
                            }
                            bf'8
                        }
                    }   % measure
                }

        Defaults to none.

        Set to durations or none.

        Returns durations or none.
        """
        return self._durations

    @property
    def lmr_specifier(self):
        r"""
        Gets LMR specifier.

        ..  container:: example

            As many acciaccaturas as possible per collection:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     acciaccatura_specifiers=[
            ...         baca.AcciaccaturaSpecifier()
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=8,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state_manifest = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/4
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''16
                                [                                                                        %! ACC_1
                                e''16
                                ]                                                                        %! ACC_1
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! ACC_1
                                g''16
                                a'16
                                ]                                                                        %! ACC_1
                            }
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                                [                                                                        %! ACC_1
                                bf'16
                                fs''16
                                e''16
                                ]                                                                        %! ACC_1
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! ACC_1
                                g''16
                                a'16
                                c'16
                                d'16
                                ]                                                                        %! ACC_1
                            }
                            bf'8
                        }
                    }   % measure
                }


        ..  container:: example

            At most two acciaccaturas at the beginning of every collection:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     acciaccatura_specifiers=[
            ...         baca.AcciaccaturaSpecifier(
            ...             lmr_specifier=baca.LMRSpecifier(
            ...                 left_length=3,
            ...                 right_counts=[1],
            ...                 right_cyclic=True,
            ...                 ),
            ...             ),
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=8,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state_manifest = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/2
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''16
                                [                                                                        %! ACC_1
                                e''16
                                ]                                                                        %! ACC_1
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! ACC_1
                                g''16
                                ]                                                                        %! ACC_1
                            }
                            a'8
                            [
                            c'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                                [                                                                        %! ACC_1
                                bf'16
                                ]                                                                        %! ACC_1
                            }
                            fs''8
                            [
                            e''8
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! ACC_1
                                g''16
                                ]                                                                        %! ACC_1
                            }
                            a'8
                            [
                            c'8
                            d'8
                            bf'8
                            ]
                        }
                    }   % measure
                }

        ..  container:: example

            At most two acciaccaturas at the end of every collection:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     acciaccatura_specifiers=[
            ...         baca.AcciaccaturaSpecifier(
            ...             lmr_specifier=baca.LMRSpecifier(
            ...                 right_length=3,
            ...                 left_counts=[1],
            ...                 left_cyclic=True,
            ...                 ),
            ...             ),
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=8,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state_manifest = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/2
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''16
                                [                                                                        %! ACC_1
                                e''16
                                ]                                                                        %! ACC_1
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            af''8
                            [
                            \acciaccatura {
                                g''16
                                [                                                                        %! ACC_1
                                a'16
                                ]                                                                        %! ACC_1
                            }
                            c'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            d'8
                            [
                            bf'8
                            \acciaccatura {
                                fs''16
                                [                                                                        %! ACC_1
                                e''16
                                ]                                                                        %! ACC_1
                            }
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            af''8
                            [
                            g''8
                            a'8
                            \acciaccatura {
                                c'16
                                [                                                                        %! ACC_1
                                d'16
                                ]                                                                        %! ACC_1
                            }
                            bf'8
                            ]
                        }
                    }   % measure
                }

        ..  container:: example

            At most two acciaccaturas at the beginning of every collection and
            then at most two acciaccaturas at the end of every collection:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     acciaccatura_specifiers=[
            ...         baca.AcciaccaturaSpecifier(
            ...             lmr_specifier=baca.LMRSpecifier(
            ...                 left_length=3,
            ...                 middle_counts=[1],
            ...                 middle_cyclic=True,
            ...                 right_length=3,
            ...                 ),
            ...             ),
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=8,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state_manifest = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 9/8
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''16
                                [                                                                        %! ACC_1
                                e''16
                                ]                                                                        %! ACC_1
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! ACC_1
                                g''16
                                ]                                                                        %! ACC_1
                            }
                            a'8
                            [
                            c'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                                [                                                                        %! ACC_1
                                bf'16
                                ]                                                                        %! ACC_1
                            }
                            fs''8
                            [
                            \acciaccatura {
                                e''16
                            }
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! ACC_1
                                g''16
                                ]                                                                        %! ACC_1
                            }
                            a'8
                            [
                            \acciaccatura {
                                c'16
                                [                                                                        %! ACC_1
                                d'16
                                ]                                                                        %! ACC_1
                            }
                            bf'8
                            ]
                        }
                    }   % measure
                }

        ..  container:: example

            As many acciaccaturas as possible in the middle of every collection:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     acciaccatura_specifiers=[
            ...         baca.AcciaccaturaSpecifier(
            ...             lmr_specifier=baca.LMRSpecifier(
            ...                 left_length=1,
            ...                 ),
            ...             ),
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=8,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state_manifest = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 11/8
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            d'8
                            [
                            bf'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''8
                            [
                            \acciaccatura {
                                e''16
                            }
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            af''8
                            [
                            \acciaccatura {
                                g''16
                                [                                                                        %! ACC_1
                                a'16
                                ]                                                                        %! ACC_1
                            }
                            c'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            d'8
                            [
                            \acciaccatura {
                                bf'16
                                [                                                                        %! ACC_1
                                fs''16
                                e''16
                                ]                                                                        %! ACC_1
                            }
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            af''8
                            [
                            \acciaccatura {
                                g''16
                                [                                                                        %! ACC_1
                                a'16
                                c'16
                                d'16
                                ]                                                                        %! ACC_1
                            }
                            bf'8
                            ]
                        }
                    }   % measure
                }

        Defaults to none.

        Set to LMR specifier or none.

        Returns LMR specifier or none.
        """
        return self._lmr_specifier

    @property
    def pattern(self):
        r"""
        Gets pattern.

        ..  container:: example

            Applies to all collections by default:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     acciaccatura_specifiers=[
            ...         baca.AcciaccaturaSpecifier()
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=8,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state_manifest = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/4
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''16
                                [                                                                        %! ACC_1
                                e''16
                                ]                                                                        %! ACC_1
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! ACC_1
                                g''16
                                a'16
                                ]                                                                        %! ACC_1
                            }
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                                [                                                                        %! ACC_1
                                bf'16
                                fs''16
                                e''16
                                ]                                                                        %! ACC_1
                            }
                            ef''8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! ACC_1
                                g''16
                                a'16
                                c'16
                                d'16
                                ]                                                                        %! ACC_1
                            }
                            bf'8
                        }
                    }   % measure
                }

        ..  container:: example

            Applies to last collection:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     acciaccatura_specifiers=[
            ...         baca.AcciaccaturaSpecifier(
            ...             pattern=abjad.index_last(1),
            ...             ),
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=8,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state_manifest = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 2/1
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            d'8
                            [
                            bf'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''8
                            [
                            e''8
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            af''8
                            [
                            g''8
                            a'8
                            c'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            d'8
                            [
                            bf'8
                            fs''8
                            e''8
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! ACC_1
                                g''16
                                a'16
                                c'16
                                d'16
                                ]                                                                        %! ACC_1
                            }
                            bf'8
                        }
                    }   % measure
                }

        ..  container:: example

            Applies to every other collection:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     acciaccatura_specifiers=[
            ...         baca.AcciaccaturaSpecifier(
            ...             pattern=abjad.index([1], 2),
            ...             ),
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=8,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state_manifest = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/2
                        \scaleDurations #'(1 . 1) {
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                            }
                            bf'8
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''8
                            [
                            e''8
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! ACC_1
                                g''16
                                a'16
                                ]                                                                        %! ACC_1
                            }
                            c'8
                        }
                        \scaleDurations #'(1 . 1) {
                            d'8
                            [
                            bf'8
                            fs''8
                            e''8
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! ACC_1
                                g''16
                                a'16
                                c'16
                                d'16
                                ]                                                                        %! ACC_1
                            }
                            bf'8
                        }
                    }   % measure
                }

        Defaults to none.

        Set to pattern or none.

        Returns pattern or none.
        """
        return self._pattern

class AnchorSpecifier(abjad.AbjadValueObject):
    """
    Anchor specifier.

    ..  container:: example

        >>> baca.AnchorSpecifier()
        AnchorSpecifier()

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_figure_name',
        '_local_selector',
        '_remote_selector',
        '_remote_voice_name',
        '_use_remote_stop_offset',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        figure_name=None,
        local_selector=None,
        remote_selector=None,
        remote_voice_name=None,
        use_remote_stop_offset=None,
        ):
        # for selector evaluation:
        import baca
        if figure_name is not None:
            assert isinstance(figure_name, str), repr(figure_name)
        self._figure_name = figure_name
        if isinstance(local_selector, str):
            local_selector = eval(local_selector)
        if (local_selector is not None and
            not isinstance(local_selector, abjad.Expression)):
            raise TypeError(f'must be selector: {local_selector!r}.')
        self._local_selector = local_selector
        if isinstance(remote_selector, str):
            remote_selector = eval(remote_selector)
        if (remote_selector is not None and
            not isinstance(remote_selector, abjad.Expression)):
            raise TypeError(f'must be selector: {remote_selector!r}.')
        self._remote_selector = remote_selector
        if (remote_voice_name is not None and
            not isinstance(remote_voice_name, str)):
            raise TypeError(f'must be string: {remote_voice_name!r}.')
        self._remote_voice_name = remote_voice_name
        if use_remote_stop_offset is not None:
            use_remote_stop_offset = bool(use_remote_stop_offset)
        self._use_remote_stop_offset = use_remote_stop_offset

    ### PUBLIC PROPERTIES ###

    @property
    def figure_name(self):
        """
        Gets figure name.

        Returns strings or none.
        """
        return self._figure_name

    @property
    def local_selector(self):
        """
        Gets local selector.

        Returns selector or none.
        """
        return self._local_selector

    @property
    def remote_selector(self):
        """
        Gets remote selector.

        Returns selector or none.
        """
        return self._remote_selector

    @property
    def remote_voice_name(self):
        """
        Gets remote voice name.

        Set to string or none.

        Returns strings or none.
        """
        return self._remote_voice_name

    @property
    def use_remote_stop_offset(self):
        """
        Is true when contribution anchors to remote selection stop offset.

        Otherwise anchors to remote selection start offset.

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        """
        return self._use_remote_stop_offset

class Coat(abjad.AbjadObject):
    """
    Coat.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_argument',
        )

    ### INITIALIZER ###

    def __init__(self, argument):
        self._argument = argument

    ### PUBLIC PROPERTIES ###

    @property
    def argument(self):
        """
        Gets argument.
        """
        return self._argument

class ImbricationCommand(scoping.Command):
    r"""
    Imbrication command.

    >>> from abjadext import rmakers

    ..  container:: example

        Defaults:

        >>> music_maker = baca.MusicMaker(
        ...     rmakers.BeamSpecifier(
        ...         beam_divisions_together=True,
        ...         ),
        ...     )

        >>> collections = [
        ...     [0, 2, 10, 18, 16],
        ...     [15, 20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ...     ]
        >>> contribution = music_maker(
        ...     'Voice 2',
        ...     collections,
        ...     baca.ImbricationCommand(
        ...         'Voice 1',
        ...         [2, 19, 9, 18, 16],
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    {   % measure
                        \time 15/16
                        s1 * 15/16
                    }   % measure
                }
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            \scaleDurations #'(1 . 1) {
                                s16
                                d'16
                                s16
                                s16
                                s16
                            }
                            \scaleDurations #'(1 . 1) {
                                s16
                                s16
                                g''16
                                [
                                a'16
                                ]
                                s16
                            }
                            \scaleDurations #'(1 . 1) {
                                s16
                                s16
                                fs''16
                                [
                                e''16
                                ]
                                s16
                            }
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }
                    }
                    \context Voice = "Voice 2"
                    {
                        \voiceTwo
                        {
                            \scaleDurations #'(1 . 1) {
                                \set stemLeftBeamCount = 0
                                \set stemRightBeamCount = 2
                                c'16
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                e''16
                            }
                            \scaleDurations #'(1 . 1) {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                ef''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                af''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                g''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                a'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                c'16
                            }
                            \scaleDurations #'(1 . 1) {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                d'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                e''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                ef''16
                                ]
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        Multiple imbricated voices:

        >>> music_maker = baca.MusicMaker(
        ...     rmakers.BeamSpecifier(
        ...         beam_divisions_together=True,
        ...         ),
        ...     )

        >>> collections = [
        ...     [0, 2, 10, 18, 16],
        ...     [15, 20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ...     ]
        >>> contribution = music_maker(
        ...     'Voice 2',
        ...     collections,
        ...     baca.ImbricationCommand(
        ...         'Voice 1',
        ...         [2, 19, 9],
        ...         baca.beam_everything(),
        ...         baca.staccato(selector=baca.pheads()),
        ...         ),
        ...     baca.ImbricationCommand(
        ...         'Voice 3',
        ...         [16, 10, 18],
        ...         baca.beam_everything(),
        ...         baca.accent(selector=baca.pheads()),
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    {   % measure
                        \time 15/16
                        s1 * 15/16
                    }   % measure
                }
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            \scaleDurations #'(1 . 1) {
                                s16
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16
                                -\staccato                                                           %! INDICATOR_COMMAND
                                s16
                                s16
                                s16
                            }
                            \scaleDurations #'(1 . 1) {
                                s16
                                s16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                g''16
                                -\staccato                                                           %! INDICATOR_COMMAND
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                a'16
                                -\staccato                                                           %! INDICATOR_COMMAND
                                s16
                            }
                            \scaleDurations #'(1 . 1) {
                                s16
                                s16
                                s16
                                s16
                                s16
                                ]
                            }
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }
                    }
                    \context Voice = "Voice 2"
                    {
                        \voiceTwo
                        {
                            \scaleDurations #'(1 . 1) {
                                \set stemLeftBeamCount = 0
                                \set stemRightBeamCount = 2
                                c'16
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                e''16
                            }
                            \scaleDurations #'(1 . 1) {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                ef''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                af''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                g''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                a'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                c'16
                            }
                            \scaleDurations #'(1 . 1) {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                d'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                e''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                ef''16
                                ]
                            }
                        }
                    }
                    \context Voice = "Voice 3"
                    {
                        \voiceThree
                        {
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            \scaleDurations #'(1 . 1) {
                                s16
                                [
                                s16
                                s16
                                s16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                e''16
                                -\accent                                                             %! INDICATOR_COMMAND
                            }
                            \scaleDurations #'(1 . 1) {
                                s16
                                s16
                                s16
                                s16
                                s16
                            }
                            \scaleDurations #'(1 . 1) {
                                s16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16
                                -\accent                                                             %! INDICATOR_COMMAND
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16
                                -\accent                                                             %! INDICATOR_COMMAND
                                s16
                                s16
                                ]
                            }
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }
                    }
                >>
            >>

    ..  container:: example

        Hides tuplet brackets above imbricated voice:

        >>> music_maker = baca.MusicMaker(
        ...     rmakers.BeamSpecifier(
        ...         beam_divisions_together=True,
        ...         beam_rests=True,
        ...         ),
        ...     baca.staccato(selector=baca.pheads()),
        ...     baca.PitchFirstRhythmCommand(
        ...         rhythm_maker=baca.PitchFirstRhythmMaker(
        ...             talea=rmakers.Talea(
        ...                 counts=[1],
        ...                 denominator=16,
        ...                 ),
        ...             time_treatments=[1],
        ...             ),
        ...         ),
        ...     )

        >>> collections = [
        ...     [0, 2, 10, 18, 16],
        ...     [15, 20, 19, 9, 0],
        ...     [2, 10, 18, 16, 15],
        ...     ]
        >>> contribution = music_maker(
        ...     'Voice 2',
        ...     collections,
        ...     baca.ImbricationCommand(
        ...         'Voice 1',
        ...         [2, 19, 9, 18, 16],
        ...         baca.accent(selector=baca.pheads()),
        ...         baca.beam_everything(),
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    {   % measure
                        \time 9/8
                        s1 * 9/8
                    }   % measure
                }
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/5 {
                                s16
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16
                                -\accent                                                             %! INDICATOR_COMMAND
                                s16
                                s16
                                s16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/5 {
                                s16
                                s16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                g''16
                                -\accent                                                             %! INDICATOR_COMMAND
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                a'16
                                -\accent                                                             %! INDICATOR_COMMAND
                                s16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/5 {
                                s16
                                s16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16
                                -\accent                                                             %! INDICATOR_COMMAND
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                e''16
                                -\accent                                                             %! INDICATOR_COMMAND
                                s16
                                ]
                            }
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }
                    }
                    \context Voice = "Voice 2"
                    {
                        \voiceTwo
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/5 {
                                \set stemLeftBeamCount = 0
                                \set stemRightBeamCount = 2
                                c'16
                                -\staccato                                                           %! INDICATOR_COMMAND
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16
                                -\staccato                                                           %! INDICATOR_COMMAND
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16
                                -\staccato                                                           %! INDICATOR_COMMAND
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16
                                -\staccato                                                           %! INDICATOR_COMMAND
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                e''16
                                -\staccato                                                           %! INDICATOR_COMMAND
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/5 {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                ef''16
                                -\staccato                                                           %! INDICATOR_COMMAND
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                af''16
                                -\staccato                                                           %! INDICATOR_COMMAND
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                g''16
                                -\staccato                                                           %! INDICATOR_COMMAND
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                a'16
                                -\staccato                                                           %! INDICATOR_COMMAND
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                c'16
                                -\staccato                                                           %! INDICATOR_COMMAND
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/5 {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                d'16
                                -\staccato                                                           %! INDICATOR_COMMAND
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16
                                -\staccato                                                           %! INDICATOR_COMMAND
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                fs''16
                                -\staccato                                                           %! INDICATOR_COMMAND
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                e''16
                                -\staccato                                                           %! INDICATOR_COMMAND
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                ef''16
                                -\staccato                                                           %! INDICATOR_COMMAND
                                ]
                            }
                        }
                    }
                >>
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_allow_unused_pitches',
        '_by_pitch_class',
        '_extend_beam',
        '_hocket',
        '_segment',
        '_selector',
        '_specifiers',
        '_truncate_ties',
        '_voice_name',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        voice_name=None,
        segment=None,
        *specifiers,
        allow_unused_pitches=None,
        by_pitch_class=None,
        extend_beam=None,
        hocket=None,
        selector=None,
        truncate_ties=None
        ):
        if voice_name is not None:
            assert isinstance(voice_name, str), repr(voice_name)
        self._voice_name = voice_name
        self._segment = segment
        self._specifiers = specifiers
        if allow_unused_pitches is not None:
            allow_unused_pitches = bool(allow_unused_pitches)
        self._allow_unused_pitches = allow_unused_pitches
        if by_pitch_class is not None:
            by_pitch_class = bool(by_pitch_class)
        self._by_pitch_class = by_pitch_class
        if extend_beam is not None:
            extend_beam = bool(extend_beam)
        self._extend_beam = extend_beam
        if hocket is not None:
            hocket = bool(hocket)
        self._hocket = hocket
        if selector is not None:
            if not isinstance(selector, abjad.Expression):
                raise TypeError(f'selector or none only: {selector!r}.')
        self._selector = selector
        if truncate_ties is not None:
            truncate_ties = bool(truncate_ties)
        self._truncate_ties = truncate_ties

    ### SPECIAL METHODS ###

    def __call__(self, container=None):
        r"""
        Calls command on ``container``.

        ..  container:: example

            Works with pitch-classes:

            >>> music_maker = baca.MusicMaker(
            ...     baca.PitchFirstRhythmCommand(
            ...         rhythm_maker=baca.PitchFirstRhythmMaker(
            ...             talea=rmakers.Talea(
            ...                 counts=[3],
            ...                 denominator=16,
            ...                 ),
            ...             ),
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> segment = [
            ...     abjad.NumberedPitchClass(10),
            ...     abjad.NumberedPitchClass(6),
            ...     abjad.NumberedPitchClass(4),
            ...     abjad.NumberedPitchClass(3),
            ...     ]
            >>> contribution = music_maker(
            ...     'Voice 2',
            ...     collections,
            ...     baca.ImbricationCommand(
            ...         'Voice 1',
            ...         segment,
            ...         baca.accent(selector=baca.pheads()),
            ...         baca.beam_everything(),
            ...         ),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        {   % measure
                            \time 27/16
                            s1 * 27/16
                        }   % measure
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice 1"
                        {
                            \voiceOne
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1) {
                                    s8.
                                    [
                                    s8.
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    bf'8.
                                    -\accent                                                             %! INDICATOR_COMMAND
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    fs''8.
                                    -\accent                                                             %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    e''8.
                                    -\accent                                                             %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    ef''8.
                                    -\accent                                                             %! INDICATOR_COMMAND
                                    s8.
                                    s8.
                                }
                                \scaleDurations #'(1 . 1) {
                                    s8.
                                    ]
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                        \context Voice = "Voice 2"
                        {
                            \voiceTwo
                            {
                                \scaleDurations #'(1 . 1) {
                                    c'8.
                                    [
                                    d'8.
                                    bf'8.
                                    ]
                                }
                                \scaleDurations #'(1 . 1) {
                                    fs''8.
                                    [
                                    e''8.
                                    ef''8.
                                    af''8.
                                    g''8.
                                    ]
                                }
                                \scaleDurations #'(1 . 1) {
                                    a'8.
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Skips wrapped pitches:

            >>> music_maker = baca.MusicMaker()

            >>> collections = [
            ...     [0, 2, 10, 18, 16], [15, 20, 19, 9],
            ...     [0, 2, 10, 18, 16], [15, 20, 19, 9],
            ...     ]
            >>> segment = [
            ...     0,
            ...     baca.coat(10),
            ...     baca.coat(18),
            ...     10, 18,
            ...     ]
            >>> contribution = music_maker(
            ...     'Voice 2',
            ...     collections,
            ...     baca.ImbricationCommand(
            ...         'Voice 1',
            ...         segment,
            ...         baca.accent(selector=baca.pheads()),
            ...         baca.beam_everything(),
            ...         ),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        {   % measure
                            \time 9/8
                            s1 * 9/8
                        }   % measure
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice 1"
                        {
                            \voiceOne
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16
                                    -\accent                                                             %! INDICATOR_COMMAND
                                    [
                                    s16
                                    s16
                                    s16
                                    s16
                                }
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    s16
                                    s16
                                    s16
                                }
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16
                                    -\accent                                                             %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16
                                    -\accent                                                             %! INDICATOR_COMMAND
                                    s16
                                }
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    s16
                                    s16
                                    s16
                                    ]
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                        \context Voice = "Voice 2"
                        {
                            \voiceTwo
                            {
                                \scaleDurations #'(1 . 1) {
                                    c'16
                                    [
                                    d'16
                                    bf'16
                                    fs''16
                                    e''16
                                    ]
                                }
                                \scaleDurations #'(1 . 1) {
                                    ef''16
                                    [
                                    af''16
                                    g''16
                                    a'16
                                    ]
                                }
                                \scaleDurations #'(1 . 1) {
                                    c'16
                                    [
                                    d'16
                                    bf'16
                                    fs''16
                                    e''16
                                    ]
                                }
                                \scaleDurations #'(1 . 1) {
                                    ef''16
                                    [
                                    af''16
                                    g''16
                                    a'16
                                    ]
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Segment-maker allows for beam extension.

            Extends beam across figures:

                >>> music_maker = baca.MusicMaker(
                ...     rmakers.BeamSpecifier(
                ...         beam_divisions_together=True,
                ...         ),
                ...     )

            >>> voice_1_selections = []
            >>> voice_2_selections = []
            >>> time_signatures = []
            >>> contribution = music_maker(
            ...     'Voice 2',
            ...     [[0, 2, 10, 18], [16, 15, 23]],
            ...     baca.ImbricationCommand(
            ...         'Voice 1',
            ...         [2, 10],
            ...         baca.staccato(selector=baca.pheads()),
            ...         baca.beam_everything(),
            ...         extend_beam=True,
            ...         ),
            ...     )
            >>> dictionary = contribution.selections
            >>> voice_1_selections.append(dictionary['Voice 1'])
            >>> voice_2_selections.append(dictionary['Voice 2'])
            >>> time_signatures.append(contribution.time_signature)
            >>> contribution = music_maker(
            ...     'Voice 2',
            ...     [[19, 13, 9, 8]],
            ...     baca.ImbricationCommand(
            ...         'Voice 1',
            ...         [13, 9],
            ...         baca.staccato(selector=baca.pheads()),
            ...         baca.beam_everything(),
            ...         ),
            ...     )
            >>> dictionary = contribution.selections
            >>> voice_1_selections.append(dictionary['Voice 1'])
            >>> voice_2_selections.append(dictionary['Voice 2'])
            >>> time_signatures.append(contribution.time_signature)

            >>> maker = baca.SegmentMaker(
            ...     ignore_repeat_pitch_classes=True,
            ...     score_template=baca.TwoVoiceStaffScoreTemplate(),
            ...     spacing=baca.HorizontalSpacingSpecifier(
            ...         minimum_duration=abjad.Duration(1, 24),
            ...         ),
            ...     time_signatures=time_signatures,
            ...     )
            >>> maker(
            ...     ('MusicVoiceTwo', 1),
            ...     baca.RhythmCommand(
            ...         rhythm_maker=voice_2_selections[0],
            ...         ),
            ...     )
            >>> maker(
            ...     ('MusicVoiceTwo', 2),
            ...     baca.RhythmCommand(
            ...         rhythm_maker=voice_2_selections[1],
            ...         ),
            ...     )
            >>> maker(
            ...     ('MusicVoiceOne', 1),
            ...     baca.RhythmCommand(
            ...         rhythm_maker=voice_1_selections[0],
            ...         ),
            ...     )
            >>> maker(
            ...     ('MusicVoiceOne', 2),
            ...     baca.RhythmCommand(
            ...         rhythm_maker=voice_1_selections[1],
            ...         ),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! COMMENT_MEASURE_NUMBERS
                            \baca_new_spacing_section #1 #24                                             %! HSS1:SPACING
                            \time 7/16                                                                   %! SET_STATUS_TAG:EXPLICIT_TIME_SIGNATURE:MAKE_GLOBAL_SKIPS_2
                            \baca_time_signature_color "blue"                                            %! ATTACH_COLOR_LITERAL_2:EXPLICIT_TIME_SIGNATURE_COLOR:MAKE_GLOBAL_SKIPS_2
                            s1 * 7/16                                                                    %! MAKE_GLOBAL_SKIPS_1
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! COMMENT_MEASURE_NUMBERS
                            \baca_new_spacing_section #1 #24                                             %! HSS1:SPACING
                            \time 1/4                                                                    %! SET_STATUS_TAG:EXPLICIT_TIME_SIGNATURE:MAKE_GLOBAL_SKIPS_2
                            \baca_time_signature_color "blue"                                            %! ATTACH_COLOR_LITERAL_2:EXPLICIT_TIME_SIGNATURE_COLOR:MAKE_GLOBAL_SKIPS_2
                            s1 * 1/4                                                                     %! MAKE_GLOBAL_SKIPS_1
                            \baca_bar_line_visible                                                       %! ATTACH_FINAL_BAR_LINE
                            \bar "|"                                                                     %! ATTACH_FINAL_BAR_LINE
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context MusicStaff = "MusicStaff"
                        <<
                            \context MusicVoiceOne = "MusicVoiceOne"
                            {
                                {
                                    \override TupletBracket.stencil = ##f
                                    \override TupletNumber.stencil = ##f
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoiceOne measure 1]                                      %! COMMENT_MEASURE_NUMBERS
                                        s16
                                        [                                                                %! SM_35
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2                                       %! SM_35
                                        \set stemRightBeamCount = 2                                      %! SM_35
                                        d'16
                                        -\staccato                                                       %! INDICATOR_COMMAND
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2                                       %! SM_35
                                        \set stemRightBeamCount = 2                                      %! SM_35
                                        bf'!16
                                        -\staccato                                                       %! INDICATOR_COMMAND
                <BLANKLINE>
                                        s16
                                    }
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        s16
                <BLANKLINE>
                                        s16
                                    }
                                    \revert TupletBracket.stencil
                                    \revert TupletNumber.stencil
                                }
                                {
                                    \override TupletBracket.stencil = ##f
                                    \override TupletNumber.stencil = ##f
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoiceOne measure 2]                                      %! COMMENT_MEASURE_NUMBERS
                                        s16
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2                                       %! SM_35
                                        \set stemRightBeamCount = 2                                      %! SM_35
                                        cs''!16
                                        -\staccato                                                       %! INDICATOR_COMMAND
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2                                       %! SM_35
                                        \set stemRightBeamCount = 2                                      %! SM_35
                                        a'16
                                        -\staccato                                                       %! INDICATOR_COMMAND
                <BLANKLINE>
                                        s16
                                        ]                                                                %! SM_35
                <BLANKLINE>
                                    }
                                    \revert TupletBracket.stencil
                                    \revert TupletNumber.stencil
                                }
                            }
                            \context MusicVoiceTwo = "MusicVoiceTwo"
                            {
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoiceTwo measure 1]                                      %! COMMENT_MEASURE_NUMBERS
                                        \set stemLeftBeamCount = 0
                                        \set stemRightBeamCount = 2
                                        c'16
                                        [
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        d'16
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        bf'!16
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 1
                                        fs''!16
                                    }
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        \set stemLeftBeamCount = 1
                                        \set stemRightBeamCount = 2
                                        e''16
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        ef''!16
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 0
                                        b''16
                                        ]
                                    }
                                }
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoiceTwo measure 2]                                      %! COMMENT_MEASURE_NUMBERS
                                        \set stemLeftBeamCount = 0
                                        \set stemRightBeamCount = 2
                                        g''16
                                        [
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        cs''!16
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 2
                                        a'16
                <BLANKLINE>
                                        \set stemLeftBeamCount = 2
                                        \set stemRightBeamCount = 0
                                        af'!16
                                        ]
                <BLANKLINE>
                                    }
                                }
                            }
                        >>
                    >>
                >>

        ..  container:: example

            Works with chords:

            >>> music_maker = baca.MusicMaker(
            ...     rmakers.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         ),
            ...     )

            >>> collections = [
            ...     {0, 2, 10, 18, 16},
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     ]
            >>> contribution = music_maker(
            ...     'Voice 2',
            ...     collections,
            ...     baca.ImbricationCommand(
            ...         'Voice 1',
            ...         [2, 19, 9, 18, 16],
            ...         ),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        {   % measure
                            \time 11/16
                            s1 * 11/16
                        }   % measure
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice 1"
                        {
                            \voiceOne
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1) {
                                    d'16
                                }
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    s16
                                    g''16
                                    [
                                    a'16
                                    ]
                                    s16
                                }
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    s16
                                    fs''16
                                    [
                                    e''16
                                    ]
                                    s16
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                        \context Voice = "Voice 2"
                        {
                            \voiceTwo
                            {
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    <c' d' bf' e'' fs''>16
                                    [
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    c'16
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    d'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    e''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    ef''16
                                    ]
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Works with rests:

            >>> music_maker = baca.MusicMaker(
            ...     rmakers.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     ]
            >>> contribution = music_maker(
            ...     'Voice 2',
            ...     collections,
            ...     baca.ImbricationCommand(
            ...         'Voice 1',
            ...         [2, 19, 9, 18, 16],
            ...         ),
            ...     baca.rests_around([2], [2]),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        {   % measure
                            \time 19/16
                            s1 * 19/16
                        }   % measure
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice 1"
                        {
                            \voiceOne
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1) {
                                    s8
                                    s16
                                    d'16
                                    s16
                                    s16
                                    s16
                                }
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    s16
                                    g''16
                                    [
                                    a'16
                                    ]
                                    s16
                                }
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    s16
                                    fs''16
                                    [
                                    e''16
                                    ]
                                    s16
                                    s8
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                        \context Voice = "Voice 2"
                        {
                            \voiceTwo
                            {
                                \scaleDurations #'(1 . 1) {
                                    r8
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    c'16
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    c'16
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    d'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    e''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    ef''16
                                    ]
                                    r8
                                }
                            }
                        }
                    >>
                >>

        Returns new container.
        """
        original_container = container
        container = copy.deepcopy(container)
        abjad.override(container).tuplet_bracket.stencil = False
        abjad.override(container).tuplet_number.stencil = False
        segment = classes.Sequence(self.segment).flatten(depth=-1)
        if self.by_pitch_class:
            segment = [abjad.NumberedPitchClass(_) for _ in segment]
        cursor = classes.Cursor(
            singletons=True,
            source=segment,
            suppress_exception=True,
            )
        pitch_number = cursor.next()
        if self.selector is not None:
            selection = self.selector(original_container)
        selected_logical_ties = None
        if self.selector is not None:
            selection = self.selector(container)
            agent = abjad.iterate(selection)
            selected_logical_ties = agent.logical_ties(pitched=True)
            selected_logical_ties = list(selected_logical_ties)
        selector = abjad.select(original_container)
        original_logical_ties = selector.logical_ties()
        logical_ties = abjad.select(container).logical_ties()
        pairs = zip(logical_ties, original_logical_ties)
        for logical_tie, original_logical_tie in pairs:
            if (selected_logical_ties is not None and
                logical_tie not in selected_logical_ties):
                for leaf in logical_tie:
                    duration = leaf.written_duration
                    skip = abjad.Skip(duration)
                    abjad.mutate(leaf).replace([skip])
            elif isinstance(logical_tie.head, abjad.Rest):
                for leaf in logical_tie:
                    duration = leaf.written_duration
                    skip = abjad.Skip(duration)
                    abjad.mutate(leaf).replace([skip])
            elif isinstance(logical_tie.head, abjad.Skip):
                pass
            elif self._matches_pitch(logical_tie.head, pitch_number):
                if isinstance(pitch_number, Coat):
                    for leaf in logical_tie:
                        duration = leaf.written_duration
                        skip = abjad.Skip(duration)
                        abjad.mutate(leaf).replace([skip])
                    pitch_number = cursor.next()
                    continue
                self._trim_matching_chord(logical_tie, pitch_number)
                pitch_number = cursor.next()
                if self.truncate_ties:
                    for leaf in logical_tie[1:]:
                        duration = leaf.written_duration
                        skip = abjad.Skip(duration)
                        abjad.mutate(leaf).replace([skip])
                if self.hocket:
                    for leaf in original_logical_tie:
                        duration = leaf.written_duration
                        skip = abjad.Skip(duration)
                        abjad.mutate(leaf).replace([skip])
            else:
                for leaf in logical_tie:
                    duration = leaf.written_duration
                    skip = abjad.Skip(duration)
                    abjad.mutate(leaf).replace([skip])
        if not self.allow_unused_pitches and not cursor.is_exhausted:
            current, total = cursor.position - 1, len(cursor)
            message = f'{cursor!r} used only {current} of {total} pitches.'
            raise Exception(message)
        self._apply_specifiers(container)
        if self.extend_beam:
            last_leaf = abjad.select(container).leaf(-1)
            abjad.attach(abjad.tags.RIGHT_BROKEN_BEAM, last_leaf)
        selection = abjad.select(container)
        if not self.hocket:
            for pleaf in classes.Selection(container).pleaves():
                abjad.attach(abjad.tags.ALLOW_OCTAVE, pleaf)
        return {self.voice_name: selection}

    ### PRIVATE METHODS ###

    def _apply_specifiers(self, container):
        assert isinstance(container, abjad.Container), repr(container)
        nested_selections = None
        specifiers = self.specifiers or []
        selections = container[:]
        for specifier in specifiers:
            if isinstance(specifier, PitchFirstRhythmCommand):
                continue
            if isinstance(specifier, rhythmcommands.RhythmCommand):
                continue
            if isinstance(specifier, ImbricationCommand):
                continue
            if isinstance(specifier, rmakers.BeamSpecifier):
                specifier._detach_all_beams(selections)
            if isinstance(specifier, NestingCommand):
                nested_selections = specifier(selections)
            else:
                specifier(selections)
        if nested_selections is not None:
            return nested_selections
        return selections

    @staticmethod
    def _matches_pitch(pitched_leaf, pitch_object):
        if isinstance(pitch_object, Coat):
            pitch_object = pitch_object.argument
        if pitch_object is None:
            return False
        if isinstance(pitched_leaf, abjad.Note):
            written_pitches = [pitched_leaf.written_pitch]
        elif isinstance(pitched_leaf, abjad.Chord):
            written_pitches = pitched_leaf.written_pitches
        else:
            raise TypeError(pitched_leaf)
        if isinstance(pitch_object, (int, float)):
            source = [_.number for _ in written_pitches]
        elif isinstance(pitch_object, abjad.NamedPitch):
            source = written_pitches
        elif isinstance(pitch_object, abjad.NumberedPitch):
            source = [abjad.NumberedPitch(_) for _ in written_pitches]
        elif isinstance(pitch_object, abjad.NamedPitchClass):
            source = [abjad.NamedPitchClass(_) for _ in written_pitches]
        elif isinstance(pitch_object, abjad.NumberedPitchClass):
            source = [abjad.NumberedPitchClass(_) for _ in written_pitches]
        else:
            raise TypeError(f'unknown pitch object: {pitch_object!r}.')
        if not type(source[0]) is type(pitch_object):
            raise TypeError(f'{source!r} type must match {pitch_object!r}.')
        return pitch_object in source

    @staticmethod
    def _trim_matching_chord(logical_tie, pitch_object):
        if isinstance(logical_tie.head, abjad.Note):
            return
        assert isinstance(logical_tie.head, abjad.Chord), repr(logical_tie)
        if isinstance(pitch_object, abjad.PitchClass):
            raise NotImplementedError(logical_tie, pitch_object)
        for chord in logical_tie:
            duration = chord.written_duration
            note = abjad.Note(pitch_object, duration)
            abjad.mutate(chord).replace([note])

    ### PUBLIC PROPERTIES ###

    @property
    def allow_unused_pitches(self):
        r"""
        Is true when specifier allows unused pitches.

        ..  container:: example

            Allows unused pitches:

            >>> music_maker = baca.MusicMaker(
            ...     rmakers.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         beam_rests=True,
            ...         ),
            ...     baca.staccato(selector=baca.pheads()),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     ]
            >>> contribution = music_maker(
            ...     'Voice 2',
            ...     collections,
            ...     baca.ImbricationCommand(
            ...         'Voice 1',
            ...         [2, 19, 9, 18, 16],
            ...         baca.accent(selector=baca.pheads()),
            ...         baca.beam_everything(),
            ...         allow_unused_pitches=True,
            ...         ),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        {   % measure
                            \time 5/8
                            s1 * 5/8
                        }   % measure
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice 1"
                        {
                            \voiceOne
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    -\accent                                                             %! INDICATOR_COMMAND
                                    s16
                                    s16
                                    s16
                                }
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16
                                    -\accent                                                             %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16
                                    -\accent                                                             %! INDICATOR_COMMAND
                                    s16
                                    ]
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                        \context Voice = "Voice 2"
                        {
                            \voiceTwo
                            {
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    c'16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    ]
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Raises exception on unused pitches:

            >>> music_maker = baca.MusicMaker(
            ...     rmakers.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         beam_rests=True,
            ...         ),
            ...     baca.staccato(selector=baca.pheads()),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     ]
            >>> result = music_maker(
            ...     'Voice 2',
            ...     collections,
            ...     baca.ImbricationCommand(
            ...         'Voice 1',
            ...         [2, 19, 9, 18, 16],
            ...         baca.accent(selector=baca.pheads()),
            ...         baca.beam_everything(),
            ...         ),
            ...     )
            Traceback (most recent call last):
                ...
            Exception: Cursor(source=Sequence(items=(2, 19, 9, 18, 16)),
            position=4, singletons=True, suppress_exception=True) used only 3
            of 5 pitches.

        ..  container:: example

            Defaults to none:

            >>> specifier = baca.ImbricationCommand()
            >>> specifier.allow_unused_pitches is None
            True

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._allow_unused_pitches

    @property
    def by_pitch_class(self):
        """
        Is true when specifier matches on pitch-class rather than pitch.

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        """
        return self._by_pitch_class

    @property
    def extend_beam(self):
        """
        Is true when specifier extends beam.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._extend_beam

    @property
    def hocket(self):
        r"""
        Is true when specifier hockets voices.

        ..  container:: example

            Hockets voices:

            >>> music_maker = baca.MusicMaker(
            ...     rmakers.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         beam_rests=True,
            ...         ),
            ...     baca.staccato(selector=baca.pheads()),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     ]
            >>> contribution = music_maker(
            ...     'Voice 2',
            ...     collections,
            ...     baca.ImbricationCommand(
            ...         'Voice 1',
            ...         [2, 19, 9, 18, 16],
            ...         baca.accent(selector=baca.pheads()),
            ...         baca.beam_everything(),
            ...         hocket=True,
            ...         ),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        {   % measure
                            \time 15/16
                            s1 * 15/16
                        }   % measure
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice 1"
                        {
                            \voiceOne
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    -\accent                                                             %! INDICATOR_COMMAND
                                    s16
                                    s16
                                    s16
                                }
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16
                                    -\accent                                                             %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16
                                    -\accent                                                             %! INDICATOR_COMMAND
                                    s16
                                }
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16
                                    -\accent                                                             %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    e''16
                                    -\accent                                                             %! INDICATOR_COMMAND
                                    s16
                                    ]
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                        \context Voice = "Voice 2"
                        {
                            \voiceTwo
                            {
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    [
                                    s16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    s16
                                    s16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    c'16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    d'16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    s16
                                    s16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    ef''16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    ]
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Defaults to none:

            >>> specifier = baca.ImbricationCommand()
            >>> specifier.hocket is None
            True

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._hocket

    @property
    def segment(self):
        """
        Gets to-be-imbricated segment.

        Returns pitch or pitch-class segment.
        """
        return self._segment

    @property
    def selector(self):
        r"""
        Gets selector.

        ..  container:: example

            Selects last nine notes:

            >>> music_maker = baca.MusicMaker(
            ...     rmakers.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         beam_rests=True,
            ...         ),
            ...     baca.staccato(selector=baca.pheads()),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18, 16], [15, 20, 19, 9],
            ...     [0, 2, 10, 18, 16], [15, 20, 19, 9],
            ...     ]
            >>> contribution = music_maker(
            ...     'Voice 2',
            ...     collections,
            ...     baca.ImbricationCommand(
            ...         'Voice 1',
            ...         [2, 18, 16, 15],
            ...         baca.accent(selector=baca.pheads()),
            ...         baca.beam_everything(),
            ...         selector=baca.plts()[-9:],
            ...         ),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        {   % measure
                            \time 9/8
                            s1 * 9/8
                        }   % measure
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice 1"
                        {
                            \voiceOne
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    [
                                    s16
                                    s16
                                    s16
                                    s16
                                }
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    s16
                                    s16
                                    s16
                                }
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    -\accent                                                             %! INDICATOR_COMMAND
                                    s16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16
                                    -\accent                                                             %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16
                                    -\accent                                                             %! INDICATOR_COMMAND
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16
                                    -\accent                                                             %! INDICATOR_COMMAND
                                    s16
                                    s16
                                    s16
                                    ]
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                        \context Voice = "Voice 2"
                        {
                            \voiceTwo
                            {
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    a'16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    c'16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    a'16
                                    -\staccato                                                           %! INDICATOR_COMMAND
                                    ]
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Defaults to none:

            >>> specifier = baca.ImbricationCommand()
            >>> specifier.selector is None
            True

        Set to selector or none.

        Returns selector or none.
        """
        return self._selector

    @property
    def specifiers(self):
        r"""
        Gets specifiers.

        ..  container:: example

            Beams nothing:

            >>> music_maker = baca.MusicMaker(
            ...     rmakers.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     ]
            >>> contribution = music_maker(
            ...     'Voice 2',
            ...     collections,
            ...     baca.ImbricationCommand(
            ...         'Voice 1',
            ...         [2, 19, 9, 18, 16],
            ...         rmakers.BeamSpecifier(
            ...             beam_each_division=False,
            ...             ),
            ...         ),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        {   % measure
                            \time 15/16
                            s1 * 15/16
                        }   % measure
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice 1"
                        {
                            \voiceOne
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    d'16
                                    s16
                                    s16
                                    s16
                                }
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    s16
                                    g''16
                                    a'16
                                    s16
                                }
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    s16
                                    fs''16
                                    e''16
                                    s16
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                        \context Voice = "Voice 2"
                        {
                            \voiceTwo
                            {
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    c'16
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    d'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    e''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    ef''16
                                    ]
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Beams divisions together but excludes skips:

            >>> music_maker = baca.MusicMaker(
            ...     rmakers.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     ]
            >>> contribution = music_maker(
            ...     'Voice 2',
            ...     collections,
            ...     baca.ImbricationCommand(
            ...         'Voice 1',
            ...         [2, 19, 9, 18, 16],
            ...         rmakers.BeamSpecifier(
            ...             beam_divisions_together=True,
            ...             ),
            ...         ),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        {   % measure
                            \time 15/16
                            s1 * 15/16
                        }   % measure
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice 1"
                        {
                            \voiceOne
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    [
                                    ]
                                    s16
                                    s16
                                    s16
                                }
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16
                                    ]
                                    s16
                                }
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    e''16
                                    ]
                                    s16
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                        \context Voice = "Voice 2"
                        {
                            \voiceTwo
                            {
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    c'16
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    d'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    e''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    ef''16
                                    ]
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Beams divisions together and includes skips:

            >>> music_maker = baca.MusicMaker(
            ...     rmakers.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     ]
            >>> contribution = music_maker(
            ...     'Voice 2',
            ...     collections,
            ...     baca.ImbricationCommand(
            ...         'Voice 1',
            ...         [2, 19, 9, 18, 16],
            ...         baca.beam_everything(),
            ...         ),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        {   % measure
                            \time 15/16
                            s1 * 15/16
                        }   % measure
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice 1"
                        {
                            \voiceOne
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    s16
                                    s16
                                    s16
                                }
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16
                                    s16
                                }
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    s16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    e''16
                                    s16
                                    ]
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                        \context Voice = "Voice 2"
                        {
                            \voiceTwo
                            {
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    c'16
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    d'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    e''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    ef''16
                                    ]
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Beams each division and includes skips:

            >>> music_maker = baca.MusicMaker(
            ...     rmakers.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     ]
            >>> contribution = music_maker(
            ...     'Voice 2',
            ...     collections,
            ...     baca.ImbricationCommand(
            ...         'Voice 1',
            ...         [2, 19, 9, 18, 16],
            ...         rmakers.BeamSpecifier(
            ...             beam_rests=True,
            ...             ),
            ...         ),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        {   % measure
                            \time 15/16
                            s1 * 15/16
                        }   % measure
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice 1"
                        {
                            \voiceOne
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    [
                                    d'16
                                    s16
                                    s16
                                    s16
                                    ]
                                }
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    [
                                    s16
                                    g''16
                                    a'16
                                    s16
                                    ]
                                }
                                \scaleDurations #'(1 . 1) {
                                    s16
                                    [
                                    s16
                                    fs''16
                                    e''16
                                    s16
                                    ]
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                        \context Voice = "Voice 2"
                        {
                            \voiceTwo
                            {
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    e''16
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    ef''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    g''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    c'16
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    d'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    fs''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    e''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    ef''16
                                    ]
                                }
                            }
                        }
                    >>
                >>

        Returns specifiers or none.
        """
        return list(self._specifiers)

    @property
    def truncate_ties(self):
        r"""
        Is true when specifier truncates ties.

        ..  container:: example

            Truncates ties:

            >>> music_maker = baca.MusicMaker(
            ...     baca.PitchFirstRhythmCommand(
            ...         rhythm_maker=baca.PitchFirstRhythmMaker(
            ...             talea=rmakers.Talea(
            ...                 counts=[5],
            ...                 denominator=32,
            ...                 ),
            ...             ),
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice 2',
            ...     collections,
            ...     baca.ImbricationCommand(
            ...         'Voice 1',
            ...         [2, 10, 18, 19, 9],
            ...         baca.beam_everything(),
            ...         truncate_ties=True,
            ...         ),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        {   % measure
                            \time 45/32
                            s1 * 45/32
                        }   % measure
                    }
                    \new Staff
                    <<
                        \context Voice = "Voice 1"
                        {
                            \voiceOne
                            {
                                \override TupletBracket.stencil = ##f
                                \override TupletNumber.stencil = ##f
                                \scaleDurations #'(1 . 1) {
                                    s8
                                    [
                                    s32
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    d'8
                                    s32
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    bf'8
                                    s32
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    fs''8
                                    s32
                                    s8
                                    s32
                                    s8
                                    s32
                                    s8
                                    s32
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    g''8
                                    s32
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 1
                                    a'8
                                    s32
                                    ]
                                }
                                \revert TupletBracket.stencil
                                \revert TupletNumber.stencil
                            }
                        }
                        \context Voice = "Voice 2"
                        {
                            \voiceTwo
                            {
                                \scaleDurations #'(1 . 1) {
                                    c'8
                                    ~
                                    [
                                    c'32
                                    d'8
                                    ~
                                    d'32
                                    bf'8
                                    ~
                                    bf'32
                                    ]
                                }
                                \scaleDurations #'(1 . 1) {
                                    fs''8
                                    ~
                                    [
                                    fs''32
                                    e''8
                                    ~
                                    e''32
                                    ef''8
                                    ~
                                    ef''32
                                    af''8
                                    ~
                                    af''32
                                    g''8
                                    ~
                                    g''32
                                    ]
                                }
                                \scaleDurations #'(1 . 1) {
                                    a'8
                                    ~
                                    [
                                    a'32
                                    ]
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Defaults to none:

            >>> specifier = baca.ImbricationCommand()
            >>> specifier.truncate_ties is None
            True

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._truncate_ties

    @property
    def voice_name(self):
        """
        Gets voice name.

        Returns string.
        """
        return self._voice_name

class LMRSpecifier(abjad.AbjadObject):
    """
    Left-middle-right specifier.

    ..  container:: example

        Default LMR specifier:

        >>> lmr_specifier = baca.LMRSpecifier()

        >>> parts = lmr_specifier([1])
        >>> for part in parts: part
        Sequence([1])

        >>> parts =lmr_specifier([1, 2])
        >>> for part in parts: part
        Sequence([1, 2])

        >>> parts = lmr_specifier([1, 2, 3])
        >>> for part in parts: part
        Sequence([1, 2, 3])

        >>> parts = lmr_specifier([1, 2, 3, 4])
        >>> for part in parts: part
        Sequence([1, 2, 3, 4])

        >>> parts = lmr_specifier([1, 2, 3, 4, 5])
        >>> for part in parts: part
        Sequence([1, 2, 3, 4, 5])

        >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
        >>> for part in parts: part
        Sequence([1, 2, 3, 4, 5, 6])

        >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
        >>> for part in parts: part
        Sequence([1, 2, 3, 4, 5, 6, 7])

        >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
        >>> for part in parts: part
        Sequence([1, 2, 3, 4, 5, 6, 7, 8])

        >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> for part in parts: part
        Sequence([1, 2, 3, 4, 5, 6, 7, 8, 9])

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_left_counts',
        '_left_cyclic',
        '_left_length',
        '_left_reversed',
        '_middle_counts',
        '_middle_cyclic',
        '_middle_reversed',
        '_priority',
        '_right_counts',
        '_right_cyclic',
        '_right_length',
        '_right_reversed',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        left_counts=None,
        left_cyclic=None,
        left_length=None,
        left_reversed=None,
        middle_counts=None,
        middle_cyclic=None,
        middle_reversed=None,
        priority=None,
        right_counts=None,
        right_cyclic=None,
        right_length=None,
        right_reversed=None,
        ):
        if left_counts is not None:
            assert abjad.mathtools.all_are_positive_integers(left_counts)
        self._left_counts = left_counts
        if left_cyclic is not None:
            left_cyclic = bool(left_cyclic)
        self._left_cyclic = left_cyclic
        if left_length is not None:
            left_length = int(left_length)
            assert 0 <= left_length, repr(left_length)
        self._left_length = left_length
        if left_reversed is not None:
            left_reversed = bool(left_reversed)
        self._left_reversed = left_reversed
        if middle_counts is not None:
            assert abjad.mathtools.all_are_positive_integers(middle_counts)
        self._middle_counts = middle_counts
        if middle_cyclic is not None:
            middle_cyclic = bool(middle_cyclic)
        self._middle_cyclic = middle_cyclic
        if middle_reversed is not None:
            middle_reversed = bool(middle_reversed)
        self._middle_reversed = middle_reversed
        if priority is not None:
            assert priority in (abjad.Left, abjad.Right)
        self._priority = priority
        if right_counts is not None:
            assert abjad.mathtools.all_are_positive_integers(right_counts)
        self._right_counts = right_counts
        if right_cyclic is not None:
            right_cyclic = bool(right_cyclic)
        self._right_cyclic = right_cyclic
        if right_length is not None:
            right_length = int(right_length)
            assert 0 <= right_length, repr(right_length)
        self._right_length = right_length
        if right_reversed is not None:
            right_reversed = bool(right_reversed)
        self._right_reversed = right_reversed

    ### SPECIAL METHODS ###

    def __call__(self, sequence=None):
        """
        Calls LMR specifier on ``sequence``.

        Returns list of subsequences.
        """
        top_lengths = self._get_top_lengths(len(sequence))
        top_parts = abjad.sequence(sequence).partition_by_counts(
            top_lengths,
            cyclic=False,
            overhang=abjad.Exact,
            )
        parts = []
        left_part, middle_part, right_part = top_parts
        if left_part:
            if self.left_counts:
                parts_ = abjad.sequence(left_part).partition_by_counts(
                    self.left_counts,
                    cyclic=self.left_cyclic,
                    overhang=True,
                    reversed_=self.left_reversed,
                    )
                parts.extend(parts_)
            else:
                parts.append(left_part)
        if middle_part:
            if self.middle_counts:
                parts_ = abjad.sequence(middle_part).partition_by_counts(
                    self.middle_counts,
                    cyclic=self.middle_cyclic,
                    overhang=True,
                    reversed_=self.middle_reversed,
                    )
                parts.extend(parts_)
            else:
                parts.append(middle_part)
        if right_part:
            if self.right_counts:
                parts_ = abjad.sequence(right_part).partition_by_counts(
                    self.right_counts,
                    cyclic=self.right_cyclic,
                    overhang=True,
                    reversed_=self.right_reversed,
                    )
                parts.extend(parts_)
            else:
                parts.append(right_part)
        return parts

    ### PRIVATE METHODS ###

    def _get_priority(self):
        if self.priority is None:
            return abjad.Left
        return self.priority

    def _get_top_lengths(self, total_length):
        left_length, middle_length, right_length = 0, 0, 0
        left_length = self.left_length or 0
        middle_length = 0
        right_length = self.right_length or 0
        if left_length and right_length:
            if self._get_priority() == abjad.Left:
                left_length = self.left_length or 0
                left_length = min([left_length, total_length])
                remaining_length = total_length - left_length
                if self.right_length is None:
                    right_length = remaining_length
                    middle_length = 0
                else:
                    right_length = self.right_length or 0
                    right_length = min([right_length, remaining_length])
                    remaining_length = total_length - (left_length + right_length)
                    middle_length = remaining_length
            else:
                right_length = self.right_length or 0
                right_length = min([right_length, total_length])
                remaining_length = total_length - right_length
                if self.left_length is None:
                    left_length = remaining_length
                    middle_length = 0
                else:
                    left_length = self.left_length or 0
                    left_length = min([left_length, remaining_length])
                    remaining_length = total_length - (right_length + left_length)
                    middle_length = remaining_length
        elif left_length and not right_length:
            left_length = min([left_length, total_length])
            remaining_length = total_length - left_length
            right_length = remaining_length
        elif not left_length and right_length:
            right_length = min([right_length, total_length])
            remaining_length = total_length - right_length
            left_length = remaining_length
        elif not left_length and not right_length:
            middle_length = total_length
        return left_length, middle_length, right_length

    ### PUBLIC PROPERTIES ###

    @property
    def left_counts(self):
        """
        Gets left counts.

        ..  container:: example

            Left counts equal to a single 1:

            >>> lmr_specifier = baca.LMRSpecifier(
            ...     left_counts=[1],
            ...     left_cyclic=False,
            ...     left_length=3,
            ...     right_length=2,
            ...     )

            >>> parts = lmr_specifier([1])
            >>> for part in parts: part
            Sequence([1])

            >>> parts = lmr_specifier([1, 2])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])

            >>> parts = lmr_specifier([1, 2, 3])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])

            >>> parts = lmr_specifier([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4, 5])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4])
            Sequence([5, 6])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4, 5])
            Sequence([6, 7])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4, 5, 6])
            Sequence([7, 8])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4, 5, 6, 7])
            Sequence([8, 9])

        ..  container:: example

            Left counts all equal to 1:

            >>> lmr_specifier = baca.LMRSpecifier(
            ...     left_counts=[1],
            ...     left_cyclic=True,
            ...     left_length=3,
            ...     right_length=2,
            ...     )

            >>> parts = lmr_specifier([1])
            >>> for part in parts: part
            Sequence([1])

            >>> parts = lmr_specifier([1, 2])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])

            >>> parts = lmr_specifier([1, 2, 3])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])
            Sequence([3])

            >>> parts = lmr_specifier([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])
            Sequence([3])
            Sequence([4])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])
            Sequence([3])
            Sequence([4, 5])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])
            Sequence([3])
            Sequence([4])
            Sequence([5, 6])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])
            Sequence([3])
            Sequence([4, 5])
            Sequence([6, 7])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])
            Sequence([3])
            Sequence([4, 5, 6])
            Sequence([7, 8])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])
            Sequence([3])
            Sequence([4, 5, 6, 7])
            Sequence([8, 9])

        Defaults to none.

        Set to positive integers or none.

        Returns tuple of positive integers or none.
        """
        return self._left_counts

    @property
    def left_cyclic(self):
        """
        Is true when specifier reads left counts cyclically.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._left_cyclic

    @property
    def left_length(self):
        """
        Gets left length.

        ..  container:: example

            Left length equal to 2:

            >>> lmr_specifier = baca.LMRSpecifier(
            ...     left_length=2,
            ...     )

            >>> parts = lmr_specifier([1])
            >>> for part in parts: part
            Sequence([1])

            >>> parts = lmr_specifier([1, 2])
            >>> for part in parts: part
            Sequence([1, 2])

            >>> parts = lmr_specifier([1, 2, 3])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3])

            >>> parts = lmr_specifier([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6, 7])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6, 7, 8])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6, 7, 8, 9])

        Defaults to none.

        Set to nonnegative integer or none.

        Returns nonnegative integer or none.
        """
        return self._left_length

    @property
    def left_reversed(self):
        """
        Is true when specifier reverses left partition.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._left_reversed

    @property
    def middle_counts(self):
        """
        Gets middle counts.

        Defaults to none.

        Set to positive integers or none.

        Returns positive integers or none.
        """
        return self._middle_counts

    @property
    def middle_cyclic(self):
        """
        Is true when specifier reads middle counts cyclically.

        ..  container:: example

            Cyclic middle counts equal to [2]:

            >>> lmr_specifier = baca.LMRSpecifier(
            ...     middle_counts=[2],
            ...     middle_cyclic=True,
            ...     )

            >>> parts = lmr_specifier([1])
            >>> for part in parts: part
            Sequence([1])

            >>> parts = lmr_specifier([1, 2])
            >>> for part in parts: part
            Sequence([1, 2])

            >>> parts = lmr_specifier([1, 2, 3])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3])

            >>> parts = lmr_specifier([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5, 6])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5, 6])
            Sequence([7])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5, 6])
            Sequence([7, 8])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5, 6])
            Sequence([7, 8])
            Sequence([9])

            Odd parity produces length-1 part at right.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._middle_cyclic

    @property
    def middle_reversed(self):
        """
        Is true when specifier reverses middle partition.

        ..  container:: example

            Reversed cyclic middle counts equal to [2]:

            >>> lmr_specifier = baca.LMRSpecifier(
            ...     middle_counts=[2],
            ...     middle_cyclic=True,
            ...     middle_reversed=True,
            ...     )

            >>> parts = lmr_specifier([1])
            >>> for part in parts: part
            Sequence([1])

            >>> parts = lmr_specifier([1, 2])
            >>> for part in parts: part
            Sequence([1, 2])

            >>> parts = lmr_specifier([1, 2, 3])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])

            >>> parts = lmr_specifier([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4, 5])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5, 6])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4, 5])
            Sequence([6, 7])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5, 6])
            Sequence([7, 8])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4, 5])
            Sequence([6, 7])
            Sequence([8, 9])

            Odd parity produces length-1 part at left.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._middle_reversed

    @property
    def priority(self):
        """
        Gets priority.

        ..  container:: example

            Priority to the left:

            >>> lmr_specifier = baca.LMRSpecifier(
            ...     left_length=2,
            ...     right_length=1,
            ...     )

            >>> parts = lmr_specifier([1])
            >>> for part in parts: part
            Sequence([1])

            >>> parts = lmr_specifier([1, 2])
            >>> for part in parts: part
            Sequence([1, 2])

            >>> parts = lmr_specifier([1, 2, 3])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3])

            >>> parts = lmr_specifier([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3])
            Sequence([4])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5])
            Sequence([6])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6])
            Sequence([7])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6, 7])
            Sequence([8])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6, 7, 8])
            Sequence([9])

        ..  container:: example

            Priority to the right:

            >>> lmr_specifier = baca.LMRSpecifier(
            ...     left_length=2,
            ...     priority=abjad.Right,
            ...     right_length=1,
            ...     )

            >>> parts = lmr_specifier([1])
            >>> for part in parts: part
            Sequence([1])

            >>> parts = lmr_specifier([1, 2])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])

            >>> parts = lmr_specifier([1, 2, 3])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3])

            >>> parts = lmr_specifier([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3])
            Sequence([4])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])
            Sequence([5])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5])
            Sequence([6])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6])
            Sequence([7])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6, 7])
            Sequence([8])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4, 5, 6, 7, 8])
            Sequence([9])

        Defaults to none.

        Set to left, right or none.

        Returns left, right or none.
        """
        return self._priority

    @property
    def right_counts(self):
        """
        Gets right counts.

        Defaults to none.

        Set to positive integers or none.

        Returns positive integers or none.
        """
        return self._right_counts

    @property
    def right_cyclic(self):
        """
        Is true when specifier reads right counts cyclically.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._right_cyclic

    @property
    def right_length(self):
        """
        Gets right length.

        ..  container:: example

            Right length equal to 2:

            >>> lmr_specifier = baca.LMRSpecifier(
            ...     right_length=2,
            ...     )

            >>> parts = lmr_specifier([1])
            >>> for part in parts: part
            Sequence([1])

            >>> parts = lmr_specifier([1, 2])
            >>> for part in parts: part
            Sequence([1, 2])

            >>> parts = lmr_specifier([1, 2, 3])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])

            >>> parts = lmr_specifier([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1, 2])
            Sequence([3, 4])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1, 2, 3])
            Sequence([4, 5])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1, 2, 3, 4])
            Sequence([5, 6])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1, 2, 3, 4, 5])
            Sequence([6, 7])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1, 2, 3, 4, 5, 6])
            Sequence([7, 8])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1, 2, 3, 4, 5, 6, 7])
            Sequence([8, 9])

        ..  container:: example

            Right length equal to 2 and left counts equal to [1]:

            >>> lmr_specifier = baca.LMRSpecifier(
            ...     left_counts=[1],
            ...     left_cyclic=False,
            ...     right_length=2,
            ...     )

            >>> parts = lmr_specifier([1])
            >>> for part in parts: part
            Sequence([1])

            >>> parts = lmr_specifier([1, 2])
            >>> for part in parts: part
            Sequence([1, 2])

            >>> parts = lmr_specifier([1, 2, 3])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])

            >>> parts = lmr_specifier([1, 2, 3, 4])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2])
            Sequence([3, 4])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3])
            Sequence([4, 5])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3, 4])
            Sequence([5, 6])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3, 4, 5])
            Sequence([6, 7])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3, 4, 5, 6])
            Sequence([7, 8])

            >>> parts = lmr_specifier([1, 2, 3, 4, 5, 6, 7, 8, 9])
            >>> for part in parts: part
            Sequence([1])
            Sequence([2, 3, 4, 5, 6, 7])
            Sequence([8, 9])

        Defaults to none.

        Set to nonnegative integer or none.

        Returns nonnegative integer or none.
        """
        return self._right_length

    @property
    def right_reversed(self):
        """
        Is true when specifier reverses right partition.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._right_reversed

class MusicAccumulator(abjad.AbjadObject):
    """
    Music-accumulator.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_current_offset',
        '_figure_index',
        '_figure_names',
        '_floating_selections',
        '_music_maker',
        '_score_stop_offset',
        '_score_template',
        '_time_signatures',
        '_voice_names',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        score_template: abjad.ScoreTemplate,
        ) -> None:
        self._score_template = score_template
        voice_names = []
        dummy_score = score_template()
        for voice in abjad.iterate(dummy_score).components(abjad.Voice):
            voice_names.append(voice.name)
        self._voice_names = voice_names
        self._current_offset = abjad.Offset(0)
        self._figure_index = 0
        self._music_maker = self._make_default_figure_maker()
        self._figure_names: typing.List[str] = []
        self._floating_selections = self._make_voice_dictionary()
        self._score_stop_offset = abjad.Offset(0)
        self._time_signatures: typing.List[abjad.TimeSignature] = []

    ### SPECIAL METHODS ###

    def __call__(self, music_contribution=None):
        r"""
        Calls figure-accumulator on ``music_contribution``.

        Raises exception on duplicate figure name.

        ..  container:: example

            >>> score_template = baca.StringTrioScoreTemplate()
            >>> accumulator = baca.MusicAccumulator(score_template=score_template)
            >>> accumulator(
            ...     accumulator.music_maker(
            ...         'ViolinMusicVoice',
            ...         [[0, 1, 2, 3]],
            ...         figure_name='D',
            ...         ),
            ...     )

            >>> accumulator(
            ...     accumulator.music_maker(
            ...         'ViolinMusicVoice',
            ...         [[4, 5, 6, 7]],
            ...         figure_name='D',
            ...         ),
            ...     )
            Traceback (most recent call last):
                ...
            Exception: duplicate figure name: 'D'.

        Returns none.
        """
        self._cache_figure_name(music_contribution)
        self._cache_floating_selection(music_contribution)
        self._cache_time_signature(music_contribution)
        self._figure_index += 1

    ### PRIVATE METHODS ###

    def _cache_figure_name(self, music_contribution):
        if music_contribution.figure_name is None:
            return
        if music_contribution.figure_name in self._figure_names:
            name = music_contribution.figure_name
            raise Exception(f'duplicate figure name: {name!r}.')
        self._figure_names.append(music_contribution.figure_name)

    def _cache_floating_selection(self, music_contribution):
        for voice_name in music_contribution:
            voice_name = self.score_template.voice_abbreviations.get(
                voice_name,
                voice_name,
                )
            selection = music_contribution[voice_name]
            if not selection:
                continue
            start_offset = self._get_start_offset(
                selection,
                music_contribution,
                )
            stop_offset = start_offset + abjad.inspect(selection).duration()
            timespan = abjad.Timespan(start_offset, stop_offset)
            floating_selection = abjad.AnnotatedTimespan(
                timespan.start_offset,
                timespan.stop_offset,
                annotation=selection,
                )
            self._floating_selections[voice_name].append(floating_selection)
        self._current_offset = stop_offset
        self._score_stop_offset = max(self._score_stop_offset, stop_offset)

    def _cache_time_signature(self, music_contribution):
        if music_contribution.hide_time_signature:
            return
        if (music_contribution.anchor is None or
            music_contribution.hide_time_signature is False or
            (music_contribution.anchor and
            music_contribution.anchor.remote_voice_name is None)):
            self.time_signatures.append(music_contribution.time_signature)

    def _get_figure_start_offset(self, figure_name):
        for voice_name in sorted(self._floating_selections.keys()):
            for floating_selection in self._floating_selections[voice_name]:
                leaf_start_offset = floating_selection.start_offset
                leaves = abjad.iterate(floating_selection.annotation).leaves()
                for leaf in leaves:
                    markup = abjad.inspect(leaf).indicators(abjad.Markup)
                    for markup_ in markup:
                        if (isinstance(markup_._annotation, str) and
                            markup_._annotation.startswith('figure name: ')):
                            figure_name_ = markup_._annotation
                            figure_name_ = figure_name_.replace(
                                'figure name: ',
                                '',
                                )
                            if figure_name_ == figure_name:
                                return leaf_start_offset
                    leaf_duration = abjad.inspect(leaf).duration()
                    leaf_start_offset += leaf_duration
        raise Exception(f'can not find figure {figure_name!r}.')

    def _get_leaf_timespan(self, leaf, floating_selections):
        found_leaf = False
        for floating_selection in floating_selections:
            leaf_start_offset = abjad.Offset(0)
            for leaf_ in abjad.iterate(floating_selection.annotation).leaves():
                leaf_duration = abjad.inspect(leaf_).duration()
                if leaf_ is leaf:
                    found_leaf = True
                    break
                leaf_start_offset += leaf_duration
            if found_leaf:
                break
        if not found_leaf:
            raise Exception(f'can not find {leaf!r} in floating selections.')
        selection_start_offset = floating_selection.start_offset
        leaf_start_offset = selection_start_offset + leaf_start_offset
        leaf_stop_offset = leaf_start_offset + leaf_duration
        return abjad.Timespan(leaf_start_offset, leaf_stop_offset)

    def _get_start_offset(self, selection, music_contribution):
        if (music_contribution.anchor is not None and
            music_contribution.anchor.figure_name is not None):
            figure_name = music_contribution.anchor.figure_name
            start_offset = self._get_figure_start_offset(figure_name)
            return start_offset
        anchored = False
        if music_contribution.anchor is not None:
            remote_voice_name = music_contribution.anchor.remote_voice_name
            remote_selector = music_contribution.anchor.remote_selector
            use_remote_stop_offset = \
                music_contribution.anchor.use_remote_stop_offset
            anchored = True
        else:
            remote_voice_name = None
            remote_selector = None
            use_remote_stop_offset = None
        if not anchored:
            return self._current_offset
        if anchored and remote_voice_name is None:
            return self._score_stop_offset
        remote_selector = remote_selector or classes.selector().leaf(0)
        floating_selections = self._floating_selections[remote_voice_name]
        selections = [_.annotation for _ in floating_selections]
        result = remote_selector(selections)
        selected_leaves = list(abjad.iterate(result).leaves())
        first_selected_leaf = selected_leaves[0]
        timespan = self._get_leaf_timespan(
            first_selected_leaf,
            floating_selections,
            )
        if use_remote_stop_offset:
            remote_anchor_offset = timespan.stop_offset
        else:
            remote_anchor_offset = timespan.start_offset
        local_anchor_offset = abjad.Offset(0)
        if music_contribution.anchor is not None:
            local_selector = music_contribution.anchor.local_selector
        else:
            local_selector = None
        if local_selector is not None:
            result = local_selector(selection)
            selected_leaves = list(abjad.iterate(result).leaves())
            first_selected_leaf = selected_leaves[0]
            dummy_container = abjad.Container(selection)
            timespan = abjad.inspect(first_selected_leaf).timespan()
            del(dummy_container[:])
            local_anchor_offset = timespan.start_offset
        start_offset = remote_anchor_offset - local_anchor_offset
        return start_offset

    @staticmethod
    def _insert_skips(floating_selections, voice_name):
        for floating_selection in floating_selections:
            assert isinstance(floating_selection, abjad.AnnotatedTimespan)
        floating_selections = list(floating_selections)
        floating_selections.sort()
        try:
            first_start_offset = floating_selections[0].start_offset
        except:
            raise Exception(floating_selections, voice_name)
        timespans = abjad.TimespanList(floating_selections)
        gaps = ~timespans
        if 0 < first_start_offset:
            first_gap = abjad.Timespan(0, first_start_offset)
            gaps.append(first_gap)
        selections = floating_selections + list(gaps)
        selections.sort()
        fused_selection = []
        for selection in selections:
            if isinstance(selection, abjad.AnnotatedTimespan):
                fused_selection.extend(selection.annotation)
            else:
                assert isinstance(selection, abjad.Timespan)
                multiplier = abjad.Multiplier(selection.duration)
                skip = abjad.Skip(1)
                abjad.attach(multiplier, skip)
                fused_selection.append(skip)
        fused_selection = abjad.select(fused_selection)
        return fused_selection

    @staticmethod
    def _make_default_figure_maker():
        return MusicMaker(
            rmakers.BeamSpecifier(
                beam_divisions_together=True,
                ),
            PitchFirstRhythmCommand(
                rhythm_maker=PitchFirstRhythmMaker(
                    talea=rmakers.Talea(
                        counts=[1],
                        denominator=16,
                        ),
                    ),
                ),
            color_unregistered_pitches=True,
            denominator=16,
            )

    def _make_voice_dictionary(self):
        return dict([(_, []) for _ in self._voice_names])

    ### PUBLIC PROPERTIES ###

    @property
    def music_maker(self) -> 'MusicMaker':
        """
        Gets default music-maker.
        """
        return self._music_maker

    @property
    def score_template(self) -> abjad.ScoreTemplate:
        """
        Gets score template.
        """
        return self._score_template

    @property
    def time_signatures(self) -> typing.List[abjad.TimeSignature]:
        """
        Gets time signatures.
        """
        return self._time_signatures

    ### PUBLIC METHODS ###

    def assemble(self, voice_name):
        """
        Assembles complete selection for ``voice_name``.

        Returns selection or none.
        """
        floating_selections = self._floating_selections[voice_name]
        if not floating_selections:
            return
        selection = self._insert_skips(floating_selections, voice_name)
        assert isinstance(selection, abjad.Selection), repr(selection)
        return selection

    def populate_segment_maker(self, segment_maker):
        """
        Populates ``segment_maker``.

        Returns none.
        """
        for voice_name in sorted(self._floating_selections):
            selection = self.assemble(voice_name)
            if selection:
                segment_maker(
                    (voice_name, 1),
                    rhythmcommands.make_rhythm(selection)
                    )

    @staticmethod
    def show(contribution, time_signatures):
        """
        Makes rhythm-maker-style LilyPond file for documentation examples.

        Returns LilyPond file.
        """
        return abjad.LilyPondFile.rhythm(
            contribution,
            divisions=time_signatures,
            pitched_staff=True,
            )

class MusicContribution(abjad.AbjadValueObject):
    """
    Music contribution.

    ..  container:: example

        >>> baca.MusicContribution()
        MusicContribution()

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_anchor',
        '_color_selector',
        '_color_selector_result',
        '_figure_name',
        '_hide_time_signature',
        '_selections',
        '_state_manifest',
        '_time_signature',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        anchor=None,
        color_selector=None,
        color_selector_result=None,
        figure_name=None,
        hide_time_signature=None,
        selections=None,
        state_manifest=None,
        time_signature=None,
        ):
        if (anchor is not None and
            not isinstance(anchor, AnchorSpecifier)):
            raise TypeError(f'anchor specifier only: {anchor!r}.')
        self._anchor = anchor
        self._color_selector = color_selector
        self._color_selector_result = color_selector_result
        self._figure_name = figure_name
        if hide_time_signature is not None:
            hide_time_signature = bool(hide_time_signature)
        self._hide_time_signature = hide_time_signature
        self._selections = selections
        self._state_manifest = state_manifest
        self._time_signature = time_signature

    ### SPECIAL METHODS ###

    def __getitem__(self, voice_name):
        """
        Gets ``voice_name`` selection list.

        Returns list of selections.
        """
        return self.selections.__getitem__(voice_name)

    def __iter__(self):
        """
        Iterates figure contribution.

        Yields voice names.
        """
        for voice_name in self.selections:
            yield voice_name

    ### PRIVATE METHODS ###

    def _get_duration(self):
        durations = []
        for voice_name in sorted(self.selections):
            selection = self[voice_name]
            if selection:
                durations.append(abjad.inspect(selection).duration())
        assert len(set(durations)) == 1, repr(durations)
        return durations[0]

    ### PUBLIC PROPERTIES ###

    @property
    def anchor(self):
        """
        Gets anchor.

        Returns anchor specifier or none.
        """
        return self._anchor

    @property
    def color_selector(self):
        """
        Gets color selector.

        Returns selector or none.
        """
        return self._color_selector

    @property
    def color_selector_result(self):
        """
        Gets color selector result.

        Returns selector result or none.
        """
        return self._color_selector_result

    @property
    def figure_name(self):
        """
        Gets figure name.

        Returns string or none.
        """
        return self._figure_name

    @property
    def hide_time_signature(self):
        """
        Is true when contribution hides time signature.

        Returns true, false or none.
        """
        return self._hide_time_signature

    @property
    def selections(self):
        """
        Gets selections.

        Returns list of selections or none.
        """
        if self._selections is not None:
            assert isinstance(self._selections, dict), repr(self._selections)
            for value in self._selections.values():
                assert isinstance(value, abjad.Selection), repr(value)
        return self._selections

    @property
    def state_manifest(self):
        """
        Gets state manifest.

        Returns state manifest or none.
        """
        return self._state_manifest

    @property
    def time_signature(self):
        """
        Gets time signature.

        Returns time signature or none.
        """
        return self._time_signature

    ### PUBLIC METHODS ###

    def print_color_selector_result(self):
        """
        Prints color selector result.

        Returns none.
        """
        if self.color_selector is None:
            return
        if self.color_selector_result is None:
            return
        self.color_selector.print(self.color_selector_result)

class MusicMaker(abjad.AbjadObject):
    r"""
    Music-maker.

    >>> from abjadext import rmakers

    ..  container:: example

        Default music-maker:

        >>> music_maker = baca.MusicMaker()

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker('Voice 1', collections)
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            c'16
                            [
                            d'16
                            bf'16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''16
                            [
                            e''16
                            ef''16
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'16
                        }
                    }
                }
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_allow_repeats',
        '_color_unregistered_pitches',
        '_denominator',
        '_next_figure',
        '_specifiers',
        '_thread',
        '_voice_names',
        )

    _publish_storage_format = True

    _state_variables = (
        '_next_figure',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *specifiers,
        allow_repeats=None,
        color_unregistered_pitches=None,
        denominator=None,
        thread=None,
        voice_names=None
        ):
        specifiers = classes.Sequence(specifiers)
        specifiers = specifiers.flatten()
        if allow_repeats is not None:
            allow_repeats = bool(allow_repeats)
        self._allow_repeats = allow_repeats
        if color_unregistered_pitches is not None:
            color_unregistered_pitches = bool(color_unregistered_pitches)
        self._color_unregistered_pitches = color_unregistered_pitches
        if denominator is not None:
            assert abjad.mathtools.is_positive_integer(denominator)
        self._denominator = denominator
        self._next_figure = 0
        self._specifiers = specifiers
        if thread is not None:
            thread = bool(thread)
        self._thread = thread
        if voice_names is not None:
            assert all([isinstance(_, str) for _ in voice_names])
        self._voice_names = voice_names

    ### SPECIAL METHODS ###

    def __call__(
        self,
        voice_name,
        collections,
        *specifiers,
        allow_repeats=None,
        color_unregistered_pitches=None,
        counts=None,
        division_masks=None,
        exhaustive=None,
        extend_beam=None,
        figure_index=None,
        figure_name=None,
        hide_time_signature=None,
        imbrication_map=None,
        is_foreshadow=None,
        is_incomplete=None,
        is_recollection=None,
        logical_tie_masks=None,
        denominator=None,
        state_manifest=None,
        talea_denominator=None,
        thread=None,
        time_treatments=None,
        tuplet_denominator=None,
        tuplet_force_fraction=None
        ):
        r"""
        Calls music-maker on ``collections`` with keywords.

        ..  container:: example

            Default music-maker:

            >>> music_maker = baca.MusicMaker()

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                g''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a'16
                            }
                        }
                    }
                >>

        ..  container:: example

            Calltime counts:

            >>> music_maker = baca.MusicMaker()

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     counts=[1, 2],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'16
                                [
                                d'8
                                bf'16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                fs''16
                                [
                                e''8
                                ef''16
                                af''8
                                g''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a'16
                            }
                        }
                    }
                >>

        ..  container:: example

            Calltime denominator:

            >>> music_maker = baca.MusicMaker()

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     talea_denominator=32,
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'32
                                [
                                d'32
                                bf'32
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                fs''32
                                [
                                e''32
                                ef''32
                                af''32
                                g''32
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a'32
                            }
                        }
                    }
                >>

        ..  container:: example

            Calltime time treatments:

            >>> music_maker = baca.MusicMaker()

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     time_treatments=[1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 4/3 {
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/5 {
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                g''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a'16
                            }
                        }
                    }
                >>

        ..  container:: example

            Rest input:

            >>> music_maker = baca.MusicMaker()

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [abjad.Rest((3, 8)), abjad.Rest((3, 8))],
            ...     baca.nest('+1/8'),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/6 {
                                \scaleDurations #'(1 . 1) {
                                    r4.
                                    r4.
                                }
                            }
                        }
                    }
                >>

        ..  container:: example

            The following negative-valued talea count patterns work:

            >>> music_maker = baca.MusicMaker()

            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[18, 16, 15, 20, 19]],
            ...     counts=[2, -1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                fs''8
                                r16
                                e''8
                                r16
                                ef''8
                                r16
                                af''8
                                r16
                                g''8
                                r16
                            }
                        }
                    }
                >>

            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[18, 16, 15, 20, 19]],
            ...     counts=[2, -1, -1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                fs''8
                                r16
                                r16
                                e''8
                                r16
                                r16
                                ef''8
                                r16
                                r16
                                af''8
                                r16
                                r16
                                g''8
                                r16
                                r16
                            }
                        }
                    }
                >>

            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[18, 16, 15, 20, 19]],
            ...     counts=[-1, 2],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                r16
                                fs''8
                                r16
                                e''8
                                r16
                                ef''8
                                r16
                                af''8
                                r16
                                g''8
                            }
                        }
                    }
                >>

            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[18, 16, 15, 20, 19]],
            ...     counts=[-1, -1, 2],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                r16
                                r16
                                fs''8
                                r16
                                r16
                                e''8
                                r16
                                r16
                                ef''8
                                r16
                                r16
                                af''8
                                r16
                                r16
                                g''8
                            }
                        }
                    }
                >>

            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[18, 16, 15, 20, 19]],
            ...     counts=[-1, -1, 2, -2, -2],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                r16
                                r16
                                fs''8
                                r8
                                r8
                                r16
                                r16
                                e''8
                                r8
                                r8
                                r16
                                r16
                                ef''8
                                r8
                                r8
                                r16
                                r16
                                af''8
                                r8
                                r8
                                r16
                                r16
                                g''8
                                r8
                                r8
                            }
                        }
                    }
                >>

        ..  note:: Write hide_time_signature calltime examples.


        ..  container:: example

            Works with chords:

            >>> music_maker = baca.MusicMaker()

            >>> collections = [
            ...     {0, 2, 10},
            ...     [18, 16, 15, 20, 19],
            ...     [9],
            ...     ]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                <c' d' bf'>16
                            }
                            \scaleDurations #'(1 . 1) {
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                g''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a'16
                            }
                        }
                    }
                >>

        Returns selection, time signature, state manifest.
        """
        specifiers = classes.Sequence(specifiers)
        specifiers = specifiers.flatten()
        if self._is_pitch_input(collections):
            color_unregistered_pitches = False
        self._validate_voice_name(voice_name)
        self._apply_state_manifest(state_manifest)
        specifiers = list(self.specifiers or []) + list(specifiers)
        if all(isinstance(_, abjad.Rest) for _ in collections):
            tuplet = abjad.Tuplet((1, 1), collections, hide=True)
            selections = [abjad.select(tuplet)]
            specifiers = [
                _ for _ in specifiers
                if not isinstance(_, PitchFirstRhythmCommand)
                ]
        else:
            collections = self._coerce_collections(collections)
            collections, specifiers = self._apply_pitch_specifiers(
                collections,
                specifiers,
                )
            collections, specifiers = self._apply_spacing_specifiers(
                collections,
                specifiers,
                )
            selections, specifiers = self._call_rhythm_commands(
                collections,
                specifiers,
                counts=counts,
                division_masks=division_masks,
                logical_tie_masks=logical_tie_masks,
                talea_denominator=talea_denominator,
                thread=thread,
                time_treatments=time_treatments,
                tuplet_denominator=tuplet_denominator,
                tuplet_force_fraction=tuplet_force_fraction,
                )
        anchor, specifiers = self._get_anchor_specifier(specifiers)
        container = abjad.Container(selections)
        self._color_unregistered_pitches_(
            container,
            color_unregistered_pitches=color_unregistered_pitches,
            )
        specifiers = self._call_tie_commands(selections, specifiers)
        specifiers = self._call_cluster_commands(selections, specifiers)
        specifiers = self._call_nesting_commands(selections, specifiers)
        specifiers = self._call_register_commands(selections, specifiers)
        imbricated_selections, specifiers = self._call_imbrication_commands(
            container,
            specifiers,
            )
        result = self._call_color_commands(selections, specifiers)
        specifiers, color_selector, color_selector_result = result
        self._call_remaining_commands(selections, specifiers)
        self._label_figure_name_(container, figure_name, figure_index)
        self._annotate_collection_list(container, collections)
        self._annotate_deployment(
            container,
            is_foreshadow=is_foreshadow,
            is_recollection=is_recollection,
            )
        self._annotate_repeat_pitches(container)
        self._extend_beam_(container, extend_beam)
        self._check_wellformedness(container)
        state_manifest = self._make_state_manifest()
        selection = abjad.select([container])
        time_signature = self._make_time_signature(
            selection,
            denominator=denominator,
            )
        selections = {voice_name: selection}
        selections.update(imbricated_selections)
        for value in selections.values():
            assert isinstance(value, abjad.Selection), repr(value)
        return MusicContribution(
            anchor=anchor,
            color_selector=color_selector,
            color_selector_result=color_selector_result,
            figure_name=figure_name,
            hide_time_signature=hide_time_signature,
            selections=selections,
            state_manifest=state_manifest,
            time_signature=time_signature,
            )

    ### PRIVATE METHODS ###

    @staticmethod
    def _all_are_selections(argument):
        prototype = abjad.Selection
        return all(isinstance(_, prototype) for _ in argument)

    @staticmethod
    def _annotate_collection_list(container, collections):
        for leaf in abjad.iterate(container).leaves():
            collections_ = copy.deepcopy(collections)
            abjad.attach(collections_, leaf, tag=None)

    def _annotate_deployment(
        self,
        argument,
        is_foreshadow=False,
        is_incomplete=False,
        is_recollection=False,
        ):
        if not is_foreshadow and not is_recollection and not is_incomplete:
            return
        for leaf in abjad.iterate(argument).leaves():
            if is_foreshadow:
                abjad.attach(abjad.tags.FORESHADOW, leaf)
            if is_incomplete:
                abjad.attach(abjad.tags.INCOMPLETE, leaf)
            if is_recollection:
                abjad.attach(abjad.tags.RECOLLECTION, leaf)

    def _annotate_repeat_pitches(self, container):
        if not self.allow_repeats:
            return
        for leaf in abjad.iterate(container).leaves(pitched=True):
            abjad.attach(abjad.tags.ALLOW_REPEAT_PITCH, leaf)

    def _apply_pitch_specifiers(self, collections, specifiers):
        prototype = (pitchclasses.CollectionList, list, abjad.Sequence)
        assert isinstance(collections, prototype), repr(collections)
        specifiers_ = []
        for specifier in specifiers:
            if isinstance(specifier, PitchSpecifier):
                collections = specifier(collections)
            else:
                specifiers_.append(specifier)
        return collections, specifiers_

    def _apply_spacing_specifiers(self, collections, specifiers):
        prototype = (pitchclasses.CollectionList, list, abjad.Sequence)
        assert isinstance(collections, prototype), repr(collections)
        specifiers_ = []
        prototype = (
            pitchclasses.ArpeggiationSpacingSpecifier,
            pitchclasses.ChordalSpacingSpecifier,
            )
        for specifier in specifiers:
            if isinstance(specifier, prototype):
                collections = specifier(collections)
            else:
                specifiers_.append(specifier)
        return collections, specifiers_

    def _apply_state_manifest(self, state_manifest=None):
        state_manifest = state_manifest or {}
        assert isinstance(state_manifest, dict), repr(state_manifest)
        for key in state_manifest:
            value = state_manifest[key]
            setattr(self, key, value)

    def _call_cluster_commands(self, selections, specifiers):
        assert self._all_are_selections(selections), repr(selections)
        specifiers_ = []
        for specifier in specifiers:
            if isinstance(specifier, pitchcommands.ClusterCommand):
                specifier(selections)
            else:
                specifiers_.append(specifier)
        return specifiers_

    def _call_color_commands(self, selections, specifiers):
        assert self._all_are_selections(selections), repr(selections)
        specifiers_ = []
        color_selector, color_selector_result = None, None
        for specifier in specifiers:
            if isinstance(specifier, commands.ColorCommand):
                color_selector = specifier.selector
                color_selector_result = specifier(selections)
            else:
                specifiers_.append(specifier)
        return specifiers_, color_selector, color_selector_result

    def _call_imbrication_commands(self, container, specifiers):
        specifiers_ = []
        imbricated_selections = {}
        for specifier in specifiers:
            if isinstance(specifier, ImbricationCommand):
                imbricated_selection = specifier(container)
                imbricated_selections.update(imbricated_selection)
            else:
                specifiers_.append(specifier)
        return imbricated_selections, specifiers_

    def _call_nesting_commands(self, selections, specifiers):
        assert self._all_are_selections(selections), repr(selections)
        specifiers_ = []
        for specifier in specifiers:
            if isinstance(specifier, NestingCommand):
                specifier(selections)
            else:
                specifiers_.append(specifier)
        return specifiers_

    def _call_register_commands(self, selections, specifiers):
        assert self._all_are_selections(selections), repr(selections)
        specifiers_ = []
        prototype = (
            pitchcommands.RegisterCommand,
            pitchcommands.RegisterInterpolationCommand,
            pitchcommands.RegisterToOctaveCommand,
            )
        for specifier in specifiers:
            if isinstance(specifier, prototype):
                specifier(selections)
            else:
                specifiers_.append(specifier)
        return specifiers_

    def _call_remaining_commands(self, selections, specifiers):
        assert self._all_are_selections(selections), repr(selections)
        for specifier in specifiers:
            if not isinstance(specifier, rmakers.BeamSpecifier):
                assert isinstance(specifier, scoping.Command), format(specifier)
            specifier(selections)

    def _call_rhythm_commands(
        self,
        collections,
        specifiers,
        counts=None,
        division_masks=None,
        logical_tie_masks=None,
        talea_denominator=None,
        thread=None,
        time_treatments=None,
        tuplet_denominator=None,
        tuplet_force_fraction=None,
        ):
        selections = len(collections) * [None]
        rhythm_commands, rest_affix_specifiers, specifiers_ = [], [], []
        for specifier in specifiers:
            if isinstance(specifier, PitchFirstRhythmCommand):
                rhythm_commands.append(specifier)
            elif isinstance(specifier, RestAffixSpecifier):
                rest_affix_specifiers.append(specifier)
            else:
                specifiers_.append(specifier)
        if not rhythm_commands:
            rhythm_commands.append(self._make_default_rhythm_command())
        if not rest_affix_specifiers:
            rest_affix_specifier = None
        elif len(rest_affix_specifiers) == 1:
            rest_affix_specifier = rest_affix_specifiers[0]
        else:
            message = f'max 1 rest affix specifier: {rest_affix_specifiers!r}.'
            raise Exception(message)
        thread = thread or self.thread
        for rhythm_command in rhythm_commands:
            rhythm_command(
                collections=collections,
                selections=selections,
                division_masks=division_masks,
                logical_tie_masks=logical_tie_masks,
                rest_affix_specifier=rest_affix_specifier,
                talea_counts=counts,
                talea_denominator=talea_denominator,
                thread=thread,
                time_treatments=time_treatments,
                tuplet_denominator=tuplet_denominator,
                tuplet_force_fraction=tuplet_force_fraction,
                )
        return selections, specifiers_

    def _call_tie_commands(self, selections, specifiers):
        assert self._all_are_selections(selections), repr(selections)
        specifiers_ = []
        for specifier in specifiers:
            if (isinstance(specifier, spannercommands.SpannerCommand) and
                isinstance(specifier.spanner, abjad.Tie)):
                specifier(selections)
            else:
                specifiers_.append(specifier)
        return specifiers_

    @staticmethod
    def _check_wellformedness(selections):
        for component in abjad.iterate(selections).components():
            inspector = abjad.inspect(component)
            if not inspector.is_wellformed():
                report = inspector.tabulate_wellformedness()
                report = repr(component) + '\n' + report
                raise Exception(report)

    @staticmethod
    def _coerce_collections(collections):
        prototype = (abjad.Segment, abjad.Set)
        if isinstance(collections, prototype):
            return pitchclasses.CollectionList(collections=[collections])
        item_class = abjad.NumberedPitch
        for collection in collections:
            for item in collection:
                if isinstance(item, str):
                    item_class = abjad.NamedPitch
                    break
        return pitchclasses.CollectionList(
            collections=collections,
            item_class=item_class,
            )

    def _color_unregistered_pitches_(
        self,
        argument,
        color_unregistered_pitches=None,
        ):
        if color_unregistered_pitches is None:
            color_unregistered_pitches = self.color_unregistered_pitches
        if not color_unregistered_pitches:
            return
        for pleaf in abjad.iterate(argument).leaves(pitched=True):
            abjad.attach(abjad.tags.NOT_YET_REGISTERED, pleaf, tag='')

    @staticmethod
    def _exactly_double(selections):
        length = len(selections)
        if length % 2 == 1:
            return False
        half_length = int(length / 2)
        for index in range(half_length):
            first_selection = selections[index]
            index_ = index + half_length
            second_selection = selections[index_]
            first_format = format(first_selection, 'lilypond')
            second_format = format(second_selection, 'lilypond')
            if not first_format == second_format:
                return False
        return True

    def _extend_beam_(self, selections, extend_beam):
        if not extend_beam:
            return
        leaves = list(abjad.iterate(selections).leaves())
        last_leaf = leaves[-1]
        abjad.attach(abjad.tags.RIGHT_BROKEN_BEAM, last_leaf)

    @staticmethod
    def _get_anchor_specifier(specifiers):
        anchor_specifiers, specifiers_ = [], []
        for specifier in specifiers:
            if isinstance(specifier, AnchorSpecifier):
                anchor_specifiers.append(specifier)
            else:
                specifiers_.append(specifier)
        if not anchor_specifiers:
            anchor_specifier = None
        elif len(anchor_specifiers) == 1:
            anchor_specifier = anchor_specifiers[0]
        else:
            raise Exception(f'max 1 anchor specifier: {anchor_specifiers!r}.')
        return anchor_specifier, specifiers_

    def _get_storage_format_specification(self):
        agent = abjad.StorageFormatManager(self)
        keyword_argument_names = agent.signature_keyword_names
        positional_argument_values = self.specifiers
        return abjad.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            positional_argument_values=positional_argument_values,
            )

    def _is_pitch_input(self, collections):
        prototype = (abjad.PitchSegment, abjad.PitchSet)
        if isinstance(collections, prototype):
            return True
        try:
            if isinstance(collections[0], prototype):
                return True
        except (IndexError, TypeError):
            pass
        return False

    @staticmethod
    def _label_figure_name_(container, figure_name, figure_index):
        if figure_name is None:
            return
        figure_name = str(figure_name)
        original_figure_name = figure_name
        parts = figure_name.split('_')
        if len(parts) == 1:
            body = parts[0]
            figure_name = abjad.Markup(body)
        elif len(parts) == 2:
            body, subscript = parts
            figure_name = abjad.Markup.concat([
                abjad.Markup(body),
                abjad.Markup(subscript).sub(),
                ])
        else:
            raise Exception(f'unrecognized figure name: {figure_name!r}.')
        figure_index = f' ({figure_index})'
        figure_index = abjad.Markup(figure_index).fontsize(-2).raise_(0.25)
        figure_name_markup = abjad.Markup.concat([
            '[',
            figure_name,
            abjad.Markup.hspace(1),
            figure_index,
            ']',
            ])
        figure_name_markup = figure_name_markup.fontsize(2)
        figure_name_markup = abjad.Markup(
            figure_name_markup, direction=abjad.Up)
        annotation = f'figure name: {original_figure_name}'
        figure_name_markup._annotation = annotation
        leaves = list(abjad.iterate(container).leaves())
        abjad.attach(
            figure_name_markup,
            leaves[0],
            tag=abjad.tags.FIGURE_NAME_MARKUP,
            )

    @staticmethod
    def _make_default_rhythm_command():
        return PitchFirstRhythmCommand(
            rhythm_maker=PitchFirstRhythmMaker(),
            )

    def _make_state_manifest(self):
        state_manifest = {}
        for name in self._state_variables:
            value = getattr(self, name)
            state_manifest[name] = value
        return state_manifest

    def _make_time_signature(self, selection, denominator=None):
        if denominator is None:
            denominator = self.denominator
        duration = abjad.inspect(selection).duration()
        if denominator is not None:
            duration = duration.with_denominator(denominator)
        time_signature = abjad.TimeSignature(duration)
        return time_signature

    @staticmethod
    def _to_pitch_item_class(item_class):
        if item_class in (abjad.NamedPitch, abjad.NumberedPitch):
            return item_class
        elif item_class is abjad.NamedPitchClass:
            return abjad.NamedPitch
        elif item_class is abjad.NumberedPitchClass:
            return abjad.NumberedPitch
        else:
            raise TypeError(item_class)

    def _validate_voice_name(self, voice_name):
        if not isinstance(voice_name, str):
            raise TypeError(f'voice name must be string: {voice_name!r}.')
        if self.voice_names and voice_name not in self.voice_names:
            raise ValueError(f'unknown voice name: {voice_name!r}.')

    ### PUBLIC PROPERTIES ###

    @property
    def allow_repeats(self):
        """
        Is true when music-maker allows repeat pitches.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._allow_repeats

    @property
    def color_unregistered_pitches(self):
        """
        Is true when music-maker colors unregistered pitches.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._color_unregistered_pitches

    @property
    def denominator(self):
        r"""
        Gets denominator.

        ..  container:: example

            No denominator by default:

            >>> music_maker = baca.MusicMaker()

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23, 17],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'16
                                [
                                d'16
                                bf'16
                                fs''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                e''16
                                [
                                ef''16
                                b''16
                                f''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                g''16
                                [
                                cs''16
                                a'16
                                af'16
                                ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Denominator supplied at configuration time:

            >>> music_maker = baca.MusicMaker(
            ...     denominator=16,
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23, 17],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(
            ...     contribution,
            ...     time_signatures=[contribution.time_signature],
            ...     )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'16
                                [
                                d'16
                                bf'16
                                fs''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                e''16
                                [
                                ef''16
                                b''16
                                f''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                g''16
                                [
                                cs''16
                                a'16
                                af'16
                                ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Denominator supplied at call time:

            >>> music_maker = baca.MusicMaker()

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23, 17],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     denominator=8,
            ...     )
            >>> lilypond_file = music_maker.show(
            ...     contribution,
            ...     time_signatures=[contribution.time_signature],
            ...     )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'16
                                [
                                d'16
                                bf'16
                                fs''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                e''16
                                [
                                ef''16
                                b''16
                                f''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                g''16
                                [
                                cs''16
                                a'16
                                af'16
                                ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Denominator supplied at call time overrides denominator supplied at
            configuration time:

            >>> music_maker = baca.MusicMaker(
            ...     denominator=16,
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23, 17],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     denominator=8,
            ...     )
            >>> lilypond_file = music_maker.show(
            ...     contribution,
            ...     time_signatures=[contribution.time_signature],
            ...     )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'16
                                [
                                d'16
                                bf'16
                                fs''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                e''16
                                [
                                ef''16
                                b''16
                                f''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                g''16
                                [
                                cs''16
                                a'16
                                af'16
                                ]
                            }
                        }
                    }
                >>

        Defaults to none.

        Set to positive integer or none.

        Returns positive integer or none.
        """
        return self._denominator

    @property
    def specifiers(self):
        r"""
        Gets specifiers.

        ..  container:: example

            Register specifier transposes to octave rooted on F#3:

            >>> music_maker = baca.MusicMaker(baca.register(-6))

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'16
                                [
                                d'16
                                bf16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                fs16
                                [
                                e'16
                                ef'16
                                af16
                                g16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a16
                            }
                        }
                    }
                >>

        ..  container:: example

            Ocatve-transposes to a target interpolated from C4 up to C5:

            >>> music_maker = baca.MusicMaker(baca.register(0, 12))

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                fs'16
                                [
                                e''16
                                ef''16
                                af'16
                                g''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a''16
                            }
                        }
                    }
                >>

        ..  container:: example

            Hairpin specifier selects all leaves:

            >>> music_maker = baca.MusicMaker(
            ...     baca.hairpin('p < f'),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 4.5
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4.5
                }
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'16
                                \p                                                                       %! PIC_1
                                \<                                                                       %! PIC_1
                                [
                                d'16
                                bf'16
                                fs''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                e''16
                                [
                                ef''16
                                b''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                g''16
                                [
                                cs''16
                                a'16
                                af'16
                                \f                                                                       %! PIC_2
                                ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Maps hairpin to each run:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10, 18], [15, 23], [19, 13, 9, 8]],
            ...     baca.map(
            ...         baca.runs(),
            ...         baca.hairpin('p < f'),
            ...         ),
            ...     baca.RestAffixSpecifier(
            ...         pattern=abjad.Pattern(
            ...             indices=[0, -1],
            ...             inverted=True,
            ...             ),
            ...         prefix=[1],
            ...         ),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 4.5
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4.5
                }
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'16
                                \p                                                                       %! PIC_1
                                \<                                                                       %! PIC_1
                                [
                                d'16
                                bf'16
                                fs''16
                                \f                                                                       %! PIC_2
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                r16
                                ef''16
                                \p                                                                       %! PIC_1
                                \<                                                                       %! PIC_1
                                [
                                b''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                g''16
                                [
                                cs''16
                                a'16
                                af'16
                                \f                                                                       %! PIC_2
                                ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Hairpin specifiers select notes of first and last tuplet:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10, 18], [16, 15, 23], [19, 13, 9, 8]],
            ...     baca.map(
            ...         baca.tuplet(0),
            ...         baca.hairpin('p < f'),
            ...         ),
            ...     baca.map(
            ...         baca.tuplet(-1),
            ...         baca.hairpin('f > p'),
            ...         ),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 4.5
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4.5
                }
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'16
                                \p                                                                       %! PIC_1
                                \<                                                                       %! PIC_1
                                [
                                d'16
                                bf'16
                                fs''16
                                \f                                                                       %! PIC_2
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                e''16
                                [
                                ef''16
                                b''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                g''16
                                \f                                                                       %! PIC_1
                                \>                                                                       %! PIC_1
                                [
                                cs''16
                                a'16
                                af'16
                                \p                                                                       %! PIC_2
                                ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Hairpin specifiers treat first two tuplets and then the rest:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10, 18], [16, 15, 23], [19, 13, 9, 8]],
            ...     baca.map(
            ...         baca.tuplets()[:2],
            ...         baca.hairpin('p < f'),
            ...         ),
            ...     baca.map(
            ...         baca.tuplet(-1),
            ...         baca.hairpin('f > p'),
            ...         ),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 6
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #6
                }
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'16
                                \p                                                                       %! PIC_1
                                \<                                                                       %! PIC_1
                                [
                                d'16
                                bf'16
                                fs''16
                                \f                                                                       %! PIC_2
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                e''16
                                \p                                                                       %! PIC_1
                                \<                                                                       %! PIC_1
                                [
                                ef''16
                                b''16
                                \f                                                                       %! PIC_2
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                g''16
                                \f                                                                       %! PIC_1
                                \>                                                                       %! PIC_1
                                [
                                cs''16
                                a'16
                                af'16
                                \p                                                                       %! PIC_2
                                ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Spanner specifier selects all leaves by default:

            >>> music_maker = baca.MusicMaker(
            ...     baca.slur(),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).stem.direction = Down
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override Stem.direction = #down
                }
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'16
                                [
                                (                                                                        %! SC
                                d'16
                                bf'16
                                fs''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                e''16
                                [
                                ef''16
                                b''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                g''16
                                [
                                cs''16
                                a'16
                                af'16
                                ]
                                )                                                                        %! SC
                            }
                        }
                    }
                >>

        ..  container:: example

            Slur specifier selects leaves in each tuplet:

            >>> music_maker = baca.MusicMaker(
            ...     baca.map(
            ...         baca.tuplets(),
            ...         baca.slur(),
            ...         ),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).stem.direction = Down
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override Stem.direction = #down
                }
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'16
                                [
                                (                                                                        %! SC
                                d'16
                                bf'16
                                fs''16
                                ]
                                )                                                                        %! SC
                            }
                            \scaleDurations #'(1 . 1) {
                                e''16
                                [
                                (                                                                        %! SC
                                ef''16
                                b''16
                                ]
                                )                                                                        %! SC
                            }
                            \scaleDurations #'(1 . 1) {
                                g''16
                                [
                                (                                                                        %! SC
                                cs''16
                                a'16
                                af'16
                                ]
                                )                                                                        %! SC
                            }
                        }
                    }
                >>

        ..  container:: example

            Slur specifier selects first two pitched leaves in each tuplet:

            >>> getter = baca.pleaves()[:2]
            >>> selector = baca.tuplets().map(getter)
            >>> music_maker = baca.MusicMaker(
            ...     baca.map(
            ...         selector,
            ...         baca.slur(),
            ...         ),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).stem.direction = Down
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override Stem.direction = #down
                }
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'16
                                [
                                (                                                                        %! SC
                                d'16
                                )                                                                        %! SC
                                bf'16
                                fs''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                e''16
                                [
                                (                                                                        %! SC
                                ef''16
                                )                                                                        %! SC
                                b''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                g''16
                                [
                                (                                                                        %! SC
                                cs''16
                                )                                                                        %! SC
                                a'16
                                af'16
                                ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Slur specifier selects last two pitched leaves in each tuplet:

            >>> getter = baca.pleaves()[-2:]
            >>> selector = baca.tuplets().map(getter)
            >>> music_maker = baca.MusicMaker(
            ...     baca.map(
            ...         selector,
            ...         baca.slur(),
            ...         ),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).stem.direction = Down
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override Stem.direction = #down
                }
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'16
                                [
                                d'16
                                bf'16
                                (                                                                        %! SC
                                fs''16
                                ]
                                )                                                                        %! SC
                            }
                            \scaleDurations #'(1 . 1) {
                                e''16
                                [
                                ef''16
                                (                                                                        %! SC
                                b''16
                                ]
                                )                                                                        %! SC
                            }
                            \scaleDurations #'(1 . 1) {
                                g''16
                                [
                                cs''16
                                a'16
                                (                                                                        %! SC
                                af'16
                                ]
                                )                                                                        %! SC
                            }
                        }
                    }
                >>

        ..  container:: example

            Beam specifier beams divisions together:

            >>> music_maker = baca.MusicMaker(
            ...     rmakers.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).beam.positions = (-6, -6)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override Beam.positions = #'(-6 . -6)
                }
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                \set stemLeftBeamCount = 0
                                \set stemRightBeamCount = 2
                                c'16
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                fs''16
                            }
                            \scaleDurations #'(1 . 1) {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                e''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                ef''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                b''16
                            }
                            \scaleDurations #'(1 . 1) {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                g''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                cs''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                a'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                af'16
                                ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Beam specifier beams nothing:

            >>> music_maker = baca.MusicMaker(
            ...     rmakers.BeamSpecifier(
            ...         beam_each_division=False,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'16
                                d'16
                                bf'16
                                fs''16
                            }
                            \scaleDurations #'(1 . 1) {
                                e''16
                                ef''16
                                b''16
                            }
                            \scaleDurations #'(1 . 1) {
                                g''16
                                cs''16
                                a'16
                                af'16
                            }
                        }
                    }
                >>

        ..  container:: example

            Nesting specifier augments one sixteenth:

            >>> music_maker = baca.MusicMaker(
            ...     baca.NestingCommand(
            ...         time_treatments=['+1/16'],
            ...         ),
            ...     rmakers.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).beam.positions = (-5.5, -5.5)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override Beam.positions = #'(-5.5 . -5.5)
                }
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 12/11 {
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    fs''16
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    e''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    ef''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    b''16
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    g''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    cs''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 0
                                    af'16
                                    ]
                                }
                            }
                        }
                    }
                >>

        ..  container:: example

            Nesting specifier augments first two collections one sixteenth:

            >>> music_maker = baca.MusicMaker(
            ...     baca.NestingCommand(
            ...         lmr_specifier=baca.LMRSpecifier(
            ...             left_length=2,
            ...             ),
            ...         time_treatments=['+1/16', None],
            ...         ),
            ...     rmakers.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).beam.positions = (-5.5, -5.5)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override Beam.positions = #'(-5.5 . -5.5)
                }
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 8/7 {
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 0
                                    \set stemRightBeamCount = 2
                                    c'16
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    fs''16
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    e''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    ef''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    b''16
                                }
                            }
                            \scaleDurations #'(1 . 1) {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                g''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                cs''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                a'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                af'16
                                ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Sixteenths followed by eighths:

            >>> music_maker = baca.MusicMaker(
            ...     baca.PitchFirstRhythmCommand(
            ...         rhythm_maker=baca.PitchFirstRhythmMaker(
            ...             talea=rmakers.Talea(
            ...                 counts=[1],
            ...                 denominator=8,
            ...                 ),
            ...             ),
            ...         ),
            ...     baca.PitchFirstRhythmCommand(
            ...         pattern=abjad.index_first(1),
            ...         rhythm_maker=baca.PitchFirstRhythmMaker(
            ...             talea=rmakers.Talea(
            ...                 counts=[1],
            ...                 denominator=16,
            ...                 ),
            ...             ),
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                fs''8
                                [
                                e''8
                                ef''8
                                af''8
                                g''8
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a'8
                            }
                        }
                    }
                >>

        ..  container:: example

            Sixteenths surrounding dotted eighths:

            >>> music_maker = baca.MusicMaker(
            ...     baca.PitchFirstRhythmCommand(
            ...         rhythm_maker=baca.PitchFirstRhythmMaker(
            ...             talea=rmakers.Talea(
            ...                 counts=[3],
            ...                 denominator=16,
            ...                 ),
            ...             ),
            ...         ),
            ...     baca.PitchFirstRhythmCommand(
            ...         pattern=abjad.Pattern(indices=[0, -1]),
            ...         rhythm_maker=baca.PitchFirstRhythmMaker(
            ...             talea=rmakers.Talea(
            ...                 counts=[1],
            ...                 denominator=16,
            ...                 ),
            ...             ),
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                fs''8.
                                [
                                e''8.
                                ef''8.
                                af''8.
                                g''8.
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a'16
                            }
                        }
                    }
                >>

        ..  container:: example

            Sixteenths surrounding argumented dotted eighths:

            >>> music_maker = baca.MusicMaker(
            ...     baca.PitchFirstRhythmCommand(
            ...         rhythm_maker=baca.PitchFirstRhythmMaker(
            ...             talea=rmakers.Talea(
            ...                 counts=[3],
            ...                 denominator=16,
            ...                 ),
            ...             time_treatments=[1],
            ...             ),
            ...         ),
            ...     baca.PitchFirstRhythmCommand(
            ...         pattern=abjad.Pattern(indices=[0, -1]),
            ...         rhythm_maker=baca.PitchFirstRhythmMaker(
            ...             talea=rmakers.Talea(
            ...                 counts=[1],
            ...                 denominator=16,
            ...                 ),
            ...             ),
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 16/15 {
                                fs''8.
                                [
                                e''8.
                                ef''8.
                                af''8.
                                g''8.
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a'16
                            }
                        }
                    }
                >>

        ..  container:: example

            Augmented sixteenths surrounding dotted eighths:

            >>> music_maker = baca.MusicMaker(
            ...     baca.PitchFirstRhythmCommand(
            ...         rhythm_maker=baca.PitchFirstRhythmMaker(
            ...             talea=rmakers.Talea(
            ...                 counts=[3],
            ...                 denominator=16,
            ...                 ),
            ...             ),
            ...         ),
            ...     baca.PitchFirstRhythmCommand(
            ...         pattern=abjad.Pattern(indices=[0, -1]),
            ...         rhythm_maker=baca.PitchFirstRhythmMaker(
            ...             talea=rmakers.Talea(
            ...                 counts=[1],
            ...                 denominator=16,
            ...                 ),
            ...             time_treatments=[1],
            ...             ),
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 4/3 {
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                fs''8.
                                [
                                e''8.
                                ef''8.
                                af''8.
                                g''8.
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a'16
                            }
                        }
                    }
                >>

        ..  container:: example

            Diminished sixteenths surrounding dotted eighths:

            >>> music_maker = baca.MusicMaker(
            ...     baca.PitchFirstRhythmCommand(
            ...         rhythm_maker=baca.PitchFirstRhythmMaker(
            ...             talea=rmakers.Talea(
            ...                 counts=[3],
            ...                 denominator=16,
            ...                 ),
            ...             ),
            ...         ),
            ...     baca.PitchFirstRhythmCommand(
            ...         pattern=abjad.Pattern(indices=[0, -1]),
            ...         rhythm_maker=baca.PitchFirstRhythmMaker(
            ...             talea=rmakers.Talea(
            ...                 counts=[1],
            ...                 denominator=16,
            ...                 ),
            ...             time_treatments=[-1],
            ...             ),
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \times 2/3 {
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                fs''8.
                                [
                                e''8.
                                ef''8.
                                af''8.
                                g''8.
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a'16
                            }
                        }
                    }
                >>

        Defaults to none.

        Set to specifiers or none.

        Returns specifiers or none.
        """
        return self._specifiers

    @property
    def thread(self):
        r"""
        Is true when music-maker threads rhythm-maker over collections.

        ..  container:: example

            Does not thread rhythm-maker over collections:

            >>> music_maker = baca.MusicMaker()

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     counts=[1, 2, 3],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'16
                                [
                                d'8
                                bf'8.
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                fs''16
                                [
                                e''8
                                ef''8.
                                af''16
                                g''8
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a'16
                            }
                        }
                    }
                >>

            Does thread rhythm-maker over collections:

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     counts=[1, 2, 3],
            ...     thread=True,
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'16
                                [
                                d'8
                                bf'8.
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                fs''16
                                [
                                e''8
                                ef''8.
                                af''16
                                g''8
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a'8.
                            }
                        }
                    }
                >>

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        """
        return self._thread

    @property
    def voice_names(self):
        """
        Gets voice names.

        Used to check call-time voice names.

        Defaults to none.

        Set to list of strings or none.

        Returns list or strings or none.
        """
        if self._voice_names:
            return list(self._voice_names)

    ### PUBLIC METHODS ###

    @staticmethod
    def show(music_contribution, time_signatures=None):
        """
        Makes rhythm-maker-style LilyPond file for documentation examples.

        Returns LilyPond file.
        """
        assert isinstance(music_contribution, MusicContribution)
        return abjad.LilyPondFile.rhythm(
            music_contribution.selections,
            time_signatures=time_signatures,
            attach_lilypond_voice_commands=True,
            )

class NestingCommand(scoping.Command):
    r"""
    Nesting command.

    >>> from abjadext import rmakers

    ..  container:: example

        Augments one sixteenth:

        >>> music_maker = baca.MusicMaker(
        ...     baca.NestingCommand(
        ...         time_treatments=['+1/16'],
        ...         ),
        ...     rmakers.BeamSpecifier(
        ...         beam_divisions_together=True,
        ...         ),
        ...     )

        >>> collections = [
        ...     [0, 2, 10, 18],
        ...     [16, 15, 23],
        ...     [19, 13, 9, 8],
        ...     ]
        >>> contribution = music_maker('Voice 1', collections)
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 12/11 {
                            \scaleDurations #'(1 . 1) {
                                \set stemLeftBeamCount = 0
                                \set stemRightBeamCount = 2
                                c'16
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                fs''16
                            }
                            \scaleDurations #'(1 . 1) {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                e''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                ef''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                b''16
                            }
                            \scaleDurations #'(1 . 1) {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                g''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                cs''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                a'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 0
                                af'16
                                ]
                            }
                        }
                    }
                }
            >>

    ..  container:: example

        Calltime nesting command preserves beam subdivisions and works with
        extend beam:

            >>> music_maker = baca.MusicMaker(
            ...     rmakers.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         ),
            ...     )

        >>> containers, time_signatures = [], []
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10, 18], [16, 15, 23]],
        ...     baca.NestingCommand(
        ...         time_treatments=['+1/16'],
        ...         ),
        ...     extend_beam=True,
        ...     )
        >>> containers.extend(contribution['Voice 1'])
        >>> time_signatures.append(contribution.time_signature)
        >>> contribution = music_maker('Voice 1', [[19, 13, 9, 8]])
        >>> containers.extend(contribution['Voice 1'])
        >>> time_signatures.append(contribution.time_signature)
        >>> selection = abjad.select(containers)

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.HorizontalSpacingSpecifier(
        ...         minimum_duration=abjad.Duration(1, 24),
        ...         ),
        ...     time_signatures=time_signatures,
        ...     )
        >>> maker(
        ...     'MusicVoice',
        ...     baca.RhythmCommand(
        ...         rhythm_maker=selection,
        ...         ),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> staff = lilypond_file[abjad.Staff]
        >>> abjad.override(staff).beam.positions = (-5.5, -5.5)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #24                                             %! HSS1:SPACING
                        \time 1/2                                                                    %! SET_STATUS_TAG:EXPLICIT_TIME_SIGNATURE:MAKE_GLOBAL_SKIPS_2
                        \baca_time_signature_color "blue"                                            %! ATTACH_COLOR_LITERAL_2:EXPLICIT_TIME_SIGNATURE_COLOR:MAKE_GLOBAL_SKIPS_2
                        s1 * 1/2                                                                     %! MAKE_GLOBAL_SKIPS_1
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! COMMENT_MEASURE_NUMBERS
                        \baca_new_spacing_section #1 #24                                             %! HSS1:SPACING
                        \time 1/4                                                                    %! SET_STATUS_TAG:EXPLICIT_TIME_SIGNATURE:MAKE_GLOBAL_SKIPS_2
                        \baca_time_signature_color "blue"                                            %! ATTACH_COLOR_LITERAL_2:EXPLICIT_TIME_SIGNATURE_COLOR:MAKE_GLOBAL_SKIPS_2
                        s1 * 1/4                                                                     %! MAKE_GLOBAL_SKIPS_1
                        \baca_bar_line_visible                                                       %! ATTACH_FINAL_BAR_LINE
                        \bar "|"                                                                     %! ATTACH_FINAL_BAR_LINE
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    \with
                    {
                        \override Beam.positions = #'(-5.5 . -5.5)
                    }
                    {
                        \context Voice = "MusicVoice"
                        {
                            {
                                \tweak text #tuplet-number::calc-fraction-text
                                \times 8/7 {
                                    \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                        % [MusicVoice measure 1]                                     %! COMMENT_MEASURE_NUMBERS
                                        \set stemLeftBeamCount = 0                                   %! SM_35
                                        \set stemRightBeamCount = 2                                  %! SM_35
                                        c'16
                                        [                                                            %! SM_35
            <BLANKLINE>
                                        \set stemLeftBeamCount = 2                                   %! SM_35
                                        \set stemRightBeamCount = 2                                  %! SM_35
                                        d'16
            <BLANKLINE>
                                        \set stemLeftBeamCount = 2                                   %! SM_35
                                        \set stemRightBeamCount = 2                                  %! SM_35
                                        bf'!16
            <BLANKLINE>
                                        \set stemLeftBeamCount = 2                                   %! SM_35
                                        \set stemRightBeamCount = 1                                  %! SM_35
                                        fs''!16
                                    }
                                    \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                        \set stemLeftBeamCount = 1                                   %! SM_35
                                        \set stemRightBeamCount = 2                                  %! SM_35
                                        e''16
            <BLANKLINE>
                                        \set stemLeftBeamCount = 2                                   %! SM_35
                                        \set stemRightBeamCount = 2                                  %! SM_35
                                        ef''!16
            <BLANKLINE>
                                        \set stemLeftBeamCount = 2                                   %! SM_35
                                        \set stemRightBeamCount = 1                                  %! SM_35
                                        b''16
                                    }
                                }
                            }
                            {
                                \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                    % [MusicVoice measure 2]                                         %! COMMENT_MEASURE_NUMBERS
                                    \set stemLeftBeamCount = 1                                       %! SM_35
                                    \set stemRightBeamCount = 2                                      %! SM_35
                                    g''16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2                                       %! SM_35
                                    \set stemRightBeamCount = 2                                      %! SM_35
                                    cs''!16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2                                       %! SM_35
                                    \set stemRightBeamCount = 2                                      %! SM_35
                                    a'16
            <BLANKLINE>
                                    \set stemLeftBeamCount = 2                                       %! SM_35
                                    \set stemRightBeamCount = 0                                      %! SM_35
                                    af'!16
                                    ]                                                                %! SM_35
            <BLANKLINE>
                                }
                            }
                        }
                    }
                >>
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_lmr_specifier',
        '_time_treatments',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        lmr_specifier=None,
        time_treatments=None,
        ):
        if lmr_specifier is not None:
            prototype = LMRSpecifier
            assert isinstance(lmr_specifier, prototype)
        self._lmr_specifier = lmr_specifier
        if time_treatments is not None:
            assert isinstance(time_treatments, (list, tuple))
            is_time_treatment = PitchFirstRhythmMaker._is_time_treatment
            for time_treatment in time_treatments:
                assert is_time_treatment(time_treatment), repr(time_treatment)
        self._time_treatments = time_treatments

    ### SPECIAL METHODS ###

    def __call__(self, selections=None):
        r"""
        Calls command on ``selections``.

        ..  container:: example

            With rest affixes:

            >>> music_maker = baca.MusicMaker(
            ...     baca.NestingCommand(time_treatments=['+1/16']),
            ...     baca.RestAffixSpecifier(
            ...         prefix=[2],
            ...         suffix=[3],
            ...         ),
            ...     rmakers.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18],
            ...     [16, 15, 23],
            ...     [19, 13, 9, 8],
            ...     ]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 17/16 {
                                \scaleDurations #'(1 . 1) {
                                    r8
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    c'16
                                    [
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    d'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    bf'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    fs''16
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    e''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    ef''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 1
                                    b''16
                                }
                                \scaleDurations #'(1 . 1) {
                                    \set stemLeftBeamCount = 1
                                    \set stemRightBeamCount = 2
                                    g''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    cs''16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    a'16
                                    \set stemLeftBeamCount = 2
                                    \set stemRightBeamCount = 2
                                    af'16
                                    ]
                                    r8.
                                }
                            }
                        }
                    }
                >>

        Returns new selections.
        """
        if selections is None:
            return
        time_treatments = self._get_time_treatments()
        if time_treatments is None:
            return selections
        tuplets = []
        for selection in selections:
            if not isinstance(selection, abjad.Selection):
                raise Exception(f'should be selection: {selection!r}.')
            assert len(selection) == 1, repr(selection)
            assert isinstance(selection[0], abjad.Tuplet)
            tuplets.append(selection[0])
        if self.lmr_specifier is None:
            tuplet_selections = [abjad.select(tuplets)]
        else:
            tuplet_selections = self.lmr_specifier(tuplets)
            tuplet_selections = [
                abjad.select(list(_)) for _ in tuplet_selections]
        selections_ = []
        prototype = abjad.Selection
        for index, tuplet_selection in enumerate(tuplet_selections):
            assert isinstance(tuplet_selection, prototype), repr(
                tuplet_selection)
            time_treatment = time_treatments[index]
            if time_treatment is None:
                selections_.append(tuplet_selection)
            else:
                nested_tuplet = self._make_nested_tuplet(
                    tuplet_selection,
                    time_treatment,
                    )
                selection_ = abjad.Selection([nested_tuplet])
                selections_.append(selection_)
        return selections_

    ### PRIVATE METHODS ###

    def _get_time_treatments(self):
        if self.time_treatments:
            return abjad.CyclicTuple(self.time_treatments)

    @staticmethod
    def _make_nested_tuplet(tuplet_selection, time_treatment):
        assert isinstance(tuplet_selection, abjad.Selection)
        for tuplet in tuplet_selection:
            assert isinstance(tuplet, abjad.Tuplet), repr(tuplet)
        if isinstance(time_treatment, str):
            addendum = abjad.Duration(time_treatment)
            contents_duration = abjad.inspect(tuplet_selection).duration()
            target_duration = contents_duration + addendum
            multiplier = target_duration / contents_duration
            tuplet = abjad.Tuplet(multiplier, [])
            abjad.mutate(tuplet_selection).wrap(tuplet)
        elif time_treatment.__class__ is abjad.Multiplier:
            #tuplet = abjad.Tuplet(time_treatment, tuplet_selection)
            tuplet = abjad.Tuplet(time_treatment, [])
            abjad.mutate(tuplet_selection).wrap(tuplet)
        elif time_treatment.__class__ is abjad.Duration:
            target_duration = time_treatment
            contents_duration = abjad.inspect(tuplet_selection).duration()
            multiplier = target_duration / contents_duration
            #tuplet = abjad.Tuplet(multiplier, tuplet_selection)
            tuplet = abjad.Tuplet(multiplier, [])
            abjad.mutate(tuplet_selection).wrap(tuplet)
        else:
            raise Exception(f'bad time treatment: {time_treatment!r}.')
        return tuplet

    ### PUBLIC PROPERTIES ###

    # TODO: write LMR specifier examples
    @property
    def lmr_specifier(self):
        """
        Gets LMR specifier.

        Defaults to none.

        Set to LMR specifier or none.

        Returns LMR specifier or none.
        """
        return self._lmr_specifier

    @property
    def time_treatments(self):
        """
        Gets time treatments.

        Defaults to none.

        Set to time treatments or none.

        Returns time treatments or none.
        """
        return self._time_treatments

class PitchFirstRhythmCommand(scoping.Command):
    """
    Pitch-first rhythm command.

    ..  container:: example

        >>> baca.PitchFirstRhythmCommand()
        PitchFirstRhythmCommand()

    """

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_pattern',
        '_rhythm_maker',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        pattern=None,
        rhythm_maker=None,
        ):
        if pattern is not None:
            assert isinstance(pattern, abjad.Pattern), repr(pattern)
        self._pattern = pattern
        self._rhythm_maker = rhythm_maker

    ### SPECIAL METHODS ###

    def __call__(
        self,
        collections,
        selections,
        division_masks=None,
        logical_tie_masks=None,
        rest_affix_specifier=None,
        talea_counts=None,
        talea_denominator=None,
        thread=None,
        time_treatments=None,
        tuplet_denominator=None,
        tuplet_force_fraction=None,
        ):
        assert len(selections) == len(collections)
        rhythm_maker = self._get_rhythm_maker(
            division_masks=division_masks,
            logical_tie_masks=logical_tie_masks,
            talea_counts=talea_counts,
            talea_denominator=talea_denominator,
            time_treatments=time_treatments,
            tuplet_denominator=tuplet_denominator,
            tuplet_force_fraction=tuplet_force_fraction,
            )
        length = len(selections)
        pattern = self.pattern or abjad.index_all()
        prototype = (abjad.Segment, abjad.Set, list)
        collections_, indices = [], []
        for index, collection in enumerate(collections):
            assert isinstance(collection, prototype), repr(collection)
            if isinstance(collection, (abjad.Set, set)):
                collection_ = list(sorted(collection))[:1]
            else:
                collection_ = collection
            if not pattern.matches_index(index, length):
                continue
            collections_.append(collection_)
            indices.append(index)
        if thread:
            stage_selections, state_manifest = rhythm_maker(
                collections_,
                rest_affix_specifier=rest_affix_specifier,
                )
        else:
            stage_selections = []
            total_collections = len(collections_)
            for collection_index, collection_ in enumerate(collections_):
                stage_selections_, stage_manifest = rhythm_maker(
                    [collection_],
                    rest_affix_specifier=rest_affix_specifier,
                    collection_index=collection_index,
                    total_collections=total_collections,
                    )
                stage_selections.extend(stage_selections_)
        triples = zip(indices, stage_selections, collections)
        for index, stage_selection, collection in triples:
            assert len(stage_selection) == 1, repr(stage_selection)
            if not isinstance(collection, (abjad.Set, set)):
                selections[index] = stage_selection
                continue
            assert len(stage_selection) == 1, repr(stage_selection)
            tuplet = stage_selection[0]
            assert isinstance(tuplet, abjad.Tuplet), repr(tuplet)
            agent = abjad.iterate(stage_selection)
            logical_ties = agent.logical_ties(pitched=True)
            logical_ties = list(logical_ties)
            assert len(logical_ties) == 1, repr(stage_selection)
            logical_tie = logical_ties[0]
            for note in logical_tie.leaves:
                assert isinstance(note, abjad.Note), repr(note)
                duration = note.written_duration
                pitches = collection
                chord = abjad.Chord(pitches, duration)
                abjad.mutate(note).replace([chord])
            selections[index] = stage_selection
        return selections

    def _get_rhythm_maker(
        self,
        division_masks=None,
        logical_tie_masks=None,
        talea_counts=None,
        talea_denominator=None,
        time_treatments=None,
        tuplet_denominator=None,
        tuplet_force_fraction=None,
        ):
        rhythm_maker = self.rhythm_maker
        if rhythm_maker is None:
            mask = rmakers.silence([0], 1, use_multimeasure_rests=True)
            rhythm_maker = rmakers.NoteRhythmMaker(division_masks=[mask])
        keywords = {}
        if division_masks is not None:
            keywords['division_masks'] = division_masks
        if logical_tie_masks is not None:
            keywords['logical_tie_masks'] = logical_tie_masks
        if talea_counts is not None:
            keywords['talea__counts'] = talea_counts
        if talea_denominator is not None:
            keywords['talea__denominator'] = talea_denominator
        if time_treatments is not None:
            keywords['time_treatments'] = time_treatments
        if keywords:
            rhythm_maker = abjad.new(rhythm_maker, **keywords)
        if (tuplet_denominator is not None or
            tuplet_force_fraction is not None):
            specifier = rhythm_maker.tuplet_specifier
            if specifier is None:
                specifier = rmakers.TupletSpecifier()
            specifier = abjad.new(
                specifier,
                denominator=tuplet_denominator,
                force_fraction=tuplet_force_fraction,
                )
            rhythm_maker = abjad.new(
                rhythm_maker,
                tuplet_specifier=specifier,
                )
        return rhythm_maker

    ### PUBLIC PROPERTIES ###

    @property
    def pattern(self):
        """
        Gets pattern.

        Set to pattern or none.

        Defaults to none.

        Returns pattern or none.
        """
        return self._pattern

    @property
    def rhythm_maker(self):
        """
        Gets rhythm-maker.

        Set to rhythm-maker or none.

        Defaults to none.

        Returns rhythm-maker or music.
        """
        return self._rhythm_maker

class PitchFirstRhythmMaker(rmakers.RhythmMaker):
    r"""
    Collection rhythm-maker.

    >>> from abjadext import rmakers

    ..  container:: example

        Sixteenths and eighths:

        >>> rhythm_maker = baca.PitchFirstRhythmMaker(
        ...     talea=rmakers.Talea(
        ...         counts=[1, 1, 2],
        ...         denominator=16,
        ...         ),
        ...     )

        >>> collections = [[0, 2, 10, 8]]
        >>> selections, state = rhythm_maker(collections)
        >>> lilypond_file = rhythm_maker.show(selections)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            {
                {   % measure
                    \time 5/16
                    \scaleDurations #'(1 . 1) {
                        c'16
                        [
                        d'16
                        bf'8
                        af'16
                        ]
                    }
                }   % measure
            }

        >>> collections = [[18, 16, 15, 20, 19]]
        >>> selections, state = rhythm_maker(collections)
        >>> lilypond_file = rhythm_maker.show(selections)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            {
                {   % measure
                    \time 3/8
                    \scaleDurations #'(1 . 1) {
                        fs''16
                        [
                        e''16
                        ef''8
                        af''16
                        g''16
                        ]
                    }
                }   % measure
            }

        >>> collections = [[9]]
        >>> selections, state = rhythm_maker(collections)
        >>> lilypond_file = rhythm_maker.show(selections)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            {
                {   % measure
                    \time 1/16
                    \scaleDurations #'(1 . 1) {
                        a'16
                    }
                }   % measure
            }

        >>> collections = [[0, 2, 10, 8], [18, 16, 15, 20, 19], [9]]
        >>> selections, state = rhythm_maker(collections)
        >>> lilypond_file = rhythm_maker.show(selections)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            {
                {   % measure
                    \time 13/16
                    \scaleDurations #'(1 . 1) {
                        c'16
                        [
                        d'16
                        bf'8
                        af'16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        fs''16
                        [
                        e''8
                        ef''16
                        af''16
                        g''8
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        a'16
                    }
                }   % measure
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_acciaccatura_specifiers',
        '_next_attack',
        '_next_segment',
        '_talea',
        '_time_treatments',
        )

    _state_variables = (
        '_next_attack',
        '_next_segment',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        acciaccatura_specifiers=None,
        beam_specifier=None,
        division_masks=None,
        duration_specifier=None,
        logical_tie_masks=None,
        talea=None,
        tie_specifier=None,
        time_treatments=None,
        tuplet_specifier=None,
        ):
        rmakers.RhythmMaker.__init__(
            self,
            beam_specifier=beam_specifier,
            duration_specifier=duration_specifier,
            division_masks=division_masks,
            logical_tie_masks=logical_tie_masks,
            tie_specifier=tie_specifier,
            tuplet_specifier=tuplet_specifier,
            )
        if acciaccatura_specifiers is not None:
            prototype = AcciaccaturaSpecifier
            for acciaccatura_specifier in acciaccatura_specifiers:
                assert isinstance(acciaccatura_specifier, prototype)
        self._acciaccatura_specifiers = acciaccatura_specifiers
        self._next_attack = 0
        self._next_segment = 0
        self._state = abjad.OrderedDict()
        talea = talea or rmakers.Talea()
        if not isinstance(talea, rmakers.Talea):
            raise TypeError(f'must be talea: {talea!r}.')
        self._talea = talea
        if time_treatments is not None:
            for time_treatment in time_treatments:
                if not self._is_time_treatment(time_treatment):
                    raise Exception(f'bad time treatment: {time_treatment!r}.')
        self._time_treatments = time_treatments

    ### SPECIAL METHODS ###

    def __call__(
        self,
        collections,
        collection_index=None,
        rest_affix_specifier=None,
        state=None,
        total_collections=None,
        ):
        r"""
        Calls rhythm-maker on ``collections``.

        ..  container:: example

            Without state manifest:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/4
                        \scaleDurations #'(1 . 1) {
                            c'16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'8
                        }
                    }   % measure
                }

            >>> abjad.f(rhythm_maker._make_state())
            abjad.OrderedDict(
                [
                    ('_next_attack', 9),
                    ('_next_segment', 3),
                    ]
                )

        ..  container:: example

            With state manifest:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> state = {'_next_attack': 2}
            >>> selections, state = rhythm_maker(
            ...     collections,
            ...     state=state,
            ...     )
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/4
                        \scaleDurations #'(1 . 1) {
                            c'8
                            [
                            d'16
                            bf'16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''8
                            [
                            e''16
                            ef''16
                            af''8
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'16
                        }
                    }   % measure
                }

            >>> abjad.f(rhythm_maker._make_state())
            abjad.OrderedDict(
                [
                    ('_next_attack', 11),
                    ('_next_segment', 3),
                    ]
                )

        Returns selections together with state manifest.
        """
        self._state = state or abjad.OrderedDict()
        self._apply_state(state=state)
        selections = self._make_music(
            collections,
            rest_affix_specifier=rest_affix_specifier,
            collection_index=collection_index,
            total_collections=total_collections,
            )
        selections = self._apply_specifiers(selections)
        #self._check_wellformedness(selections)
        state = self._make_state()
        return selections, state

    ### PRIVATE METHODS ###

    @staticmethod
    def _add_rest_affixes(
        leaves,
        talea,
        rest_prefix,
        rest_suffix,
        affix_skips_instead_of_rests,
        decrease_durations,
        ):
        if rest_prefix:
            durations = [(_, talea.denominator) for _ in rest_prefix]
            maker = abjad.LeafMaker(
                decrease_monotonic=decrease_durations,
                skips_instead_of_rests=affix_skips_instead_of_rests,
                )
            leaves_ = maker([None], durations)
            leaves[0:0] = leaves_
        if rest_suffix:
            durations = [(_, talea.denominator) for _ in rest_suffix]
            maker = abjad.LeafMaker(
                decrease_monotonic=decrease_durations,
                skips_instead_of_rests=affix_skips_instead_of_rests,
                )
            leaves_ = maker([None], durations)
            leaves.extend(leaves_)
        return leaves

    def _apply_state(self, state=None):
        for name in self._state_variables:
            value = setattr(self, name, 0)
        state = state or {}
        assert isinstance(state, dict), repr(state)
        for key in state:
            value = state[key]
            setattr(self, key, value)

    @staticmethod
    def _fix_rounding_error(durations, total_duration):
        current_duration = sum(durations)
        if current_duration < total_duration:
            missing_duration = total_duration - current_duration
            if durations[0] < durations[-1]:
                durations[-1] += missing_duration
            else:
                durations[0] += missing_duration
        elif sum(durations) == total_duration:
            return durations
        elif total_duration < current_duration:
            extra_duration = current_duration - total_duration
            if durations[0] < durations[-1]:
                durations[-1] -= extra_duration
            else:
                durations[0] -= extra_duration
        assert sum(durations) == total_duration
        return durations

    def _get_acciaccatura_specifier(self, collection_index, total_collections):
        if not self.acciaccatura_specifiers:
            return
        for acciaccatura_specifier in self.acciaccatura_specifiers:
            pattern = acciaccatura_specifier._get_pattern()
            if pattern.matches_index(collection_index, total_collections):
                return acciaccatura_specifier

    def _get_talea(self):
        if self.talea is not None:
            return self.talea
        return rmakers.Talea()

    def _get_time_treatments(self):
        if not self.time_treatments:
            return abjad.CyclicTuple([0])
        return abjad.CyclicTuple(self.time_treatments)

    @staticmethod
    def _is_time_treatment(argument):
        if argument is None:
            return True
        elif isinstance(argument, int):
            return True
        elif isinstance(argument, str):
            return True
        elif isinstance(argument, abjad.Ratio):
            return True
        elif isinstance(argument, abjad.Multiplier):
            return True
        elif argument.__class__ is abjad.Duration:
            return True
        elif argument in ('accel', 'rit'):
            return True
        return False

    @classmethod
    def _make_accelerando(class_, leaf_selection, accelerando_indicator):
        assert accelerando_indicator in ('accel', 'rit')
        tuplet = abjad.Tuplet((1, 1), leaf_selection)
        if len(tuplet) == 1:
            return tuplet
        durations = [abjad.inspect(_).duration() for _ in leaf_selection]
        if accelerando_indicator == 'accel':
            exponent = 0.625
        elif accelerando_indicator == 'rit':
            exponent = 1.625
        multipliers = class_._make_accelerando_multipliers(durations, exponent)
        assert len(leaf_selection) == len(multipliers)
        for multiplier, leaf in zip(multipliers, leaf_selection):
            abjad.attach(multiplier, leaf)
        rhythm_maker_class = rmakers.AccelerandoRhythmMaker
        if rhythm_maker_class._is_accelerando(leaf_selection):
            abjad.override(leaf_selection[0]).beam.grow_direction = abjad.Right
        elif rhythm_maker_class._is_ritardando(leaf_selection):
            abjad.override(leaf_selection[0]).beam.grow_direction = abjad.Left
        duration = abjad.inspect(tuplet).duration()
        duration = abjad.Duration(duration)
        markup = duration.to_score_markup()
        markup = markup.scale((0.75, 0.75))
        abjad.override(tuplet).tuplet_number.text = markup
        return tuplet

    @classmethod
    def _make_accelerando_multipliers(class_, durations, exponent):
        r"""
        Makes accelerando multipliers.

        ..  container:: example

            Set exponent less than 1 for decreasing durations:

            >>> class_ = baca.PitchFirstRhythmMaker
            >>> durations = 4 * [abjad.Duration(1)]
            >>> result = class_._make_accelerando_multipliers(
            ...     durations,
            ...     0.5,
            ...     )
            >>> for multiplier in result: multiplier
            ...
            NonreducedFraction(2048, 1024)
            NonreducedFraction(848, 1024)
            NonreducedFraction(651, 1024)
            NonreducedFraction(549, 1024)

        ..  container:: example

            Set exponent to 1 for trivial multipliers:

            >>> class_ = baca.PitchFirstRhythmMaker
            >>> durations = 4 * [abjad.Duration(1)]
            >>> result = class_._make_accelerando_multipliers(durations, 1)
            >>> for multiplier in result: multiplier
            ...
            NonreducedFraction(1024, 1024)
            NonreducedFraction(1024, 1024)
            NonreducedFraction(1024, 1024)
            NonreducedFraction(1024, 1024)

        ..  container:: example

            Set exponent greater than 1 for increasing durations:

            >>> class_ = baca.PitchFirstRhythmMaker
            >>> durations = 4 * [abjad.Duration(1)]
            >>> result = class_._make_accelerando_multipliers(
            ...     durations,
            ...     0.5,
            ...     )
            >>> for multiplier in result: multiplier
            ...
            NonreducedFraction(2048, 1024)
            NonreducedFraction(848, 1024)
            NonreducedFraction(651, 1024)
            NonreducedFraction(549, 1024)

        Set exponent greater than 1 for ritardando.

        Set exponent less than 1 for accelerando.
        """
        pairs = abjad.mathtools.cumulative_sums_pairwise(durations)
        total_duration = pairs[-1][-1]
        start_offsets = [_[0] for _ in pairs]
        #print(total_duration, start_offsets)
        start_offsets = [_ / total_duration for _ in start_offsets]
        #print(total_duration, start_offsets)
        start_offsets_ = []
        rhythm_maker_class = rmakers.AccelerandoRhythmMaker
        for start_offset in start_offsets:
            start_offset_ = rhythm_maker_class._interpolate_exponential(
                0,
                total_duration,
                start_offset,
                exponent,
                )
            start_offsets_.append(start_offset_)
        #print(start_offsets_)
        #start_offsets_ = [float(total_duration * _) for _ in start_offsets_]
        start_offsets_.append(float(total_duration))
        durations_ = abjad.mathtools.difference_series(start_offsets_)
        durations_ = rhythm_maker_class._round_durations(durations_, 2**10)
        durations_ = class_._fix_rounding_error(durations_, total_duration)
        multipliers = []
        assert len(durations) == len(durations_)
        for duration_, duration in zip(durations_, durations):
            multiplier = duration_ / duration
            multiplier = abjad.Multiplier(multiplier)
            multiplier = multiplier.with_denominator(2**10)
            multipliers.append(multiplier)
        return multipliers

    def _make_music(
        self,
        collections,
        rest_affix_specifier=None,
        collection_index=None,
        total_collections=None,
        ):
        segment_count = len(collections)
        selections = []
        if collection_index is None:
            for i, segment in enumerate(collections):
                if rest_affix_specifier is not None:
                    result = rest_affix_specifier(i, segment_count)
                    rest_prefix, rest_suffix = result
                    affix_skips_instead_of_rests = \
                        rest_affix_specifier.skips_instead_of_rests
                else:
                    rest_prefix, rest_suffix = None, None
                    affix_skips_instead_of_rests = None
                selection = self._make_selection(
                    segment,
                    segment_count,
                    rest_prefix=rest_prefix,
                    rest_suffix=rest_suffix,
                    affix_skips_instead_of_rests=affix_skips_instead_of_rests,
                    )
                selections.append(selection)
        else:
            assert len(collections) == 1, repr(collections)
            segment = collections[0]
            if rest_affix_specifier is not None:
                result = rest_affix_specifier(collection_index, total_collections)
                rest_prefix, rest_suffix = result
                affix_skips_instead_of_rests = \
                    rest_affix_specifier.skips_instead_of_rests
            else:
                rest_prefix, rest_suffix = None, None
                affix_skips_instead_of_rests = None
            selection = self._make_selection(
                segment,
                segment_count,
                rest_prefix=rest_prefix,
                rest_suffix=rest_suffix,
                affix_skips_instead_of_rests=affix_skips_instead_of_rests,
                )
            selections.append(selection)
        beam_specifier = self._get_beam_specifier()
        beam_specifier(selections)
        selections = self._apply_division_masks(selections)
        specifier = self._get_duration_specifier()
        if specifier.rewrite_meter:
            #selections = specifier._rewrite_meter_(
            #    selections,
            #    input_divisions,
            #    )
            raise NotImplementedError()
        return selections

    def _make_selection(
        self,
        segment,
        segment_count,
        rest_prefix=None,
        rest_suffix=None,
        affix_skips_instead_of_rests=None,
        ):
        collection_index = self._next_segment
        acciaccatura_specifier = self._get_acciaccatura_specifier(
            collection_index,
            segment_count,
            )
        self._next_segment += 1
        if not segment:
            return abjad.Selection()
        talea = self._get_talea()
        leaves = []
        specifier = self._get_duration_specifier()
        decrease_durations = specifier.decrease_monotonic
        current_selection = self._next_segment - 1
        time_treatment = self._get_time_treatments()[current_selection]
        if time_treatment is None:
            time_treatment = 0
        grace_containers = None
        if acciaccatura_specifier is not None:
            grace_containers, segment = acciaccatura_specifier(segment)
            assert len(grace_containers) == len(segment)
        for pitch_expression in segment:
            prototype = abjad.NumberedPitchClass
            if isinstance(pitch_expression, prototype):
                pitch_expression = pitch_expression.number
            count = self._next_attack
            while talea[count] < 0:
                self._next_attack += 1
                duration = -talea[count]
                maker = abjad.LeafMaker(
                    decrease_monotonic=decrease_durations,
                    )
                leaves_ = maker([None], [duration])
                leaves.extend(leaves_)
                count = self._next_attack
            self._next_attack += 1
            duration = talea[count]
            assert 0 < duration, repr(duration)
            skips_instead_of_rests = False
            if (isinstance(pitch_expression, tuple) and
                len(pitch_expression) == 2 and
                pitch_expression[-1] in (None, 'skip')):
                multiplier = pitch_expression[0]
                duration = abjad.Duration(1, talea.denominator)
                duration *= multiplier
                if pitch_expression[-1] == 'skip':
                    skips_instead_of_rests = True
                pitch_expression = None
            maker = abjad.LeafMaker(
                decrease_monotonic=decrease_durations,
                skips_instead_of_rests=skips_instead_of_rests,
                )
            leaves_ = maker([pitch_expression], [duration])
            leaves.extend(leaves_)
            count = self._next_attack
            while talea[count] < 0 and not count % len(talea) == 0:
                self._next_attack += 1
                duration = -talea[count]
                maker = abjad.LeafMaker(
                    decrease_monotonic=decrease_durations,
                    )
                leaves_ = maker([None], [duration])
                leaves.extend(leaves_)
                count = self._next_attack
        leaves = self._add_rest_affixes(
            leaves,
            talea,
            rest_prefix,
            rest_suffix,
            affix_skips_instead_of_rests,
            decrease_durations,
            )
        leaf_selection = abjad.select(leaves)
        if isinstance(time_treatment, int):
            tuplet = self._make_tuplet_with_extra_count(
                leaf_selection,
                time_treatment,
                talea.denominator,
                )
        elif time_treatment in ('accel', 'rit'):
            tuplet = self._make_accelerando(leaf_selection, time_treatment)
        elif isinstance(time_treatment, abjad.Ratio):
            numerator, denominator = time_treatment.numbers
            multiplier = abjad.NonreducedFraction((denominator, numerator))
            tuplet = abjad.Tuplet(multiplier, leaf_selection)
        elif isinstance(time_treatment, abjad.Multiplier):
            tuplet = abjad.Tuplet(time_treatment, leaf_selection)
        elif time_treatment.__class__ is abjad.Duration:
            tuplet_duration = time_treatment
            contents_duration = abjad.inspect(leaf_selection).duration()
            multiplier = tuplet_duration / contents_duration
            tuplet = abjad.Tuplet(multiplier, leaf_selection)
            if not tuplet.multiplier.normalized():
                tuplet.normalize_multiplier()
        else:
            raise Exception(f'bad time treatment: {time_treatment!r}.')
        assert isinstance(tuplet, abjad.Tuplet)
        if grace_containers is not None:
            logical_ties = abjad.iterate(tuplet).logical_ties()
            pairs = zip(grace_containers, logical_ties)
            for grace_container, logical_tie in pairs:
                if grace_container is None:
                    continue
                abjad.attach(
                    grace_container,
                    logical_tie.head,
                    tag='PFRM_1',
                    )
        if tuplet.trivial():
            tuplet.hide = True
        selection = abjad.select([tuplet])
        return selection

    def _make_state(self):
        state = abjad.OrderedDict()
        for name in sorted(self._state_variables):
            value = getattr(self, name)
            state[name] = value
        return state

    @staticmethod
    def _make_tuplet_with_extra_count(
        leaf_selection,
        extra_count,
        denominator,
        ):
        contents_duration = abjad.inspect(leaf_selection).duration()
        contents_duration = contents_duration.with_denominator(denominator)
        contents_count = contents_duration.numerator
        if 0 < extra_count:
            extra_count %= contents_count
        elif extra_count < 0:
            extra_count = abs(extra_count)
            extra_count %= math.ceil(contents_count / 2.0)
            extra_count *= -1
        new_contents_count = contents_count + extra_count
        tuplet_multiplier = abjad.Multiplier(
            new_contents_count,
            contents_count,
            )
        if not tuplet_multiplier.normalized():
            message = f'{leaf_selection!r} gives {tuplet_multiplier}'
            message += ' with {contents_count} and {new_contents_count}.'
            raise Exception(message)
        tuplet = abjad.Tuplet(tuplet_multiplier, leaf_selection)
        return tuplet

    @staticmethod
    def _normalize_multiplier(multiplier):
        assert 0 < multiplier, repr(multiplier)
        while multiplier <= abjad.Multiplier(1, 2):
            multiplier *= 2
        while abjad.Multiplier(2) <= multiplier:
            multiplier /= 2
        return multiplier

    ### PUBLIC PROPERTIES ###

    @property
    def acciaccatura_specifiers(self):
        r"""
        Gets acciaccatura specifiers.

        ..  container:: example

            Graced quarters:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     acciaccatura_specifiers=[
            ...         baca.AcciaccaturaSpecifier()
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=4,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/2
                        \scaleDurations #'(1 . 1) {
                            c'4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                            }
                            bf'4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''16
                                [                                                                        %! ACC_1
                                e''16
                                ]                                                                        %! ACC_1
                            }
                            ef''4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! ACC_1
                                g''16
                                a'16
                                ]                                                                        %! ACC_1
                            }
                            c'4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                                [                                                                        %! ACC_1
                                bf'16
                                fs''16
                                e''16
                                ]                                                                        %! ACC_1
                            }
                            ef''4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! ACC_1
                                g''16
                                a'16
                                c'16
                                d'16
                                ]                                                                        %! ACC_1
                            }
                            bf'4
                        }
                    }   % measure
                }

        ..  container:: example

            Graced rests:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     acciaccatura_specifiers=[
            ...         baca.AcciaccaturaSpecifier(
            ...             lmr_specifier=baca.LMRSpecifier()
            ...             ),
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=4,
            ...         ),
            ...     )

            >>> collections = [
            ...     [None],
            ...     [0, None],
            ...     [2, 10, None],
            ...     [18, 16, 15, None],
            ...     [20, 19, 9, 0, None],
            ...     [2, 10, 18, 16, 15, None],
            ...     [20, 19, 9, 0, 2, 10, None],
            ...     ]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 7/4
                        \scaleDurations #'(1 . 1) {
                            r4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                c'16
                            }
                            r4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                                [                                                                        %! ACC_1
                                bf'16
                                ]                                                                        %! ACC_1
                            }
                            r4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                fs''16
                                [                                                                        %! ACC_1
                                e''16
                                ef''16
                                ]                                                                        %! ACC_1
                            }
                            r4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! ACC_1
                                g''16
                                a'16
                                c'16
                                ]                                                                        %! ACC_1
                            }
                            r4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                d'16
                                [                                                                        %! ACC_1
                                bf'16
                                fs''16
                                e''16
                                ef''16
                                ]                                                                        %! ACC_1
                            }
                            r4
                        }
                        \scaleDurations #'(1 . 1) {
                            \acciaccatura {
                                af''16
                                [                                                                        %! ACC_1
                                g''16
                                a'16
                                c'16
                                d'16
                                bf'16
                                ]                                                                        %! ACC_1
                            }
                            r4
                        }
                    }   % measure
                }

        ..  container:: example

            Defaults to none:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker()
            >>> rhythm_maker.acciaccatura_specifiers is None
            True

        Set to acciaccatura specifiers or none.

        Returns acciaccatura specifiers or none.
        """
        return self._acciaccatura_specifiers

    @property
    def beam_specifier(self):
        r"""
        Gets beam specifier.

        ..  container:: example

            Beams each division by default:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     time_treatments=[1],
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).tuplet_bracket.staff_padding = 1.5
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.staff-padding = #1.5
                }
                {
                    {   % measure
                        \time 15/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/4 {
                            c'16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/6 {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            g''16
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/2 {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Beams divisions together:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     beam_specifier=rmakers.BeamSpecifier(
            ...         beam_divisions_together=True,
            ...         ),
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     time_treatments=[1],
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).beam.positions = (-5.5, -5.5)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override Beam.positions = #'(-5.5 . -5.5)
                }
                {
                    {   % measure
                        \time 15/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/4 {
                            \set stemLeftBeamCount = 0
                            \set stemRightBeamCount = 2
                            c'16
                            [
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            d'16
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 1
                            bf'8
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/6 {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            fs''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            e''16
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 1
                            ef''8
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 2
                            af''16
                            \set stemLeftBeamCount = 2
                            \set stemRightBeamCount = 1
                            g''16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/2 {
                            \set stemLeftBeamCount = 1
                            \set stemRightBeamCount = 0
                            a'8
                            ]
                        }
                    }   % measure
                }

        ..  container:: example

            Beams nothing:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     beam_specifier=rmakers.BeamSpecifier(
            ...         beam_each_division=False,
            ...         ),
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     time_treatments=[1],
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 15/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/4 {
                            c'16
                            d'16
                            bf'8
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/6 {
                            fs''16
                            e''16
                            ef''8
                            af''16
                            g''16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/2 {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Does not beam rests:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     time_treatments=[1],
            ...     )

            >>> collections = [[None, 2, 10], [18, 16, 15, 20, None], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).tuplet_bracket.staff_padding = 1.5
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.staff-padding = #1.5
                }
                {
                    {   % measure
                        \time 15/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/4 {
                            r16
                            d'16
                            [
                            bf'8
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/6 {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            ]
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/2 {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Does beam rests:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     beam_specifier=rmakers.BeamSpecifier(
            ...         beam_rests=True,
            ...     ),
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     time_treatments=[1],
            ...     )

            >>> collections = [[None, 2, 10], [18, 16, 15, 20, None], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).tuplet_bracket.staff_padding = 1.5
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.staff-padding = #1.5
                }
                {
                    {   % measure
                        \time 15/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/4 {
                            r16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/6 {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            r16
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/2 {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Beams rests with stemlets:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     beam_specifier=rmakers.BeamSpecifier(
            ...         beam_rests=True,
            ...         stemlet_length=0.75,
            ...     ),
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     time_treatments=[1],
            ...     )

            >>> collections = [[None, 2, 10], [18, 16, 15, 20, None], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).tuplet_bracket.staff_padding = 1.5
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.staff-padding = #1.5
                }
                {
                    {   % measure
                        \time 15/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/4 {
                            \override Staff.Stem.stemlet-length = 0.75
                            r16
                            [
                            d'16
                            \revert Staff.Stem.stemlet-length
                            bf'8
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/6 {
                            \override Staff.Stem.stemlet-length = 0.75
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            \revert Staff.Stem.stemlet-length
                            r16
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/2 {
                            \override Staff.Stem.stemlet-length = 0.75
                            \revert Staff.Stem.stemlet-length
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Defaults to none:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker()
            >>> rhythm_maker.beam_specifier is None
            True

        Set to beam specifier or none.

        Returns beam specifier or none.
        """
        return rmakers.RhythmMaker.beam_specifier.fget(self)

    @property
    def division_masks(self):
        r"""
        Gets division masks.

        ..  container:: example

            No division masks:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/4
                        \scaleDurations #'(1 . 1) {
                            c'16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Silences every other division:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     division_masks=[
            ...         rmakers.silence([1], 2),
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/4
                        \scaleDurations #'(1 . 1) {
                            c'16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        r4.
                        \scaleDurations #'(1 . 1) {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Sustains every other division:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     division_masks=[
            ...         rmakers.sustain([1], 2),
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/4
                        \scaleDurations #'(1 . 1) {
                            c'16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        c'4.
                        \scaleDurations #'(1 . 1) {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Defaults to none:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker()
            >>> rhythm_maker.division_masks is None
            True

        Set to division masks or none.

        Returns tuple of division masks or none.
        """
        return rmakers.RhythmMaker.division_masks.fget(self)

    @property
    def duration_specifier(self):
        r"""
        Gets duration specifier.

        ..  container:: example

            Spells nonassignable durations with monontonically decreasing
            durations by default:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     talea=rmakers.Talea(
            ...         counts=[4, 4, 5],
            ...         denominator=32,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 39/32
                        \scaleDurations #'(1 . 1) {
                            c'8
                            [
                            d'8
                            bf'8
                            ~
                            bf'32
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''8
                            [
                            e''8
                            ef''8
                            ~
                            ef''32
                            af''8
                            g''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'8
                            ~
                            [
                            a'32
                            ]
                        }
                    }   % measure
                }

        ..  container:: example

            Spells nonassignable durations with monontonically increasing
            durations:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     duration_specifier=rmakers.DurationSpecifier(
            ...         decrease_monotonic=False,
            ...         ),
            ...     talea=rmakers.Talea(
            ...         counts=[4, 4, 5],
            ...         denominator=32,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 39/32
                        \scaleDurations #'(1 . 1) {
                            c'8
                            [
                            d'8
                            bf'32
                            ~
                            bf'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''8
                            [
                            e''8
                            ef''32
                            ~
                            ef''8
                            af''8
                            g''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'32
                            ~
                            [
                            a'8
                            ]
                        }
                    }   % measure
                }

        ..  container:: example

            Defaults to none:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker()
            >>> rhythm_maker.duration_specifier is None
            True

        Set to duration specifier or none.

        Returns duration specifier or none.
        """
        return rmakers.RhythmMaker.duration_specifier.fget(self)

    @property
    def logical_tie_masks(self):
        r"""
        Gets logical tie masks.

        ..  container:: example

            Silences every third logical tie:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     logical_tie_masks=[
            ...         rmakers.silence([2], 3),
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/4
                        \scaleDurations #'(1 . 1) {
                            c'16
                            [
                            d'16
                            ]
                            r8
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''16
                            [
                            e''16
                            ]
                            r8
                            af''16
                            [
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            r8
                        }
                    }   % measure
                }

        ..  container:: example

            Silences first and last logical ties:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     logical_tie_masks=[
            ...         rmakers.silence([0]),
            ...         rmakers.silence([-1]),
            ...         ],
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/4
                        \scaleDurations #'(1 . 1) {
                            r16
                            d'16
                            [
                            bf'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            r8
                        }
                    }   % measure
                }

        ..  container:: example

            Defaults to none:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker()
            >>> rhythm_maker.logical_tie_masks is None
            True

        Set to patterns or none.

        Returns tuple patterns or none.
        """
        return rmakers.RhythmMaker.logical_tie_masks.fget(self)

    @property
    def talea(self):
        r"""
        Gets talea.

        ..  container:: example

            With rests:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     beam_specifier=rmakers.BeamSpecifier(
            ...         beam_rests=True,
            ...         stemlet_length=1.5,
            ...         ),
            ...     talea=rmakers.Talea(
            ...         counts=[3, -1, 2, 2],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/2
                        \scaleDurations #'(1 . 1) {
                            \override Staff.Stem.stemlet-length = 1.5
                            c'8.
                            [
                            r16
                            d'8
                            \revert Staff.Stem.stemlet-length
                            bf'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \override Staff.Stem.stemlet-length = 1.5
                            fs''8.
                            [
                            r16
                            e''8
                            ef''8
                            af''8.
                            r16
                            \revert Staff.Stem.stemlet-length
                            g''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \override Staff.Stem.stemlet-length = 1.5
                            \revert Staff.Stem.stemlet-length
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            With very large nonassignable counts:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     talea=rmakers.Talea(
            ...         counts=[29],
            ...         denominator=64,
            ...         ),
            ...     tie_specifier=rmakers.TieSpecifier(
            ...         repeat_ties=True,
            ...         ),
            ...     )

            >>> collections = [[0, 2]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 29/32
                        \scaleDurations #'(1 . 1) {
                            c'4..
                            c'64
                            \repeatTie
                            d'4..
                            d'64
                            \repeatTie
                        }
                    }   % measure
                }

        ..  container:: example

            Defaults to even sixteenths:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker()
            >>> rhythm_maker.talea
            Talea(counts=[1], denominator=16)

        Set to talea or none.

        Returns talea.
        """
        return self._talea

    @property
    def tie_specifier(self):
        r"""
        Gets tie specifier.

        ..  container:: example

            Ties across divisions with matching pitches:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     tie_specifier=rmakers.TieSpecifier(
            ...         tie_across_divisions=True,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [10, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/4
                        \scaleDurations #'(1 . 1) {
                            c'16
                            [
                            d'16
                            bf'8
                            ~
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            bf'16
                            [
                            e''16
                            ef''8
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Ties consecutive notes with matching pitches:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     tie_specifier=rmakers.TieSpecifier(
            ...         tie_consecutive_notes=True,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [10, 16, 16, 19, 19], [19]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 3/4
                        \scaleDurations #'(1 . 1) {
                            c'16
                            [
                            d'16
                            bf'8
                            ~
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            bf'16
                            [
                            e''16
                            ~
                            e''8
                            g''16
                            ~
                            g''16
                            ~
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            g''8
                        }
                    }   % measure
                }

        ..  container:: example

            Defaults to none:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker()
            >>> rhythm_maker.tie_specifier is None
            True

        Set to tie specifier or none.

        Returns tie specifier or none.
        """
        return rmakers.RhythmMaker.tie_specifier.fget(self)

    @property
    def time_treatments(self):
        r"""
        Gets time treatments.

        ..  container:: example

            One extra count per division:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     time_treatments=[1],
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 15/16
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/4 {
                            c'16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/6 {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            g''16
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/2 {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            One missing count per division:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     time_treatments=[-1],
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 5/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/6 {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Accelerandi:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     time_treatments=['accel'],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state = rhythm_maker(collections)

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 5/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/6 {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Ritardandi:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     time_treatments=['rit'],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state = rhythm_maker(collections)

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 5/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/6 {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Accelerandi followed by ritardandi:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     time_treatments=['accel', 'rit'],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0, 2],
            ...     [10, 18, 16, 15, 20],
            ...     [19, 9, 0, 2, 10, 18],
            ...     ]
            >>> selections, state = rhythm_maker(collections)

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 5/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/6 {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Mixed accelerandi, ritardandi and prolation:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     time_treatments=['accel', -2, 'rit'],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=16,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2],
            ...     [10, 18, 16, 15, 20],
            ...     [19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state = rhythm_maker(collections)

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                {
                    {   % measure
                        \time 5/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 3/4 {
                            c'16
                            [
                            d'16
                            bf'8
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 5/6 {
                            fs''16
                            [
                            e''16
                            ef''8
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'8
                        }
                    }   % measure
                }

        ..  container:: example

            Specified by tuplet multiplier:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     time_treatments=[abjad.Ratio((3, 2))],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=8,
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).beam.positions = (-6, -6)
            >>> abjad.override(staff).stem.direction = Down
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override Beam.positions = #'(-6 . -6)
                    \override Stem.direction = #down
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak edge-height #'(0.7 . 0)
                        \times 2/3 {
                            c'8
                        }
                        \tweak edge-height #'(0.7 . 0)
                        \times 2/3 {
                            d'8
                            [
                            bf'8
                            ]
                        }
                        \times 2/3 {
                            fs''8
                            [
                            e''8
                            ef''8
                            ]
                        }
                        \tweak edge-height #'(0.7 . 0)
                        \times 2/3 {
                            af''8
                            [
                            g''8
                            a'8
                            c'8
                            ]
                        }
                        \tweak edge-height #'(0.7 . 0)
                        \times 2/3 {
                            d'8
                            [
                            bf'8
                            fs''8
                            e''8
                            ef''8
                            ]
                        }
                        \times 2/3 {
                            af''8
                            [
                            g''8
                            a'8
                            c'8
                            d'8
                            bf'8
                            ]
                        }
                    }   % measure
                }

        ..  container:: example

            Segment durations equal to a quarter:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     time_treatments=[abjad.Duration(1, 4)],
            ...     talea=rmakers.Talea(
            ...         counts=[1],
            ...         denominator=8,
            ...         ),
            ...     tuplet_specifier=rmakers.TupletSpecifier(
            ...         denominator=abjad.Duration(1, 16),
            ...         ),
            ...     )

            >>> collections = [
            ...     [0],
            ...     [2, 10],
            ...     [18, 16, 15],
            ...     [20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).beam.positions = (-6, -6)
            >>> abjad.override(staff).stem.direction = Down
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override Beam.positions = #'(-6 . -6)
                    \override Stem.direction = #down
                }
                {
                    {   % measure
                        \time 3/2
                        \scaleDurations #'(1 . 1) {
                            c'4
                        }
                        \scaleDurations #'(1 . 1) {
                            d'8
                            [
                            bf'8
                            ]
                        }
                        \times 4/6 {
                            fs''8
                            [
                            e''8
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            af''16
                            [
                            g''16
                            a'16
                            c'16
                            ]
                        }
                        \times 4/5 {
                            d'16
                            [
                            bf'16
                            fs''16
                            e''16
                            ef''16
                            ]
                        }
                        \times 4/6 {
                            af''16
                            [
                            g''16
                            a'16
                            c'16
                            d'16
                            bf'16
                            ]
                        }
                    }   % measure
                }

        ..  container:: example

            Segment durations alternating between a quarter and a dotted
            quarter:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     time_treatments=[abjad.Duration(1, 4), abjad.Duration(3, 8)],
            ...     talea=rmakers.Talea(
            ...         counts=[1, 1, 2],
            ...         denominator=8,
            ...         ),
            ...     tuplet_specifier=rmakers.TupletSpecifier(
            ...         denominator=abjad.Duration(1, 16),
            ...         ),
            ...     )

            >>> collections = [
            ...     [0, 2, 10, 18, 16],
            ...     [15, 20, 19, 9, 0],
            ...     [2, 10, 18, 16, 15],
            ...     [20, 19, 9, 0, 2],
            ...     [10, 18, 16, 15, 20],
            ...     [19, 9, 0, 2, 10],
            ...     ]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).beam.positions = (-6, -6)
            >>> abjad.override(staff).stem.direction = Down
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override Beam.positions = #'(-6 . -6)
                    \override Stem.direction = #down
                }
                {
                    {   % measure
                        \time 15/8
                        \times 4/6 {
                            c'16
                            [
                            d'16
                            bf'8
                            fs''16
                            e''16
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7 {
                            ef''8
                            [
                            af''16
                            g''16
                            a'8
                            c'16
                            ]
                        }
                        \times 4/7 {
                            d'16
                            [
                            bf'8
                            fs''16
                            e''16
                            ef''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            af''16
                            [
                            g''16
                            a'8
                            c'16
                            d'16
                            ]
                        }
                        \times 4/7 {
                            bf'8
                            [
                            fs''16
                            e''16
                            ef''8
                            af''16
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7 {
                            g''16
                            [
                            a'8
                            c'16
                            d'16
                            bf'8
                            ]
                        }
                    }   % measure
                }

        ..  container:: example

            Defaults to none:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker()
            >>> rhythm_maker.time_treatments is None
            True

        Set to time treatments or none.

        Time treatments defined equal to integers; positive multipliers;
        positive durations; and the strings ``'accel'`` and ``'rit'``.

        Returns tuple of time treatments or none.
        """
        return self._time_treatments

    @property
    def tuplet_specifier(self):
        r"""
        Gets tuplet specifier.

        ..  container:: example

            Does not simplify redudant tuplets by default:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     talea=rmakers.Talea(
            ...         counts=[3],
            ...         denominator=16,
            ...         ),
            ...     time_treatments=[-2],
            ...     )

            >>> collections = [[0, 2], [10, 18, 16], [15, 20], [19, 9, None]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).tuplet_bracket.staff_padding = 1.5
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.staff-padding = #1.5
                }
                {
                    {   % measure
                        \time 11/8
                        \times 2/3 {
                            c'8.
                            [
                            d'8.
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/9 {
                            bf'8.
                            [
                            fs''8.
                            e''8.
                            ]
                        }
                        \times 2/3 {
                            ef''8.
                            [
                            af''8.
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/9 {
                            g''8.
                            [
                            a'8.
                            ]
                            r8.
                        }
                    }   % measure
                }

        ..  container:: example

            Trivializes tuplets:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker(
            ...     talea=rmakers.Talea(
            ...         counts=[3],
            ...         denominator=16,
            ...         ),
            ...     time_treatments=[-2],
            ...     tuplet_specifier=rmakers.TupletSpecifier(
            ...         trivialize=True,
            ...         ),
            ...     )

            >>> collections = [[0, 2], [10, 18, 16], [15, 20], [19, 9, None]]
            >>> selections, state = rhythm_maker(collections)
            >>> lilypond_file = rhythm_maker.show(selections)
            >>> staff = lilypond_file[abjad.Staff]
            >>> abjad.override(staff).tuplet_bracket.staff_padding = 1.5
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.staff-padding = #1.5
                }
                {
                    {   % measure
                        \time 11/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            c'8
                            [
                            d'8
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/9 {
                            bf'8.
                            [
                            fs''8.
                            e''8.
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 1/1 {
                            ef''8
                            [
                            af''8
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/9 {
                            g''8.
                            [
                            a'8.
                            ]
                            r8.
                        }
                    }   % measure
                }

        ..  container:: example

            Defaults to none:

            >>> rhythm_maker = baca.PitchFirstRhythmMaker()
            >>> rhythm_maker.tuplet_specifier is None
            True

        Set to tuplet specifier or none.

        Returns tuplet specifier or none.
        """
        return rmakers.RhythmMaker.tuplet_specifier.fget(self)

    ### PUBLIC METHODS ###

    @staticmethod
    def show(selections, time_signatures=None):
        """
        Makes rhythm-maker-style LilyPond file for documentation examples.

        Returns LilyPond file.
        """
        return abjad.LilyPondFile.rhythm(
            selections,
            time_signatures=time_signatures,
            )

class PitchSpecifier(abjad.AbjadObject):
    r"""
    Pitch specifier.

    ..  container:: example

        Accumulates transposed pitch-classes to identity:

        >>> transposition = baca.pitch_class_segment().transpose(n=3)
        >>> expression = baca.sequence().map(transposition)
        >>> expression = baca.sequence().accumulate([transposition])
        >>> expression = expression.join()[0]
        >>> music_maker = baca.MusicMaker(
        ...     baca.PitchSpecifier(
        ...         expressions=[expression],
        ...         to_pitch_classes=True,
        ...         ),
        ...     )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker('Voice 1', collections)
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            c'16
                            [
                            d'16
                            bf'16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs'16
                            [
                            e'16
                            ef'16
                            af'16
                            g'16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'16
                        }
                        \scaleDurations #'(1 . 1) {
                            ef'16
                            [
                            f'16
                            cs'16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'16
                            [
                            g'16
                            fs'16
                            b'16
                            bf'16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            c'16
                        }
                        \scaleDurations #'(1 . 1) {
                            fs'16
                            [
                            af'16
                            e'16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            c'16
                            [
                            bf'16
                            a'16
                            d'16
                            cs'16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            ef'16
                        }
                        \scaleDurations #'(1 . 1) {
                            a'16
                            [
                            b'16
                            g'16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            ef'16
                            [
                            cs'16
                            c'16
                            f'16
                            e'16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs'16
                        }
                    }
                }
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_expressions',
        '_remove_duplicate_pitch_classes',
        '_remove_duplicates',
        '_to_pitch_classes',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        expressions=None,
        remove_duplicate_pitch_classes=None,
        remove_duplicates=None,
        to_pitch_classes=None,
        ):
        self._expressions = expressions
        if to_pitch_classes is not None:
            to_pitch_classes = bool(to_pitch_classes)
        self._remove_duplicate_pitch_classes = remove_duplicate_pitch_classes
        self._remove_duplicates = remove_duplicates
        self._to_pitch_classes = to_pitch_classes

    ### SPECIAL METHODS ###

    def __call__(self, collections=None):
        """
        Calls specifier on ``collections``.

        ..  container:: example

            Returns none when ``collections`` is none:

            >>> specifier = baca.PitchSpecifier()
            >>> specifier() is None
            True

        ..  container:: example

            Returns sequence of numbered pitch collections by default:

            >>> specifier = baca.PitchSpecifier()
            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> for collection in specifier(collections):
            ...     collection
            ...
            PitchSegment([0, 2, 10])
            PitchSegment([18, 16, 15, 20, 19])
            PitchSegment([9])

        Returns new collection list.
        """
        if collections is None:
            return
        collections = pitchclasses.CollectionList(collections=collections)
        if self.to_pitch_classes:
            collections = collections.to_pitch_classes()
        collections = self._remove_duplicates_(collections)
        collections = self._apply_expressions(collections)
        return collections

    def __repr__(self):
        """
        Gets interpreter representation of specifier.

        ..  container:: example

            >>> baca.PitchSpecifier()
            PitchSpecifier()

        Returns string.
        """
        return super().__repr__()

    ### PRIVATE METHODS ###

    def _apply_expressions(self, collections):
        sequence = classes.Sequence(items=collections)
        for expression in self.expressions or []:
            assert isinstance(expression, abjad.Expression), repr(expression)
            sequence = expression(sequence)
        return abjad.new(collections, collections=sequence)

    def _remove_duplicates_(self, collections):
        if self.remove_duplicates:
            collections = collections.remove_duplicates()
        if self.remove_duplicate_pitch_classes:
            collections = collections.remove_duplicate_pitch_classes()
        return collections

    def _to_pitch_tree(self, collections):
        item_class = None
        if self.to_pitch_classes:
            item_class = abjad.NumberedPitchClass
        return baca.PitchTree(
            item_class=item_class,
            items=collections,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def expressions(self):
        r"""
        Gets expressions.

        ..  container:: example

            Transposes pitch-classes:

            >>> transposition = baca.pitch_class_segment().transpose(n=3)
            >>> transposition = baca.sequence().map(transposition)
            >>> music_maker = baca.MusicMaker(
            ...     baca.PitchSpecifier(
            ...         expressions=[transposition],
            ...         to_pitch_classes=True,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                ef'16
                                [
                                f'16
                                cs'16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a'16
                                [
                                g'16
                                fs'16
                                b'16
                                bf'16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                c'16
                            }
                        }
                    }
                >>

        ..  container:: example

            Defaults to none:

            >>> specifier = baca.PitchSpecifier()
            >>> specifier.expressions is None
            True

        Set to expressions or none.

        Returns list of expressions or none.
        """
        if self._expressions is not None:
            return list(self._expressions)

    @property
    def remove_duplicate_pitch_classes(self):
        r"""
        Is true when specifier removes duplicate pitch-classes.

        ..  container:: example

            >>> specifier = baca.PitchSpecifier(
            ...     remove_duplicate_pitch_classes=True
            ...     )
            >>> collections = [[0, 2, 10], [18, 16, 15, 22, 19], [9]]
            >>> for collection in specifier(collections):
            ...     collection
            ...
            PitchSegment([0, 2, 10])
            PitchSegment([18, 16, 15, 19])
            PitchSegment([9])

        Returns true, false or none.
        """
        return self._remove_duplicate_pitch_classes

    @property
    def remove_duplicates(self):
        r"""
        Is true when specifier removes duplicates.

        ..  container:: example

            >>> specifier = baca.PitchSpecifier(
            ...     remove_duplicates=True
            ...     )
            >>> collections = [[0, 2, 10], [18, 16, 15, 10, 19], [9]]
            >>> for collection in specifier(collections):
            ...     collection
            ...
            PitchSegment([0, 2, 10])
            PitchSegment([18, 16, 15, 19])
            PitchSegment([9])

        Returns true, false or none.
        """
        return self._remove_duplicates

    @property
    def to_pitch_classes(self):
        r"""
        Is true when specifier changes pitches to pitch-classes.

        ..  note:: Applies prior to expressions.

        ..  container:: example

            Example figure:

            >>> music_maker = baca.MusicMaker()

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                g''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a'16
                            }
                        }
                    }
                >>

        ..  container:: example

            Changes pitches to pitch-classes:

            >>> music_maker = baca.MusicMaker(
            ...     baca.PitchSpecifier(
            ...         to_pitch_classes=True,
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                fs'16
                                [
                                e'16
                                ef'16
                                af'16
                                g'16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a'16
                            }
                        }
                    }
                >>

        ..  container:: example

            >>> specifier = baca.PitchSpecifier(
            ...     to_pitch_classes=True,
            ...     )
            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> for collection in specifier(collections):
            ...     collection
            ...
            PitchClassSegment([0, 2, 10])
            PitchClassSegment([6, 4, 3, 8, 7])
            PitchClassSegment([9])

        ..  container:: example

            >>> specifier = baca.PitchSpecifier(
            ...     to_pitch_classes=True,
            ...     )
            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> collections = baca.CollectionList(collections)
            >>> for collection in specifier(collections):
            ...     collection
            ...
            PitchClassSegment([0, 2, 10])
            PitchClassSegment([6, 4, 3, 8, 7])
            PitchClassSegment([9])

        ..  container:: example

            Defaults to none:

            >>> specifier = baca.PitchSpecifier()
            >>> specifier.to_pitch_classes is None
            True

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._to_pitch_classes

class RestAffixSpecifier(abjad.AbjadValueObject):
    r"""
    Rest affix specifier.

    ..  container:: example

        Works together with negative-valued talea:

        >>> music_maker = baca.MusicMaker()

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     collections,
        ...     baca.RestAffixSpecifier(
        ...         prefix=[2],
        ...         suffix=[3],
        ...         ),
        ...     counts=[1, -1],
        ...     time_treatments=[1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> staff = lilypond_file[abjad.Staff]
        >>> abjad.override(staff).tuplet_bracket.staff_padding = 4
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            \with
            {
                \override TupletBracket.staff-padding = #4
            }
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/8 {
                            r8
                            c'16
                            r16
                            d'16
                            r16
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 11/10 {
                            fs''16
                            r16
                            e''16
                            r16
                            ef''16
                            r16
                            af''16
                            r16
                            g''16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/5 {
                            a'16
                            r16
                            r8.
                        }
                    }
                }
            >>

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     collections,
        ...     baca.RestAffixSpecifier(
        ...         prefix=[2],
        ...         suffix=[3],
        ...         ),
        ...     counts=[-1, 1],
        ...     time_treatments=[1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> staff = lilypond_file[abjad.Staff]
        >>> abjad.override(staff).tuplet_bracket.staff_padding = 4
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            \with
            {
                \override TupletBracket.staff-padding = #4
            }
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/8 {
                            r8
                            r16
                            c'16
                            r16
                            d'16
                            r16
                            bf'16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 11/10 {
                            r16
                            fs''16
                            r16
                            e''16
                            r16
                            ef''16
                            r16
                            af''16
                            r16
                            g''16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/5 {
                            r16
                            a'16
                            r8.
                        }
                    }
                }
            >>

    ..  container:: example

        >>> baca.RestAffixSpecifier()
        RestAffixSpecifier()

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_pattern',
        '_prefix',
        '_skips_instead_of_rests',
        '_suffix',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        pattern=None,
        prefix=None,
        skips_instead_of_rests=None,
        suffix=None,
        ):
        if (pattern is not None and
            not isinstance(pattern, abjad.Pattern)):
            raise TypeError(f'pattern or none: {pattern!r}.')
        self._pattern = pattern
        if prefix is not None:
            assert isinstance(prefix, collections.Iterable), repr(prefix)
        self._prefix = prefix
        if skips_instead_of_rests is not None:
            skips_instead_of_rests = bool(skips_instead_of_rests)
        self._skips_instead_of_rests = skips_instead_of_rests
        if suffix is not None:
            assert isinstance(suffix, collections.Iterable), repr(suffix)
        self._suffix = suffix

    ### SPECIAL METHODS ###

    def __call__(self, collection_index=None, total_collections=None):
        r"""
        Calls command on ``collection_index`` and ``total_collections``.

        ..  container:: example

            With time treatments:

            >>> music_maker = baca.MusicMaker()

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     baca.RestAffixSpecifier(prefix=[1], suffix=[1]),
            ...     time_treatments=[-1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 3/4 {
                                r16
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \times 4/5 {
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                g''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a'16
                                r16
                            }
                        }
                    }
                >>

        Returns prefix, suffix pair.
        """
        if self.pattern is None:
            if collection_index == 0 and collection_index == total_collections - 1:
                return self.prefix, self.suffix
            if collection_index == 0:
                return self.prefix, None
            if collection_index == total_collections - 1:
                return None, self.suffix
        elif self.pattern.matches_index(collection_index, total_collections):
            return self.prefix, self.suffix
        return None, None

    ### PUBLIC PROPERTIES ###

    @property
    def pattern(self):
        r"""
        Gets pattern.

        ..  container:: example

            Treats entire figure when pattern is none:

            >>> music_maker = baca.MusicMaker()

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     baca.RestAffixSpecifier(
            ...         prefix=[1],
            ...         suffix=[2],
            ...         ),
            ...     time_treatments=[1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 5/4 {
                                r16
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/5 {
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                g''16
                                ]
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 4/3 {
                                a'16
                                r8
                            }
                        }
                    }
                >>

        ..  container:: example

            Treats entire figure (of only one segment) when pattern is none:

            >>> music_maker = baca.MusicMaker()

            >>> collections = [[18, 16, 15, 20, 19]]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     baca.RestAffixSpecifier(
            ...         prefix=[1],
            ...         suffix=[2],
            ...         ),
            ...     time_treatments=[1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/8 {
                                r16
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                g''16
                                ]
                                r8
                            }
                        }
                    }
                >>

        ..  container:: example

            Treats first segment and last segment in figure:

            >>> music_maker = baca.MusicMaker()

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     baca.RestAffixSpecifier(
            ...         pattern=abjad.Pattern(indices=[0, -1]),
            ...         prefix=[1],
            ...         suffix=[2],
            ...         ),
            ...     time_treatments=[1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/6 {
                                r16
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                                r8
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/5 {
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                g''16
                                ]
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 5/4 {
                                r16
                                a'16
                                r8
                            }
                        }
                    }
                >>

        ..  container:: example

            Treats every segment in figure:

            >>> music_maker = baca.MusicMaker()

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     baca.RestAffixSpecifier(
            ...         pattern=abjad.index_all(),
            ...         prefix=[1],
            ...         suffix=[2],
            ...         ),
            ...     time_treatments=[1],
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/6 {
                                r16
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                                r8
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/8 {
                                r16
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                g''16
                                ]
                                r8
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 5/4 {
                                r16
                                a'16
                                r8
                            }
                        }
                    }
                >>

        Set to pattern or none.

        Defaults to none.

        Returns pattern or none.
        """
        return self._pattern

    @property
    def prefix(self):
        r"""
        Gets prefix.

        ..  container:: example

            >>> music_maker = baca.MusicMaker()

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     baca.RestAffixSpecifier(prefix=[3]),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                r8.
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                g''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a'16
                            }
                        }
                    }
                >>

        Set to list of positive integers or none.

        Defaults to none.

        Returns list of positive integers or none.
        """
        return self._prefix

    @property
    def skips_instead_of_rests(self):
        """
        Is true when command makes skips instead of rests.

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        """
        return self._skips_instead_of_rests

    @property
    def suffix(self):
        r"""
        Gets suffix.

        ..  container:: example

            >>> music_maker = baca.MusicMaker()

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     baca.RestAffixSpecifier(suffix=[3]),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                g''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a'16
                                r8.
                            }
                        }
                    }
                >>

        Set to list of positive integers or none.

        Defaults to none.

        Returns list of positive integers or none.
        """
        return self._suffix

### FACTORY FUNCTIONS ###

def anchor(
    remote_voice_name: str,
    remote_selector: typings.Selector = None,
    local_selector: typings.Selector = None,
    ) -> AnchorSpecifier:
    """
    Anchors music in this figure (filtered by ``local_selector``) to
    start offset of ``remote_voice_name`` (filtered by
    ``remote_selector``).

    :param remote_voice_name: name of voice to which this music anchors.

    :param remote_seelctor: selector applied to remote voice.

    :param local_selector: selector applied to this music.
    """
    return AnchorSpecifier(
        local_selector=local_selector,
        remote_selector=remote_selector,
        remote_voice_name=remote_voice_name,
        )

def anchor_after(
    remote_voice_name: str,
    remote_selector: typings.Selector = None,
    local_selector: typings.Selector = None,
    ) -> AnchorSpecifier:
    """
    Anchors music in this figure (filtered by ``local_selector``) to
    stop offset of ``remote_voice_name`` (filtered by ``remote_selector``).

    :param remote_voice_name: name of voice to which this music anchors.

    :param remote_selector: selector applied to remote voice.

    :param local_selector: selector applied to this music.
    """
    return AnchorSpecifier(
        local_selector=local_selector,
        remote_selector=remote_selector,
        remote_voice_name=remote_voice_name,
        use_remote_stop_offset=True,
        )

def anchor_to_figure(figure_name: str) -> AnchorSpecifier:
    """
    Anchors music in this figure to start of ``figure_name``.

    :param figure_name: figure name.
    """
    return AnchorSpecifier(
        figure_name=figure_name,
        )

def coat(pitch: typing.Union[int, str, abjad.Pitch]) -> Coat:
    r"""
    Coats ``pitch``.

    ..  container:: example

        Coats pitches:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     3 * [[0, 2, 10]],
        ...     baca.imbricate(
        ...         'Voice 2',
        ...         [baca.coat(0), baca.coat(2), 10, 0, 2],
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \times 4/5 {
                            r8
                            c'16
                            [
                            d'16
                            bf'16
                            ]
                        }
                        \times 2/3 {
                            c'16
                            [
                            d'16
                            bf'16
                            ]
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7 {
                            c'16
                            [
                            d'16
                            bf'16
                            ]
                            r4
                        }
                    }
                }
                \context Voice = "Voice 2"
                {
                    \voiceTwo
                    {
                        \override TupletBracket.stencil = ##f
                        \override TupletNumber.stencil = ##f
                        \times 4/5 {
                            s8
                            s16
                            s16
                            bf'16
                        }
                        \times 2/3 {
                            c'16
                            [
                            d'16
                            ]
                            s16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 6/7 {
                            s16
                            s16
                            s16
                            s4
                        }
                        \revert TupletBracket.stencil
                        \revert TupletNumber.stencil
                    }
                }
            >>

    """
    return Coat(pitch)

def imbricate(
    voice_name: str,
    segment: typing.List,
    *specifiers: typing.Any,
    allow_unused_pitches: bool = None,
    by_pitch_class: bool = None,
    extend_beam: bool = None,
    hocket: bool = None,
    selector: typings.Selector = None,
    truncate_ties: bool = None
    ):
    r"""
    Imbricates ``segment`` in voice with ``voice_name``.

    ..  container:: example

        Imbricates segment:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.imbricate('Voice 2', [10, 20, 19]),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
                        }
                    }
                }
                \context Voice = "Voice 2"
                {
                    \voiceTwo
                    {
                        \override TupletBracket.stencil = ##f
                        \override TupletNumber.stencil = ##f
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            s8
                            s16
                            s16
                            bf'4
                            ~
                            bf'16
                            s16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            s16
                            s16
                            s4
                            s16
                            s16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            s16
                            s4
                        }
                        \revert TupletBracket.stencil
                        \revert TupletNumber.stencil
                    }
                }
            >>

    """
    return ImbricationCommand(
        voice_name,
        segment,
        *specifiers,
        allow_unused_pitches=allow_unused_pitches,
        by_pitch_class=by_pitch_class,
        extend_beam=extend_beam,
        hocket=hocket,
        selector=selector,
        truncate_ties=truncate_ties,
        )

def nest(
    time_treatments: typing.Iterable = None,
    ) -> NestingCommand:
    r"""
    Nests music.

    ..  container:: example

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.nest('+4/16'),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 13/11 {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                           %! OVERRIDE_COMMAND_1
                                r8
                                c'16
                                [
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                [
                                e''16
                                ]
                                ef''4
                                ~
                                ef''16
                                r16
                                af''16
                                [
                                g''16
                                ]
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding                                  %! OVERRIDE_COMMAND_2
                            }
                        }
                    }
                }
            >>

    """
    if not isinstance(time_treatments, list):
        time_treatments = [time_treatments]
    return NestingCommand(
        lmr_specifier=None,
        time_treatments=time_treatments,
        )

def rests_after(counts: typing.Iterable[int]) -> RestAffixSpecifier:
    r"""
    Makes rests after music.

    ..  container:: example

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_after([2]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/8 {
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 2/3 {
                            a'16
                            r8
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
                        }
                    }
                }
            >>

    """
    return RestAffixSpecifier(
        suffix=counts,
        )

def rests_around(
    prefix: typing.List[int],
    suffix: typing.List[int],
    ) -> RestAffixSpecifier:
    r"""
    Makes rests around music.

    ..  container:: example

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [2]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 2/3 {
                            a'16
                            r8
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
                        }
                    }
                }
            >>

    """
    return RestAffixSpecifier(
        prefix=prefix,
        suffix=suffix,
        )

def rests_before(counts: typing.List[int]) -> RestAffixSpecifier:
    r"""
    Makes rests before music.

    ..  container:: example

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_before([2]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'16
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
                        }
                    }
                }
            >>

    """
    return RestAffixSpecifier(
        prefix=counts,
        )

def resume() -> AnchorSpecifier:
    """
    Resumes music at next offset across all voices in score.
    """
    return AnchorSpecifier()

def resume_after(remote_voice_name) -> AnchorSpecifier:
    """
    Resumes music after remote selection.
    """
    return AnchorSpecifier(
        remote_selector='baca.leaf(-1)',
        remote_voice_name=remote_voice_name,
        use_remote_stop_offset=True,
        )

def skips_after(counts: typing.List[int]) -> RestAffixSpecifier:
    r"""
    Makes skips after music.

    ..  container:: example

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.skips_after([2]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/8 {
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 2/3 {
                            a'16
                            s8
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
                        }
                    }
                }
            >>

    """
    return RestAffixSpecifier(
        skips_instead_of_rests=True,
        suffix=counts,
        )

def skips_around(
    prefix: typing.List[int],
    suffix: typing.List[int],
    ) -> RestAffixSpecifier:
    r"""
    Makes skips around music.

    ..  container:: example

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.skips_around([2], [2]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
                            s8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 2/3 {
                            a'16
                            s8
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
                        }
                    }
                }
            >>

    """
    return RestAffixSpecifier(
        prefix=prefix,
        skips_instead_of_rests=True,
        suffix=suffix,
        )

def skips_before(
    counts: typing.List[int],
    ) -> RestAffixSpecifier:
    r"""
    Makes skips before music.

    ..  container:: example

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.skips_before([2]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OVERRIDE_COMMAND_1
                            s8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'16
                            \revert TupletBracket.staff-padding                                      %! OVERRIDE_COMMAND_2
                        }
                    }
                }
            >>

    """
    return RestAffixSpecifier(
        prefix=counts,
        skips_instead_of_rests=True,
        )
