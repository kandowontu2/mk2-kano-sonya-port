"""Actual cold initialized windows for the coordinate-only native successor."""
import code
import inspect
import json
import struct
import traceback
from pathlib import Path

import verify_native_shang_drain_startup as initial
import verify_native_shang_drain_startup_successor as corrected

ROOT=initial.ROOT
NAME='diagnostic_native_shang_drain_anchors'
OUT=ROOT/'audit_native_shang_drain_anchors_startup'
BUILD_GUARD=ROOT/'audit_native_shang_drain_anchors_build_source/report.json'
ANCHORS=ROOT/'audit_native_shang_drain_anchors_source/report.json'
RAM={}

def expected(folder):
    wanted=initial.expected(folder)
    physical=(ROOT/NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    wanted['owned'],_=corrected.expected_owned(physical)
    anchors=json.loads(ANCHORS.read_text())
    initial.need(anchors['passed'] and anchors['changedHighBytes']==18 and
                 len(anchors['actualCppFaultsRejected'])==36,'Whole source-qualified coordinate repair')
    high=bytearray(wanted['high'])
    for row in anchors['ownCoordinateRepair']:
        at=(row['descriptor']-0xff800000)//8+4
        initial.need(struct.unpack_from('<hh',high,at)==(row['previousX'],row['previousY']),
                     'Independent v1 descriptor exactly matches predecessor geometry')
        struct.pack_into('<hh',high,at,row['x'],row['y'])
    initial.need(sum(a!=b for a,b in zip(wanted['high'],high))==18,'Exactly18 independent coordinate byte changes')
    wanted['high']=bytes(high)
    initial.need({k:initial.digest(v)for k,v in wanted.items()}==dict(
        high=anchors['proposedGuestSHA256'],owned=anchors['proposedOwnedSHA256'],
        graphics=anchors['proposedNewGraphicsSHA256']),'All three independent complete window models match source proof')
    return wanted

def run():
    source=inspect.getsource(initial.run)
    before="meta['prior_candidate'] == old.NAME"
    initial.need(source.count(before)==1,'Unique actual compiled predecessor guard')
    source=source.replace(before,"meta['prior_candidate'] == 'diagnostic_native_shang_owned_drain'",1)
    before='paths = [Path(__file__), LUA, meta_path, BUILD_GUARD,'
    initial.need(source.count(before)==1,'Unique startup independent model provenance boundary')
    source=source.replace(before,'paths = [Path(__file__), Path(initial.__file__), Path(corrected.__file__), ANCHORS, LUA, meta_path, BUILD_GUARD,',1)
    scope=dict(vars(initial),initial=initial,corrected=corrected,expected=expected,NAME=NAME,
               OUT=OUT,BUILD_GUARD=BUILD_GUARD,ANCHORS=ANCHORS,RAM=RAM,__file__=__file__)
    exec(compile(source,__file__+'::unchanged_native_startup_with_complete_corrected_models','exec'),scope)
    return scope['run']()

if __name__=='__main__':
    try:run()
    except Exception as error:
        failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
        if OUT.exists():
            path=OUT/'failure.json';initial.need(not path.exists(),'Frozen original failure must not be overwritten')
            path.write_text(json.dumps(failure,indent=2)+'\n')
        print(json.dumps(failure,indent=2),flush=True)
        code.interact(banner='Same original startup handle and actual buffers retained; never timeout-reboot.',local=dict(RAM=RAM))
