# -*- coding: utf-8 -*-
import abjad


class PitchArrayInventory(abjad.datastructuretools.TypedList):
    r'''Pitch array inventory.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        A pitch array inventory:

        ::

            >>> array_1 = baca.tools.PitchArray([
            ...   [1, (2, 1), ([-2, -1.5], 2)],
            ...   [(7, 2), (6, 1), 1]])

        ::

            >>> array_2 = baca.tools.PitchArray([
            ...   [1, 1, 1],
            ...   [1, 1, 1]])

        ::

            >>> arrays = [array_1, array_2]
            >>> inventory = baca.tools.PitchArrayInventory(arrays)

        ::

            >>> f(inventory)
            baca.tools.PitchArrayInventory(
                [
                    baca.tools.PitchArray(
                        rows=(
                            baca.tools.PitchArrayRow(
                                cells=(
                                    baca.tools.PitchArrayCell(
                                        width=1,
                                        ),
                                    baca.tools.PitchArrayCell(
                                        pitches=[
                                            pitchtools.NamedPitch("d'"),
                                            ],
                                        width=1,
                                        ),
                                    baca.tools.PitchArrayCell(
                                        pitches=[
                                            pitchtools.NamedPitch('bf'),
                                            pitchtools.NamedPitch('bqf'),
                                            ],
                                        width=2,
                                        ),
                                    ),
                                ),
                            baca.tools.PitchArrayRow(
                                cells=(
                                    baca.tools.PitchArrayCell(
                                        pitches=[
                                            pitchtools.NamedPitch("g'"),
                                            ],
                                        width=2,
                                        ),
                                    baca.tools.PitchArrayCell(
                                        pitches=[
                                            pitchtools.NamedPitch("fs'"),
                                            ],
                                        width=1,
                                        ),
                                    baca.tools.PitchArrayCell(
                                        width=1,
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    baca.tools.PitchArray(
                        rows=(
                            baca.tools.PitchArrayRow(
                                cells=(
                                    baca.tools.PitchArrayCell(
                                        width=1,
                                        ),
                                    baca.tools.PitchArrayCell(
                                        width=1,
                                        ),
                                    baca.tools.PitchArrayCell(
                                        width=1,
                                        ),
                                    ),
                                ),
                            baca.tools.PitchArrayRow(
                                cells=(
                                    baca.tools.PitchArrayCell(
                                        width=1,
                                        ),
                                    baca.tools.PitchArrayCell(
                                        width=1,
                                        ),
                                    baca.tools.PitchArrayCell(
                                        width=1,
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ]
                )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        )

    _publish_storage_format = True

    ### PUBLIC METHODS ###

    def to_score(self):
        r'''Makes score from pitch arrays in inventory.

        ..  container:: example

            ::

                >>> array_1 = baca.tools.PitchArray([
                ...   [1, (2, 1), ([-2, -1.5], 2)],
                ...   [(7, 2), (6, 1), 1]])

            ::

                >>> array_2 = baca.tools.PitchArray([
                ...   [1, 1, 1],
                ...   [1, 1, 1]])

            ::

                >>> arrays = [array_1, array_2]
                >>> inventory = baca.tools.PitchArrayInventory(arrays)

            ::

                >>> score = inventory.to_score()
                >>> show(score) # doctest: +SKIP

            ..  doctest::

                >>> f(score)
                \new Score <<
                    \new StaffGroup <<
                        \new Staff {
                            {
                                \time 4/8
                                r8
                                d'8
                                <bf bqf>4
                            }
                            {
                                \time 3/8
                                r8
                                r8
                                r8
                            }
                        }
                        \new Staff {
                            {
                                \time 4/8
                                g'4
                                fs'8
                                r8
                            }
                            {
                                \time 3/8
                                r8
                                r8
                                r8
                            }
                        }
                    >>
                >>

        Creates one staff per pitch-array row.

        Returns score.
        '''
        score = abjad.Score([])
        staff_group = abjad.StaffGroup([])
        score.append(staff_group)
        number_staves = self[0].depth
        staves = number_staves * abjad.Staff([])
        staff_group.extend(staves)
        for pitch_array in self:
            measures = pitch_array.to_measures()
            for staff, measure in zip(staves, measures):
                staff.append(measure)
        return score
