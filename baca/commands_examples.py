r"""
commands.py examles

..  container:: example

    Bow contact points. Tweaks LilyPond ``TextSpanner`` grob:

    >>> score = baca.docs.make_empty_score(1)
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )
    >>> baca.SpacingSpecifier((1, 16))(score)
    >>> music = baca.make_even_divisions(accumulator.get())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.bcps_function(
    ...     voice,
    ...     [(1, 5), (2, 5)],
    ...     abjad.Tweak(r"- \tweak color #red"),
    ...     abjad.Tweak(r"- \tweak staff-padding 2.5"),
    ... )
    >>> _ = baca.pitches_function(voice, "E4 F4")
    >>> _ = baca.script_staff_padding_function(voice, 5)

    >>> _, _ = baca.interpret.section(
    ...     score,
    ...     {},
    ...     accumulator.time_signatures,
    ...     commands=accumulator.commands,
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.lilypond.file(
    ...     score,
    ...     includes=["baca.ily"],
    ... )
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    Style LilyPond ``Script`` grob with overrides (instead of tweaks).

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            <<
                \context Voice = "Skips"
                {
                    \baca-new-spacing-section #1 #16
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #16
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #16
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #16
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override Script.staff-padding = 5
                    e'8
                    - \downbow
                    [
                    - \tweak color #red
                    - \tweak staff-padding 2.5
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #1 #5
                    \bacaStartTextSpanBCP
                    f'8
                    - \upbow
                    \bacaStopTextSpanBCP
                    - \tweak color #red
                    - \tweak staff-padding 2.5
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #2 #5
                    \bacaStartTextSpanBCP
                    e'8
                    - \downbow
                    \bacaStopTextSpanBCP
                    - \tweak color #red
                    - \tweak staff-padding 2.5
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #1 #5
                    \bacaStartTextSpanBCP
                    f'8
                    - \upbow
                    \bacaStopTextSpanBCP
                    ]
                    - \tweak color #red
                    - \tweak staff-padding 2.5
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #2 #5
                    \bacaStartTextSpanBCP
                    e'8
                    - \downbow
                    \bacaStopTextSpanBCP
                    [
                    - \tweak color #red
                    - \tweak staff-padding 2.5
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #1 #5
                    \bacaStartTextSpanBCP
                    f'8
                    - \upbow
                    \bacaStopTextSpanBCP
                    - \tweak color #red
                    - \tweak staff-padding 2.5
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #2 #5
                    \bacaStartTextSpanBCP
                    e'8
                    - \downbow
                    \bacaStopTextSpanBCP
                    ]
                    - \tweak color #red
                    - \tweak staff-padding 2.5
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #1 #5
                    \bacaStartTextSpanBCP
                    f'8
                    - \upbow
                    \bacaStopTextSpanBCP
                    [
                    - \tweak color #red
                    - \tweak staff-padding 2.5
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #2 #5
                    \bacaStartTextSpanBCP
                    e'8
                    - \downbow
                    \bacaStopTextSpanBCP
                    - \tweak color #red
                    - \tweak staff-padding 2.5
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #1 #5
                    \bacaStartTextSpanBCP
                    f'8
                    - \upbow
                    \bacaStopTextSpanBCP
                    - \tweak color #red
                    - \tweak staff-padding 2.5
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #2 #5
                    \bacaStartTextSpanBCP
                    e'8
                    - \downbow
                    \bacaStopTextSpanBCP
                    ]
                    - \tweak color #red
                    - \tweak staff-padding 2.5
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #1 #5
                    \bacaStartTextSpanBCP
                    f'8
                    - \upbow
                    \bacaStopTextSpanBCP
                    [
                    - \tweak color #red
                    - \tweak staff-padding 2.5
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #2 #5
                    \bacaStartTextSpanBCP
                    e'8
                    - \downbow
                    \bacaStopTextSpanBCP
                    - \tweak color #red
                    - \tweak staff-padding 2.5
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #1 #5
                    - \baca-bcp-spanner-right-text #2 #5
                    \bacaStartTextSpanBCP
                    f'8
                    \bacaStopTextSpanBCP
                    ]
                    \revert Script.staff-padding
                }
            >>
        }

..  container:: example

    PATTERN. Define chunkwise spanners like this:

    >>> score = baca.docs.make_empty_score(1)
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )
    >>> baca.SpacingSpecifier((1, 16))(score)
    >>> music = baca.make_even_divisions(accumulator.get())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.bcps_function(voice[:7], bcps=[(1, 5), (2, 5)])
    >>> _ = baca.bcps_function(voice[7:], bcps=[(3, 5), (4, 5)])
    >>> _ = baca.pitches_function(voice, "E4 F4")
    >>> _ = baca.script_staff_padding_function(voice, 5.5)
    >>> _ = baca.text_spanner_staff_padding_function(voice, 2.5)

    >>> _, _ = baca.interpret.section(
    ...     score,
    ...     {},
    ...     accumulator.time_signatures,
    ...     commands=accumulator.commands,
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.lilypond.file(
    ...     score,
    ...     includes=["baca.ily"],
    ... )
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            <<
                \context Voice = "Skips"
                {
                    \baca-new-spacing-section #1 #16
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #16
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #16
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #16
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override Script.staff-padding = 5.5
                    \override TextSpanner.staff-padding = 2.5
                    e'8
                    - \downbow
                    [
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #1 #5
                    \bacaStartTextSpanBCP
                    f'8
                    - \upbow
                    \bacaStopTextSpanBCP
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #2 #5
                    \bacaStartTextSpanBCP
                    e'8
                    - \downbow
                    \bacaStopTextSpanBCP
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #1 #5
                    \bacaStartTextSpanBCP
                    f'8
                    - \upbow
                    \bacaStopTextSpanBCP
                    ]
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #2 #5
                    \bacaStartTextSpanBCP
                    e'8
                    - \downbow
                    \bacaStopTextSpanBCP
                    [
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #1 #5
                    \bacaStartTextSpanBCP
                    f'8
                    - \upbow
                    \bacaStopTextSpanBCP
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #2 #5
                    - \baca-bcp-spanner-right-text #1 #5
                    \bacaStartTextSpanBCP
                    e'8
                    \bacaStopTextSpanBCP
                    ]
                    f'8
                    - \downbow
                    [
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #3 #5
                    \bacaStartTextSpanBCP
                    e'8
                    - \upbow
                    \bacaStopTextSpanBCP
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #4 #5
                    \bacaStartTextSpanBCP
                    f'8
                    - \downbow
                    \bacaStopTextSpanBCP
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #3 #5
                    \bacaStartTextSpanBCP
                    e'8
                    - \upbow
                    \bacaStopTextSpanBCP
                    ]
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #4 #5
                    \bacaStartTextSpanBCP
                    f'8
                    - \downbow
                    \bacaStopTextSpanBCP
                    [
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #3 #5
                    \bacaStartTextSpanBCP
                    e'8
                    - \upbow
                    \bacaStopTextSpanBCP
                    - \abjad-solid-line-with-arrow
                    - \baca-bcp-spanner-left-text #4 #5
                    - \baca-bcp-spanner-right-text #3 #5
                    \bacaStartTextSpanBCP
                    f'8
                    \bacaStopTextSpanBCP
                    ]
                    \revert Script.staff-padding
                    \revert TextSpanner.staff-padding
                }
            >>
        }

..  container:: example

    Effort dynamics:

    >>> container = baca.figure_function(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam_function(container)
    >>> _ = baca.dynamic_function(baca.select.pleaf(container, 0), '"f"')
    >>> _ = baca.tuplet_bracket_staff_padding_function(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(
    ...     selection, includes=["baca.ily"]
    ... )
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
                    \time 11/8
                    r8
                    c'16
                    \baca-effort-f
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
                \times 4/5
                {
                    a'16
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Works with hairpins:

    >>> score = baca.docs.make_empty_score(1)
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )
    >>> baca.SpacingSpecifier((1, 13))(score)
    >>> music = baca.make_even_divisions(accumulator.get())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches_function(voice, "E4 D5 F4 C5 G4 F5")
    >>> pleaf = baca.select.pleaf(voice, 0)
    >>> _ = baca.dynamic_function(pleaf, "p")
    >>> _ = baca.dynamic_function(pleaf, "<")
    >>> _ = baca.dynamic_function(baca.select.pleaf(voice, -1), "!")
    >>> _ = baca.dls_staff_padding_function(voice, 5)
    >>> _, _ = baca.interpret.section(
    ...     score,
    ...     {},
    ...     accumulator.time_signatures,
    ...     commands=accumulator.commands,
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.lilypond.file(
    ...     score,
    ...     includes=["baca.ily"],
    ... )
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
                    \baca-new-spacing-section #1 #13
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #13
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #13
                    \time 4/8
                    s1 * 4/8
                    \baca-new-spacing-section #1 #13
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override DynamicLineSpanner.staff-padding = 5
                    e'8
                    - \tweak color #(x11-color 'blue)
                    \p
                    [
                    \<
                    d''8
                    f'8
                    c''8
                    ]
                    g'8
                    [
                    f''8
                    e'8
                    ]
                    d''8
                    [
                    f'8
                    c''8
                    g'8
                    ]
                    f''8
                    [
                    e'8
                    d''8
                    \!
                    ]
                    \revert DynamicLineSpanner.staff-padding
                }
            >>
        }

..  container:: example

    Works with tweaks:

    >>> score = baca.docs.make_empty_score(1)
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )
    >>> baca.SpacingSpecifier((1, 12))(score)
    >>> music = baca.make_even_divisions(accumulator.get())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches_function(voice, "E4 D5 F4 C5 G4 F5")
    >>> _ = baca.dynamic_function(
    ...     baca.select.pleaf(voice, 0),
    ...     "p",
    ...     abjad.Tweak(r"- \tweak extra-offset #'(-4 . 0)"),
    ... )
    >>> _ = baca.dls_staff_padding_function(voice, 5)
    >>> _, _ = baca.interpret.section(
    ...     score,
    ...     {},
    ...     accumulator.time_signatures,
    ...     commands=accumulator.commands,
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.lilypond.file(
    ...     score,
    ...     includes=["baca.ily"],
    ... )
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
                    \override DynamicLineSpanner.staff-padding = 5
                    e'8
                    - \tweak extra-offset #'(-4 . 0)
                    \p
                    [
                    d''8
                    f'8
                    c''8
                    ]
                    g'8
                    [
                    f''8
                    e'8
                    ]
                    d''8
                    [
                    f'8
                    c''8
                    g'8
                    ]
                    f''8
                    [
                    e'8
                    d''8
                    ]
                    \revert DynamicLineSpanner.staff-padding
                }
            >>
        }

..  container:: example

    Force accidentals. Inverts edition-specific tags:

    >>> score = baca.docs.make_empty_score(1)
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )

    >>> music = baca.make_notes(accumulator.get(), repeat_ties=True)
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches_function(voice, "E4 F4")
    >>> baca.force_accidental_function(
    ...     baca.select.pleaves(voice)[:2], tag=baca.tags.NOT_PARTS
    ... )

    >>> _, _ = baca.interpret.section(
    ...     score,
    ...     {},
    ...     accumulator.time_signatures,
    ...     commands=accumulator.commands,
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.lilypond.file(
    ...     score,
    ...     includes=["baca.ily"],
    ... )
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
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    e'2
                    %@% e'!2
                    f'4.
                    %@% f'!4.
                    e'2
                    f'4.
                }
            >>
        }

..  container:: example

    Attaches short instrument name.

    >>> short_instrument_names = {}
    >>> markup = abjad.Markup(r"\markup Fl.")
    >>> short_instrument_names["Fl."] = abjad.ShortInstrumentName(markup)
    >>> manifests = {"abjad.ShortInstrumentName": short_instrument_names}
    >>> score = baca.docs.make_empty_score(1)
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )

    >>> music = baca.make_notes(accumulator.get(), repeat_ties=True)
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.short_instrument_name_function(voice[0], "Fl.", manifests)
    >>> _ = baca.pitches_function(voice, "E4 F4")

    >>> _, _ = baca.interpret.section(
    ...     score,
    ...     {},
    ...     accumulator.time_signatures,
    ...     commands=accumulator.commands,
    ...     first_section=True,
    ...     short_instrument_names=short_instrument_names,
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.lilypond.file(
    ...     score,
    ...     includes=["baca.ily"],
    ... )
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
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \set Staff.shortInstrumentName = \markup Fl.
                    e'2
                    f'4.
                    e'2
                    f'4.
                }
            >>
        }

..  container:: example

    Single-line staff with percussion clef:

    >>> score = baca.docs.make_empty_score(1)
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )
    >>> baca.SpacingSpecifier((1, 12))(score)

    >>> music = baca.make_notes(accumulator.get())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.clef_function(voice[0], "percussion")
    >>> _ = baca.staff_lines_function(voice[0], 1)
    >>> _ = baca.staff_positions_function(voice, [-2, -1, 0, 1, 2])

    >>> _, _ = baca.interpret.section(
    ...     score,
    ...     {},
    ...     accumulator.time_signatures,
    ...     commands=accumulator.commands,
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.lilypond.file(
    ...     score,
    ...     includes=["baca.ily"],
    ... )
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
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override Staff.BarLine.bar-extent = #'(0 . 0)
                    \stopStaff
                    \once \override Staff.StaffSymbol.line-count = 1
                    \startStaff
                    \clef "percussion"
                    a4.
                    b4.
                    c'4.
                    d'4.
                    e'4.
                }
            >>
        }


    Single-line staff with bass clef:

    >>> score = baca.docs.make_empty_score(1)
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )
    >>> baca.SpacingSpecifier((1, 12))(score)

    >>> music = baca.make_notes(accumulator.get())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.clef_function(voice[0], "bass")
    >>> _ = baca.staff_lines_function(voice[0], 1)
    >>> _ = baca.staff_positions_function(voice, [-2, -1, 0, 1, 2])

    >>> _, _ = baca.interpret.section(
    ...     score,
    ...     {},
    ...     accumulator.time_signatures,
    ...     commands=accumulator.commands,
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.lilypond.file(
    ...     score,
    ...     includes=["baca.ily"],
    ... )
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
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override Staff.BarLine.bar-extent = #'(0 . 0)
                    \stopStaff
                    \once \override Staff.StaffSymbol.line-count = 1
                    \startStaff
                    \clef "bass"
                    b,4.
                    c4.
                    d4.
                    e4.
                    f4.
                }
            >>
        }

..  container:: example

    Two-line staff with percussion clef:

    >>> score = baca.docs.make_empty_score(1)
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )
    >>> baca.SpacingSpecifier((1, 12))(score)

    >>> music = baca.make_notes(accumulator.get())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.clef_function(voice[0], "percussion")
    >>> _ = baca.staff_lines_function(voice[0], 2)
    >>> _ = baca.staff_positions_function(voice, [-2, -1, 0, 1, 2])

    >>> _, _ = baca.interpret.section(
    ...     score,
    ...     {},
    ...     accumulator.time_signatures,
    ...     commands=accumulator.commands,
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.lilypond.file(
    ...     score,
    ...     includes=["baca.ily"],
    ... )
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
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override Staff.BarLine.bar-extent = #'(-0.5 . 0.5)
                    \stopStaff
                    \once \override Staff.StaffSymbol.line-count = 2
                    \startStaff
                    \clef "percussion"
                    a4.
                    b4.
                    c'4.
                    d'4.
                    e'4.
                }
            >>
        }

    Two-line staff with bass clef; clef set before staff positions:

    >>> score = baca.docs.make_empty_score(1)
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )
    >>> baca.SpacingSpecifier((1, 12))(score)

    >>> music = baca.make_notes(accumulator.get())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.clef_function(voice[0], "bass")
    >>> _ = baca.staff_lines_function(voice[0], 2)
    >>> _ = baca.staff_positions_function(voice, [-2, -1, 0, 1, 2])

    >>> _, _ = baca.interpret.section(
    ...     score,
    ...     {},
    ...     accumulator.time_signatures,
    ...     commands=accumulator.commands,
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.lilypond.file(
    ...     score,
    ...     includes=["baca.ily"],
    ... )
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
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override Staff.BarLine.bar-extent = #'(-0.5 . 0.5)
                    \stopStaff
                    \once \override Staff.StaffSymbol.line-count = 2
                    \startStaff
                    \clef "bass"
                    b,4.
                    c4.
                    d4.
                    e4.
                    f4.
                }
            >>
        }

    Two-line staff with bass clef; staff positions set before clef:

    >>> score = baca.docs.make_empty_score(1)
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )
    >>> baca.SpacingSpecifier((1, 12))(score)

    >>> music = baca.make_notes(accumulator.get())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.staff_lines_function(voice[0], 2)
    >>> _ = baca.staff_positions_function(voice, [-2, -1, 0, 1, 2])
    >>> _ = baca.clef_function(voice[0], "bass")

    >>> _, _ = baca.interpret.section(
    ...     score,
    ...     {},
    ...     accumulator.time_signatures,
    ...     commands=accumulator.commands,
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.lilypond.file(
    ...     score,
    ...     includes=["baca.ily"],
    ... )
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
                    \time 3/8
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                    \baca-new-spacing-section #1 #12
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    \override Staff.BarLine.bar-extent = #'(-0.5 . 0.5)
                    \stopStaff
                    \once \override Staff.StaffSymbol.line-count = 2
                    \startStaff
                    \clef "bass"
                    g'4.
                    a'4.
                    b'4.
                    c''4.
                    d''4.
                }
            >>
        }

..  container:: example

    Colors leaves:

    >>> container = baca.figure_function(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam_function(container)
    >>> baca.color_function(abjad.select.leaves(container))
    >>> rmakers.unbeam_function(container)
    >>> _ = baca.tuplet_bracket_staff_padding_function(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
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
                    \abjad-color-music #'red
                    \time 11/8
                    r8
                    \abjad-color-music #'blue
                    c'16
                    \abjad-color-music #'red
                    d'16
                    \abjad-color-music #'blue
                    bf'4
                    ~
                    \abjad-color-music #'red
                    bf'16
                    \abjad-color-music #'blue
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \abjad-color-music #'red
                    fs''16
                    \abjad-color-music #'blue
                    e''16
                    \abjad-color-music #'red
                    ef''4
                    ~
                    \abjad-color-music #'blue
                    ef''16
                    \abjad-color-music #'red
                    r16
                    \abjad-color-music #'blue
                    af''16
                    \abjad-color-music #'red
                    g''16
                }
                \times 4/5
                {
                    \abjad-color-music #'blue
                    a'16
                    \abjad-color-music #'red
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Colors leaves in tuplet 1:

    >>> def color_selector(argument):
    ...     result = abjad.select.tuplet(argument, 1)
    ...     result = abjad.select.leaves(result)
    ...     return result
    >>> container = baca.figure_function(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam_function(container)
    >>> baca.color_function(color_selector(container))
    >>> rmakers.unbeam_function(container)
    >>> _ = baca.tuplet_bracket_staff_padding_function(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
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
                    \time 11/8
                    r8
                    c'16
                    d'16
                    bf'4
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    \abjad-color-music #'red
                    fs''16
                    \abjad-color-music #'blue
                    e''16
                    \abjad-color-music #'red
                    ef''4
                    ~
                    \abjad-color-music #'blue
                    ef''16
                    \abjad-color-music #'red
                    r16
                    \abjad-color-music #'blue
                    af''16
                    \abjad-color-music #'red
                    g''16
                }
                \times 4/5
                {
                    a'16
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Attaches cross-staff command to last two pitched leaves:

    >>> score = baca.docs.make_empty_score(1, 1)
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=[(4, 4)],
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )
    >>> music = abjad.Container("e'4 f' g' a'")[:]
    >>> score["Music.1"].extend(music)
    >>> music = abjad.Container("c'4 d' e' f'")[:]
    >>> score["Music.2"].extend(music)
    >>> _ = baca.cross_staff_function(baca.select.pleaves(score["Music.2"])[-2:])
    >>> _, _ = baca.interpret.section(
    ...     score,
    ...     {},
    ...     accumulator.time_signatures,
    ...     commands=accumulator.commands,
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.lilypond.file(
    ...     score,
    ...     includes=["baca.ily"],
    ... )
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context StaffGroup = "StaffGroup"
            <<
                \context Staff = "Staff.1"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/4
                        s1 * 4/4
                    }
                    \context Voice = "Music.1"
                    {
                        e'4
                        f'4
                        g'4
                        a'4
                    }
                >>
                \context Staff = "Staff.2"
                {
                    \context Voice = "Music.2"
                    {
                        c'4
                        d'4
                        \crossStaff
                        e'4
                        \crossStaff
                        f'4
                    }
                }
            >>
        }

..  container:: example

    Makes finger pressure transition glissando.

    >>> score = baca.docs.make_empty_score(1)
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )
    >>> baca.SpacingSpecifier((1, 12))(score)

    >>> music = baca.make_notes(accumulator.get())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitch_function(voice, "C5")
    >>> notes = abjad.select.notes(voice)
    >>> _ = baca.note_head_style_harmonic_function(notes[0])
    >>> _ = baca.note_head_style_harmonic_function(notes[2])
    >>> baca.finger_pressure_transition_function(notes[:2])
    >>> baca.finger_pressure_transition_function(notes[2:])

    >>> _, _ = baca.interpret.section(
    ...     score,
    ...     {},
    ...     accumulator.time_signatures,
    ...     commands=accumulator.commands,
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.lilypond.file(
    ...     score,
    ...     includes=["baca.ily"],
    ... )
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

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
                    \once \override NoteHead.style = #'harmonic
                    c''2
                    - \tweak arrow-length 2
                    - \tweak arrow-width 0.5
                    - \tweak bound-details.right.arrow ##t
                    - \tweak thickness 3
                    \glissando
                    c''4.
                    \once \override NoteHead.style = #'harmonic
                    c''2
                    - \tweak arrow-length 2
                    - \tweak arrow-width 0.5
                    - \tweak bound-details.right.arrow ##t
                    - \tweak thickness 3
                    \glissando
                    c''4.
                }
            >>
        }

..  container:: example

    Glissando works with tweaks:

    >>> score = baca.docs.make_empty_score(1)
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )

    >>> music = baca.make_even_divisions(accumulator.get())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches_function(voice, "E4 D5 F4 E5 G4 F5")
    >>> baca.glissando_function(
    ...     voice,
    ...     abjad.Tweak(r"- \tweak color #red"),
    ... )

    >>> _, _ = baca.interpret.section(
    ...     score,
    ...     {},
    ...     accumulator.time_signatures,
    ...     commands=accumulator.commands,
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.lilypond.file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            <<
                \context Voice = "Skips"
                {
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    e'8
                    [
                    - \tweak color #red
                    \glissando
                    d''8
                    - \tweak color #red
                    \glissando
                    f'8
                    - \tweak color #red
                    \glissando
                    e''8
                    ]
                    - \tweak color #red
                    \glissando
                    g'8
                    [
                    - \tweak color #red
                    \glissando
                    f''8
                    - \tweak color #red
                    \glissando
                    e'8
                    ]
                    - \tweak color #red
                    \glissando
                    d''8
                    [
                    - \tweak color #red
                    \glissando
                    f'8
                    - \tweak color #red
                    \glissando
                    e''8
                    - \tweak color #red
                    \glissando
                    g'8
                    ]
                    - \tweak color #red
                    \glissando
                    f''8
                    [
                    - \tweak color #red
                    \glissando
                    e'8
                    - \tweak color #red
                    \glissando
                    d''8
                    ]
                }
            >>
        }

..  container:: example

    Glissando works with indexed tweaks:

    >>> score = baca.docs.make_empty_score(1)
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )

    >>> music = baca.make_even_divisions(accumulator.get())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitches_function(voice, "E4 D5 F4 E5 G4 F5")
    >>> baca.glissando_function(
    ...     voice,
    ...     (abjad.Tweak(r"- \tweak color #red"), 0),
    ...     (abjad.Tweak(r"- \tweak color #red"), -1),
    ... )

    >>> _, _ = baca.interpret.section(
    ...     score,
    ...     {},
    ...     accumulator.time_signatures,
    ...     commands=accumulator.commands,
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.lilypond.file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

        >>> string = abjad.lilypond(score)
        >>> print(string)
        \context Score = "Score"
        {
            \context Staff = "Staff"
            <<
                \context Voice = "Skips"
                {
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                    \time 4/8
                    s1 * 4/8
                    \time 3/8
                    s1 * 3/8
                }
                \context Voice = "Music"
                {
                    e'8
                    [
                    - \tweak color #red
                    \glissando
                    d''8
                    \glissando
                    f'8
                    \glissando
                    e''8
                    ]
                    \glissando
                    g'8
                    [
                    \glissando
                    f''8
                    \glissando
                    e'8
                    ]
                    \glissando
                    d''8
                    [
                    \glissando
                    f'8
                    \glissando
                    e''8
                    \glissando
                    g'8
                    ]
                    \glissando
                    f''8
                    [
                    \glissando
                    e'8
                    - \tweak color #red
                    \glissando
                    d''8
                    ]
                }
            >>
        }

..  container:: example

    Attaches ``\baca-invisible-music`` literal to middle leaves:

    >>> score = baca.docs.make_empty_score(1)
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )
    >>> baca.SpacingSpecifier((1, 12))(score)

    >>> music = baca.make_notes(accumulator.get())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.pitch_function(voice, "C5")
    >>> _ = baca.invisible_music_function(baca.select.leaves(voice)[1:-1])

    >>> _, _ = baca.interpret.section(
    ...     score,
    ...     {},
    ...     accumulator.time_signatures,
    ...     commands=accumulator.commands,
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.lilypond.file(
    ...     score,
    ...     includes=["baca.ily"],
    ... )
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    ..  docs::

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
                    c''2
                    %@% \abjad-invisible-music
                    \abjad-invisible-music-coloring
                    c''4.
                    %@% \abjad-invisible-music
                    \abjad-invisible-music-coloring
                    c''2
                    c''4.
                }
            >>
        }

..  container:: example

    Labels pitch names:

    >>> container = baca.figure_function(
    ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
    ...     [1, 1, 5, -1],
    ...     16,
    ...     affix=baca.rests_around([2], [4]),
    ...     restart_talea=True,
    ...     treatments=[-1],
    ... )
    >>> rmakers.beam_function(container)
    >>> abjad.label.with_pitches(container, locale="us")
    >>> _ = baca.tuplet_bracket_staff_padding_function(container, 2)
    >>> selection = container[:]
    >>> container[:] = []
    >>> lilypond_file = abjad.illustrators.selection(selection)
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
                    \time 11/8
                    r8
                    c'16
                    ^ \markup { C4 }
                    [
                    d'16
                    ^ \markup { D4 }
                    ]
                    bf'4
                    ^ \markup { Bb4 }
                    ~
                    bf'16
                    r16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 9/10
                {
                    fs''16
                    ^ \markup { "F#5" }
                    [
                    e''16
                    ^ \markup { E5 }
                    ]
                    ef''4
                    ^ \markup { Eb5 }
                    ~
                    ef''16
                    r16
                    af''16
                    ^ \markup { Ab5 }
                    [
                    g''16
                    ^ \markup { G5 }
                    ]
                }
                \times 4/5
                {
                    a'16
                    ^ \markup { A4 }
                    r4
                    \revert TupletBracket.staff-padding
                }
            }
        >>

..  container:: example

    Assigns parts.

    >>> score = baca.docs.make_empty_score(1)
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )

    >>> music = baca.make_notes(accumulator.get())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.assign_part_function(voice, baca.parts.PartAssignment("Music"))
    >>> _ = baca.pitch_function(voice, "E4")

    >>> _, _ = baca.interpret.section(
    ...     score,
    ...     {},
    ...     accumulator.time_signatures,
    ...     commands=accumulator.commands,
    ...     move_global_context=True,
    ...     remove_tags=baca.tags.documentation_removal_tags(),
    ... )
    >>> lilypond_file = baca.lilypond.file(score)
    >>> abjad.show(lilypond_file) # doctest: +SKIP

    >>> string = abjad.lilypond(score)
    >>> print(string)
    \context Score = "Score"
    {
        \context Staff = "Staff"
        <<
            \context Voice = "Skips"
            {
                \time 4/8
                s1 * 4/8
                \time 3/8
                s1 * 3/8
                \time 4/8
                s1 * 4/8
                \time 3/8
                s1 * 3/8
            }
            \context Voice = "Music"
            {
                {   %*% PartAssignment('Music')
                    e'2
                    e'4.
                    e'2
                    e'4.
                }   %*% PartAssignment('Music')
            }
        >>
    }

..  container:: example exception

    Raises exception when voice does not allow part assignment:

    >>> score = baca.docs.make_empty_score(1)
    >>> accumulator = baca.CommandAccumulator(
    ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
    ... )
    >>> first_measure_number = baca.interpret.set_up_score(
    ...     score,
    ...     accumulator.time_signatures,
    ...     accumulator,
    ...     docs=True,
    ... )

    >>> part_assignment = baca.parts.PartAssignment("Flute")

    >>> music = baca.make_notes(accumulator.get())
    >>> score["Music"].extend(music)
    >>> voice = score["Music"]
    >>> _ = baca.assign_part_function(voice, baca.parts.PartAssignment("Flute.Music"))
    Traceback (most recent call last):
        ...
    Exception: Music does not allow Flute.Music part assignment:
        PartAssignment(name='Flute.Music', token=None)

"""


def dummy():
    """
    Makes Sphinx read this module.
    """
    pass
