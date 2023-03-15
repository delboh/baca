r"""
spanners.py examples

..  container:: example

    Beams everything and sets beam direction down:

    >>> score = baca.docs.make_empty_score(1)
    >>> time_signatures = baca.section.time_signatures([(4, 8), (3, 8), (4, 8), (3, 8)])
    >>> baca.section.set_up_score(score, time_signatures(), docs=True)
    >>> baca.SpacingSpecifier(fallback_duration=(1, 12))(score)
    >>> music = baca.make_even_divisions(time_signatures())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitch(voice, "C4")
    >>> _ = baca.beam(voice, direction=abjad.DOWN)
    >>> baca.docs.remove_deactivated_wrappers(score)
    >>> lilypond_file = baca.lilypond.file(score, includes=["baca.ily"])
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            <<
                \context Voice = "Skips"
                {
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #12
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    c'8
                    _ [
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    ]
                }
            >>
        }

..  container:: example

    Attaches ottava indicators to trimmed leaves:

    >>> tuplets = baca.make_tuplets(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     treatments=["10:9"],
    ... )
    >>> baca.rests_around(tuplets, [2], [4], 16)
    >>> rmakers.beam(tuplets)
    >>> _ = baca.ottava(baca.select.tleaves(tuplets))
    >>> _ = baca.tuplet_bracket_staff_padding(tuplets, 2)
    >>> lilypond_file = abjad.illustrators.components(tuplets)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override TupletBracket.staff-padding = 2
                    \time 27/16
                    r8
                    \ottava 1
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
                \times 9/10
                {
                    fs''16
                    [
                    e''16
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
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    a'4
                    ~
                    a'16
                    \ottava 0
                    r16
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Attaches ottava bassa indicators to trimmed leaves:

    >>> tuplets = baca.make_tuplets(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     treatments=["10:9"],
    ... )
    >>> baca.rests_around(tuplets, [2], [4], 16)
    >>> rmakers.beam(tuplets)
    >>> _ = baca.ottava_bassa(baca.select.tleaves(tuplets))
    >>> _ = baca.tuplet_bracket_staff_padding(tuplets, 2)
    >>> lilypond_file = abjad.illustrators.components(tuplets)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override TupletBracket.staff-padding = 2
                    \time 27/16
                    r8
                    \ottava -1
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
                \times 9/10
                {
                    fs''16
                    [
                    e''16
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
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    a'4
                    ~
                    a'16
                    \ottava 0
                    r16
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Attaches slur to trimmed leaves:

    >>> tuplets = baca.make_tuplets(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     treatments=["10:9"],
    ... )
    >>> baca.rests_around(tuplets, [2], [4], 16)
    >>> rmakers.beam(tuplets)
    >>> _ = baca.slur(baca.select.tleaves(tuplets))
    >>> _ = baca.slur_down(tuplets)
    >>> _ = baca.tuplet_bracket_staff_padding(tuplets, 2)
    >>> lilypond_file = abjad.illustrators.components(tuplets)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override Slur.direction = #down
                    \override TupletBracket.staff-padding = 2
                    \time 27/16
                    r8
                    c'16
                    [
                    (
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    [
                    e''16
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
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    a'4
                    ~
                    a'16
                    )
                    r16
                    r4
                    \revert Slur.direction
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Pedals leaves:

    >>> tuplets = baca.make_tuplets(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     treatments=["10:9"],
    ... )
    >>> baca.rests_around(tuplets, [2], [4], 16)
    >>> rmakers.beam(tuplets)
    >>> _ = baca.sustain_pedal(tuplets)
    >>> _ = baca.sustain_pedal_staff_padding(tuplets, 4)
    >>> _ = baca.tuplet_bracket_staff_padding(tuplets, 2)
    >>> lilypond_file = abjad.illustrators.components(tuplets)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override Staff.SustainPedalLineSpanner.staff-padding = 4
                    \override TupletBracket.staff-padding = 2
                    \time 27/16
                    r8
                    \sustainOn
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
                \times 9/10
                {
                    fs''16
                    [
                    e''16
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
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    a'4
                    ~
                    a'16
                    r16
                    r4
                    \sustainOff
                    \revert Staff.SustainPedalLineSpanner.staff-padding
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Attaches trill spanner to trimmed leaves (leaked to the right):

    >>> tuplets = baca.make_tuplets(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     treatments=["10:9"],
    ... )
    >>> baca.rests_around(tuplets, [2], [4], 16)
    >>> rmakers.beam(tuplets)
    >>> _ = baca.trill_spanner(baca.select.tleaves(tuplets, rleak=True))
    >>> _ = baca.tuplet_bracket_staff_padding(tuplets, 2)
    >>> lilypond_file = abjad.illustrators.components(tuplets)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override TupletBracket.staff-padding = 2
                    \time 27/16
                    r8
                    c'16
                    [
                    \startTrillSpan
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    [
                    e''16
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
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    a'4
                    ~
                    a'16
                    r16
                    \stopTrillSpan
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Attaches trill to trimmed leaves (leaked to the right) in every
    run:

    >>> tuplets = baca.make_tuplets(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     treatments=["10:9"],
    ... )
    >>> baca.rests_around(tuplets, [2], [4], 16)
    >>> rmakers.beam(tuplets)
    >>> container = abjad.Container(tuplets)
    >>> for run in baca.select.runs(tuplets):
    ...     run = baca.select.rleak(run)
    ...     _ = baca.trill_spanner(run)

    >>> _ = baca.tuplet_bracket_staff_padding(tuplets, 2)
    >>> components = abjad.mutate.eject_contents(container)
    >>> lilypond_file = abjad.illustrators.components(components)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override TupletBracket.staff-padding = 2
                    \time 27/16
                    r8
                    c'16
                    [
                    \startTrillSpan
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                    \stopTrillSpan
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    [
                    \startTrillSpan
                    e''16
                    ]
                    ef''4
                    ~
                    ef''16
                    r16
                    \stopTrillSpan
                    af''16
                    [
                    \startTrillSpan
                    g''16
                    ]
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    a'4
                    ~
                    a'16
                    r16
                    \stopTrillSpan
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Tweaks trill spanner:

    >>> tuplets = baca.make_tuplets(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     treatments=["10:9"],
    ... )
    >>> baca.rests_around(tuplets, [2], [4], 16)
    >>> rmakers.beam(tuplets)
    >>> _ = baca.trill_spanner(
    ...     baca.select.tleaves(tuplets, rleak=True),
    ...     abjad.Tweak(r"- \tweak color #red"),
    ...     alteration="M2",
    ... )
    >>> _ = baca.tuplet_bracket_staff_padding(tuplets, 2)
    >>> lilypond_file = abjad.illustrators.components(tuplets)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> score = lilypond_file["Score"]
        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        <<
            \context Staff = "Staff"
            {
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \override TupletBracket.staff-padding = 2
                    \time 27/16
                    r8
                    \pitchedTrill
                    c'16
                    [
                    - \tweak color #red
                    \startTrillSpan d'
                    d'16
                    ]
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    [
                    e''16
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
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    a'4
                    ~
                    a'16
                    r16
                    \stopTrillSpan
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

"""


def dummy():
    """
    Read module-level examples.
    """
