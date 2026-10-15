"""Bounded actual native records/RGB observer comparison and transport faults.

Exact recorded states against the completed no-hook capture, and every visible
field against the completed lightweight palette/reset observer. Neither proves
unobserved world-state, other scenes, audio, or universal noninterference.
"""
import copy
import json
import re
import subprocess
from pathlib import Path
import numpy as np

import run_current_tomb_ram_v3633 as current

ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v3639_current_tomb_observer_equivalence_checked'


def lines(value):
    return [line for line in value.splitlines()if line.startswith('MK2_STAGE_')and
            not line.startswith(('MK2_STAGE_FORENSIC_','MK2_STAGE_TRANSFER_'))]


def transport_gate(guest):
    adapter=current.model.Transport();previous=None;records=[]
    encode=lambda raw:np.frombuffer(raw,dtype='<u4').astype('>u4').tobytes().hex().upper()
    for index,raw in enumerate((guest[:524288],guest[524288:])):
        row=dict(file=f'display_pre_{index}.bin',family='pre',bytes='524288',prior=str(index),
                 blocks='',block_bytes='64',encoding='u32le_numeric_hex_delta')
        blocks=[str(first//64)+':'+encode(raw[first:first+64])for first in range(0,len(raw),64)
                if previous is None or raw[first:first+64]!=previous[first:first+64]]
        row['blocks']=str(len(blocks));need(adapter.decode(row,','.join(blocks))==raw,
             'Entire current native guest-block transport round trip, no approximation')
        records.append(dict(rawSHA256=current.model.digest(raw),blocks=len(blocks)));previous=raw
    changed=bytearray(previous[:64]);changed[0]^=1;changed=bytes(changed)
    row=dict(file='display_pre_2.bin',family='pre',bytes='524288',prior='1',blocks='1',
             block_bytes='64',encoding='u32le_numeric_hex_delta')
    faults=[]
    vectors=[('duplicate changed block','0:'+encode(changed)+',0:'+encode(changed),'Unique increasing native blocks'),
             ('out of range','8192:'+encode(changed),'Complete bounded native block'),
             ('omitted native word','0:'+encode(changed[:60]),'Complete bounded native block'),
             ('unchanged block declared changed','0:'+encode(previous[:64]),'Only exact changed transport blocks')]
    for label,encoded,wanted in vectors:
        bad=dict(row);bad['blocks']=str(len(encoded.split(',')))
        try:copy.deepcopy(adapter).decode(bad,encoded)
        except ValueError as error:
            need(str(error)==wanted,'Qualified actual transport fault reaches intended contract')
            faults.append(dict(label=label,rejectedBy=str(error)))
        else:raise ValueError('Malformed native transport accepted')
    need(adapter.previous['pre']==previous,'Counterexamples never alter actual transport base')
    return dict(actualCurrentNativeBytesRoundTripped=1048576,records=records,qualifiedFaults=faults)


def main():
    need(not OUT.exists(),'Fresh immutable bounded observer comparison')
    proof_path=current.OUT/'report.json';proof=json.loads(proof_path.read_text())
    need(proof['passed']and proof['sampledFrames']==537 and proof['nativeScene']['nativeDrop'],
         'Actual current rare-drop rendering proof')
    inherited=json.loads((ROOT/'audit_v3623_current_tomb_drop_full_scope_checkpoint/checkpoint.json').read_text())
    no_hook=ROOT/'audit_v3611_current_tomb_snapshot_forensic/run.log'
    light=ROOT/'audit_v3598_current_kano_tomb_p1_palette_pixels/visible_frames.json'
    native_file=current.CASE/'run.log';visible_file=current.CASE/'continuous_scene_records.json'
    for path in (no_hook,light):need(sha(path)==inherited['inputHashes'][str(path)],'Previously pinned actual capture unchanged')
    for path in (native_file,visible_file):need(sha(path)==proof['inputHashes'][str(path)],'Current live checked actual capture unchanged')
    actual=lines(native_file.read_text());prior=lines(no_hook.read_text())
    need(actual==prior and len(actual)==8811,'All actual recorded native/control/provenance rows exactly match no-hook capture')
    actual_rgb=json.loads(visible_file.read_text());prior_rgb=json.loads(light.read_text())
    need([r['frame']for r in actual_rgb]==[r['frame']for r in prior_rgb]==list(range(8174,8711))and
         all(a['rgbSHA256']==b['currentRGB_SHA256']for a,b in zip(actual_rgb,prior_rgb)),
         'All actual heavyweight and lightweight current RGB fields exactly match')
    guest,_,payload,_,_=current.stage.inventory.current.expected_current()
    guest_file=current.CASE/'guest_maincpu.bin'
    need(guest_file.read_bytes()==guest and sha(guest_file)==proof['inputHashes'][str(guest_file)],
         'Actual complete initialized native current guest')
    transport=transport_gate(guest)
    # Comparison counterexamples use actual recorded rows/hashes and restore
    # the real datasets, without normalizing field timing or native randoms.
    bad=list(actual);bad[0]=bad[0].replace('frame=1 ','frame=2 ')
    need(bad[0]!=actual[0]and bad!=prior,'Actual native row alteration is rejected')
    bad_rgb=copy.deepcopy(actual_rgb);value=bad_rgb[0]['rgbSHA256']
    bad_rgb[0]['rgbSHA256']=value[:-1]+('0'if value[-1]!='0'else'1')
    need(sum(a['rgbSHA256']!=b['currentRGB_SHA256']for a,b in zip(bad_rgb,prior_rgb))==1,
         'One actual visible-field hash alteration is rejected')
    need(actual==prior and all(a['rgbSHA256']==b['currentRGB_SHA256']for a,b in zip(actual_rgb,prior_rgb)),
         'Unmodified native/RGB positives remain exact')
    pins={str(path):sha(path)for path in(proof_path,no_hook,light,native_file,visible_file,guest_file,
         ROOT/'audit_v3623_current_tomb_drop_full_scope_checkpoint/checkpoint.json',Path(__file__).resolve(),
         Path(current.__file__),Path(current.model.__file__))}
    value=dict(passed=True,candidate=current.stage.NAME,exactActualNativeControlAndProvenanceRecords=8811,
               exactCurrentHeavyAndLightVisibleFields=537,exactCurrentHeavyAndLightVisibleRGBPixels=54559200,
               noHookRecordedStatesAndLightHookVisibleFieldsAcceptedForThisOneScene=True,
               fullHiddenWorldStateObserverEquivalenceAccepted=False,universalHookNoninterferenceAccepted=False,
               priorFailedHeldOracleInvocationsNotRelabeled=True,qualifiedComparisonFaults=2,
               transport=transport,newRuntimeOrRasterVRAMAudioPlayableCopies=0,
               stageAudioFidelityAccepted=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)
    OUT.mkdir();file=OUT/'report.json';file.write_text(json.dumps(value,indent=2)+'\n')
    before=sha(file);result=subprocess.run(['compact.exe','/C','/I','/Q',str(file)],capture_output=True,text=True)
    need(result.returncode==0 and sha(file)==before,'Lossless compact bounded comparison')
    print(json.dumps({k:v for k,v in value.items()if k not in('inputHashes','transport')},indent=2))


if __name__=='__main__':main()
