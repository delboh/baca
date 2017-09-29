import abjad


class ClusterCommand(abjad.AbjadObject):
    r"""Cluster command.

    :    ..  container:: example

        With music-maker:

        ::

            >>> music_maker = baca.MusicMaker(
            ...     baca.ClusterCommand(
            ...         widths=[3, 4],
            ...         ),
            ...     )

        ::

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <c' e' g'>16 [
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <d' f' a' c''>16
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <bf' d'' f''>16 ]
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                        }
                        {
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <fs'' a'' c''' e'''>16 [
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <e'' g'' b''>16
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <ef'' g'' b'' d'''>16
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <af'' c''' e'''>16
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <g'' b'' d''' f'''>16 ]
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                        }
                        {
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <a' c'' e''>16
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                        }
                    }
                }
            >>

    ..  container:: example

        With segment-maker:

        Clusters widths alternating 3 and 4:

        ::

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_commands(
            ...     'vn',
            ...     baca.select_stages(1),
            ...     baca.pitches('E4'),
            ...     baca.messiaen_notes(),
            ...     baca.ClusterCommand(
            ...         widths=[3, 4],
            ...         ),
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin
                \context GlobalContext = "Global Context" <<
                    \context GlobalRests = "Global Rests" {
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
                    \context GlobalSkips = "Global Skips" {
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
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            \set ViolinMusicStaff.instrumentName = \markup { Violin }
                            \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                            \clef "treble"
                            <e' g' b'>2
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <e' g' b' d''>4.
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <e' g' b'>2
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                                \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <e' g' b' d''>4.
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                            \bar "|"
                        }
                    }
                >>
            >>

    """

    ### CLASS VARIABLES ##

    __documentation_section__ = 'Commands'

    __slots__ = (
        '_hide_flat_markup',
        '_hide_natural_markup',
        '_start_pitch',
        '_widths',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        hide_flat_markup=None,
        hide_natural_markup=None,
        start_pitch=None,
        widths=None,
        ):
        assert isinstance(hide_flat_markup, (bool, type(None)))
        self._hide_flat_markup = hide_flat_markup
        assert isinstance(hide_natural_markup, (bool, type(None)))
        self._hide_natural_markup = hide_natural_markup
        if start_pitch is not None:
            start_pitch = abjad.NamedPitch(start_pitch)
        self._start_pitch = start_pitch
        if widths is not None:
            assert abjad.mathtools.all_are_nonnegative_integers(widths)
        self._widths = widths

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        if self.widths is None:
            return
        widths = abjad.CyclicTuple(self.widths)
        logical_ties = abjad.iterate(argument).by_logical_tie()
        logical_ties = list(logical_ties)
        first_note = logical_ties[0].head
        root = abjad.inspect(first_note).get_parentage().root
        with abjad.ForbidUpdate(component=root):
            for index, logical_tie in enumerate(logical_ties):
                width = widths[index]
                for note in logical_tie:
                    self._make_cluster(note, width)

    ### PRIVATE METHODS ###

    def _make_cluster(self, note, width):
        if not width:
            return
        if self.start_pitch is not None:
            pitches = self._make_pitches(self.start_pitch, width)
        else:
            start_pitch = note.written_pitch
            pitches = self._make_pitches(start_pitch, width)
        chord = abjad.Chord(pitches, note.written_duration)
        abjad.mutate(note).replace(chord)
        indicator = abjad.KeyCluster(
            include_black_keys=not self.hide_flat_markup,
            include_white_keys=not self.hide_natural_markup,
            )
        abjad.attach(indicator, chord)

    def _make_pitches(self, start_pitch, width):
        pitches = [start_pitch]
        for i in range(width - 1):
            pitch = pitches[-1] + abjad.NamedInterval('M3')
            pitch = abjad.NamedPitch(pitch._get_diatonic_pitch_name())
            assert pitch.accidental.name == 'natural'
            pitches.append(pitch)
        return pitches

    def _mutates_score(self):
        return True

    ### PUBLIC PROPERTIES ###

    @property
    def hide_flat_markup(self):
        r'''Is true when cluster hides flat markup.

        ..  container:: example

            Hides flat markup:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.pitches('E4'),
                ...     baca.messiaen_notes(),
                ...     baca.ClusterCommand(
                ...         hide_flat_markup=True,
                ...         widths=[3],
                ...         ),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
                                <e' g' b'>2
                                    ^ \markup {
                                        \center-align
                                            \natural
                                        }
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b'>4.
                                    ^ \markup {
                                        \center-align
                                            \natural
                                        }
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b'>2
                                    ^ \markup {
                                        \center-align
                                            \natural
                                        }
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b'>4.
                                    ^ \markup {
                                        \center-align
                                            \natural
                                        }
                                \bar "|"
                            }
                        }
                    >>
                >>

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._hide_flat_markup

    @property
    def hide_natural_markup(self):
        r'''Is true when cluster hides natural markup.

        ..  container:: example

            Hides natural markup:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.pitches('E4'),
                ...     baca.messiaen_notes(),
                ...     baca.ClusterCommand(
                ...         hide_natural_markup=True,
                ...         widths=[3],
                ...         ),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
                                <e' g' b'>2
                                    ^ \markup {
                                        \center-align
                                            \flat
                                        }
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b'>4.
                                    ^ \markup {
                                        \center-align
                                            \flat
                                        }
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b'>2
                                    ^ \markup {
                                        \center-align
                                            \flat
                                        }
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b'>4.
                                    ^ \markup {
                                        \center-align
                                            \flat
                                        }
                                \bar "|"
                            }
                        }
                    >>
                >>

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._hide_natural_markup

    @property
    def start_pitch(self):
        r'''Gets start pitch of cluster.

        ..  container:: example

            Takes start pitch from input notes:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.messiaen_notes(),
                ...     baca.pitches('C4 D4 E4 F4'),
                ...     baca.ClusterCommand(
                ...         widths=[3],
                ...         ),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
                                <c' e' g'>2
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <d' f' a'>4.
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b'>2
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <f' a' c''>4.
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                                \bar "|"
                            }
                        }
                    >>
                >>

        ..  container:: example

            Sets start pitch explicitly:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.messiaen_notes(),
                ...     baca.pitches('C4 D4 E4 F4'),
                ...     baca.ClusterCommand(
                ...         start_pitch='G4',
                ...         widths=[3],
                ...         ),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
                                <g' b' d''>2
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <g' b' d''>4.
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <g' b' d''>2
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <g' b' d''>4.
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                                \bar "|"
                            }
                        }
                    >>
                >>

        Set to named pitch or none.

        Returns named pitch or none.
        '''
        return self._start_pitch

    @property
    def widths(self):
        r'''Gets widths.

        ..  container:: example

            Increasing widths:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.pitches('E4'),
                ...     baca.messiaen_notes(),
                ...     baca.ClusterCommand(
                ...         widths=[0, 1, 2, 3],
                ...         ),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
                                e'2
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e'>4.
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g'>2
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b'>4.
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                                \bar "|"
                            }
                        }
                    >>
                >>

        ..  container:: example

            Patterned widths:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.messiaen_notes(),
                ...     baca.pitches('E4'),
                ...     baca.ClusterCommand(
                ...         widths=[0, 3],
                ...         ),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
                                e'2
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b'>4.
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                                e'2
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                    \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g' b'>4.
                                    ^ \markup {
                                        \center-align
                                            \concat
                                                {
                                                    \natural
                                                    \flat
                                                }
                                        }
                                \bar "|"
                            }
                        }
                    >>
                >>

        ..  container:: example

            Leaves notes and chords unchanged:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.messiaen_notes(),
                ...     baca.pitches('E4', allow_repeat_pitches=True),
                ...     baca.ClusterCommand(
                ...         widths=None,
                ...         ),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
                                e'2
                                e'4.
                                e'2
                                e'4.
                                \bar "|"
                            }
                        }
                    >>
                >>

        Inteprets positive integers as widths in thirds.

        Interprets zero to mean input note or chord is left unchanged.

        Set to nonnegative integers or none.

        Returns nonnegative integers or none.
        '''
        return self._widths
