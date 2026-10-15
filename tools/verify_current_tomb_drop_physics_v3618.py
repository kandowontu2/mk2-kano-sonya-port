"""Source-qualified current KanoP1 native random Tomb drop; not a held RGB gate.

The retained1836 held image oracle is inapplicable after the actual native RNG
chooses7<50. Preserve all failed invocations and test the original branch's
complete signed field/gravity cadence from actual current callbacks instead.
No new physical capture, RNG/health/position edits, or visual/audio promotion.
"""
import copy
import hashlib
import json
import re
import subprocess
from pathlib import Path

import run_current_stage_palette_pixels_v3602 as stage

ROOT, need, sha = stage.ROOT, stage.need, stage.sha
CASE = ROOT / 'audit_v3611_current_tomb_snapshot_forensic'
OUT = ROOT / 'audit_v3619_current_kano_tomb_native_drop_physics_checked'


def records(log, prefix):
    return [dict(re.findall(r'(\w+)=([^\s]+)', line)) for line in log.splitlines() if line.startswith(prefix + ' ')]


def n(row, field, base=10):
    return int(row[field], base)


def phase_contract(rows, branch, floor):
    ceiling = floor - 259
    first = branch + 1
    need(all(frame in rows for frame in range(first, branch + 270)), 'Every actual native drop callback field')
    for frame in range(first, branch + 129):
        row = rows[frame]
        need((n(row,'y'),n(row,'vy',16),n(row,'gravity',16),n(row,'action',16)) == (ceiling,0,0,0x503),
             'Original native128-field ceiling hold and action')
    for frame in range(branch + 129, branch + 241):
        row = rows[frame]
        need((n(row,'y'),n(row,'vy',16),n(row,'gravity',16),n(row,'action',16)) ==
             (ceiling+(frame-(branch+129))//8,0x2000,0,0x503),
             'Original native112-field slow descent at one-eighth pixel')
    first_fall = branch + 241
    row = rows[first_fall]; initial_y = ceiling + 14
    need((n(row,'y'),n(row,'vy',16),n(row,'gravity',16),n(row,'action',16)) ==
         (initial_y,0x20000,0x8000,0x503), 'Actual original two-pixel launch/half-pixel gravity')
    lo, hi, total = 0, 65535, 0
    for frame in range(first_fall + 1, branch + 269):
        prior, row = rows[frame-1], rows[frame]
        vy = n(row,'vy',16)
        need(vy == n(prior,'vy',16)+0x8000 and n(row,'gravity',16)==0x8000 and n(row,'action',16)==0x503,
             'Every original native falling velocity/gravity callback')
        total += vy; delta = n(row,'y')-initial_y
        lo=max(lo,delta*65536-total);hi=min(hi,(delta+1)*65536-1-total)
        need(lo<=hi,'Actual signed integer fall has one consistent native16.16 fractional origin')
    row=rows[branch+269]
    need((n(row,'y'),n(row,'vy',16),n(row,'gravity',16)) == (floor,0,0),
         'Actual original native own-floor landing and velocity/gravity clear')
    return dict(branchFrame=branch, floor=floor, ceiling=ceiling, ceilingHoldFields=128,
                slowDescentFields=112, originalFallFirstField=first_fall,
                nativeLandingField=branch+269, consistentFractionalOriginInterval=[lo,hi],
                checkedConsecutiveCallbacks=269)


def run():
    need(not OUT.exists(),'Fresh narrow native drop proof')
    stage.controls()
    log=(CASE/'run.log').read_text()
    old=(stage.REFERENCE/'run.log').read_text(encoding='utf-8-sig')
    actual=[line for line in stage.classic(log).splitlines() if not line.startswith('MK2_STAGE_FORENSIC_')]
    original=stage.classic(old).splitlines()
    keep=('MK2_STAGE_BOOT ','MK2_STAGE_INPUT ','MK2_STAGE_DAMAGE ','MK2_STAGE_MATCH ',
          'MK2_STAGE_SELECT ','MK2_STAGE_SELECT_ID ','MK2_STAGE_WINDOW ','MK2_STAGE_COMMAND ','MK2_STAGE_RESULT ')
    need([line for line in actual if line.startswith(keep)] == [line for line in original if line.startswith(keep)],
         'Every original physical coin/start/select/input/earned-damage/window/command/terminal record unchanged')
    need(not re.search(r'LUA ERROR|Lua error|stack traceback|Fatal error',log+(CASE/'stderr.log').read_text(),re.I),
         'No observer/native runtime errors in complete actual capture')
    guest,old_guest,payload,_,_=stage.inventory.current.expected_current()
    need((CASE/'guest_maincpu.bin').read_bytes()==guest and
         (ROOT/stage.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()==payload, 'Whole actual current native guest/payload')
    original_program=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for first,last in ((0xff8eaf00,0xff8eb490),(0xff876650,0xff876b40),(0xff80e980,0xff80ecf0),
                       (0xff82b800,0xff82bca0)):
        lo,hi=(first-0xff800000)//8,(last-0xff800000)//8
        need(guest[lo:hi]==old_guest[lo:hi]==original_program[lo:hi],
             'Original native Tomb/RNG/fall/teardown implementation bytes untouched')
    lines='\n'.join(actual)
    fields=stage.native.rows(lines,'FIELD')
    need([n(row,'age')for row in fields[:801]]==list(range(801)) and
         [n(row,'frame')for row in fields[:801]]==list(range(8173,8974)), 'Complete actual action/cleanup fields')
    actor,main=fields[0]['own'],fields[0]['main'];victim,victim_main=fields[0]['victim'],fields[0]['victim_main']
    need((fields[0]['id'],fields[0]['victim_id'])==('17','18'),'Actual own real Kano/Sonya, no proxy IDs')
    for row in fields:
        need((row['own'],row['main'],row['id']) in ((actor,main,'17'),('00000000','00000000','-1')) and
             (row['victim'],row['victim_main'],row['victim_id']) in ((victim,victim_main,'18'),('00000000','00000000','-1')),
             'Actual native body/owner identity throughout action and cleanup')
    need(next(n(r,'frame')for r in fields if r['own']==r['victim']=='00000000')==8680 and
         fields[800]['mode']=='3'and fields[800]['arena']=='2','Native actor cleanup and next arena, no softlock')
    tags=records(log,'MK2_STAGE_PROVENANCE_BRANCH')
    selected=[row for row in tags if n(row,'frame')>=8173 and row['entry'] in
              ('FF8EB0D0','FF8EB150','FF80EC20','FF8EB1A0','FF8EB1B0','FF8EB200','FF8EB290','FF876650','FF8EB3C0','FF8EB400')]
    wanted=['FF8EB0D0','FF8EB150','FF80EC20','FF8EB1A0','FF8EB1B0','FF8EB200','FF8EB290','FF876650','FF8EB3C0']
    need([r['entry']for r in selected]==wanted,'Actual original native rare drop dispatch, not the held branch')
    branch=n(selected[0],'frame');value=n(selected[3],'a0',16)
    need(branch==8217 and selected[2]['a0']=='00000032'and value==7 and 0<=value<50 and
         [n(r,'frame')for r in selected[4:]]==[branch,branch+128,branch+240,branch+240,branch+268] and
         all(r['io0']=='FFFFFFFF'and r['a8']==r['actor']==victim and r['a13']==r['main']==victim_main for r in selected),
         'Original5-percent random gate, unpressed controls, actual native victim task and cadence')
    need(tuple(selected[7][field]for field in('a0','a1','a2','a3')) ==
         ('00000000','00020000','00008000','00000FFF'), 'Original native fall helper parameters')
    callbacks=[row for row in records(log,'MK2_STAGE_PROVENANCE_FIELD') if 8173<n(row,'frame')<=8680]
    callback_map={n(row,'frame'):row for row in callbacks}
    need(len(callback_map)==len(callbacks) and all(row['actor']==victim and row['main']==victim_main and
         row['id']=='18'for row in callbacks), 'Actual complete native victim callback ownership')
    phase=phase_contract(callback_map,branch,85)
    faults=[]
    for label,frame,field,change in (('hold position',branch+2,'y',1),
                                   ('slow descent velocity',branch+130,'vy',1),
                                   ('fall gravity',branch+242,'gravity',1),
                                   ('own floor landing',branch+269,'y',1)):
        changed=copy.deepcopy(callback_map);base=16 if field in('vy','gravity') else 10
        before=n(changed[frame],field,base);after=before+change
        changed[frame][field]=f'{after:08X}'if base==16 else str(after)
        try:phase_contract(changed,branch,85)
        except ValueError as error:faults.append(dict(label=label,frame=frame,field=field,before=before,after=after,rejectedBy=str(error)))
        else:raise ValueError('Changed actual native drop field accepted')
        phase_contract(callback_map,branch,85)
    before=json.loads((CASE/'input_hashes_before.json').read_text())
    pins={}
    def pin(file,wanted=None):
        key=str(Path(file).resolve());value=sha(file)
        need(wanted is None or value==wanted,'Actual relevant source/evidence unchanged');pins[key]=value
    for file,wanted in before.items():pin(file,wanted)
    for file in CASE.rglob('*'):
        if file.is_file():pin(file)
    pin(stage.REFERENCE/'run.log',json.loads(stage.OLD_REPORT.read_text())['inputHashes'][str(stage.REFERENCE/'run.log')])
    pin(ROOT/'audit_v3612_stage_snapshot_forensic/report.json')
    pin(ROOT/'tools/run_stage_snapshot_forensic_v3610.py')
    pin(ROOT/'mk2/mk2-maincpu.bin');pin(ROOT/'tools/verify_current_tomb_drop_physics_v3614.py')
    pin(ROOT/'tools/verify_current_tomb_drop_physics_v3616.py');pin(__file__)
    return dict(passed=True,candidate=stage.NAME,actualNativeKanoP1TombRandomDropPhysicsAndCleanupAccepted=True,
                actualNativeRandomValue=value,nativeThreshold=50,actualTrueWinner=17,actualTrueVictim=18,
                phase=phase,allOriginalPhysicalInputsAndEarnedDamageRecordsUnchanged=True,
                qualifiedActualFieldFaults=faults,completeOriginalNativeSourceRangesUnchanged=True,
                originalHeldReferenceInvocationNotRelabeledPassed=True,
                rejectedPreActionOwnerComparison=dict(tool=str(ROOT/'tools/verify_current_tomb_drop_physics_v3616.py'),
                    terminalExitCode=1,error='Compared earlier finish-window callbacks with the later Tomb victim task; action-scoped original2080 callback window restored'),
                rejectedPreExecutionSyntaxAttempt=dict(tool=str(ROOT/'tools/verify_current_tomb_drop_physics_v3614.py'),
                    terminalExitCode=1,error='SyntaxError: missing space in conditional expression else10; no verifier ran'),
                standaloneCurrentForensicChildExitCodeMetadataAvailable=False,
                actualCurrentVisibleSceneArtShadowsEraseAndAudioAccepted=False,
                actualHeldSceneRGBReferenceApplicableToThisRandomDrop=False,
                hiddenCurrentVRAMOrUniversalStageRuntimeAcceptance=False,
                newRuntimeOrExecutableROMWAVPixelVRAMCopies=0,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)


if __name__=='__main__':
    need(not OUT.exists(),'Immutable original-branch proof')
    value=run();OUT.mkdir();saved=OUT/'report.json';saved.write_text(json.dumps(value,indent=2)+'\n')
    before=sha(saved);result=subprocess.run(['compact.exe','/C','/I','/Q',str(saved)],capture_output=True,text=True)
    need(result.returncode==0 and sha(saved)==before,'Lossless compact native phase proof')
    print(json.dumps({k:v for k,v in value.items()if k not in('inputHashes','qualifiedActualFieldFaults')},indent=2))
