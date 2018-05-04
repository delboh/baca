import abjad
import typing
from .Command import Command
from .IndicatorCommand import IndicatorCommand
from .MarkupLibrary import MarkupLibrary
from .Typing import Selector


class TextSpannerCommand(Command):
    r'''Text spanner command.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.text_spanner(
        ...         baca.markup.half_clt(),
        ...         selector=baca.leaves()[:4 + 1],
        ...         ),
        ...     baca.make_even_runs(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
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
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \override Score.BarLine.transparent = ##f                                    %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
                            {
            <BLANKLINE>
                                % [MusicVoice measure 1]                                             %! SM4
                                \override TextSpanner.staff-padding = #4.5                           %! OC1
                                e'8
                                [
                                -\tweak Y-extent ##f
                                -\tweak bound-details.left.text \markup {
                                    \concat
                                        {
                                            \whiteout
                                                \upright
                                                    "1/2 clt"
                                            \hspace
                                                #0.5
                                        }
                                    }
                                -\tweak dash-fraction 0.25
                                -\tweak dash-period 1.5
                                -\tweak bound-details.left-broken.text ##f
                                -\tweak bound-details.left.stencil-align-dir-y 0
                                -\tweak bound-details.right-broken.arrow ##f
                                -\tweak bound-details.right-broken.padding 0
                                -\tweak bound-details.right-broken.text ##f
                                -\tweak bound-details.right.padding 1.25
                                -\tweak bound-details.right.text \markup {
                                    \draw-line
                                        #'(0 . -1)
                                    }
                                \startTextSpan
            <BLANKLINE>
                                d''8
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                e''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 2]                                             %! SM4
                                g'8
                                \stopTextSpan
                                [
            <BLANKLINE>
                                f''8
            <BLANKLINE>
                                e'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 3]                                             %! SM4
                                d''8
                                [
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                e''8
            <BLANKLINE>
                                g'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 4]                                             %! SM4
                                f''8
                                [
            <BLANKLINE>
                                e'8
            <BLANKLINE>
                                d''8
                                ]
                                \revert TextSpanner.staff-padding                                    %! OC2
            <BLANKLINE>
                            }
                        }
                    }
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_line_segment',
        '_text',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        line_segment: abjad.LineSegment = None,
        selector: Selector = 'baca.leaves()',
        text: typing.Union[str, abjad.Markup, IndicatorCommand] = None,
        ) -> None:
        Command.__init__(self, selector=selector)
        if line_segment is not None:
            assert isinstance(line_segment, abjad.LineSegment)
        self._line_segment = line_segment
        if isinstance(text, str):
            markup_library = MarkupLibrary()
            command = markup_library(text)
            assert command.indicators is not None
            markup = command.indicators[0]
        elif isinstance(text, abjad.Markup):
            markup = text
        else:
            assert isinstance(text, IndicatorCommand), repr(text)
            assert text.indicators is not None
            assert len(text.indicators) == 1
            markup = text.indicators[0]
            assert isinstance(markup, abjad.Markup)
        self._text = markup
        self._tags = []

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        r'''Calls command on `argument`.
        '''
        if argument is None:
            return
        if self.text is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        leaves = abjad.select(argument).leaves()
        if not leaves:
            return
        spanner = abjad.TextSpanner()
        abjad.attach(spanner, leaves)
        first_leaf = leaves[0]
        spanner.attach(
            self.text,
            first_leaf,
            tag=self.tag.prepend('TSC1'),
            )
        if self.line_segment is None:
            return
        spanner.attach(
            self.line_segment,
            first_leaf,
            tag=self.tag.prepend('TSC2'),
            )

    ### PUBLIC PROPERTIES ###

    @property
    def line_segment(self) -> typing.Optional[abjad.LineSegment]:
        r'''Gets line segment.
        '''
        return self._line_segment

    @property
    def text(self) -> abjad.Markup:
        r'''Gets text.
        '''
        return self._text
