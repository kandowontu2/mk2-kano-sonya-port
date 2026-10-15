"""Whole current native campaign: explicit stage16 Ring/retreat input replay."""
import argparse
import inspect
import json
import re
import sys
from pathlib import Path
from types import SimpleNamespace
import verify_current_boss_shao_cooldown_retreat_v2630 as old
import verify_current_cpu_square_v3280 as current
import current_shao_ring_source_v3487 as policy

ROOT=current.ROOT;need=current.need;sha=current.assembly.sha
DRIVER=policy.DRIVER
BASELINE=policy.BASELINE
RUNNER=policy.RUNNER

def source_boundary():
    policy.runner_boundary()
    return policy.source_boundary()

def matched(folder,pins):
    meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    build=json.loads((ROOT/current.current.CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    snapshots=json.loads((folder/'source_snapshot_paths.json').read_text(encoding='utf-8-sig'))
    need(meta['candidate']==current.current.CANDIDATE and meta['exit_code']==0 and
         not meta['cheats_enabled'] and meta['assistance']=='none' and meta['snapshot_schema']==2 and
         meta['raw_audio_files_written']==meta['new_builds_or_rom_copies']==0 and before==meta['input_hashes'],
         'Terminal current cold input-only campaign with exact hierarchy snapshots')
    need(meta['executable_sha256']==build['executable_sha256']==current.current.EXE and
         meta['payload_sha256']==build['payload_sha256']==current.current.PAYLOAD and
         all(before.get(path)==digest for path,digest in build['input_hashes'].items()),'Every actual compiled input and playable byte bound')
    for file,digest in before.items():
        need(sha(file)==digest,'Actual campaign input unchanged');pins[file]=digest
        if Path(file).suffix in('.lua','.ps1','.json'):
            target=Path(snapshots[file]).resolve()
            need(target.is_relative_to(folder.resolve()) and sha(target)==digest,'Exact collision-free frozen input')
            pins[str(target)]=digest
        if Path(file).suffix=='.lua':
            need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',Path(file).read_text()),'No Lua guest/actor/AI/health/RNG injection')
    runner=(ROOT/RUNNER).read_text()
    need('-nocheat' in runner and '-noautoframeskip -frameskip 0' in runner and
         '-wavwrite'not in runner and 'MK2KS_DIAGNOSTIC_CPU_ID'not in runner,
         'Native run; no added audio files or prescribed opponent')
    source_boundary()

def make_verifier(expected):
    source=inspect.getsource(old.verify)
    changes={
      'if text_override is None:':'if False: # Do not compare current3172 chronology to obsolete1836.',
      "harnesses=list((folder/'input_sources').glob('mk2ks_natural_campaign_*v*.lua'))":
      "harnesses=[folder/'input_sources/tree'/DRIVER]",
      "need(r['height']<=8,'Every held boss physical attempt is grounded; native crouch/recovery/hit state may ignore it and no successful activation is implied')":
      "need(r['stage']==16 or r['height']<=8,'Kintaro ground plan unchanged; Shao buttons may be ignored during native hurt/air states, never assumed activated')",
      "('Down','High_Punch','Block','Up','Left','Right','High_Kick')":
      "('Down','High_Punch','Block','Up','Left','Right','High_Kick','Low_Punch')",
      "need(not any(r['tag']=='SPECIAL'and r['stage']in(15,16)for r in rows),'No special/proxy attack credited at bosses')":
      "need(all(r['stage']==16 and identity==18 and r['move']=='ring' for r in rows if r['tag']=='SPECIAL' and r['stage']in(15,16)),'Only true native Sonya Ring allowed by declared Shao policy; original full special instruction/actor/Main checks below remain mandatory')",
      "need(len(confirmed)==2 and all(r['roster']==identity and r['state']==3 for r in confirmed),'Own true ID before native confirm')":
      """terminal=[r for r in rows if r['tag']=='RESULT']
        need(len(terminal)==1,'Exactly one terminal for bounded final selection')
        final_frame=terminal[0]['frame']
        expected_checks=[selection['frame']+age for age in (130,146)if selection['frame']+age<=final_frame]
        need([r['frame']for r in confirmed]==expected_checks and all(r['roster']==identity and r['state']==3 for r in confirmed),'Every due native selection check retains own true ID')
        if len(expected_checks)<2:
            need(selection is selections[-1] and 0<=final_frame-selection['frame']<146 and
                 not any(r['tag']=='FIGHT'and r['event']>selection['event']for r in rows),
                 'Only final time-limit-interrupted CSS may lack not-yet-due checks; never accept a started match without confirmation')
        else:
            need(len(confirmed)==2,'Both original completed selection checks retained')""",
    }
    for before,after in changes.items():
        need(source.count(before)==1,'Explicit single full-verifier adaptation');source=source.replace(before,after)
    source=source.replace('mk2ks_natural_campaign_boss_shao_cooldown_retreat_v2628.lua',DRIVER).replace('shao_cooldown_retreat','shao_ring_retreat')
    reset='if frame-1 not in boss_frames:first=frame;command=-1000;down_since=None;jump=-1000;direction=None'
    need(source.count(reset)==1,'Unique original input replay reset')
    source=source.replace(reset,reset+';projectile=None;projectile_direction=None')
    first=source.index("            if f['stage']==16:\n")
    last=source.index('            elif False:',first)
    source=source[:first]+"""            if f['stage']==16:
                down_since=None
                back='Left'if forward=='Right'else'Right'
                if projectile is not None and frame-projectile<64:
                    age=frame-projectile
                    if 2<=age<5:expected.add('Down')
                    if 7<=age<10:expected.add(projectile_direction)
                    if 8<=age<12:expected.add('Low_Punch')
                    if age>=15:expected.update(('Down','Block'))
                elif f['height']>8:
                    if frame-jump<48:expected.add(direction)
                    if frame%6<3:expected.add('High_Kick')
                elif f['gap']<140:
                    projectile=None
                    if frame-jump>=40:
                        jump=frame;direction=back;planned_direction=back
                        should_plan='shao_ring_retreat_jump_attempt';expected={'Up',back}
                    elif frame-jump<4:expected={'Up',direction}
                    else:expected={'Down','Block'}
                else:
                    projectile=frame;projectile_direction=forward;planned_direction=forward
                    should_plan='shao_ring_command_attempt'
"""+source[last:]
    namespace=dict(vars(old));namespace.update(NAME=current.current.CANDIDATE,matched=matched,
        DRIVER=DRIVER,current_source=SimpleNamespace(expected=lambda:expected),
        restore_shao_ring_retreat_policy=lambda source:source_boundary())
    exec(compile(source,__file__+'::whole_native_campaign_with_explicit_input_policy','exec'),namespace)
    return namespace['verify']

def verify(folder):
    expected=current.expected_current()
    native=make_verifier(expected)
    result=native(folder)
    need(result['passed'],'Whole native campaign invariants: '+repr(result['errors']))
    need(result['player']=='sonya','This declared Ring input policy is Sonya only')
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    rows=old.parse(log,result['human_slot'],result['player'])
    terminal=next(r['frame']for r in rows if r['tag']=='RESULT')
    selections=[r for r in rows if r['tag']=='SELECT']
    pending=[r for r in selections if terminal-r['frame']<146]
    need(len(pending)<=1 and (not pending or pending[0]is selections[-1]),'Only last bounded CSS can be incomplete')
    fields=[r for r in rows if r['tag']=='BOSS_FIELD'and r['stage']==16]
    # Qualified input replay faults use the exact same whole-campaign verifier,
    # with unchanged original source/guest/capture hashes and positive control.
    negatives=[]
    if fields:
        attack=next((line for line in log.splitlines()if line.startswith('MK2_NAT_CAMPAIGN_INPUT ')and
                   'button=Low_Punch 'in line and int(re.search(r' frame=(\d+)',line)[1])in{r['frame']for r in fields}),None)
        if attack:
            for label,changed in (
                ('missing_actual_Ring_LP',log.replace(attack+'\n','',1)),
                ('wrong_actual_Ring_attack',log.replace(attack,attack.replace('button=Low_Punch','button=High_Punch'),1))):
                need(changed!=log,'Non-vacuous actual boss input fault')
                rejected=native(folder,text_override=changed)
                need(not rejected['passed']and any('independently replayed native state'in error for error in rejected['errors']),
                     'Specific actual physical input replay rejection, not unrelated exception')
                negatives.append(label)
            need(native(folder)['passed'],'Same-path unchanged full-campaign positive control')
    for path in folder.rglob('*'):
        if path.is_file():result['inputHashes'][str(path.resolve())]=sha(path)
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).suffix=='.py'and Path(file).resolve().is_relative_to(ROOT/'tools'):
            result['inputHashes'][str(Path(file).resolve())]=sha(file)
    for file,digest in result['inputHashes'].items():need(sha(file)==digest,'Captured native proof inputs unchanged')
    result.update(current3172WholeGuestAndCampaignAccepted=True,wholeOriginalCampaignVerifierRetained=True,
        obsolete1836ChronologyNotUsedAsCurrent3172Oracle=True,originalOrdinaryAndKintaroInputsAndNativeObserversExact=True,
        actualShaoRingPolicyFields=len(fields),specificActualInputCounterexamples=negatives,
        actualShaoNativeRingEntries=sum(r['tag']=='SPECIAL' and r['stage']==16 and r['move']=='ring' for r in rows),
        ringEntriesNeverAssumedChildCollisionDamageOrBossVictory=True,
        rawAudioFilesWritten=0,newBuildsOrROMCopies=0,fullPortAcceptance=False)
    result.update(finalTimeLimitInterruptedSelection=pending,
        incompleteFinalSelectionNotAcceptedAsConfirmed=True,
        allCompletedSelectionConfirmationChecksRetained=True)
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();need(not args.output.exists(),'Immutable campaign report')
    value=verify(args.folder.resolve());args.output.mkdir()
    path=args.output/'report.json';path.write_text(json.dumps(value,indent=2)+'\n')
    import subprocess
    digest=sha(path);compact=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(compact.returncode==0 and sha(path)==digest,'Lossless report compression')
    print(json.dumps({k:v for k,v in value.items()if k not in('inputHashes','uppercutAssignmentFrames')},indent=2))
