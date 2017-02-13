# -*- coding: utf-8 -*-
import abjad
import baca


class RegisterSpecifier(abjad.abctools.AbjadObject):
    r"""Register specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        With segment-maker:

        ::

            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.select.stages(1)),
            ...     [
            ...         baca.pitches('G4 G+4 G#4 G#+4 A~4 Ab4 Ab~4'),
            ...         baca.make_even_run_rhythm_specifier(),
            ...         baca.tools.RegisterSpecifier(
            ...             registration=abjad.Registration(
            ...                 [('[A0, C8]', 15)],
            ...                 ),
            ...             ),
            ...         ],
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, segment_metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin
                \context TimeSignatureContext = "Time Signature Context" <<
                    \context TimeSignatureContextMultimeasureRests = "Time Signature Context Multimeasure Rests" {
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                    }
                    \context TimeSignatureContextSkips = "Time Signature Context Skips" {
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \tag violin
                    \context ViolinMusicStaff = "Violin Music Staff" {
                        \clef "treble"
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            {
                                g''8 [
                                gqs''8
                                gs''8
                                gtqs''8 ]
                            }
                            {
                                aqf''8 [
                                af''8
                                atqf''8 ]
                            }
                            {
                                g''8 [
                                gqs''8
                                gs''8
                                gtqs''8 ]
                            }
                            {
                                aqf''8 [
                                af''8
                                atqf''8 ]
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        With figure-maker:

        ::

            >>> figure_maker = baca.tools.FigureMaker()

        ::

            >>> contribution = figure_maker(
            ...     'Voice 1',
            ...     [[10, 12, 14], [10, 12, 14], [10, 12, 14]],
            ...     baca.tools.RegisterSpecifier(
            ...         registration=abjad.Registration(
            ...             [('[A0, C8]', 15)],
            ...             ),
            ...         ),
            ...     )
            >>> lilypond_file = figure_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            bf''16 [
                            c'''16
                            d'''16 ]
                        }
                        {
                            bf''16 [
                            c'''16
                            d'''16 ]
                        }
                        {
                            bf''16 [
                            c'''16
                            d'''16 ]
                        }
                    }
                }
            >>

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_pattern',
        '_registration',
        )

    ### INITIALIZER ###

    def __init__(self, pattern=None, registration=None):
        if pattern is not None:
            assert isinstance(pattern, abjad.Pattern), repr(pattern)
        self._pattern = pattern
        if registration is not None:
            prototype = abjad.Registration
            assert isinstance(registration, prototype), repr(registration)
        self._registration = registration

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls registration specifier on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        if isinstance(argument, baca.tools.ScopedSpecifier):
            selections = [argument]
        if isinstance(argument, abjad.Selection):
            selections = [argument]
        else:
            assert isinstance(argument, list), repr(argument)
            assert isinstance(argument[0], abjad.Selection), repr(argument)
            selections = argument
        pattern = self.pattern or abjad.select_all()
        selections = pattern.get_matching_items(selections)
        for selection in selections:
            for logical_tie in abjad.iterate(selection).by_logical_tie(
                pitched=True,
                with_grace_notes=True,
                ):
                for note in logical_tie:
                    written_pitch = self.registration([note.written_pitch])
                    self._set_pitch(note, written_pitch)

    ### PRIVATE METHODS ###

    @staticmethod
    def _set_pitch(note, written_pitch):
        note.written_pitch = written_pitch
        abjad.detach('not yet registered', note)

    ### PUBLIC PROPERTIES ###

    @property
    def pattern(self):
        r'''Gets pattern.

        ..  container:: example

            First stage only:

            ::

                >>> figure_maker = baca.tools.FigureMaker()

            ::

                >>> contribution = figure_maker(
                ...     'Voice 1',
                ...     [[10, 12, 14], [10, 12, 14], [10, 12, 14]],
                ...     baca.tools.RegisterSpecifier(
                ...         pattern=abjad.select_first(),
                ...         registration=abjad.Registration(
                ...             [('[A0, C8]', 0)],
                ...             ),
                ...         ),
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                bf'16 [
                                c'16
                                d'16 ]
                            }
                            {
                                bf'16 [
                                c''16
                                d''16 ]
                            }
                            {
                                bf'16 [
                                c''16
                                d''16 ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Last stage only:

            ::

                >>> figure_maker = baca.tools.FigureMaker()

            ::

                >>> contribution = figure_maker(
                ...     'Voice 1',
                ...     [[10, 12, 14], [10, 12, 14], [10, 12, 14]],
                ...     baca.tools.RegisterSpecifier(
                ...         pattern=abjad.select_last(),
                ...         registration=abjad.Registration(
                ...             [('[A0, C8]', 0)],
                ...             ),
                ...         ),
                ...     )
                >>> lilypond_file = figure_maker.show(contribution)
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                bf'16 [
                                c''16
                                d''16 ]
                            }
                            {
                                bf'16 [
                                c''16
                                d''16 ]
                            }
                            {
                                bf'16 [
                                c'16
                                d'16 ]
                            }
                        }
                    }
                >>

        Set to pattern or none.

        Returns pattern or none.
        '''
        return self._pattern

    @property
    def registration(self):
        r'''Gets registration.

        ..  container:: example

            ::

                >>> specifier = baca.tools.RegisterSpecifier(
                ...     registration=abjad.Registration(
                ...         [('[A0, C4)', 15), ('[C4, C8)', 27)],
                ...         ),
                ...     )

            ::

                >>> specifier.registration
                Registration([('[A0, C4)', 15), ('[C4, C8)', 27)])

        Set to registration or none.

        Returns registration or none.
        '''
        return self._registration
