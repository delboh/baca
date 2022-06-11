import abjad

from . import score as _score

_global_context_string = r"""\layout
{
    \context
    {
        \name GlobalSkips
        \type Engraver_group
        \consists Staff_symbol_engraver
        \override StaffSymbol.stencil = ##f
    }
    \context
    {
        \name GlobalContext
        \type Engraver_group
        \consists Axis_group_engraver
        \consists Mark_engraver
        \consists Metronome_mark_engraver
        \consists Time_signature_engraver
        \accepts GlobalSkips
        \override TimeSignature.X-extent = #'(0 . 0)
        \override TimeSignature.break-align-symbol = #'left-edge
        \override TimeSignature.break-visibility = #end-of-line-invisible
        \override TimeSignature.space-alist.clef = #'(extra-space . 0.5)
    }
    \context { \Staff \remove Time_signature_engraver }
    \context
    {
        \name MusicContext
        \type Engraver_group
        \consists System_start_delimiter_engraver
        \accepts StaffGroup
    }
    \context
    {
        \Score
        \accepts GlobalContext
        \accepts MusicContext
        \remove Bar_number_engraver
        \remove Mark_engraver
        \remove Metronome_mark_engraver
        \remove System_start_delimiter_engraver
    }
}
"""


def global_context_string():
    """
    Makes global context string.
    """
    return _global_context_string


def make_empty_score(*counts):
    r"""
    Makes empty score for doc examples.

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1)
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context GlobalContext = "GlobalContext"
            <<
                \context GlobalRests = "Rests"
                {
                }
                \context GlobalSkips = "Skips"
                {
                }
            >>
            \context MusicContext = "MusicContext"
            {
                \context Staff = "Staff"
                {
                    \context Voice = "Music"
                    {
                    }
                }
            }
        >>

    ..  container:: example

        >>> score = baca.docs.make_empty_score(4)
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context GlobalContext = "GlobalContext"
            <<
                \context GlobalRests = "Rests"
                {
                }
                \context GlobalSkips = "Skips"
                {
                }
            >>
            \context MusicContext = "MusicContext"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Music.1"
                    {
                    }
                    \context Voice = "Music.2"
                    {
                    }
                    \context Voice = "Music.3"
                    {
                    }
                    \context Voice = "Music.4"
                    {
                    }
                >>
            }
        >>

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1, 1, 1, 1)
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context GlobalContext = "GlobalContext"
            <<
                \context GlobalRests = "Rests"
                {
                }
                \context GlobalSkips = "Skips"
                {
                }
            >>
            \context MusicContext = "MusicContext"
            <<
                \context StaffGroup = "StaffGroup"
                <<
                    \context Staff = "Staff.1"
                    {
                        \context Voice = "Music.1"
                        {
                        }
                    }
                    \context Staff = "Staff.2"
                    {
                        \context Voice = "Music.2"
                        {
                        }
                    }
                    \context Staff = "Staff.3"
                    {
                        \context Voice = "Music.3"
                        {
                        }
                    }
                    \context Staff = "Staff.4"
                    {
                        \context Voice = "Music.4"
                        {
                        }
                    }
                >>
            >>
        >>

    ..  container:: example

        >>> score = baca.docs.make_empty_score(1, 2, 1)
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context GlobalContext = "GlobalContext"
            <<
                \context GlobalRests = "Rests"
                {
                }
                \context GlobalSkips = "Skips"
                {
                }
            >>
            \context MusicContext = "MusicContext"
            <<
                \context StaffGroup = "StaffGroup"
                <<
                    \context Staff = "Staff.1"
                    {
                        \context Voice = "Music.1"
                        {
                        }
                    }
                    \context Staff = "Staff.2"
                    <<
                        \context Voice = "Music.2"
                        {
                        }
                        \context Voice = "Music.3"
                        {
                        }
                    >>
                    \context Staff = "Staff.3"
                    {
                        \context Voice = "Music.4"
                        {
                        }
                    }
                >>
            >>
        >>

    """
    # TODO: use _tags.function_name()
    function_name = "baca.make_configuration_empty_score()"
    tag = abjad.Tag(function_name)
    global_context = _score.make_global_context()
    single_staff = len(counts) == 1
    single_voice = single_staff and counts[0] == 1
    staves, voice_number = [], 1
    for staff_index, voice_count in enumerate(counts):
        if single_staff:
            name = "Staff"
        else:
            staff_number = staff_index + 1
            name = f"Staff.{staff_number}"
        simultaneous = 1 < voice_count
        staff = abjad.Staff(name=name, simultaneous=simultaneous, tag=tag)
        voices = []
        for voice_index in range(voice_count):
            if single_voice:
                name = "Music"
            else:
                name = f"Music.{voice_number}"
            voice = abjad.Voice(name=name, tag=tag)
            voices.append(voice)
            voice_number += 1
        staff.extend(voices)
        staves.append(staff)

    if len(staves) == 1:
        music = staves
        simultaneous = False
    else:
        music = [abjad.StaffGroup(staves, name="StaffGroup")]
        simultaneous = True

    music_context = abjad.Context(
        music,
        lilypond_type="MusicContext",
        simultaneous=simultaneous,
        name="MusicContext",
        tag=tag,
    )

    score = abjad.Score([global_context, music_context], name="Score", tag=tag)
    return score
