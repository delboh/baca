import abjad
from .Command import Command


class DiatonicClusterCommand(Command):
    r'''Diatonic cluster command.

    ..  container:: example

        ::

            >>> staff = abjad.Staff("c' d' e' f'")
            >>> command = baca.diatonic_clusters([4, 6])
            >>> command(staff)
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                <c' d' e' f'>4
                <d' e' f' g' a' b'>4
                <e' f' g' a'>4
                <f' g' a' b' c'' d''>4
            }

    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_widths',
        )

    ### INITIALIZER ###

    def __init__(self, widths, selector='baca.select().plts()'):
        Command.__init__(self, selector=selector)
        assert abjad.mathtools.all_are_nonnegative_integers(widths)
        widths = abjad.CyclicTuple(widths)
        self._widths = widths

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        plts = self._select(argument)
        if not plts:
            return
        for i, plt in enumerate(plts):
            width = self.widths[i]
            start = self._get_lowest_diatonic_pitch_number(plt)
            diatonic_numbers = range(start, start + width)
            class_ = abjad.PitchClass
            dictionary = \
                class_._diatonic_pitch_class_number_to_pitch_class_number
            numbers = [
                (12 * (x // 7)) + dictionary[x % 7] for x in diatonic_numbers
                ]
            pitches = [abjad.NamedPitch(_) for _ in numbers]
            for pl in plt:
                chord = abjad.Chord(pl)
                chord.note_heads[:] = pitches
                abjad.mutate(pl).replace(chord)

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

    def _select(self, argument):
        if argument is None:
            return
        assert self.selector is not None, repr(self)
        plts = argument
        if self.selector is not None:
            plts = self.selector(plts)
            last = self.selector.callbacks[-1]
            if isinstance(last, abjad.GetItemCallback):
                plts = [plts]
        if not plts:
            return
        for plt in plts:
            if not isinstance(plt, abjad.LogicalTie):
                raise Exception(f'must be PLTs: {plts!r}')
            if not plt.is_pitched:
                raise Exception(f'must be PLTs: {plts!r}')
        return plts

    ### PUBLIC PROPERTIES ###

    @property
    def widths(self):
        r'''Gets widths.

        Defaults to none.

        Set to positive integers or none.

        Returns positive integers or none.
        '''
        return self._widths
