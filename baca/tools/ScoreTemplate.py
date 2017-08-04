# -*- coding: utf-8 -*-
import abc
import abjad


class ScoreTemplate(abjad.ScoreTemplate):
    r'''Score template
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    voice_abbreviations = {
        }

    voice_colors = {
        }

#    ### SPECIAL METHODS ###
#
#    @abc.abstractmethod
#    def __call__(self):
#        r'''Calls score template.
#
#        Returns score.
#        '''
#        pass

    ### PRIVATE METHODS ###

    def _attach_tag(self, instrument_tag, context):
        assert isinstance(instrument_tag, str), repr(str)
        tag_string = 'tag {}'.format(instrument_tag)
        tag_command = abjad.LilyPondCommand(
            tag_string,
            'before',
            )
        abjad.attach(tag_command, context)

    def _make_time_signature_context(self):
        time_signature_context_multimeasure_rests = abjad.Context(
            context_name='TimeSignatureContextMultimeasureRests',
            name='Time Signature Context Multimeasure Rests',
            )
        time_signature_context_skips = abjad.Context(
            context_name='TimeSignatureContextSkips',
            name='Time Signature Context Skips',
            )
        time_signature_context = abjad.Context(
            [
                time_signature_context_multimeasure_rests,
                time_signature_context_skips,
            ],
            context_name='TimeSignatureContext',
            is_simultaneous=True,
            name='Time Signature Context',
            )
        return time_signature_context

    def _validate_voice_names(self, score):
        voice_names = []
        for voice in abjad.iterate(score).by_class(abjad.Voice):
            voice_names.append(voice.name)
        for voice_name in sorted(self.voice_abbreviations.items()):
            if voice_name not in voice_names:
                message = 'voice not found in score: {!r}.'
                message = message.format(voice_name)
                raise Exception(message)
        for voice_name in sorted(self.voice_colors):
            if voice_name not in voice_names:
                message = 'voice not found in score: {!r}.'
                message = message.format(voice_name)
                raise Exception(message)
