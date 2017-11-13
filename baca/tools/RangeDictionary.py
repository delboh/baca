import abjad
import copy
from abjad.tools.datastructuretools.TypedOrderedDict import TypedOrderedDict


class RangeDictionary(TypedOrderedDict):
    r"""Range dictionary.

    ..  container:: example

        Two ranges:

        >>> ranges = baca.RangeDictionary([
        ...     ('tenor', '[C3, C6]'),
        ...     ('soprano', '[C4, C6]'),
        ...     ])

        >>> abjad.f(ranges)
        baca.RangeDictionary(
            [
                (
                    'tenor',
                    abjad.PitchRange('[C3, C6]'),
                    ),
                (
                    'soprano',
                    abjad.PitchRange('[C4, C6]'),
                    ),
                ]
            )

        >>> abjad.show(ranges) # doctest: +SKIP

        ..  docs::

            >>> lilypond_file = ranges.__illustrate__()
            >>> abjad.f(lilypond_file[abjad.Score])
            \new Score \with {
                \override BarLine.stencil = ##f
                \override Glissando.thickness = #2
                \override SpanBar.stencil = ##f
                \override TimeSignature.stencil = ##f
            } <<
                \new PianoStaff <<
                    \context Staff = "Treble Staff" {
                        \clef "treble"
                        s1 * 1/4
                        s1 * 1/4
                        c'1 * 1/4 \glissando
                        c'''1 * 1/4
                    }
                    \context Staff = "Bass Staff" {
                        \clef "bass"
                        c1 * 1/4 \glissando
                        \change Staff = "Treble Staff"
                        c'''1 * 1/4
                        s1 * 1/4
                        s1 * 1/4
                    }
                >>
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    __documentation_section__ = '(5) Utilities'

    ### SPECIAL METHODS ###

    def __illustrate__(self):
        r"""Illustrates pitch ranges.

        ..  container:: example

            >>> ranges = baca.RangeDictionary([
            ...     ('tenor', '[C3, C6]'),
            ...     ('soprano', '[C4, C6]'),
            ...     ])

            >>> abjad.show(ranges) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = ranges.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.stencil = ##f
                    \override Glissando.thickness = #2
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                } <<
                    \new PianoStaff <<
                        \context Staff = "Treble Staff" {
                            \clef "treble"
                            s1 * 1/4
                            s1 * 1/4
                            c'1 * 1/4 \glissando
                            c'''1 * 1/4
                        }
                        \context Staff = "Bass Staff" {
                            \clef "bass"
                            c1 * 1/4 \glissando
                            \change Staff = "Treble Staff"
                            c'''1 * 1/4
                            s1 * 1/4
                            s1 * 1/4
                        }
                    >>
                >>

        Returns LilyPond file.
        """
        start_note_clefs = []
        stop_note_clefs = []
        for pitch_range in self.values():
            start_note_clef = abjad.Clef.from_selection(
                pitch_range.start_pitch)
            start_note_clefs.append(start_note_clef)
            stop_note_clef = abjad.Clef.from_selection(
                pitch_range.stop_pitch)
            stop_note_clefs.append(stop_note_clef)
        if start_note_clefs == stop_note_clefs:
            clef = start_note_clefs[0]
            staff = abjad.Staff()
            abjad.attach(clef, staff)
            score = abjad.Score([staff])
            for pitch_range in self.items:
                start_note = abjad.Note(pitch_range.start_pitch, 1)
                stop_note = abjad.Note(pitch_range.stop_pitch, 1)
                notes = [start_note, stop_note]
                glissando = abjad.Glissando()
                staff.extend(notes)
                abjad.attach(glissando, notes)
        else:
            result = abjad.Score.make_piano_score()
            score, treble_staff, bass_staff = result
            for pitch_range in self.values():
                start_note = abjad.Note(pitch_range.start_pitch, 1)
                start_note_clef = abjad.Clef.from_selection(
                    pitch_range.start_pitch)
                stop_note = abjad.Note(pitch_range.stop_pitch, 1)
                stop_note_clef = abjad.Clef.from_selection(
                    pitch_range.stop_pitch)
                notes = abjad.select([start_note, stop_note])
                glissando = abjad.Glissando()
                skips = 2 * abjad.Skip(1)
                treble_clef = abjad.Clef('treble')
                bass_clef = abjad.Clef('bass')
                if start_note_clef == stop_note_clef == treble_clef:
                    treble_staff.extend(notes)
                    bass_staff.extend(skips)
                elif start_note_clef == stop_note_clef == bass_clef:
                    bass_staff.extend(notes)
                    treble_staff.extend(skips)
                else:
                    assert start_note_clef == bass_clef
                    assert stop_note_clef == treble_clef
                    bass_staff.extend(notes)
                    treble_staff.extend(skips)
                    staff_change = abjad.StaffChange(treble_staff)
                    abjad.attach(staff_change, stop_note)
                abjad.attach(glissando, notes)
            abjad.attach(abjad.Clef('treble'), treble_staff[0])
            abjad.attach(abjad.Clef('bass'), bass_staff[0])
        for leaf in abjad.iterate(score).leaves():
            multiplier = abjad.Multiplier(1, 4)
            abjad.attach(multiplier, leaf)
        abjad.override(score).bar_line.stencil = False
        abjad.override(score).span_bar.stencil = False
        abjad.override(score).glissando.thickness = 2
        abjad.override(score).time_signature.stencil = False
        lilypond_file = abjad.LilyPondFile.new(score)
        lilypond_file.items.remove(lilypond_file['layout'])
        lilypond_file.items.remove(lilypond_file['paper'])
        lilypond_file.header_block.tagline = False
        return lilypond_file

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        def coerce_(argument):
            if isinstance(argument, str):
                range_ = abjad.PitchRange(argument)
            elif isinstance(argument, tuple):
                range_ = abjad.PitchRange.from_pitches(*argument)
            elif isinstance(argument, abjad.PitchRange):
                range_ = copy.copy(argument)
            else:
                raise TypeError(argument)
            return range_
        return coerce_
