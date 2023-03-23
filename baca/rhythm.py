"""
Rhythm.
"""
import dataclasses
import fractions
import math as python_math
import typing
from inspect import currentframe as _frame

import abjad
from abjadext import rmakers

from . import select as _select
from . import tags as _tags
from .enums import enums as _enums

_collection_classes = (
    abjad.PitchClassSegment,
    abjad.PitchSegment,
    abjad.PitchSet,
    list,
    tuple,
)

_collection_typing = typing.Union[
    abjad.PitchClassSegment,
    abjad.PitchSegment,
    abjad.PitchSet,
    list,
    tuple,
]


def _make_accelerando_multipliers(
    durations: list[abjad.Duration], exponent: float
) -> list[tuple[int, int]]:
    sums = abjad.math.cumulative_sums(durations)
    generator = abjad.sequence.nwise(sums, n=2)
    pairs = list(generator)
    total_duration = pairs[-1][-1]
    start_offsets = [_[0] for _ in pairs]
    start_offsets = [_ / total_duration for _ in start_offsets]
    start_offsets_ = []
    for start_offset in start_offsets:
        start_offset_ = rmakers.rmakers._interpolate_exponential(
            0, total_duration, start_offset, exponent
        )
        start_offsets_.append(start_offset_)
    start_offsets_.append(float(total_duration))
    durations_ = abjad.math.difference_series(start_offsets_)
    durations_ = rmakers.rmakers._round_durations(durations_, 2**10)
    current_duration = sum(durations_)
    if current_duration < total_duration:
        missing_duration = total_duration - current_duration
        if durations_[0] < durations_[-1]:
            durations_[-1] += missing_duration
        else:
            durations_[0] += missing_duration
    elif total_duration < current_duration:
        extra_duration = current_duration - total_duration
        if durations_[0] < durations_[-1]:
            durations_[-1] -= extra_duration
        else:
            durations_[0] -= extra_duration
    assert sum(durations_) == total_duration
    pairs = []
    assert len(durations) == len(durations_)
    for duration_, duration in zip(durations_, durations):
        fraction = duration_ / duration
        pair = abjad.duration.with_denominator(fraction, 2**10)
        pairs.append(pair)
    return pairs


def _style_accelerando(
    container: abjad.Container | abjad.Tuplet,
    exponent: float,
    total_duration: abjad.Duration | None = None,
) -> abjad.Container | abjad.Tuplet:
    assert isinstance(container, abjad.Container), repr(container)
    if 1 < len(container):
        assert isinstance(container, abjad.Tuplet), repr(container)
        assert isinstance(exponent, float), repr(exponent)
        if total_duration is not None:
            assert isinstance(total_duration, abjad.Duration), repr(total_duration)
        leaves = abjad.select.leaves(container)
        leaf_durations = [abjad.get.duration(_) for _ in leaves]
        pairs = _make_accelerando_multipliers(leaf_durations, exponent)
        if total_duration is not None:
            multiplier = total_duration / sum(leaf_durations)
            scaled_pairs = []
            for pair in pairs:
                numerator, denominator = pair
                numerator *= multiplier.numerator
                denominator *= multiplier.denominator
                scaled_pair = (numerator, denominator)
                scaled_pairs.append(scaled_pair)
            pairs = scaled_pairs
        assert len(leaves) == len(pairs)
        for pair, leaf in zip(pairs, leaves):
            leaf.multiplier = pair
        rmakers.feather_beam([container])
        rmakers.duration_bracket(container)
    return container


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class AccelerandoSpecifier:
    denominator: int
    items: list
    numerator: int
    coefficient: fractions.Fraction | None = None
    ritardando: bool = False

    def __post_init__(self):
        assert isinstance(self.denominator, int), repr(self.denominator)
        assert isinstance(self.items, list), repr(self.items)
        assert isinstance(self.numerator, int), repr(self.numerator)
        assert isinstance(self.ritardando, bool), repr(self.ritardando)

    def __call__(self):
        pass


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Grace:
    denominator: int
    grace_note_numerators: list[int]
    main_note_numerator: int

    def __post_init__(self):
        assert isinstance(self.denominator, int), repr(self.denominator)
        assert isinstance(self.main_note_numerator, int), repr(self.main_note_numerator)
        assert all(isinstance(_, int) for _ in self.grace_note_numerators), repr(
            self.grace_note_numerators
        )

    def __call__(self):
        main_duration = abjad.Duration(abs(self.main_note_numerator), self.denominator)
        if 0 < self.main_note_numerator:
            pitch = 0
        else:
            pitch = None
        main_components = abjad.makers.make_leaves([pitch], main_duration)
        first_leaf = abjad.get.leaf(main_components, 0)
        grace_durations = [
            abjad.Duration(abs(_), self.denominator) for _ in self.grace_note_numerators
        ]
        pitches = []
        for grace_note_numerator in self.grace_note_numerators:
            if 0 < grace_note_numerator:
                pitches.append(0)
            else:
                pitches.append(None)
        grace_leaves = abjad.makers.make_leaves(pitches, grace_durations)
        grace_container = abjad.BeforeGraceContainer(grace_leaves)
        abjad.attach(grace_container, first_leaf)
        return main_components


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class LMR:
    left_counts: typing.Sequence[int] = ()
    left_cyclic: bool = False
    left_length: int = 0
    left_reversed: bool = False
    middle_counts: typing.Sequence[int] = ()
    middle_cyclic: bool = False
    middle_reversed: bool = False
    priority: int | None = None
    right_counts: typing.Sequence[int] = ()
    right_cyclic: bool = False
    right_length: int = 0
    right_reversed: bool = False

    def __post_init__(self):
        if self.left_counts is not None:
            assert abjad.math.all_are_positive_integers(self.left_counts)
        assert isinstance(self.left_cyclic, bool), repr(self.left_cyclic)
        if self.left_length is not None:
            assert isinstance(self.left_length, int), repr(self.left_length)
            assert 0 <= self.left_length, repr(self.left_length)
        assert isinstance(self.left_reversed, bool), repr(self.left_reversed)
        if self.middle_counts is not None:
            assert abjad.math.all_are_positive_integers(self.middle_counts)
        assert isinstance(self.middle_cyclic, bool), repr(self.middle_cyclic)
        assert isinstance(self.middle_reversed, bool), repr(self.middle_reversed)
        if self.priority is not None:
            assert self.priority in (abjad.LEFT, abjad.RIGHT)
        if self.right_counts is not None:
            assert abjad.math.all_are_positive_integers(self.right_counts)
        assert isinstance(self.right_cyclic, bool), repr(self.right_cyclic)
        if self.right_length is not None:
            assert isinstance(self.right_length, int), repr(self.right_length)
            assert 0 <= self.right_length, repr(self.right_length)
        assert isinstance(self.right_reversed, bool), repr(self.right_reversed)

    def __call__(self, sequence=None):
        assert isinstance(sequence, list), repr(sequence)
        top_lengths = self._get_top_lengths(len(sequence))
        top_parts = abjad.sequence.partition_by_counts(
            list(sequence), top_lengths, cyclic=False, overhang=abjad.EXACT
        )
        parts = []
        left_part, middle_part, right_part = top_parts
        if left_part:
            if self.left_counts:
                parts_ = abjad.sequence.partition_by_counts(
                    left_part,
                    self.left_counts,
                    cyclic=self.left_cyclic,
                    overhang=True,
                    reversed_=self.left_reversed,
                )
                parts.extend(parts_)
            else:
                parts.append(left_part)
        if middle_part:
            if self.middle_counts:
                parts_ = abjad.sequence.partition_by_counts(
                    middle_part,
                    self.middle_counts,
                    cyclic=self.middle_cyclic,
                    overhang=True,
                    reversed_=self.middle_reversed,
                )
                parts.extend(parts_)
            else:
                parts.append(middle_part)
        if right_part:
            if self.right_counts:
                parts_ = abjad.sequence.partition_by_counts(
                    right_part,
                    self.right_counts,
                    cyclic=self.right_cyclic,
                    overhang=True,
                    reversed_=self.right_reversed,
                )
                parts.extend(parts_)
            else:
                parts.append(right_part)
        assert isinstance(parts, list), repr(parts)
        assert all(isinstance(_, list) for _ in parts)
        return parts

    def _get_priority(self):
        if self.priority is None:
            return abjad.LEFT
        return self.priority

    def _get_top_lengths(self, total_length):
        left_length, middle_length, right_length = 0, 0, 0
        left_length = self.left_length or 0
        middle_length = 0
        right_length = self.right_length or 0
        if left_length and right_length:
            if self._get_priority() == abjad.LEFT:
                left_length = self.left_length or 0
                left_length = min([left_length, total_length])
                remaining_length = total_length - left_length
                if self.right_length is None:
                    right_length = remaining_length
                    middle_length = 0
                else:
                    right_length = self.right_length or 0
                    right_length = min([right_length, remaining_length])
                    remaining_length = total_length - (left_length + right_length)
                    middle_length = remaining_length
            else:
                right_length = self.right_length or 0
                right_length = min([right_length, total_length])
                remaining_length = total_length - right_length
                if self.left_length is None:
                    left_length = remaining_length
                    middle_length = 0
                else:
                    left_length = self.left_length or 0
                    left_length = min([left_length, remaining_length])
                    remaining_length = total_length - (right_length + left_length)
                    middle_length = remaining_length
        elif left_length and not right_length:
            left_length = min([left_length, total_length])
            remaining_length = total_length - left_length
            right_length = remaining_length
        elif not left_length and right_length:
            right_length = min([right_length, total_length])
            remaining_length = total_length - right_length
            left_length = remaining_length
        elif not left_length and not right_length:
            middle_length = total_length
        return left_length, middle_length, right_length


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class OBGC:
    denominator: int
    grace_note_numerators: list[int]
    main_note_numerator: int

    def __post_init__(self):
        assert isinstance(self.denominator, int), repr(self.denominator)
        assert all(isinstance(_, int) for _ in self.grace_note_numerators), repr(
            self.grace_note_numerators
        )
        assert isinstance(self.main_note_numerator, int), repr(self.main_note_numerator)

    def __call__(self):
        pass


def attach_before_grace_containers(before_grace_containers, tuplet):
    tag = _tags.function_name(_frame())
    if before_grace_containers is None:
        return
    logical_ties = abjad.iterate.logical_ties(tuplet)
    pairs = zip(before_grace_containers, logical_ties)
    for before_grace_container, logical_tie in pairs:
        if before_grace_container is None:
            continue
        abjad.attach(before_grace_container, logical_tie.head, tag=tag)


def from_collection(
    collection: _collection_typing,
    counts: list[int],
    denominator: int,
    prolation: int | str | abjad.Duration | None = None,
) -> abjad.Tuplet:
    collection = getattr(collection, "argument", collection)
    prototype = (
        abjad.PitchClassSegment,
        abjad.PitchSegment,
        abjad.PitchSet,
        list,
        tuple,
    )
    assert isinstance(collection, prototype), repr(collection)
    if isinstance(collection, tuple | abjad.PitchSet):
        collection = [tuple(collection)]
    talea = rmakers.Talea(counts, denominator)
    leaves, i = [], 0
    for item in collection:
        item = getattr(item, "number", item)
        assert isinstance(item, int | float | str | tuple), repr(item)
        while abjad.Fraction(*talea[i]) < 0:
            pair = talea[i]
            duration = -abjad.Duration(*pair)
            tag = _tags.function_name(_frame(), n=1)
            rests = abjad.makers.make_leaves([None], [duration], tag=tag)
            leaves.extend(rests)
            i += 1
        pair = talea[i]
        duration = abjad.Duration(*pair)
        assert 0 < duration, repr(duration)
        tag = _tags.function_name(_frame(), n=3)
        pleaves = abjad.makers.make_leaves([item], [duration], tag=tag)
        leaves.extend(pleaves)
        i += 1
        while abjad.Fraction(*talea[i]) < 0 and not i % len(talea) == 0:
            pair = talea[i]
            duration = -abjad.Duration(*pair)
            tag = _tags.function_name(_frame(), n=4)
            rests = abjad.makers.make_leaves([None], [duration], tag=tag)
            leaves.extend(rests)
            i += 1
    assert all(isinstance(_, abjad.Leaf) for _ in leaves), repr(leaves)
    tuplet = abjad.Tuplet("1:1", leaves)
    if prolation is not None:
        prolate(tuplet, prolation, denominator=denominator)
    return tuplet


def get_previous_rhythm_state(
    previous_parameter_to_state: dict, name: str
) -> dict | None:
    previous_rhythm_state = None
    if previous_parameter_to_state:
        previous_rhythm_state = previous_parameter_to_state.get(_enums.RHYTHM.name)
        if (
            previous_rhythm_state is not None
            and previous_rhythm_state.get("name") != name
        ):
            previous_rhythm_state = None
    if previous_rhythm_state is not None:
        assert len(previous_rhythm_state) in (4, 5), repr(previous_rhythm_state)
        assert previous_rhythm_state["name"] == name, repr(previous_rhythm_state)
    return previous_rhythm_state


def make_accelerando(
    vector: list, denominator: int, duration: abjad.Duration, *, exponent: float = 0.625
) -> abjad.Tuplet:
    r"""
    Makes accelerando.

    ..  container:: example

        >>> duration = abjad.Duration(1, 4)
        >>> tuplet = baca.make_accelerando([1, 1, 1], 16, duration)
        >>> string = abjad.lilypond(tuplet)
        >>> print(string)
        \override TupletNumber.text = \markup \scale #'(0.75 . 0.75) \rhythm { 4 }
        \times 1/1
        {
            \once \override Beam.grow-direction = #right
            c'16 * 6208/3072
            [
            c'16 * 3328/3072
            c'16 * 2752/3072
            ]
        }
        \revert TupletNumber.text

    """
    tag = _tags.function_name(_frame())
    leaves = []
    assert isinstance(denominator, int), repr(denominator)
    assert isinstance(duration, abjad.Duration), repr(duration)
    assert isinstance(exponent, float), repr(exponent)
    for item in vector:
        if isinstance(item, int) and 0 < item:
            leaf_duration = abjad.Duration(item, denominator)
            notes = abjad.makers.make_leaves([0], [leaf_duration], tag=tag)
            leaves.extend(notes)
        elif isinstance(item, int) and item < 0:
            leaf_duration = abjad.Duration(-item, denominator)
            rests = abjad.makers.make_leaves([None], [leaf_duration], tag=tag)
            leaves.extend(rests)
        else:
            raise Exception(item)
    tuplet = abjad.Tuplet("1:1", leaves, tag=tag)
    _style_accelerando(tuplet, exponent, total_duration=duration)
    return tuplet


def make_before_grace_containers(
    collection, lmr: LMR, *, duration: abjad.Duration = abjad.Duration(1, 16)
):
    assert isinstance(collection, list), repr(collection)
    assert isinstance(duration, abjad.Duration), repr(duration)
    assert isinstance(lmr, LMR), repr(LMR)
    segment_parts = lmr(collection)
    segment_parts = [_ for _ in segment_parts if _]
    collection = [_[-1] for _ in segment_parts]
    before_grace_containers: list[abjad.BeforeGraceContainer | None] = []
    for segment_part in segment_parts:
        if len(segment_part) <= 1:
            before_grace_containers.append(None)
            continue
        grace_token = list(segment_part[:-1])
        grace_leaves = abjad.makers.make_leaves(
            grace_token, [duration], tag=_tags.function_name(_frame(), n=1)
        )
        container = abjad.BeforeGraceContainer(
            grace_leaves,
            command=r"\acciaccatura",
            tag=_tags.function_name(_frame(), n=2),
        )
        if 1 < len(container):
            abjad.beam(
                container[:],
                tag=_tags.function_name(_frame(), n=3),
            )
        before_grace_containers.append(container)
    assert len(before_grace_containers) == len(collection)
    assert isinstance(collection, list), repr(collection)
    return before_grace_containers, collection


def make_even_divisions(time_signatures) -> list[abjad.Leaf | abjad.Tuplet]:
    tag = _tags.function_name(_frame())
    durations = [_.duration for _ in time_signatures]
    tuplets = rmakers.even_division(durations, [8], tag=tag)
    voice = rmakers.wrap_in_time_signature_staff(tuplets, time_signatures)
    rmakers.beam(voice, tag=tag)
    rmakers.extract_trivial(voice)
    components = abjad.mutate.eject_contents(voice)
    music: list[abjad.Leaf | abjad.Tuplet] = []
    for component in components:
        assert isinstance(component, abjad.Leaf | abjad.Tuplet)
        music.append(component)
    return music


def make_mmrests(
    time_signatures, *, head: str = ""
) -> list[abjad.MultimeasureRest | abjad.Container]:
    assert isinstance(head, str), repr(head)
    mmrests: list[abjad.MultimeasureRest | abjad.Container] = []
    if not head:
        tag = _tags.function_name(_frame(), n=1)
        for time_signature in time_signatures:
            mmrest = abjad.MultimeasureRest(1, multiplier=time_signature.pair, tag=tag)
            mmrests.append(mmrest)
    else:
        assert isinstance(head, str)
        voice_name = head
        for i, time_signature in enumerate(time_signatures):
            if i == 0:
                tag = _tags.function_name(_frame(), n=2)
                tag = tag.append(_tags.HIDDEN)
                note_or_rest = _tags.NOTE
                tag = tag.append(_tags.NOTE)
                note = abjad.Note("c'1", multiplier=time_signature.pair, tag=tag)
                abjad.override(note).Accidental.stencil = False
                abjad.override(note).NoteColumn.ignore_collision = True
                abjad.attach(_enums.NOTE, note)
                abjad.attach(_enums.NOT_YET_PITCHED, note)
                abjad.attach(_enums.HIDDEN, note)
                tag = _tags.function_name(_frame(), n=3)
                tag = tag.append(note_or_rest)
                tag = tag.append(_tags.INVISIBLE_MUSIC_COLORING)
                literal = abjad.LilyPondLiteral(
                    r"\abjad-invisible-music-coloring", site="before"
                )
                abjad.attach(literal, note, tag=tag)
                tag = _tags.function_name(_frame(), n=4)
                tag = tag.append(note_or_rest)
                tag = tag.append(_tags.INVISIBLE_MUSIC_COMMAND)
                literal = abjad.LilyPondLiteral(
                    r"\abjad-invisible-music", site="before"
                )
                abjad.attach(literal, note, deactivate=True, tag=tag)
                tag = _tags.function_name(_frame(), n=5)
                hidden_note_voice = abjad.Voice([note], name=voice_name, tag=tag)
                abjad.attach(_enums.INTERMITTENT, hidden_note_voice)
                tag = _tags.function_name(_frame(), n=6)
                tag = tag.append(_tags.REST_VOICE)
                tag = tag.append(_tags.MULTIMEASURE_REST)
                rest = abjad.MultimeasureRest(
                    1, multiplier=time_signature.pair, tag=tag
                )
                abjad.attach(_enums.MULTIMEASURE_REST, rest)
                abjad.attach(_enums.REST_VOICE, rest)
                if "Music" in voice_name:
                    name = voice_name.replace("Music", "Rests")
                else:
                    assert "Voice" in voice_name
                    name = f"{voice_name}.Rests"
                tag = _tags.function_name(_frame(), n=7)
                multimeasure_rest_voice = abjad.Voice([rest], name=name, tag=tag)
                abjad.attach(_enums.INTERMITTENT, multimeasure_rest_voice)
                tag = _tags.function_name(_frame(), n=8)
                container = abjad.Container(
                    [hidden_note_voice, multimeasure_rest_voice],
                    simultaneous=True,
                    tag=tag,
                )
                abjad.attach(_enums.MULTIMEASURE_REST_CONTAINER, container)
                mmrests.append(container)
            else:
                mmrest = abjad.MultimeasureRest(
                    1, multiplier=time_signature.pair, tag=tag
                )
                mmrests.append(mmrest)
    assert all(isinstance(_, abjad.MultimeasureRest | abjad.Container) for _ in mmrests)
    return mmrests


def make_monads(fractions) -> list[abjad.Leaf | abjad.Tuplet]:
    music: list[abjad.Leaf | abjad.Tuplet] = []
    pitch = 0
    for fraction in fractions.split():
        leaves = abjad.makers.make_leaves([pitch], [fraction])
        music.extend(leaves)
    assert all(isinstance(_, abjad.Leaf | abjad.Tuplet) for _ in music)
    return music


def make_notes(
    time_signatures,
    *,
    repeat_ties: bool = False,
) -> list[abjad.Leaf | abjad.Tuplet]:
    assert all(isinstance(_, abjad.TimeSignature) for _ in time_signatures)
    tag = _tags.function_name(_frame())
    durations = [_.duration for _ in time_signatures]
    components = rmakers.note(durations, tag=tag)
    voice = rmakers.wrap_in_time_signature_staff(components, time_signatures)
    rmakers.rewrite_meter(voice)
    if repeat_ties is True:
        rmakers.force_repeat_tie(voice)
    contents, music = abjad.mutate.eject_contents(voice), []
    for component in contents:
        assert isinstance(component, abjad.Leaf | abjad.Tuplet)
        music.append(component)
    return music


def make_repeat_tied_notes(
    time_signatures,
    *,
    do_not_rewrite_meter: bool = False,
) -> list[abjad.Leaf | abjad.Tuplet]:
    tag = _tags.function_name(_frame())
    durations = [_.duration for _ in time_signatures]
    leaves_and_tuplets = rmakers.note(durations, tag=tag)
    voice = rmakers.wrap_in_time_signature_staff(leaves_and_tuplets, time_signatures)
    rmakers.beam(_select.plts(voice))
    rmakers.repeat_tie(_select.pheads(voice)[1:], tag=tag)
    if not do_not_rewrite_meter:
        rmakers.rewrite_meter(voice)
    rmakers.force_repeat_tie(voice)
    components = abjad.mutate.eject_contents(voice)
    music: list[abjad.Leaf | abjad.Tuplet] = []
    for component in components:
        assert isinstance(component, abjad.Leaf | abjad.Tuplet)
        music.append(component)
    return music


def make_repeated_duration_notes(
    time_signatures,
    weights,
    *,
    do_not_rewrite_meter=None,
) -> list[abjad.Leaf | abjad.Tuplet]:
    assert all(isinstance(_, abjad.TimeSignature) for _ in time_signatures)
    tag = _tags.function_name(_frame())
    if isinstance(weights, abjad.Duration):
        weights = [weights]
    elif isinstance(weights, tuple):
        assert len(weights) == 2
        weights = [abjad.Duration(weights)]
    durations = [_.duration for _ in time_signatures]
    durations = [sum(durations)]
    weights = abjad.durations(weights)
    durations = abjad.sequence.split(durations, weights, cyclic=True, overhang=True)
    durations = abjad.sequence.flatten(durations, depth=-1)
    components = rmakers.note(durations, tag=tag)
    voice = rmakers.wrap_in_time_signature_staff(components, time_signatures)
    if not do_not_rewrite_meter:
        rmakers.rewrite_meter(voice, tag=tag)
    rmakers.force_repeat_tie(voice)
    contents = abjad.mutate.eject_contents(voice)
    music: list[abjad.Leaf | abjad.Tuplet] = []
    for component in contents:
        assert isinstance(component, abjad.Leaf | abjad.Tuplet)
        music.append(component)
    return music


def make_rests(time_signatures) -> list[abjad.Rest | abjad.Tuplet]:
    assert all(isinstance(_, abjad.TimeSignature) for _ in time_signatures)
    tag = _tags.function_name(_frame())
    durations = [_.duration for _ in time_signatures]
    components = rmakers.note(durations, tag=tag)
    voice = rmakers.wrap_in_time_signature_staff(components, time_signatures)
    lts = _select.lts(voice)
    rmakers.force_rest(lts, tag=tag)
    contents = abjad.mutate.eject_contents(voice)
    music: list[abjad.Rest | abjad.Tuplet] = []
    for component in contents:
        assert isinstance(component, abjad.Rest | abjad.Tuplet)
        music.append(component)
    return music


def make_single_attack(time_signatures, duration) -> list[abjad.Leaf | abjad.Tuplet]:
    assert all(isinstance(_, abjad.TimeSignature) for _ in time_signatures)
    durations = [_.duration for _ in time_signatures]
    tag = _tags.function_name(_frame())
    duration = abjad.Duration(duration)
    numerator, denominator = duration.pair
    tuplets = rmakers.incised(
        durations,
        fill_with_rests=True,
        outer_tuplets_only=True,
        prefix_talea=[numerator],
        prefix_counts=[1],
        tag=tag,
        talea_denominator=denominator,
    )
    voice = rmakers.wrap_in_time_signature_staff(tuplets, time_signatures)
    rmakers.beam(voice)
    rmakers.extract_trivial(voice)
    components = abjad.mutate.eject_contents(voice)
    music: list[abjad.Leaf | abjad.Tuplet] = []
    for component in components:
        assert isinstance(component, abjad.Leaf | abjad.Tuplet)
        music.append(component)
    return music


def make_tied_notes(time_signatures) -> list[abjad.Note | abjad.Tuplet]:
    assert all(isinstance(_, abjad.TimeSignature) for _ in time_signatures)
    durations = [_.duration for _ in time_signatures]
    tag = _tags.function_name(_frame())
    components = rmakers.note(durations, tag=tag)
    voice = rmakers.wrap_in_time_signature_staff(components, time_signatures)
    plts = _select.plts(voice)
    rmakers.beam(plts, tag=tag)
    ptails = _select.ptails(voice)[:-1]
    rmakers.tie(ptails, tag=tag)
    rmakers.rewrite_meter(voice, tag=tag)
    contents = abjad.mutate.eject_contents(voice)
    music: list[abjad.Note | abjad.Tuplet] = []
    for component in contents:
        assert isinstance(component, abjad.Note | abjad.Tuplet)
        music.append(component)
    return music


def make_tied_repeated_durations(
    time_signatures, weights
) -> list[abjad.Leaf | abjad.Tuplet]:
    assert all(isinstance(_, abjad.TimeSignature) for _ in time_signatures)
    tag = _tags.function_name(_frame())
    durations = [_.duration for _ in time_signatures]
    durations = [sum(durations)]
    weights = abjad.durations(weights)
    durations = abjad.sequence.split(durations, weights, cyclic=True, overhang=True)
    durations = abjad.sequence.flatten(durations, depth=-1)
    if isinstance(weights, abjad.Duration):
        weights = [weights]
    elif isinstance(weights, tuple):
        assert len(weights) == 2
        weights = [abjad.Duration(weights)]
    components = rmakers.note(durations, tag=tag)
    voice = rmakers.wrap_in_time_signature_staff(components, time_signatures)
    pheads = _select.pheads(voice)[1:]
    rmakers.repeat_tie(pheads, tag=tag)
    rmakers.force_repeat_tie(voice)
    contents = abjad.mutate.eject_contents(voice)
    music: list[abjad.Leaf | abjad.Tuplet] = []
    for component in contents:
        assert isinstance(component, abjad.Leaf | abjad.Tuplet)
        music.append(component)
    return music


def make_time_signatures(
    time_signatures,
    count: int,
    *,
    fermata_measures: list[int] | None = None,
    rotation: int = 0,
):
    assert isinstance(count, int), repr(count)
    if fermata_measures is not None:
        assert all(isinstance(_, int) for _ in fermata_measures)
        fermata_measures = list(fermata_measures)
    result = []
    time_signatures = abjad.sequence.rotate(time_signatures, rotation)
    time_signatures = abjad.sequence.flatten(time_signatures, depth=1)
    time_signatures_ = abjad.CyclicTuple(time_signatures)
    fermata_measures = fermata_measures or []
    nfms = []
    for n in fermata_measures:
        if 0 < n:
            nfms.append(n)
        elif n == 0:
            raise ValueError(n)
        else:
            nfms.append(count - abs(n) + 1)
    nfms.sort()
    i = 0
    for j in range(count):
        measure_number = j + 1
        if measure_number in nfms:
            result.append(abjad.TimeSignature((1, 4)))
        else:
            time_signature = time_signatures_[i]
            result.append(time_signature)
            i += 1
    return result


def nest(containers: list[abjad.Tuplet], treatment: str) -> abjad.Tuplet:
    assert isinstance(containers, list), repr(containers)
    assert all(isinstance(_, abjad.Container) for _ in containers), repr(containers)
    assert isinstance(treatment, str), repr(treatment)
    if "/" in treatment:
        assert treatment.startswith("+") or treatment.startswith("-"), repr(treatment)
        addendum = abjad.Duration(treatment)
        contents_duration = abjad.get.duration(containers)
        target_duration = contents_duration + addendum
        multiplier = target_duration / contents_duration
        pair = abjad.duration.pair(multiplier)
        nested_tuplet = abjad.Tuplet(pair, [])
        abjad.mutate.wrap(containers, nested_tuplet)
    else:
        assert ":" in treatment
        nested_tuplet = abjad.Tuplet(treatment, [])
        abjad.mutate.wrap(containers, nested_tuplet)
    return nested_tuplet


def parse(string: str) -> list[abjad.Component]:
    tag = _tags.function_name(_frame())
    assert isinstance(string, str), repr(string)
    string = f"{{ {string} }}"
    container = abjad.parse(string, tag=tag)
    components = abjad.mutate.eject_contents(container)
    return components


def prolate(
    tuplet: abjad.Tuplet,
    treatment: int | str | abjad.Duration,
    denominator: int | None = None,
):
    if isinstance(treatment, int):
        extra_count = treatment
        contents_duration = abjad.get.duration(tuplet)
        pair = abjad.duration.with_denominator(contents_duration, denominator)
        contents_duration_pair = pair
        contents_count = contents_duration_pair[0]
        if 0 < extra_count:
            extra_count %= contents_count
        elif extra_count < 0:
            extra_count = abs(extra_count)
            extra_count %= python_math.ceil(contents_count / 2.0)
            extra_count *= -1
        new_contents_count = contents_count + extra_count
        tuplet_multiplier = abjad.Fraction(new_contents_count, contents_count)
        if not abjad.Duration(tuplet_multiplier).normalized():
            message = f"{tuplet!r} gives {tuplet_multiplier}"
            message += " with {contents_count} and {new_contents_count}."
            raise Exception(message)
        pair = abjad.duration.pair(tuplet_multiplier)
        multiplier = pair
    elif isinstance(treatment, str) and ":" in treatment:
        n, d = treatment.split(":")
        multiplier = (int(d), int(n))
    elif isinstance(treatment, abjad.Duration):
        tuplet_duration = treatment
        contents_duration = abjad.get.duration(tuplet)
        multiplier = tuplet_duration / contents_duration
        pair = abjad.duration.pair(multiplier)
        multiplier = pair
    else:
        raise Exception(f"bad treatment: {treatment!r}.")
    tuplet.multiplier = multiplier
    if not abjad.Duration(tuplet.multiplier).normalized():
        tuplet.normalize_multiplier()
    return tuplet


def style_accelerando(
    container: abjad.Container | abjad.Tuplet, exponent: float = 0.625
) -> abjad.Container | abjad.Tuplet:
    assert isinstance(container, abjad.Container), repr(container)
    assert isinstance(exponent, float), repr(exponent)
    return _style_accelerando(container, exponent)


def style_ritardando(
    container: abjad.Container | abjad.Tuplet, exponent: float = 1.625
) -> abjad.Container | abjad.Tuplet:
    assert isinstance(container, abjad.Container), repr(container)
    assert isinstance(exponent, float), repr(exponent)
    return _style_accelerando(container, exponent)
