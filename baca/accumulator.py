import abjad

from . import scoping as _scoping
from . import sequence as _sequence


def segment_accumulation_defaults():
    return {
        "append_phantom_measure": True,
    }


def _get_voice_names(score_template):
    voice_names = ["Global_Skips", "Global_Rests", "Timeline_Scope"]
    score = score_template()
    for voice in abjad.iterate.components(score, abjad.Voice):
        if voice.name is not None:
            voice_names.append(voice.name)
            if "Music_Voice" in voice.name:
                name = voice.name.replace("Music_Voice", "Rest_Voice")
            else:
                name = voice.name.replace("Voice", "Rest_Voice")
            voice_names.append(name)
    return tuple(voice_names)


def _initialize_time_signatures(time_signatures):
    time_signatures = time_signatures or ()
    time_signatures_ = list(time_signatures)
    time_signatures_ = []
    for time_signature in time_signatures:
        if isinstance(time_signature, str):
            time_signature = abjad.TimeSignature.from_string(time_signature)
        else:
            time_signature = abjad.TimeSignature(time_signature)
        time_signatures_.append(time_signature)
    time_signatures_ = tuple(time_signatures_)
    if not time_signatures_:
        time_signatures_ = None
    return time_signatures_


def _unpack_measure_token_list(measure_token_list):
    assert isinstance(measure_token_list, list), repr(measure_token_list)
    measure_tokens = []
    for measure_token in measure_token_list:
        if isinstance(measure_token, int):
            measure_tokens.append(measure_token)
        elif isinstance(measure_token, tuple):
            assert len(measure_token) == 2
            start, stop = measure_token
            measure_tokens.append((start, stop))
        else:
            raise TypeError(measure_token_list)
    return measure_tokens


def _unpack_scope_pair(scopes, abbreviations):
    assert isinstance(scopes, tuple), repr(scopes)
    assert len(scopes) == 2, repr(scopes)
    assert isinstance(scopes[0], (list, str)), repr(scopes)
    assert isinstance(scopes[1], (int, list, tuple)), repr(scopes)
    if isinstance(scopes[0], str):
        voice_names = [scopes[0]]
    else:
        voice_names = scopes[0]
    assert isinstance(voice_names, list), repr(voice_names)
    assert all(isinstance(_, str) for _ in voice_names)
    measure_tokens = []
    if isinstance(scopes[1], int):
        measure_tokens.append(scopes[1])
    elif isinstance(scopes[1], tuple):
        assert len(scopes[1]) == 2, repr(scopes)
        start, stop = scopes[1]
        measure_tokens.append((start, stop))
    elif isinstance(scopes[1], list):
        measure_tokens = _unpack_measure_token_list(scopes[1])
    else:
        raise TypeError(scopes)
    scopes_ = []
    voice_names_ = []
    for voice_name in voice_names:
        result = abbreviations.get(voice_name, voice_name)
        if isinstance(result, list):
            voice_names_.extend(result)
        else:
            assert isinstance(result, str)
            voice_names_.append(result)
    voice_names = voice_names_
    for voice_name in voice_names:
        for measure_token in measure_tokens:
            scope = _scoping.Scope(measures=measure_token, voice_name=voice_name)
            scopes_.append(scope)
    prototype = (_scoping.Scope, _scoping.TimelineScope)
    assert all(isinstance(_, prototype) for _ in scopes_)
    return scopes_


def _unpack_scopes(scopes, abbreviations):
    scope_type = (_scoping.Scope, _scoping.TimelineScope)
    if isinstance(scopes, str):
        result = abbreviations.get(scopes, scopes)
        if isinstance(result, str):
            voice_names = [result]
        else:
            assert isinstance(result, list), repr(result)
            voice_names = result
        scopes__ = []
        for voice_name in voice_names:
            scope = _scoping.Scope(voice_name=voice_name)
            scopes__.append(scope)
    elif isinstance(scopes, tuple):
        scopes__ = _unpack_scope_pair(scopes, abbreviations)
    elif isinstance(scopes, scope_type):
        scopes__ = [scopes]
    else:
        assert isinstance(scopes, list), repr(scopes)
        scopes_ = []
        for scope in scopes:
            if isinstance(scope, tuple):
                scopes__ = _unpack_scope_pair(scope, abbreviations)
                scopes_.extend(scopes__)
            else:
                scopes_.append(scope)
        scopes__ = scopes_
    assert isinstance(scopes__, list), repr(scopes__)
    scopes_ = []
    for scope in scopes__:
        if isinstance(scope, str):
            voice_name = abbreviations.get(scope, scope)
            scope_ = _scoping.Scope(voice_name=voice_name)
            scopes_.append(scope_)
        elif isinstance(scope, tuple):
            voice_name, measures = scope
            voice_name = abbreviations.get(voice_name, voice_name)
            if isinstance(measures, list):
                measures = _unpack_measure_token_list(measures)
                for measure_token in measures:
                    scope_ = _scoping.Scope(
                        measures=measure_token, voice_name=voice_name
                    )
                    scopes_.append(scope_)
            else:
                scope_ = _scoping.Scope(measures=measures, voice_name=voice_name)
                scopes_.append(scope_)
        else:
            scope_ = scope
            scopes_.append(scope_)
    return scopes_


class CommandAccumulator:
    """
    Segment-maker.
    """

    __slots__ = (
        "append_phantom_measure",
        "commands",
        "functions",
        "instruments",
        "margin_markups",
        "metronome_marks",
        "score_template",
        "skips_instead_of_rests",
        "time_signatures",
        "voice_metadata",
        "voice_names",
    )

    def __init__(
        self,
        *functions,
        append_phantom_measure=False,
        instruments=None,
        margin_markups=None,
        metronome_marks=None,
        score_template=None,
        skips_instead_of_rests=False,
        time_signatures=None,
    ):
        self.functions = functions or ()
        assert append_phantom_measure in (True, False)
        self.append_phantom_measure = append_phantom_measure
        self.commands = []
        self.instruments = instruments
        self.margin_markups = margin_markups
        self.metronome_marks = metronome_marks
        assert score_template is not None, repr(score_template)
        self.score_template = score_template
        self.skips_instead_of_rests = skips_instead_of_rests
        self.time_signatures = _initialize_time_signatures(time_signatures)
        self.voice_metadata = {}
        self.voice_names = _get_voice_names(score_template)

    def __call__(self, scopes, *commands):
        """
        Calls segment-maker on ``scopes`` and ``commands``.
        """
        classes = (list, _scoping.Suite)
        commands_ = _sequence.Sequence(commands).flatten(classes=classes, depth=-1)
        commands = tuple(commands_)
        if self.score_template is not None and hasattr(
            self.score_template, "voice_abbreviations"
        ):
            abbreviations = self.score_template.voice_abbreviations
        else:
            abbreviations = {}
        abbreviations = abbreviations or {}
        scopes_ = _unpack_scopes(scopes, abbreviations)
        scope_type = (_scoping.Scope, _scoping.TimelineScope)
        assert all(isinstance(_, scope_type) for _ in scopes_), repr(scopes_)
        for command in commands:
            if command is None:
                continue
            if isinstance(command, list):
                raise Exception("use baca.suite().")
            if not isinstance(command, _scoping.Command):
                message = "\n\nMust be command:"
                message += f"\n\n{repr(command)}"
                raise Exception(message)
        scope_count = len(scopes_)
        for i, current_scope in enumerate(scopes_):
            if current_scope.voice_name not in self.voice_names:
                raise Exception(f"unknown voice name {current_scope.voice_name!r}.")
            if isinstance(current_scope, _scoping.TimelineScope):
                for scope_ in current_scope.scopes:
                    if scope_.voice_name in abbreviations:
                        voice_name = abbreviations[scope_.voice_name]
                        scope_._voice_name = voice_name
            for command in commands:
                if command is None:
                    continue
                assert isinstance(command, _scoping.Command), repr(command)
                if not command._matches_scope_index(scope_count, i):
                    continue
                if isinstance(command, _scoping.Command):
                    commands_ = _sequence.Sequence([command])
                else:
                    commands_ = command
                for command_ in commands_:
                    assert isinstance(command_, _scoping.Command), repr(command_)
                    measures = command_.measures
                    if isinstance(measures, int):
                        measures = (measures, measures)
                    if measures is not None:
                        scope_ = abjad.new(current_scope, measures=measures)
                    else:
                        scope_ = abjad.new(current_scope)
                    command_ = abjad.new(command_, scope=scope_)
                    self.commands.append(command_)
