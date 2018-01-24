import abjad


class SchemeManifest(abjad.AbjadObject):
    r'''Scheme manifest.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(1) Library'

    _dynamics = (
        ('sfz_f', 'f'),
        ('sfz_p', 'p'),
        )

    ### PUBLIC PROPERTIES ###

    @property
    def dynamics(self):
        r'''Gets dynamics.

        ..  container:: example

            >>> for dynamic in baca.scheme.dynamics:
            ...     dynamic
            ...
            'sfz_f'
            'sfz_p'

        Returns list.
        '''
        return [_[0] for _ in self._dynamics]

    ### PUBLIC METHODS ###

    def dynamic_to_steady_state(self, dynamic):
        r'''Changes `dynamic` to steady state.

        ..  container:: example

            >>> baca.scheme.dynamic_to_steady_state('sfz_p')
            'p'

        Returns string.
        '''
        for dynamic_, steady_state in self._dynamics:
            if dynamic_ == dynamic:
                return steady_state
        raise KeyError(dynamic)
