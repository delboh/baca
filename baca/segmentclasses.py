import abjad
import collections
import typing
from . import classes
from . import commands as baca_commands
from . import indicators
from . import scoping
from . import typings


### CLASSES ###

class BreakMeasureMap(object):
    r"""
    Breaks measure map.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.StringTrioScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8), (4, 8)],
        ...     breaks=baca.breaks(baca.page([1, 0, (10, 20,)])),
        ...     )

        >>> maker(
        ...     'Violin_Music_Voice',
        ...     baca.make_even_divisions(),
        ...     baca.pitch('E4'),
        ...     )
        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! StringTrioScoreTemplate
            <<                                                                                       %! StringTrioScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \autoPageBreaksOff                                                           %! BreakMeasureMap(1):BREAK
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \baca-lbsd #0 #'(10 20)                                                      %! BREAK:IndicatorCommand
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        \pageBreak                                                                   %! BREAK:IndicatorCommand
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! _comment_measure_numbers
                        \noBreak                                                                     %! BreakMeasureMap(2):BREAK
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! StringTrioScoreTemplate
                <<                                                                                   %! StringTrioScoreTemplate
            <BLANKLINE>
                    \context StringSectionStaffGroup = "String_Section_Staff_Group"                  %! StringTrioScoreTemplate
                    <<                                                                               %! StringTrioScoreTemplate
            <BLANKLINE>
                        \tag Violin                                                                  %! ScoreTemplate(5)
                        \context ViolinMusicStaff = "Violin_Music_Staff"                             %! StringTrioScoreTemplate
                        {                                                                            %! StringTrioScoreTemplate
            <BLANKLINE>
                            \context ViolinMusicVoice = "Violin_Music_Voice"                         %! StringTrioScoreTemplate
                            {                                                                        %! StringTrioScoreTemplate
            <BLANKLINE>
                                % [Violin_Music_Voice measure 1]                                     %! _comment_measure_numbers
                                \clef "treble"                                                       %! DEFAULT_CLEF:_set_status_tag:attach_defaults
                                \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:_attach_color_literal(2)
                            %@% \override ViolinMusicStaff.Clef.color = ##f                          %! DEFAULT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                \set ViolinMusicStaff.forceClef = ##t                                %! DEFAULT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):attach_defaults
                                e'8                                                                  %! baca_make_even_divisions
                                ^ \baca-default-indicator-markup "(Violin)"                          %! DEFAULT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                                [                                                                    %! baca_make_even_divisions
                                \override ViolinMusicStaff.Clef.color = #(x11-color 'violet)         %! DEFAULT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
            <BLANKLINE>
                                e'8                                                                  %! baca_make_even_divisions
            <BLANKLINE>
                                e'8                                                                  %! baca_make_even_divisions
            <BLANKLINE>
                                e'8                                                                  %! baca_make_even_divisions
                                ]                                                                    %! baca_make_even_divisions
            <BLANKLINE>
                                % [Violin_Music_Voice measure 2]                                     %! _comment_measure_numbers
                                e'8                                                                  %! baca_make_even_divisions
                                [                                                                    %! baca_make_even_divisions
            <BLANKLINE>
                                e'8                                                                  %! baca_make_even_divisions
            <BLANKLINE>
                                e'8                                                                  %! baca_make_even_divisions
                                ]                                                                    %! baca_make_even_divisions
            <BLANKLINE>
                                % [Violin_Music_Voice measure 3]                                     %! _comment_measure_numbers
                                e'8                                                                  %! baca_make_even_divisions
                                [                                                                    %! baca_make_even_divisions
            <BLANKLINE>
                                e'8                                                                  %! baca_make_even_divisions
            <BLANKLINE>
                                e'8                                                                  %! baca_make_even_divisions
            <BLANKLINE>
                                e'8                                                                  %! baca_make_even_divisions
                                ]                                                                    %! baca_make_even_divisions
            <BLANKLINE>
                                % [Violin_Music_Voice measure 4]                                     %! _comment_measure_numbers
                                e'8                                                                  %! baca_make_even_divisions
                                [                                                                    %! baca_make_even_divisions
            <BLANKLINE>
                                e'8                                                                  %! baca_make_even_divisions
            <BLANKLINE>
                                e'8                                                                  %! baca_make_even_divisions
                                ]                                                                    %! baca_make_even_divisions
            <BLANKLINE>
                                % [Violin_Music_Voice measure 5]                                     %! _comment_measure_numbers
                                e'8                                                                  %! baca_make_even_divisions
                                [                                                                    %! baca_make_even_divisions
            <BLANKLINE>
                                e'8                                                                  %! baca_make_even_divisions
            <BLANKLINE>
                                e'8                                                                  %! baca_make_even_divisions
            <BLANKLINE>
                                e'8                                                                  %! baca_make_even_divisions
                                ]                                                                    %! baca_make_even_divisions
            <BLANKLINE>
                            }                                                                        %! StringTrioScoreTemplate
            <BLANKLINE>
                        }                                                                            %! StringTrioScoreTemplate
            <BLANKLINE>
                        \tag Viola                                                                   %! ScoreTemplate(5)
                        \context ViolaMusicStaff = "Viola_Music_Staff"                               %! StringTrioScoreTemplate
                        {                                                                            %! StringTrioScoreTemplate
            <BLANKLINE>
                            \context ViolaMusicVoice = "Viola_Music_Voice"                           %! StringTrioScoreTemplate
                            {                                                                        %! StringTrioScoreTemplate
            <BLANKLINE>
                                % [Viola_Music_Voice measure 1]                                      %! _comment_measure_numbers
                                \clef "alto"                                                         %! DEFAULT_CLEF:_set_status_tag:attach_defaults
                                \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:_attach_color_literal(2)
                            %@% \override ViolaMusicStaff.Clef.color = ##f                           %! DEFAULT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                \set ViolaMusicStaff.forceClef = ##t                                 %! DEFAULT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):attach_defaults
                                R1 * 1/2                                                             %! _call_rhythm_commands
                                ^ \baca-default-indicator-markup "(Viola)"                           %! DEFAULT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                                \override ViolaMusicStaff.Clef.color = #(x11-color 'violet)          %! DEFAULT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
            <BLANKLINE>
                                % [Viola_Music_Voice measure 2]                                      %! _comment_measure_numbers
                                R1 * 3/8                                                             %! _call_rhythm_commands
            <BLANKLINE>
                                % [Viola_Music_Voice measure 3]                                      %! _comment_measure_numbers
                                R1 * 1/2                                                             %! _call_rhythm_commands
            <BLANKLINE>
                                % [Viola_Music_Voice measure 4]                                      %! _comment_measure_numbers
                                R1 * 3/8                                                             %! _call_rhythm_commands
            <BLANKLINE>
                                % [Viola_Music_Voice measure 5]                                      %! _comment_measure_numbers
                                R1 * 1/2                                                             %! _call_rhythm_commands
            <BLANKLINE>
                            }                                                                        %! StringTrioScoreTemplate
            <BLANKLINE>
                        }                                                                            %! StringTrioScoreTemplate
            <BLANKLINE>
                        \tag Cello                                                                   %! ScoreTemplate(5)
                        \context CelloMusicStaff = "Cello_Music_Staff"                               %! StringTrioScoreTemplate
                        {                                                                            %! StringTrioScoreTemplate
            <BLANKLINE>
                            \context CelloMusicVoice = "Cello_Music_Voice"                           %! StringTrioScoreTemplate
                            {                                                                        %! StringTrioScoreTemplate
            <BLANKLINE>
                                % [Cello_Music_Voice measure 1]                                      %! _comment_measure_numbers
                                \clef "bass"                                                         %! DEFAULT_CLEF:_set_status_tag:attach_defaults
                                \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:_attach_color_literal(2)
                            %@% \override CelloMusicStaff.Clef.color = ##f                           %! DEFAULT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                \set CelloMusicStaff.forceClef = ##t                                 %! DEFAULT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):attach_defaults
                                R1 * 1/2                                                             %! _call_rhythm_commands
                                ^ \baca-default-indicator-markup "(Cello)"                           %! DEFAULT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                                \override CelloMusicStaff.Clef.color = #(x11-color 'violet)          %! DEFAULT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
            <BLANKLINE>
                                % [Cello_Music_Voice measure 2]                                      %! _comment_measure_numbers
                                R1 * 3/8                                                             %! _call_rhythm_commands
            <BLANKLINE>
                                % [Cello_Music_Voice measure 3]                                      %! _comment_measure_numbers
                                R1 * 1/2                                                             %! _call_rhythm_commands
            <BLANKLINE>
                                % [Cello_Music_Voice measure 4]                                      %! _comment_measure_numbers
                                R1 * 3/8                                                             %! _call_rhythm_commands
            <BLANKLINE>
                                % [Cello_Music_Voice measure 5]                                      %! _comment_measure_numbers
                                R1 * 1/2                                                             %! _call_rhythm_commands
            <BLANKLINE>
                            }                                                                        %! StringTrioScoreTemplate
            <BLANKLINE>
                        }                                                                            %! StringTrioScoreTemplate
            <BLANKLINE>
                    >>                                                                               %! StringTrioScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! StringTrioScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! StringTrioScoreTemplate

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bol_measure_numbers',
        '_commands',
        '_deactivate',
        '_local_measure_numbers',
        '_page_count',
        '_partial_score',
        '_tags',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        commands: abjad.OrderedDict = None,
        deactivate: bool = None,
        local_measure_numbers: bool = None,
        page_count: int = None,
        partial_score: int = None,
        tags: typing.List[str] = None,
        ) -> None:
        tags = scoping.Command._preprocess_tags(tags)
        assert scoping.Command._validate_tags(tags), repr(tags)
        if abjad.tags.BREAK not in tags:
            tags.append(abjad.tags.BREAK)
        self._tags = tags
        self._bol_measure_numbers: typing.List[int] = []
        self._deactivate = deactivate
        if local_measure_numbers is not None:
            local_measure_numbers = bool(local_measure_numbers)
        self._local_measure_numbers = local_measure_numbers
        if page_count is not None:
            assert isinstance(page_count, int), repr(page_count)
        self._page_count = page_count
        if partial_score is not None:
            assert isinstance(partial_score, int), repr(partial_score)
        self._partial_score = partial_score
        if commands is not None:
            commands_ = abjad.OrderedDict()
            for measure_number, list_ in commands.items():
                commands_[measure_number] = []
                for command in list_:
                    command_ = abjad.new(
                        command,
                        deactivate=self.deactivate,
                        tags=self.tags,
                        )
                    commands_[measure_number].append(command_)
            commands = commands_
        self._commands = commands

    ### SPECIAL METHODS ###

    def __call__(self, context: abjad.Context = None) -> None:
        """
        Calls map on ``context``.
        """
        if context is None:
            return
        skips = classes.Selection(context).skips()
        measure_count = self.partial_score or len(skips)
        final_measure_number = self.first_measure_number + measure_count - 1
        literal = abjad.LilyPondLiteral(r'\autoPageBreaksOff', 'before')
        abjad.attach(
            literal,
            skips[0],
            deactivate=self.deactivate,
            tag=self.tag.prepend('BreakMeasureMap(1)'),
            )
        for skip in skips[:measure_count]:
            if not abjad.inspect(skip).has_indicator(LBSD):
                literal = abjad.LilyPondLiteral(r'\noBreak', 'before')
                abjad.attach(
                    literal,
                    skip,
                    deactivate=self.deactivate,
                    tag=self.tag.prepend('BreakMeasureMap(2)'),
                    )
        assert self.commands is not None
        for measure_number, commands in self.commands.items():
            if final_measure_number < measure_number:
                message = f'score ends at measure {final_measure_number}'
                message += f' (not {measure_number}).'
                raise Exception(message)
            for command in commands:
                command(context)

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return abjad.FormatSpecification()

    ### PUBLIC PROPERTIES ###

    @property
    def bol_measure_numbers(self) -> typing.List[int]:
        """
        Gets beginning-of-line measure numbers.

        Populated during ``baca.breaks()`` initialization.
        """
        return  self._bol_measure_numbers

    @property
    def commands(self) -> typing.Optional[abjad.OrderedDict]:
        """
        Gets commands.
        """
        return self._commands

    @property
    def deactivate(self) -> typing.Optional[bool]:
        """
        Is true when tags should write deactivated.
        """
        return self._deactivate

    @property
    def first_measure_number(self) -> int:
        """
        Gets first measure number.
        """
        return self.bol_measure_numbers[0]

    @property
    def local_measure_numbers(self) -> typing.Optional[bool]:
        """
        Is true when segment measures numbers starting from 1.
        """
        return self._local_measure_numbers

    @property
    def page_count(self) -> typing.Optional[int]:
        """
        Gets page count.
        """
        return self._page_count

    @property
    def partial_score(self) -> typing.Optional[int]:
        """
        Gets number of measures in partial score.

        Set to a positive integer to cap total measures generated.

        Leave set to none to render all measures in score.
        """
        return self._partial_score

    @property
    def tag(self) -> abjad.Tag:
        """
        Gets tag.
        """
        if self.tags:
            return abjad.Tag.from_words(self.tags)
        else:
            return abjad.Tag()

    @property
    def tags(self) -> typing.List[str]:
        """
        Gets tags.
        """
        assert scoping.Command._validate_tags(self._tags), repr(self._tags)
        return self._tags[:]

class HorizontalSpacingSpecifier(object):
    r"""
    Horizontal spacing specifier.

    >>> from abjadext import rmakers

    ..  container:: example

        No spacing command:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(8, 16), (4, 8), (2, 4), (1, 2)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_even_divisions(),
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
                        \time 8/16                                                                   %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 2/4                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 1/2                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
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
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            e'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            e'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            e'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
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

        Null spacing command:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.HorizontalSpacingSpecifier(),
        ...     time_signatures=[(8, 16), (4, 8), (2, 4), (1, 2)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_even_divisions(),
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
                        \baca-new-spacing-section #1 #8                                              %! HorizontalSpacingSpecifier(1):SPACING
                        \time 8/16                                                                   %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #8                                              %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #8                                              %! HorizontalSpacingSpecifier(1):SPACING
                        \time 2/4                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #8                                              %! HorizontalSpacingSpecifier(1):SPACING
                        \time 1/2                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
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
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            e'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            e'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            e'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
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

        Measurewise proportional spacing based on minimum duration per measure:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.HorizontalSpacingSpecifier(
        ...         multiplier=abjad.Multiplier(1),
        ...         ),
        ...     time_signatures=[(8, 16), (4, 8), (2, 4), (1, 2)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_even_divisions(),
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
                        \baca-new-spacing-section #1 #8                                              %! HorizontalSpacingSpecifier(1):SPACING
                        \time 8/16                                                                   %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #8                                              %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #8                                              %! HorizontalSpacingSpecifier(1):SPACING
                        \time 2/4                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #8                                              %! HorizontalSpacingSpecifier(1):SPACING
                        \time 1/2                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
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
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            e'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            e'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            e'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
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

        Measurewise proportional spacing based on twice the minimum duration
        per measure:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.HorizontalSpacingSpecifier(
        ...         multiplier=abjad.Multiplier(2),
        ...         ),
        ...     time_signatures=[(8, 16), (4, 8), (2, 4), (1, 2)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_even_divisions(),
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
                        \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 8/16                                                                   %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 2/4                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 1/2                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
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
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            e'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            e'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            e'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
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

        Measurewise proportional spacing based on twice the minimum duration
        per measure with minimum duration equal to an eighth note:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.HorizontalSpacingSpecifier(
        ...         multiplier=abjad.Multiplier(2),
        ...         minimum_duration=abjad.Duration(1, 8),
        ...         ),
        ...     time_signatures=[(8, 16), (4, 8), (2, 4), (1, 2)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_even_divisions(),
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
                        \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 8/16                                                                   %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 2/4                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 1/2                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
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
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            e'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            e'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            e'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
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

        Works with accelerando and ritardando figures:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.HorizontalSpacingSpecifier(
        ...         minimum_duration=abjad.Duration(1, 8),
        ...         ),
        ...     time_signatures=[(4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.pitches('E4 F4'),
        ...     baca.RhythmCommand(
        ...         rhythm_maker=rmakers.AccelerandoRhythmMaker(
        ...             beam_specifier=rmakers.BeamSpecifier(
        ...             use_feather_beams=True,
        ...                 ),
        ...             interpolation_specifiers=rmakers.InterpolationSpecifier(
        ...                 start_duration=abjad.Duration(1, 8),
        ...                 stop_duration=abjad.Duration(1, 20),
        ...                 written_duration=abjad.Duration(1, 16),
        ...                 ),
        ...             tuplet_specifier=rmakers.TupletSpecifier(
        ...                 duration_bracket=True,
        ...                 ),
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
                        \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #16                                             %! HorizontalSpacingSpecifier(1):SPACING
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
                            \override TupletNumber.text = \markup {
                                \scale
                                    #'(0.75 . 0.75)
                                    \score
                                        {
                                            \new Score
                                            \with
                                            {
                                                \override SpacingSpanner.spacing-increment = #0.5
                                                proportionalNotationDuration = ##f
                                            }
                                            <<
                                                \new RhythmicStaff
                                                \with
                                                {
                                                    \remove Time_signature_engraver
                                                    \remove Staff_symbol_engraver
                                                    \override Stem.direction = #up
                                                    \override Stem.length = #5
                                                    \override TupletBracket.bracket-visibility = ##t
                                                    \override TupletBracket.direction = #up
                                                    \override TupletBracket.minimum-length = #4
                                                    \override TupletBracket.padding = #1.25
                                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                    \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                                    \override TupletNumber.font-size = #0
                                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                    tupletFullLength = ##t
                                                }
                                                {
                                                    c'2
                                                }
                                            >>
                                            \layout {
                                                indent = #0
                                                ragged-right = ##t
                                            }
                                        }
                                }
                            \times 1/1 {
            <BLANKLINE>
                                % [Music_Voice measure 1]                                            %! _comment_measure_numbers
                                \once \override Beam.grow-direction = #right
                                e'16 * 63/32
                                [
            <BLANKLINE>
                                f'16 * 115/64
            <BLANKLINE>
                                e'16 * 91/64
            <BLANKLINE>
                                f'16 * 35/32
            <BLANKLINE>
                                e'16 * 29/32
            <BLANKLINE>
                                f'16 * 13/16
                                ]
            <BLANKLINE>
                            }
                            \revert TupletNumber.text
            <BLANKLINE>
                            \override TupletNumber.text = \markup {
                                \scale
                                    #'(0.75 . 0.75)
                                    \score
                                        {
                                            \new Score
                                            \with
                                            {
                                                \override SpacingSpanner.spacing-increment = #0.5
                                                proportionalNotationDuration = ##f
                                            }
                                            <<
                                                \new RhythmicStaff
                                                \with
                                                {
                                                    \remove Time_signature_engraver
                                                    \remove Staff_symbol_engraver
                                                    \override Stem.direction = #up
                                                    \override Stem.length = #5
                                                    \override TupletBracket.bracket-visibility = ##t
                                                    \override TupletBracket.direction = #up
                                                    \override TupletBracket.minimum-length = #4
                                                    \override TupletBracket.padding = #1.25
                                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                    \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                                    \override TupletNumber.font-size = #0
                                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                    tupletFullLength = ##t
                                                }
                                                {
                                                    c'4.
                                                }
                                            >>
                                            \layout {
                                                indent = #0
                                                ragged-right = ##t
                                            }
                                        }
                                }
                            \times 1/1 {
            <BLANKLINE>
                                % [Music_Voice measure 2]                                            %! _comment_measure_numbers
                                \once \override Beam.grow-direction = #right
                                e'16 * 117/64
                                [
            <BLANKLINE>
                                f'16 * 99/64
            <BLANKLINE>
                                e'16 * 69/64
            <BLANKLINE>
                                f'16 * 13/16
            <BLANKLINE>
                                e'16 * 47/64
                                ]
            <BLANKLINE>
                            }
                            \revert TupletNumber.text
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

        Minimum duration in each measure is taken from the **nonmultiplied**
        duration of each note.

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_breaks',
        '_fermata_measure_numbers',
        '_fermata_measure_duration',
        '_fermata_start_offsets',
        '_first_measure_number',
        '_forbid_segment_maker_adjustments',
        '_measure_count',
        '_measures',
        '_minimum_duration',
        '_multiplier',
        '_overriden_fermata_measures',
        '_phantom',
        )

    _magic_lilypond_eol_adjustment = abjad.Multiplier(35, 24)

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        breaks: BreakMeasureMap = None,
        fermata_measure_numbers: typing.List[int] = None,
        fermata_measure_duration: typings.IntegerPair = (1, 4),
        first_measure_number: int = None,
        measure_count: int = None,
        measures: abjad.OrderedDict = None,
        minimum_duration: typings.IntegerPair = None,
        multiplier: typings.IntegerPair = None,
        phantom: bool = None,
        ) -> None:
        if breaks is not None:
            assert isinstance(breaks, BreakMeasureMap), repr(breaks)
        self._breaks = breaks
        if fermata_measure_numbers is not None:
            assert isinstance(fermata_measure_numbers, collections.Iterable)
            assert all(isinstance(_, int) for _ in fermata_measure_numbers)
        self._fermata_measure_numbers = fermata_measure_numbers or []
        duration_ = None
        if fermata_measure_duration is not None:
            duration_ = abjad.Duration(fermata_measure_duration)
        self._fermata_measure_duration = duration_
        self._fermata_start_offsets: typing.List[abjad.Offset] = []
        if first_measure_number is not None:
            assert isinstance(first_measure_number, int)
            assert 1 <= first_measure_number
        self._first_measure_number = first_measure_number
        self._forbid_segment_maker_adjustments: typing.Optional[bool] = None
        if measure_count is not None:
            assert isinstance(measure_count, int)
            assert 0 <= measure_count
        self._measure_count = measure_count
        if minimum_duration is not None:
            minimum_duration = abjad.Duration(minimum_duration)
        self._minimum_duration = minimum_duration
        if multiplier is not None:
            multiplier = abjad.Multiplier(multiplier)
        self._multiplier = multiplier
        if measures is not None:
            assert isinstance(measures, abjad.OrderedDict), repr(measures)
        else:
            measures = abjad.OrderedDict()
        self._measures = measures
        self._overriden_fermata_measures: typing.List[int] = []
        if phantom is not None:
            phantom = bool(phantom)
        self._phantom = phantom

    ### SPECIAL METHODS ###

    def __call__(self, segment_maker=None) -> None:
        """
        Calls command on ``segment_maker``.
        """
        score = segment_maker.score
        skips = classes.Selection(score['Global_Skips']).skips()
        programmatic = True
        if self.measures and len(self.measures) == len(skips):
            programmatic = False
        if programmatic:
            leaves = abjad.iterate(score).leaves(grace_notes=False)
            method = self._get_minimum_durations_by_measure
            minimum_durations_by_measure = method(skips, leaves)
        else:
            minimum_durations_by_measure = []
        string = '_fermata_start_offsets'
        self._fermata_start_offsets = getattr(segment_maker, string, [])
        first_measure_number = self.first_measure_number or 1
        total = len(skips)
        for measure_index, skip in enumerate(skips):
            measure_number = first_measure_number + measure_index
            duration, eol_adjusted, duration_ = self._calculate_duration(
                measure_index,
                measure_number,
                skip,
                minimum_durations_by_measure,
                )
            if self.phantom and measure_index == total - 1:
                duration = abjad.Duration(1, 4)
            spacing_section = indicators.SpacingSection(duration=duration)
            tag = abjad.Tag(abjad.tags.SPACING)
            abjad.attach(
                spacing_section,
                skip,
                tag=tag.prepend('HorizontalSpacingSpecifier(1)'),
                )
            string_ = self._make_annotation(duration, eol_adjusted, duration_)
            if measure_index < total - 1:
                tag = abjad.Tag(abjad.tags.SPACING_MARKUP)
                if not self.phantom and measure_index == total - 2:
                    next_skip = skips[measure_index + 1]
                    next_measure_index = measure_index + 1
                    next_measure_number = measure_number + 1
                    result = self._calculate_duration(
                        next_measure_index,
                        next_measure_number,
                        next_skip,
                        minimum_durations_by_measure,
                        )
                    next_string = self._make_annotation(*result)
                    string = r'- \baca-start-spm-both'
                    string += f' "{string_}" "{next_string}"'
                else:
                    string = r'- \baca-start-spm-left-only'
                    string += f' "{string_}"'
                start_text_span = abjad.StartTextSpan(
                    command=r'\bacaStartTextSpanSPM',
                    left_text=string,
                    )
                abjad.attach(
                    start_text_span,
                    skip,
                    context='GlobalSkips',
                    deactivate=True,
                    tag=tag,
                    )
            if 0 < measure_index:
                tag = abjad.Tag(abjad.tags.SPACING_MARKUP)
                stop_text_span = abjad.StopTextSpan(
                    command=r'\bacaStopTextSpanSPM',
                    )
                abjad.attach(
                    stop_text_span,
                    skip,
                    context='GlobalSkips',
                    deactivate=True,
                    tag=tag,
                    )

    ### PRIVATE METHODS ###

    def _calculate_duration(
        self,
        measure_index,
        measure_number,
        skip,
        minimum_durations_by_measure,
        ):
        if (self._is_fermata_measure(measure_number, skip) and
            measure_number in self._overriden_fermata_measures):
            duration = self.measures[measure_number]
            duration = abjad.NonreducedFraction(duration)
        elif (self.fermata_measure_duration is not None and
            self._is_fermata_measure(measure_number, skip)):
            duration = self.fermata_measure_duration
        elif self.measures and measure_number in self.measures:
            duration = self.measures[measure_number]
            duration = abjad.NonreducedFraction(duration)
        else:
            duration = minimum_durations_by_measure[measure_index]
            if self.minimum_duration is not None:
                if self.minimum_duration < duration:
                    duration = self.minimum_duration
            if self.multiplier is not None:
                duration = duration / self.multiplier
        eol_adjusted, duration_ = False, None
        if measure_number in self.eol_measure_numbers:
            duration_ = duration
            duration *= self._magic_lilypond_eol_adjustment
            eol_adjusted = True
        return duration, eol_adjusted, duration_

    def _coerce_measure_number(self, measure_number, force_local=False):
        if measure_number == 0:
            raise Exception(f'zero-valued measure number not allowed.')
        if force_local is True:
            measure_number = self.first_measure_number + measure_number - 1
        if measure_number < 0:
            measure_number = self.final_measure_number - abs(measure_number) + 1
        if measure_number < self.first_measure_number:
            measure_number += self.first_measure_number - 1
        if self.final_measure_number < measure_number:
            raise Exception(f'measure number {measure_number} greater than'
                f' last measure number ({self.final_measure_number}).')
        return measure_number

    def _get_minimum_durations_by_measure(self, skips, leaves):
        measure_timespans = []
        durations_by_measure = []
        for skip in skips:
            measure_timespan = abjad.inspect(skip).timespan()
            measure_timespans.append(measure_timespan)
            durations_by_measure.append([])
        leaf_timespans = set()
        leaf_count = 0
        for leaf in leaves:
            leaf_timespan = abjad.inspect(leaf).timespan()
            leaf_duration = leaf_timespan.duration
            if leaf.multiplier is not None:
                leaf_duration = leaf_duration / leaf.multiplier
            pair = (leaf_timespan, leaf_duration)
            leaf_timespans.add(pair)
            leaf_count += 1
        measure_index = 0
        measure_timespan = measure_timespans[measure_index]
        leaf_timespans = list(leaf_timespans)
        leaf_timespans.sort(key=lambda _: _[0].start_offset)
        start_offset = 0
        for pair in leaf_timespans:
            leaf_timespan, leaf_duration = pair
            assert start_offset <= leaf_timespan.start_offset
            start_offset = leaf_timespan.start_offset
            if leaf_timespan.starts_during_timespan(measure_timespan):
                durations_by_measure[measure_index].append(leaf_duration)
            else:
                measure_index += 1
                if len(measure_timespans) <= measure_index:
                    continue
                measure_timespan = measure_timespans[measure_index]
                assert leaf_timespan.starts_during_timespan(measure_timespan)
                durations_by_measure[measure_index].append(leaf_duration)
        minimum_durations_by_measure = [min(_) for _ in durations_by_measure]
        return minimum_durations_by_measure

    def _is_fermata_measure(self, measure_number, skip):
        if (self.fermata_measure_numbers and
            measure_number in self.fermata_measure_numbers):
            return True
        measure_timespan = abjad.inspect(skip).timespan()
        return measure_timespan.start_offset in self._fermata_start_offsets

    def _make_annotation(self, duration, eol_adjusted, duration_):
        if eol_adjusted:
            multiplier = self._magic_lilypond_eol_adjustment
            string = f'[[{duration_!s} * {multiplier!s}]]'
        else:
            string = f'[{duration!s}]'
        return string

    ### PUBLIC PROPERTIES ###

    @property
    def bol_measure_numbers(self) -> typing.List[int]:
        """
        Gets beginning-of-line measure numbers.

        ..  container:: example

            >>> breaks = baca.breaks(
            ...     baca.page([1, 15, (10, 20)], [9, 115, (10, 20)])
            ...     )
            >>> spacing = baca.scorewide_spacing(
            ...     (95, 18, [103, 105]),
            ...     breaks=breaks,
            ...     fallback_duration=(1, 20),
            ...     )

            >>> spacing.bol_measure_numbers
            [95, 103]

        """
        bol_measure_numbers = []
        if self.breaks and self.breaks.bol_measure_numbers:
            first_breaks_measure_number = self.breaks.bol_measure_numbers[0]
            assert isinstance(self.first_measure_number, int)
            for bol_measure_number in self.breaks.bol_measure_numbers:
                offset = bol_measure_number - first_breaks_measure_number
                bol_measure_number = self.first_measure_number + offset
                bol_measure_numbers.append(bol_measure_number)
        return bol_measure_numbers

    @property
    def breaks(self) -> typing.Optional[BreakMeasureMap]:
        """
        Gets break measure map.
        """
        return self._breaks

    @property
    def eol_measure_numbers(self) -> typing.List[int]:
        """
        Gets end-of-line measure numbers.

        ..  container:: example

            >>> breaks = baca.breaks(
            ...     baca.page([1, 15, (10, 20)], [9, 115, (10, 20)])
            ...     )
            >>> spacing = baca.scorewide_spacing(
            ...     (95, 18, [103, 105]),
            ...     breaks=breaks,
            ...     fallback_duration=(1, 20),
            ...     )

            >>> spacing.eol_measure_numbers
            [102, 112]

        """
        eol_measure_numbers = []
        for bol_measure_number in self.bol_measure_numbers[1:]:
            eol_measure_number = bol_measure_number - 1
            eol_measure_numbers.append(eol_measure_number)
        if (self.final_measure_number and
            not self.phantom and
            self.final_measure_number not in eol_measure_numbers):
            eol_measure_numbers.append(self.final_measure_number)
        return eol_measure_numbers

    @property
    def fermata_measure_duration(self) -> typing.Optional[abjad.Duration]:
        """
        Gets fermata measure duration.

        Sets fermata measures to exactly this duration when set; ignores
        minimum duration and multiplier.
        """
        return self._fermata_measure_duration

    @property
    def fermata_measure_numbers(self) -> typing.List[int]:
        """
        Gets fermata measure numbers.

        ..  container:: example

            >>> breaks = baca.breaks(
            ...     baca.page([1, 15, (10, 20)], [9, 115, (10, 20)])
            ...     )
            >>> spacing = baca.scorewide_spacing(
            ...     (95, 18, [103, 105]),
            ...     breaks=breaks,
            ...     fallback_duration=(1, 20),
            ...     )

            >>> spacing.fermata_measure_numbers
            [103, 105]

        """
        return self._fermata_measure_numbers

    @property
    def final_measure_number(self) -> typing.Optional[int]:
        """
        Gets last measure number.

        ..  container:: example

            >>> breaks = baca.breaks(
            ...     baca.page([1, 15, (10, 20)], [9, 115, (10, 20)])
            ...     )
            >>> spacing = baca.scorewide_spacing(
            ...     (95, 18, [103, 105]),
            ...     breaks=breaks,
            ...     fallback_duration=(1, 20),
            ...     )

            >>> spacing.final_measure_number
            112

        Returns none when first measure number is not defined.

        Returns none when measure count is not defined.
        """
        if (self.first_measure_number is not None and
            self.measure_count is not None):
            return self.first_measure_number + self.measure_count - 1
        else:
            return None

    @property
    def first_measure_number(self) -> typing.Optional[int]:
        """
        Gets first measure number.

        ..  container:: example

            >>> breaks = baca.breaks(
            ...     baca.page([1, 15, (10, 20)], [9, 115, (10, 20)])
            ...     )
            >>> spacing = baca.scorewide_spacing(
            ...     (95, 18, [103, 105]),
            ...     breaks=breaks,
            ...     fallback_duration=(1, 20),
            ...     )

            >>> spacing.first_measure_number
            95

        """
        return self._first_measure_number

    @property
    def magic_lilypond_eol_adjustment(self):
        """
        Gets magic LilyPond EOL adjustment.

        ..  container

            >>> breaks = baca.breaks(
            ...     baca.page([1, 15, (10, 20)], [9, 115, (10, 20)])
            ...     )
            >>> spacing = baca.scorewide_spacing(
            ...     (95, 18, [103, 105]),
            ...     breaks=breaks,
            ...     fallback_duration=(1, 20),
            ...     )

            >>> spacing.magic_lilypond_eol_adjustment
            Multiplier(35, 24)

        Optically determined to correct LilyPond end-of-line spacing bug.

        Class property.
        """
        return self._magic_lilypond_eol_adjustment

    @property
    def measure_count(self) -> typing.Optional[int]:
        """
        Gets measure count.

        ..  container:: example

            >>> breaks = baca.breaks(
            ...     baca.page([1, 15, (10, 20)], [9, 115, (10, 20)])
            ...     )
            >>> spacing = baca.scorewide_spacing(
            ...     (95, 18, [103, 105]),
            ...     breaks=breaks,
            ...     fallback_duration=(1, 20),
            ...     )

            >>> spacing.measure_count
            18

        """
        return self._measure_count

    @property
    def measures(self) -> abjad.OrderedDict:
        """
        Gets measure overrides.
        """
        return self._measures

    @property
    def minimum_duration(self) -> typing.Optional[abjad.NonreducedFraction]:
        """
        Gets minimum duration.

        Defaults to none and interprets none equal to ``1/8``.
        """
        return self._minimum_duration

    @property
    def multiplier(self) -> typing.Optional[abjad.Multiplier]:
        """
        Gets multiplier.
        """
        return self._multiplier

    @property
    def phantom(self) -> typing.Optional[bool]:
        """
        Is true when segment concludes with phantom measure.
        """
        return self._phantom
    
    ### PUBLIC METHODS ###

    def override(
        self,
        measures: typing.Union[int, tuple, list],
        pair: typing.Union[typings.IntegerPair, str],
        *,
        fermata: bool = None,
        force_local: bool = None,
        ) -> None:
        r"""
        Overrides ``measures`` with spacing ``pair``.

        ..  container:: example

            >>> breaks = baca.breaks(
            ...     baca.page([1, 15, (10, 20)]),
            ...     )
            >>> spacing = baca.scorewide_spacing(
            ...     (95, 5, []),
            ...     breaks=breaks,
            ...     fallback_duration=(1, 20),
            ...     )

            >>> abjad.f(spacing.measures)
            abjad.OrderedDict(
                [
                    (
                        95,
                        abjad.NonreducedFraction(1, 20),
                        ),
                    (
                        96,
                        abjad.NonreducedFraction(1, 20),
                        ),
                    (
                        97,
                        abjad.NonreducedFraction(1, 20),
                        ),
                    (
                        98,
                        abjad.NonreducedFraction(1, 20),
                        ),
                    (
                        99,
                        abjad.NonreducedFraction(1, 20),
                        ),
                    ]
                )

            >>> spacing.override((1, -1), (1, 24))
            >>> abjad.f(spacing.measures)
            abjad.OrderedDict(
                [
                    (
                        95,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        96,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        97,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        98,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        99,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    ]
                )

            Works with measure number:

            >>> spacing.override((1, -1), (1, 16))
            >>> spacing.override(95, (1, 24))
            >>> abjad.f(spacing.measures)
            abjad.OrderedDict(
                [
                    (
                        95,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        96,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        97,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        98,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        99,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    ]
                )

            Works with range of measure numbers:

            >>> spacing.override((1, -1), (1, 16))
            >>> spacing.override((95, 97), (1, 24))
            >>> abjad.f(spacing.measures)
            abjad.OrderedDict(
                [
                    (
                        95,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        96,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        97,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        98,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        99,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    ]
                )

            Works with list of measure numbers:

            >>> spacing.override((1, -1), (1, 16))
            >>> spacing.override([95, 97, 99], (1, 24))
            >>> abjad.f(spacing.measures)
            abjad.OrderedDict(
                [
                    (
                        95,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        96,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        97,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        98,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        99,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    ]
                )

            Works with negative indices:

            >>> spacing.override((1, -1), (1, 16))
            >>> spacing.override([-3, -1], (1, 24))
            >>> abjad.f(spacing.measures)
            abjad.OrderedDict(
                [
                    (
                        95,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        96,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        97,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        98,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        99,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    ]
                )

        ..  container:: example exception

            Raises exception when measures is not int, pair or list:

            >>> spacing.override('all', (1, 16))
            Traceback (most recent call last):
                ...
            TypeError: measures must be int, pair or list (not 'all').

        """
        measures_ = []
        duration = abjad.NonreducedFraction(pair)
        if isinstance(measures, int):
            number = self._coerce_measure_number(
                measures,
                force_local=force_local,
                )
            self.measures[number] = duration
            measures_.append(number)
        elif isinstance(measures, tuple):
            assert len(measures) == 2, repr(measures)
            start_measure, stop_measure = measures
            start_measure = self._coerce_measure_number(
                start_measure,
                force_local=force_local,
                )
            stop_measure = self._coerce_measure_number(
                stop_measure,
                force_local=force_local,
                )
            for number in range(start_measure, stop_measure + 1):
                self.measures[number] = duration
                measures_.append(number)
        elif isinstance(measures, list):
            for measure in measures:
                number = self._coerce_measure_number(
                    measure,
                    force_local=force_local,
                    )
                self.measures[number] = duration
                measures_.append(number)
        else:
            message = f'measures must be int, pair or list (not {measures!r}).'
            raise TypeError(message)
        if fermata:
            self._overriden_fermata_measures.extend(measures_)


class LBSD(object):
    """
    Line-break system details.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_alignment_distances',
        '_y_offset',
        )

    _override = r'\overrideProperty'
    _override += ' Score.NonMusicalPaperColumn.line-break-system-details'

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        y_offset=None,
        alignment_distances=None,
        ):
        self._y_offset = y_offset
        if alignment_distances is not None:
            assert isinstance(alignment_distances, collections.Iterable)
            alignment_distances = tuple(alignment_distances)
        self._alignment_distances = alignment_distances

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = abjad.LilyPondFormatBundle()
        alignment_distances = ' '.join(
            str(_) for _ in self.alignment_distances
            )
        string = rf"\baca-lbsd #{self.y_offset} #'({alignment_distances})"
        bundle.before.commands.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def alignment_distances(self):
        """
        Gets alignment distances.
        """
        return self._alignment_distances

    @property
    def y_offset(self):
        """
        Gets Y offset.
        """
        return self._y_offset

class PageSpecifier(object):
    """
    Page specifier.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        '_systems',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        number: int = None,
        systems: typing.List[typing.Union[list, 'SystemSpecifier']] = None,
        ) -> None:
        if number is not None:
            assert isinstance(number, int), repr(number)
            assert 1 <= number, repr(number)
        self._number = number
        if systems is not None:
            y_offsets: list = []
            for system in systems:
                if isinstance(system, SystemSpecifier):
                    y_offset = system.y_offset
                elif isinstance(system, list):
                    y_offset = system[1]
                if y_offset in y_offsets:
                    message = f'systems overlap at Y-offset {y_offset}.'
                    raise Exception(message)
                else:
                    y_offsets.append(y_offset)
        self._systems = systems

    ### PUBLIC PROPERTIES ###

    @property
    def number(self) -> typing.Optional[int]:
        """
        Gets page number.
        """
        return self._number

    @property
    def systems(self) -> typing.Optional[
        typing.List[typing.Union[list, 'SystemSpecifier']]
        ]:
        """
        Gets systems.
        """
        return self._systems

class SystemSpecifier(object):
    """
    System specifier.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_distances',
        '_measure',
        '_y_offset',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        distances: typing.Iterable[typings.Number] = None,
        measure: int = None,
        y_offset: typings.Number = None,
        ) -> None:
        distances_: typing.Optional[typing.List[typings.Number]] = None
        if distances is not None:
            assert isinstance(distances, collections.Iterable), repr(distances)
            for distance in distances:
                assert isinstance(distance, (int, float)), repr(distance)
            distances_ = list(distances)
        else:
            distances_ = None
        self._distances = distances_
        if measure is not None:
            assert isinstance(measure, int), repr(measure)
        self._measure = measure
        if y_offset is not None:
            assert isinstance(y_offset, (int, float)), repr(y_offset)
        self._y_offset = y_offset

    ### PUBLIC PROPERTIES ###

    @property
    def distances(self) -> typing.Optional[typing.List[typings.Number]]:
        """
        Gets distances.
        """
        return self._distances

    @property
    def measure(self) -> typing.Optional[int]:
        """
        Gets start measure.
        """
        return self._measure

    @property
    def y_offset(self) -> typing.Optional[typings.Number]:
        """
        Gets Y-offset.
        """
        return self._y_offset

class TimeSignatureMaker(object):
    """
    Time-signature-maker.

    ..  container:: example

        >>> time_signatures = [
        ...     [(1, 16), (2, 16), (3, 16)],
        ...     [(1, 8), (2, 8), (3, 8)],
        ...     ]
        >>> maker = baca.TimeSignatureMaker(
        ...     time_signatures=time_signatures,
        ...     count=5,
        ...     fermata_measures=[5],
        ...     )
        >>> maker.run()
        [(1, 16), (2, 16), (3, 16), (1, 8), TimeSignature((1, 4))]

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_count',
        '_fermata_measures',
        '_rotation',
        '_time_signatures',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        time_signatures,
        *,
        count: int = None,
        fermata_measures: typing.List[int] = None,
        rotation: int = None,
        ) -> None:
        self._time_signatures = time_signatures
        if count is not None:
            assert isinstance(count, int), repr(count)
        self._count = count
        if fermata_measures is not None:
            assert isinstance(count, int), repr(count)
        self._fermata_measures = fermata_measures
        self._rotation = rotation

    ### PRIVATE METHODS ###

    def _normalize_fermata_measures(self):
        fermata_measures = []
        if self.fermata_measures is None:
            return fermata_measures
        for n in self.fermata_measures:
            if 0 < n:
                fermata_measures.append(n)
            elif n == 0:
                raise ValueError(n)
            else:
                fermata_measures.append(self.count - abs(n) + 1)
        fermata_measures.sort()
        return fermata_measures

    ### PUBLIC PROPERTIES ###

    @property
    def count(self) -> typing.Optional[int]:
        """
        Gets count.
        """
        return self._count

    @property
    def fermata_measures(self) -> typing.Optional[typing.List[int]]:
        """
        Gets fermata measures.
        """
        return self._fermata_measures

    @property
    def rotation(self) -> typing.Optional[int]:
        """
        Gets rotation.
        """
        return self._rotation

    @property
    def time_signatures(self) -> typing.List[abjad.TimeSignature]:
        """
        Gets time signatures.
        """
        return self._time_signatures

    ### PUBLIC METHODS ###

    def run(self) -> typing.List[abjad.TimeSignature]:
        """
        Makes time signatures (without stages).

        Accounts for fermata measures.

        Does not account for stages.
        """
        if not self.count:
            raise Exception('must specify count with run().')
        result = []
        time_signatures = classes.Sequence(self.time_signatures)
        time_signatures = time_signatures.rotate(self.rotation)
        time_signatures = time_signatures.flatten(depth=1)
        time_signatures_ = abjad.CyclicTuple(time_signatures)
        i = 0
        fermata_measures = self._normalize_fermata_measures()
        for j in range(self.count):
            measure_number = j + 1
            if measure_number in fermata_measures:
                result.append(abjad.TimeSignature((1, 4)))
            else:
                time_signature = time_signatures_[i]
                result.append(time_signature)
                i += 1
        return result

### FACTORY FUNCTIONS ###

def breaks(
    *page_specifiers: typing.Any,
    local_measure_numbers: bool = None,
    partial_score: typing.Optional[int] = None,
    ) -> BreakMeasureMap:
    r"""
    Makes breaks.

    ..  container:: example

        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         [1, 20, [15, 20, 20]], 
        ...         [13, 140, [15, 20, 20]], 
        ...         ),
        ...     baca.page(
        ...         [23, 20, [15, 20, 20]],
        ...         ),
        ...     )

    Set ``partial_score`` when rendering only the first measures of a
    score; leave ``partial_score`` set to none when rendering a complete
    score.

    ..  container:: example exception

        Raises exception on misnumbered pages:

        >>> breaks = baca.breaks(
        ...     baca.page(
        ...         [1, 20, [15, 20, 20]], 
        ...         [13, 140, [15, 20, 20]], 
        ...         number=1,
        ...         ),
        ...     baca.page(
        ...         [23, 20, [15, 20, 20]],
        ...         number=9,
        ...         ),
        ...     )
        Traceback (most recent call last):
            ... 
        Exception: page number (9) is not 2.

    ..  container:: example exception

        Raises exception on too few measures:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.StringTrioScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8), (4, 8)],
        ...     breaks=baca.breaks(
        ...         baca.page([99, 0, (10, 20,)]),
        ...         baca.page([109, 0, (10, 20,)]),
        ...         ),
        ...     )

        >>> maker(
        ...     'Violin_Music_Voice',
        ...     baca.make_even_divisions(),
        ...     baca.pitch('E4'),
        ...     )
        >>> lilypond_file = maker.run(environment='docs')
        Traceback (most recent call last):
            ...
        Exception: score ends at measure 103 (not 109).

    """
    commands = abjad.OrderedDict()
    page_count = len(page_specifiers)
    if not page_specifiers:
        return BreakMeasureMap(
            commands=commands,
            page_count=0,
            partial_score=partial_score,
            )
    first_system = page_specifiers[0].systems[0]
    if hasattr(first_system, 'measure'):
        first_measure_number = first_system.measure
    else:
        first_measure_number = first_system[0]
    bol_measure_numbers = []
    for i, page_specifier in enumerate(page_specifiers):
        page_number = i + 1
        if page_specifier.number is not None:
            if page_specifier.number != page_number:
                message = f'page number ({page_specifier.number})'
                message += f' is not {page_number}.'
                raise Exception(message)
        for j, system in enumerate(page_specifier.systems):
            if hasattr(system, 'measure'):
                measure_number = system.measure
            else:
                measure_number = system[0]
            bol_measure_numbers.append(measure_number)
            skip_index = measure_number - first_measure_number
            if hasattr(system, 'y_offset'):
                y_offset = system.y_offset
            else:
                y_offset = system[1]
            if hasattr(system, 'distances'):
                alignment_distances = system.distances
            else:
                alignment_distances = system[2]
            selector = f'baca.skip({skip_index})'
            if j == 0:
                break_ = abjad.LilyPondLiteral(r'\pageBreak')
            else:
                break_ = abjad.LilyPondLiteral(r'\break')
            command = baca_commands.IndicatorCommand(
                indicators=[break_],
                selector=selector,
                )
            alignment_distances = classes.Sequence(alignment_distances)
            alignment_distances = alignment_distances.flatten()
            lbsd = LBSD(
                alignment_distances=alignment_distances,
                y_offset=y_offset,
                )
            lbsd_command = baca_commands.IndicatorCommand(
                indicators=[lbsd],
                selector=selector,
                )
            commands[measure_number] = [command, lbsd_command]
    breaks = BreakMeasureMap(
        commands=commands,
        local_measure_numbers=local_measure_numbers,
        page_count=page_count,
        partial_score=partial_score,
        )
    breaks._bol_measure_numbers.extend(bol_measure_numbers)
    return breaks

def minimum_duration(
    duration: typing.Union[typings.IntegerPair, abjad.Duration],
    ) -> HorizontalSpacingSpecifier:
    """
    Makes horizontal spacing specifier with ``duration`` minimum width.
    """
    return HorizontalSpacingSpecifier(
        minimum_duration=duration,
        )

def page(
    *systems: typing.Any,
    number: int = None
    ) -> PageSpecifier:
    r"""
    Makes page specifier.

    ..  container:: example exception
        
        Raises exception when systems overlap at Y-offset:

        >>> baca.page(
        ...     [1, 60, (20, 20,)],
        ...     [4, 60, (20, 20,)],
        ...     )
        Traceback (most recent call last):
            ...
        Exception: systems overlap at Y-offset 60.

    """
    if systems is None:
        systems_ = None
    else:
        systems_ = []
        prototype = (list, SystemSpecifier)
        for system in systems:
            assert isinstance(system, prototype), repr(system)
            systems_.append(system)
    return PageSpecifier(number=number, systems=systems_)

def scorewide_spacing(
    path: typing.Union[abjad.Path, typing.Tuple[int, int, list]],
    fallback_duration: typings.IntegerPair,
    breaks: BreakMeasureMap = None,
    fermata_measure_duration: typings.IntegerPair = (1, 4),
    ) -> HorizontalSpacingSpecifier:
    r"""
    Makes scorewide spacing.

    :param path: path from which first measure number, measure count,
        and fermata measure numbers metadata will be read;
        triple may be passed directly for tests.

    :param fallback_duration: spacing for measures without override.

    :param breaks: break measure map giving beginning-of-line and
        end-of-line measure numbers.

    :param fermata_measure_duration: spacing for measures found in fermata
        measure numbers path metadata.

    ..  container:: example

        >>> breaks = baca.breaks(
        ...     baca.page([1, 15, (10, 20)], [9, 115, (10, 20)])
        ...     )
        >>> spacing = baca.scorewide_spacing(
        ...     (95, 18, [105, 107]),
        ...     breaks=breaks,
        ...     fallback_duration=(1, 20),
        ...     )

        >>> spacing.bol_measure_numbers
        [95, 103]

        >>> spacing.eol_measure_numbers
        [102, 112]

        >>> spacing.fermata_measure_numbers
        [105, 107]

        >>> spacing.first_measure_number
        95

        >>> spacing.final_measure_number
        112

        >>> spacing.measure_count
        18

        >>> len(spacing.measures)
        18

    """
    if isinstance(path, tuple):
        assert len(path) == 3, repr(path)
        first_measure_number, measure_count, fermata_measure_numbers = path
        phantom = None
    else:
        path = abjad.Path(path)
        tuple_ = path.get_measure_profile_metadata()
        first_measure_number = tuple_[0]
        measure_count = tuple_[1]
        fermata_measure_numbers = tuple_[2]
        phantom = tuple_[3]
        first_measure_number = first_measure_number or 1
    fallback_fraction = abjad.NonreducedFraction(fallback_duration)
    measures = abjad.OrderedDict()
    final_measure_number = first_measure_number + measure_count - 1
    for n in range(first_measure_number, final_measure_number + 1):
        measures[n] = fallback_fraction
    specifier = HorizontalSpacingSpecifier(
        breaks=breaks,
        fermata_measure_duration=fermata_measure_duration,
        fermata_measure_numbers=fermata_measure_numbers,
        first_measure_number=first_measure_number,
        measure_count=measure_count,
        measures=measures,
        phantom=phantom,
        )
    specifier._forbid_segment_maker_adjustments = True
    return specifier

def system(
    *distances: typing.Any,
    measure: int = None,
    y_offset: typings.Number = None
    ) -> SystemSpecifier:
    """
    Makes system specifier.
    """
    distances_ = classes.Sequence(distances).flatten()
    return SystemSpecifier(
        distances=distances_,
        measure=measure,
        y_offset=y_offset,
        )
