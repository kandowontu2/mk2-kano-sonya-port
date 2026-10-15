"""Original samples.cpp pre-existing-length source-number semantics.

First Square loads channel12 from length0; second Square and bicycle load
it from retained length45512. stop()/EOF retain source_len. Waveform and
position operations are unchanged; all earlier actual rejections retained.
"""
import inspect
import json
import traceback
from pathlib import Path
import qualify_native_selector_sonya_repeated_cue_pcm_bound as previous

original=previous.original
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_native_selector_sonya_repeated_cue_pcm_loaded_checked'
FAIL=previous.OUT/'failure.json'


def execute(state):
    failure=json.loads(FAIL.read_text())
    need(not failure['passed'] and "'3012', '12', (13, 45512, 0.0), (4294967295, 45512, 0.0)" in failure['error'],
         'Original real second-launch source-number rejection preserved')
    sample_source=(ROOT/'mame-mkp/src/devices/sound/samples.cpp').read_text()
    need('chan.source_num = (chan.source_len > 0) ? samplenum : -1;\n\tchan.source_len = sample.data.size();' in sample_source and
         'chan.source = nullptr;\n\tchan.source_num = -1;' in sample_source,
         'Actual native start uses previous length; stop retains that length')
    scope=dict(vars(original),OUT=OUT,__file__=__file__,original=original,previous=previous,FAIL=FAIL)
    source=inspect.getsource(original.bindings)
    need(source.count('source.count(old)==3')==1,'Exact prior two-use binding correction')
    source=source.replace('source.count(old)==3','source.count(old)==2',1)
    old="    exec(compile(clocks,__file__+'::whole_original_clocks_each_actual_launch','exec'),scope)"
    new="""    old_number=\"number=14 if spec['word']=='6B01'and pos<spec['length']else 0xffffffff\"
    new_number=\"previous=[s for s in extra if s['channel']==channel and s['start']<spec['start']];number=spec['sample'] if previous and previous[-1]['length']>0 and pos<spec['length'] else 0xffffffff\"
    need(clocks.count(old_number)==1,'Whole original source-number expression')
    clocks=clocks.replace(old_number,new_number,1)
    exec(compile(clocks,__file__+'::whole_original_clocks_each_actual_launch','exec'),scope)"""
    need(source.count(old)==1,'Whole original native clock model retained')
    exec(compile(source.replace(old,new,1),__file__+'::original_previous_length_source_number','exec'),scope)
    source=inspect.getsource(original.execute)
    old='paths=(Path(__file__),PARENT,'
    new='paths=(Path(__file__),Path(original.__file__),Path(previous.__file__),original.OUT/\'failure.json\',FAIL,previous.OUT/\'waveform.json\',PARENT,'
    need(source.count(old)==1,'Pin every original source and actual rejection')
    exec(compile(source.replace(old,new,1),__file__+'::whole_original_repeated_cue_PCM','exec'),scope)
    return scope['execute'](state)


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        if not OUT.exists():OUT.mkdir()
        need(not (OUT/'failure.json').exists(),'Preserve original loaded-source rejection')
        original.geometry.coverage.original.phases.original.capture.choices.current.prior.save(OUT/'failure.json',
            dict(passed=False,goalStatus='active',error=repr(error),traceback=traceback.format_exc(),
                 newNativeGames=0,fullPortAcceptance=False))
        raise
