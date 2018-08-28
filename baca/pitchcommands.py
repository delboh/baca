import abjad
import collections
import numbers
import typing
from . import classes
from . import pitchclasses
from . import scoping
from . import typings


### CLASSES ###

class AccidentalAdjustmentCommand(scoping.Command):
    r"""
    Accidental adjustment command.

    ..  container:: example

        >>> baca.AccidentalAdjustmentCommand()
        AccidentalAdjustmentCommand(selector=baca.pleaf(0), tags=[])

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.force_accidental(selector=baca.pleaves()[:2]),
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.pitches('E4 F4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            e'!2                                                                     %! baca_make_notes
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            f'!4.                                                                    %! baca_make_notes
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            e'2                                                                      %! baca_make_notes
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            f'4.                                                                     %! baca_make_notes
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_cautionary',
        '_forced',
        '_parenthesized',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        cautionary: bool = None,
        forced: bool = None,
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        parenthesized: bool = None,
        scope: scoping.ScopeTyping = None,
        selector: typings.Selector = 'baca.pleaf(0)',
        tags: typing.List[typing.Union[str, abjad.Tag, None]] = None,
        ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
            tags=tags,
            )
        if cautionary is not None:
            cautionary = bool(cautionary)
        self._cautionary = cautionary
        if forced is not None:
            forced = bool(forced)
        self._forced = forced
        if parenthesized is not None:
            parenthesized = bool(parenthesized)
        self._parenthesized = parenthesized

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Inserts ``selector`` output in container.
        """
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        if self.tag:
            if not self.tag.only_edition() and not self.tag.not_editions():
                raise Exception(f'tag must have edition: {self.tag!r}.')
            alternative_tag = self.tag.prepend('AccidentalAdjustmentCommand')
            primary_tag = alternative_tag.invert_edition_tags()
        for pleaf in classes.Selection(argument).pleaves():
            if isinstance(pleaf, abjad.Note):
                note_heads = [pleaf.note_head]
            else:
                assert isinstance(pleaf, abjad.Chord)
                note_heads = pleaf.note_heads
            for note_head in note_heads:
                assert note_head is not None
                if not self.tag:
                    if self.cautionary:
                        note_head.is_cautionary = True
                    if self.forced:
                        note_head.is_forced = True
                    if self.parenthesized:
                        note_head.is_parenthesized = True
                else:
                    alternative = abjad.new(note_head)
                    if self.cautionary:
                        alternative.is_cautionary = True
                    if self.forced:
                        alternative.is_forced = True
                    if self.parenthesized:
                        alternative.is_parenthesized = True
                    note_head.alternative = (
                        alternative,
                        str(alternative_tag),
                        str(primary_tag),
                        )

    ### PUBLIC PROPERTIES ###

    @property
    def cautionary(self) -> typing.Optional[bool]:
        """
        Is true when command makes accidentals cautionary.
        """
        return self._cautionary

    @property
    def forced(self) -> typing.Optional[bool]:
        """
        Is true when command forces accidentals.
        """
        return self._forced

    @property
    def parenthesized(self) -> typing.Optional[bool]:
        """
        Is true when command parenthesizes accidentals.
        """
        return self._parenthesized

class ClusterCommand(scoping.Command):
    r"""
    Cluster command.

    ..  container:: example

        With music-maker:

        >>> music_maker = baca.MusicMaker(baca.clusters([3, 4]))

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker('Voice_1', collections)
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                            	\filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <c' e' g'>16
                            ^ \markup {
                                \center-align
                                    \concat
                                        {
                                            \natural
                                            \flat
                                        }
                                }
                            [
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
                            <bf' d'' f''>16
                            ^ \markup {
                                \center-align
                                    \concat
                                        {
                                            \natural
                                            \flat
                                        }
                                }
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                            	\filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <fs'' a'' c''' e'''>16
                            ^ \markup {
                                \center-align
                                    \concat
                                        {
                                            \natural
                                            \flat
                                        }
                                }
                            [
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
                            <g'' b'' d''' f'''>16
                            ^ \markup {
                                \center-align
                                    \concat
                                        {
                                            \natural
                                            \flat
                                        }
                                }
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
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

        In tuplet 1:

        >>> music_maker = baca.MusicMaker(
        ...     baca.clusters(
        ...         [3, 4],
        ...         selector=baca.tuplets()[1:2].plts().group(),
        ...         ),
        ...     )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker('Voice_1', collections)
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
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
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                            	\filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <fs'' a'' c'''>16
                            ^ \markup {
                                \center-align
                                    \concat
                                        {
                                            \natural
                                            \flat
                                        }
                                }
                            [
                            \once \override Accidental.stencil = ##f
                            \once \override AccidentalCautionary.stencil = ##f
                            \once \override Arpeggio.X-offset = #-2
                            \once \override NoteHead.stencil = #ly:text-interface::print
                            \once \override NoteHead.text = \markup {
                            	\filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                            }
                            <e'' g'' b'' d'''>16
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
                            <ef'' g'' b''>16
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
                            <af'' c''' e''' g'''>16
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
                            <g'' b'' d'''>16
                            ^ \markup {
                                \center-align
                                    \concat
                                        {
                                            \natural
                                            \flat
                                        }
                                }
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'16
                        }
                    }
                }
            >>

    ..  container:: example

        PLT -1:

        >>> music_maker = baca.MusicMaker(
        ...     baca.clusters([3, 4], selector=baca.plt(-1)),
        ...     )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker('Voice_1', collections)
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
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

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.clusters([3, 4], start_pitch='E4'),
        ...     baca.make_notes(repeat_ties=True),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
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
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
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
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
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
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
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
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    """

    ### CLASS VARIABLES ##

    __slots__ = (
        '_hide_flat_markup',
        '_start_pitch',
        '_widths',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        hide_flat_markup=None,
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        scope: scoping.ScopeTyping = None,
        selector='baca.plts()',
        start_pitch=None,
        widths=None,
        ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
            )
        assert isinstance(hide_flat_markup, (bool, type(None)))
        self._hide_flat_markup = hide_flat_markup
        if start_pitch is not None:
            start_pitch = abjad.NamedPitch(start_pitch)
        self._start_pitch = start_pitch
        assert abjad.mathtools.all_are_nonnegative_integers(widths)
        widths = abjad.CyclicTuple(widths)
        self._widths = widths

    ### SPECIAL METHODS ###

    def _call(self, argument=None):
        """
        Calls command on ``argument``.

        Returns none.
        """
        if argument is None:
            return
        if not self.widths:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        leaf = classes.Selection(argument).leaf(0)
        root = abjad.inspect(leaf).parentage().root
        with abjad.ForbidUpdate(component=root):
            for i, plt in enumerate(classes.Selection(argument).plts()):
                width = self.widths[i]
                self._make_cluster(plt, width)

    ### PRIVATE METHODS ###

    def _make_cluster(self, plt, width):
        assert plt.is_pitched, repr(plt)
        if not width:
            return
        if self.start_pitch is not None:
            start_pitch = self.start_pitch
        else:
            start_pitch = plt.head.written_pitch
        pitches = self._make_pitches(start_pitch, width)
        indicator = abjad.KeyCluster(
            include_black_keys=not self.hide_flat_markup,
            )
        for pleaf in plt:
            chord = abjad.Chord(pitches, pleaf.written_duration)
            abjad.mutate(pleaf).replace(chord)
            abjad.attach(indicator, chord)
            abjad.attach(abjad.tags.ALLOW_REPEAT_PITCH, chord)

    def _make_pitches(self, start_pitch, width):
        pitches = [start_pitch]
        for i in range(width - 1):
            pitch = pitches[-1] + abjad.NamedInterval('M3')
            pitch = abjad.NamedPitch(pitch, accidental='natural')
            assert pitch.accidental == abjad.Accidental('natural')
            pitches.append(pitch)
        return pitches

    def _mutates_score(self):
        return True

    ### PUBLIC PROPERTIES ###

    @property
    def hide_flat_markup(self):
        r"""
        Is true when cluster hides flat markup.

        ..  container:: example

            Hides flat markup:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.pitch('E4'),
            ...     baca.make_notes(repeat_ties=True),
            ...     baca.natural_clusters(widths=[3]),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                <BLANKLINE>
                \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
                <<                                                                                       %! SingleStaffScoreTemplate
                <BLANKLINE>
                    \context GlobalContext = "Global_Context"                                            %! _make_global_context
                    <<                                                                                   %! _make_global_context
                <BLANKLINE>
                        \context GlobalSkips = "Global_Skips"                                            %! _make_global_context
                        {                                                                                %! _make_global_context
                <BLANKLINE>
                            % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca-bar-line-visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
                <BLANKLINE>
                        }                                                                                %! _make_global_context
                <BLANKLINE>
                    >>                                                                                   %! _make_global_context
                <BLANKLINE>
                    \context MusicContext = "Music_Context"                                              %! SingleStaffScoreTemplate
                    <<                                                                                   %! SingleStaffScoreTemplate
                <BLANKLINE>
                        \context Staff = "Music_Staff"                                                   %! SingleStaffScoreTemplate
                        {                                                                                %! SingleStaffScoreTemplate
                <BLANKLINE>
                            \context Voice = "Music_Voice"                                               %! SingleStaffScoreTemplate
                            {                                                                            %! SingleStaffScoreTemplate
                <BLANKLINE>
                                % [Music_Voice measure 1]                                                %! _comment_measure_numbers
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
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! _comment_measure_numbers
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
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! _comment_measure_numbers
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
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! _comment_measure_numbers
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
                <BLANKLINE>
                            }                                                                            %! SingleStaffScoreTemplate
                <BLANKLINE>
                        }                                                                                %! SingleStaffScoreTemplate
                <BLANKLINE>
                    >>                                                                                   %! SingleStaffScoreTemplate
                <BLANKLINE>
                >>                                                                                       %! SingleStaffScoreTemplate

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._hide_flat_markup

    @property
    def selector(self):
        """
        Selects PLTs.

        ..  container:: example

            >>> baca.clusters([3, 4]).selector
            baca.plts()

        Returns selector.
        """
        return self._selector

    @property
    def start_pitch(self):
        r"""
        Gets start pitch.

        ..  container:: example

            Takes start pitch from input notes:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.make_notes(repeat_ties=True),
            ...     baca.pitches('C4 D4 E4 F4'),
            ...     baca.clusters([3]),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                <BLANKLINE>
                \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
                <<                                                                                       %! SingleStaffScoreTemplate
                <BLANKLINE>
                    \context GlobalContext = "Global_Context"                                            %! _make_global_context
                    <<                                                                                   %! _make_global_context
                <BLANKLINE>
                        \context GlobalSkips = "Global_Skips"                                            %! _make_global_context
                        {                                                                                %! _make_global_context
                <BLANKLINE>
                            % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca-bar-line-visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
                <BLANKLINE>
                        }                                                                                %! _make_global_context
                <BLANKLINE>
                    >>                                                                                   %! _make_global_context
                <BLANKLINE>
                    \context MusicContext = "Music_Context"                                              %! SingleStaffScoreTemplate
                    <<                                                                                   %! SingleStaffScoreTemplate
                <BLANKLINE>
                        \context Staff = "Music_Staff"                                                   %! SingleStaffScoreTemplate
                        {                                                                                %! SingleStaffScoreTemplate
                <BLANKLINE>
                            \context Voice = "Music_Voice"                                               %! SingleStaffScoreTemplate
                            {                                                                            %! SingleStaffScoreTemplate
                <BLANKLINE>
                                % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                	\filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <c' e' g'>2
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! _comment_measure_numbers
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
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! _comment_measure_numbers
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
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! _comment_measure_numbers
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
                <BLANKLINE>
                            }                                                                            %! SingleStaffScoreTemplate
                <BLANKLINE>
                        }                                                                                %! SingleStaffScoreTemplate
                <BLANKLINE>
                    >>                                                                                   %! SingleStaffScoreTemplate
                <BLANKLINE>
                >>                                                                                       %! SingleStaffScoreTemplate

        ..  container:: example

            Sets start pitch explicitly:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.make_notes(repeat_ties=True),
            ...     baca.clusters([3], start_pitch='G4'),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                <BLANKLINE>
                \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
                <<                                                                                       %! SingleStaffScoreTemplate
                <BLANKLINE>
                    \context GlobalContext = "Global_Context"                                            %! _make_global_context
                    <<                                                                                   %! _make_global_context
                <BLANKLINE>
                        \context GlobalSkips = "Global_Skips"                                            %! _make_global_context
                        {                                                                                %! _make_global_context
                <BLANKLINE>
                            % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca-bar-line-visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
                <BLANKLINE>
                        }                                                                                %! _make_global_context
                <BLANKLINE>
                    >>                                                                                   %! _make_global_context
                <BLANKLINE>
                    \context MusicContext = "Music_Context"                                              %! SingleStaffScoreTemplate
                    <<                                                                                   %! SingleStaffScoreTemplate
                <BLANKLINE>
                        \context Staff = "Music_Staff"                                                   %! SingleStaffScoreTemplate
                        {                                                                                %! SingleStaffScoreTemplate
                <BLANKLINE>
                            \context Voice = "Music_Voice"                                               %! SingleStaffScoreTemplate
                            {                                                                            %! SingleStaffScoreTemplate
                <BLANKLINE>
                                % [Music_Voice measure 1]                                                %! _comment_measure_numbers
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
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! _comment_measure_numbers
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
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! _comment_measure_numbers
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
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! _comment_measure_numbers
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
                <BLANKLINE>
                            }                                                                            %! SingleStaffScoreTemplate
                <BLANKLINE>
                        }                                                                                %! SingleStaffScoreTemplate
                <BLANKLINE>
                    >>                                                                                   %! SingleStaffScoreTemplate
                <BLANKLINE>
                >>                                                                                       %! SingleStaffScoreTemplate

        Set to named pitch or none.

        Returns named pitch or none.
        """
        return self._start_pitch

    @property
    def widths(self):
        r"""
        Gets widths.

        ..  container:: example

            Increasing widths:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.clusters([1, 2, 3, 4], start_pitch='E4'),
            ...     baca.make_notes(repeat_ties=True),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                <BLANKLINE>
                \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
                <<                                                                                       %! SingleStaffScoreTemplate
                <BLANKLINE>
                    \context GlobalContext = "Global_Context"                                            %! _make_global_context
                    <<                                                                                   %! _make_global_context
                <BLANKLINE>
                        \context GlobalSkips = "Global_Skips"                                            %! _make_global_context
                        {                                                                                %! _make_global_context
                <BLANKLINE>
                            % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca-bar-line-visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
                <BLANKLINE>
                        }                                                                                %! _make_global_context
                <BLANKLINE>
                    >>                                                                                   %! _make_global_context
                <BLANKLINE>
                    \context MusicContext = "Music_Context"                                              %! SingleStaffScoreTemplate
                    <<                                                                                   %! SingleStaffScoreTemplate
                <BLANKLINE>
                        \context Staff = "Music_Staff"                                                   %! SingleStaffScoreTemplate
                        {                                                                                %! SingleStaffScoreTemplate
                <BLANKLINE>
                            \context Voice = "Music_Voice"                                               %! SingleStaffScoreTemplate
                            {                                                                            %! SingleStaffScoreTemplate
                <BLANKLINE>
                                % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                	\filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e'>2
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                	\filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e' g'>4.
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! _comment_measure_numbers
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
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! _comment_measure_numbers
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
                <BLANKLINE>
                            }                                                                            %! SingleStaffScoreTemplate
                <BLANKLINE>
                        }                                                                                %! SingleStaffScoreTemplate
                <BLANKLINE>
                    >>                                                                                   %! SingleStaffScoreTemplate
                <BLANKLINE>
                >>                                                                                       %! SingleStaffScoreTemplate

        ..  container:: example

            Patterned widths:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.clusters([1, 3], start_pitch='E4'),
            ...     baca.make_notes(repeat_ties=True),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                <BLANKLINE>
                \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
                <<                                                                                       %! SingleStaffScoreTemplate
                <BLANKLINE>
                    \context GlobalContext = "Global_Context"                                            %! _make_global_context
                    <<                                                                                   %! _make_global_context
                <BLANKLINE>
                        \context GlobalSkips = "Global_Skips"                                            %! _make_global_context
                        {                                                                                %! _make_global_context
                <BLANKLINE>
                            % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca-bar-line-visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
                <BLANKLINE>
                        }                                                                                %! _make_global_context
                <BLANKLINE>
                    >>                                                                                   %! _make_global_context
                <BLANKLINE>
                    \context MusicContext = "Music_Context"                                              %! SingleStaffScoreTemplate
                    <<                                                                                   %! SingleStaffScoreTemplate
                <BLANKLINE>
                        \context Staff = "Music_Staff"                                                   %! SingleStaffScoreTemplate
                        {                                                                                %! SingleStaffScoreTemplate
                <BLANKLINE>
                            \context Voice = "Music_Voice"                                               %! SingleStaffScoreTemplate
                            {                                                                            %! SingleStaffScoreTemplate
                <BLANKLINE>
                                % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                	\filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e'>2
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! _comment_measure_numbers
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
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                                \once \override Accidental.stencil = ##f
                                \once \override AccidentalCautionary.stencil = ##f
                                \once \override Arpeggio.X-offset = #-2
                                \once \override NoteHead.stencil = #ly:text-interface::print
                                \once \override NoteHead.text = \markup {
                                	\filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
                                }
                                <e'>2
                                ^ \markup {
                                    \center-align
                                        \concat
                                            {
                                                \natural
                                                \flat
                                            }
                                    }
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! _comment_measure_numbers
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
                <BLANKLINE>
                            }                                                                            %! SingleStaffScoreTemplate
                <BLANKLINE>
                        }                                                                                %! SingleStaffScoreTemplate
                <BLANKLINE>
                    >>                                                                                   %! SingleStaffScoreTemplate
                <BLANKLINE>
                >>                                                                                       %! SingleStaffScoreTemplate

        ..  container:: example

            Leaves notes and chords unchanged:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.make_notes(repeat_ties=True),
            ...     baca.pitch('E4'),
            ...     baca.clusters([]),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                <BLANKLINE>
                \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
                <<                                                                                       %! SingleStaffScoreTemplate
                <BLANKLINE>
                    \context GlobalContext = "Global_Context"                                            %! _make_global_context
                    <<                                                                                   %! _make_global_context
                <BLANKLINE>
                        \context GlobalSkips = "Global_Skips"                                            %! _make_global_context
                        {                                                                                %! _make_global_context
                <BLANKLINE>
                            % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca-bar-line-visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
                <BLANKLINE>
                        }                                                                                %! _make_global_context
                <BLANKLINE>
                    >>                                                                                   %! _make_global_context
                <BLANKLINE>
                    \context MusicContext = "Music_Context"                                              %! SingleStaffScoreTemplate
                    <<                                                                                   %! SingleStaffScoreTemplate
                <BLANKLINE>
                        \context Staff = "Music_Staff"                                                   %! SingleStaffScoreTemplate
                        {                                                                                %! SingleStaffScoreTemplate
                <BLANKLINE>
                            \context Voice = "Music_Voice"                                               %! SingleStaffScoreTemplate
                            {                                                                            %! SingleStaffScoreTemplate
                <BLANKLINE>
                                % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                                e'2                                                                      %! baca_make_notes
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                                e'4.                                                                     %! baca_make_notes
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                                e'2                                                                      %! baca_make_notes
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                                e'4.                                                                     %! baca_make_notes
                <BLANKLINE>
                            }                                                                            %! SingleStaffScoreTemplate
                <BLANKLINE>
                        }                                                                                %! SingleStaffScoreTemplate
                <BLANKLINE>
                    >>                                                                                   %! SingleStaffScoreTemplate
                <BLANKLINE>
                >>                                                                                       %! SingleStaffScoreTemplate

        Inteprets positive integers as widths in thirds.

        Interprets zero to mean input note or chord is left unchanged.

        Set to nonnegative integers or none.

        Returns nonnegative integers or none.
        """
        return self._widths

class ColorFingeringCommand(scoping.Command):
    r"""
    Color fingering command.

    ..  container:: example

        With segment-maker:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.pitch('E4'),
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.ColorFingeringCommand(numbers=[0, 1, 2, 1]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            e'2                                                                      %! baca_make_notes
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            e'4.                                                                     %! baca_make_notes
                            ^ \markup {
                                \override
                                    #'(circle-padding . 0.25)
                                    \circle
                                        \finger
                                            1
                                }
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            e'2                                                                      %! baca_make_notes
                            ^ \markup {
                                \override
                                    #'(circle-padding . 0.25)
                                    \circle
                                        \finger
                                            2
                                }
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            e'4.                                                                     %! baca_make_notes
                            ^ \markup {
                                \override
                                    #'(circle-padding . 0.25)
                                    \circle
                                        \finger
                                            1
                                }
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    """

    ### CLASS VARIABLES ##

    __slots__ = (
        '_numbers',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        numbers=None,
        scope: scoping.ScopeTyping = None,
        selector='baca.pheads()',
        ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
            )
        if numbers is not None:
            assert abjad.mathtools.all_are_nonnegative_integers(numbers)
            numbers = abjad.CyclicTuple(numbers)
        self._numbers = numbers

    ### SPECIAL METHODS ###

    def _call(self, argument=None):
        """
        Calls command on ``argument``.

        Returns none.
        """
        if argument is None:
            return
        if not self.numbers:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        for i, phead in enumerate(classes.Selection(argument).pheads()):
            number = self.numbers[i]
            if number != 0:
                fingering = abjad.ColorFingering(number)
                abjad.attach(fingering, phead)

    ### PUBLIC PROPERTIES ###

    @property
    def numbers(self):
        """
        Gets numbers.

        ..  container:: example

            >>> command = baca.ColorFingeringCommand(numbers=[0, 1, 2, 1])
            >>> command.numbers
            CyclicTuple([0, 1, 2, 1])

        Set to nonnegative integers.
        """
        return self._numbers

class DiatonicClusterCommand(scoping.Command):
    r"""
    Diatonic cluster command.

    ..  container:: example

        >>> staff = abjad.Staff("c' d' e' f'")
        >>> command = baca.diatonic_clusters([4, 6])
        >>> command(staff)
        >>> abjad.show(staff, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff, strict=89)
            \new Staff
            {
                <c' d' e' f'>4
                <d' e' f' g' a' b'>4
                <e' f' g' a'>4
                <f' g' a' b' c'' d''>4
            }

    """

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_widths',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        scope: scoping.ScopeTyping = None,
        widths,
        selector='baca.plts()',
        ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
            )
        assert abjad.mathtools.all_are_nonnegative_integers(widths)
        widths = abjad.CyclicTuple(widths)
        self._widths = widths

    ### SPECIAL METHODS ###

    def _call(self, argument=None):
        """
        Calls command on ``argument``.

        Returns none.
        """
        if argument is None:
            return
        if not self.widths:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        for i, plt in enumerate(classes.Selection(argument).plts()):
            width = self.widths[i]
            start = self._get_lowest_diatonic_pitch_number(plt)
            numbers = range(start, start + width)
            module = abjad.pitch.constants
            change = module._diatonic_pc_number_to_pitch_class_number
            numbers = [(12 * (x // 7)) + change[x % 7] for x in numbers]
            pitches = [abjad.NamedPitch(_) for _ in numbers]
            for pleaf in plt:
                chord = abjad.Chord(pleaf)
                chord.note_heads[:] = pitches
                abjad.mutate(pleaf).replace(chord)

    ### PRIVATE METHODS ###

    def _get_lowest_diatonic_pitch_number(self, plt):
        if isinstance(plt.head, abjad.Note):
            pitch = plt.head.written_pitch
        elif isinstance(plt.head, abjad.Chord):
            pitch = plt.head.written_pitches[0]
        else:
            raise TypeError(plt)
        return pitch._get_diatonic_pitch_number()

    def _mutates_score(self):
        return True

    ### PUBLIC PROPERTIES ###

    @property
    def widths(self):
        """
        Gets widths.

        Defaults to none.

        Set to positive integers or none.

        Returns positive integers or none.
        """
        return self._widths

class Loop(abjad.CyclicTuple):
    """
    Loop.

    ..  container::

        >>> loop = baca.Loop([0, 2, 4], intervals=[1])
        >>> abjad.f(loop, strict=89)
        baca.Loop(
            [
                abjad.NamedPitch("c'"),
                abjad.NamedPitch("d'"),
                abjad.NamedPitch("e'"),
                ],
            intervals=abjad.CyclicTuple(
                [1]
                ),
            )

        >>> for i in range(12):
        ...     loop[i]
        NamedPitch("c'")
        NamedPitch("d'")
        NamedPitch("e'")
        NamedPitch("cs'")
        NamedPitch("ef'")
        NamedPitch("f'")
        NamedPitch("d'")
        NamedPitch("e'")
        NamedPitch("fs'")
        NamedPitch("ef'")
        NamedPitch("f'")
        NamedPitch("g'")

        >>> isinstance(loop, abjad.CyclicTuple)
        True

    ..  container:: example

        >>> command = baca.loop([0, 2, 4], [1])
        >>> abjad.f(command, strict=89)
        baca.PitchCommand(
            cyclic=True,
            pitches=baca.Loop(
                [
                    abjad.NamedPitch("c'"),
                    abjad.NamedPitch("d'"),
                    abjad.NamedPitch("e'"),
                    ],
                intervals=abjad.CyclicTuple(
                    [1]
                    ),
                ),
            selector=baca.plts(),
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_intervals',
        '_items',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        *,
        intervals=None,
        ):
        if items is not None:
            assert isinstance(items, collections.Iterable), repr(items)
            items = [abjad.NamedPitch(_) for _ in items]
            items = abjad.CyclicTuple(items)
        abjad.CyclicTuple.__init__(self, items=items)
        if intervals is not None:
            assert isinstance(items, collections.Iterable), repr(items)
            intervals = abjad.CyclicTuple(intervals)
        self._intervals = intervals

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        """
        Gets pitch ``i`` cyclically with intervals.

        Returns pitch.
        """
        if isinstance(i, slice):
            raise NotImplementedError
        iteration = i // len(self)
        if self.intervals is None:
            transposition = 0
        else:
            transposition = sum(self.intervals[:iteration])
        pitch = abjad.CyclicTuple(self)[i]
        pitch = type(pitch)(pitch.number + transposition)
        return pitch

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return abjad.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_args_values=[list(self.items)],
            storage_format_kwargs_names=['intervals'],
            )

    ### PUBLIC PROPERTIES ###

    @property
    def intervals(self):
        """
        Gets intervals.
        """
        return self._intervals

    @property
    def items(self):
        """
        Gets items.
        """
        return self._items

class MicrotoneDeviationCommand(scoping.Command):
    r"""
    Microtone deviation command.

    ..  container:: example

        With alternating up- and down-quatertones:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.pitches('E4'),
        ...     baca.make_even_divisions(),
        ...     baca.deviation([0, 0.5, 0, -0.5]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            e'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            eqs'!8                                                                   %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            eqf'!8                                                                   %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            e'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            eqs'!8                                                                   %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            eqf'!8                                                                   %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            eqs'!8                                                                   %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            eqf'!8                                                                   %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            eqs'!8                                                                   %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    """

    ### CLASS VARIABLES ##

    __slots__ = (
        '_deviations',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        deviations=None,
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        scope: scoping.ScopeTyping = None,
        selector='baca.plts()',
        ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
            )
        if deviations is not None:
            assert isinstance(deviations, collections.Iterable)
            assert all(isinstance(_, numbers.Number) for _ in deviations)
        self._deviations = abjad.CyclicTuple(deviations)

    ### SPECIAL METHODS ###

    def _call(self, argument=None):
        """
        Cyclically applies deviations to plts in ``argument``.

        Returns none.
        """
        if argument is None:
            return
        if not self.deviations:
            return
        if self.selector:
            argument = self.selector(argument)
        for i, plt in enumerate(classes.Selection(argument).plts()):
            deviation = self.deviations[i]
            self._adjust_pitch(plt, deviation)
            
    ### PRIVATE METHODS ###

    def _adjust_pitch(self, plt, deviation):
        assert deviation in (0.5, 0, -0.5)
        if deviation == 0:
            return
        for pleaf in plt:
            pitch = pleaf.written_pitch
            accidental = pitch.accidental.semitones + deviation
            pitch = abjad.NamedPitch(pitch, accidental=accidental)
            pleaf.written_pitch = pitch
            annotation = {'color microtone': True}
            abjad.attach(annotation, pleaf)

    ### PUBLIC PROPERTIES ###

    @property
    def deviations(self):
        """
        Gets deviations.

        ..  container:: example

            >>> command = baca.deviation([0, -0.5, 0, 0.5])
            >>> command.deviations
            CyclicTuple([0, -0.5, 0, 0.5])

        Set to iterable of items (each -0.5, 0 or 0.5).

        Returns cyclic tuple or none.
        """
        return self._deviations

class OctaveDisplacementCommand(scoping.Command):
    r"""
    Octave displacement command.

    ..  container:: example

        Displaces octaves:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_even_divisions(),
        ...     baca.suite(
        ...         baca.pitch('G4'),
        ...         baca.displacement([0, 0, 1, 1, 0, 0, -1, -1, 2, 2]),
        ...         ),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            g''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            g8                                                                       %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            g8                                                                       %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            g'''8                                                                    %! baca_make_even_divisions
            <BLANKLINE>
                            g'''8                                                                    %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            g''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    """

    ### CLASS VARIABLES ##

    __slots__ = (
        '_displacements',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        displacements=None,
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        scope: scoping.ScopeTyping = None,
        selector='baca.plts()',
        ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
            )
        if displacements is not None:
            displacements = tuple(displacements)
            assert self._is_octave_displacement_vector(displacements)
            displacements = abjad.CyclicTuple(displacements)
        self._displacements = displacements

    ### SPECIAL METHODS ###

    def _call(self, argument=None):
        """
        Calls command on ``argument``.

        Returns none.
        """
        if argument is None:
            return
        if self.displacements is None:
            return
        if self.selector:
            argument = self.selector(argument)
        for i, plt in enumerate(classes.Selection(argument).plts()):
            displacement = self.displacements[i]
            interval = abjad.NumberedInterval(12 * displacement)
            for pleaf in plt:
                if isinstance(pleaf, abjad.Note):
                    pitch = pleaf.written_pitch
                    pitch += interval
                    pleaf.written_pitch = pitch
                elif isinstance(pleaf, abjad.Chord):
                    pitches = [_ + interval for _ in pleaf.written_pitches]
                    pleaf.written_pitches = pitches
                else:
                    raise TypeError(pleaf)

    ### PRIVATE METHODS ###

    def _is_octave_displacement_vector(self, argument):
        if isinstance(argument, (tuple, list)):
            if all(isinstance(_, int) for _ in argument):
                return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def displacements(self):
        """
        Gets displacements.

        ..  container:: example

            >>> command = baca.displacement(
            ...     [0, 0, 0, 1, 1, 0, 0, 0, -1, 1, 1, 2, 2],
            ...     )
            >>> command.displacements
            CyclicTuple([0, 0, 0, 1, 1, 0, 0, 0, -1, 1, 1, 2, 2])

        Defaults to none.

        Set to integers or none.

        Returns cyclic tuple of integers, or none.
        """
        return self._displacements

class PitchCommand(scoping.Command):
    r"""
    Pitch command.

    ..  container:: example

        With pitch numbers:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_even_divisions(),
        ...     baca.pitches([19, 13, 15, 16, 17, 23]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            g''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            cs''!8                                                                   %! baca_make_even_divisions
            <BLANKLINE>
                            ef''!8                                                                   %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            b''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            cs''!8                                                                   %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            ef''!8                                                                   %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            b''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            g''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            cs''!8                                                                   %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    ..  container:: example

        With pitch numbers:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_even_divisions(),
        ...     baca.pitches('C4 F4 F#4 <B4 C#5> D5'), 
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            c'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            fs'!8                                                                    %! baca_make_even_divisions
            <BLANKLINE>
                            <b' cs''!>8
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            fs'!8                                                                    %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            <b' cs''!>8
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            f'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            fs'!8                                                                    %! baca_make_even_divisions
            <BLANKLINE>
                            <b' cs''!>8
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    ..  container:: example

        Large chord:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_even_divisions(),
        ...     baca.pitches('<C4 D4 E4 F4 G4 A4 B4 C4>', allow_repeats=True)
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            <c' d' e' f' g' a' b'>8
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            <c' d' e' f' g' a' b'>8
            <BLANKLINE>
                            <c' d' e' f' g' a' b'>8
            <BLANKLINE>
                            <c' d' e' f' g' a' b'>8
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            <c' d' e' f' g' a' b'>8
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            <c' d' e' f' g' a' b'>8
            <BLANKLINE>
                            <c' d' e' f' g' a' b'>8
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            <c' d' e' f' g' a' b'>8
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            <c' d' e' f' g' a' b'>8
            <BLANKLINE>
                            <c' d' e' f' g' a' b'>8
            <BLANKLINE>
                            <c' d' e' f' g' a' b'>8
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            <c' d' e' f' g' a' b'>8
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            <c' d' e' f' g' a' b'>8
            <BLANKLINE>
                            <c' d' e' f' g' a' b'>8
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    ..  container:: example

        Works with Abjad container:

        >>> command = baca.PitchCommand(
        ...     cyclic=True,
        ...     pitches=[19, 13, 15, 16, 17, 23],
        ...     )

        >>> staff = abjad.Staff("c'8 c' c' c' c' c' c' c'")
        >>> command(staff)
        >>> abjad.show(staff, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff, strict=89)
            \new Staff
            {
                g''8
                cs''8
                ef''8
                e''8
                f''8
                b''8
                g''8
                cs''8
            }


    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_allow_octaves',
        '_allow_out_of_range',
        '_allow_repeats',
        '_cyclic',
        '_do_not_transpose',
        '_ignore_incomplete',
        '_mutated_score',
        '_persist',
        '_pitches',
        '_state',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        allow_octaves: bool = None,
        allow_out_of_range: bool = None,
        allow_repeats: bool = None,
        cyclic: bool = None,
        do_not_transpose: bool = None,
        ignore_incomplete: bool = None,
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        persist: str = None,
        pitches: typing.Iterable = None,
        scope: scoping.ScopeTyping = None,
        selector: typings.Selector = None,
        ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
            )
        if allow_octaves is not None:
            allow_octaves = bool(allow_octaves)
        self._allow_octaves = allow_octaves
        if allow_out_of_range is not None:
            allow_out_of_range = bool(allow_out_of_range)
        self._allow_out_of_range = allow_out_of_range
        if allow_repeats is not None:
            allow_repeats = bool(allow_repeats)
        self._allow_repeats = allow_repeats
        if cyclic is not None:
            cyclic = bool(cyclic)
        self._cyclic = cyclic
        if do_not_transpose is not None:
            do_not_transpose = bool(do_not_transpose)
        self._do_not_transpose = do_not_transpose
        if ignore_incomplete is not None:
            ignore_incomplete = bool(ignore_incomplete)
        self._ignore_incomplete = ignore_incomplete
        self._mutated_score = None
        if persist is not None:
            assert isinstance(persist, str), repr(persist)
        self._persist = persist
        if pitches is not None:
            pitches = self._coerce_pitches(pitches)
        self._pitches = pitches
        self._state: abjad.OrderedDict = abjad.OrderedDict()

    ### SPECIAL METHODS ###

    def _call(self, argument=None):
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        if not self.pitches:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        plts = []
        for pleaf in classes.Selection(argument).pleaves():
            plt = abjad.inspect(pleaf).logical_tie()
            if plt.head is pleaf:
                plts.append(plt)
        self._check_length(plts)
        pitches = self.pitches
        if self.cyclic and not isinstance(pitches, abjad.CyclicTuple):
            pitches = abjad.CyclicTuple(pitches)
        previous_pitches_consumed = self._previous_pitches_consumed()
        if self.cyclic and not isinstance(pitches, abjad.CyclicTuple):
            pitches = abjad.CyclicTuple(pitches)
        pitches_consumed = 0
        for i, plt in enumerate(plts):
            pitch = pitches[i + previous_pitches_consumed]
            new_plt = self._set_lt_pitch(plt, pitch)
            if new_plt is not None:
                self._mutated_score = True
                plt = new_plt
            if self.allow_octaves:
                for pleaf in plt:
                    abjad.attach(abjad.tags.ALLOW_OCTAVE, pleaf)
            if self.allow_out_of_range:
                for pleaf in plt:
                    abjad.attach(abjad.tags.ALLOW_OUT_OF_RANGE, pleaf)
            if self.allow_repeats:
                for pleaf in plt:
                    abjad.attach(abjad.tags.ALLOW_REPEAT_PITCH, pleaf)
            if self.do_not_transpose is True:
                for pleaf in plt:
                    abjad.attach(abjad.tags.DO_NOT_TRANSPOSE, pleaf)
            pitches_consumed += 1
        self._state = abjad.OrderedDict()
        pitches_consumed += previous_pitches_consumed
        self.state['pitches_consumed'] = pitches_consumed

    ### PRIVATE METHODS ###

    def _check_length(self, plts):
        if self.cyclic:
            return
        if len(self.pitches) < len(plts):
            message = f'only {len(self.pitches)} pitches'
            message += f' for {len(plts)} logical ties:\n\n'
            message += f'{self!r} and {plts!r}.'
            raise Exception(message)

    @staticmethod
    def _coerce_pitches(pitches):
        if isinstance(pitches, str):
            pitches = PitchCommand._parse_string(pitches)
        items = []
        for item in pitches:
            if isinstance(item, str) and '<' in item and '>' in item:
                item = item.strip('<')
                item = item.strip('>')
                item = abjad.PitchSet(item, abjad.NamedPitch)
            elif isinstance(item, str):
                item = abjad.NamedPitch(item)
            elif isinstance(item, collections.Iterable):
                item = abjad.PitchSet(item, abjad.NamedPitch)
            else:
                item = abjad.NamedPitch(item)
            items.append(item)
        if isinstance(pitches, Loop):
            pitches = type(pitches)(items=items, intervals=pitches.intervals)
        else:
            pitches = abjad.CyclicTuple(items)
        return pitches

    def _mutates_score(self):
        pitches = self.pitches or []
        if any(isinstance(_, collections.Iterable) for _ in pitches):
            return True
        return self._mutated_score

    @staticmethod
    def _parse_string(string):
        items, current_chord = [], []
        for part in string.split():
            if '<' in part:
                assert not current_chord
                current_chord.append(part)
            elif '>' in part:
                assert current_chord
                current_chord.append(part)
                item = ' '.join(current_chord)
                items.append(item)
                current_chord = []
            elif current_chord:
                current_chord.append(part)
            else:
                items.append(part)
        assert not current_chord, repr(current_chord)
        return items

    def _previous_pitches_consumed(self):
        dictionary = self.runtime.get('previous_segment_voice_metadata', None)
        if not dictionary:
            return 0
        dictionary = dictionary.get(abjad.tags.PITCH, None)
        if not dictionary:
            return 0
        if dictionary.get('name') != self.persist:
            return 0
        pitches_consumed = dictionary.get('pitches_consumed', None)
        if not pitches_consumed:
            return 0
        assert 1 <= pitches_consumed
        if self.ignore_incomplete:
            return pitches_consumed
        dictionary = self.runtime['previous_segment_voice_metadata']
        dictionary = dictionary.get(abjad.tags.RHYTHM, None)
        if dictionary:
            if dictionary.get('incomplete_last_note', False):
                pitches_consumed -= 1
        return pitches_consumed

    @staticmethod
    def _set_lt_pitch(lt, pitch):
        new_lt = None
        for leaf in lt:
            abjad.detach(abjad.tags.NOT_YET_PITCHED, leaf)
        if pitch is None:
            if not lt.is_pitched:
                pass
            else:
                for leaf in lt:
                    rest = abjad.Rest(leaf.written_duration)
                    abjad.mutate(leaf).replace(rest, wrappers=True)
                new_lt = abjad.inspect(rest).logical_tie()
        elif isinstance(pitch, collections.Iterable):
            if isinstance(lt.head, abjad.Chord):
                for chord in lt:
                    chord.written_pitches = pitch
            else:
                assert isinstance(lt.head, (abjad.Note, abjad.Rest))
                for leaf in lt:
                    chord = abjad.Chord(pitch, leaf.written_duration)
                    abjad.mutate(leaf).replace(chord, wrappers=True)
                new_lt = abjad.inspect(chord).logical_tie()
        else:
            if isinstance(lt.head, abjad.Note):
                for note in lt:
                    note.written_pitch = pitch
            else:
                assert isinstance(lt.head, (abjad.Chord, abjad.Rest))
                for leaf in lt:
                    note = abjad.Note(pitch, leaf.written_duration)
                    abjad.mutate(leaf).replace(note, wrappers=True)
                new_lt = abjad.inspect(note).logical_tie()
        return new_lt

    ### PUBLIC PROPERTIES ###

    @property
    def allow_octaves(self) -> typing.Optional[bool]:
        """
        Is true when command allows octaves.
        """
        return self._allow_octaves

    @property
    def allow_out_of_range(self) -> typing.Optional[bool]:
        """
        Is true when command allows out-of-range pitches.
        """
        return self._allow_out_of_range

    @property
    def allow_repeats(self) -> typing.Optional[bool]:
        """
        Is true when command allows repeat pitches.
        """
        return self._allow_repeats

    @property
    def cyclic(self) -> typing.Optional[bool]:
        """
        Is true when command reads pitches cyclically.
        """
        return self._cyclic

    @property
    def do_not_transpose(self) -> typing.Optional[bool]:
        """
        Is true when pitch escapes transposition.
        """
        return self._do_not_transpose

    @property
    def ignore_incomplete(self) -> typing.Optional[bool]:
        """
        Is true when persistent pitch command ignores previous segment
        incomplete last note.
        """
        return self._ignore_incomplete

    @property
    def parameter(self) -> str:
        """
        Gets persistence parameter.

        ..  container:: example

            >>> baca.PitchCommand().parameter
            'PITCH'

        """
        return abjad.tags.PITCH
        
    @property
    def persist(self) -> typing.Optional[str]:
        """
        Gets persist name.
        """
        return self._persist

    @property
    def pitches(self) -> typing.Optional[typing.Iterable]:
        """
        Gets pitches.

        ..  container:: example

            Gets pitches:

            >>> command = baca.PitchCommand(
            ...     pitches=[19, 13, 15, 16, 17, 23],
            ...     )

            >>> for pitch in command.pitches:
            ...     pitch
            NamedPitch("g''")
            NamedPitch("cs''")
            NamedPitch("ef''")
            NamedPitch("e''")
            NamedPitch("f''")
            NamedPitch("b''")

        """
        return self._pitches

    @property
    def state(self) -> abjad.OrderedDict:
        """
        Gets state dictionary.
        """
        return self._state

class RegisterCommand(scoping.Command):
    r"""
    Register command.

    ..  container:: example

        With music-maker:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[10, 12, 14], [10, 12, 14], [10, 12, 14]],
        ...     baca.RegisterCommand(
        ...         registration=baca.Registration(
        ...             [('[A0, C8]', 15)],
        ...             ),
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            bf''16
                            [
                            c'''16
                            d'''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            bf''16
                            [
                            c'''16
                            d'''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            bf''16
                            [
                            c'''16
                            d'''16
                            ]
                        }
                    }
                }
            >>

    ..  container:: example

        Tuplet 0 only:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[10, 12, 14], [10, 12, 14], [10, 12, 14]],
        ...     baca.RegisterCommand(
        ...         registration=baca.Registration(
        ...             [('[A0, C8]', 0)],
        ...             ),
        ...         selector=baca.tuplet(0),
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            bf'16
                            [
                            c'16
                            d'16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            bf'16
                            [
                            c''16
                            d''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            bf'16
                            [
                            c''16
                            d''16
                            ]
                        }
                    }
                }
            >>

    ..  container:: example

        Tuplet -1 only:

        >>> music_maker = baca.MusicMaker()

        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[10, 12, 14], [10, 12, 14], [10, 12, 14]],
        ...     baca.RegisterCommand(
        ...         registration=baca.Registration(
        ...             [('[A0, C8]', 0)],
        ...             ),
        ...         selector=baca.tuplet(-1),
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            bf'16
                            [
                            c''16
                            d''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            bf'16
                            [
                            c''16
                            d''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            bf'16
                            [
                            c'16
                            d'16
                            ]
                        }
                    }
                }
            >>

    ..  container:: example

        With segment-maker:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.pitches('G4 G+4 G#4 G#+4 A~4 Ab4 Ab~4'),
        ...     baca.make_even_divisions(),
        ...     baca.RegisterCommand(
        ...         registration=baca.Registration(
        ...             [('[A0, C8]', 15)],
        ...             ),
        ...         ),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            g''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            gqs''!8                                                                  %! baca_make_even_divisions
            <BLANKLINE>
                            gs''!8                                                                   %! baca_make_even_divisions
            <BLANKLINE>
                            gtqs''!8                                                                 %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            aqf''!8                                                                  %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            af''!8                                                                   %! baca_make_even_divisions
            <BLANKLINE>
                            atqf''!8                                                                 %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            g''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            gqs''!8                                                                  %! baca_make_even_divisions
            <BLANKLINE>
                            gs''!8                                                                   %! baca_make_even_divisions
            <BLANKLINE>
                            gtqs''!8                                                                 %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            aqf''!8                                                                  %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            af''!8                                                                   %! baca_make_even_divisions
            <BLANKLINE>
                            atqf''!8                                                                 %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    ..  container:: example

        Works with chords:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [{10, 12, 14}],
        ...     baca.RegisterCommand(
        ...         registration=baca.Registration([('[A0, C8]', -6)]),
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            <bf c' d'>16
                        }
                    }
                }
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_registration',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        registration=None,
        scope: scoping.ScopeTyping = None,
        selector='baca.plts()',
        ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
            )
        if registration is not None:
            prototype = pitchclasses.Registration
            assert isinstance(registration, prototype), repr(registration)
        self._registration = registration

    ### SPECIAL METHODS ###

    def _call(self, argument=None):
        """
        Calls command on ``argument``.

        Returns none.
        """
        if argument is None:
            return
        if self.registration is None:
            return
        if self.selector:
            argument = self.selector(argument)
        for plt in classes.Selection(argument).plts():
            for pleaf in plt:
                if isinstance(pleaf, abjad.Note):
                    pitch = pleaf.written_pitch
                    pitches = self.registration([pitch])
                    pleaf.written_pitch = pitches[0]
                elif isinstance(pleaf, abjad.Chord):
                    pitches = pleaf.written_pitches
                    pitches = self.registration(pitches)
                    pleaf.written_pitches = pitches
                else:
                    raise TypeError(pleaf)
                abjad.detach(abjad.tags.NOT_YET_REGISTERED, pleaf)

    ### PUBLIC PROPERTIES ###

    @property
    def registration(self):
        """
        Gets registration.

        ..  container:: example

            >>> command = baca.RegisterCommand(
            ...     registration=baca.Registration(
            ...         [('[A0, C4)', 15), ('[C4, C8)', 27)],
            ...         ),
            ...     )

            >>> abjad.f(command.registration, strict=89)
            baca.Registration(
                components=[
                    baca.RegistrationComponent(
                        source_pitch_range=abjad.PitchRange('[A0, C4)'),
                        target_octave_start_pitch=abjad.NumberedPitch(15),
                        ),
                    baca.RegistrationComponent(
                        source_pitch_range=abjad.PitchRange('[C4, C8)'),
                        target_octave_start_pitch=abjad.NumberedPitch(27),
                        ),
                    ],
                )

        Set to registration or none.

        Returns registration or none.
        """
        return self._registration

class RegisterInterpolationCommand(scoping.Command):
    r"""
    Register interpolation command.

    :param selector: command selector.

    :param start_pitch: interpolation start pitch.

    :param stop_pitch: interpolation stop pitch.

    ..  container:: example

        With music-maker:

        >>> music_maker = baca.MusicMaker()

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     collections,
        ...     baca.register(0, 24),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            fs'16
                            [
                            e'16
                            ef'16
                            f'16
                            a'16
                            bf'16
                            c''16
                            b'16
                            af'16
                            g''16
                            cs''16
                            d''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''16
                            [
                            e''16
                            ef''16
                            f''16
                            a''16
                            bf''16
                            c'''16
                            b''16
                            af''16
                            g'''16
                            cs'''16
                            d'''16
                            ]
                        }
                    }
                }
            >>

    ..  container:: example

        With chords:

        >>> music_maker = baca.MusicMaker()

        >>> collections = [
        ...     [6, 4], [3, 5], [9, 10], [0, 11], [8, 7], [1, 2],
        ...     ]
        >>> collections = [set(_) for _ in collections]
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     collections,
        ...     baca.register(0, 24),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            <e' fs'>16
                        }
                        \scaleDurations #'(1 . 1) {
                            <f' ef''>16
                        }
                        \scaleDurations #'(1 . 1) {
                            <a' bf'>16
                        }
                        \scaleDurations #'(1 . 1) {
                            <c'' b''>16
                        }
                        \scaleDurations #'(1 . 1) {
                            <g'' af''>16
                        }
                        \scaleDurations #'(1 . 1) {
                            <cs''' d'''>16
                        }
                    }
                }
            >>

    ..  container:: example

        Holds register constant:

            >>> time_signatures = 4 * [(4, 8), (3, 8)]
            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=time_signatures,
            ...     )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> maker(
        ...     'Music_Voice',
        ...     baca.pitches(pitches),
        ...     baca.make_even_divisions(),
        ...     baca.register(12, 12),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 6]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 7]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 8]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            fs''!8                                                                   %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            ef''!8                                                                   %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            a''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            bf''!8                                                                   %! baca_make_even_divisions
            <BLANKLINE>
                            c''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            b''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            af''!8                                                                   %! baca_make_even_divisions
            <BLANKLINE>
                            g''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            cs''!8                                                                   %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            fs''!8                                                                   %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 5]                                                %! _comment_measure_numbers
                            ef''!8                                                                   %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            a''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            bf''!8                                                                   %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 6]                                                %! _comment_measure_numbers
                            c''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            b''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            af''!8                                                                   %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 7]                                                %! _comment_measure_numbers
                            g''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            cs''!8                                                                   %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            fs''!8                                                                   %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 8]                                                %! _comment_measure_numbers
                            e''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            ef''!8                                                                   %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    ..  container:: example

        Octave-transposes to a target interpolated from 12 down to 0:

            >>> time_signatures = 4 * [(4, 8), (3, 8)]
            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=time_signatures,
            ...     )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> maker(
        ...     'Music_Voice',
        ...     baca.pitches(pitches),
        ...     baca.make_even_divisions(),
        ...     baca.register(12, 0),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 6]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 7]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 8]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            fs''!8                                                                   %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            ef''!8                                                                   %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            a''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            bf'!8                                                                    %! baca_make_even_divisions
            <BLANKLINE>
                            c''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            b'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            af'!8                                                                    %! baca_make_even_divisions
            <BLANKLINE>
                            g''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            cs''!8                                                                   %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            fs'!8                                                                    %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 5]                                                %! _comment_measure_numbers
                            ef''!8                                                                   %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            a'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            bf'!8                                                                    %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 6]                                                %! _comment_measure_numbers
                            c''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            b'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            af'!8                                                                    %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 7]                                                %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            cs''!8                                                                   %! baca_make_even_divisions
            <BLANKLINE>
                            d'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            fs'!8                                                                    %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 8]                                                %! _comment_measure_numbers
                            e'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            ef'!8                                                                    %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    ..  container:: example

        Octave-transposes to a target interpolated from 0 up to 12:

            >>> time_signatures = 4 * [(4, 8), (3, 8)]
            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=time_signatures,
            ...     )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> maker(
        ...     'Music_Voice',
        ...     baca.pitches(pitches),
        ...     baca.make_even_divisions(),
        ...     baca.register(0, 12),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 6]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 7]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 8]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            fs'!8                                                                    %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            ef'!8                                                                    %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            a'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            bf'!8                                                                    %! baca_make_even_divisions
            <BLANKLINE>
                            c''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            b'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            af'!8                                                                    %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            cs''!8                                                                   %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            fs'!8                                                                    %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 5]                                                %! _comment_measure_numbers
                            ef''!8                                                                   %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            a'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            bf'!8                                                                    %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 6]                                                %! _comment_measure_numbers
                            c''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            b'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            af'!8                                                                    %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 7]                                                %! _comment_measure_numbers
                            g''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            cs''!8                                                                   %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            fs''!8                                                                   %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 8]                                                %! _comment_measure_numbers
                            e''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            ef''!8                                                                   %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    ..  container:: example

        Octave-transposes to a target interpolated from 12 down to -12:

            >>> time_signatures = 4 * [(4, 8), (3, 8)]
            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=time_signatures,
            ...     )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> maker(
        ...     'Music_Voice',
        ...     baca.pitches(pitches),
        ...     baca.make_even_divisions(),
        ...     baca.register(12, -12),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 6]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 7]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 8]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            fs''!8                                                                   %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            ef''!8                                                                   %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            a'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            bf'!8                                                                    %! baca_make_even_divisions
            <BLANKLINE>
                            c''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            b'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            af'!8                                                                    %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            cs''!8                                                                   %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            d'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            fs'!8                                                                    %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 5]                                                %! _comment_measure_numbers
                            ef'!8                                                                    %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            a'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            bf!8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 6]                                                %! _comment_measure_numbers
                            c'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            b8                                                                       %! baca_make_even_divisions
            <BLANKLINE>
                            af!8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 7]                                                %! _comment_measure_numbers
                            g8                                                                       %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            cs'!8                                                                    %! baca_make_even_divisions
            <BLANKLINE>
                            d'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            fs!8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 8]                                                %! _comment_measure_numbers
                            e8                                                                       %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            ef!8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f8                                                                       %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    ..  container:: example

        Octave-transposes to a target interpolated from -12 up to 12:

            >>> time_signatures = 4 * [(4, 8), (3, 8)]
            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=time_signatures,
            ...     )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> maker(
        ...     'Music_Voice',
        ...     baca.pitches(pitches),
        ...     baca.make_even_divisions(),
        ...     baca.register(-12, 12),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 6]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 7]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 8]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            fs!8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e8                                                                       %! baca_make_even_divisions
            <BLANKLINE>
                            ef!8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f8                                                                       %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            a8                                                                       %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            bf!8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            b8                                                                       %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            af!8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            cs'!8                                                                    %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            d'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            fs'!8                                                                    %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 5]                                                %! _comment_measure_numbers
                            ef'!8                                                                    %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            a'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            bf'!8                                                                    %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 6]                                                %! _comment_measure_numbers
                            c''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            b'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            af'!8                                                                    %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 7]                                                %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            cs''!8                                                                   %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            fs''!8                                                                   %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 8]                                                %! _comment_measure_numbers
                            e''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            ef''!8                                                                   %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_start_pitch',
        '_stop_pitch',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        scope: scoping.ScopeTyping = None,
        selector: typings.Selector = 'baca.plts()',
        start_pitch: typing.Union[typings.Number, abjad.NumberedPitch] = 0,
        stop_pitch: typing.Union[typings.Number, abjad.NumberedPitch] = 0,
        ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
            )
        start_pitch = abjad.NumberedPitch(start_pitch)
        self._start_pitch: abjad.NumberedPitch = start_pitch
        stop_pitch = abjad.NumberedPitch(stop_pitch)
        self._stop_pitch: abjad.NumberedPitch = stop_pitch

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        if self.selector:
            argument = self.selector(argument)
        plts = classes.Selection(argument).plts()
        length = len(plts)
        for i, plt in enumerate(plts):
            registration = self._get_registration(i, length)
            for pleaf in plt:
                if isinstance(pleaf, abjad.Note):
                    written_pitches = registration([pleaf.written_pitch])
                    pleaf.written_pitch = written_pitches[0]
                elif isinstance(pleaf, abjad.Chord):
                    written_pitches = registration(pleaf.written_pitches)
                    pleaf.written_pitches = written_pitches
                else:
                    raise TypeError(pleaf)
                abjad.detach(abjad.tags.NOT_YET_REGISTERED, pleaf)

    ### PRIVATE METHODS ###

    def _get_registration(self, i, length):
        start_pitch = self.start_pitch.number
        stop_pitch = self.stop_pitch.number
        compass = stop_pitch - start_pitch
        fraction = abjad.Fraction(i, length)
        addendum = fraction * compass
        current_pitch = start_pitch + addendum
        current_pitch = int(current_pitch)
        return pitchclasses.Registration([('[A0, C8]', current_pitch)])

    ### PUBLIC PROPERTIES ###

    @property
    def selector(self) -> typing.Optional[abjad.Expression]:
        r"""
        Gets selector.

        ..  container:: example

            Selects tuplet 0:

            >>> music_maker = baca.MusicMaker()

            >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
            >>> contribution = music_maker(
            ...     'Voice_1',
            ...     collections,
            ...     baca.color(selector=baca.tuplet(0)),
            ...     baca.register(0, 24, selector=baca.tuplet(0)),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                \abjad-color-music #'green
                                fs'16
                                [
                                \abjad-color-music #'green
                                e'16
                                \abjad-color-music #'green
                                ef''16
                                \abjad-color-music #'green
                                f''16
                                \abjad-color-music #'green
                                a'16
                                \abjad-color-music #'green
                                bf'16
                                \abjad-color-music #'green
                                c''16
                                \abjad-color-music #'green
                                b''16
                                \abjad-color-music #'green
                                af''16
                                \abjad-color-music #'green
                                g''16
                                \abjad-color-music #'green
                                cs'''16
                                \abjad-color-music #'green
                                d'''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                fs'16
                                [
                                e'16
                                ef'16
                                f'16
                                a'16
                                bf'16
                                c'16
                                b'16
                                af'16
                                g'16
                                cs'16
                                d'16
                                ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Selects tuplet -1:

            >>> music_maker = baca.MusicMaker()

            >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
            >>> contribution = music_maker(
            ...     'Voice_1',
            ...     collections,
            ...     baca.color(selector=baca.tuplet(-1)),
            ...     baca.register(0, 24, selector=baca.tuplet(-1)),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                fs'16
                                [
                                e'16
                                ef'16
                                f'16
                                a'16
                                bf'16
                                c'16
                                b'16
                                af'16
                                g'16
                                cs'16
                                d'16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                \abjad-color-music #'green
                                fs'16
                                [
                                \abjad-color-music #'green
                                e'16
                                \abjad-color-music #'green
                                ef''16
                                \abjad-color-music #'green
                                f''16
                                \abjad-color-music #'green
                                a'16
                                \abjad-color-music #'green
                                bf'16
                                \abjad-color-music #'green
                                c''16
                                \abjad-color-music #'green
                                b''16
                                \abjad-color-music #'green
                                af''16
                                \abjad-color-music #'green
                                g''16
                                \abjad-color-music #'green
                                cs'''16
                                \abjad-color-music #'green
                                d'''16
                                ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Maps to tuplets:

            >>> music_maker = baca.MusicMaker()

            >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
            >>> contribution = music_maker(
            ...     'Voice_1',
            ...     collections,
            ...     baca.color(selector=baca.tuplets()),
            ...     baca.new(
            ...         baca.register(0, 24),
            ...         map=baca.tuplets(),
            ...         ),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice_1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                \abjad-color-music #'red
                                fs'16
                                [
                                \abjad-color-music #'red
                                e'16
                                \abjad-color-music #'red
                                ef''16
                                \abjad-color-music #'red
                                f''16
                                \abjad-color-music #'red
                                a'16
                                \abjad-color-music #'red
                                bf'16
                                \abjad-color-music #'red
                                c''16
                                \abjad-color-music #'red
                                b''16
                                \abjad-color-music #'red
                                af''16
                                \abjad-color-music #'red
                                g''16
                                \abjad-color-music #'red
                                cs'''16
                                \abjad-color-music #'red
                                d'''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                \abjad-color-music #'blue
                                fs'16
                                [
                                \abjad-color-music #'blue
                                e'16
                                \abjad-color-music #'blue
                                ef''16
                                \abjad-color-music #'blue
                                f''16
                                \abjad-color-music #'blue
                                a'16
                                \abjad-color-music #'blue
                                bf'16
                                \abjad-color-music #'blue
                                c''16
                                \abjad-color-music #'blue
                                b''16
                                \abjad-color-music #'blue
                                af''16
                                \abjad-color-music #'blue
                                g''16
                                \abjad-color-music #'blue
                                cs'''16
                                \abjad-color-music #'blue
                                d'''16
                                ]
                            }
                        }
                    }
                >>

        """
        return self._selector

    @property
    def start_pitch(self) -> abjad.NumberedPitch:
        """
        Gets start pitch.
        """
        return self._start_pitch

    @property
    def stop_pitch(self) -> abjad.NumberedPitch:
        """
        Gets stop pitch.
        """
        return self._stop_pitch

class RegisterToOctaveCommand(scoping.Command):
    r"""
    Register-to-octave command.

    ..  container:: example

        Chords:

        >>> music_maker = baca.MusicMaker()

        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [{0, 14, 28}],
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Down,
        ...         octave_number=4,
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            <c' d'' e'''>16
                        }
                    }
                }
            >>

        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [{0, 14, 28}],
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Center,
        ...         octave_number=4,
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            <c d' e''>16
                        }
                    }
                }
            >>

        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [{0, 14, 28}],
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Up,
        ...         octave_number=4,
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            <c, d e'>16
                        }
                    }
                }
            >>

    ..  container:: example

        Disjunct notes:

        >>> music_maker = baca.MusicMaker()

        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 14, 28]],
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Down,
        ...         octave_number=4,
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            c'16
                            [
                            d''16
                            e'''16
                            ]
                        }
                    }
                }
            >>

        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 14, 28]],
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Center,
        ...         octave_number=4,
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            c16
                            [
                            d'16
                            e''16
                            ]
                        }
                    }
                }
            >>

        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 14, 28]],
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Up,
        ...         octave_number=4,
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            c,16
                            [
                            d16
                            e'16
                            ]
                        }
                    }
                }
            >>

    ..  container:: example

        Conjunct notes:

        >>> music_maker = baca.MusicMaker()

        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[10, 12, 14]],
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Down,
        ...         octave_number=4,
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            bf'16
                            [
                            c''16
                            d''16
                            ]
                        }
                    }
                }
            >>

        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[10, 12, 14]],
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Center,
        ...         octave_number=4,
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            bf16
                            [
                            c'16
                            d'16
                            ]
                        }
                    }
                }
            >>

        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[10, 12, 14]],
        ...     baca.RegisterToOctaveCommand(
        ...         anchor=abjad.Up,
        ...         octave_number=4,
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            bf16
                            [
                            c'16
                            d'16
                            ]
                        }
                    }
                }
            >>

    ..  container:: example

        >>> baca.RegisterToOctaveCommand()
        RegisterToOctaveCommand(selector=baca.plts())

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_anchor',
        '_octave_number',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        anchor=None,
        octave_number=None,
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        scope: scoping.ScopeTyping = None,
        selector='baca.plts()',
        ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
            )
        if anchor is not None:
            prototype = (abjad.Center, abjad.Down, abjad.Up)
            assert anchor in prototype, repr(anchor)
        self._anchor = anchor
        if octave_number is not None:
            assert isinstance(octave_number, int), repr(octave_number)
        self._octave_number = octave_number

    ### SPECIAL METHODS ###

    def _call(self, argument=None):
        """
        Calls command on ``argument``.

        Returns none.
        """
        if argument is None:
            return
        if self.octave_number is None:
            return
        if self.selector:
            argument = self.selector(argument)
        target_octave_number = self.octave_number or 4
        current_octave_number = self._get_anchor_octave_number(argument)
        octave_adjustment = target_octave_number - current_octave_number
        transposition = abjad.Transposition(n=12 * octave_adjustment)
        for pleaf in classes.Selection(argument).pleaves():
            self._set_pitch(pleaf, transposition)

    ### PRIVATE METHODS ###

    def _get_anchor_octave_number(self, argument):
        pitches = []
        for leaf in abjad.iterate(argument).leaves(pitched=True):
            if isinstance(leaf, abjad.Note):
                pitches.append(leaf.written_pitch)
            elif isinstance(leaf, abjad.Chord):
                pitches.extend(leaf.written_pitches)
            else:
                raise TypeError(leaf)
        pitches = list(set(pitches))
        pitches.sort()
        anchor = self.anchor or abjad.Down
        if anchor == abjad.Down:
            pitch = pitches[0]
        elif anchor == abjad.Up:
            pitch = pitches[-1]
        elif anchor == abjad.Center:
            pitch = self._get_centroid(pitches)
        else:
            raise ValueError(anchor)
        return pitch.octave.number

    @staticmethod
    def _get_centroid(pitches):
        soprano = max(pitches)
        bass = min(pitches)
        centroid = (soprano.number + bass.number) / 2.0
        return abjad.NumberedPitch(centroid)

    def _set_pitch(self, leaf, transposition):
        if isinstance(leaf, abjad.Note):
            pitch = transposition(leaf.written_pitch)
            leaf.written_pitch = pitch
        elif isinstance(leaf, abjad.Chord):
            pitches = [transposition(_) for _ in leaf.written_pitches]
            leaf.written_pitches = pitches
        abjad.detach(abjad.tags.NOT_YET_REGISTERED, leaf)

    ### PUBLIC PROPERTIES ###

    @property
    def anchor(self):
        """
        Gets anchor.

        ..  container:: example

            Bass anchored at octave 5:

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> command = baca.RegisterToOctaveCommand(
            ...     anchor=abjad.Down,
            ...     octave_number=5,
            ...     )
            >>> command(chord)
            >>> staff = abjad.Staff([chord])
            >>> abjad.show(staff, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord, strict=89)
                <c'' d''' e''''>1

        ..  container:: example

            Center anchored at octave 5:

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> command = baca.RegisterToOctaveCommand(
            ...     anchor=abjad.Center,
            ...     octave_number=5,
            ...     )
            >>> command(chord)
            >>> staff = abjad.Staff([chord])
            >>> abjad.show(staff, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord, strict=89)
                <c' d'' e'''>1

        ..  container:: example

            Soprano anchored at octave 5:

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> command = baca.RegisterToOctaveCommand(
            ...     anchor=abjad.Up,
            ...     octave_number=5,
            ...     )
            >>> command(chord)
            >>> staff = abjad.Staff([chord])
            >>> abjad.show(staff, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord, strict=89)
                <c d' e''>1

        Set to up, down, center or none.

        Returns up, down, center or none.
        """
        return self._anchor

    @property
    def octave_number(self):
        r"""
        Gets octave number.

        ..  container:: example

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> staff = abjad.Staff([chord])
            >>> abjad.attach(abjad.Clef('bass'), staff[0])
            >>> abjad.show(staff, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord, strict=89)
                \clef "bass"
                <c, d e'>1

        ..  container:: example

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> command = baca.RegisterToOctaveCommand(octave_number=1)
            >>> command(chord)
            >>> staff = abjad.Staff([chord])
            >>> abjad.attach(abjad.Clef('bass'), staff[0])
            >>> abjad.show(staff, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord, strict=89)
                \clef "bass"
                <c,, d, e>1

        ..  container:: example

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> command = baca.RegisterToOctaveCommand(octave_number=2)
            >>> command(chord)
            >>> staff = abjad.Staff([chord])
            >>> abjad.attach(abjad.Clef('bass'), staff[0])
            >>> abjad.show(staff, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord, strict=89)
                \clef "bass"
                <c, d e'>1

        ..  container:: example

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> command = baca.RegisterToOctaveCommand(octave_number=3)
            >>> command(chord)
            >>> staff = abjad.Staff([chord])
            >>> abjad.attach(abjad.Clef('bass'), staff[0])
            >>> abjad.show(chord, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord, strict=89)
                \clef "bass"
                <c d' e''>1

        ..  container:: example

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> command = baca.RegisterToOctaveCommand(octave_number=4)
            >>> command(chord)
            >>> abjad.show(chord, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord, strict=89)
                <c' d'' e'''>1

        ..  container:: example

            >>> chord = abjad.Chord("<c, d e'>1")
            >>> command = baca.RegisterToOctaveCommand(octave_number=5)
            >>> command(chord)
            >>> abjad.show(chord, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(chord, strict=89)
                <c'' d''' e''''>1

        Returns integer.
        """
        return self._octave_number

class StaffPositionCommand(scoping.Command):
    r"""
    Staff position command.

    ..  container:: example

        >>> staff = abjad.Staff("c' d' e' f'")
        >>> abjad.attach(abjad.Clef('treble'), staff[0])
        >>> command = baca.staff_positions([0, 2])
        >>> command(staff)
        >>> abjad.show(staff, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff, strict=89)
            \new Staff
            {
                \clef "treble"
                b'4
                d''4
                b'4
                d''4
            }

    ..  container:: example

        >>> staff = abjad.Staff("c' d' e' f'")
        >>> abjad.attach(abjad.Clef('percussion'), staff[0])
        >>> command = baca.staff_positions([0, 2])
        >>> command(staff)
        >>> abjad.show(staff, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff, strict=89)
            \new Staff
            {
                \clef "percussion"
                c'4
                e'4
                c'4
                e'4
            }

    """

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_allow_repeats',
        '_exact',
        '_numbers',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        numbers,
        allow_repeats: bool = None,
        exact: bool = None, 
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        scope: scoping.ScopeTyping = None,
        selector: typings.Selector = 'baca.plts()',
        ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
            )
        if exact is not None:
            exact = bool(exact)
        self._exact = exact
        if numbers is not None:
            assert all(isinstance(_, int) for _ in numbers), repr(numbers)
            numbers = abjad.CyclicTuple(numbers)
        self._numbers = numbers
        if allow_repeats is not None:
            allow_repeats = bool(allow_repeats)
        self._allow_repeats = allow_repeats

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        if not self.numbers:
            return
        if self.selector:
            argument = self.selector(argument)
        plt_count = 0
        for i, plt in enumerate(classes.Selection(argument).plts()):
            clef = abjad.inspect(plt.head).effective(
                abjad.Clef,
                default=abjad.Clef('treble'),
                )
            number = self.numbers[i]
            position = abjad.StaffPosition(number)
            pitch = position.to_pitch(clef)
            PitchCommand._set_lt_pitch(plt, pitch)
            plt_count += 1
            for pleaf in plt:
                abjad.attach(abjad.tags.STAFF_POSITION, pleaf)
                if self.allow_repeats:
                    abjad.attach(abjad.tags.ALLOW_REPEAT_PITCH, pleaf)
                    abjad.attach(abjad.tags.DO_NOT_TRANSPOSE, pleaf)
        if self.exact and plt_count != len(self.numbers):
            message = f'PLT count ({plt_count}) does not match'
            message += f' staff position count ({len(self.numbers)}).'
            raise Exception(message)

    ### PUBLIC PROPERTIES ###

    @property
    def allow_repeats(self) -> typing.Optional[bool]:
        """
        Is true when repeat staff positions are allowed.
        """
        return self._allow_repeats

    @property
    def exact(self) -> typing.Optional[bool]:
        """
        Is true when number of staff positions must match number of leaves
        exactly.
        """
        return self._exact

    @property
    def numbers(self) -> typing.Optional[abjad.CyclicTuple]:
        """
        Gets numbers.
        """
        return self._numbers

class StaffPositionInterpolationCommand(scoping.Command):
    r"""
    Staff position interpolation command.

    :param selector: command selector.

    :param start_pitch: interpolation start pitch.

    :param stop_pitch: interpolation stop pitch.

    ..  container:: example

        >>> music_maker = baca.MusicMaker()

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     collections,
        ...     baca.clef('treble'),
        ...     baca.interpolate_staff_positions('Eb4', 'F#5'),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            \clef "treble"                                                           %! baca_clef:IndicatorCommand
                            ef'16
                            [
                            e'16
                            f'16
                            f'16
                            f'16
                            g'16
                            g'16
                            g'16
                            a'16
                            a'16
                            a'16
                            b'16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            b'16
                            [
                            c''16
                            c''16
                            c''16
                            d''16
                            d''16
                            d''16
                            e''16
                            e''16
                            e''16
                            f''16
                            fs''16
                            ]
                        }
                    }
                }
            >>

    ..  container:: example

        >>> music_maker = baca.MusicMaker()

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     collections,
        ...     baca.clef('treble'),
        ...     baca.interpolate_staff_positions('Eb4', 'F#5'),
        ...     baca.glissando(allow_repeats=True, stems=True), 
        ...     baca.glissando_thickness(3),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            \override Glissando.thickness = #'3                                      %! baca_glissando_thickness:OverrideCommand(1)
                            \clef "treble"                                                           %! baca_clef:IndicatorCommand
                            ef'16
                            [
                            \glissando                                                               %! baca_glissando:SpannerCommand
                            \hide NoteHead                                                           %! baca_glissando:SpannerCommand
                            \override Accidental.stencil = ##f                                       %! baca_glissando:SpannerCommand
                            \override NoteColumn.glissando-skip = ##t                                %! baca_glissando:SpannerCommand
                            \override NoteHead.no-ledgers = ##t                                      %! baca_glissando:SpannerCommand
                            e'16
                            \glissando                                                               %! baca_glissando:SpannerCommand
                            f'16
                            \glissando                                                               %! baca_glissando:SpannerCommand
                            f'16
                            \glissando                                                               %! baca_glissando:SpannerCommand
                            f'16
                            \glissando                                                               %! baca_glissando:SpannerCommand
                            g'16
                            \glissando                                                               %! baca_glissando:SpannerCommand
                            g'16
                            \glissando                                                               %! baca_glissando:SpannerCommand
                            g'16
                            \glissando                                                               %! baca_glissando:SpannerCommand
                            a'16
                            \glissando                                                               %! baca_glissando:SpannerCommand
                            a'16
                            \glissando                                                               %! baca_glissando:SpannerCommand
                            a'16
                            \glissando                                                               %! baca_glissando:SpannerCommand
                            b'16
                            ]
                            \glissando                                                               %! baca_glissando:SpannerCommand
                        }
                        \scaleDurations #'(1 . 1) {
                            b'16
                            [
                            \glissando                                                               %! baca_glissando:SpannerCommand
                            c''16
                            \glissando                                                               %! baca_glissando:SpannerCommand
                            c''16
                            \glissando                                                               %! baca_glissando:SpannerCommand
                            c''16
                            \glissando                                                               %! baca_glissando:SpannerCommand
                            d''16
                            \glissando                                                               %! baca_glissando:SpannerCommand
                            d''16
                            \glissando                                                               %! baca_glissando:SpannerCommand
                            d''16
                            \glissando                                                               %! baca_glissando:SpannerCommand
                            e''16
                            \glissando                                                               %! baca_glissando:SpannerCommand
                            e''16
                            \glissando                                                               %! baca_glissando:SpannerCommand
                            e''16
                            \glissando                                                               %! baca_glissando:SpannerCommand
                            f''16
                            \glissando                                                               %! baca_glissando:SpannerCommand
                            \revert Accidental.stencil                                               %! baca_glissando:SpannerCommand
                            \revert NoteColumn.glissando-skip                                        %! baca_glissando:SpannerCommand
                            \revert NoteHead.no-ledgers                                              %! baca_glissando:SpannerCommand
                            \undo \hide NoteHead                                                     %! baca_glissando:SpannerCommand
                            fs''16
                            ]
                            \revert Glissando.thickness                                              %! baca_glissando_thickness:OverrideCommand(2)
                        }
                    }
                }
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_start_pitch',
        '_stop_pitch',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        scope: scoping.ScopeTyping = None,
        selector: typings.Selector = 'baca.plts()',
        start_pitch: typing.Union[str, abjad.NamedPitch] = 'C4',
        stop_pitch: typing.Union[str, abjad.NamedPitch] = 'C4',
        ) -> None:
        scoping.Command.__init__(
            self,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
            )
        start_pitch = abjad.NamedPitch(start_pitch)
        self._start_pitch: abjad.NamedPitch = start_pitch
        stop_pitch = abjad.NamedPitch(stop_pitch)
        self._stop_pitch: abjad.NamedPitch = stop_pitch

    ### SPECIAL METHODS ###

    def _call(self, argument=None) -> None:
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        if self.selector:
            argument = self.selector(argument)
        plts = classes.Selection(argument).plts()
        if not plts:
            return
        count = len(plts)
        start_pl = plts[0].head
        clef = abjad.inspect(start_pl).effective(abjad.Clef)
        start_staff_position = self.start_pitch.to_staff_position(clef=clef)
        stop_pl = plts[-1].head
        clef = abjad.inspect(stop_pl).effective(
            abjad.Clef,
            default=abjad.Clef('treble'),
            )
        stop_staff_position = self.stop_pitch.to_staff_position(clef=clef)
        unit_distance = abjad.Fraction(
            stop_staff_position.number - start_staff_position.number,
            count - 1,
            )
        for i, plt in enumerate(plts):
            staff_position = unit_distance * i + start_staff_position.number
            staff_position = round(staff_position)
            staff_position = abjad.StaffPosition(staff_position)
            clef = abjad.inspect(plt.head).effective(
                abjad.Clef,
                default=abjad.Clef('treble'),
                )
            pitch = staff_position.to_pitch(clef=clef)
            PitchCommand._set_lt_pitch(plt, pitch)
            for leaf in plt:
                abjad.attach(abjad.tags.ALLOW_REPEAT_PITCH, leaf)
        PitchCommand._set_lt_pitch(plts[0], self.start_pitch)
        PitchCommand._set_lt_pitch(plts[-1], self.stop_pitch)

    ### PUBLIC PROPERTIES ###

    @property
    def start_pitch(self) -> abjad.NamedPitch:
        """
        Gets start pitch.
        """
        return self._start_pitch

    @property
    def stop_pitch(self) -> abjad.NamedPitch:
        """
        Gets stop pitch.
        """
        return self._stop_pitch

### FACTORY FUNCTIONS ###

def bass_to_octave(
    n: int,
    *,
    selector: typings.Selector = 'baca.plts()',
    ) -> RegisterToOctaveCommand:
    r"""
    Octave-transposes music.

    ..  container:: example

        Octave-transposes music such that the lowest note in the entire
        selection appears in octave 3:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
        ...     baca.bass_to_octave(3),
        ...     baca.color(selector=baca.plts().group()),
        ...     counts=[5, -3],
        ...     talea_denominator=32,
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'green
                            <c d bf>8
                            ~
                            [
                            \abjad-color-music #'green
                            <c d bf>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'green
                            f'8
                            ~
                            [
                            \abjad-color-music #'green
                            f'32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'green
                            <ef' e' fs''>8
                            ~
                            [
                            \abjad-color-music #'green
                            <ef' e' fs''>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'green
                            <g af'>8
                            ~
                            [
                            \abjad-color-music #'green
                            <g af'>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'green
                            a8
                            ~
                            [
                            \abjad-color-music #'green
                            a32
                            ]
                            r16.
                        }
                    }
                }
            >>

    ..  container:: example

        Octave-transposes music such that the lowest pitch in each pitched
        logical tie appears in octave 3:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
        ...     baca.new(
        ...         baca.bass_to_octave(3),
        ...         map=baca.plts(),
        ...         ),
        ...     baca.color(selector=baca.plts()),
        ...     counts=[5, -3],
        ...     talea_denominator=32,
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'red
                            <c d bf>8
                            ~
                            [
                            \abjad-color-music #'red
                            <c d bf>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'blue
                            f8
                            ~
                            [
                            \abjad-color-music #'blue
                            f32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'red
                            <ef e fs'>8
                            ~
                            [
                            \abjad-color-music #'red
                            <ef e fs'>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'blue
                            <g af'>8
                            ~
                            [
                            \abjad-color-music #'blue
                            <g af'>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'red
                            a8
                            ~
                            [
                            \abjad-color-music #'red
                            a32
                            ]
                            r16.
                        }
                    }
                }
            >>

    ..  container:: example

        Octave-transposes music such that the lowest pitch in each of the
        last two pitched logical ties appears in octave 3:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
        ...     baca.new(
        ...         baca.bass_to_octave(3),
        ...         map=baca.plts()[-2:],
        ...         ),
        ...     baca.color(selector=baca.plts()[-2:]),
        ...     counts=[5, -3],
        ...     talea_denominator=32,
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            <c' d' bf'>8
                            ~
                            [
                            <c' d' bf'>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            f''8
                            ~
                            [
                            f''32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            <ef'' e'' fs'''>8
                            ~
                            [
                            <ef'' e'' fs'''>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'red
                            <g af'>8
                            ~
                            [
                            \abjad-color-music #'red
                            <g af'>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'blue
                            a8
                            ~
                            [
                            \abjad-color-music #'blue
                            a32
                            ]
                            r16.
                        }
                    }
                }
            >>

    """
    return RegisterToOctaveCommand(
        anchor=abjad.Down,
        octave_number=n,
        selector=selector,
        )

def center_to_octave(
    n: int,
    *,
    selector: typings.Selector = 'baca.plts()',
    ) -> RegisterToOctaveCommand:
    r"""
    Octave-transposes music.

    ..  container:: example

        Octave-transposes music such that the centroid of all PLTs appears
        in octave 3:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
        ...     baca.center_to_octave(3),
        ...     baca.color(selector=baca.plts().group()),
        ...     counts=[5, -3],
        ...     talea_denominator=32,
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'green
                            <c, d, bf,>8
                            ~
                            [
                            \abjad-color-music #'green
                            <c, d, bf,>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'green
                            f8
                            ~
                            [
                            \abjad-color-music #'green
                            f32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'green
                            <ef e fs'>8
                            ~
                            [
                            \abjad-color-music #'green
                            <ef e fs'>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'green
                            <g, af>8
                            ~
                            [
                            \abjad-color-music #'green
                            <g, af>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'green
                            a,8
                            ~
                            [
                            \abjad-color-music #'green
                            a,32
                            ]
                            r16.
                        }
                    }
                }
            >>

    ..  container:: example

        Octave-transposes music such that the centroid of each pitched
        logical tie appears in octave 3:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
        ...     baca.new(
        ...         baca.center_to_octave(3),
        ...         map=baca.plts(),
        ...         ),
        ...     baca.color(selector=baca.plts()),
        ...     counts=[5, -3],
        ...     talea_denominator=32,
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'red
                            <c d bf>8
                            ~
                            [
                            \abjad-color-music #'red
                            <c d bf>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'blue
                            f8
                            ~
                            [
                            \abjad-color-music #'blue
                            f32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'red
                            <ef e fs'>8
                            ~
                            [
                            \abjad-color-music #'red
                            <ef e fs'>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'blue
                            <g, af>8
                            ~
                            [
                            \abjad-color-music #'blue
                            <g, af>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'red
                            a8
                            ~
                            [
                            \abjad-color-music #'red
                            a32
                            ]
                            r16.
                        }
                    }
                }
            >>

    ..  container:: example

        Octave-transposes music such that the centroid of each of the last
        two pitched logical ties appears in octave 3:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
        ...     baca.new(
        ...         baca.center_to_octave(3),
        ...         map=baca.plts()[-2:],
        ...         ),
        ...     baca.color(selector=baca.plts()[-2:]),
        ...     counts=[5, -3],
        ...     talea_denominator=32,
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            <c' d' bf'>8
                            ~
                            [
                            <c' d' bf'>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            f''8
                            ~
                            [
                            f''32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            <ef'' e'' fs'''>8
                            ~
                            [
                            <ef'' e'' fs'''>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'red
                            <g, af>8
                            ~
                            [
                            \abjad-color-music #'red
                            <g, af>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'blue
                            a8
                            ~
                            [
                            \abjad-color-music #'blue
                            a32
                            ]
                            r16.
                        }
                    }
                }
            >>

    """
    return RegisterToOctaveCommand(
        anchor=abjad.Center,
        octave_number=n,
        selector=selector,
        )

def clusters(
    widths: typing.List[int],
    *,
    selector: typings.Selector = 'baca.plts()',
    start_pitch: typing.Union[int, str, abjad.NamedPitch] = None,
    ) -> ClusterCommand:
    """
    Makes clusters with ``widths`` and ``start_pitch``.
    """
    return ClusterCommand(
        selector=selector,
        start_pitch=start_pitch,
        widths=widths,
        )

def color_fingerings(
    numbers: typing.List[typings.Number],
    *,
    selector: typings.Selector = 'baca.pheads()',
    ) -> ColorFingeringCommand:
    """
    Adds color fingerings.
    """
    return ColorFingeringCommand(numbers=numbers, selector=selector)

def deviation(
    deviations: typing.List[typings.Number],
    *,
    selector: typings.Selector = 'baca.plts()',
    ) -> MicrotoneDeviationCommand:
    """
    Sets microtone ``deviations``.
    """
    return MicrotoneDeviationCommand(
        deviations=deviations,
        selector=selector,
        )

def diatonic_clusters(
    widths: typing.List[int],
    *,
    selector: typings.Selector = 'baca.plts()',
    ) -> DiatonicClusterCommand:
    """
    Makes diatonic clusters with ``widths``.
    """
    return DiatonicClusterCommand(
        selector=selector,
        widths=widths,
        )

def displacement(
    displacements: typing.List[int],
    *,
    selector: typings.Selector = 'baca.plts()',
    ) -> OctaveDisplacementCommand:
    r"""
    Octave-displaces ``selector`` output.

    ..  container:: example

        Octave-displaces PLTs:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     3 * [[0, 2, 3]],
        ...     baca.displacement([0, 0, -1, -1, 1, 1]),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            ef4
                            ~
                            ef16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/8 {
                            c16
                            [
                            d''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 11/12 {
                            c'16
                            [
                            d'16
                            ]
                            ef4
                            ~
                            ef16
                            r16
                            r4
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Octave-displaces chords:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     6 * [{0, 2, 3}],
        ...     baca.displacement([0, 0, -1, -1, 1, 1]),
        ...     baca.rests_around([2], [4]),
        ...     counts=[4],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            r8
                            <c' d' ef'>4
                        }
                        \scaleDurations #'(1 . 1) {
                            <c' d' ef'>4
                        }
                        \scaleDurations #'(1 . 1) {
                            <c d ef>4
                        }
                        \scaleDurations #'(1 . 1) {
                            <c d ef>4
                        }
                        \scaleDurations #'(1 . 1) {
                            <c'' d'' ef''>4
                        }
                        \scaleDurations #'(1 . 1) {
                            <c'' d'' ef''>4
                            r4
                        }
                    }
                }
            >>

    ..  container:: example

        Octave-displaces last six pitched logical ties:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     3 * [[0, 2, 3]],
        ...     baca.displacement(
        ...         [0, 0, -1, -1, 1, 1],
        ...         selector=baca.plts()[-6:],
        ...         ),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            ef'4
                            ~
                            ef'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 7/8 {
                            c'16
                            [
                            d'16
                            ]
                            ef4
                            ~
                            ef16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 11/12 {
                            c16
                            [
                            d''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            r4
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return OctaveDisplacementCommand(
        displacements=displacements,
        selector=selector,
        )

def force_accidental(
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
    ) -> AccidentalAdjustmentCommand:
    r"""
    Forces accidental.

    ..  container:: example

        Inverts edition-specific tags:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.not_parts(baca.force_accidental(selector=baca.pleaves()[:2])),
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.pitches('E4 F4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            e'2                                                                      %! AccidentalAdjustmentCommand:+PARTS
                        %@% e'!2                                                                     %! AccidentalAdjustmentCommand:-PARTS %! baca_make_notes
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            f'4.                                                                     %! AccidentalAdjustmentCommand:+PARTS
                        %@% f'!4.                                                                    %! AccidentalAdjustmentCommand:-PARTS %! baca_make_notes
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            e'2                                                                      %! baca_make_notes
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            f'4.                                                                     %! baca_make_notes
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    """
    return AccidentalAdjustmentCommand(
        forced=True,
        selector=selector,
        )

def interpolate_staff_positions(
    start_pitch: typing.Union[str, abjad.NamedPitch],
    stop_pitch: typing.Union[str, abjad.NamedPitch],
    *,
    selector: typings.Selector = 'baca.plts()',
    ) -> StaffPositionInterpolationCommand:
    """
    Interpolates from staff position of ``start_pitch`` to staff
    position of ``stop_pitch``.
    """
    return StaffPositionInterpolationCommand(
        start_pitch=start_pitch,
        stop_pitch=stop_pitch,
        selector=selector,
        )

def loop(
    items: typing.Iterable,
    intervals: typing.Iterable,
    *,
    selector: typings.Selector = 'baca.plts()',
    ) -> PitchCommand:
    """
    Loops ``items`` at ``intervals``.
    """
    loop = Loop(items=items, intervals=intervals)
    return pitches(loop, selector=selector)

def natural_clusters(
    widths: typing.Iterable[int],
    *,
    selector: typings.Selector = 'baca.plts()',
    start_pitch: typing.Union[int, str, abjad.NamedPitch] = None,
    ) -> ClusterCommand:
    """
    Makes natural clusters with ``widths`` and ``start_pitch``.
    """
    return ClusterCommand(
        hide_flat_markup=True,
        selector=selector,
        start_pitch=start_pitch,
        widths=widths,
        )

def pitch(
    pitch,
    *,
    allow_out_of_range: bool = None,
    do_not_transpose: bool = None,
    persist: str = None,
    selector: typings.Selector = 'baca.plts()',
    ) -> PitchCommand:
    """
    Makes pitch command.
    """
    if isinstance(pitch, (list, tuple)) and len(pitch) == 1:
        raise Exception(f'one-note chord {pitch!r}?')
    if allow_out_of_range not in (None, True, False):
        raise Exception('allow_out_of_range must be boolean'
            f' (not {allow_out_of_range!r}).')
    if do_not_transpose not in (None, True, False):
        raise Exception('do_not_transpose must be boolean'
            f' (not {do_not_transpose!r}).')
    if persist is not None and not isinstance(persist, str):
        raise Exception(f'persist name must be string (not {persist!r}).')
    return PitchCommand(
        allow_out_of_range=allow_out_of_range,
        allow_repeats=True,
        cyclic=True,
        do_not_transpose=do_not_transpose,
        persist=persist,
        pitches=[pitch],
        selector=selector,
        )

def pitches(
    pitches: typing.Iterable,
    *,
    allow_octaves: bool = None,
    allow_repeats: bool = None,
    do_not_transpose: bool = None,
    exact: bool = None,
    ignore_incomplete: bool = None,
    persist: str = None,
    selector: typings.Selector = 'baca.plts()',
    ) -> PitchCommand:
    """
    Makes pitch command.
    """
    if do_not_transpose not in (None, True, False):
        raise Exception('do_not_transpose must be boolean'
            f' (not {do_not_transpose!r}).')
    if bool(exact):
        cyclic = False
    else:
        cyclic = True
    if ignore_incomplete not in (None, True, False):
        raise Exception('ignore_incomplete must be boolean'
            f' (not {ignore_incomplete!r}).')
    if ignore_incomplete is True and not persist:
        raise Exception(f'ignore_incomplete is ignored'
            ' when persist is not set.')
    if persist is not None and not isinstance(persist, str):
        raise Exception(f'persist name must be string (not {persist!r}).')
    return PitchCommand(
        allow_octaves=allow_octaves,
        allow_repeats=allow_repeats,
        cyclic=cyclic,
        do_not_transpose=do_not_transpose,
        ignore_incomplete=ignore_incomplete,
        persist=persist,
        pitches=pitches,
        selector=selector,
        )

def register(
    start: int,
    stop: int = None,
    *,
    selector: typings.Selector = 'baca.plts()',
    ) -> typing.Union[RegisterCommand, RegisterInterpolationCommand]:
    r"""
    Octave-transposes ``selector`` output.

    ..  container:: example

        Octave-transposes all PLTs to the octave rooted at -6:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.register(-6),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf4
                            ~
                            bf16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs16
                            [
                            e'16
                            ]
                            ef'4
                            ~
                            ef'16
                            r16
                            af16
                            [
                            g16
                            ]
                        }
                        \times 4/5 {
                            a16
                            r4
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

        Octave-transposes PLTs in tuplet 1 to the octave rooted at -6:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.color(selector=baca.tuplet(1)),
        ...     baca.register(-6, selector=baca.tuplet(1)),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
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
                            \abjad-color-music #'green
                            fs16
                            [
                            \abjad-color-music #'green
                            e'16
                            ]
                            \abjad-color-music #'green
                            ef'4
                            ~
                            \abjad-color-music #'green
                            ef'16
                            \abjad-color-music #'green
                            r16
                            \abjad-color-music #'green
                            af16
                            [
                            \abjad-color-music #'green
                            g16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Octave-transposes all PLTs to an octave interpolated from -6 to 18:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.register(-6, 18),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
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
                            fs'16
                            [
                            e'16
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
                            a''16
                            r4
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

        Octave-transposes PLTs in tuplet 1 to an octave interpolated from
        -6 to 18:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.color(selector=baca.tuplet(1)),
        ...     baca.register(-6, 18, selector=baca.tuplet(1)),
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
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
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
                            \abjad-color-music #'green
                            fs16
                            [
                            \abjad-color-music #'green
                            e'16
                            ]
                            \abjad-color-music #'green
                            ef'4
                            ~
                            \abjad-color-music #'green
                            ef'16
                            \abjad-color-music #'green
                            r16
                            \abjad-color-music #'green
                            af'16
                            [
                            \abjad-color-music #'green
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    if stop is None:
        return RegisterCommand(
            registration=pitchclasses.Registration([('[A0, C8]', start)]),
            selector=selector,
            )
    return RegisterInterpolationCommand(
        selector=selector,
        start_pitch=start,
        stop_pitch=stop,
        )

def soprano_to_octave(
    n: int,
    *,
    selector: typings.Selector = 'baca.plts()',
    ) -> RegisterToOctaveCommand:
    r"""
    Octave-transposes music.

    ..  container:: example

        Octave-transposes music such that the highest note in the
        collection of all PLTs appears in octave 3:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
        ...     baca.color(selector=baca.plts().group()),
        ...     baca.soprano_to_octave(3),
        ...     counts=[5, -3],
        ...     talea_denominator=32,
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'green
                            <c,, d,, bf,,>8
                            ~
                            [
                            \abjad-color-music #'green
                            <c,, d,, bf,,>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'green
                            f,8
                            ~
                            [
                            \abjad-color-music #'green
                            f,32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'green
                            <ef, e, fs>8
                            ~
                            [
                            \abjad-color-music #'green
                            <ef, e, fs>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'green
                            <g,, af,>8
                            ~
                            [
                            \abjad-color-music #'green
                            <g,, af,>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'green
                            a,,8
                            ~
                            [
                            \abjad-color-music #'green
                            a,,32
                            ]
                            r16.
                        }
                    }
                }
            >>

    ..  container:: example

        Octave-transposes music that such that the highest note in each
        pitched logical tie appears in octave 3:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
        ...     baca.new(
        ...         baca.soprano_to_octave(3),
        ...         map=baca.plts(),
        ...         ),
        ...     baca.color(selector=baca.plts()),
        ...     counts=[5, -3],
        ...     talea_denominator=32,
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'red
                            <c d bf>8
                            ~
                            [
                            \abjad-color-music #'red
                            <c d bf>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'blue
                            f8
                            ~
                            [
                            \abjad-color-music #'blue
                            f32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'red
                            <ef, e, fs>8
                            ~
                            [
                            \abjad-color-music #'red
                            <ef, e, fs>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'blue
                            <g, af>8
                            ~
                            [
                            \abjad-color-music #'blue
                            <g, af>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'red
                            a8
                            ~
                            [
                            \abjad-color-music #'red
                            a32
                            ]
                            r16.
                        }
                    }
                }
            >>

    ..  container:: example

        Octave-transposes music that such that the highest note in each
        of the last two PLTs appears in octave 3:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice_1',
        ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
        ...     baca.new(
        ...         baca.soprano_to_octave(3),
        ...         map=baca.plts()[-2:],
        ...         ),
        ...     baca.color(selector=baca.plts()[-2:]),
        ...     counts=[5, -3],
        ...     talea_denominator=32,
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice_1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            <c' d' bf'>8
                            ~
                            [
                            <c' d' bf'>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            f''8
                            ~
                            [
                            f''32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            <ef'' e'' fs'''>8
                            ~
                            [
                            <ef'' e'' fs'''>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'red
                            <g, af>8
                            ~
                            [
                            \abjad-color-music #'red
                            <g, af>32
                            ]
                            r16.
                        }
                        \scaleDurations #'(1 . 1) {
                            \abjad-color-music #'blue
                            a8
                            ~
                            [
                            \abjad-color-music #'blue
                            a32
                            ]
                            r16.
                        }
                    }
                }
            >>

    """
    return RegisterToOctaveCommand(
        anchor=abjad.Up,
        octave_number=n,
        selector=selector,
        )

def staff_position(
    number: int,
    *,
    selector: typings.Selector = 'baca.plts()',
    ) -> StaffPositionCommand:
    """
    Makes staff position command; allows repeats.
    """
    assert isinstance(number, int), repr(number)
    return StaffPositionCommand(
        allow_repeats=True,
        numbers=[number],
        selector=selector,
        ) 

def staff_positions(
    numbers,
    *,
    allow_repeats: bool = None,
    exact: bool = None,
    selector: typings.Selector = 'baca.plts()',
    ) -> StaffPositionCommand:
    """
    Makes staff position command; does not allow repeats.
    """
    if allow_repeats is None and len(numbers) == 1:
        allow_repeats = True
    return StaffPositionCommand(
        allow_repeats=allow_repeats,
        exact=exact,
        numbers=numbers,
        selector=selector,
        ) 
