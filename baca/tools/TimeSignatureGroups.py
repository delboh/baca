# -*- coding: utf-8 -*-
import abjad


class TimeSignatureGroups(abjad.abctools.AbjadObject):
    r'''Time signature groups.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Time signature groups:

        ::

            >>> group_1 = [(3, 8), (3, 16), (3, 16)]
            >>> group_1 = [abjad.TimeSignature(_) for _ in group_1]
            >>> group_2 = [(5, 8), (5, 16), (5, 16), (5, 16)]
            >>> group_2 = [abjad.TimeSignature(_) for _ in group_2]
            >>> groups = [group_1, group_2]
            >>> groups = baca.tools.TimeSignatureGroups(groups)

        ::

            >>> f(groups)
            baca.tools.TimeSignatureGroups(
                [
                    [
                        indicatortools.TimeSignature((3, 8)),
                        indicatortools.TimeSignature((3, 16)),
                        indicatortools.TimeSignature((3, 16)),
                        ],
                    [
                        indicatortools.TimeSignature((5, 8)),
                        indicatortools.TimeSignature((5, 16)),
                        indicatortools.TimeSignature((5, 16)),
                        indicatortools.TimeSignature((5, 16)),
                        ],
                    ]
                )

        ::

            >>> show(groups) # doctest: +SKIP

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        '_groups',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, groups):
        prototype = abjad.indicatortools.TimeSignature
        for group in groups:
            assert all(isinstance(_, prototype) for _ in group), repr(group)
        self._groups = groups

    ### SPECIAL METHODS ###

    def __illustrate__(self):
        r'''Illustrates time signature groups.

        ::

            >>> show(groups) # doctest: +SKIP

        ..  doctest::

            >>> lilypond_file = groups.__illustrate__()
            >>> f(lilypond_file[abjad.Score])
            \new Score \with {
                proportionalNotationDuration = #(ly:make-moment 1 8)
            } <<
                \new Staff \with {
                    \consists Horizontal_bracket_engraver
                    \override Clef.stencil = ##f
                    \override HorizontalBracket.bracket-flare = #'(0 . 0)
                    \override HorizontalBracket.direction = #up
                    \override HorizontalBracket.extra-offset = #'(-4 . 0)
                    \override HorizontalBracket.staff-padding = #2.5
                    \override Rest.transparent = ##t
                    \override TextScript.extra-offset = #'(-4 . 0)
                    \override TextScript.staff-padding = #4.5
                } {
                    {
                        \time 3/8
                        r1 * 3/8 \startGroup
                            ^ \markup {
                                \circle
                                    \smaller
                                        0
                                }
                    }
                    {
                        \time 3/16
                        r1 * 3/16
                    }
                    {
                        \time 3/16
                        r1 * 3/16 \stopGroup
                    }
                    {
                        \time 5/8
                        r1 * 5/8 \startGroup
                            ^ \markup {
                                \circle
                                    \smaller
                                        1
                                }
                    }
                    {
                        \time 5/16
                        r1 * 5/16
                    }
                    {
                        \time 5/16
                        r1 * 5/16
                    }
                    {
                        \time 5/16
                        r1 * 5/16 \stopGroup
                    }
                }
            >>

        Returns LilyPond file.
        ''' 
        staff = abjad.scoretools.Staff()
        staff.consists_commands.append('Horizontal_bracket_engraver')
        for group_index, group in enumerate(self.groups):
            measure_group = self._make_measure_group(group)
            spanner = abjad.spannertools.HorizontalBracketSpanner()
            leaves = list(abjad.iterate(measure_group).by_leaf())
            abjad.attach(spanner, leaves)
            staff.extend(measure_group)
            markup = abjad.markuptools.Markup(group_index, direction=Up)
            markup = markup.smaller()
            markup = markup.circle()
            abjad.attach(markup, measure_group[0])
        slide = -4
        abjad.override(staff).clef.stencil = False
        abjad.override(staff).horizontal_bracket.bracket_flare = (0, 0)
        abjad.override(staff).horizontal_bracket.direction = Up
        abjad.override(staff).horizontal_bracket.extra_offset = (slide, 0)
        abjad.override(staff).horizontal_bracket.staff_padding = 2.5
        abjad.override(staff).rest.transparent = True
        abjad.override(staff).text_script.extra_offset = (slide, 0)
        abjad.override(staff).text_script.staff_padding = 4.5
        score = abjad.scoretools.Score([staff])
        moment = abjad.schemetools.SchemeMoment((1, 8))
        abjad.set_(score).proportional_notation_duration = moment
        lilypond_file = abjad.lilypondfiletools.LilyPondFile.new(score)
        lilypond_file.header_block.tagline = abjad.markuptools.Markup.null()
        return lilypond_file

    ### PRIVATE METHODS ###

    def _make_measure_group(self, group):
        measure_group = []
        for time_signature in group:
            multiplier = abjad.durationtools.Multiplier(
                time_signature.duration)
            rest = abjad.scoretools.Rest(abjad.durationtools.Duration(1))
            abjad.attach(multiplier, rest)
            measure = abjad.scoretools.Measure(time_signature, [rest])
            measure.always_format_time_signature = True
            measure_group.append(measure)
        return measure_group

    ### PUBLIC PROPERTIES ###

    @property
    def groups(self):
        r'''Gets groups.

        Returns list of time signature lists.
        '''
        return self._groups
