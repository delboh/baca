import abjad
import baca
from typing import List
from typing import Optional
from .Command import Command


class BreakMeasureMap(abjad.AbjadObject):
    r'''Breaks measure map.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.StringTrioScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8), (4, 8)],
        ...     breaks=baca.BreakMeasureMap([
        ...         baca.line_break(baca.skip(0)),
        ...         baca.lbsd(100, [30, 30], baca.skip(1)),
        ...         baca.line_break(baca.skip(1)),
        ...         ]),
        ...     )

        >>> maker(
        ...     baca.scope('ViolinMusicVoice', 1),
        ...     baca.make_even_runs(),
        ...     baca.pitches('E4', repeats=True),
        ...     )
        >>> lilypond_file = maker.run(environment='docs')
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
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \autoPageBreaksOff                                                           %! BREAK:BMM1
                        \noBreak                                                                     %! BREAK:BMM2
                        \time 4/8                                                                    %! SM1:EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM1:EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                        \break                                                                       %! BREAK:IC
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \noBreak                                                                     %! BREAK:BMM2
                        \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
                        #'((Y-offset . 100) (alignment-distances . (30 30)))                         %! BREAK:IC
                        \time 3/8                                                                    %! SM1:EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM1:EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                        \break                                                                       %! BREAK:IC
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \noBreak                                                                     %! BREAK:BMM2
                        \time 4/8                                                                    %! SM1:EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM1:EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \noBreak                                                                     %! BREAK:BMM2
                        \time 3/8                                                                    %! SM1:EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM1:EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 5]                                                    %! SM4
                        \noBreak                                                                     %! BREAK:BMM2
                        \time 4/8                                                                    %! SM1:EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM1:EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                        \override Score.BarLine.transparent = ##f                                    %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context StringSectionStaffGroup = "String Section Staff Group"
                    <<
                        \tag Violin                                                                  %! ST4
                        \context ViolinMusicStaff = "ViolinMusicStaff"
                        {
                            \context ViolinMusicVoice = "ViolinMusicVoice"
                            {
                                {
            <BLANKLINE>
                                    % [ViolinMusicVoice measure 1]                                   %! SM4
                                    \set ViolinMusicStaff.instrumentName = \markup {                 %! ST1:DEFAULT_INSTRUMENT:SM8
                                        \hcenter-in                                                  %! ST1:DEFAULT_INSTRUMENT:SM8
                                            #10                                                      %! ST1:DEFAULT_INSTRUMENT:SM8
                                            Violin                                                   %! ST1:DEFAULT_INSTRUMENT:SM8
                                        }                                                            %! ST1:DEFAULT_INSTRUMENT:SM8
                                    \set ViolinMusicStaff.shortInstrumentName = \markup {            %! ST1:DEFAULT_INSTRUMENT:SM8
                                        \hcenter-in                                                  %! ST1:DEFAULT_INSTRUMENT:SM8
                                            #10                                                      %! ST1:DEFAULT_INSTRUMENT:SM8
                                            Vn.                                                      %! ST1:DEFAULT_INSTRUMENT:SM8
                                        }                                                            %! ST1:DEFAULT_INSTRUMENT:SM8
                                    \clef "treble"                                                   %! ST3:DEFAULT_CLEF:SM8
                                    \once \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! ST1:DEFAULT_INSTRUMENT_COLOR:SM6
                                    \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! ST3:DEFAULT_CLEF_COLOR:SM6
                                %@% \override ViolinMusicStaff.Clef.color = ##f                      %! ST3:DEFAULT_CLEF_COLOR_CANCELLATION:SM7
                                    \set ViolinMusicStaff.forceClef = ##t                            %! ST3:DEFAULT_CLEF:SM8
                                    e'8
                                    [
                                    ^ \markup {                                                      %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                        \with-color                                                  %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                            #(x11-color 'DarkViolet)                                 %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                            (Violin)                                                 %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                        }                                                            %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                    \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'violet) %! ST1:REDRAWN_DEFAULT_INSTRUMENT_COLOR:SM6
                                    \set ViolinMusicStaff.instrumentName = \markup {                 %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        \hcenter-in                                                  %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                            #10                                                      %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                            Violin                                                   %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        }                                                            %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \set ViolinMusicStaff.shortInstrumentName = \markup {            %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        \hcenter-in                                                  %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                            #10                                                      %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                            Vn.                                                      %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        }                                                            %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \override ViolinMusicStaff.Clef.color = #(x11-color 'violet)     %! ST3:DEFAULT_CLEF_REDRAW_COLOR:SM6
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
                                    ]
                                }
                                {
            <BLANKLINE>
                                    % [ViolinMusicVoice measure 2]                                   %! SM4
                                    e'8
                                    [
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
                                    ]
                                }
                                {
            <BLANKLINE>
                                    % [ViolinMusicVoice measure 3]                                   %! SM4
                                    e'8
                                    [
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
                                    ]
                                }
                                {
            <BLANKLINE>
                                    % [ViolinMusicVoice measure 4]                                   %! SM4
                                    e'8
                                    [
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
                                    ]
                                }
                                {
            <BLANKLINE>
                                    % [ViolinMusicVoice measure 5]                                   %! SM4
                                    e'8
                                    [
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
                                    ]
            <BLANKLINE>
                                }
                            }
                        }
                        \tag Viola                                                                   %! ST4
                        \context ViolaMusicStaff = "ViolaMusicStaff"
                        {
                            \context ViolaMusicVoice = "ViolaMusicVoice"
                            {
            <BLANKLINE>
                                % [ViolaMusicVoice measure 1]                                        %! SM4
                                \set ViolaMusicStaff.instrumentName = \markup {                      %! ST1:DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! ST1:DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! ST1:DEFAULT_INSTRUMENT:SM8
                                        Viola                                                        %! ST1:DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! ST1:DEFAULT_INSTRUMENT:SM8
                                \set ViolaMusicStaff.shortInstrumentName = \markup {                 %! ST1:DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! ST1:DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! ST1:DEFAULT_INSTRUMENT:SM8
                                        Va.                                                          %! ST1:DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! ST1:DEFAULT_INSTRUMENT:SM8
                                \clef "alto"                                                         %! ST3:DEFAULT_CLEF:SM8
                                \once \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! ST1:DEFAULT_INSTRUMENT_COLOR:SM6
                                \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! ST3:DEFAULT_CLEF_COLOR:SM6
                            %@% \override ViolaMusicStaff.Clef.color = ##f                           %! ST3:DEFAULT_CLEF_COLOR_CANCELLATION:SM7
                                \set ViolaMusicStaff.forceClef = ##t                                 %! ST3:DEFAULT_CLEF:SM8
                                R1 * 1/2
                                ^ \markup {                                                          %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                    \with-color                                                      %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'DarkViolet)                                     %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                        (Viola)                                                      %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                    }                                                                %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'violet) %! ST1:REDRAWN_DEFAULT_INSTRUMENT_COLOR:SM6
                                \set ViolaMusicStaff.instrumentName = \markup {                      %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        Viola                                                        %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \set ViolaMusicStaff.shortInstrumentName = \markup {                 %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        Va.                                                          %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \override ViolaMusicStaff.Clef.color = #(x11-color 'violet)          %! ST3:DEFAULT_CLEF_REDRAW_COLOR:SM6
            <BLANKLINE>
                                % [ViolaMusicVoice measure 2]                                        %! SM4
                                R1 * 3/8
            <BLANKLINE>
                                % [ViolaMusicVoice measure 3]                                        %! SM4
                                R1 * 1/2
            <BLANKLINE>
                                % [ViolaMusicVoice measure 4]                                        %! SM4
                                R1 * 3/8
            <BLANKLINE>
                                % [ViolaMusicVoice measure 5]                                        %! SM4
                                R1 * 1/2
            <BLANKLINE>
                            }
                        }
                        \tag Cello                                                                   %! ST4
                        \context CelloMusicStaff = "CelloMusicStaff"
                        {
                            \context CelloMusicVoice = "CelloMusicVoice"
                            {
            <BLANKLINE>
                                % [CelloMusicVoice measure 1]                                        %! SM4
                                \set CelloMusicStaff.instrumentName = \markup {                      %! ST1:DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! ST1:DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! ST1:DEFAULT_INSTRUMENT:SM8
                                        Cello                                                        %! ST1:DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! ST1:DEFAULT_INSTRUMENT:SM8
                                \set CelloMusicStaff.shortInstrumentName = \markup {                 %! ST1:DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! ST1:DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! ST1:DEFAULT_INSTRUMENT:SM8
                                        Vc.                                                          %! ST1:DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! ST1:DEFAULT_INSTRUMENT:SM8
                                \clef "bass"                                                         %! ST3:DEFAULT_CLEF:SM8
                                \once \override CelloMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! ST1:DEFAULT_INSTRUMENT_COLOR:SM6
                                \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! ST3:DEFAULT_CLEF_COLOR:SM6
                            %@% \override CelloMusicStaff.Clef.color = ##f                           %! ST3:DEFAULT_CLEF_COLOR_CANCELLATION:SM7
                                \set CelloMusicStaff.forceClef = ##t                                 %! ST3:DEFAULT_CLEF:SM8
                                R1 * 1/2
                                ^ \markup {                                                          %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                    \with-color                                                      %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                        #(x11-color 'DarkViolet)                                     %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                        (Cello)                                                      %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                    }                                                                %! ST1:DEFAULT_INSTRUMENT_ALERT:SM11
                                \override CelloMusicStaff.InstrumentName.color = #(x11-color 'violet) %! ST1:REDRAWN_DEFAULT_INSTRUMENT_COLOR:SM6
                                \set CelloMusicStaff.instrumentName = \markup {                      %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        Cello                                                        %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \set CelloMusicStaff.shortInstrumentName = \markup {                 %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        Vc.                                                          %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! ST1:REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \override CelloMusicStaff.Clef.color = #(x11-color 'violet)          %! ST3:DEFAULT_CLEF_REDRAW_COLOR:SM6
            <BLANKLINE>
                                % [CelloMusicVoice measure 2]                                        %! SM4
                                R1 * 3/8
            <BLANKLINE>
                                % [CelloMusicVoice measure 3]                                        %! SM4
                                R1 * 1/2
            <BLANKLINE>
                                % [CelloMusicVoice measure 4]                                        %! SM4
                                R1 * 3/8
            <BLANKLINE>
                                % [CelloMusicVoice measure 5]                                        %! SM4
                                R1 * 1/2
            <BLANKLINE>
                            }
                        }
                    >>
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_bol_measure_numbers',
        '_commands',
        '_deactivate',
        '_tags',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, commands=None, deactivate=None, tags=None):
        tags = tags or []
        assert baca.Command._are_valid_tags(tags), repr(tags)
        if abjad.tags.BREAK not in tags:
            tags.append(abjad.tags.BREAK)
        self._tags = tags
        self._bol_measure_numbers = []
        self._deactivate = deactivate
        if commands is not None:
            commands_ = []
            for command in commands:
                command_ = abjad.new(
                    command,
                    deactivate=self.deactivate,
                    tags=self.tags,
                    )
                commands_.append(command_)
            commands = commands_
            commands = tuple(commands)
        self._commands = commands

    ### SPECIAL METHODS ###

    def __call__(self, context=None):
        r'''Calls map on `context`.

        Returns none.
        '''
        if context is None:
            return
        skips = baca.select(context).skips()
        literal = abjad.LilyPondLiteral(r'\autoPageBreaksOff', 'before')
        abjad.attach(
            literal,
            skips[0],
            deactivate=self.deactivate,
            tag=self.tag.append('BMM1'),
            )
        for skip in skips:
            if not abjad.inspect(skip).has_indicator(baca.LBSD):
                literal = abjad.LilyPondLiteral(r'\noBreak', 'before')
                abjad.attach(
                    literal,
                    skip,
                    deactivate=self.deactivate,
                    tag=self.tag.append('BMM2'),
                    )
        for command in self.commands:
            command(context)

    ### PUBLIC PROPERTIES ###

    @property
    def commands(self):
        r'''Gets commands.

        ..  container:: example

            >>> breaks = baca.BreakMeasureMap([
            ...     baca.line_break(baca.skip(0)),
            ...     baca.page_break(baca.skip(1)),
            ...     ])

            >>> for command in breaks.commands:
            ...     abjad.f(command)
            ...
            baca.IndicatorCommand(
                indicators=abjad.CyclicTuple(
                    [
                        abjad.LilyPondLiteral('\\break', format_slot='after', ),
                        ]
                    ),
                selector=baca.skip(0),
                tags=['BREAK'],
                )
            baca.IndicatorCommand(
                indicators=abjad.CyclicTuple(
                    [
                        abjad.LilyPondLiteral('\\pageBreak', format_slot='after', ),
                        ]
                    ),
                selector=baca.skip(1),
                tags=['BREAK'],
                )

        Returns commands.
        '''
        return self._commands

    @property
    def deactivate(self):
        r'''Is true when tags should write deactivated.

        Returns true, false or none.
        '''
        return self._deactivate

    @property
    def tag(self) -> Optional[abjad.Tag]:
        r'''Gets tag.
        '''
        if self.tags:
            return abjad.Tag.from_words(self.tags)
        return None

    @property
    def tags(self) -> List[str]:
        r'''Gets tags.
        '''
        assert Command._are_valid_tags(self._tags), repr(self._tags)
        return self._tags[:]
