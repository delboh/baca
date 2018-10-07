"""
Pitch library.
"""
import abjad
import collections as collections_module
import copy
import inspect
import math
import typing
from . import classes


### CLASSES ###

class ArpeggiationSpacingSpecifier(object):
    """
    Arpeggiation spacing specifier.

    ..  container:: example

        >>> specifier = baca.ArpeggiationSpacingSpecifier()
        >>> specifier([[6, 0, 4, 5, 8]])
        CollectionList([<6, 12, 16, 17, 20>])

    ..  container:: example

        >>> specifier = baca.ArpeggiationSpacingSpecifier()
        >>> specifier([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        CollectionList([<0, 2, 10>, <6, 16, 27, 32, 43>, <9>])

    ..  container:: example

        >>> baca.ArpeggiationSpacingSpecifier()
        ArpeggiationSpacingSpecifier()

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_direction',
        '_pattern',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        direction=None,
        pattern=None,
        ):
        if direction is not None:
            assert direction in (abjad.Up, abjad.Down), repr(direction)
        self._direction = direction
        if pattern is not None:
            assert isinstance(pattern, abjad.Pattern), repr(pattern)
        self._pattern = pattern

    ### SPECIAL METHODS ###

    def __call__(self, collections=None):
        """
        Calls specifier on ``collections``.

        ..  container:: example

            >>> specifier = baca.ArpeggiationSpacingSpecifier()
            >>> specifier([])
            PitchSegment([])

        ..  container:: example

            >>> specifier = baca.ArpeggiationSpacingSpecifier()
            >>> specifier() is None
            True

        Returns collection list or none.
        """
        if collections is None:
            return
        if collections == []:
            return PitchSegment(item_class=abjad.NumberedPitch)
        if not isinstance(collections, CollectionList):
            collections = CollectionList(collections)
        pitch_class_collections = collections.to_pitch_classes()
        pattern = self.pattern or abjad.index_all()
        collections_ = []
        total_length = len(collections)
        class_ = ChordalSpacingSpecifier
        direction = self.direction or abjad.Up
        for i in range(total_length):
            if pattern.matches_index(i, total_length):
                pitch_class_collection = pitch_class_collections[i]
                if isinstance(pitch_class_collection, abjad.Set):
                    pitch_classes = list(sorted(pitch_class_collection))
                else:
                    pitch_classes = list(pitch_class_collection)
                if direction == abjad.Up:
                    pitches = class_._to_tightly_spaced_pitches_ascending(
                        pitch_classes,
                        )
                else:
                    pitches = class_._to_tightly_spaced_pitches_descending(
                        pitch_classes,
                        )
                if isinstance(pitch_class_collection, abjad.Set):
                    collection_ = PitchSet(items=pitches)
                else:
                    collection_ = PitchSegment(items=pitches)
                collections_.append(collection_)
            else:
                collections_.append(collections[i])
        return CollectionList(collections_)

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __format__(self, format_specification='') -> str:
        """
        Formats Abjad object.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f'unhashable type: {self}')
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self):
        r"""
        Gets direction.

        ..  container:: example

            >>> music_maker = baca.MusicMaker()

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice_1',
            ...     collections,
            ...     baca.ArpeggiationSpacingSpecifier(
            ...         direction=abjad.Up,
            ...         ),
            ...     baca.bass_to_octave(2),
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
                                d,16
                                bf,16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                fs,16
                                [
                                e16
                                ef'16
                                af'16
                                g''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a,16
                            }
                        }
                    }
                >>

        ..  container:: example

            >>> music_maker = baca.MusicMaker()

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker(
            ...     'Voice_1',
            ...     collections,
            ...     baca.ArpeggiationSpacingSpecifier(
            ...         direction=abjad.Down,
            ...         ),
            ...     baca.bass_to_octave(2),
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
                                d16
                                bf,16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                fs16
                                [
                                e16
                                ef16
                                af,16
                                g,16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a,16
                            }
                        }
                    }
                >>


        Set to up, down or none.

        Returns up, down or none.
        """
        return self._direction

    @property
    def pattern(self):
        """
        Gets pattern.

        Set to pattern or none.

        Returns pattern or none.
        """
        return self._pattern

class ChordalSpacingSpecifier(object):
    """
    Chordal spacing specifier.

    ..  container:: example

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     soprano=7,
        ...     )
        >>> specifier([[-6, -3, -5, -1, -7]])
        CollectionList([<6, 9, 11, 17, 19>])

    ..  container:: example

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=6,
        ...     direction=abjad.Down,
        ...     soprano=7,
        ...     )
        >>> specifier([[-6, -3, -5, -1, -7]])
        CollectionList([<19, 17, 11, 9, 6>])

    ..  container:: example

        >>> specifier = baca.ChordalSpacingSpecifier(
        ...     bass=11,
        ...     direction=abjad.Down,
        ...     soprano=7,
        ...     )
        >>> specifier([[-6, -3, -5, -1, -7]])
        CollectionList([<31, 30, 29, 21, 11>])

    ..  container:: example

        >>> specifier = baca.ChordalSpacingSpecifier()
        >>> specifier([[0, 1, 2]])
        CollectionList([<0, 1, 2>])

        >>> specifier([[0, 2, 1]])
        CollectionList([<0, 1, 2>])

        >>> specifier([[1, 0, 2]])
        CollectionList([<1, 2, 12>])

        >>> specifier([[1, 2, 0]])
        CollectionList([<1, 2, 12>])

        >>> specifier([[2, 0, 1]])
        CollectionList([<2, 12, 13>])

        >>> specifier([[2, 1, 0]])
        CollectionList([<2, 12, 13>])

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bass',
        '_direction',
        '_minimum_semitones',
        '_pattern',
        '_soprano',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        bass=None,
        direction=None,
        minimum_semitones=None,
        pattern=None,
        soprano=None,
        ):
        self._bass = bass
        if direction is not None:
            assert direction in (abjad.Up, abjad.Down)
        self._direction = direction
        if minimum_semitones is not None:
            assert isinstance(minimum_semitones, int)
            assert 1 <= minimum_semitones
        self._minimum_semitones = minimum_semitones
        if pattern is not None:
            assert isinstance(pattern, abjad.Pattern)
        self._pattern = pattern
        self._soprano = soprano

    ### SPECIAL METHODS ###

    def __call__(self, collections=None):
        """
        Calls specifier on ``collections``.

        ..  container:: example

            >>> specifier = baca.ChordalSpacingSpecifier()
            >>> specifier() is None
            True

        Returns pitch collection or none.
        """
        if collections is None:
            return
        if not isinstance(collections, CollectionList):
            collections = CollectionList(collections)
        pattern = self.pattern or abjad.index_all()
        collections_ = []
        total_length = len(collections)
        for i in range(total_length):
            if not pattern.matches_index(i, total_length):
                collections_.append(collections[i])
            else:
                collection = collections[i]
                collection_ = self._space_collection(collection)
                collections_.append(collection_)
        return CollectionList(collections_)

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __format__(self, format_specification='') -> str:
        """
        Formats Abjad object.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f'unhashable type: {self}')
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _sort_pitch_classes_ascending(self, start, pitch_classes):
        pitch_classes, pitch_classes_, iterations = pitch_classes[:], [], 0
        if self.minimum_semitones is not None:
            candidate = start + self.minimum_semitones
        else:
            candidate = start + 1
        while pitch_classes:
            if candidate in pitch_classes:
                pitch_classes_.append(candidate)
                pitch_classes.remove(candidate)
                if self.minimum_semitones is not None:
                    candidate += self.minimum_semitones
            else:
                candidate += 1
            if 999 <= iterations:
                message = 'stuck in while-loop.'
                raise Exception(message)
            iterations += 1
        assert not pitch_classes, repr(pitch_classes)
        return pitch_classes_

    def _sort_pitch_classes_descending(self, start, pitch_classes):
        pitch_classes, pitch_classes_, iterations = pitch_classes[:], [], 0
        if self.minimum_semitones is not None:
            candidate = abjad.NumberedPitchClass(
                start.number - self.minimum_semitones
                )
        else:
            candidate = abjad.NumberedPitchClass(start.number - 1)
        while pitch_classes:
            if candidate in pitch_classes:
                pitch_classes_.append(candidate)
                pitch_classes.remove(candidate)
                if self.minimum_semitones is not None:
                    candidate = abjad.NumberedPitchClass(
                        candidate.number - self.minimum_semitones
                        )
            else:
                candidate = abjad.NumberedPitchClass(candidate.number - 1)
            if 999 <= iterations:
                raise Exception('stuck in while-loop.')
            iterations += 1
        assert not pitch_classes, repr(pitch_classes)
        return pitch_classes_

    def _space_collection(self, collection):
        original_collection = collection
        if isinstance(collection, abjad.Set):
            pitch_classes = list(sorted(collection.to_pitch_classes()))
        else:
            pitch_classes = list(collection.to_pitch_classes())
        cardinality = len(pitch_classes)
        bass, soprano, outer = None, None, []
        if self.bass is not None:
            bass = abjad.NumberedPitchClass(self.bass)
            if bass not in pitch_classes:
                raise ValueError(f'bass pc {bass} not in {pitch_classes}.')
            outer.append(bass)
        if self.soprano is not None:
            soprano = abjad.NumberedPitchClass(self.soprano)
            if soprano not in pitch_classes:
                raise ValueError(f'soprano pc {bass} not in {pitch_classes}.')
            outer.append(soprano)
        inner = []
        for pitch_class in pitch_classes:
            if pitch_class not in outer:
                inner.append(pitch_class)
        pitch_classes = []
        pitches = []
        direction = self.direction or abjad.Up
        if direction is abjad.Up:
            if bass is not None:
                pitch_classes.append(bass)
            elif inner:
                pitch_classes.append(inner.pop(0))
            elif soprano:
                pitch_classes.append(soprano)
                soprano = None
            start = pitch_classes[0]
            inner = self._sort_pitch_classes_ascending(start, inner)
            pitch_classes.extend(inner)
            if soprano:
                pitch_classes.append(soprano)
            pitches = self._to_tightly_spaced_pitches_ascending(pitch_classes)
        else:
            if soprano is not None:
                pitch_classes.append(soprano)
            elif inner:
                pitch_classes.append(inner.pop(0))
            elif bass:
                pitch_classes.append(bass)
                bass = None
            start = pitch_classes[0]
            inner = self._sort_pitch_classes_descending(start, inner)
            pitch_classes.extend(inner)
            if bass:
                pitch_classes.append(bass)
            pitches = self._to_tightly_spaced_pitches_descending(pitch_classes)
        if isinstance(original_collection, abjad.Set):
            return PitchSet(pitches)
        else:
            return PitchSegment(pitches)

    @staticmethod
    def _to_tightly_spaced_pitches_ascending(pitch_classes):
        pitches = []
        pitch_class = pitch_classes[0]
        pitch = abjad.NumberedPitch((pitch_class, 4))
        pitches.append(pitch)
        for pitch_class in pitch_classes[1:]:
            candidate_octave = pitches[-1].octave.number
            candidate = abjad.NumberedPitch((pitch_class, candidate_octave))
            if pitches[-1] <= candidate:
                pitches.append(candidate)
            else:
                octave = candidate_octave + 1
                pitch = abjad.NumberedPitch((pitch_class, octave))
                assert pitches[-1] <= pitch
                pitches.append(pitch)
        return pitches

    @staticmethod
    def _to_tightly_spaced_pitches_descending(pitch_classes):
        pitches = []
        pitch_class = pitch_classes[0]
        pitch = abjad.NumberedPitch((pitch_class, 4))
        pitches.append(pitch)
        for pitch_class in pitch_classes[1:]:
            candidate_octave = pitches[-1].octave.number
            candidate = abjad.NumberedPitch((pitch_class, candidate_octave))
            if candidate <= pitches[-1]:
                pitches.append(candidate)
            else:
                octave = candidate_octave - 1
                pitch = abjad.NumberedPitch((pitch_class, octave))
                assert pitch <= pitches[-1]
                pitches.append(pitch)
        collection = PitchSegment(pitches)
        while collection[-1].octave.number < 4:
            collection = collection.transpose(n=12)
        return collection

    ### PUBLIC PROPERTIES ###

    @property
    def bass(self):
        """
        Gets bass.

        ..  container:: example

            Up-directed bass specification:

            >>> specifier = baca.ChordalSpacingSpecifier(
            ...     bass=None,
            ...     )
            >>> specifier([[-6, -3, -5, -1, -7]])
            CollectionList([<6, 7, 9, 11, 17>])

            >>> specifier = baca.ChordalSpacingSpecifier(
            ...     bass=6,
            ...     )
            >>> specifier([[-6, -3, -5, -1, -7]])
            CollectionList([<6, 7, 9, 11, 17>])

            >>> specifier = baca.ChordalSpacingSpecifier(
            ...     bass=7,
            ...     )
            >>> specifier([[-6, -3, -5, -1, -7]])
            CollectionList([<7, 9, 11, 17, 18>])

            >>> specifier = baca.ChordalSpacingSpecifier(
            ...     bass=9,
            ...     )
            >>> specifier([[-6, -3, -5, -1, -7]])
            CollectionList([<9, 11, 17, 18, 19>])

            >>> specifier = baca.ChordalSpacingSpecifier(
            ...     bass=11,
            ...     )
            >>> specifier([[-6, -3, -5, -1, -7]])
            CollectionList([<11, 17, 18, 19, 21>])

            >>> specifier = baca.ChordalSpacingSpecifier(
            ...     bass=5,
            ...     )
            >>> specifier([[-6, -3, -5, -1, -7]])
            CollectionList([<5, 6, 7, 9, 11>])

        Returns pitch-class or none.
        """
        return self._bass

    @property
    def direction(self):
        """
        Gets direction.

        ..  container:: example

            Up-directed joint control:

            >>> specifier = baca.ChordalSpacingSpecifier(
            ...     bass=6,
            ...     soprano=7,
            ...     )
            >>> specifier([[-6, -3, -5, -1, -7]])
            CollectionList([<6, 9, 11, 17, 19>])

            >>> specifier = baca.ChordalSpacingSpecifier(
            ...     bass=6,
            ...     soprano=9,
            ...     )
            >>> specifier([[-6, -3, -5, -1, -7]])
            CollectionList([<6, 7, 11, 17, 21>])

            >>> specifier = baca.ChordalSpacingSpecifier(
            ...     bass=6,
            ...     soprano=11,
            ...     )
            >>> specifier([[-6, -3, -5, -1, -7]])
            CollectionList([<6, 7, 9, 17, 23>])

            >>> specifier = baca.ChordalSpacingSpecifier(
            ...     bass=6,
            ...     soprano=5
            ...     )
            >>> specifier([[-6, -3, -5, -1, -7]])
            CollectionList([<6, 7, 9, 11, 17>])

        Returns up, down or none.
        """
        return self._direction

    @property
    def minimum_semitones(self):
        """
        Gets minimum semitones.

        ..  container:: example

            Up-directed spacing with semitone constraints.

            First three examples give the same spacing:

            >>> specifier = baca.ChordalSpacingSpecifier(
            ...     bass=6,
            ...     soprano=7,
            ...     )
            >>> specifier([[5, 6, 7, 9, 11]])
            CollectionList([<6, 9, 11, 17, 19>])

            >>> specifier = baca.ChordalSpacingSpecifier(
            ...     bass=6,
            ...     minimum_semitones=1,
            ...     soprano=7,
            ...     )
            >>> specifier([[5, 6, 7, 9, 11]])
            CollectionList([<6, 9, 11, 17, 19>])

            >>> specifier = baca.ChordalSpacingSpecifier(
            ...     bass=6,
            ...     minimum_semitones=2,
            ...     soprano=7,
            ...     )
            >>> specifier([[5, 6, 7, 9, 11]])
            CollectionList([<6, 9, 11, 17, 19>])

            >>> specifier = baca.ChordalSpacingSpecifier(
            ...     bass=6,
            ...     minimum_semitones=3,
            ...     soprano=7,
            ...     )
            >>> specifier([[5, 6, 7, 9, 11]])
            CollectionList([<6, 9, 17, 23, 31>])

        ..  container:: example

            Down-directed spacing with semitone constraints.

            First three examples give the same spacing:

            >>> specifier = baca.ChordalSpacingSpecifier(
            ...     bass=6,
            ...     direction=abjad.Down,
            ...     soprano=7,
            ...     )
            >>> specifier([[5, 6, 7, 9, 11]])
            CollectionList([<19, 17, 11, 9, 6>])

            >>> specifier = baca.ChordalSpacingSpecifier(
            ...     bass=6,
            ...     direction=abjad.Down,
            ...     minimum_semitones=1,
            ...     soprano=7,
            ...     )
            >>> specifier([[5, 6, 7, 9, 11]])
            CollectionList([<19, 17, 11, 9, 6>])

            >>> specifier = baca.ChordalSpacingSpecifier(
            ...     bass=6,
            ...     direction=abjad.Down,
            ...     minimum_semitones=2,
            ...     soprano=7,
            ...     )
            >>> specifier([[5, 6, 7, 9, 11]])
            CollectionList([<19, 17, 11, 9, 6>])

            >>> specifier = baca.ChordalSpacingSpecifier(
            ...     bass=6,
            ...     direction=abjad.Down,
            ...     minimum_semitones=3,
            ...     soprano=7,
            ...     )
            >>> specifier([[5, 6, 7, 9, 11]])
            CollectionList([<31, 23, 17, 9, 6>])

        Set to positive integer or none.

        Returns positive integer or none.
        """
        return self._minimum_semitones

    @property
    def pattern(self):
        """
        Gets pattern.

        Set to pattern or none.

        Returns pattern or none.
        """
        return self._pattern

    @property
    def soprano(self):
        """
        Gets soprano.

        ..  container:: example

            Down-directed soprano control:

            >>> specifier = baca.ChordalSpacingSpecifier(
            ...     direction=abjad.Down,
            ...     soprano=None,
            ...     )
            >>> specifier([[-6, -3, -5, -1, -7]])
            CollectionList([<18, 17, 11, 9, 7>])

            >>> specifier = baca.ChordalSpacingSpecifier(
            ...     direction=abjad.Down,
            ...     soprano=6,
            ...     )
            >>> specifier([[-6, -3, -5, -1, -7]])
            CollectionList([<18, 17, 11, 9, 7>])

            >>> specifier = baca.ChordalSpacingSpecifier(
            ...     direction=abjad.Down,
            ...     soprano=5,
            ...     )
            >>> specifier([[-6, -3, -5, -1, -7]])
            CollectionList([<17, 11, 9, 7, 6>])

            >>> specifier = baca.ChordalSpacingSpecifier(
            ...     direction=abjad.Down,
            ...     soprano=11,
            ...     )
            >>> specifier([[-6, -3, -5, -1, -7]])
            CollectionList([<11, 9, 7, 6, 5>])

            >>> specifier = baca.ChordalSpacingSpecifier(
            ...     direction=abjad.Down,
            ...     soprano=9,
            ...     )
            >>> specifier([[-6, -3, -5, -1, -7]])
            CollectionList([<21, 19, 18, 17, 11>])

            >>> specifier = baca.ChordalSpacingSpecifier(
            ...     direction=abjad.Down,
            ...     soprano=7,
            ...     )
            >>> specifier([[-6, -3, -5, -1, -7]])
            CollectionList([<19, 18, 17, 11, 9>])

        Returns pitch-class or none.
        """
        return self._soprano

class CollectionList(collections_module.Sequence):
    """
    Collection list.

    ..  container:: example

        Initializes numbered pitch segments:

        >>> for collection in baca.CollectionList([
        ...     [12, 14, 18, 17],
        ...     [16, 20, 19],
        ...     ]):
        ...     collection
        ...
        PitchSegment([12, 14, 18, 17])
        PitchSegment([16, 20, 19])

    ..  container:: example

        Initializes named pitch segments:

        >>> for collection in baca.CollectionList([
        ...     [12, 14, 18, 17],
        ...     [16, 20, 19],
        ...     ],
        ...     item_class=abjad.NamedPitch,
        ...     ):
        ...     collection
        ...
        PitchSegment("c'' d'' fs'' f''")
        PitchSegment("e'' af'' g''")

    ..  container:: example

        Initializes numbered pitch-class segments:

        >>> for collection in baca.CollectionList([
        ...     [12, 14, 18, 17],
        ...     [16, 20, 19],
        ...     ],
        ...     item_class=abjad.NumberedPitchClass,
        ...     ):
        ...     collection
        ...
        PitchClassSegment([0, 2, 6, 5])
        PitchClassSegment([4, 8, 7])

    ..  container:: example

        Initializes named pitch-class segments:

        >>> for collection in baca.CollectionList([
        ...     [12, 14, 18, 17],
        ...     [16, 20, 19],
        ...     ],
        ...     item_class=abjad.NamedPitchClass,
        ...     ):
        ...     collection
        ...
        PitchClassSegment("c d fs f")
        PitchClassSegment("e af g")

    ..  container:: example

        Initializes mixed numbered and named pitch segments:

        >>> for collection in baca.CollectionList([
        ...     [12, 14, 18, 17],
        ...     "ff'' gs'' g''",
        ...     ]):
        ...     collection
        ...
        PitchSegment([12, 14, 18, 17])
        PitchSegment("ff'' gs'' g''")

    ..  container:: example

        Initializes numbered pitch sets:

        >>> for collection in baca.CollectionList([
        ...     {12, 14, 18, 17},
        ...     {16, 20, 19},
        ...     ]):
        ...     collection
        ...
        PitchSet([12, 14, 17, 18])
        PitchSet([16, 19, 20])

    ..  container:: example

        Initializes named pitch sets:

        >>> for collection in baca.CollectionList([
        ...     {12, 14, 18, 17},
        ...     {16, 20, 19},
        ...     ],
        ...     item_class=abjad.NamedPitch,
        ...     ):
        ...     collection
        ...
        PitchSet(["c''", "d''", "f''", "fs''"])
        PitchSet(["e''", "g''", "af''"])

    ..  container:: example

        Initializes numbered pitch-class sets:

        >>> for collection in baca.CollectionList([
        ...     {12, 14, 18, 17},
        ...     {16, 20, 19},
        ...     ],
        ...     item_class=abjad.NumberedPitchClass,
        ...     ):
        ...     collection
        ...
        PitchClassSet([0, 2, 5, 6])
        PitchClassSet([4, 7, 8])

    ..  container:: example

        Initializes named pitch-class sets:

        >>> for collection in baca.CollectionList([
        ...     {12, 14, 18, 17},
        ...     {16, 20, 19},
        ...     ],
        ...     item_class=abjad.NamedPitchClass,
        ...     ):
        ...     collection
        ...
        PitchClassSet(['c', 'd', 'f', 'fs'])
        PitchClassSet(['e', 'g', 'af'])

    ..  container:: example

        Initializes mixed numbered and named pitch segments:

        >>> for collection in baca.CollectionList([
        ...     [12, 14, 18, 17],
        ...     "ff'' gs'' g''",
        ...     ]):
        ...     collection
        ...
        PitchSegment([12, 14, 18, 17])
        PitchSegment("ff'' gs'' g''")

    ..  container:: example

        Initializes mixed segments and sets:

        >>> for collection in baca.CollectionList([
        ...     {12, 14, 18, 17},
        ...     [16, 20, 19],
        ...     ]):
        ...     collection
        ...
        PitchSet([12, 14, 17, 18])
        PitchSegment([16, 20, 19])

    ..  container:: example

        Initializes from collection list:

        >>> collections = baca.CollectionList([[12, 13, 14], [15, 16, 17]])
        >>> baca.CollectionList(collections)
        CollectionList([<12, 13, 14>, <15, 16, 17>])

    ..  container:: example

        Initializes from list of collection lists:

        >>> collection_list_1 = baca.CollectionList([[12, 13, 14]])
        >>> collection_list_2 = baca.CollectionList([[15, 16, 17]])
        >>> baca.CollectionList([collection_list_1, collection_list_2])
        CollectionList([<12, 13, 14>, <15, 16, 17>])

    ..  container:: example

        Initializes empty:

        >>> baca.CollectionList()
        CollectionList([])

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_collections',
        '_expression',
        '_item_class',
        )

    _item_class_prototype = (
        abjad.NumberedPitch,
        abjad.NumberedPitchClass,
        abjad.NamedPitch,
        abjad.NamedPitchClass,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        collections=None,
        *,
        item_class=None,
        ):
        self._expression = None
        if item_class is not None:
            if item_class not in self._item_class_prototype:
                raise TypeError(f'only pitch or pitch-class: {item_class!r}.')
        self._item_class = item_class
        collections = self._coerce(collections)
        collections = collections or []
        self._collections = tuple(collections)

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        """
        Adds ``argument`` to collections.

        ..  container:: example

                >>> collections_1 = baca.CollectionList([[12, 14, 18, 17]])
                >>> collections_2 = baca.CollectionList([[16, 20, 19]])
                >>> collections_1 + collections_2
                CollectionList([<12, 14, 18, 17>, <16, 20, 19>])

        Returns new collection list.
        """
        if not isinstance(argument, collections_module.Iterable):
            raise TypeError(f'must be collection list: {argument!r}.')
        argument_collections = [
            self._initialize_collection(_) for _ in argument
            ]
        collections = self.collections + argument_collections
        return abjad.new(self, collections=collections)

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a collection list with collections
        equal to those of this collection list.

        ..  container:: example

            >>> collections_1 = baca.CollectionList([[12, 13, 14], [15, 16, 17]])
            >>> collections_2 = baca.CollectionList([[12, 13, 14], [15, 16, 17]])
            >>> collections_3 = baca.CollectionList([[12, 13, 14]])

            >>> collections_1 == collections_1
            True
            >>> collections_1 == collections_2
            True
            >>> collections_1 == collections_3
            False

            >>> collections_2 == collections_1
            True
            >>> collections_2 == collections_2
            True
            >>> collections_2 == collections_3
            False

            >>> collections_3 == collections_1
            False
            >>> collections_3 == collections_2
            False
            >>> collections_3 == collections_3
            True

        ..  container:: example

            Ignores item class:

            >>> collections_1 = baca.CollectionList(
            ...     collections=[[12, 13, 14], [15, 16, 17]],
            ...     item_class=None,
            ...     )
            >>> collections_2 = baca.CollectionList(
            ...     collections=[[12, 13, 14], [15, 16, 17]],
            ...     item_class=abjad.NumberedPitch,
            ...     )

            >>> collections_1.item_class == collections_2.item_class
            False

            >>> collections_1 == collections_2
            True

        Returns true or false.
        """
        if not isinstance(argument, type(self)):
            return False
        return self.collections == argument.collections

    def __format__(self, format_specification=''):
        """
        Gets storage format of collections.

        ..  container:: example

            >>> collections = baca.CollectionList([
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ...     ])

            >>> abjad.f(collections, strict=89)
            baca.CollectionList(
                collections=[
                    baca.PitchSegment(
                        (
                            abjad.NumberedPitch(12),
                            abjad.NumberedPitch(14),
                            abjad.NumberedPitch(18),
                            abjad.NumberedPitch(17),
                            ),
                        item_class=abjad.NumberedPitch,
                        ),
                    baca.PitchSegment(
                        (
                            abjad.NumberedPitch(16),
                            abjad.NumberedPitch(20),
                            abjad.NumberedPitch(19),
                            ),
                        item_class=abjad.NumberedPitch,
                        ),
                    ],
                )

        Returns string.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __getitem__(self, argument):
        """
        Gets collection or collection slice identified by ``argument``.

        ..  container:: example

            Gets collections:

            >>> collections = baca.CollectionList([
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ...     ])

            >>> collections[0]
            PitchSegment([12, 14, 18, 17])

            >>> collections[-1]
            PitchSegment([16, 20, 19])

        ..  container:: example

            Gets collections lists:

            >>> collections = baca.CollectionList([
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ...     ])

            >>> collections[:1]
            CollectionList([<12, 14, 18, 17>])

            >>> collections[-1:]
            CollectionList([<16, 20, 19>])

        Returns collection.
        """
        collections = self.collections or []
        result = collections.__getitem__(argument)
        try:
            return abjad.new(self, collections=result)
        except TypeError:
            return result

    # TODO: reimplement to show all four types of collection
    def __illustrate__(self):
        r"""
        Illustrates collections.

        ..  container:: example

            >>> collections = baca.CollectionList([
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ...     ])

            >>> abjad.show(collections, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = collections.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                }
                <<
                    \new Staff
                    {
                        \new Voice
                        \with
                        {
                            \consists Horizontal_bracket_engraver
                        }
                        {
                            \time 1/8
                            c''8
                            ^ \markup { 0 }
                            \startGroup
                            d''8
                            fs''8
                            f''8
                            \stopGroup
                            s8
                            e''8
                            ^ \markup { 1 }
                            \startGroup
                            af''8
                            g''8
                            \stopGroup
                            s8
                            \bar "|."                                                                    %! SCORE_1
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        Returns LilyPond file.
        """
        tree = PitchTree(list(self))
        return tree.__illustrate__()

    def __len__(self):
        """
        Gets length of collections.

        ..  container:: example

            >>> collections = baca.CollectionList([
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ...     ])

            >>> len(collections)
            2

        Returns nonnegative integer.
        """
        return len(self.collections)

    def __repr__(self):
        """
        Gets interpreter representation of collections.

        ..  container:: example

            >>> baca.CollectionList([
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ...     ])
            CollectionList([<12, 14, 18, 17>, <16, 20, 19>])

        Returns string.
        """
        collections = self.collections or []
        collections = ', '.join([str(_) for _ in collections])
        string = f'{type(self).__name__}([{collections}])'
        if self._expression:
            string = '*' + string
        return string

    ### PRIVATE METHODS ###

    def _coerce(self, collections):
        prototype = (
            PitchSegment,
            PitchSet,
            PitchClassSegment,
            PitchClassSet,
            )
        collections_ = []
        for item in collections or []:
            if isinstance(item, type(self)):
                for collection in item:
                    collection_ = self._initialize_collection(collection)
                    collections_.append(collection_)
            else:
                collection_ = self._initialize_collection(item)
                collections_.append(collection_)
        collections_ = [self._to_baca_collection(_) for _ in collections_]
        assert all(isinstance(_, prototype) for _ in collections_)
        return collections_

    def _get_format_specification(self):
        return abjad.FormatSpecification(client=self)

    def _get_pitch_class_class(self):
        item_class = self.item_class or abjad.NumberedPitch
        if item_class in (abjad.NumberedPitchClass, abjad.NamedPitchClass):
            return item_class
        elif item_class is abjad.NumberedPitch:
            return abjad.NumberedPitchClass
        elif item_class is abjad.NamedPitch:
            return abjad.NamedPitchClass
        else:
            raise TypeError(f'only pitch or pc class: {item_class!r}.')

    def _initialize_collection(self, argument, prototype=None):
        items = argument
        item_class = self.item_class or abjad.NumberedPitch
        if prototype is not None:
            return abjad.new(prototype, items=items)
        elif isinstance(argument, abjad.Segment):
            return argument
        elif isinstance(argument, abjad.Set):
            return argument
        elif isinstance(argument, set):
            if item_class in (abjad.NumberedPitch, abjad.NamedPitch):
                return abjad.PitchSet(items=items, item_class=item_class)
            elif item_class in (
                abjad.NumberedPitchClass,
                abjad.NamedPitchClass,
                ):
                return PitchClassSet(
                    items=items,
                    item_class=item_class,
                    )
            else:
                raise TypeError(item_class)
        elif self.item_class is not None:
            if item_class in (abjad.NumberedPitch, abjad.NamedPitch):
                return PitchSegment(items=items, item_class=item_class)
            elif item_class in (
                abjad.NumberedPitchClass,
                abjad.NamedPitchClass,
                ):
                return PitchClassSegment(
                    items=items,
                    item_class=item_class,
                    )
            else:
                raise TypeError(item_class)
        else:
            if isinstance(argument, str):
                return PitchSegment(
                    items=items,
                    item_class=abjad.NamedPitch,
                    )
            elif isinstance(argument, collections_module.Iterable):
                return PitchSegment(
                    items=items,
                    item_class=abjad.NumberedPitch,
                    )
            else:
                raise TypeError(f'only string or iterable: {argument!r}.')

    @staticmethod
    def _to_baca_collection(collection):
        abjad_prototype = (
            abjad.PitchClassSegment,
            abjad.PitchClassSet,
            abjad.PitchSegment,
            abjad.PitchSet,
            )
        assert isinstance(collection, abjad_prototype), repr(collection)
        baca_prototype = (
            PitchClassSegment,
            PitchClassSet,
            PitchSegment,
            PitchSet,
            )
        if isinstance(collection, baca_prototype):
            pass
        elif isinstance(collection, abjad.PitchClassSegment):
            collection = PitchClassSegment(
                items=collection,
                item_class=collection.item_class,
                )
        elif isinstance(collection, abjad.PitchClassSet):
            collection = PitchClassSet(
                items=collection,
                item_class=collection.item_class,
                )
        elif isinstance(collection, abjad.PitchSegment):
            collection = PitchSegment(
                items=collection,
                item_class=collection.item_class,
                )
        elif isinstance(collection, abjad.PitchSet):
            collection = PitchSet(
                items=collection,
                item_class=collection.item_class,
                )
        elif isinstance(collection, abjad.PitchSet):
            collection = PitchSet(
                items=collection,
                item_class=collection.item_class,
                )
        else:
            raise TypeError(collection)
        assert isinstance(collection, baca_prototype)
        return collection

    @staticmethod
    def _to_pitch_class_item_class(item_class):
        item_class = item_class or abjad.NumberedPitch
        if item_class in (abjad.NamedPitchClass, abjad.NumberedPitchClass):
            return item_class
        elif item_class is abjad.NamedPitch:
            return abjad.NamedPitchClass
        elif item_class is abjad.NumberedPitch:
            return abjad.NumberedPitchClass
        else:
            raise TypeError(item_class)

    @staticmethod
    def _to_pitch_item_class(item_class):
        item_class = item_class or abjad.NumberedPitch
        if item_class in (abjad.NamedPitch, abjad.NumberedPitch):
            return item_class
        elif item_class is abjad.NamedPitchClass:
            return abjad.NamedPitch
        elif item_class is abjad.NumberedPitchClass:
            return abjad.NumberedPitch
        else:
            raise TypeError(item_class)

    ### PUBLIC PROPERTIES ###

    @property
    def collections(self):
        """
        Gets collections in list.

        ..  container:: example

            >>> collections = baca.CollectionList([
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ...     ])

            >>> collections.collections
            [PitchSegment([12, 14, 18, 17]), PitchSegment([16, 20, 19])]

        Returns list.
        """
        if self._collections:
            return list(self._collections)

    @property
    def item_class(self):
        """
        Gets item class of collections in list.

        Set to class modeling pitch or pitch-class.

        Returns class or none.
        """
        return self._item_class

    ### PUBLIC METHODS ###

    def accumulate(self, operands=None):
        """
        Accumulates ``operands`` against collections to identity.

        ..  container:: example

            Accumulates transposition:

            >>> collections = baca.CollectionList(
            ...     [[0, 2, 6, 5], [4, 8, 7]],
            ...     item_class=abjad.NumberedPitchClass,
            ...     )

            >>> transposition = baca.pitch_class_segment().transpose(n=3)
            >>> for collection in collections.accumulate([transposition]):
            ...     collection
            ...
            PitchClassSegment([0, 2, 6, 5])
            PitchClassSegment([4, 8, 7])
            PitchClassSegment([3, 5, 9, 8])
            PitchClassSegment([7, 11, 10])
            PitchClassSegment([6, 8, 0, 11])
            PitchClassSegment([10, 2, 1])
            PitchClassSegment([9, 11, 3, 2])
            PitchClassSegment([1, 5, 4])

        ..  container:: example

            Accumulates transposition followed by alpha:

            >>> collections = baca.CollectionList(
            ...     [[0, 2, 6, 5], [4, 8, 7]],
            ...     item_class=abjad.NumberedPitchClass,
            ...     )

            >>> transposition = baca.pitch_class_segment().transpose(n=3)
            >>> alpha = baca.pitch_class_segment().alpha()
            >>> operands = [transposition, alpha]
            >>> for collection in collections.accumulate(operands):
            ...     collection
            ...
            PitchClassSegment([0, 2, 6, 5])
            PitchClassSegment([4, 8, 7])
            PitchClassSegment([3, 5, 9, 8])
            PitchClassSegment([7, 11, 10])
            PitchClassSegment([2, 4, 8, 9])
            PitchClassSegment([6, 10, 11])
            PitchClassSegment([5, 7, 11, 0])
            PitchClassSegment([9, 1, 2])
            PitchClassSegment([4, 6, 10, 1])
            PitchClassSegment([8, 0, 3])
            PitchClassSegment([7, 9, 1, 4])
            PitchClassSegment([11, 3, 6])
            PitchClassSegment([6, 8, 0, 5])
            PitchClassSegment([10, 2, 7])
            PitchClassSegment([9, 11, 3, 8])
            PitchClassSegment([1, 5, 10])
            PitchClassSegment([8, 10, 2, 9])
            PitchClassSegment([0, 4, 11])
            PitchClassSegment([11, 1, 5, 0])
            PitchClassSegment([3, 7, 2])
            PitchClassSegment([10, 0, 4, 1])
            PitchClassSegment([2, 6, 3])
            PitchClassSegment([1, 3, 7, 4])
            PitchClassSegment([5, 9, 6])

        Returns new collection list.
        """
        sequence = classes.Sequence(items=self)
        collections = []
        for sequence_ in sequence.accumulate(operands=operands):
            collections.extend(sequence_)
        return abjad.new(self, collections=collections)

    def arpeggiate_down(self, pattern=None):
        """
        Apreggiates collections down according to ``pattern``.

        ..  container:: example

            Down-arpeggiates all collections:

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
            ...     )

            >>> collections.arpeggiate_down()
            CollectionList([<29, 24, 14, 6, 5>, <28, 17, 7>, <3, 2, 1, 0>])

        ..  container:: example

            Down-arpeggiates collection -1:

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
            ...     )

            >>> collections.arpeggiate_down(pattern=[-1])
            CollectionList([<5, 12, 14, 18, 17>, <16, 17, 19>, <3, 2, 1, 0>])

        Returns new collection list.
        """
        if isinstance(pattern, list):
            pattern = abjad.Pattern(indices=pattern)
        pattern = pattern or abjad.index_all()
        length = len(self)
        collections = []
        for i, collection in enumerate(self):
            if pattern.matches_index(i, length):
                if isinstance(collection, abjad.PitchSegment):
                    collection = collection.to_pitch_classes()
                    collection = PitchClassSegment(
                        items=collection,
                        item_class=collection.item_class,
                        )
                collection = collection.arpeggiate_down()
            collections.append(collection)
        return abjad.new(self, collections=collections)

    def arpeggiate_up(self, pattern=None):
        """
        Apreggiates collections up according to ``pattern``.

        ..  container:: example

            Up-arpeggiates all collections:

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
            ...     )

            >>> collections.arpeggiate_up()
            CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <3, 14, 25, 36>])

        ..  container:: example

            Up-arpeggiates collection -1:

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
            ...     )

            >>> collections.arpeggiate_up(pattern=[-1])
            CollectionList([<5, 12, 14, 18, 17>, <16, 17, 19>, <3, 14, 25, 36>])

        Returns new collection list.
        """
        if isinstance(pattern, list):
            pattern = abjad.Pattern(indices=pattern)
        pattern = pattern or abjad.index_all()
        length = len(self)
        collections = []
        for i, collection in enumerate(self):
            if pattern.matches_index(i, length):
                if isinstance(collection, abjad.PitchSegment):
                    collection = collection.to_pitch_classes()
                    collection = PitchClassSegment(
                        items=collection,
                        item_class=collection.item_class,
                        )
                collection = collection.arpeggiate_up()
            collections.append(collection)
        return abjad.new(self, collections=collections)

    def bass_to_octave(self, n=4, pattern=None):
        """
        Octave-transposes collections to bass in octave ``n``.

        ..  container:: example

            Octave-transposes all collections:

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
            ...     )
            >>> collections = collections.arpeggiate_up()

            >>> collections
            CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <3, 14, 25, 36>])

            >>> collections.bass_to_octave(n=3)
            CollectionList([<-7, 0, 2, 6, 17>, <-8, -7, -5>, <-9, 2, 13, 24>])

        ..  container:: example

            Octave-transposes collection -1:

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
            ...     )
            >>> collections = collections.arpeggiate_up()

            >>> collections
            CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <3, 14, 25, 36>])

            >>> collections.bass_to_octave(n=3, pattern=[-1])
            CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <-9, 2, 13, 24>])

        Returns new collection list.
        """
        if isinstance(pattern, list):
            pattern = abjad.Pattern(indices=pattern)
        pattern = pattern or abjad.index_all()
        length = len(self)
        collections = []
        for i, collection in enumerate(self):
            if pattern.matches_index(i, length):
                collection = collection.bass_to_octave(n=n)
            collections.append(collection)
        return abjad.new(self, collections=collections)

    def center_to_octave(self, n=4, pattern=None):
        """
        Octave-transposes collections to center in octave ``n``.

        ..  container:: example

            Octave-transposes all collections:

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
            ...     )
            >>> collections = collections.arpeggiate_up()

            >>> collections
            CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <3, 14, 25, 36>])

            >>> collections.center_to_octave(n=3)
            CollectionList([<-19, -12, -10, -6, 5>, <-8, -7, -5>, <-21, -10, 1, 12>])

        ..  container:: example

            Octave-transposes collection -1:

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
            ...     )
            >>> collections = collections.arpeggiate_up()

            >>> collections
            CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <3, 14, 25, 36>])

            >>> collections.center_to_octave(n=3, pattern=[-1])
            CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <-21, -10, 1, 12>])

        Returns new collection list.
        """
        if isinstance(pattern, list):
            pattern = abjad.Pattern(indices=pattern)
        pattern = pattern or abjad.index_all()
        length = len(self)
        collections = []
        for i, collection in enumerate(self):
            if pattern.matches_index(i, length):
                collection = collection.center_to_octave(n=n)
            collections.append(collection)
        return abjad.new(self, collections=collections)

    def chords(self, pattern=None):
        """
        Turns collections into chords according to ``pattern``.

        ..  container:: example

            Without pattern:

            >>> collections = baca.CollectionList([
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ...     ])

            >>> for collection in collections:
            ...     collection
            ...
            PitchSegment([12, 14, 18, 17])
            PitchSegment([16, 20, 19])
            PitchSegment([12, 14, 18, 17])
            PitchSegment([16, 20, 19])

            >>> for collection in collections.chords():
            ...     collection
            ...
            PitchSet([12, 14, 17, 18])
            PitchSet([16, 19, 20])
            PitchSet([12, 14, 17, 18])
            PitchSet([16, 19, 20])

        ..  container:: example

            With pattern:

            >>> collections = baca.CollectionList([
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ...     ])

            >>> pattern = abjad.index([1], 2)
            >>> for collection in collections.chords(pattern=pattern):
            ...     collection
            ...
            PitchSegment([12, 14, 18, 17])
            PitchSet([16, 19, 20])
            PitchSegment([12, 14, 18, 17])
            PitchSet([16, 19, 20])

        Returns new collection list.
        """
        collections = []
        length = len(self)
        pattern = pattern or abjad.index_all()
        for i, collection in enumerate(self):
            if pattern.matches_index(i, length):
                collections.append(collection.chord())
            else:
                collections.append(collection)
        return abjad.new(self, collections=collections)

    def cursor(self, cyclic=None, singletons=None):
        """
        Wraps collections in cursor.

        ..  container:: example

            >>> collections = baca.CollectionList([[5, 12, 14, 18], [16, 17]])
            >>> cursor = collections.cursor()

            >>> abjad.f(cursor, strict=89)
            baca.Cursor(
                source=baca.CollectionList(
                    collections=[
                        baca.PitchSegment(
                            (
                                abjad.NumberedPitch(5),
                                abjad.NumberedPitch(12),
                                abjad.NumberedPitch(14),
                                abjad.NumberedPitch(18),
                                ),
                            item_class=abjad.NumberedPitch,
                            ),
                        baca.PitchSegment(
                            (
                                abjad.NumberedPitch(16),
                                abjad.NumberedPitch(17),
                                ),
                            item_class=abjad.NumberedPitch,
                            ),
                        ],
                    ),
                )

            >>> cursor.next()
            [PitchSegment([5, 12, 14, 18])]

            >>> cursor.next()
            [PitchSegment([16, 17])]

        Returns cursor.
        """
        return classes.Cursor(
            cyclic=cyclic,
            singletons=singletons,
            source=self,
            )

    def flatten(self):
        """
        Flattens collections.

        ..  container:: example

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19]],
            ...     )

            >>> str(collections.flatten())
            '<5, 12, 14, 18, 17, 16, 17, 19>'

        ..  container:: example

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19]],
            ...     item_class=abjad.NamedPitch,
            ...     )

            >>> str(collections.flatten())
            "<f' c'' d'' fs'' f'' e'' f'' g''>"

        Returns collection.
        """
        return self.join()[0]

    def has_duplicate_pitch_classes(self, level=-1):
        """
        Is true when collections have duplicate pitch-classes at ``level``.

        ..  container:: example

            >>> collections = baca.CollectionList([
            ...     [4, 5, 7],
            ...     [15, 16, 17, 19]
            ...     ])

            >>> collections.has_duplicate_pitch_classes(level=1)
            False

            >>> collections.has_duplicate_pitch_classes(level=-1)
            True

        Set ``level`` to 1 or -1.

        Returns true or false.
        """
        pitch_class_class = self._get_pitch_class_class()
        if level == 1:
            for collection in self:
                known_pitch_classes = []
                for item in collection:
                    pitch_class = pitch_class_class(item)
                    if pitch_class in known_pitch_classes:
                        return True
                    known_pitch_classes.append(pitch_class)
        elif level == -1:
            known_pitch_classes = []
            for collection in self:
                for item in collection:
                    pitch_class = pitch_class_class(item)
                    if pitch_class in known_pitch_classes:
                        return True
                    known_pitch_classes.append(pitch_class)
        else:
            raise ValueError(f'level must be 1 or -1: {level!r}.')
        return False

    def has_duplicates(self, level=-1):
        """
        Is true when collections have duplicates at ``level``.

        ..  container:: example

            >>> collections = baca.CollectionList([
            ...     [16, 17], [13], [16, 17],
            ...     ])

            >>> collections.has_duplicates(level=0)
            True

            >>> collections.has_duplicates(level=1)
            False

            >>> collections.has_duplicates(level=-1)
            True

        ..  container:: example

            >>> collections = baca.CollectionList([[16, 17], [14, 20, 14]])

            >>> collections.has_duplicates(level=0)
            False

            >>> collections.has_duplicates(level=1)
            True

            >>> collections.has_duplicates(level=-1)
            True

        ..  container:: example

            >>> collections = baca.CollectionList([
            ...     [16, 17], [14, 20], [14],
            ...     ])

            >>> collections.has_duplicates(level=0)
            False

            >>> collections.has_duplicates(level=1)
            False

            >>> collections.has_duplicates(level=-1)
            True

        Set ``level`` to 0, 1 or -1.

        Returns true or false.
        """
        if level == 0:
            known_items = []
            for collection in self:
                if collection in known_items:
                    return True
                known_items.append(collection)
        elif level == 1:
            for collection in self:
                known_items = []
                for item in collection:
                    if item in known_items:
                        return True
                    known_items.append(item)
        elif level == -1:
            known_items = []
            for collection in self:
                for item in collection:
                    if item in known_items:
                        return True
                    known_items.append(item)
        else:
            raise ValueError(f'level must be 0, 1 or -1: {level!r}.')
        return False

    def has_repeat_pitch_classes(self, level=-1):
        """
        Is true when collections have repeat pitch-classes as ``level``.

        ..  container:: example

            >>> collections = baca.CollectionList([[4, 5, 4, 5], [17, 18]])

            >>> collections.has_repeat_pitch_classes(level=1)
            False

            >>> collections.has_repeat_pitch_classes(level=-1)
            True

        Set ``level`` to 0 or -1.

        Returns true or false.
        """
        pitch_class_class = self._get_pitch_class_class()
        if level == 1:
            for collection in self:
                previous_pitch_class = None
                for item in collection:
                    pitch_class = pitch_class_class(item)
                    if pitch_class == previous_pitch_class:
                        return True
                    previous_pitch_class = pitch_class
        elif level == -1:
            previous_pitch_class = None
            for collection in self:
                for item in collection:
                    pitch_class = pitch_class_class(item)
                    if pitch_class == previous_pitch_class:
                        return True
                    previous_pitch_class = pitch_class
        else:
            raise ValueError(f'level must be 0 or -1: {level!r}.')
        return False

    def has_repeats(self, level=-1):
        """
        Is true when collections have repeats at ``level``.

        ..  container:: example

            >>> collections = baca.CollectionList([[4, 5], [4, 5]])

            >>> collections.has_repeats(level=0)
            True

            >>> collections.has_repeats(level=1)
            False

            >>> collections.has_repeats(level=-1)
            False

        ..  container:: example

            >>> collections = baca.CollectionList([
            ...     [4, 5], [18, 18], [4, 5],
            ...     ])

            >>> collections.has_repeats(level=0)
            False

            >>> collections.has_repeats(level=1)
            True

            >>> collections.has_repeats(level=-1)
            True

        ..  container:: example

            >>> collections = baca.CollectionList([
            ...     [4, 5], [5, 18], [4, 5],
            ...     ])

            >>> collections.has_repeats(level=0)
            False

            >>> collections.has_repeats(level=1)
            False

            >>> collections.has_repeats(level=-1)
            True

        Set ``level`` to 0, 1 or -1.

        Returns true or false.
        """
        if level == 0:
            previous_collection = None
            for collection in self:
                if collection == previous_collection:
                    return True
                previous_collection = collection
        elif level == 1:
            for collection in self:
                previous_item = None
                for item in collection:
                    if item == previous_item:
                        return True
                    previous_item = item
        elif level == -1:
            previous_item = None
            for collection in self:
                for item in collection:
                    if item == previous_item:
                        return True
                    previous_item = item
        else:
            raise ValueError(f'level must be 0, 1 or -1: {level!r}.')
        return False

    def helianthate(self, n=0, m=0):
        """
        Helianthates collections.

        ..  container:: example

            >>> collections = baca.CollectionList([[1, 2, 3], [4, 5], [6, 7, 8]])
            >>> for collection in collections.helianthate(n=-1, m=1):
            ...     collection
            ...
            PitchSegment([1, 2, 3])
            PitchSegment([4, 5])
            PitchSegment([6, 7, 8])
            PitchSegment([5, 4])
            PitchSegment([8, 6, 7])
            PitchSegment([3, 1, 2])
            PitchSegment([7, 8, 6])
            PitchSegment([2, 3, 1])
            PitchSegment([4, 5])
            PitchSegment([1, 2, 3])
            PitchSegment([5, 4])
            PitchSegment([6, 7, 8])
            PitchSegment([4, 5])
            PitchSegment([8, 6, 7])
            PitchSegment([3, 1, 2])
            PitchSegment([7, 8, 6])
            PitchSegment([2, 3, 1])
            PitchSegment([5, 4])

        Returns new collection list.
        """
        collections = classes.Sequence(items=self)
        collections = collections.helianthate(n=n, m=m)
        return abjad.new(self, collections=collections)

    def join(self):
        """
        Joins collections.

        ..  container:: example

            >>> collections = baca.CollectionList([
            ...     [5, 12, 14, 18, 17],
            ...     [16, 17, 19],
            ...     ])

            >>> collections.join()
            CollectionList([<5, 12, 14, 18, 17, 16, 17, 19>])

        Returns new collection list.
        """
        collections = []
        if self:
            collection = self[0]
            for collection_ in self[1:]:
                collection = collection + collection_
            collections.append(collection)
        return abjad.new(self, collections=collections)

    def partition(self, argument, cyclic=False, join=False, overhang=False):
        """
        Partitions collections according to ``argument``.

        ..  container:: example

            Returns sequence:

            >>> collections = baca.CollectionList([
            ...     [5, 12, 14, 18, 17],
            ...     [16, 17, 19],
            ...     [16, 17, 19],
            ...     ])

            >>> sequence = collections.partition([1, 2], overhang=abjad.Exact)
            >>> for collection_list in sequence:
            ...     collection_list
            ...
            CollectionList([<5, 12, 14, 18, 17>])
            CollectionList([<16, 17, 19>, <16, 17, 19>])

            >>> isinstance(sequence, baca.Sequence)
            True

        ..  container:: example

            Joins parts. Returns new collection list:

            >>> collections = baca.CollectionList([
            ...     [5, 12, 14, 18, 17],
            ...     [16, 17, 19],
            ...     [16, 17, 19],
            ...     ])

            >>> collections
            CollectionList([<5, 12, 14, 18, 17>, <16, 17, 19>, <16, 17, 19>])

            >>> collections.partition([1, 2], join=True, overhang=abjad.Exact)
            CollectionList([<5, 12, 14, 18, 17>, <16, 17, 19, 16, 17, 19>])

        ..  container:: example

            Repeats, partitions, joins parts. Returns new collection list:

            >>> collections = baca.CollectionList([
            ...     [5, 12, 14, 18, 17],
            ...     [16, 17, 19],
            ...     [16, 17, 19],
            ...     ])

            >>> collections = collections.repeat(2)
            >>> for collection in collections.partition(
            ...     [2],
            ...     cyclic=True,
            ...     join=True,
            ...     ):
            ...     collection
            ...
            PitchSegment([5, 12, 14, 18, 17, 16, 17, 19])
            PitchSegment([16, 17, 19, 5, 12, 14, 18, 17])
            PitchSegment([16, 17, 19, 16, 17, 19])

        Returns sequence.
        """
        if isinstance(argument, abjad.Ratio):
            message = 'implement ratio-partition at some point.'
            raise NotImplementedError(message)
        sequence = classes.Sequence(self)
        parts = sequence.partition_by_counts(
            argument,
            cyclic=cyclic,
            overhang=overhang,
            )
        collection_lists = [abjad.new(self, collections=_) for _ in parts]
        if join:
            collections = [_.join()[0] for _ in collection_lists]
            result = abjad.new(self, collections=collections)
        else:
            result = classes.Sequence(collection_lists)
        return result

    def read(self, counts=None, check=None):
        """
        Reads collections by ``counts``.

        ..  container:: example

            >>> collections = baca.CollectionList([
            ...     [5, 12, 14, 18, 17],
            ...     [16, 17, 19],
            ...     ])

            >>> for collection in collections.read([3, 3, 3, 5, 5, 5]):
            ...     collection
            ...
            PitchSegment([5, 12, 14])
            PitchSegment([18, 17, 16])
            PitchSegment([17, 19, 5])
            PitchSegment([12, 14, 18, 17, 16])
            PitchSegment([17, 19, 5, 12, 14])
            PitchSegment([18, 17, 16, 17, 19])

        ..  container:: example exception

            Raises exception on inexact read:

            >>> collections = baca.CollectionList([
            ...     [5, 12, 14, 18, 17],
            ...     [16, 17, 19],
            ...     ])

            >>> len(collections.flatten())
            8

            >>> collections.read([10, 10, 10], check=abjad.Exact)
            Traceback (most recent call last):
                ...
            ValueError: call reads 30 items; not a multiple of 8 items.

        Returns new collection list.
        """
        if counts in (None, []):
            return abjad.new(self)
        counts = list(counts)
        assert all(isinstance(_, int) for _ in counts), repr(counts)
        collection = self.join()[0]
        source = abjad.CyclicTuple(collection)
        i = 0
        collections = []
        for count in counts:
            stop = i + count
            items = source[i:stop]
            collection = self._initialize_collection(items)
            collections.append(collection)
            i += count
        result = abjad.new(self, collections=collections)
        if check == abjad.Exact:
            self_item_count = len(self.flatten())
            result_item_count = len(result.flatten())
            quotient = result_item_count / self_item_count
            if quotient != int(quotient):
                message = f'call reads {result_item_count} items;'
                message += f' not a multiple of {self_item_count} items.'
                raise ValueError(message)
        return result

    # TODO: change indices to pattern
    # TODO: add level=-1 keyword
    def remove(self, indices=None, period=None):
        """
        Removes collections at ``indices``.

        ..  container:: example

            >>> collections = baca.CollectionList([[0, 1], [2, 3], [4], [5, 6]])
            >>> collections.remove([0, -1])
            CollectionList([<2, 3>, <4>])

        Returns new collection list.
        """
        sequence = classes.Sequence(items=self)
        collections = sequence.remove(indices=indices, period=period)
        return abjad.new(self, collections=collections)

    def remove_duplicate_pitch_classes(self, level=-1):
        """
        Removes duplicate pitch-classes at ``level``.

        ..  container:: example

            >>> collections = baca.CollectionList([[4, 5, 7], [16, 17, 16, 18]])

            >>> collections.remove_duplicate_pitch_classes(level=1)
            CollectionList([<4, 5, 7>, <16, 17, 18>])

            >>> collections.remove_duplicate_pitch_classes(level=-1)
            CollectionList([<4, 5, 7>, <18>])

        Set ``level`` to 1 or -1.

        Returns new collection list.
        """
        pitch_class_class = self._get_pitch_class_class()
        collections_ = []
        if level == 1:
            for collection in self:
                items, known_pitch_classes = [], []
                for item in collection:
                    pitch_class = pitch_class_class(item)
                    if pitch_class in known_pitch_classes:
                        continue
                    known_pitch_classes.append(pitch_class)
                    items.append(item)
                if items:
                    collection_ = self._initialize_collection(items)
                    collections_.append(collection_)
        elif level == -1:
            known_pitch_classes = []
            for collection in self:
                items = []
                for item in collection:
                    pitch_class = pitch_class_class(item)
                    if pitch_class in known_pitch_classes:
                        continue
                    known_pitch_classes.append(pitch_class)
                    items.append(item)
                if items:
                    collection_ = self._initialize_collection(
                        items, collection)
                    collections_.append(collection_)
        else:
            raise ValueError(f'level must be 1 or -1: {level!r}.')
        return abjad.new(self, collections=collections_)

    def remove_duplicates(self, level=-1):
        """
        Removes duplicates at ``level``.

        ..  container:: example

            >>> collections = baca.CollectionList(
            ...     [[16, 17, 16], [13, 14, 16], [16, 17, 16]],
            ...     )

            >>> collections.remove_duplicates(level=0)
            CollectionList([<16, 17, 16>, <13, 14, 16>])

            >>> collections.remove_duplicates(level=1)
            CollectionList([<16, 17>, <13, 14, 16>, <16, 17>])

            >>> collections.remove_duplicates(level=-1)
            CollectionList([<16, 17>, <13, 14>])

        Set ``level`` to 0, 1 or -1.

        Returns new collection list.
        """
        collections_ = []
        if level == 0:
            collections_, known_items = [], []
            for collection in self:
                if collection in known_items:
                    continue
                known_items.append(collection)
                collections_.append(collection)
        elif level == 1:
            for collection in self:
                items, known_items = [], []
                for item in collection:
                    if item in known_items:
                        continue
                    known_items.append(item)
                    items.append(item)
                if items:
                    collection_ = self._initialize_collection(items)
                    collections_.append(collection_)
        elif level == -1:
            known_items = []
            for collection in self:
                items = []
                for item in collection:
                    if item in known_items:
                        continue
                    known_items.append(item)
                    items.append(item)
                if items:
                    collection_ = self._initialize_collection(items)
                    collections_.append(collection_)
        else:
            raise ValueError(f'level must be 0, 1 or -1: {level!r}.')
        return abjad.new(self, collections=collections_)

    def remove_repeat_pitch_classes(self, level=-1):
        """
        Removes repeat pitch-classes at ``level``.

        ..  container:: example

            >>> collections = baca.CollectionList([[4, 4, 4, 5], [17, 18]])

            >>> collections.remove_repeat_pitch_classes(level=1)
            CollectionList([<4, 5>, <17, 18>])

            >>> collections.remove_repeat_pitch_classes(level=-1)
            CollectionList([<4, 5>, <18>])

        Set ``level`` to 1 or -1.

        Returns new collection list.
        """
        pitch_class_class = self._get_pitch_class_class()
        collections_ = []
        if level == 1:
            for collection in self:
                items, previous_pitch_class = [], None
                for item in collection:
                    pitch_class = pitch_class_class(item)
                    if pitch_class == previous_pitch_class:
                        continue
                    items.append(item)
                    previous_pitch_class = pitch_class
                if items:
                    collection_ = self._initialize_collection(items)
                    collections_.append(collection_)
        elif level == -1:
            previous_pitch_class = None
            for collection in self:
                items = []
                for item in collection:
                    pitch_class = pitch_class_class(item)
                    if pitch_class == previous_pitch_class:
                        continue
                    items.append(item)
                    previous_pitch_class = pitch_class
                if items:
                    collection_ = self._initialize_collection(items)
                    collections_.append(collection_)
        else:
            raise ValueError(f'level must be 1 or -1: {level!r}.')
        return abjad.new(self, collections=collections_)

    def remove_repeats(self, level=-1):
        """
        Removes repeats at ``level``.

        ..  container:: example

            >>> collections = baca.CollectionList([[4, 5], [4, 5], [5, 7, 7]])

            >>> collections.remove_repeats(level=0)
            CollectionList([<4, 5>, <5, 7, 7>])

            >>> collections.remove_repeats(level=1)
            CollectionList([<4, 5>, <4, 5>, <5, 7>])

            >>> collections.remove_repeats(level=-1)
            CollectionList([<4, 5>, <4, 5>, <7>])

        Set ``level`` to 0, 1 or -1.

        Returns true or false.
        """
        collections_ = []
        if level == 0:
            previous_collection = None
            for collection in self:
                if collection == previous_collection:
                    continue
                collections_.append(collection)
                previous_collection = collection
        elif level == 1:
            for collection in self:
                items, previous_item = [], None
                for item in collection:
                    if item == previous_item:
                        continue
                    items.append(item)
                    previous_item = item
                if items:
                    collection_ = self._initialize_collection(items)
                    collections_.append(collection_)
        elif level == -1:
            previous_item = None
            for collection in self:
                items = []
                for item in collection:
                    if item == previous_item:
                        continue
                    items.append(item)
                    previous_item = item
                if items:
                    collection_ = self._initialize_collection(items)
                    collections_.append(collection_)
        else:
            raise ValueError(f'level must be 0, 1 or -1: {level!r}.')
        return abjad.new(self, collections=collections_)

    def repeat(self, n=1):
        """
        Repeats collections.

        ..  container:: example

            >>> collections = baca.CollectionList([[12, 14, 18, 17], [16, 19]])
            >>> for collection in collections.repeat(n=3):
            ...     collection
            ...
            PitchSegment([12, 14, 18, 17])
            PitchSegment([16, 19])
            PitchSegment([12, 14, 18, 17])
            PitchSegment([16, 19])
            PitchSegment([12, 14, 18, 17])
            PitchSegment([16, 19])

        Returns new collection list.
        """
        collections = classes.Sequence(items=self)
        collections = collections.repeat(n=n)
        collections = collections.flatten(depth=1)
        return abjad.new(self, collections=collections)

    # TODO: change indices to pattern
    # TODO: add level=-1 keyword
    def retain(self, indices=None, period=None):
        """
        Retains collections at ``indices``.

        ..  container:: example

            >>> collections = baca.CollectionList([[0, 1], [2, 3], [4], [5, 6]])
            >>> collections.retain([0, -1])
            CollectionList([<0, 1>, <5, 6>])

        ..  container:: example

            >>> collections = baca.CollectionList(
            ...     [[0, 1], [2, 3], [4], [5, 6], [7], [8]],
            ...     )
            >>> collections.retain([0], period=2)
            CollectionList([<0, 1>, <4>, <7>])

        Returns new collection list.
        """
        sequence = classes.Sequence(items=self)
        collections = sequence.retain(indices=indices, period=period)
        return abjad.new(self, collections=collections)

    def soprano_to_octave(self, n=4, pattern=None):
        """
        Octave-transposes collections to soprano in octave ``n``.

        ..  container:: example

            Octave-transposes all collections:

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
            ...     )
            >>> collections = collections.arpeggiate_up()

            >>> collections
            CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <3, 14, 25, 36>])

            >>> collections.soprano_to_octave(n=4)
            CollectionList([<-19, -12, -10, -6, 5>, <4, 5, 7>, <-33, -22, -11, 0>])

        ..  container:: example

            Octave-transposes collection -1:

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
            ...     )
            >>> collections = collections.arpeggiate_up()

            >>> collections
            CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <3, 14, 25, 36>])

            >>> collections.soprano_to_octave(n=4, pattern=[-1])
            CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <-33, -22, -11, 0>])

        Returns new collection list.
        """
        if isinstance(pattern, list):
            pattern = abjad.Pattern(indices=pattern)
        pattern = pattern or abjad.index_all()
        length = len(self)
        collections = []
        for i, collection in enumerate(self):
            if pattern.matches_index(i, length):
                collection = collection.soprano_to_octave(n=n)
            collections.append(collection)
        return abjad.new(self, collections=collections)

    def space_down(
        self,
        bass=None,
        pattern=None,
        semitones=None,
        soprano=None,
        ):
        """
        Spaces collections down.

        ..  container:: example

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19]],
            ...     )

            >>> collections.space_down(bass=5)
            CollectionList([<24, 18, 14, 5>, <16, 7, 5>])

        """
        if isinstance(pattern, list):
            pattern = abjad.Pattern(indices=pattern)
        pattern = pattern or abjad.index_all()
        length = len(self)
        collections = []
        for i, collection in enumerate(self):
            if pattern.matches_index(i, length):
                collection = collection.space_down(
                    bass=bass,
                    semitones=semitones,
                    soprano=soprano,
                    )
            collections.append(collection)
        return abjad.new(self, collections=collections)

    def space_up(
        self,
        bass=None,
        pattern=None,
        semitones=None,
        soprano=None,
        ):
        """
        Spaces collections up.

        ..  container:: example

            >>> collections = baca.CollectionList(
            ...     [[5, 12, 14, 18, 17], [16, 17, 19]],
            ...     )

            >>> collections.space_up(bass=5)
            CollectionList([<5, 6, 12, 14>, <5, 7, 16>])

        """
        if isinstance(pattern, list):
            pattern = abjad.Pattern(indices=pattern)
        pattern = pattern or abjad.index_all()
        length = len(self)
        collections = []
        for i, collection in enumerate(self):
            if pattern.matches_index(i, length):
                collection = collection.space_up(
                    bass=bass,
                    semitones=semitones,
                    soprano=soprano,
                    )
            collections.append(collection)
        return abjad.new(self, collections=collections)

    def to_pitch_classes(self):
        """
        Changes to pitch-class collections.

        ..  container:: example

            To numbered pitch-class collections:

            ..  container:: example

                >>> collections = baca.CollectionList(
                ...     [[12, 14, 18, 17], [16, 20, 19]],
                ...     item_class=abjad.NumberedPitch,
                ...     )

                >>> collections.to_pitch_classes()
                CollectionList([PC<0, 2, 6, 5>, PC<4, 8, 7>])

            ..  container:: example

                >>> collections = baca.CollectionList(
                ...     [[0, 2, 6, 5], [4, 8, 7]],
                ...     item_class=abjad.NumberedPitchClass,
                ...     )

                >>> collections.to_pitch_classes()
                CollectionList([PC<0, 2, 6, 5>, PC<4, 8, 7>])

        ..  container:: example

            To named pitch-class collections:

            ..  container:: example

                >>> collections = baca.CollectionList(
                ...     [[12, 14, 18, 17], [16, 20, 19]],
                ...     item_class=abjad.NamedPitch,
                ...     )

                >>> collections.to_pitch_classes()
                CollectionList([PC<c d fs f>, PC<e af g>])

            ..  container:: example

                >>> collections = baca.CollectionList(
                ...     [[0, 2, 6, 5], [4, 8, 7]],
                ...     item_class=abjad.NamedPitchClass,
                ...     )

                >>> collections.to_pitch_classes()
                CollectionList([PC<c d fs f>, PC<e af g>])

        Returns new collection list.
        """
        item_class = self._to_pitch_class_item_class(self.item_class)
        collections_ = []
        for collection in self:
            collection_ = collection.to_pitch_classes()
            collections_.append(collection_)
        return abjad.new(self, collections=collections_, item_class=item_class)

    def to_pitches(self):
        """
        Changes to pitch collections.

        ..  container:: example

            To numbered pitch collections:

            ..  container:: example

                >>> collections = baca.CollectionList(
                ...     [[12, 14, 18, 17], [16, 20, 19]],
                ...     item_class=abjad.NumberedPitch,
                ...     )

                >>> collections.to_pitches()
                CollectionList([<12, 14, 18, 17>, <16, 20, 19>])

            ..  container:: example

                >>> collections = baca.CollectionList(
                ...     [[0, 2, 6, 5], [4, 8, 7]],
                ...     item_class=abjad.NumberedPitchClass,
                ...     )

                >>> collections.to_pitches()
                CollectionList([<0, 2, 6, 5>, <4, 8, 7>])

        ..  container:: example

            To named pitch collections:

            ..  container:: example

                >>> collections = baca.CollectionList(
                ...     [[12, 14, 18, 17], [16, 20, 19]],
                ...     item_class=abjad.NamedPitch,
                ...     )

                >>> collections.to_pitches()
                CollectionList([<c'' d'' fs'' f''>, <e'' af'' g''>])

            ..  container:: example

                >>> collections = baca.CollectionList(
                ...     [[0, 2, 6, 5], [4, 8, 7]],
                ...     item_class=abjad.NamedPitchClass,
                ...     )

                >>> collections.to_pitches()
                CollectionList([<c' d' fs' f'>, <e' af' g'>])

        Returns new collection list.
        """
        item_class = self._to_pitch_item_class(self.item_class)
        collections_ = []
        for collection in self:
            collection_ = collection.to_pitches()
            collections_.append(collection_)
        return abjad.new(self, collections=collections_, item_class=item_class)

    def transpose(self, n=0):
        """
        Transposes collections.

        ..  container:: example

            To numbered pitch collections:

            ..  container:: example

                >>> collections = baca.CollectionList(
                ...     [[12, 14, 18, 17], [16, 20, 19]],
                ...     item_class=abjad.NumberedPitch,
                ...     )

                >>> collections.transpose(28)
                CollectionList([<40, 42, 46, 45>, <44, 48, 47>])

            ..  container:: example

                >>> collections = baca.CollectionList(
                ...     [[0, 2, 6, 5], [4, 8, 7]],
                ...     item_class=abjad.NumberedPitchClass,
                ...     )

                >>> collections.transpose(28)
                CollectionList([PC<4, 6, 10, 9>, PC<8, 0, 11>])

        ..  container:: example

            To named pitch collections:

            ..  container:: example

                >>> collections = baca.CollectionList(
                ...     [[12, 14, 18, 17], [16, 20, 19]],
                ...     item_class=abjad.NamedPitch,
                ...     )

                >>> collections.transpose(-28)
                CollectionList([<af, bf, d df>, <c ff ef>])

            ..  container:: example

                >>> collections = baca.CollectionList(
                ...     [[0, 2, 6, 5], [4, 8, 7]],
                ...     item_class=abjad.NamedPitchClass,
                ...     )

                >>> collections.transpose(-28)
                CollectionList([PC<af bf d df>, PC<c ff ef>])

        Returns new collection list.
        """
        collections_ = []
        for collection in self:
            collection_ = collection.transpose(n)
            collections_.append(collection_)
        return abjad.new(self, collections=collections_)

class Constellation(object):
    """
    Constellation.

    ..  container:: example

        >>> cells = [
        ...     [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]],
        ...     [[-12, -10, -2], [4, 11, 27, 33, 37], [8, 17, 19, 30]],
        ...     [[-8, 2, 15, 25], [-1, 20, 29, 31], [0, 10, 21, 42]],
        ...     [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]],
        ...     [[-12, -9, 1, 4], [-1, 18, 20, 33], [14, 19, 22, 29]],
        ...     [[-10, -2, 0, 5], [-5, 3, 13, 16], [11, 30, 32, 45]],
        ...     [[-10, -2, 5, 15, 25], [-1, 7, 18, 20], [0, 28, 33]],
        ...     [[-12, 17, 27, 37], [-1, 7, 18, 21], [2, 10, 16, 20]],
        ...     ]
        >>> range_ = abjad.PitchRange('[A0, C8]')
        >>> constellation_circuit = baca.ConstellationCircuit(
        ...     cells,
        ...     range_,
        ...     )

        >>> for constellation in constellation_circuit:
        ...     constellation
        Constellation(180)
        Constellation(140)
        Constellation(80)
        Constellation(100)
        Constellation(180)
        Constellation(150)
        Constellation(120)
        Constellation(108)

    """

    ### CLASS VARIABLES ###

    ### INITIALIZER ###

    def __init__(self, circuit, partitioned_generator_pitch_numbers):
        self._circuit = circuit
        self._partitioned_generator_pitch_numbers = \
            partitioned_generator_pitch_numbers
        self._constellate_partitioned_generator_pitch_numbers()
        self._chord_duration = abjad.Duration(1, 4)
        self._chords = []

    ### SPECIAL METHODS ###

    def __contains__(self, pitch_set):
        """
        Is true when constellation contains ``pitch_set``.

        ..  container:: example

            >>> pitch_numbers = [
            ...     -38, -36, -34, -29, -28, -25,
            ...     -21, -20, -19, -18, -15, -11,
            ...     ]
            >>> pitch_set = baca.Sequence(items=pitch_numbers)
            >>> constellation = constellation_circuit[0]
            >>> pitch_set in constellation
            True

        ..  container:: example

            >>> constellation = constellation_circuit[0]
            >>> [-38] in constellation
            False

        Returns true or false.
        """
        return pitch_set in self._pitch_number_lists

    def __getitem__(self, argument):
        """
        Gets item or slice identified by ``argument``.

        ..  container:: example

            >>> constellation = constellation_circuit[0]
            >>> constellation[0]
            Sequence([-38, -36, -34, -29, -28, -25, -21, -20, -19, -18, -15, -11])

        Returns list.
        """
        return self._pitch_number_lists.__getitem__(argument)

    def __len__(self):
        """
        Gets length of constellation.

        ..  container::

            >>> constellation = constellation_circuit[0]
            >>> len(constellation)
            180

        Returns nonnegative integer.
        """
        return len(self._pitch_number_lists)

    def __repr__(self):
        """
        Gets interpreter representation of constellation.

        ..  container:: example

            >>> constellation = constellation_circuit[0]
            >>> constellation
            Constellation(180)

        """
        return f'{type(self).__name__}({len(self)})'

    ### PRIVATE PROPERTIES ###

    @property
    def _color_map(self):
        pitches = self._partitioned_generator_pitch_numbers
        colors = ['red', 'blue', 'green']
        return abjad.ColorMap(colors=colors, pitch_iterables=pitches)

    @property
    def _colored_generator(self):
        generator_chord = self.generator_chord
        abjad.label(generator_chord).color_note_heads(self._color_map)
        return generator_chord

    @property
    def _constellation_number(self):
        constellation_index = self._circuit._constellations.index(self)
        constellation_number = constellation_index + 1
        return constellation_number

    @property
    def _generator_chord_number(self):
        return self.get_number_of_chord(self.generator_chord)

    @property
    def _generator_pitch_numbers(self):
        result = self._partitioned_generator_pitch_numbers
        result = classes.Sequence(result).flatten(depth=-1)
        return list(sorted(result))

    @property
    def _next(self):
        return self._advance(1)

    @property
    def _pivot_chord_number(self):
        pivot = self.pivot_chord
        return self.get_number_of_chord(pivot)

    @property
    def _prev(self):
        return self._advance(-1)

    ### PRIVATE METHODS ###

    def _advance(self, i):
        my_idx = self._circuit._constellations.index(self)
        len_circuit = len(self._circuit)
        next_idx = (my_idx + i) % len_circuit
        next_constellation = self._circuit._constellations[next_idx]
        return next_constellation

    def _constellate_partitioned_generator_pitch_numbers(self):
        self._pitch_number_lists = self.constellate(
            self._partitioned_generator_pitch_numbers,
            self.pitch_range,
            )

    def _label_chord(self, chord):
        chord_number = self.get_number_of_chord(chord)
        label = f'{self._constellation_number}-{chord_number}'
        markup = abjad.Markup(label)
        abjad.attach(markup, chord)

    def _make_lilypond_file_and_score_from_chords(self, chords):
        score, treble, bass = abjad.Score.make_piano_score(
            leaves=chords,
            sketch=True,
            )
        score.override.text_script.staff_padding = 10
        score.set.proportional_notation_duration = abjad.SchemeMoment((1, 30))
        lilypond_file = abjad.LilyPondFile.new(score)
        lilypond_file.default_paper_size = 'letter', 'landscape'
        lilypond_file.global_staff_size = 18
        lilypond_file.layout_block.indent = 0
        lilypond_file.layout_block.ragged_right = True
        lilypond_file.paper_block.system_system_spacing = abjad.SchemeVector(
            abjad.SchemePair('basic_distance', 0),
            abjad.SchemePair('minimum_distance', 0),
            abjad.SchemePair('padding', 12),
            abjad.SchemePair('stretchability', 0),
            )
        lilypond_file.paper_block.top_margin = 24
        return lilypond_file, score

    def _show_chords(self, chords):
        lilypond_file, score = \
            self._make_lilypond_file_and_score_from_chords(chords)
        abjad.show(lilypond_file, strict=89)

    ### PUBLIC PROPERTIES ###

    @property
    def constellation_number(self):
        """
        Gets constellation number.

        ..  container:: example

            >>> constellation = constellation_circuit[0]
            >>> constellation.constellation_number
            1

        Returns positive integer.
        """
        return self._circuit._constellations.index(self) + 1

    @property
    def generator_chord(self):
        r"""
        Gets generator chord.

        ..  container:: example

            >>> constellation = constellation_circuit[0]
            >>> abjad.show(constellation.generator_chord, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(constellation.generator_chord, strict=89)
                <c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                - \markup { 1-80 }

        """
        pitch_numbers = self._generator_pitch_numbers
        generator_chord = abjad.Chord(pitch_numbers, (1, 4))
        self._label_chord(generator_chord)
        return generator_chord

    @property
    def partitioned_generator_pitch_numbers(self):
        """
        Gets partitioned generator pitch numbers.

        ..  container:: example

            >>> for constellation in constellation_circuit:
            ...     constellation.partitioned_generator_pitch_numbers
            [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
            [[-12, -10, -2], [4, 11, 27, 33, 37], [8, 17, 19, 30]]
            [[-8, 2, 15, 25], [-1, 20, 29, 31], [0, 10, 21, 42]]
            [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]]
            [[-12, -9, 1, 4], [-1, 18, 20, 33], [14, 19, 22, 29]]
            [[-10, -2, 0, 5], [-5, 3, 13, 16], [11, 30, 32, 45]]
            [[-10, -2, 5, 15, 25], [-1, 7, 18, 20], [0, 28, 33]]
            [[-12, 17, 27, 37], [-1, 7, 18, 21], [2, 10, 16, 20]]

        Returns list of lists.
        """
        return self._partitioned_generator_pitch_numbers

    @property
    def pitch_range(self):
        """
        Gets pitch range of constellation.

        ..  container:: example

            >>> constellation = constellation_circuit[0]
            >>> constellation.pitch_range
            PitchRange('[A0, C8]')

        """
        return self._circuit.pitch_range

    @property
    def pivot_chord(self):
        r"""
        Gets pivot chord.

        ..  container:: example

            >>> constellation = constellation_circuit[0]
            >>> abjad.show(constellation.pivot_chord, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(constellation.pivot_chord, strict=89)
                <c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                - \markup { 1-80 }

        """
        next_pitch_number_list = self._next._generator_pitch_numbers
        pivot_chord = abjad.Chord(next_pitch_number_list, (1, 4))
        self._label_chord(pivot_chord)
        return pivot_chord

    ### PUBLIC METHODS ###

    @staticmethod
    def constellate(cells, range):
        """
        Constellates ``cells``.

        ..  container:: example

            >>> pitches = [[0, 2, 10], [16, 19, 20]]
            >>> range_ = abjad.PitchRange('[C4, C#7]')
            >>> segments = baca.Constellation.constellate(pitches, range_)
            >>> for segment in segments:
            ...     segment
            Sequence([0, 2, 4, 7, 8, 10])
            Sequence([0, 2, 10, 16, 19, 20])
            Sequence([0, 2, 10, 28, 31, 32])
            Sequence([4, 7, 8, 12, 14, 22])
            Sequence([12, 14, 16, 19, 20, 22])
            Sequence([12, 14, 22, 28, 31, 32])
            Sequence([4, 7, 8, 24, 26, 34])
            Sequence([16, 19, 20, 24, 26, 34])
            Sequence([24, 26, 28, 31, 32, 34])

        ..  container:: example

            >>> pitches = [[4, 8, 11], [7, 15, 17]]
            >>> range_ = abjad.PitchRange('[C4, C#7]')
            >>> segments = baca.Constellation.constellate(pitches, range_)
            >>> for segment in segments:
            ...     segment
            Sequence([4, 7, 8, 11, 15, 17])
            Sequence([4, 8, 11, 19, 27, 29])
            Sequence([7, 15, 16, 17, 20, 23])
            Sequence([16, 19, 20, 23, 27, 29])
            Sequence([7, 15, 17, 28, 32, 35])
            Sequence([19, 27, 28, 29, 32, 35])

        Returns outer product of octave transpositions of ``cells`` in
        ``range``.
        """
        if not isinstance(range, abjad.PitchRange):
            raise TypeError(f'pitch range only: {range!r}.')
        transposition_list = []
        for cell in cells:
            transpositions = range.list_octave_transpositions(cell)
            transposition_list.append(transpositions)
        enumerator = abjad.Enumerator(transposition_list)
        result = enumerator.yield_outer_product()
        result = list(result)
        for i, part in enumerate(result):
            result[i] = classes.Sequence(part).flatten(depth=-1)
        for i, cell in enumerate(result[:]):
            result[i] = cell.sort()
        return result

    def get_chord(self, chord_number):
        """
        Gets chord with 1-indexed chord number.

        ..  container:: example

            >>> constellation = constellation_circuit[0]
            >>> constellation.get_chord(1)
            Sequence([-38, -36, -34, -29, -28, -25, -21, -20, -19, -18, -15, -11])

        Returns list of numbers.
        """
        assert 1 <= chord_number
        chord_index = chord_number - 1
        return self._pitch_number_lists[chord_index]

    def get_number_of_chord(self, chord):
        """
        Gets number of chord.

        ..  container:: example

            >>> constellation = constellation_circuit[0]
            >>> chord = constellation.get_chord(17)
            >>> constellation.get_number_of_chord(chord)
            17

        Returns positive integer.
        """
        chord = abjad.Chord(chord, (1, 4))
        pitch_numbers = [_.number for _ in chord.written_pitches]
        pitch_numbers = classes.Sequence(items=pitch_numbers)
        for i, pitch_number_list in enumerate(self):
            if pitch_number_list == pitch_numbers:
                return i + 1
        raise ValueError(f'{chord} not in {self}')

    def make_chords(self):
        result = []
        for pitch_number_list in self._pitch_number_lists:
            chord = abjad.Chord(pitch_number_list, self._chord_duration)
            result.append(chord)
        return result

    def make_labeled_chords(self):
        result = self.make_chords()
        for chord in result:
            self._label_chord(chord)
        return result

    def make_labeled_colored_chords(self):
        result = self.make_labeled_chords()
        for chord in result:
            abjad.label(chord).color_note_heads(self._color_map)
        return result

    def show_colored_generator_chord(self):
        colored_generator = self._colored_generator
        self._label_chord(colored_generator)
        self._show_chords([colored_generator])

    def show_colored_generator_chord_and_pivot_chord(self):
        colored_generator = self._colored_generator
        self._label_chord(colored_generator)
        pivot = self.pivot_chord
        self._label_chord(pivot)
        self._show_chords([colored_generator, pivot])

    def show_generator_chord(self):
        generator = self.generator_chord
        self._label_chord(generator)
        self._show_chords([generator])

    def show_generator_chord_and_pivot_chord(self):
        generator = self.generator_chord
        self._label_chord(generator)
        pivot = self.pivot_chord
        self._label_chord(pivot)
        self._show_chords([generator, pivot])

    def show_pivot_chord(self):
        pivot = self.pivot_chord
        self._label_chord(pivot)
        self._show_chords([pivot])

class ConstellationCircuit(object):
    """
    Constellation circuit.

    ..  container:: example

        >>> range_ = abjad.PitchRange('[A0, C8]')
        >>> constellation_circuit = baca.ConstellationCircuit(
        ...     baca.ConstellationCircuit.CC1,
        ...     range_,
        ...     )

        >>> for constellation in constellation_circuit:
        ...     constellation
        Constellation(180)
        Constellation(140)
        Constellation(80)
        Constellation(100)
        Constellation(180)
        Constellation(150)
        Constellation(120)
        Constellation(108)

    """

    ### CLASS VARIABLES ###

    CC1 = [
        [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]],
        [[-12, -10, -2], [4, 11, 27, 33, 37], [8, 17, 19, 30]],
        [[-8, 2, 15, 25], [-1, 20, 29, 31], [0, 10, 21, 42]],
        [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]],
        [[-12, -9, 1, 4], [-1, 18, 20, 33], [14, 19, 22, 29]],
        [[-10, -2, 0, 5], [-5, 3, 13, 16], [11, 30, 32, 45]],
        [[-10, -2, 5, 15, 25], [-1, 7, 18, 20], [0, 28, 33]],
        [[-12, 17, 27, 37], [-1, 7, 18, 21], [2, 10, 16, 20]],
        ]

    ### INITIALIZER ###

    def __init__(self, partitioned_generator_pnls, pitch_range):
        self._partitioned_generator_pnls = partitioned_generator_pnls
        self._pitch_range = pitch_range
        self._constellate_partitioned_generator_pnls()

    ### SPECIAL METHODS ###

    def __getitem__(self, argument):
        """
        Gets item or slice identified by ``argument``.

        ..  container:: example

            >>> constellation_circuit[-1]
            Constellation(108)

        Returns constellation.
        """
        return self._constellations.__getitem__(argument)

    def __len__(self):
        """
        Gets length of circuit.

        ..  container:: example

            >>> len(constellation_circuit)
            8

        """
        return len(self._constellations)

    def __repr__(self):
        """
        Gets interpreter representation of circuit.

        ..  container:: example

            >>> constellation_circuit
            ConstellationCircuit(8)

        Returns string.
        """
        return f'{type(self).__name__}({len(self)})'

    ### PRIVATE PROPERTIES ###

    # FIXME
    @property
    def _colored_generator_chords(self):
        result = []
        for constellation in self:
            result.append(constellation._colored_generator)
        return result

    @property
    def _generator_chord_numbers(self):
        result = []
        for constellation in self:
            result.append(constellation._generator_chord_number)
        return result

    @property
    def _pivot_chord_numbers(self):
        result = []
        for constellation in self:
            result.append(constellation._pivot_chord_number)
        return result

    ### PRIVATE METHODS ###

    def _constellate_partitioned_generator_pnls(self):
        self._constellations = []
        enumeration = enumerate(self._partitioned_generator_pnls)
        for i, partitioned_generator_pnl in enumeration:
            constellation = Constellation(
                self,
                partitioned_generator_pnl,
                )
            self._constellations.append(constellation)

    def _illustrate_chords(self, chords):
        result = abjad.Score.make_piano_score(leaves=chords, sketch=True)
        score, treble, bass = result
        abjad.override(score).text_script.staff_padding = 10
        moment = abjad.SchemeMoment((1, 30))
        abjad.setting(score).proportional_notation_duration = moment
        lilypond_file = abjad.LilyPondFile.new(
            score,
            global_staff_size=18,
            )
        lilypond_file.layout_block.indent = 0
        lilypond_file.layout_block.ragged_right = True
        vector = abjad.SpacingVector(0, 0, 12, 0)
        lilypond_file.paper_block.system_system_spacing = vector
        lilypond_file.paper_block.top_margin = 24
        return lilypond_file

    ### PUBLIC PROPERTIES ###

    @property
    def generator_chords(self):
        """
        Gets generator chords.

        ..  container:: example

            >>> for chord in constellation_circuit.generator_chords:
            ...     chord
            Chord("<c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4")
            Chord("<c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4")
            Chord("<e b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4")
            Chord("<e c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4")
            Chord("<c ef b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4")
            Chord("<d g bf c' ef' f' b' cs'' e'' fs''' af''' a''''>4")
            Chord("<d bf b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4")
            Chord("<c b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4")

        Returns list of chords.
        """
        result = []
        for constellation in self:
            result.append(constellation.generator_chord)
        return result

    @property
    def pitch_range(self):
        """
        Gets pitch range.

        ..  container:: example

            >>> constellation_circuit.pitch_range
            PitchRange('[A0, C8]')

        Returns pitch range.
        """
        return self._pitch_range

    @property
    def pivot_chords(self):
        """
        Gets pivot chords.

        ..  container:: example

            >>> for chord in constellation_circuit.pivot_chords:
            ...     chord
            ...
            Chord("<c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4")
            Chord("<e b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4")
            Chord("<e c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4")
            Chord("<c ef b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4")
            Chord("<d g bf c' ef' f' b' cs'' e'' fs''' af''' a''''>4")
            Chord("<d bf b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4")
            Chord("<c b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4")
            Chord("<c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4")

        Returns list of chords.
        """
        result = []
        for constellation in self:
            result.append(constellation.pivot_chord)
        return result

    ### PUBLIC METHODS ###

    def get(self, *arguments):
        """
        Gets constellation in circuit.

        ..  container:: example

            >>> constellation_circuit.get(8)
            Constellation(108)

        ..  container:: example

            >>> constellation_circuit.get(8, 108)
            Sequence([-12, 17, 23, 26, 27, 31, 34, 37, 40, 42, 44, 45])

        Returns constellation or list.
        """
        if len(arguments) == 1:
            constellation_number = arguments[0]
            constellation_index = constellation_number - 1
            return self._constellations[constellation_index]
        elif len(arguments) == 2:
            constellation_number, chord_number = arguments
            constellation_index = constellation_number - 1
            constellation = self._constellations[constellation_index]
            return constellation.get_chord(chord_number)

    def illustrate_colored_generator_chords(self):
        r"""
        Illustrates colored generator chords.

        ..  container:: example

            >>> lilypond_file = constellation_circuit.illustrate_colored_generator_chords()
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TextScript.staff-padding = #10
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 30)
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble_Staff"
                        {
                            \clef "treble"
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                            <b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4
                            <c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4
                            <b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4
                            <c' ef' f' b' cs'' e'' fs''' af''' a''''>4
                            <b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4
                            <b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            <c d bf>4
                            <c d bf>4
                            e4
                            e4
                            <c ef>4
                            <d g bf>4
                            <d bf>4
                            c4
                        }
                    >>
                >>

        Returns LilyPond file.
        """
        return self._illustrate_chords(self._colored_generator_chords)

    def illustrate_colored_generator_chords_and_pivot_chords(self):
        r"""
        Illustrates colored generator chords and pivot chords.

        ..  container:: example

            >>> lilypond_file = constellation_circuit.illustrate_colored_generator_chords_and_pivot_chords()
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TextScript.staff-padding = #10
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 30)
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble_Staff"
                        {
                            \clef "treble"
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                            <b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4
                            <b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4
                            <c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4
                            <c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4
                            <b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4
                            <b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4
                            <c' ef' f' b' cs'' e'' fs''' af''' a''''>4
                            <c' ef' f' b' cs'' e'' fs''' af''' a''''>4
                            <b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4
                            <b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4
                            <b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4
                            <b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            <c d bf>4
                            <c d bf>4
                            <c d bf>4
                            e4
                            e4
                            e4
                            e4
                            <c ef>4
                            <c ef>4
                            <d g bf>4
                            <d g bf>4
                            <d bf>4
                            <d bf>4
                            c4
                            c4
                            <c d bf>4
                        }
                    >>
                >>

        Returns LilyPond file.
        """
        chords = list(zip(self._colored_generator_chords, self.pivot_chords))
        chords = classes.Sequence(chords).flatten(depth=1)
        return self._illustrate_chords(chords)

    def illustrate_generator_chords(self):
        r"""
        Illustrates generator chords.

        ..  container:: example

            >>> lilypond_file = constellation_circuit.illustrate_generator_chords()
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TextScript.staff-padding = #10
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 30)
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble_Staff"
                        {
                            \clef "treble"
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                            <b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4
                            <c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4
                            <b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4
                            <c' ef' f' b' cs'' e'' fs''' af''' a''''>4
                            <b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4
                            <b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            <c d bf>4
                            <c d bf>4
                            e4
                            e4
                            <c ef>4
                            <d g bf>4
                            <d bf>4
                            c4
                        }
                    >>
                >>

        Returns LilyPond file.
        """
        return self._illustrate_chords(self.generator_chords)

    def illustrate_generator_chords_and_pivot_chords(self):
        r"""
        Illustrates generator chords and pivot chords.

        ..  container:: example

            >>> lilypond_file = constellation_circuit.illustrate_generator_chords_and_pivot_chords()
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TextScript.staff-padding = #10
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 30)
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble_Staff"
                        {
                            \clef "treble"
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                            <b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4
                            <b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4
                            <c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4
                            <c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4
                            <b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4
                            <b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4
                            <c' ef' f' b' cs'' e'' fs''' af''' a''''>4
                            <c' ef' f' b' cs'' e'' fs''' af''' a''''>4
                            <b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4
                            <b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4
                            <b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4
                            <b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            <c d bf>4
                            <c d bf>4
                            <c d bf>4
                            e4
                            e4
                            e4
                            e4
                            <c ef>4
                            <c ef>4
                            <d g bf>4
                            <d g bf>4
                            <d bf>4
                            <d bf>4
                            c4
                            c4
                            <c d bf>4
                        }
                    >>
                >>

        Returns LilyPond file.
        """
        chords = list(zip(self.generator_chords, self.pivot_chords))
        chords = classes.Sequence(chords).flatten(depth=1)
        return self._illustrate_chords(chords)

    def illustrate_pivot_chords(self):
        r"""
        Illustrates pivot chords.

        ..  container:: example

            >>> lilypond_file = constellation_circuit.illustrate_pivot_chords()
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TextScript.staff-padding = #10
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 30)
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble_Staff"
                        {
                            \clef "treble"
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                            <b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4
                            <c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4
                            <b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4
                            <c' ef' f' b' cs'' e'' fs''' af''' a''''>4
                            <b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4
                            <b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            <c d bf>4
                            e4
                            e4
                            <c ef>4
                            <d g bf>4
                            <d bf>4
                            c4
                            <c d bf>4
                        }
                    >>
                >>

        Returns LilyPond file.
        """
        return self._illustrate_chords(self.pivot_chords)

    @classmethod
    def make_constellation_circuit_1(class_):
        """
        Makes constellation circuit 1.

            >>> class_ = baca.ConstellationCircuit
            >>> constellation_circuit = class_.make_constellation_circuit_1()
            >>> for constellation in constellation_circuit:
            ...     constellation
            Constellation(180)
            Constellation(140)
            Constellation(80)
            Constellation(100)
            Constellation(180)
            Constellation(150)
            Constellation(120)
            Constellation(108)

        Returns constellation circuit.
        """
        return class_(class_.CC1, abjad.PitchRange('[A0, C8]'))

class DesignMaker(object):
    """
    Design-maker.

    ..  container:: example

        Initializes design-maker:

        >>> baca.DesignMaker()
        DesignMaker()

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_result',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._result = []

    ### SPECIAL METHODS ###

    def __call__(self):
        """
        Calls design-maker.

        Returns pitch-class tree.
        """
        design = PitchTree(items=self._result)
        self._check_duplicate_pitch_classes(design)
        return design

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    @staticmethod
    def _apply_operator(segment, operator):
        assert isinstance(segment, PitchClassSegment)
        assert isinstance(operator, str), repr(operator)
        if operator.startswith('T'):
            index = int(operator[1:])
            segment = segment.transpose(index)
        elif operator == 'I':
            segment = segment.invert()
        elif operator.startswith('M'):
            index = int(operator[1:])
            segment = segment.multiply(index)
        elif operator == 'alpha':
            segment = segment.alpha()
        else:
            raise Exception(f'unrecognized operator: {operator!r}.')
        return segment

    @staticmethod
    def _check_duplicate_pitch_classes(design):
        leaves = design.get_payload()
        for leaf_1, leaf_2 in abjad.Sequence(leaves).nwise():
            if leaf_1 == leaf_2:
                raise Exception(f'duplicate {leaf_1!r}.')

    ### PUBLIC METHODS ###

    def partition(self, cursor, number, counts, operators=None):
        """
        Partitions next ``number`` cells in ``cursor`` by ``counts``.

        Appies optional ``operators`` to resulting parts of partition.

        Returns none.
        """
        cells = cursor.next(number)
        list_ = []
        for cell in cells:
            list_.extend(cell)
        segment = PitchClassSegment(items=list_)
        operators = operators or []
        for operator in operators:
            segment = self._apply_operator(segment, operator)
        sequence = abjad.sequence(segment)
        parts = sequence.partition_by_counts(counts, overhang=True)
        parts = [PitchClassSegment(_) for _ in parts]
        self._result.extend(parts)

    def partition_cyclic(self, cursor, number, counts, operators=None):
        """
        Partitions next `number` cells in `cursor` cyclically by `counts`.

        Applies optional `operators` to parts in resulting partition.

        Returns none.
        """
        cells = cursor.next(number)
        list_ = []
        for cell in cells:
            list_.extend(cell)
        segment = PitchClassSegment(items=list_)
        operators = operators or []
        for operator in operators:
            segment = self._apply_operator(segment, operator)
        sequence = abjad.sequence(segment)
        parts = sequence.partition_by_counts(
            counts,
            cyclic=True,
            overhang=True,
            )
        parts = [PitchClassSegment(_) for _ in parts]
        self._result.extend(parts)

class HarmonicSeries(object):
    r"""
    Harmonic series.

    ..  container:: example

        >>> harmonic_series = baca.HarmonicSeries('C2')
        >>> abjad.show(harmonic_series) # doctest: +SKIP

        ..  docs::

            >>> lilypond_file = harmonic_series.__illustrate__()
            >>> abjad.f(lilypond_file[abjad.Staff])
            \new Staff
            \with
            {
                \override BarLine.stencil = ##f
                \override Stem.transparent = ##t
                \override TextScript.font-size = #-1
                \override TextScript.staff-padding = #6
                \override TimeSignature.stencil = ##f
            }
            {
                \clef "bass"
                c,4
                _ \markup { 1 }
                c4
                _ \markup { 2 }
                g4
                ^ \markup { +2 }
                _ \markup { 3 }
                \clef "treble"
                c'4
                _ \markup { 4 }
                e'4
                ^ \markup { -14 }
                _ \markup { 5 }
                g'4
                ^ \markup { +2 }
                _ \markup { 6 }
                bf'4
                ^ \markup { -31 }
                _ \markup { 7 }
                c''4
                _ \markup { 8 }
                d''4
                ^ \markup { +4 }
                _ \markup { 9 }
                e''4
                ^ \markup { -14 }
                _ \markup { 10 }
                fqs''4
                ^ \markup { +1 }
                _ \markup { 11 }
                g''4
                ^ \markup { +2 }
                _ \markup { 12 }
                aqf''4
                ^ \markup { -9 }
                _ \markup { 13 }
                bf''4
                ^ \markup { -31 }
                _ \markup { 14 }
                b''4
                ^ \markup { -12 }
                _ \markup { 15 }
                c'''4
                _ \markup { 16 }
                cs'''4
                ^ \markup { +5 }
                _ \markup { 17 }
                d'''4
                ^ \markup { +4 }
                _ \markup { 18 }
                ef'''4
                ^ \markup { -2 }
                _ \markup { 19 }
                e'''4
                ^ \markup { -14 }
                _ \markup { 20 }
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_fundamental',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        fundamental: typing.Union[str, abjad.NamedPitch] = 'C1',
        ) -> None:
        fundamental = abjad.NamedPitch(fundamental)
        self._fundamental = fundamental

    ### SPECIAL METHODS ###

    def __illustrate__(self) -> abjad.LilyPondFile:
        r"""
        Illustrates harmonic series.

        ..  container:: example

            >>> harmonic_series = baca.HarmonicSeries('A1')
            >>> abjad.show(harmonic_series) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = harmonic_series.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Staff])
                \new Staff
                \with
                {
                    \override BarLine.stencil = ##f
                    \override Stem.transparent = ##t
                    \override TextScript.font-size = #-1
                    \override TextScript.staff-padding = #6
                    \override TimeSignature.stencil = ##f
                }
                {
                    \clef "bass"
                    a,,4
                    _ \markup { 1 }
                    a,4
                    _ \markup { 2 }
                    e4
                    ^ \markup { +2 }
                    _ \markup { 3 }
                    a4
                    _ \markup { 4 }
                    \clef "treble"
                    cs'4
                    ^ \markup { -14 }
                    _ \markup { 5 }
                    e'4
                    ^ \markup { +2 }
                    _ \markup { 6 }
                    g'4
                    ^ \markup { -31 }
                    _ \markup { 7 }
                    a'4
                    _ \markup { 8 }
                    b'4
                    ^ \markup { +4 }
                    _ \markup { 9 }
                    cs''4
                    ^ \markup { -14 }
                    _ \markup { 10 }
                    dqs''4
                    ^ \markup { +1 }
                    _ \markup { 11 }
                    e''4
                    ^ \markup { +2 }
                    _ \markup { 12 }
                    fqs''4
                    ^ \markup { -9 }
                    _ \markup { 13 }
                    g''4
                    ^ \markup { -31 }
                    _ \markup { 14 }
                    af''4
                    ^ \markup { -12 }
                    _ \markup { 15 }
                    a''4
                    _ \markup { 16 }
                    bf''4
                    ^ \markup { +5 }
                    _ \markup { 17 }
                    b''4
                    ^ \markup { +4 }
                    _ \markup { 18 }
                    c'''4
                    ^ \markup { -2 }
                    _ \markup { 19 }
                    cs'''4
                    ^ \markup { -14 }
                    _ \markup { 20 }
                }

        """
        staff = abjad.Staff()
        for n in range(1, 20 + 1):
            partial = self.partial(n)
            pitch = partial.approximation
            note = abjad.Note.from_pitch_and_duration(pitch, (1, 4))
            staff.append(note)
            deviation = partial.deviation
            if 0 < deviation:
                markup = abjad.Markup(f'+{deviation}', direction=abjad.Up)
                abjad.attach(markup, note)
            elif deviation < 0:
                markup = abjad.Markup(deviation, direction=abjad.Up)
                abjad.attach(markup, note)
            markup = abjad.Markup(n, direction=abjad.Down)
            abjad.attach(markup, note)
        notes = abjad.select(staff).notes()
        if notes[0].written_pitch < abjad.NamedPitch('C4'):
            abjad.attach(abjad.Clef('bass'), staff[0])
            for note in notes[1:]:
                if abjad.NamedPitch('C4') <= note.written_pitch:
                    abjad.attach(abjad.Clef('treble'), note)
                    break
        abjad.override(staff).bar_line.stencil = False
        abjad.override(staff).stem.transparent = True
        abjad.override(staff).text_script.font_size = -1
        abjad.override(staff).text_script.staff_padding = 6
        abjad.override(staff).time_signature.stencil = False
        score = abjad.Score([staff])
        moment = abjad.SchemeMoment((1, 8))
        abjad.setting(score).proportional_notation_duration = moment
        lilypond_file = abjad.LilyPondFile.new(score)
        return lilypond_file

    ### PUBLIC PROPERTIES ###

    @property
    def fundamental(self) -> abjad.NamedPitch:
        """
        Gets fundamental.

        ..  container:: example

            >>> baca.HarmonicSeries('C2').fundamental
            NamedPitch('c,')

        """
        return self._fundamental

    ### PUBLIC METHODS ###

    def partial(self, n: int) -> 'Partial':
        """
        Gets partial ``n``.

        ..  container:: example

            >>> baca.HarmonicSeries('C2').partial(7)
            Partial(fundamental=NamedPitch('c,'), number=7)

        """
        return Partial(
            fundamental=self.fundamental,
            number=n,
            )

class Partial(object):
    """
    Partial.

    ..  container:: example

        >>> baca.Partial('C1', 7)
        Partial(fundamental=NamedPitch('c,,'), number=7)

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_approximation',
        '_deviation',
        '_fundamental',
        '_number',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        fundamental: typing.Union[str, abjad.NamedPitch] = 'C1',
        number: int = 1,
        ) -> None:
        fundamental = abjad.NamedPitch(fundamental)
        self._fundamental = fundamental
        assert isinstance(number, int), repr(number)
        assert 1 <= number, repr(number)
        self._number = number
        hertz = number * fundamental.hertz
        approximation = abjad.NamedPitch.from_hertz(hertz)
        self._approximation = approximation
        deviation_multiplier = hertz / approximation.hertz
        semitone_base = 2 ** abjad.Fraction(1, 12)
        deviation_semitones = math.log(deviation_multiplier, semitone_base)
        deviation_cents = 100 * deviation_semitones
        deviation = round(deviation_cents)
        self._deviation = deviation

    ### SPECIAL METHODS ###

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def approximation(self) -> abjad.NamedPitch:
        """
        Gets approximation.

        ..  container:: example

            >>> baca.Partial('C1', 7).approximation
            NamedPitch('bf')

        """
        return self._approximation

    @property
    def deviation(self) -> int:
        """
        Gets deviation in cents.

        ..  container:: example

            >>> baca.Partial('C1', 7).deviation
            -31

        """
        return self._deviation

    @property
    def fundamental(self) -> abjad.NamedPitch:
        """
        Gets fundamental.

        ..  container:: example

            >>> baca.Partial('C1', 7).fundamental
            NamedPitch('c,,')

        """
        return self._fundamental

    @property
    def number(self) -> int:
        """
        Gets number.

        ..  container:: example

            >>> baca.Partial('C1', 7).number
            7

        """
        return self._number

class PitchClassSegment(abjad.PitchClassSegment):
    r"""
    Pitch-class segment.

    ..  container:: example

        Initializes segment:

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = baca.pitch_class_segment(items=items)
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice], strict=89)
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."                                                                            %! SCORE_1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example expression

            >>> expression = baca.pitch_class_segment()
            >>> segment = expression(items=[-2, -1.5, 6, 7, -1.5, 7])
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice], strict=89)
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."                                                                            %! SCORE_1
                    \override Score.BarLine.transparent = ##f
                }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when segment equals ``argument``.

        ..  container:: example

            Works with Abjad pitch-class segments:

            >>> segment_1 = abjad.PitchClassSegment([0, 1, 2, 3])
            >>> segment_2 = baca.PitchClassSegment([0, 1, 2, 3])

            >>> segment_1 == segment_2
            True

            >>> segment_2 == segment_1
            True

        """
        if (not issubclass(type(argument), type(self)) and
            not issubclass(type(self), type(argument))):
            return False
        return self._collection == argument._collection

    ### PUBLIC METHODS ###

    @abjad.Signature(is_operator=True, method_name='A')
    def alpha(self):
        r"""
        Gets alpha transform of segment.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = baca.pitch_class_segment(items=items)

            >>> abjad.show(J, strict=89) # doctest: +SKIP

        ..  container:: example

            Gets alpha transform of segment:

            ..  container:: example

                >>> J.alpha()
                PitchClassSegment([11, 11.5, 7, 6, 11.5, 6])

                >>> segment = J.alpha()
                >>> abjad.show(segment, strict=89) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice], strict=89)
                    \new Voice
                    {
                        b'8
                        bqs'8
                        g'8
                        fs'8
                        bqs'8
                        fs'8
                        \bar "|."                                                                            %! SCORE_1
                        \override Score.BarLine.transparent = ##f
                    }

            ..  container:: example expression

                >>> expression = baca.pitch_class_segment(name='J')
                >>> expression = expression.alpha()
                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([11, 11.5, 7, 6, 11.5, 6])

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> abjad.show(segment, strict=89) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice], strict=89)
                    \new Voice
                    {
                        b'8
                        bqs'8
                        g'8
                        fs'8
                        bqs'8
                        fs'8
                        \bar "|."                                                                            %! SCORE_1
                        \override Score.BarLine.transparent = ##f
                    }

        ..  container:: example

            Gets alpha transform of alpha transform of segment:

            ..  container:: example

                >>> J.alpha().alpha()
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

                >>> segment = J.alpha().alpha()
                >>> abjad.show(segment, strict=89) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> abjad.f(lilypond_file[abjad.Voice], strict=89)
                    \new Voice
                    {
                        bf'8
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|."                                                                            %! SCORE_1
                        \override Score.BarLine.transparent = ##f
                    }

                >>> segment == J
                True

            ..  container:: example expression

                >>> expression = baca.pitch_class_segment(name='J')
                >>> expression = expression.alpha()
                >>> expression = expression.alpha()

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

                >>> expression.get_string()
                'A(A(J))'

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup, strict=89) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> abjad.f(lilypond_file[abjad.Voice], strict=89)
                    \new Voice
                    {
                        bf'8
                        ^ \markup {
                            \concat
                                {
                                    A
                                    \concat
                                        {
                                            A
                                            \bold
                                                J
                                        }
                                }
                            }
                        bqf'8
                        fs'8
                        g'8
                        bqf'8
                        g'8
                        \bar "|."                                                                            %! SCORE_1
                        \override Score.BarLine.transparent = ##f
                    }

                >>> segment == J
                True

        ..  container:: example

            Returns pitch-class segment:

            >>> isinstance(segment, baca.PitchClassSegment)
            True

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        numbers = []
        for pc in self:
            pc = abs(float(pc.number))
            is_integer = True
            if not abjad.mathtools.is_integer_equivalent_number(pc):
                is_integer = False
                fraction_part = pc - int(pc)
                pc = int(pc)
            if abs(pc) % 2 == 0:
                number = (abs(pc) + 1) % 12
            else:
                number = abs(pc) - 1
            if not is_integer:
                number += fraction_part
            else:
                number = int(number)
            numbers.append(number)
        return type(self)(items=numbers)

    def arpeggiate_down(self):
        r"""
        Arpeggiates pitch-class segment down.

        ..  container:: example

            >>> segment = baca.pitch_class_segment([6, 0, 4, 5, 8])

            >>> segment.arpeggiate_down()
            PitchSegment([42, 36, 28, 17, 8])

            >>> abjad.show(segment.arpeggiate_down(), strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.arpeggiate_down().__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        fs''''1 * 1/8
                        c''''1 * 1/8
                        e'''1 * 1/8
                        f''1 * 1/8
                        af'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        Returns pitch segment.
        """
        specifier = ArpeggiationSpacingSpecifier(direction=abjad.Down)
        result = specifier([self])
        assert len(result) == 1
        segment = result[0]
        assert isinstance(segment, PitchSegment), repr(segment)
        return segment

    def arpeggiate_up(self):
        r"""
        Arpeggiates pitch-class segment up.

        ..  container:: example

            >>> segment = baca.pitch_class_segment([6, 0, 4, 5, 8])

            >>> segment.arpeggiate_up()
            PitchSegment([6, 12, 16, 17, 20])

            >>> abjad.show(segment.arpeggiate_up(), strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.arpeggiate_up().__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        fs'1 * 1/8
                        c''1 * 1/8
                        e''1 * 1/8
                        f''1 * 1/8
                        af''1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        Returns pitch segment.
        """
        specifier = ArpeggiationSpacingSpecifier(direction=abjad.Up)
        result = specifier([self])
        assert len(result) == 1
        segment = result[0]
        assert isinstance(segment, PitchSegment), repr(segment)
        return segment

    def chord(self):
        r"""
        Changes segment to set.

        ..  container:: example

            >>> segment = baca.pitch_class_segment([-2, -1.5, 6, 7])

            >>> segment.chord()
            PitchClassSet([6, 7, 10, 10.5])

            >>> abjad.show(segment.chord(), strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.chord().__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice], strict=89)
                \new Voice
                {
                    <fs' g' bf' bqf'>1
                }

        Returns pitch-class set.
        """
        return PitchClassSet(
            items=self,
            item_class=self.item_class,
            )

    def get_matching_transforms(
        self,
        segment_2,
        inversion=False,
        multiplication=False,
        retrograde=False,
        rotation=False,
        transposition=False,
        ):
        r"""
        Gets transforms of segment that match ``segment_2``.

        ..  container:: example

            Example segments:

            >>> items = [-2, -1, 6, 7, -1, 7]
            >>> segment_1 = baca.PitchClassSegment(items=items)
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            >>> items = [9, 2, 1, 6, 2, 6]
            >>> segment_2 = baca.PitchClassSegment(items=items)
            >>> abjad.show(segment_2, strict=89) # doctest: +SKIP

        ..  container:: example

            Gets matching transforms:

            >>> transforms = segment_1.get_matching_transforms(
            ...     segment_2,
            ...     inversion=True,
            ...     multiplication=True,
            ...     retrograde=True,
            ...     rotation=False,
            ...     transposition=True,
            ...     )
            >>> for operator, transform in transforms:
            ...     print(str(operator), str(transform))
            ...
            M5T11 PC<9, 2, 1, 6, 2, 6>
            M7T1I PC<9, 2, 1, 6, 2, 6>

            >>> transforms = segment_2.get_matching_transforms(
            ...     segment_1,
            ...     inversion=True,
            ...     multiplication=True,
            ...     retrograde=True,
            ...     rotation=False,
            ...     transposition=True,
            ...     )
            >>> for operator, transform in transforms:
            ...     print(str(operator), str(transform))
            ...
            M5T5 PC<10, 11, 6, 7, 11, 7>
            M7T7I PC<10, 11, 6, 7, 11, 7>

        ..  container:: example

            No matching transforms. Segments of differing lengths never
            transform into each other:

            >>> segment_2 = baca.PitchClassSegment(items=[0, 1, 2])
            >>> segment_2.get_matching_transforms(
            ...     segment_1,
            ...     inversion=True,
            ...     multiplication=True,
            ...     retrograde=True,
            ...     rotation=False,
            ...     transposition=True,
            ...     )
            []

        ..  container:: example

            Returns list of pairs:

            >>> isinstance(transforms, list)
            True

        """
        result = []
        if not len(self) == len(segment_2):
            return result
        transforms = self.get_transforms(
            inversion=inversion,
            multiplication=multiplication,
            retrograde=retrograde,
            rotation=rotation,
            transposition=transposition,
            )
        for operator, transform in transforms:
            if transform == segment_2:
                result.append((operator, transform))
        return result

    def get_transforms(
        self,
        inversion=False,
        multiplication=False,
        retrograde=False,
        rotation=False,
        show_identity_operators=False,
        transposition=False,
        ):
        r"""
        Gets transforms of ``segment``.

        ..  container:: example

            Example segment:

            >>> items = [-2, -1, 6, 7, -1, 7]
            >>> J = baca.PitchClassSegment(items=items)
            >>> abjad.show(J, strict=89) # doctest: +SKIP

        ..  container:: example

            Gets identity transform of segment:

            >>> transforms = J.get_transforms()

            >>> for operator, transform in transforms:
            ...     print(str(transform))
            PC<10, 11, 6, 7, 11, 7>

        ..  container:: example

            Gets transpositions of segment:

            >>> transforms = J.get_transforms(transposition=True)

            >>> for i, pair in enumerate(transforms):
            ...     rank = i + 1
            ...     operator, transform = pair
            ...     transform = transform._get_padded_string()
            ...     string = '{:3}:{!s:>4} J:  {!s}'
            ...     string = string.format(rank, operator, transform)
            ...     print(string)
            1:     J:  PC<10, 11,  6,  7, 11,  7>
            2:  T1 J:  PC<11,  0,  7,  8,  0,  8>
            3:  T2 J:  PC< 0,  1,  8,  9,  1,  9>
            4:  T3 J:  PC< 1,  2,  9, 10,  2, 10>
            5:  T4 J:  PC< 2,  3, 10, 11,  3, 11>
            6:  T5 J:  PC< 3,  4, 11,  0,  4,  0>
            7:  T6 J:  PC< 4,  5,  0,  1,  5,  1>
            8:  T7 J:  PC< 5,  6,  1,  2,  6,  2>
            9:  T8 J:  PC< 6,  7,  2,  3,  7,  3>
            10:  T9 J:  PC< 7,  8,  3,  4,  8,  4>
            11: T10 J:  PC< 8,  9,  4,  5,  9,  5>
            12: T11 J:  PC< 9, 10,  5,  6, 10,  6>

        ..  container:: example

            Gets all transforms of segment (without rotation):

            >>> transforms = J.get_transforms(
            ...     inversion=True,
            ...     multiplication=True,
            ...     retrograde=True,
            ...     transposition=True,
            ...     )

            >>> for i, pair in enumerate(transforms):
            ...     rank = i + 1
            ...     operator, transform = pair
            ...     transform = transform._get_padded_string()
            ...     string = '{:3}:{!s:>10} J:  {!s}'
            ...     string = string.format(rank, operator, transform)
            ...     print(string)
            1:           J:  PC<10, 11,  6,  7, 11,  7>
            2:         R J:  PC< 7, 11,  7,  6, 11, 10>
            3:        T1 J:  PC<11,  0,  7,  8,  0,  8>
            4:       RT1 J:  PC< 8,  0,  8,  7,  0, 11>
            5:        T2 J:  PC< 0,  1,  8,  9,  1,  9>
            6:       RT2 J:  PC< 9,  1,  9,  8,  1,  0>
            7:        T3 J:  PC< 1,  2,  9, 10,  2, 10>
            8:       RT3 J:  PC<10,  2, 10,  9,  2,  1>
            9:        T4 J:  PC< 2,  3, 10, 11,  3, 11>
            10:       RT4 J:  PC<11,  3, 11, 10,  3,  2>
            11:        T5 J:  PC< 3,  4, 11,  0,  4,  0>
            12:       RT5 J:  PC< 0,  4,  0, 11,  4,  3>
            13:        T6 J:  PC< 4,  5,  0,  1,  5,  1>
            14:       RT6 J:  PC< 1,  5,  1,  0,  5,  4>
            15:        T7 J:  PC< 5,  6,  1,  2,  6,  2>
            16:       RT7 J:  PC< 2,  6,  2,  1,  6,  5>
            17:        T8 J:  PC< 6,  7,  2,  3,  7,  3>
            18:       RT8 J:  PC< 3,  7,  3,  2,  7,  6>
            19:        T9 J:  PC< 7,  8,  3,  4,  8,  4>
            20:       RT9 J:  PC< 4,  8,  4,  3,  8,  7>
            21:       T10 J:  PC< 8,  9,  4,  5,  9,  5>
            22:      RT10 J:  PC< 5,  9,  5,  4,  9,  8>
            23:       T11 J:  PC< 9, 10,  5,  6, 10,  6>
            24:      RT11 J:  PC< 6, 10,  6,  5, 10,  9>
            25:         I J:  PC< 2,  1,  6,  5,  1,  5>
            26:        RI J:  PC< 5,  1,  5,  6,  1,  2>
            27:       T1I J:  PC< 3,  2,  7,  6,  2,  6>
            28:      RT1I J:  PC< 6,  2,  6,  7,  2,  3>
            29:       T2I J:  PC< 4,  3,  8,  7,  3,  7>
            30:      RT2I J:  PC< 7,  3,  7,  8,  3,  4>
            31:       T3I J:  PC< 5,  4,  9,  8,  4,  8>
            32:      RT3I J:  PC< 8,  4,  8,  9,  4,  5>
            33:       T4I J:  PC< 6,  5, 10,  9,  5,  9>
            34:      RT4I J:  PC< 9,  5,  9, 10,  5,  6>
            35:       T5I J:  PC< 7,  6, 11, 10,  6, 10>
            36:      RT5I J:  PC<10,  6, 10, 11,  6,  7>
            37:       T6I J:  PC< 8,  7,  0, 11,  7, 11>
            38:      RT6I J:  PC<11,  7, 11,  0,  7,  8>
            39:       T7I J:  PC< 9,  8,  1,  0,  8,  0>
            40:      RT7I J:  PC< 0,  8,  0,  1,  8,  9>
            41:       T8I J:  PC<10,  9,  2,  1,  9,  1>
            42:      RT8I J:  PC< 1,  9,  1,  2,  9, 10>
            43:       T9I J:  PC<11, 10,  3,  2, 10,  2>
            44:      RT9I J:  PC< 2, 10,  2,  3, 10, 11>
            45:      T10I J:  PC< 0, 11,  4,  3, 11,  3>
            46:     RT10I J:  PC< 3, 11,  3,  4, 11,  0>
            47:      T11I J:  PC< 1,  0,  5,  4,  0,  4>
            48:     RT11I J:  PC< 4,  0,  4,  5,  0,  1>
            49:           J:  PC<10, 11,  6,  7, 11,  7>
            50:         R J:  PC< 7, 11,  7,  6, 11, 10>
            51:        T1 J:  PC<11,  0,  7,  8,  0,  8>
            52:       RT1 J:  PC< 8,  0,  8,  7,  0, 11>
            53:        T2 J:  PC< 0,  1,  8,  9,  1,  9>
            54:       RT2 J:  PC< 9,  1,  9,  8,  1,  0>
            55:        T3 J:  PC< 1,  2,  9, 10,  2, 10>
            56:       RT3 J:  PC<10,  2, 10,  9,  2,  1>
            57:        T4 J:  PC< 2,  3, 10, 11,  3, 11>
            58:       RT4 J:  PC<11,  3, 11, 10,  3,  2>
            59:        T5 J:  PC< 3,  4, 11,  0,  4,  0>
            60:       RT5 J:  PC< 0,  4,  0, 11,  4,  3>
            61:        T6 J:  PC< 4,  5,  0,  1,  5,  1>
            62:       RT6 J:  PC< 1,  5,  1,  0,  5,  4>
            63:        T7 J:  PC< 5,  6,  1,  2,  6,  2>
            64:       RT7 J:  PC< 2,  6,  2,  1,  6,  5>
            65:        T8 J:  PC< 6,  7,  2,  3,  7,  3>
            66:       RT8 J:  PC< 3,  7,  3,  2,  7,  6>
            67:        T9 J:  PC< 7,  8,  3,  4,  8,  4>
            68:       RT9 J:  PC< 4,  8,  4,  3,  8,  7>
            69:       T10 J:  PC< 8,  9,  4,  5,  9,  5>
            70:      RT10 J:  PC< 5,  9,  5,  4,  9,  8>
            71:       T11 J:  PC< 9, 10,  5,  6, 10,  6>
            72:      RT11 J:  PC< 6, 10,  6,  5, 10,  9>
            73:         I J:  PC< 2,  1,  6,  5,  1,  5>
            74:        RI J:  PC< 5,  1,  5,  6,  1,  2>
            75:       T1I J:  PC< 3,  2,  7,  6,  2,  6>
            76:      RT1I J:  PC< 6,  2,  6,  7,  2,  3>
            77:       T2I J:  PC< 4,  3,  8,  7,  3,  7>
            78:      RT2I J:  PC< 7,  3,  7,  8,  3,  4>
            79:       T3I J:  PC< 5,  4,  9,  8,  4,  8>
            80:      RT3I J:  PC< 8,  4,  8,  9,  4,  5>
            81:       T4I J:  PC< 6,  5, 10,  9,  5,  9>
            82:      RT4I J:  PC< 9,  5,  9, 10,  5,  6>
            83:       T5I J:  PC< 7,  6, 11, 10,  6, 10>
            84:      RT5I J:  PC<10,  6, 10, 11,  6,  7>
            85:       T6I J:  PC< 8,  7,  0, 11,  7, 11>
            86:      RT6I J:  PC<11,  7, 11,  0,  7,  8>
            87:       T7I J:  PC< 9,  8,  1,  0,  8,  0>
            88:      RT7I J:  PC< 0,  8,  0,  1,  8,  9>
            89:       T8I J:  PC<10,  9,  2,  1,  9,  1>
            90:      RT8I J:  PC< 1,  9,  1,  2,  9, 10>
            91:       T9I J:  PC<11, 10,  3,  2, 10,  2>
            92:      RT9I J:  PC< 2, 10,  2,  3, 10, 11>
            93:      T10I J:  PC< 0, 11,  4,  3, 11,  3>
            94:     RT10I J:  PC< 3, 11,  3,  4, 11,  0>
            95:      T11I J:  PC< 1,  0,  5,  4,  0,  4>
            96:     RT11I J:  PC< 4,  0,  4,  5,  0,  1>
            97:        M5 J:  PC< 2,  7,  6, 11,  7, 11>
            98:       RM5 J:  PC<11,  7, 11,  6,  7,  2>
            99:      M5T1 J:  PC< 7,  0, 11,  4,  0,  4>
            100:     RM5T1 J:  PC< 4,  0,  4, 11,  0,  7>
            101:      M5T2 J:  PC< 0,  5,  4,  9,  5,  9>
            102:     RM5T2 J:  PC< 9,  5,  9,  4,  5,  0>
            103:      M5T3 J:  PC< 5, 10,  9,  2, 10,  2>
            104:     RM5T3 J:  PC< 2, 10,  2,  9, 10,  5>
            105:      M5T4 J:  PC<10,  3,  2,  7,  3,  7>
            106:     RM5T4 J:  PC< 7,  3,  7,  2,  3, 10>
            107:      M5T5 J:  PC< 3,  8,  7,  0,  8,  0>
            108:     RM5T5 J:  PC< 0,  8,  0,  7,  8,  3>
            109:      M5T6 J:  PC< 8,  1,  0,  5,  1,  5>
            110:     RM5T6 J:  PC< 5,  1,  5,  0,  1,  8>
            111:      M5T7 J:  PC< 1,  6,  5, 10,  6, 10>
            112:     RM5T7 J:  PC<10,  6, 10,  5,  6,  1>
            113:      M5T8 J:  PC< 6, 11, 10,  3, 11,  3>
            114:     RM5T8 J:  PC< 3, 11,  3, 10, 11,  6>
            115:      M5T9 J:  PC<11,  4,  3,  8,  4,  8>
            116:     RM5T9 J:  PC< 8,  4,  8,  3,  4, 11>
            117:     M5T10 J:  PC< 4,  9,  8,  1,  9,  1>
            118:    RM5T10 J:  PC< 1,  9,  1,  8,  9,  4>
            119:     M5T11 J:  PC< 9,  2,  1,  6,  2,  6>
            120:    RM5T11 J:  PC< 6,  2,  6,  1,  2,  9>
            121:       M5I J:  PC<10,  5,  6,  1,  5,  1>
            122:      RM5I J:  PC< 1,  5,  1,  6,  5, 10>
            123:     M5T1I J:  PC< 3, 10, 11,  6, 10,  6>
            124:    RM5T1I J:  PC< 6, 10,  6, 11, 10,  3>
            125:     M5T2I J:  PC< 8,  3,  4, 11,  3, 11>
            126:    RM5T2I J:  PC<11,  3, 11,  4,  3,  8>
            127:     M5T3I J:  PC< 1,  8,  9,  4,  8,  4>
            128:    RM5T3I J:  PC< 4,  8,  4,  9,  8,  1>
            129:     M5T4I J:  PC< 6,  1,  2,  9,  1,  9>
            130:    RM5T4I J:  PC< 9,  1,  9,  2,  1,  6>
            131:     M5T5I J:  PC<11,  6,  7,  2,  6,  2>
            132:    RM5T5I J:  PC< 2,  6,  2,  7,  6, 11>
            133:     M5T6I J:  PC< 4, 11,  0,  7, 11,  7>
            134:    RM5T6I J:  PC< 7, 11,  7,  0, 11,  4>
            135:     M5T7I J:  PC< 9,  4,  5,  0,  4,  0>
            136:    RM5T7I J:  PC< 0,  4,  0,  5,  4,  9>
            137:     M5T8I J:  PC< 2,  9, 10,  5,  9,  5>
            138:    RM5T8I J:  PC< 5,  9,  5, 10,  9,  2>
            139:     M5T9I J:  PC< 7,  2,  3, 10,  2, 10>
            140:    RM5T9I J:  PC<10,  2, 10,  3,  2,  7>
            141:    M5T10I J:  PC< 0,  7,  8,  3,  7,  3>
            142:   RM5T10I J:  PC< 3,  7,  3,  8,  7,  0>
            143:    M5T11I J:  PC< 5,  0,  1,  8,  0,  8>
            144:   RM5T11I J:  PC< 8,  0,  8,  1,  0,  5>
            145:        M7 J:  PC<10,  5,  6,  1,  5,  1>
            146:       RM7 J:  PC< 1,  5,  1,  6,  5, 10>
            147:      M7T1 J:  PC< 5,  0,  1,  8,  0,  8>
            148:     RM7T1 J:  PC< 8,  0,  8,  1,  0,  5>
            149:      M7T2 J:  PC< 0,  7,  8,  3,  7,  3>
            150:     RM7T2 J:  PC< 3,  7,  3,  8,  7,  0>
            151:      M7T3 J:  PC< 7,  2,  3, 10,  2, 10>
            152:     RM7T3 J:  PC<10,  2, 10,  3,  2,  7>
            153:      M7T4 J:  PC< 2,  9, 10,  5,  9,  5>
            154:     RM7T4 J:  PC< 5,  9,  5, 10,  9,  2>
            155:      M7T5 J:  PC< 9,  4,  5,  0,  4,  0>
            156:     RM7T5 J:  PC< 0,  4,  0,  5,  4,  9>
            157:      M7T6 J:  PC< 4, 11,  0,  7, 11,  7>
            158:     RM7T6 J:  PC< 7, 11,  7,  0, 11,  4>
            159:      M7T7 J:  PC<11,  6,  7,  2,  6,  2>
            160:     RM7T7 J:  PC< 2,  6,  2,  7,  6, 11>
            161:      M7T8 J:  PC< 6,  1,  2,  9,  1,  9>
            162:     RM7T8 J:  PC< 9,  1,  9,  2,  1,  6>
            163:      M7T9 J:  PC< 1,  8,  9,  4,  8,  4>
            164:     RM7T9 J:  PC< 4,  8,  4,  9,  8,  1>
            165:     M7T10 J:  PC< 8,  3,  4, 11,  3, 11>
            166:    RM7T10 J:  PC<11,  3, 11,  4,  3,  8>
            167:     M7T11 J:  PC< 3, 10, 11,  6, 10,  6>
            168:    RM7T11 J:  PC< 6, 10,  6, 11, 10,  3>
            169:       M7I J:  PC< 2,  7,  6, 11,  7, 11>
            170:      RM7I J:  PC<11,  7, 11,  6,  7,  2>
            171:     M7T1I J:  PC< 9,  2,  1,  6,  2,  6>
            172:    RM7T1I J:  PC< 6,  2,  6,  1,  2,  9>
            173:     M7T2I J:  PC< 4,  9,  8,  1,  9,  1>
            174:    RM7T2I J:  PC< 1,  9,  1,  8,  9,  4>
            175:     M7T3I J:  PC<11,  4,  3,  8,  4,  8>
            176:    RM7T3I J:  PC< 8,  4,  8,  3,  4, 11>
            177:     M7T4I J:  PC< 6, 11, 10,  3, 11,  3>
            178:    RM7T4I J:  PC< 3, 11,  3, 10, 11,  6>
            179:     M7T5I J:  PC< 1,  6,  5, 10,  6, 10>
            180:    RM7T5I J:  PC<10,  6, 10,  5,  6,  1>
            181:     M7T6I J:  PC< 8,  1,  0,  5,  1,  5>
            182:    RM7T6I J:  PC< 5,  1,  5,  0,  1,  8>
            183:     M7T7I J:  PC< 3,  8,  7,  0,  8,  0>
            184:    RM7T7I J:  PC< 0,  8,  0,  7,  8,  3>
            185:     M7T8I J:  PC<10,  3,  2,  7,  3,  7>
            186:    RM7T8I J:  PC< 7,  3,  7,  2,  3, 10>
            187:     M7T9I J:  PC< 5, 10,  9,  2, 10,  2>
            188:    RM7T9I J:  PC< 2, 10,  2,  9, 10,  5>
            189:    M7T10I J:  PC< 0,  5,  4,  9,  5,  9>
            190:   RM7T10I J:  PC< 9,  5,  9,  4,  5,  0>
            191:    M7T11I J:  PC< 7,  0, 11,  4,  0,  4>
            192:   RM7T11I J:  PC< 4,  0,  4, 11,  0,  7>
            193:       M11 J:  PC< 2,  1,  6,  5,  1,  5>
            194:      RM11 J:  PC< 5,  1,  5,  6,  1,  2>
            195:     M11T1 J:  PC< 1,  0,  5,  4,  0,  4>
            196:    RM11T1 J:  PC< 4,  0,  4,  5,  0,  1>
            197:     M11T2 J:  PC< 0, 11,  4,  3, 11,  3>
            198:    RM11T2 J:  PC< 3, 11,  3,  4, 11,  0>
            199:     M11T3 J:  PC<11, 10,  3,  2, 10,  2>
            200:    RM11T3 J:  PC< 2, 10,  2,  3, 10, 11>
            201:     M11T4 J:  PC<10,  9,  2,  1,  9,  1>
            202:    RM11T4 J:  PC< 1,  9,  1,  2,  9, 10>
            203:     M11T5 J:  PC< 9,  8,  1,  0,  8,  0>
            204:    RM11T5 J:  PC< 0,  8,  0,  1,  8,  9>
            205:     M11T6 J:  PC< 8,  7,  0, 11,  7, 11>
            206:    RM11T6 J:  PC<11,  7, 11,  0,  7,  8>
            207:     M11T7 J:  PC< 7,  6, 11, 10,  6, 10>
            208:    RM11T7 J:  PC<10,  6, 10, 11,  6,  7>
            209:     M11T8 J:  PC< 6,  5, 10,  9,  5,  9>
            210:    RM11T8 J:  PC< 9,  5,  9, 10,  5,  6>
            211:     M11T9 J:  PC< 5,  4,  9,  8,  4,  8>
            212:    RM11T9 J:  PC< 8,  4,  8,  9,  4,  5>
            213:    M11T10 J:  PC< 4,  3,  8,  7,  3,  7>
            214:   RM11T10 J:  PC< 7,  3,  7,  8,  3,  4>
            215:    M11T11 J:  PC< 3,  2,  7,  6,  2,  6>
            216:   RM11T11 J:  PC< 6,  2,  6,  7,  2,  3>
            217:      M11I J:  PC<10, 11,  6,  7, 11,  7>
            218:     RM11I J:  PC< 7, 11,  7,  6, 11, 10>
            219:    M11T1I J:  PC< 9, 10,  5,  6, 10,  6>
            220:   RM11T1I J:  PC< 6, 10,  6,  5, 10,  9>
            221:    M11T2I J:  PC< 8,  9,  4,  5,  9,  5>
            222:   RM11T2I J:  PC< 5,  9,  5,  4,  9,  8>
            223:    M11T3I J:  PC< 7,  8,  3,  4,  8,  4>
            224:   RM11T3I J:  PC< 4,  8,  4,  3,  8,  7>
            225:    M11T4I J:  PC< 6,  7,  2,  3,  7,  3>
            226:   RM11T4I J:  PC< 3,  7,  3,  2,  7,  6>
            227:    M11T5I J:  PC< 5,  6,  1,  2,  6,  2>
            228:   RM11T5I J:  PC< 2,  6,  2,  1,  6,  5>
            229:    M11T6I J:  PC< 4,  5,  0,  1,  5,  1>
            230:   RM11T6I J:  PC< 1,  5,  1,  0,  5,  4>
            231:    M11T7I J:  PC< 3,  4, 11,  0,  4,  0>
            232:   RM11T7I J:  PC< 0,  4,  0, 11,  4,  3>
            233:    M11T8I J:  PC< 2,  3, 10, 11,  3, 11>
            234:   RM11T8I J:  PC<11,  3, 11, 10,  3,  2>
            235:    M11T9I J:  PC< 1,  2,  9, 10,  2, 10>
            236:   RM11T9I J:  PC<10,  2, 10,  9,  2,  1>
            237:   M11T10I J:  PC< 0,  1,  8,  9,  1,  9>
            238:  RM11T10I J:  PC< 9,  1,  9,  8,  1,  0>
            239:   M11T11I J:  PC<11,  0,  7,  8,  0,  8>
            240:  RM11T11I J:  PC< 8,  0,  8,  7,  0, 11>

        ..  container:: example

            Returns list of pairs:

            >>> isinstance(transforms, list)
            True

        """
        operators = []
        if transposition:
            for n in range(12):
                operator = abjad.CompoundOperator()
                operator = operator.transpose(n=n)
                operators.append(operator)
        else:
            operator = abjad.CompoundOperator()
            operator = operator.transpose()
            operators.append(operator)
        if inversion:
            operators_ = operators[:]
            for operator in operators:
                operator_ = abjad.CompoundOperator()
                operator_ = operator_.invert()
                foo = list(operator_._operators)
                foo.extend(operator.operators)
                operator_._operators = tuple(foo)
                operators_.append(operator_)
            operators = operators_
        if multiplication:
            operators_ = operators[:]
            for operator in operators:
                operator_ = operator.multiply(n=1)
                operators_.append(operator_)
            for operator in operators:
                operator_ = operator.multiply(n=5)
                operators_.append(operator_)
            for operator in operators:
                operator_ = operator.multiply(n=7)
                operators_.append(operator_)
            for operator in operators:
                operator_ = operator.multiply(n=11)
                operators_.append(operator_)
            operators = operators_
        if retrograde:
            operators_ = []
            for operator in operators:
                operators_.append(operator)
                operator_ = operator.retrograde()
                operators_.append(operator_)
            operators = operators_
        if rotation:
            operators_ = []
            for operator in operators:
                for n in range(len(self)):
                    if rotation is abjad.Left:
                        n *= -1
                    operator_ = operator.rotate(n=n)
                    operators_.append(operator_)
            operators = operators_
        result = []
        for operator in operators:
            transform = operator(self)
            result.append((operator, transform))
        return result

    def has_duplicates(self):
        r"""
        Is true when pitch-class segment has duplicates.

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7]
            >>> segment = baca.pitch_class_segment(items=items)
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice], strict=89)
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    \bar "|."                                                                            %! SCORE_1
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment.has_duplicates()
            False

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = baca.pitch_class_segment(items=items)
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice], strict=89)
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."                                                                            %! SCORE_1
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment.has_duplicates()
            True

        Returns true or false.
        """
        return not len(set(self)) == len(self)

    def has_repeats(self):
        r"""
        Is true when pitch-class segment has repeats.

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = baca.pitch_class_segment(items=items)
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice], strict=89)
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."                                                                            %! SCORE_1
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment.has_repeats()
            False

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, 7]
            >>> segment = baca.pitch_class_segment(items=items)
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice], strict=89)
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    g'8
                    \bar "|."                                                                            %! SCORE_1
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment.has_repeats()
            True

        Returns true or false.
        """
        previous_item = None
        for item in self:
            if item == previous_item:
                return True
            previous_item = item
        return False

    def sequence(self):
        r"""
        Changes pitch-class segment into a sequence.

        ..  container:: example

            >>> segment = baca.pitch_class_segment([10, 11, 5, 6, 7])
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice], strict=89)
                \new Voice
                {
                    bf'8
                    b'8
                    f'8
                    fs'8
                    g'8
                    \bar "|."                                                                            %! SCORE_1
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment.sequence()
            Sequence([NumberedPitchClass(10), NumberedPitchClass(11), NumberedPitchClass(5), NumberedPitchClass(6), NumberedPitchClass(7)])

        Returns sequence.
        """
        return classes.Sequence(self)

    def space_down(self, bass=None, semitones=None, soprano=None):
        r"""
        Spaces segment down.

        ..  container:: example

            >>> segment = baca.pitch_class_segment([10, 11, 5, 6, 7])
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice], strict=89)
                \new Voice
                {
                    bf'8
                    b'8
                    f'8
                    fs'8
                    g'8
                    \bar "|."                                                                            %! SCORE_1
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment.space_down(bass=6, soprano=7)
            PitchSegment([19, 17, 11, 10, 6])

            >>> segment = segment.space_down(bass=6, soprano=7)
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override Rest.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble_Staff"
                        {
                            \clef "treble"
                            g''1 * 1/8
                            f''1 * 1/8
                            b'1 * 1/8
                            bf'1 * 1/8
                            fs'1 * 1/8
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                        }
                    >>
                >>

        Returns pitch segment.
        """
        specifier = ChordalSpacingSpecifier(
            bass=bass,
            direction=abjad.Down,
            minimum_semitones=semitones,
            soprano=soprano,
            )
        segments = specifier([self])
        assert len(segments) == 1, repr(segments)
        segment = segments[0]
        if not isinstance(segment, PitchSegment):
            raise TypeError(f'pitch segment only: {segment!r}.')
        return segment

    def space_up(self, bass=None, semitones=None, soprano=None):
        r"""
        Spaces segment up.

        ..  container:: example

            >>> segment = baca.pitch_class_segment([10, 11, 5, 6, 7])
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice], strict=89)
                \new Voice
                {
                    bf'8
                    b'8
                    f'8
                    fs'8
                    g'8
                    \bar "|."                                                                            %! SCORE_1
                    \override Score.BarLine.transparent = ##f
                }

            >>> segment.space_up(bass=6, soprano=7)
            PitchSegment([6, 10, 11, 17, 19])

            >>> segment = segment.space_up(bass=6, soprano=7)
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override Rest.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble_Staff"
                        {
                            \clef "treble"
                            fs'1 * 1/8
                            bf'1 * 1/8
                            b'1 * 1/8
                            f''1 * 1/8
                            g''1 * 1/8
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                            r1 * 1/8
                        }
                    >>
                >>

        Returns pitch segment.
        """
        specifier = ChordalSpacingSpecifier(
            bass=bass,
            direction=abjad.Up,
            minimum_semitones=semitones,
            soprano=soprano,
            )
        segments = specifier([self])
        assert len(segments) == 1, repr(segments)
        segment = segments[0]
        assert isinstance(segment, PitchSegment)
        return segment

class PitchClassSet(abjad.PitchClassSet):
    r"""
    Pitch-class set.

    ..  container:: example

        Initializes set:

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> setting = baca.pitch_class_set(items=items)
            >>> abjad.show(setting, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = setting.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice], strict=89)
                \new Voice
                {
                    <fs' g' bf' bqf'>1
                }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when segment equals ``argument``.

        ..  container:: example

            Works with Abjad pitch-class sets:

            >>> set_1 = abjad.PitchClassSet([0, 1, 2, 3])
            >>> set_2 = baca.PitchClassSet([0, 1, 2, 3])

            >>> set_1 == set_2
            True

            >>> set_2 == set_1
            True

        """
        if (not issubclass(type(argument), type(self)) and
            not issubclass(type(self), type(argument))):
            return False
        return self._collection == argument._collection

    ### PUBLIC METHODS ###

    def to_pitch_classes(self):
        """
        Makes new pitch-class set.

        ..  container:: example

            >>> setting = baca.pitch_class_set([-2, -1.5, 6, 7, -1.5, 7])
            >>> setting
            PitchClassSet([6, 7, 10, 10.5])

            >>> setting.to_pitch_classes()
            PitchClassSet([6, 7, 10, 10.5])

        Returns new pitch-class set.
        """
        return abjad.new(self)

    def to_pitches(self):
        """
        Makes pitch set.

        ..  container:: example

            >>> setting = baca.pitch_class_set([-2, -1.5, 6, 7, -1.5, 7])
            >>> setting
            PitchClassSet([6, 7, 10, 10.5])

            >>> setting.to_pitches()
            PitchSet([6, 7, 10, 10.5])

        Returns pitch set.
        """
        if self.item_class is abjad.NamedPitchClass:
            item_class = abjad.NamedPitch
        elif self.item_class is abjad.NumberedPitchClass:
            item_class = abjad.NumberedPitch
        else:
            raise TypeError(self.item_class)
        return PitchSet(
            items=self,
            item_class=item_class,
            )

class PitchSegment(abjad.PitchSegment):
    r"""
    Pitch segment.

    ..  container:: example

        Initializes segment:

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = baca.pitch_segment(items=items)
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

    """

    ### CLASS VARIABLES ###

    ### PRIVATE METHODS ###

    def _to_selection(self):
        maker = abjad.NoteMaker()
        return maker(self, [(1, 4)])

    ### PUBLIC METHODS ###

    def bass_to_octave(self, n=4):
        r"""
        Octave-transposes segment to bass in octave ``n``.

        ..  container:: example

            >>> segment = baca.pitch_segment([-2, -1.5, 6, 7, -1.5, 7])
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.bass_to_octave(n=4)
            PitchSegment([10, 10.5, 18, 19, 10.5, 19])

            >>> segment = segment.bass_to_octave(n=4)
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        bf'1 * 1/8
                        bqf'1 * 1/8
                        fs''1 * 1/8
                        g''1 * 1/8
                        bqf'1 * 1/8
                        g''1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        Returns new segment.
        """
        from .pitchcommands import RegisterToOctaveCommand
        # TODO: remove reference to RegisterToOctaveCommand;
        #       implement as segment-only operation
        command = RegisterToOctaveCommand(
            anchor=abjad.Down,
            octave_number=n,
            )
        selection = self._to_selection()
        command([selection])
        segment = PitchSegment.from_selection(selection)
        return abjad.new(self, items=segment)

    def center_to_octave(self, n=4):
        r"""
        Octave-transposes segment to center in octave ``n``.

        ..  container:: example

            >>> segment = baca.pitch_segment([-2, -1.5, 6, 7, -1.5, 7])
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.center_to_octave(n=3)
            PitchSegment([-14, -13.5, -6, -5, -13.5, -5])

            >>> segment = segment.center_to_octave(n=3)
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        bqf,1 * 1/8
                        fs1 * 1/8
                        g1 * 1/8
                        bqf,1 * 1/8
                        g1 * 1/8
                    }
                >>

        Returns new segment.
        """
        from .pitchcommands import RegisterToOctaveCommand
        # TODO: remove reference to RegisterToOctaveCommand;
        #       implement as segment-only operation
        command = RegisterToOctaveCommand(
            anchor=abjad.Center,
            octave_number=n,
            )
        selection = self._to_selection()
        command([selection])
        segment = PitchSegment.from_selection(selection)
        return abjad.new(self, items=segment)

    def chord(self):
        r"""
        Changes segment to set.

        ..  container:: example

            >>> segment = baca.pitch_segment([-2, -1.5, 6, 7])

            >>> segment.chord()
            PitchSet([-2, -1.5, 6, 7])

            >>> abjad.show(segment.chord(), strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.chord().__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \new Staff
                    {
                        \new Voice
                        {
                            <fs' g'>1
                        }
                    }
                    \new Staff
                    {
                        \new Voice
                        {
                            <bf bqf>1
                        }
                    }
                >>

        Returns pitch set.
        """
        return PitchSet(
            items=self,
            item_class=self.item_class,
            )

    def soprano_to_octave(self, n=4):
        r"""
        Octave-transposes segment to soprano in octave ``n``.

        ..  container:: example

            >>> segment = baca.pitch_segment([-2, -1.5, 6, 7, -1.5, 7])
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.soprano_to_octave(n=3)
            PitchSegment([-14, -13.5, -6, -5, -13.5, -5])

            >>> segment = segment.soprano_to_octave(n=3)
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        bqf,1 * 1/8
                        fs1 * 1/8
                        g1 * 1/8
                        bqf,1 * 1/8
                        g1 * 1/8
                    }
                >>

        Returns new segment.
        """
        from .pitchcommands import RegisterToOctaveCommand
        # TODO: remove reference to RegisterToOctaveCommand;
        #       implement as segment-only operation
        command = RegisterToOctaveCommand(
            anchor=abjad.Up,
            octave_number=n,
            )
        selection = self._to_selection()
        command([selection])
        segment = PitchSegment.from_selection(selection)
        return abjad.new(self, items=segment)

    def space_down(
        self,
        bass=None,
        semitones=None,
        soprano=None,
        ):
        r"""
        Spaces pitch segment down.

        ..  container:: example

            >>> segment = baca.pitch_segment([12, 14, 21, 22])
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        c''1 * 1/8
                        d''1 * 1/8
                        a''1 * 1/8
                        bf''1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.space_down(bass=0)
            PitchSegment([14, 10, 9, 0])

            >>> segment = segment.space_down(bass=0)
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        d''1 * 1/8
                        bf'1 * 1/8
                        a'1 * 1/8
                        c'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        ..  container:: example

            With 2 in bass:

            >>> segment = baca.pitch_segment([12, 14, 21, 22])
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        c''1 * 1/8
                        d''1 * 1/8
                        a''1 * 1/8
                        bf''1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.space_down(bass=2)
            PitchSegment([12, 10, 9, 2])

            >>> segment = segment.space_down(bass=2)
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        c''1 * 1/8
                        bf'1 * 1/8
                        a'1 * 1/8
                        d'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        Returns new pitch segment.
        """
        specifier = ChordalSpacingSpecifier(
            bass=bass,
            direction=abjad.Down,
            minimum_semitones=semitones,
            soprano=soprano,
            )
        result = specifier([self])
        assert isinstance(result, CollectionList), repr(result)
        assert len(result) == 1, repr(result)
        segment = result[0]
        return segment

    def space_up(
        self,
        bass=None,
        semitones=None,
        soprano=None,
        ):
        r"""
        Spaces pitch segment up.

        ..  container:: example

            >>> segment = baca.pitch_segment([12, 14, 21, 22])
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        c''1 * 1/8
                        d''1 * 1/8
                        a''1 * 1/8
                        bf''1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.space_up(bass=0)
            PitchSegment([0, 2, 9, 10])

            >>> segment = segment.space_up(bass=0)
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        c'1 * 1/8
                        d'1 * 1/8
                        a'1 * 1/8
                        bf'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        ..  container:: example

            With 2 in bass:

            >>> segment = baca.pitch_segment([12, 14, 21, 22])
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        c''1 * 1/8
                        d''1 * 1/8
                        a''1 * 1/8
                        bf''1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.space_up(bass=2)
            PitchSegment([2, 9, 10, 12])

            >>> segment = segment.space_up(bass=2)
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        d'1 * 1/8
                        a'1 * 1/8
                        bf'1 * 1/8
                        c''1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        Returns new pitch segment.
        """
        specifier = ChordalSpacingSpecifier(
            bass=bass,
            direction=abjad.Up,
            minimum_semitones=semitones,
            soprano=soprano,
            )
        result = specifier([self])
        assert isinstance(result, CollectionList), repr(result)
        assert len(result) == 1, repr(result)
        segment = result[0]
        return segment

    def split(self, pitch=0):
        r"""
        Splits segment at ``pitch``.

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> segment = baca.pitch_segment(items=items)
            >>> abjad.show(segment, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> upper, lower = segment.split(pitch=0)

            >>> upper
            PitchSegment([6, 7, 7])

            >>> abjad.show(upper, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = upper.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        fs'1 * 1/8
                        g'1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> lower
            PitchSegment([-2, -1.5, -1.5])

            >>> abjad.show(lower, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = lower.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \context Staff = "Treble_Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                    \context Staff = "Bass_Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        bqf1 * 1/8
                    }
                >>

        Returns upper, lower segments.
        """
        upper, lower = [], []
        for pitch_ in self:
            if pitch_ < pitch:
                lower.append(pitch_)
            else:
                upper.append(pitch_)
        upper = abjad.new(self, items=upper)
        lower = abjad.new(self, items=lower)
        return upper, lower

class PitchSet(abjad.PitchSet):
    r"""
    Pitch set.

    ..  container:: example

        Initializes set:

        ..  container:: example

            >>> setting = baca.pitch_set([-2, -1.5, 6, 7, -1.5, 7])
            >>> abjad.show(setting, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = setting.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new PianoStaff
                    <<
                        \new Staff
                        {
                            \new Voice
                            {
                                <fs' g'>1
                            }
                        }
                        \new Staff
                        {
                            \new Voice
                            {
                                <bf bqf>1
                            }
                        }
                    >>
                >>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when segment equals ``argument``.

        ..  container:: example

            Works with Abjad pitch sets:

            >>> set_1 = abjad.PitchSet([0, 1, 2, 3])
            >>> set_2 = baca.PitchSet([0, 1, 2, 3])

            >>> set_1 == set_2
            True

            >>> set_2 == set_1
            True

        """
        if (not issubclass(type(argument), type(self)) and
            not issubclass(type(self), type(argument))):
            return False
        return self._collection == argument._collection

    ### PUBLIC METHODS ###

    def space_down(
        self,
        bass=None,
        semitones=None,
        soprano=None,
        ):
        r"""
        Spaces pitch set down.

        ..  container:: example

            >>> setting = baca.pitch_set([12, 14, 21, 22])
            >>> abjad.show(setting, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = setting.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \new Staff
                    {
                        \new Voice
                        {
                            <c'' d'' a'' bf''>1
                        }
                    }
                    \new Staff
                    {
                        \new Voice
                        {
                            s1
                        }
                    }
                >>

            >>> setting.space_down(bass=0)
            PitchSet([0, 9, 10, 14])

            >>> setting = setting.space_down(bass=0)
            >>> abjad.show(setting, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = setting.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \new Staff
                    {
                        \new Voice
                        {
                            <c' a' bf' d''>1
                        }
                    }
                    \new Staff
                    {
                        \new Voice
                        {
                            s1
                        }
                    }
                >>

        ..  container:: example

            With 2 in bass:

            >>> setting = baca.pitch_set([12, 14, 21, 22])
            >>> abjad.show(setting, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = setting.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \new Staff
                    {
                        \new Voice
                        {
                            <c'' d'' a'' bf''>1
                        }
                    }
                    \new Staff
                    {
                        \new Voice
                        {
                            s1
                        }
                    }
                >>

            >>> setting.space_down(bass=2)
            PitchSet([2, 9, 10, 12])

            >>> setting = setting.space_down(bass=2)
            >>> abjad.show(setting, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = setting.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \new Staff
                    {
                        \new Voice
                        {
                            <d' a' bf' c''>1
                        }
                    }
                    \new Staff
                    {
                        \new Voice
                        {
                            s1
                        }
                    }
                >>

        Returns new pitch set.
        """
        specifier = ChordalSpacingSpecifier(
            bass=bass,
            direction=abjad.Down,
            minimum_semitones=semitones,
            soprano=soprano,
            )
        result = specifier([self])
        assert isinstance(result, CollectionList), repr(result)
        assert len(result) == 1, repr(result)
        segment = result[0]
        return segment

    def space_up(
        self,
        bass=None,
        semitones=None,
        soprano=None,
        ):
        r"""
        Spaces pitch set up.

        ..  container:: example

            >>> setting = baca.pitch_set([12, 14, 21, 22])
            >>> abjad.show(setting, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = setting.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \new Staff
                    {
                        \new Voice
                        {
                            <c'' d'' a'' bf''>1
                        }
                    }
                    \new Staff
                    {
                        \new Voice
                        {
                            s1
                        }
                    }
                >>

            >>> setting.space_up(bass=0)
            PitchSet([0, 2, 9, 10])

            >>> setting = setting.space_up(bass=0)
            >>> abjad.show(setting, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = setting.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \new Staff
                    {
                        \new Voice
                        {
                            <c' d' a' bf'>1
                        }
                    }
                    \new Staff
                    {
                        \new Voice
                        {
                            s1
                        }
                    }
                >>

        ..  container:: example

            With 2 in bass:

            >>> setting = baca.pitch_set([12, 14, 21, 22])
            >>> abjad.show(setting, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = setting.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \new Staff
                    {
                        \new Voice
                        {
                            <c'' d'' a'' bf''>1
                        }
                    }
                    \new Staff
                    {
                        \new Voice
                        {
                            s1
                        }
                    }
                >>

            >>> setting.space_up(bass=2)
            PitchSet([2, 9, 10, 12])

            >>> setting = setting.space_up(bass=2)
            >>> abjad.show(setting, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = setting.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup], strict=89)
                \new PianoStaff
                <<
                    \new Staff
                    {
                        \new Voice
                        {
                            <d' a' bf' c''>1
                        }
                    }
                    \new Staff
                    {
                        \new Voice
                        {
                            s1
                        }
                    }
                >>

        Returns new pitch segment.
        """
        specifier = ChordalSpacingSpecifier(
            bass=bass,
            direction=abjad.Up,
            minimum_semitones=semitones,
            soprano=soprano,
            )
        result = specifier([self])
        assert isinstance(result, CollectionList), repr(result)
        assert len(result) == 1, repr(result)
        segment = result[0]
        return segment

    def to_pitch_classes(self):
        r"""
        Makes pitch-class set.

        ..  container:: example

            >>> setting = baca.pitch_set([-2, -1.5, 6, 19, -1.5, 21])
            >>> setting
            PitchSet([-2, -1.5, 6, 19, 21])

            >>> setting.to_pitch_classes()
            PitchClassSet([6, 7, 9, 10, 10.5])

        Returns new pitch-class set.
        """
        if self.item_class is abjad.NumberedPitch:
            item_class = abjad.NumberedPitchClass
        elif self.item_class is abjad.NamedPitch:
            item_class = abjad.NamedPitchClass
        else:
            raise TypeError(self.item_class)
        return PitchClassSet(
            items=self,
            item_class=item_class,
            )

class PitchTree(classes.Tree):
    r"""
    Pitch tree.

    ..  container:: example

        Initializes numbered pitch tree:

        >>> items = [[16, 18, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
        >>> tree = baca.PitchTree(items=items)
        >>> abjad.show(tree, strict=89) # doctest: +SKIP

        ..  docs::

            >>> lilypond_file = tree.__illustrate__()
            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            \with
            {
                \override BarLine.transparent = ##t
                \override BarNumber.stencil = ##f
                \override Beam.stencil = ##f
                \override Flag.stencil = ##f
                \override HorizontalBracket.staff-padding = #4
                \override SpacingSpanner.strict-grace-spacing = ##t
                \override SpacingSpanner.strict-note-spacing = ##t
                \override SpacingSpanner.uniform-stretching = ##t
                \override Stem.stencil = ##f
                \override TextScript.X-extent = ##f
                \override TextScript.staff-padding = #2
                \override TimeSignature.stencil = ##f
                proportionalNotationDuration = #(ly:make-moment 1 16)
            }
            <<
                \new Staff
                {
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                    }
                    {
                        \time 1/8
                        e''8
                        ^ \markup { 0 }
                        \startGroup
                        fs''8
                        bf'8
                        \stopGroup
                        s8
                        a'8
                        ^ \markup { 1 }
                        \startGroup
                        g'8
                        af'8
                        b'8
                        a'8
                        cs'8
                        \stopGroup
                        s8
                        c'8
                        ^ \markup { 2 }
                        \startGroup
                        d'8
                        ef'8
                        f'8
                        \stopGroup
                        s8
                        \bar "|."                                                                    %! SCORE_1
                        \override Score.BarLine.transparent = ##f
                    }
                }
            >>

    ..  container:: example

        Initializes named pitch tree:

        >>> items = [
        ...     ['E5', 'F#5', 'Bb4'],
        ...     ['A4', 'G4', 'Ab4', 'B4', 'A4', 'C#4'],
        ...     ['C4', 'D4', 'Eb4', 'F4'],
        ...     ]
        >>> tree = baca.PitchTree(
        ...     items=items,
        ...     item_class=abjad.NamedPitch,
        ...     )
        >>> abjad.show(tree, strict=89) # doctest: +SKIP

        ..  docs::

            >>> lilypond_file = tree.__illustrate__()
            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            \with
            {
                \override BarLine.transparent = ##t
                \override BarNumber.stencil = ##f
                \override Beam.stencil = ##f
                \override Flag.stencil = ##f
                \override HorizontalBracket.staff-padding = #4
                \override SpacingSpanner.strict-grace-spacing = ##t
                \override SpacingSpanner.strict-note-spacing = ##t
                \override SpacingSpanner.uniform-stretching = ##t
                \override Stem.stencil = ##f
                \override TextScript.X-extent = ##f
                \override TextScript.staff-padding = #2
                \override TimeSignature.stencil = ##f
                proportionalNotationDuration = #(ly:make-moment 1 16)
            }
            <<
                \new Staff
                {
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                    }
                    {
                        \time 1/8
                        e''8
                        ^ \markup { 0 }
                        \startGroup
                        fs''8
                        bf'8
                        \stopGroup
                        s8
                        a'8
                        ^ \markup { 1 }
                        \startGroup
                        g'8
                        af'8
                        b'8
                        a'8
                        cs'8
                        \stopGroup
                        s8
                        c'8
                        ^ \markup { 2 }
                        \startGroup
                        d'8
                        ef'8
                        f'8
                        \stopGroup
                        s8
                        \bar "|."                                                                    %! SCORE_1
                        \override Score.BarLine.transparent = ##f
                    }
                }
            >>

    ..  container:: example

        Initializes numbered pitch-class tree:

        >>> items = [[16, 18, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
        >>> tree = baca.PitchTree(
        ...     items=items,
        ...     item_class=abjad.NumberedPitchClass,
        ...     )
        >>> abjad.show(tree, strict=89) # doctest: +SKIP

        ..  docs::

            >>> lilypond_file = tree.__illustrate__()
            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            \with
            {
                \override BarLine.transparent = ##t
                \override BarNumber.stencil = ##f
                \override Beam.stencil = ##f
                \override Flag.stencil = ##f
                \override HorizontalBracket.staff-padding = #4
                \override SpacingSpanner.strict-grace-spacing = ##t
                \override SpacingSpanner.strict-note-spacing = ##t
                \override SpacingSpanner.uniform-stretching = ##t
                \override Stem.stencil = ##f
                \override TextScript.X-extent = ##f
                \override TextScript.staff-padding = #2
                \override TimeSignature.stencil = ##f
                proportionalNotationDuration = #(ly:make-moment 1 16)
            }
            <<
                \new Staff
                {
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                    }
                    {
                        \time 1/8
                        e'8
                        ^ \markup { 0 }
                        \startGroup
                        fs'8
                        bf'8
                        \stopGroup
                        s8
                        a'8
                        ^ \markup { 1 }
                        \startGroup
                        g'8
                        af'8
                        b'8
                        a'8
                        cs'8
                        \stopGroup
                        s8
                        c'8
                        ^ \markup { 2 }
                        \startGroup
                        d'8
                        ef'8
                        f'8
                        \stopGroup
                        s8
                        \bar "|."                                                                    %! SCORE_1
                        \override Score.BarLine.transparent = ##f
                    }
                }
            >>

    ..  container:: example

        Initializes named pitch-class tree:

        >>> items = [
        ...     ['E5', 'F#5', 'Bb4'],
        ...     ['A4', 'G4', 'Ab4', 'B4', 'A4', 'C#4'],
        ...     ['C4', 'D4', 'Eb4', 'F4'],
        ...     ]
        >>> tree = baca.PitchTree(
        ...     items=items,
        ...     item_class=abjad.NamedPitchClass,
        ...     )
        >>> abjad.show(tree, strict=89) # doctest: +SKIP

        ..  docs::

            >>> lilypond_file = tree.__illustrate__()
            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            \with
            {
                \override BarLine.transparent = ##t
                \override BarNumber.stencil = ##f
                \override Beam.stencil = ##f
                \override Flag.stencil = ##f
                \override HorizontalBracket.staff-padding = #4
                \override SpacingSpanner.strict-grace-spacing = ##t
                \override SpacingSpanner.strict-note-spacing = ##t
                \override SpacingSpanner.uniform-stretching = ##t
                \override Stem.stencil = ##f
                \override TextScript.X-extent = ##f
                \override TextScript.staff-padding = #2
                \override TimeSignature.stencil = ##f
                proportionalNotationDuration = #(ly:make-moment 1 16)
            }
            <<
                \new Staff
                {
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                    }
                    {
                        \time 1/8
                        e'8
                        ^ \markup { 0 }
                        \startGroup
                        fs'8
                        bf'8
                        \stopGroup
                        s8
                        a'8
                        ^ \markup { 1 }
                        \startGroup
                        g'8
                        af'8
                        b'8
                        a'8
                        cs'8
                        \stopGroup
                        s8
                        c'8
                        ^ \markup { 2 }
                        \startGroup
                        d'8
                        ef'8
                        f'8
                        \stopGroup
                        s8
                        \bar "|."                                                                    %! SCORE_1
                        \override Score.BarLine.transparent = ##f
                    }
                }
            >>

    ..  container:: example

        Initializes from other trees:

        >>> items = [
        ...     baca.PitchTree([4, 6, 10]),
        ...     baca.PitchTree([9, 7, 8, 11, 9, 1]),
        ...     baca.PitchTree([0, 2, 3, 5]),
        ...     ]
        >>> tree = baca.PitchTree(items=items)
        >>> lilypond_file = tree.__illustrate__(
        ...     cell_indices=False,
        ...     )
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            \with
            {
                \override BarLine.transparent = ##t
                \override BarNumber.stencil = ##f
                \override Beam.stencil = ##f
                \override Flag.stencil = ##f
                \override HorizontalBracket.staff-padding = #4
                \override SpacingSpanner.strict-grace-spacing = ##t
                \override SpacingSpanner.strict-note-spacing = ##t
                \override SpacingSpanner.uniform-stretching = ##t
                \override Stem.stencil = ##f
                \override TextScript.X-extent = ##f
                \override TextScript.staff-padding = #2
                \override TimeSignature.stencil = ##f
                proportionalNotationDuration = #(ly:make-moment 1 16)
            }
            <<
                \new Staff
                {
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                    }
                    {
                        \time 1/8
                        e'8
                        \startGroup
                        fs'8
                        bf'8
                        \stopGroup
                        s8
                        a'8
                        \startGroup
                        g'8
                        af'8
                        b'8
                        a'8
                        cs'8
                        \stopGroup
                        s8
                        c'8
                        \startGroup
                        d'8
                        ef'8
                        f'8
                        \stopGroup
                        s8
                        \bar "|."                                                                    %! SCORE_1
                        \override Score.BarLine.transparent = ##f
                    }
                }
            >>

    ..  container:: example

        Initializes from pitch segments:

        >>> items = [
        ...     abjad.PitchClassSegment([4, 6, 10]),
        ...     abjad.PitchClassSegment([9, 7, 8, 11, 9, 1]),
        ...     abjad.PitchClassSegment([0, 2, 3, 5]),
        ...     ]
        >>> items = [segment.rotate(n=1) for segment in items]
        >>> tree = baca.PitchTree(items=items)
        >>> abjad.show(tree, cell_indices=False, strict=89) # doctest: +SKIP

        ..  docs::

            >>> lilypond_file = tree.__illustrate__(cell_indices=False)
            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            \with
            {
                \override BarLine.transparent = ##t
                \override BarNumber.stencil = ##f
                \override Beam.stencil = ##f
                \override Flag.stencil = ##f
                \override HorizontalBracket.staff-padding = #4
                \override SpacingSpanner.strict-grace-spacing = ##t
                \override SpacingSpanner.strict-note-spacing = ##t
                \override SpacingSpanner.uniform-stretching = ##t
                \override Stem.stencil = ##f
                \override TextScript.X-extent = ##f
                \override TextScript.staff-padding = #2
                \override TimeSignature.stencil = ##f
                proportionalNotationDuration = #(ly:make-moment 1 16)
            }
            <<
                \new Staff
                {
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                    }
                    {
                        \time 1/8
                        bf'8
                        \startGroup
                        e'8
                        fs'8
                        \stopGroup
                        s8
                        cs'8
                        \startGroup
                        a'8
                        g'8
                        af'8
                        b'8
                        a'8
                        \stopGroup
                        s8
                        f'8
                        \startGroup
                        c'8
                        d'8
                        ef'8
                        \stopGroup
                        s8
                        \bar "|."                                                                    %! SCORE_1
                        \override Score.BarLine.transparent = ##f
                    }
                }
            >>

    ..  container:: example

        Initializes nested tree:

        >>> segment_1 = abjad.PitchClassSegment([4, 6, 10])
        >>> segment_2 = abjad.PitchClassSegment([9, 7, 8, 11, 9, 1])
        >>> segment_3 = abjad.PitchClassSegment([0, 2, 3, 5])
        >>> segment_1 = segment_1.transpose(n=1)
        >>> segment_2 = segment_2.transpose(n=1)
        >>> segment_3 = segment_3.transpose(n=1)
        >>> items = [[segment_1, segment_2], segment_3]
        >>> tree = baca.PitchTree(items=items)
        >>> graph(tree) # doctest: +SKIP

        ..  docs::

            >>> graph_ = tree.__graph__() # doctest: +SKIP
            >>> abjad.f(graph_, strict=89) # doctest: +SKIP
            digraph G {
                graph [bgcolor=transparent,
                    truecolor=true];
                node_0 [label="",
                    shape=circle];
                node_1 [label="",
                    shape=circle];
                node_2 [label="",
                    shape=circle];
                node_3 [label="5",
                    shape=box];
                node_4 [label="7",
                    shape=box];
                node_5 [label="11",
                    shape=box];
                node_6 [label="",
                    shape=circle];
                node_7 [label="10",
                    shape=box];
                node_8 [label="8",
                    shape=box];
                node_9 [label="9",
                    shape=box];
                node_10 [label="0",
                    shape=box];
                node_11 [label="10",
                    shape=box];
                node_12 [label="2",
                    shape=box];
                node_13 [label="",
                    shape=circle];
                node_14 [label="1",
                    shape=box];
                node_15 [label="3",
                    shape=box];
                node_16 [label="4",
                    shape=box];
                node_17 [label="6",
                    shape=box];
                node_0 -> node_1;
                node_0 -> node_13;
                node_1 -> node_2;
                node_1 -> node_6;
                node_2 -> node_3;
                node_2 -> node_4;
                node_2 -> node_5;
                node_6 -> node_7;
                node_6 -> node_8;
                node_6 -> node_9;
                node_6 -> node_10;
                node_6 -> node_11;
                node_6 -> node_12;
                node_13 -> node_14;
                node_13 -> node_15;
                node_13 -> node_16;
                node_13 -> node_17;
            }

        >>> abjad.show(tree, cell_indices=False, strict=89) # doctest: +SKIP

        ..  docs::

            >>> lilypond_file = tree.__illustrate__(cell_indices=False)
            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            \with
            {
                \override BarLine.transparent = ##t
                \override BarNumber.stencil = ##f
                \override Beam.stencil = ##f
                \override Flag.stencil = ##f
                \override HorizontalBracket.staff-padding = #4
                \override SpacingSpanner.strict-grace-spacing = ##t
                \override SpacingSpanner.strict-note-spacing = ##t
                \override SpacingSpanner.uniform-stretching = ##t
                \override Stem.stencil = ##f
                \override TextScript.X-extent = ##f
                \override TextScript.staff-padding = #2
                \override TimeSignature.stencil = ##f
                proportionalNotationDuration = #(ly:make-moment 1 16)
            }
            <<
                \new Staff
                {
                    \new Voice
                    \with
                    {
                        \consists Horizontal_bracket_engraver
                    }
                    {
                        \time 1/8
                        f'8
                        \startGroup
                        \startGroup
                        g'8
                        b'8
                        \stopGroup
                        s8
                        bf'8
                        \startGroup
                        af'8
                        a'8
                        c'8
                        bf'8
                        d'8
                        \stopGroup
                        \stopGroup
                        s8
                        cs'8
                        \startGroup
                        ef'8
                        e'8
                        fs'8
                        \stopGroup
                        s8
                        \bar "|."                                                                    %! SCORE_1
                        \override Score.BarLine.transparent = ##f
                    }
                }
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        *,
        item_class=None,
        ):
        item_class = item_class or abjad.NumberedPitch
        classes.Tree.__init__(
            self,
            items=items,
            item_class=item_class,
            )

    ### SPECIAL METHODS ###

#    def __graph__(self, **keywords):
#        r"""
#        Graphs pitch tree.
#
#        ..  container:: example
#
#            Graphs numbered pitch tree:
#
#            >>> items = [[4, 6, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
#            >>> tree = PitchTree(items=items)
#
#            >>> graph(tree) # doctest: +SKIP
#
#            ..  docs::
#
#                >>> tree_graph = tree.__graph__()
#                >>> abjad.f(tree_graph, strict=89)
#                digraph G {
#                    graph [bgcolor=transparent,
#                        truecolor=true];
#                    node_0 [label="",
#                        shape=circle];
#                    node_1 [label="",
#                        shape=circle];
#                    node_2 [label="4",
#                        shape=box];
#                    node_3 [label="6",
#                        shape=box];
#                    node_4 [label="10",
#                        shape=box];
#                    node_5 [label="",
#                        shape=circle];
#                    node_6 [label="9",
#                        shape=box];
#                    node_7 [label="7",
#                        shape=box];
#                    node_8 [label="8",
#                        shape=box];
#                    node_9 [label="11",
#                        shape=box];
#                    node_10 [label="9",
#                        shape=box];
#                    node_11 [label="1",
#                        shape=box];
#                    node_12 [label="",
#                        shape=circle];
#                    node_13 [label="0",
#                        shape=box];
#                    node_14 [label="2",
#                        shape=box];
#                    node_15 [label="3",
#                        shape=box];
#                    node_16 [label="5",
#                        shape=box];
#                    node_0 -> node_1;
#                    node_0 -> node_5;
#                    node_0 -> node_12;
#                    node_1 -> node_2;
#                    node_1 -> node_3;
#                    node_1 -> node_4;
#                    node_5 -> node_6;
#                    node_5 -> node_7;
#                    node_5 -> node_8;
#                    node_5 -> node_9;
#                    node_5 -> node_10;
#                    node_5 -> node_11;
#                    node_12 -> node_13;
#                    node_12 -> node_14;
#                    node_12 -> node_15;
#                    node_12 -> node_16;
#                }
#
#        ..  container:: example
#
#            Graphs named pitch tree:
#
#            >>> items = [[4, 6, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
#            >>> tree = PitchTree(
#            ...     items=items,
#            ...     item_class=abjad.NamedPitch,
#            ...     )
#
#            >>> graph(tree) # doctest: +SKIP
#
#            ..  docs::
#
#                >>> tree_graph = tree.__graph__()
#                >>> abjad.f(tree_graph, strict=89)
#                digraph G {
#                    graph [bgcolor=transparent,
#                        truecolor=true];
#                    node_0 [label="",
#                        shape=circle];
#                    node_1 [label="",
#                        shape=circle];
#                    node_2 [label="e'",
#                        shape=box];
#                    node_3 [label="fs'",
#                        shape=box];
#                    node_4 [label="bf'",
#                        shape=box];
#                    node_5 [label="",
#                        shape=circle];
#                    node_6 [label="a'",
#                        shape=box];
#                    node_7 [label="g'",
#                        shape=box];
#                    node_8 [label="af'",
#                        shape=box];
#                    node_9 [label="b'",
#                        shape=box];
#                    node_10 [label="a'",
#                        shape=box];
#                    node_11 [label="cs'",
#                        shape=box];
#                    node_12 [label="",
#                        shape=circle];
#                    node_13 [label="c'",
#                        shape=box];
#                    node_14 [label="d'",
#                        shape=box];
#                    node_15 [label="ef'",
#                        shape=box];
#                    node_16 [label="f'",
#                        shape=box];
#                    node_0 -> node_1;
#                    node_0 -> node_5;
#                    node_0 -> node_12;
#                    node_1 -> node_2;
#                    node_1 -> node_3;
#                    node_1 -> node_4;
#                    node_5 -> node_6;
#                    node_5 -> node_7;
#                    node_5 -> node_8;
#                    node_5 -> node_9;
#                    node_5 -> node_10;
#                    node_5 -> node_11;
#                    node_12 -> node_13;
#                    node_12 -> node_14;
#                    node_12 -> node_15;
#                    node_12 -> node_16;
#                }
#
#        Returns Graphviz graph.
#        """
#        return super().__graph__(**keywords)

    def __illustrate__(
        self,
        after_cell_spacing=True,
        brackets=True,
        cell_indices=True,
        color_repeats=True,
        global_staff_size=16,
        markup_direction=abjad.Up,
        set_classes=False,
        **keywords
        ):
        r"""
        Illustrates pitch tree.

        ..  container:: example

            Illustrate tree:

            >>> items = [[4, 6, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
            >>> tree = baca.PitchTree(items=items)
            >>> lilypond_file = tree.__illustrate__()
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                }
                <<
                    \new Staff
                    {
                        \new Voice
                        \with
                        {
                            \consists Horizontal_bracket_engraver
                        }
                        {
                            \time 1/8
                            e'8
                            ^ \markup { 0 }
                            \startGroup
                            fs'8
                            bf'8
                            \stopGroup
                            s8
                            a'8
                            ^ \markup { 1 }
                            \startGroup
                            g'8
                            af'8
                            b'8
                            a'8
                            cs'8
                            \stopGroup
                            s8
                            c'8
                            ^ \markup { 2 }
                            \startGroup
                            d'8
                            ef'8
                            f'8
                            \stopGroup
                            s8
                            \bar "|."                                                                    %! SCORE_1
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Illustrates tree with set-classes:

            >>> items = [[4, 6, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
            >>> tree = baca.PitchTree(items=items)
            >>> lilypond_file = tree.__illustrate__(
            ...     cell_indices=abjad.Down,
            ...     set_classes=True,
            ...     )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                }
                <<
                    \new Staff
                    {
                        \new Voice
                        \with
                        {
                            \consists Horizontal_bracket_engraver
                        }
                        {
                            \time 1/8
                            e'8
                            ^ \markup {
                                \small
                                    \line
                                        {
                                            "SC(3-9){0, 2, 6}"
                                        }
                                }
                            - \tweak staff-padding #7
                            _ \markup { 0 }
                            \startGroup
                            fs'8
                            bf'8
                            \stopGroup
                            s8
                            a'8
                            ^ \markup {
                                \small
                                    \line
                                        {
                                            "SC(5-6){0, 1, 2, 4, 6}"
                                        }
                                }
                            - \tweak staff-padding #7
                            _ \markup { 1 }
                            \startGroup
                            g'8
                            af'8
                            b'8
                            a'8
                            cs'8
                            \stopGroup
                            s8
                            c'8
                            ^ \markup {
                                \small
                                    \line
                                        {
                                            "SC(4-19){0, 2, 3, 5}"
                                        }
                                }
                            - \tweak staff-padding #7
                            _ \markup { 2 }
                            \startGroup
                            d'8
                            ef'8
                            f'8
                            \stopGroup
                            s8
                            \bar "|."                                                                    %! SCORE_1
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Illustrates nested tree:

            >>> segment_1 = abjad.PitchClassSegment([4, 6, 10])
            >>> segment_2 = abjad.PitchClassSegment([9, 7, 8, 11, 9, 1])
            >>> segment_3 = abjad.PitchClassSegment([0, 2, 3, 5])
            >>> segment_1 = segment_1.transpose(n=1)
            >>> segment_2 = segment_2.transpose(n=1)
            >>> segment_3 = segment_3.transpose(n=1)
            >>> items = [[segment_1, segment_2], segment_3]
            >>> tree = baca.PitchTree(items=items)
            >>> lilypond_file = tree.__illustrate__(
            ...     cell_indices=abjad.Down,
            ...     )
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                }
                <<
                    \new Staff
                    {
                        \new Voice
                        \with
                        {
                            \consists Horizontal_bracket_engraver
                        }
                        {
                            \time 1/8
                            f'8
                            - \tweak staff-padding #7
                            _ \markup { 0 }
                            \startGroup
                            \startGroup
                            g'8
                            b'8
                            \stopGroup
                            s8
                            bf'8
                            - \tweak staff-padding #7
                            _ \markup { 1 }
                            \startGroup
                            af'8
                            a'8
                            c'8
                            bf'8
                            d'8
                            \stopGroup
                            \stopGroup
                            s8
                            cs'8
                            - \tweak staff-padding #7
                            _ \markup { 2 }
                            \startGroup
                            ef'8
                            e'8
                            fs'8
                            \stopGroup
                            s8
                            \bar "|."                                                                    %! SCORE_1
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        Returns LilyPond file.
        """
        assert cell_indices in (True, False, abjad.Up, abjad.Down), repr(cell_indices)
        voice = abjad.Voice()
        voice.consists_commands.append('Horizontal_bracket_engraver')
        staff = abjad.Staff([voice])
        score = abjad.Score([staff])
        leaf_list_stack = []
        leaf_groups = self._populate_voice(
            leaf_list_stack,
            self,
            voice,
            after_cell_spacing=after_cell_spacing,
            brackets=brackets,
            markup_direction=markup_direction,
            )
        assert leaf_list_stack == [], repr(leaf_list_stack)
        first_leaf = abjad.inspect(voice).leaf(n=0)
        abjad.attach(abjad.TimeSignature((1, 8)), first_leaf)
        self._color_repeats(color_repeats, voice)
        self._attach_cell_indices(cell_indices, leaf_groups)
        self._label_set_classes(set_classes, leaf_groups)
        score.add_final_bar_line()
        abjad.override(score).bar_line.transparent = True
        abjad.override(score).bar_number.stencil = False
        abjad.override(score).beam.stencil = False
        abjad.override(score).flag.stencil = False
        abjad.override(score).horizontal_bracket.staff_padding = 4
        abjad.override(score).stem.stencil = False
        abjad.override(score).text_script.staff_padding = 2
        abjad.override(score).time_signature.stencil = False
        last_leaf = abjad.inspect(score).leaf(-1)
        string = r'\override Score.BarLine.transparent = ##f'
        literal = abjad.LilyPondLiteral(string, 'after')
        abjad.attach(literal, last_leaf)
        moment = abjad.SchemeMoment((1, 16))
        abjad.setting(score).proportional_notation_duration = moment
        lilypond_file = abjad.LilyPondFile.new(
            date_time_token=False,
            global_staff_size=global_staff_size,
            includes=['/Users/trevorbaca/baca/lilypond/baca.ily'],
            music=score,
            )
        abjad.override(score).spacing_spanner.strict_grace_spacing = True
        abjad.override(score).spacing_spanner.strict_note_spacing = True
        abjad.override(score).spacing_spanner.uniform_stretching = True
        abjad.override(score).text_script.X_extent = False
        if 'title' in keywords:
            title = keywords.get('title')
            if not isinstance(title, abjad.Markup):
                title = abjad.Markup(title)
            lilypond_file.header_block.title = title
        if 'subtitle' in keywords:
            markup = abjad.Markup(keywords.get('subtitle'))
            lilypond_file.header_block.subtitle = markup
        string = r'\accidentalStyle dodecaphonic'
        literal = abjad.LilyPondLiteral(string)
        lilypond_file.layout_block.items.append(literal)
        lilypond_file.layout_block.indent = 0
        lilypond_file.layout_block.line_width = 287.5
        lilypond_file.layout_block.ragged_right = True
        string = 'markup-system-spacing.padding = 8'
        literal = abjad.LilyPondLiteral(string)
        lilypond_file.paper_block.items.append(literal)
        string = 'system-system-spacing.padding = 10'
        literal = abjad.LilyPondLiteral(string)
        lilypond_file.paper_block.items.append(literal)
        string = 'top-markup-spacing.padding = 4'
        literal = abjad.LilyPondLiteral(string)
        lilypond_file.paper_block.items.append(literal)
        return lilypond_file

    ### PRIVATE METHODS ###

    def _attach_cell_indices(self, cell_indices, leaf_groups):
        if not cell_indices:
            return
        leaf_groups.sort(
            key=lambda _: abjad.inspect(_[1][0]).timespan().start_offset
            )
        if cell_indices is True:
            direction = abjad.Up
        else:
            direction = cell_indices
        cell_index = 0
        for leaf_group in leaf_groups:
            negative_level = leaf_group[0]
            if negative_level != -2:
                continue
            markup = abjad.Markup(cell_index, direction=direction)
            if direction == abjad.Down:
                abjad.tweak(markup).staff_padding = 7
            first_leaf = leaf_group[1][0]
            abjad.attach(markup, first_leaf)
            cell_index += 1

    def _color_repeats(self, color_repeats, voice):
        if not color_repeats:
            return
        leaves = abjad.iterate(voice).components(prototype=abjad.Note)
        pairs = abjad.Sequence(leaves).nwise(n=2, wrapped=True)
        current_color = 'red'
        for left, right in pairs:
            if not left.written_pitch == right.written_pitch:
                continue
            abjad.label(left).color_leaves(current_color)
            abjad.label(right).color_leaves(current_color)
            if current_color == 'red':
                current_color = 'blue'
            else:
                current_color = 'red'

    def _label_set_classes(
        self,
        set_classes,
        leaf_groups,
        ):
        if not set_classes:
            return
        for leaf_group in leaf_groups:
            leaves = leaf_group[1]
            pitch_class_set = PitchClassSet.from_selection(leaves)
            if not pitch_class_set:
                continue
            set_class = abjad.SetClass.from_pitch_class_set(
                pitch_class_set,
                lex_rank=True,
                transposition_only=True,
                )
            string = str(set_class)
            markup = abjad.Markup.from_literal(string)
            label = abjad.Markup.line([markup], direction=abjad.Up)
            if label is not None:
                label = label.small()
                first_leaf = leaves[0]
                abjad.attach(label, first_leaf)

    def _populate_voice(
        self,
        leaf_list_stack,
        node,
        voice,
        after_cell_spacing=False,
        brackets=True,
        markup_direction=None,
        ):
        leaf_groups = []
        if len(node):
            if node._get_level():
                leaf_list_stack.append([])
            for child_node in node:
                leaf_groups_ = self._populate_voice(
                    leaf_list_stack,
                    child_node,
                    voice,
                    after_cell_spacing=after_cell_spacing,
                    brackets=brackets,
                    markup_direction=markup_direction,
                    )
                leaf_groups.extend(leaf_groups_)
            if node._get_level():
                first_note = leaf_list_stack[-1][0]
                last_note = leaf_list_stack[-1][-1]
                leaves_with_skips = []
                leaf = first_note
                while leaf is not last_note:
                    leaves_with_skips.append(leaf)
                    leaf = abjad.inspect(leaf).leaf(n=1)
                leaves_with_skips.append(leaf)
                negative_level = node._get_level(negative=True)
                #spanner = PitchTreeSpanner(level=negative_level)
                #leaves_with_skips = abjad.select(leaves_with_skips)
                #abjad.attach(spanner, leaves_with_skips)
                if brackets:
                    abjad.horizontal_bracket(leaves_with_skips)
                selection = abjad.select(leaves_with_skips)
                leaf_group = (negative_level, selection)
                leaf_groups.append(leaf_group)
                leaf_list_stack.pop()
        else:
            assert node._payload is not None
            note = abjad.Note(
                node._payload,
                abjad.Duration(1, 8),
                )
            if node._is_leftmost_leaf():
                for parent in node._get_parentage():
                    if parent._expression is not None:
                        node_markup = parent._expression.get_markup()
                        if node_markup is not None:
                            node_markup = abjad.new(
                                node_markup,
                                direction=markup_direction,
                                )
                            abjad.attach(node_markup, note)
            voice.append(note)
            if node._is_rightmost_leaf():
                if after_cell_spacing:
                    skip = abjad.Skip((1, 8))
                    voice.append(skip)
            for leaf_list in leaf_list_stack:
                leaf_list.append(note)
        return leaf_groups

    ### PUBLIC METHODS ###

    def has_repeats(self):
        r"""
        Is true when tree has repeats.

        ..  container:: example

            Has repeats:

                >>> items = [[4, 6, 10], [9, 7, 8, 11, 9, 1], [1, 2, 2, 4]]
                >>> tree = baca.PitchTree(items=items)
                >>> abjad.show(tree, strict=89) # doctest: +SKIP

            >>> tree.has_repeats()
            True

            ..  docs::

                >>> lilypond_file = tree.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                }
                <<
                    \new Staff
                    {
                        \new Voice
                        \with
                        {
                            \consists Horizontal_bracket_engraver
                        }
                        {
                            \time 1/8
                            \abjad-color-music #'red
                            e'8
                            ^ \markup { 0 }
                            \startGroup
                            fs'8
                            bf'8
                            \stopGroup
                            s8
                            a'8
                            ^ \markup { 1 }
                            \startGroup
                            g'8
                            af'8
                            b'8
                            a'8
                            \abjad-color-music #'red
                            cs'8
                            \stopGroup
                            s8
                            \abjad-color-music #'red
                            cs'8
                            ^ \markup { 2 }
                            \startGroup
                            \abjad-color-music #'blue
                            d'8
                            \abjad-color-music #'blue
                            d'8
                            \abjad-color-music #'red
                            e'8
                            \stopGroup
                            s8
                            \bar "|."                                                                    %! SCORE_1
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Doesn't have repeats:

            >>> items = [[4, 6, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
            >>> tree = baca.PitchTree(items=items)
            >>> abjad.show(tree, strict=89) # doctest: +SKIP

            >>> tree.has_repeats()
            False

            ..  docs::

                >>> lilypond_file = tree.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                }
                <<
                    \new Staff
                    {
                        \new Voice
                        \with
                        {
                            \consists Horizontal_bracket_engraver
                        }
                        {
                            \time 1/8
                            e'8
                            ^ \markup { 0 }
                            \startGroup
                            fs'8
                            bf'8
                            \stopGroup
                            s8
                            a'8
                            ^ \markup { 1 }
                            \startGroup
                            g'8
                            af'8
                            b'8
                            a'8
                            cs'8
                            \stopGroup
                            s8
                            c'8
                            ^ \markup { 2 }
                            \startGroup
                            d'8
                            ef'8
                            f'8
                            \stopGroup
                            s8
                            \bar "|."                                                                    %! SCORE_1
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        Returns true or false.
        """
        leaves = self.iterate(level=-1)
        for left, right in abjad.Sequence(leaves).nwise(n=2, wrapped=True):
            if left == right:
                return True
        return False

    def invert(self, axis=None):
        r"""
        Inverts pitch tree.

        ..  container:: example

            Example tree:

            >>> items = [[16, 18, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
            >>> tree = baca.PitchTree(items=items)
            >>> abjad.show(tree, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = tree.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                }
                <<
                    \new Staff
                    {
                        \new Voice
                        \with
                        {
                            \consists Horizontal_bracket_engraver
                        }
                        {
                            \time 1/8
                            e''8
                            ^ \markup { 0 }
                            \startGroup
                            fs''8
                            bf'8
                            \stopGroup
                            s8
                            a'8
                            ^ \markup { 1 }
                            \startGroup
                            g'8
                            af'8
                            b'8
                            a'8
                            cs'8
                            \stopGroup
                            s8
                            c'8
                            ^ \markup { 2 }
                            \startGroup
                            d'8
                            ef'8
                            f'8
                            \stopGroup
                            s8
                            \bar "|."                                                                    %! SCORE_1
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Inverts tree about first pitch when axis is none:

            >>> inversion = tree.invert()
            >>> abjad.show(inversion, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = inversion.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                }
                <<
                    \new Staff
                    {
                        \new Voice
                        \with
                        {
                            \consists Horizontal_bracket_engraver
                        }
                        {
                            \time 1/8
                            e''8
                            ^ \markup { 0 }
                            \startGroup
                            d''8
                            bf''8
                            \stopGroup
                            s8
                            b''8
                            ^ \markup { 1 }
                            \startGroup
                            cs'''8
                            c'''8
                            a''8
                            b''8
                            g'''8
                            \stopGroup
                            s8
                            af'''8
                            ^ \markup { 2 }
                            \startGroup
                            fs'''8
                            f'''8
                            ef'''8
                            \stopGroup
                            s8
                            \bar "|."                                                                    %! SCORE_1
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Inverts tree about pitch 0:

            >>> inversion = tree.invert(axis=0)
            >>> abjad.show(inversion, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = inversion.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                }
                <<
                    \new Staff
                    {
                        \new Voice
                        \with
                        {
                            \consists Horizontal_bracket_engraver
                        }
                        {
                            \time 1/8
                            af,8
                            ^ \markup { 0 }
                            \startGroup
                            fs,8
                            d8
                            \stopGroup
                            s8
                            ef8
                            ^ \markup { 1 }
                            \startGroup
                            f8
                            e8
                            cs8
                            ef8
                            b8
                            \stopGroup
                            s8
                            c'8
                            ^ \markup { 2 }
                            \startGroup
                            bf8
                            a8
                            g8
                            \stopGroup
                            s8
                            \bar "|."                                                                    %! SCORE_1
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Inverts tree about pitch 13:

            >>> inversion = tree.invert(axis=13)
            >>> abjad.show(inversion, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = inversion.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                }
                <<
                    \new Staff
                    {
                        \new Voice
                        \with
                        {
                            \consists Horizontal_bracket_engraver
                        }
                        {
                            \time 1/8
                            bf'8
                            ^ \markup { 0 }
                            \startGroup
                            af'8
                            e''8
                            \stopGroup
                            s8
                            f''8
                            ^ \markup { 1 }
                            \startGroup
                            g''8
                            fs''8
                            ef''8
                            f''8
                            cs'''8
                            \stopGroup
                            s8
                            d'''8
                            ^ \markup { 2 }
                            \startGroup
                            c'''8
                            b''8
                            a''8
                            \stopGroup
                            s8
                            \bar "|."                                                                    %! SCORE_1
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Returns new tree:

            >>> isinstance(inversion, baca.PitchTree)
            True

        """
        if axis is None and self:
            payload = self.get_payload()
            axis = payload[0]
        operator = abjad.Inversion(axis=axis)
        return self._apply_to_leaves_and_emit_new_tree(operator)

    def retrograde(self):
        r"""
        Gets retrograde of tree.

        ..  container:: example

            Example tree:

            >>> items = [[16, 18, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
            >>> tree = baca.PitchTree(items=items)
            >>> abjad.show(tree, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = tree.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                }
                <<
                    \new Staff
                    {
                        \new Voice
                        \with
                        {
                            \consists Horizontal_bracket_engraver
                        }
                        {
                            \time 1/8
                            e''8
                            ^ \markup { 0 }
                            \startGroup
                            fs''8
                            bf'8
                            \stopGroup
                            s8
                            a'8
                            ^ \markup { 1 }
                            \startGroup
                            g'8
                            af'8
                            b'8
                            a'8
                            cs'8
                            \stopGroup
                            s8
                            c'8
                            ^ \markup { 2 }
                            \startGroup
                            d'8
                            ef'8
                            f'8
                            \stopGroup
                            s8
                            \bar "|."                                                                    %! SCORE_1
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Gets retrograde of tree:

            >>> retrograde = tree.retrograde()
            >>> abjad.show(retrograde, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = retrograde.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                }
                <<
                    \new Staff
                    {
                        \new Voice
                        \with
                        {
                            \consists Horizontal_bracket_engraver
                        }
                        {
                            \time 1/8
                            c'8
                            ^ \markup { 0 }
                            \startGroup
                            d'8
                            ef'8
                            f'8
                            \stopGroup
                            s8
                            a'8
                            ^ \markup { 1 }
                            \startGroup
                            g'8
                            af'8
                            b'8
                            a'8
                            cs'8
                            \stopGroup
                            s8
                            e''8
                            ^ \markup { 2 }
                            \startGroup
                            fs''8
                            bf'8
                            \stopGroup
                            s8
                            \bar "|."                                                                    %! SCORE_1
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Returns new tree:

            >>> isinstance(retrograde, baca.PitchTree)
            True

        """
        items = list(self.items)
        items.reverse()
        result = abjad.new(self, items=items)
        return result

    def rotate(self, n=0):
        r"""
        Rotates tree by index ``n``.

        ..  container:: example

            Example tree:

            >>> items = [[16, 18, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
            >>> tree = baca.PitchTree(items=items)
            >>> abjad.show(tree, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = tree.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                }
                <<
                    \new Staff
                    {
                        \new Voice
                        \with
                        {
                            \consists Horizontal_bracket_engraver
                        }
                        {
                            \time 1/8
                            e''8
                            ^ \markup { 0 }
                            \startGroup
                            fs''8
                            bf'8
                            \stopGroup
                            s8
                            a'8
                            ^ \markup { 1 }
                            \startGroup
                            g'8
                            af'8
                            b'8
                            a'8
                            cs'8
                            \stopGroup
                            s8
                            c'8
                            ^ \markup { 2 }
                            \startGroup
                            d'8
                            ef'8
                            f'8
                            \stopGroup
                            s8
                            \bar "|."                                                                    %! SCORE_1
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Rotates tree to the right:

            >>> rotation = tree.rotate(n=1)
            >>> abjad.show(rotation, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = rotation.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                }
                <<
                    \new Staff
                    {
                        \new Voice
                        \with
                        {
                            \consists Horizontal_bracket_engraver
                        }
                        {
                            \time 1/8
                            c'8
                            ^ \markup { 0 }
                            \startGroup
                            d'8
                            ef'8
                            f'8
                            \stopGroup
                            s8
                            e''8
                            ^ \markup { 1 }
                            \startGroup
                            fs''8
                            bf'8
                            \stopGroup
                            s8
                            a'8
                            ^ \markup { 2 }
                            \startGroup
                            g'8
                            af'8
                            b'8
                            a'8
                            cs'8
                            \stopGroup
                            s8
                            \bar "|."                                                                    %! SCORE_1
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Rotates tree to the left:

            >>> rotation = tree.rotate(n=-1)
            >>> abjad.show(rotation, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = rotation.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                }
                <<
                    \new Staff
                    {
                        \new Voice
                        \with
                        {
                            \consists Horizontal_bracket_engraver
                        }
                        {
                            \time 1/8
                            a'8
                            ^ \markup { 0 }
                            \startGroup
                            g'8
                            af'8
                            b'8
                            a'8
                            cs'8
                            \stopGroup
                            s8
                            c'8
                            ^ \markup { 1 }
                            \startGroup
                            d'8
                            ef'8
                            f'8
                            \stopGroup
                            s8
                            e''8
                            ^ \markup { 2 }
                            \startGroup
                            fs''8
                            bf'8
                            \stopGroup
                            s8
                            \bar "|."                                                                    %! SCORE_1
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Rotates by zero:

            >>> rotation = tree.rotate(n=0)
            >>> abjad.show(rotation, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = rotation.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                }
                <<
                    \new Staff
                    {
                        \new Voice
                        \with
                        {
                            \consists Horizontal_bracket_engraver
                        }
                        {
                            \time 1/8
                            e''8
                            ^ \markup { 0 }
                            \startGroup
                            fs''8
                            bf'8
                            \stopGroup
                            s8
                            a'8
                            ^ \markup { 1 }
                            \startGroup
                            g'8
                            af'8
                            b'8
                            a'8
                            cs'8
                            \stopGroup
                            s8
                            c'8
                            ^ \markup { 2 }
                            \startGroup
                            d'8
                            ef'8
                            f'8
                            \stopGroup
                            s8
                            \bar "|."                                                                    %! SCORE_1
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Returns new tree:

            >>> isinstance(rotation, baca.PitchTree)
            True

        """
        items = list(self.items)
        items = abjad.sequence(items)
        items = items.rotate(n=n)
        result = abjad.new(self, items=items)
        return result

    def transpose(self, n=0):
        r"""
        Transposes pitch tree.

        ..  container:: example

            Example tree:

            >>> items = [[16, 18, 10], [9, 7, 8, 11, 9, 1], [0, 2, 3, 5]]
            >>> tree = baca.PitchTree(items=items)
            >>> abjad.show(tree, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = tree.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                }
                <<
                    \new Staff
                    {
                        \new Voice
                        \with
                        {
                            \consists Horizontal_bracket_engraver
                        }
                        {
                            \time 1/8
                            e''8
                            ^ \markup { 0 }
                            \startGroup
                            fs''8
                            bf'8
                            \stopGroup
                            s8
                            a'8
                            ^ \markup { 1 }
                            \startGroup
                            g'8
                            af'8
                            b'8
                            a'8
                            cs'8
                            \stopGroup
                            s8
                            c'8
                            ^ \markup { 2 }
                            \startGroup
                            d'8
                            ef'8
                            f'8
                            \stopGroup
                            s8
                            \bar "|."                                                                    %! SCORE_1
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Transposes tree by positive index:

            >>> transposition = tree.transpose(n=13)
            >>> abjad.show(transposition, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = transposition.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                }
                <<
                    \new Staff
                    {
                        \new Voice
                        \with
                        {
                            \consists Horizontal_bracket_engraver
                        }
                        {
                            \time 1/8
                            f'''8
                            ^ \markup { 0 }
                            \startGroup
                            g'''8
                            b''8
                            \stopGroup
                            s8
                            bf''8
                            ^ \markup { 1 }
                            \startGroup
                            af''8
                            a''8
                            c'''8
                            bf''8
                            d''8
                            \stopGroup
                            s8
                            cs''8
                            ^ \markup { 2 }
                            \startGroup
                            ef''8
                            e''8
                            fs''8
                            \stopGroup
                            s8
                            \bar "|."                                                                    %! SCORE_1
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Transposes tree by negative index:

            >>> transposition = tree.transpose(n=-13)
            >>> abjad.show(transposition, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = transposition.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                }
                <<
                    \new Staff
                    {
                        \new Voice
                        \with
                        {
                            \consists Horizontal_bracket_engraver
                        }
                        {
                            \time 1/8
                            ef'8
                            ^ \markup { 0 }
                            \startGroup
                            f'8
                            a8
                            \stopGroup
                            s8
                            af8
                            ^ \markup { 1 }
                            \startGroup
                            fs8
                            g8
                            bf8
                            af8
                            c8
                            \stopGroup
                            s8
                            b,8
                            ^ \markup { 2 }
                            \startGroup
                            cs8
                            d8
                            e8
                            \stopGroup
                            s8
                            \bar "|."                                                                    %! SCORE_1
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Transposes tree by zero index:

            >>> transposition = tree.transpose(n=0)
            >>> abjad.show(transposition, strict=89) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = transposition.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                }
                <<
                    \new Staff
                    {
                        \new Voice
                        \with
                        {
                            \consists Horizontal_bracket_engraver
                        }
                        {
                            \time 1/8
                            e''8
                            ^ \markup { 0 }
                            \startGroup
                            fs''8
                            bf'8
                            \stopGroup
                            s8
                            a'8
                            ^ \markup { 1 }
                            \startGroup
                            g'8
                            af'8
                            b'8
                            a'8
                            cs'8
                            \stopGroup
                            s8
                            c'8
                            ^ \markup { 2 }
                            \startGroup
                            d'8
                            ef'8
                            f'8
                            \stopGroup
                            s8
                            \bar "|."                                                                    %! SCORE_1
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        ..  container:: example

            Returns new tree:

            >>> isinstance(transposition, baca.PitchTree)
            True

        """
        operator = abjad.Transposition(n=n)
        return self._apply_to_leaves_and_emit_new_tree(operator)

class Registration(object):
    """
    Registration.

    ..  container:: example

        Registration in two parts:

        >>> components = [('[A0, C4)', 15), ('[C4, C8)', 27)]
        >>> registration = baca.Registration(components)

        >>> abjad.f(registration, strict=89)
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

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_components',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        components=None,
        ):
        components_ = []
        for component in components or []:
            if isinstance(component, RegistrationComponent):
                components_.append(component)
            else:
                component_ = RegistrationComponent(*component)
                components_.append(component_)
        self._components = components_ or None

    ### SPECIAL METHODS ###

    def __call__(self, pitches):
        r"""
        Calls registration on ``pitches``.

        ..  container:: example

            Transposes four pitches:

            >>> components = [('[A0, C4)', 15), ('[C4, C8)', 27)]
            >>> registration = baca.Registration(components)
            >>> pitches = registration([-24, -22, -23, -21])
            >>> for pitch in pitches:
            ...     pitch
            ...
            NamedPitch("c'''")
            NamedPitch("d'''")
            NamedPitch("cs'''")
            NamedPitch("ef''")

        ..  container:: example

            Transposes four other pitches:

            >>> components = [('[A0, C4)', 15), ('[C4, C8)', 27)]
            >>> registration = baca.Registration(components)
            >>> pitches = registration([0, 2, 1, 3])
            >>> for pitch in pitches:
            ...     pitch
            ...
            NamedPitch("c''''")
            NamedPitch("d''''")
            NamedPitch("cs''''")
            NamedPitch("ef'''")

        ..  container:: example

            Transposes four quartertones:

            >>> components = [('[A0, C4)', 15), ('[C4, C8)', 27)]
            >>> registration = baca.Registration(components)
            >>> pitches = registration([0.5, 2.5, 1.5, 3.5])
            >>> for pitch in pitches:
            ...     pitch
            ...
            NamedPitch("cqs''''")
            NamedPitch("dqs''''")
            NamedPitch("dqf''''")
            NamedPitch("eqf'''")

        Returns list of new pitches.
        """
        return [self._transpose_pitch(_) for _ in pitches]

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __format__(self, format_specification='') -> str:
        """
        Formats Abjad object.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f'unhashable type: {self}')
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _transpose_pitch(self, pitch):
        pitch = abjad.NamedPitch(pitch)
        for component in self.components:
            if pitch in component.source_pitch_range:
                start_pitch = component.target_octave_start_pitch
                stop_pitch = start_pitch + 12
                if start_pitch <= pitch < stop_pitch:
                    return pitch
                elif pitch < start_pitch:
                    while pitch < start_pitch:
                        pitch += 12
                    return pitch
                elif stop_pitch <= pitch:
                    while stop_pitch <= pitch:
                        pitch -= 12
                    return pitch
                else:
                    raise ValueError(pitch, self)
        else:
            raise ValueError(f'{pitch!r} not in {self!r}.')

    ### PUBLIC PROPERTIES ###

    @property
    def components(self):
        """
        Gets components.

        Returns list or none.
        """
        return self._components

class RegistrationComponent(object):
    """
    Registration component.

    ..  container:: example

        Initializes a registration component that specifies that all pitches
        from A0 up to and including C8 should be transposed to the octave
        starting at Eb5 (numbered pitch 15):

        >>> component = baca.RegistrationComponent('[A0, C8]', 15)
        >>> component
        RegistrationComponent(source_pitch_range=PitchRange('[A0, C8]'), target_octave_start_pitch=NumberedPitch(15))

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_source_pitch_range',
        '_target_octave_start_pitch',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        source_pitch_range='[A0, C8]',
        target_octave_start_pitch=0,
        ):
        if isinstance(source_pitch_range, abjad.PitchRange):
            source_pitch_range = copy.copy(source_pitch_range)
        else:
            source_pitch_range = abjad.PitchRange(source_pitch_range)
        target_octave_start_pitch = abjad.NumberedPitch(
            target_octave_start_pitch)
        self._source_pitch_range = source_pitch_range
        self._target_octave_start_pitch = target_octave_start_pitch

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a registration component with source pitch
        range and target octave start pitch equal to those of this registration
        component.

        Returns true or false.
        """
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __format__(self, format_specification=''):
        """
        Formats registration component.

        Returns string.
        """
        if format_specification in ('', 'storage'):
            return abjad.StorageFormatManager(self).get_storage_format()
        return str(self)

    def __hash__(self):
        """
        Hashes registration component.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f'unhashable type: {self}')
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return abjad.FormatSpecification(client=self)

    ### PUBLIC PROPERTIES ###

    @property
    def source_pitch_range(self):
        """
        Gets source pitch range of registration component.

        ..  container:: example

            Gets source pitch range of example component:

            >>> component = baca.RegistrationComponent('[A0, C8]', 15)
            >>> component.source_pitch_range
            PitchRange('[A0, C8]')

        Returns pitch range or none.
        """
        return self._source_pitch_range

    @property
    def target_octave_start_pitch(self):
        """
        Gets target octave start pitch of registration component.

        ..  container:: example

            Gets target octave start pitch of example component:

            >>> component = baca.RegistrationComponent('[A0, C8]', 15)
            >>> component.target_octave_start_pitch
            NumberedPitch(15)

        Returns numbered pitch or none.
        """
        return self._target_octave_start_pitch

class ZaggedPitchClassMaker(object):
    r"""
    Zagged-pitch-class-maker.

    ..  container:: example

        >>> maker = baca.ZaggedPitchClassMaker(
        ...     pc_cells=[
        ...         [7, 1, 3, 4, 5, 11],
        ...         [3, 5, 6, 7],
        ...         [9, 10, 0, 8],
        ...         ],
        ...     division_ratios=[
        ...         [[1], [1], [1], [1, 1]],
        ...         [[1], [1], [1], [1, 1, 1], [1, 1, 1]],
        ...         ],
        ...         grouping_counts=[1, 1, 1, 2, 3],
        ...     )
        >>> pitch_class_tree = maker()
        >>> abjad.show(pitch_class_tree, strict=89) # doctest: +SKIP

        >>> for tree in pitch_class_tree:
        ...     tree.get_payload(nested=True)
        [[NumberedPitchClass(7), NumberedPitchClass(1), NumberedPitchClass(3), NumberedPitchClass(4), NumberedPitchClass(5), NumberedPitchClass(11)]]
        [[NumberedPitchClass(3), NumberedPitchClass(5), NumberedPitchClass(6), NumberedPitchClass(7)]]
        [[NumberedPitchClass(9), NumberedPitchClass(10), NumberedPitchClass(0), NumberedPitchClass(8)]]
        [[NumberedPitchClass(7), NumberedPitchClass(3)], [NumberedPitchClass(5), NumberedPitchClass(6)]]
        [[NumberedPitchClass(8), NumberedPitchClass(9), NumberedPitchClass(10), NumberedPitchClass(0)], [NumberedPitchClass(11), NumberedPitchClass(7), NumberedPitchClass(1), NumberedPitchClass(3), NumberedPitchClass(4), NumberedPitchClass(5)], [NumberedPitchClass(0), NumberedPitchClass(8), NumberedPitchClass(9), NumberedPitchClass(10)]]
        [[NumberedPitchClass(5), NumberedPitchClass(11)]]
        [[NumberedPitchClass(7), NumberedPitchClass(1)]]
        [[NumberedPitchClass(3), NumberedPitchClass(4)]]
        [[NumberedPitchClass(6)], [NumberedPitchClass(7), NumberedPitchClass(3)]]
        [[NumberedPitchClass(5)], [NumberedPitchClass(4), NumberedPitchClass(5)], [NumberedPitchClass(11), NumberedPitchClass(7)]]
        [[NumberedPitchClass(1), NumberedPitchClass(3)]]
        [[NumberedPitchClass(5), NumberedPitchClass(6), NumberedPitchClass(7), NumberedPitchClass(3)]]
        [[NumberedPitchClass(10), NumberedPitchClass(0), NumberedPitchClass(8), NumberedPitchClass(9)]]
        [[NumberedPitchClass(3), NumberedPitchClass(5), NumberedPitchClass(6), NumberedPitchClass(7)], [NumberedPitchClass(9)]]
        [[NumberedPitchClass(10), NumberedPitchClass(0)], [NumberedPitchClass(8)], [NumberedPitchClass(3), NumberedPitchClass(4), NumberedPitchClass(5)]]
        [[NumberedPitchClass(11), NumberedPitchClass(7), NumberedPitchClass(1)]]
        [[NumberedPitchClass(8), NumberedPitchClass(9), NumberedPitchClass(10), NumberedPitchClass(0)]]
        [[NumberedPitchClass(1), NumberedPitchClass(3), NumberedPitchClass(4), NumberedPitchClass(5), NumberedPitchClass(11), NumberedPitchClass(7)]]
        [[NumberedPitchClass(7), NumberedPitchClass(3), NumberedPitchClass(5), NumberedPitchClass(6)], [NumberedPitchClass(7), NumberedPitchClass(1), NumberedPitchClass(3), NumberedPitchClass(4), NumberedPitchClass(5), NumberedPitchClass(11)]]
        [[NumberedPitchClass(6), NumberedPitchClass(7)], [NumberedPitchClass(3), NumberedPitchClass(5)], [NumberedPitchClass(0), NumberedPitchClass(8), NumberedPitchClass(9), NumberedPitchClass(10)]]
        [[NumberedPitchClass(5), NumberedPitchClass(6), NumberedPitchClass(7), NumberedPitchClass(3)]]
        [[NumberedPitchClass(10)]]
        [[NumberedPitchClass(0), NumberedPitchClass(8)]]
        [[NumberedPitchClass(9)], [NumberedPitchClass(11), NumberedPitchClass(7)]]
        [[NumberedPitchClass(1), NumberedPitchClass(3)], [NumberedPitchClass(4), NumberedPitchClass(5)], [NumberedPitchClass(9), NumberedPitchClass(10), NumberedPitchClass(0), NumberedPitchClass(8)]]
        [[NumberedPitchClass(5), NumberedPitchClass(11), NumberedPitchClass(7), NumberedPitchClass(1), NumberedPitchClass(3), NumberedPitchClass(4)]]
        [[NumberedPitchClass(3), NumberedPitchClass(5), NumberedPitchClass(6), NumberedPitchClass(7)]]
        [[NumberedPitchClass(4), NumberedPitchClass(5), NumberedPitchClass(11), NumberedPitchClass(7), NumberedPitchClass(1), NumberedPitchClass(3)]]
        [[NumberedPitchClass(7)], [NumberedPitchClass(3), NumberedPitchClass(5)]]
        [[NumberedPitchClass(6)], [NumberedPitchClass(8)], [NumberedPitchClass(9), NumberedPitchClass(10)]]
        [[NumberedPitchClass(0)]]
        [[NumberedPitchClass(6), NumberedPitchClass(7), NumberedPitchClass(3), NumberedPitchClass(5)]]
        [[NumberedPitchClass(0), NumberedPitchClass(8), NumberedPitchClass(9), NumberedPitchClass(10)]]
        [[NumberedPitchClass(3), NumberedPitchClass(4), NumberedPitchClass(5), NumberedPitchClass(11), NumberedPitchClass(7), NumberedPitchClass(1)], [NumberedPitchClass(10), NumberedPitchClass(0), NumberedPitchClass(8), NumberedPitchClass(9)]]
        [[NumberedPitchClass(1), NumberedPitchClass(3), NumberedPitchClass(4)], [NumberedPitchClass(5), NumberedPitchClass(11), NumberedPitchClass(7)], [NumberedPitchClass(5), NumberedPitchClass(6), NumberedPitchClass(7), NumberedPitchClass(3)]]

    """

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_division_ratios',
        '_grouping_counts',
        '_pc_cells',
        )

    _call_before_persisting_to_disk = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        pc_cells=None,
        division_ratios=None,
        grouping_counts=None,
        ):
        self._pc_cells = pc_cells
        self._division_ratios = division_ratios
        self._grouping_counts = grouping_counts

    ### SPECIAL METHODS ###

    def __call__(self):
        """
        Calls zagged pitch-class maker.

        Returns pitch-class tree.
        """
        pc_cells = classes.Sequence(self.pc_cells)
        pc_cells = pc_cells.helianthate(-1, 1)
        prototype = (tuple, abjad.Ratio)
        if self.division_ratios is None:
            division_ratios = [[1]]
        elif all(isinstance(_, prototype) for _ in self.division_ratios):
            division_ratios = self.division_ratios
        elif all(isinstance(_, list) for _ in self.division_ratios):
            division_ratios = classes.Sequence(self.division_ratios)
            division_ratios = division_ratios.helianthate(-1, 1)
            division_ratios = division_ratios.flatten(depth=1)
        division_ratios = [abjad.Ratio(_) for _ in division_ratios]
        division_ratios = abjad.CyclicTuple(division_ratios)
        pc_cells_copy = pc_cells[:]
        pc_cells = []
        for i, pc_segment in enumerate(pc_cells_copy):
            parts = classes.Sequence(pc_segment).partition_by_ratio_of_lengths(
                division_ratios[i],
                )
            pc_cells.extend(parts)
        grouping_counts = self.grouping_counts or [1]
        pc_cells = classes.Sequence(pc_cells).partition_by_counts(
            grouping_counts,
            cyclic=True,
            overhang=True,
            )
        # this block was uncommented during krummzeit
        #pc_cells = [abjad.join_subsequences(x) for x in pc_cells]
        #pc_cells = classes.Sequence(pc_cells).partition_by_counts(
        #    grouping_counts,
        #    cyclic=True,
        #    overhang=True,
        #    )
        material = PitchTree(
            items=pc_cells,
            item_class=abjad.NumberedPitchClass,
            )
        return material

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a zagged pitch-class with type and
        public properties equal to those of this zagged pitch-class maker.

        Returns boolean.
        """
        agent = abjad.StorageFormatManager(self)
        return agent.compare(argument)

    def __hash__(self):
        """
        Hashes zagged pitch-class maker.
        """
        agent = abjad.StorageFormatManager(self)
        return hash(agent.hash_values)

    ### PUBLIC PROPERTIES ###

    @property
    def division_ratios(self):
        """
        Gets division cells of maker.

        ..  container:: example

            Same as helianthation when division ratios and grouping counts are
            both none:


            >>> maker = baca.ZaggedPitchClassMaker(
            ...     pc_cells=[[0, 1, 2], [3, 4]],
            ...     division_ratios=None,
            ...     grouping_counts=None,
            ...     )
            >>> pitch_class_tree = maker()
            >>> abjad.show(pitch_class_tree, strict=89) # doctest: +SKIP

            >>> for tree in pitch_class_tree:
            ...     tree.get_payload(nested=True)
            [[NumberedPitchClass(0), NumberedPitchClass(1), NumberedPitchClass(2)]]
            [[NumberedPitchClass(3), NumberedPitchClass(4)]]
            [[NumberedPitchClass(4), NumberedPitchClass(3)]]
            [[NumberedPitchClass(2), NumberedPitchClass(0), NumberedPitchClass(1)]]
            [[NumberedPitchClass(1), NumberedPitchClass(2), NumberedPitchClass(0)]]
            [[NumberedPitchClass(3), NumberedPitchClass(4)]]
            [[NumberedPitchClass(4), NumberedPitchClass(3)]]
            [[NumberedPitchClass(0), NumberedPitchClass(1), NumberedPitchClass(2)]]
            [[NumberedPitchClass(2), NumberedPitchClass(0), NumberedPitchClass(1)]]
            [[NumberedPitchClass(3), NumberedPitchClass(4)]]
            [[NumberedPitchClass(4), NumberedPitchClass(3)]]
            [[NumberedPitchClass(1), NumberedPitchClass(2), NumberedPitchClass(0)]]

        ..  container:: example

            Divides every cell in half:

            >>> maker = baca.ZaggedPitchClassMaker(
            ...     pc_cells=[[0, 1, 2, 3], [4, 5, 6, 7]],
            ...     division_ratios=[[(1, 1)]],
            ...     grouping_counts=None,
            ...     )
            >>> pitch_class_tree = maker()
            >>> abjad.show(pitch_class_tree, strict=89) # doctest: +SKIP

            >>> for tree in pitch_class_tree:
            ...     tree.get_payload(nested=True)
            [[NumberedPitchClass(0), NumberedPitchClass(1)]]
            [[NumberedPitchClass(2), NumberedPitchClass(3)]]
            [[NumberedPitchClass(4), NumberedPitchClass(5)]]
            [[NumberedPitchClass(6), NumberedPitchClass(7)]]
            [[NumberedPitchClass(7), NumberedPitchClass(4)]]
            [[NumberedPitchClass(5), NumberedPitchClass(6)]]
            [[NumberedPitchClass(3), NumberedPitchClass(0)]]
            [[NumberedPitchClass(1), NumberedPitchClass(2)]]
            [[NumberedPitchClass(2), NumberedPitchClass(3)]]
            [[NumberedPitchClass(0), NumberedPitchClass(1)]]
            [[NumberedPitchClass(6), NumberedPitchClass(7)]]
            [[NumberedPitchClass(4), NumberedPitchClass(5)]]
            [[NumberedPitchClass(5), NumberedPitchClass(6)]]
            [[NumberedPitchClass(7), NumberedPitchClass(4)]]
            [[NumberedPitchClass(1), NumberedPitchClass(2)]]
            [[NumberedPitchClass(3), NumberedPitchClass(0)]]

        Returns list of lists.
        """
        return self._division_ratios

    @property
    def grouping_counts(self):
        """
        Gets grouping counts of maker.

        ..  container:: example

            Groups helianthated cells:

            >>> maker = baca.ZaggedPitchClassMaker(
            ...     pc_cells=[[0, 1, 2], [3, 4]],
            ...     division_ratios=None,
            ...     grouping_counts=[1, 2],
            ...     )
            >>> pitch_class_tree = maker()
            >>> abjad.show(pitch_class_tree, strict=89) # doctest: +SKIP

            >>> for tree in pitch_class_tree:
            ...     tree.get_payload(nested=True)
            [[NumberedPitchClass(0), NumberedPitchClass(1), NumberedPitchClass(2)]]
            [[NumberedPitchClass(3), NumberedPitchClass(4)], [NumberedPitchClass(4), NumberedPitchClass(3)]]
            [[NumberedPitchClass(2), NumberedPitchClass(0), NumberedPitchClass(1)]]
            [[NumberedPitchClass(1), NumberedPitchClass(2), NumberedPitchClass(0)], [NumberedPitchClass(3), NumberedPitchClass(4)]]
            [[NumberedPitchClass(4), NumberedPitchClass(3)]]
            [[NumberedPitchClass(0), NumberedPitchClass(1), NumberedPitchClass(2)], [NumberedPitchClass(2), NumberedPitchClass(0), NumberedPitchClass(1)]]
            [[NumberedPitchClass(3), NumberedPitchClass(4)]]
            [[NumberedPitchClass(4), NumberedPitchClass(3)], [NumberedPitchClass(1), NumberedPitchClass(2), NumberedPitchClass(0)]]

        Returns nonempty list of positive integers.
        """
        return self._grouping_counts

    @property
    def pc_cells(self):
        """
        Gets pitch-class cells of maker.

        Returns list of number lists.
        """
        return self._pc_cells

### EXPRESSION CONSTRUCTORS ###

def _pitch_class_segment(items=None, **keywords):
    if items:
        return PitchClassSegment(items=items, **keywords)
    name = keywords.pop('name', None)
    expression = classes.Expression(name=name)
    callback = expression._make_initializer_callback(
        PitchClassSegment,
        module_names=['baca'],
        string_template='{}',
        **keywords
        )
    expression = expression.append_callback(callback)
    return abjad.new(expression, proxy_class=PitchClassSegment)

def _pitch_class_set(items=None, **keywords):
    if items:
        return PitchClassSet(items=items, **keywords)
    name = keywords.pop('name', None)
    expression = classes.Expression(name=name)
    callback = expression._make_initializer_callback(
        PitchClassSet,
        module_names=['baca'],
        string_template='{}',
        **keywords
        )
    expression = expression.append_callback(callback)
    return abjad.new(expression, proxy_class=PitchClassSet)

def _pitch_segment(items=None, **keywords):
    if items:
        return PitchSegment(items=items, **keywords)
    name = keywords.pop('name', None)
    expression = classes.Expression(name=name)
    callback = expression._make_initializer_callback(
        PitchSegment,
        module_names=['baca'],
        string_template='{}',
        **keywords
        )
    expression = expression.append_callback(callback)
    return abjad.new(expression, proxy_class=PitchSegment)

def _pitch_set(items=None, **keywords):
    if items:
        return PitchSet(items=items, **keywords)
    name = keywords.pop('name', None)
    expression = classes.Expression(name=name)
    callback = expression._make_initializer_callback(
        PitchSet,
        module_names=['baca'],
        string_template='{}',
        **keywords
        )
    expression = expression.append_callback(callback)
    return abjad.new(expression, proxy_class=PitchSet)
