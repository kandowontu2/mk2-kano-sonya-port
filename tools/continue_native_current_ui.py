"""Keep completed runs; qualify real CPU owners and capture only missing Sonya P2."""
import inspect
import capture_launch_candidate_ui as original
import qualify_native_current_ui_audio_owners as owners

def capture_missing():
    source=inspect.getsource(original.capture)
    first=source.index('  need(len(owner_rows)==2*state')
    last=source.index('  need(all(sha(',first)
    source=source[:first]+"  owner_contract=owners.gate(text,state['terminal'])\n"+source[last:]
    scope=dict(original.__dict__,owners=owners,__file__=__file__)
    exec(compile(source,__file__+'::entire_original_capture_owned_CPU_launch','exec'),scope)
    return scope['capture']
