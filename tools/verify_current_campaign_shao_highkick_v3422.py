"""Whole native campaign proof: current3172 and explicit high-kick input replay."""
import argparse
import inspect
import json
import re
import sys
from pathlib import Path
from types import SimpleNamespace
import verify_current_boss_shao_cooldown_retreat_v2630 as old
import verify_current_cpu_square_v3280 as current

ROOT=current.ROOT;need=current.need;sha=current.assembly.sha
DRIVER='mk2ks_natural_campaign_shao_highkick_v3419.lua'
BASELINE='mk2ks_natural_campaign_shao_lowkick_v3406.lua'
RUNNER='tools/run_current_campaign_shao_highkick_v3420.ps1'

def source_boundary():
    before=(ROOT/BASELINE).read_text();after=(ROOT/DRIVER).read_text()
    proof=json.loads((ROOT/'audit_v3412_current_kano_natural_lowkick_campaign_checked/report.json').read_text())
    need(proof['passed'] and proof['inputHashes'][str(ROOT/BASELINE)]==sha(ROOT/BASELINE),
         'Previously accepted full ordinary/Kintaro/native-observer source unchanged')
    start='    if stage==16 then\n';stop='    elseif quiet then\n'
    need(before.count(start)==after.count(start)==before.count(stop)==after.count(stop)==1,'Unique Shao-only branch')
    a=before.index(start);b=before.index(stop,a);c=after.index(start);d=after.index(stop,c)
    restored=after[:c]+before[a:b]+after[d:]
    restored=restored.replace('shao_crouch_highkick','shao_crouch_lowkick')
    need(restored==before,'Only stage16 physical decisions and policy labels differ; whole ordinary/Kintaro/selection/health/win/ending source exact')
    declared="""    if stage==16 then
     -- Physical strategy only: release guard earlier and pulse high kick.
     -- The original crouching strike6 has12damage and5native contact checks;
     -- activation and success still come only from actual native records.
     boss_walk_last_x=nil
     press('Down')
     if gap<=125 and cpu_height<20 then
      if frame%12<2 then
       if frame%12==0 then decision('shao_crouch_highkick_attempt')end
       press('High Kick')
      end
     else
      press('Block')
     end
"""
    need(after[c:d]==declared,'Exact declared physical high-kick policy; no game/register/health/RNG writes')
    return after

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
      "('Down','High_Punch','Block','Up','Left','Right','High_Kick','Low_Kick')",
    }
    for before,after in changes.items():
        need(source.count(before)==1,'Explicit single full-verifier adaptation');source=source.replace(before,after)
    source=source.replace('mk2ks_natural_campaign_boss_shao_cooldown_retreat_v2628.lua',DRIVER).replace('shao_cooldown_retreat','shao_crouch_highkick')
    first=source.index("            if f['stage']==16:\n")
    last=source.index('            elif False:',first)
    source=source[:first]+"""            if f['stage']==16:
                down_since=None;expected={'Down'}
                if f['gap']<=125 and f['cpu_height']<20:
                    if frame%12<2:expected.add('High_Kick')
                    if frame%12==0:should_plan='shao_crouch_highkick_attempt'
                else:expected.add('Block')
"""+source[last:]
    namespace=dict(vars(old));namespace.update(NAME=current.current.CANDIDATE,matched=matched,
        DRIVER=DRIVER,current_source=SimpleNamespace(expected=lambda:expected),
        restore_shao_crouch_highkick_policy=lambda source:source_boundary())
    exec(compile(source,__file__+'::whole_native_campaign_with_explicit_input_policy','exec'),namespace)
    return namespace['verify']

def verify(folder):
    expected=current.expected_current()
    native=make_verifier(expected)
    result=native(folder)
    need(result['passed'],'Whole native campaign invariants: '+repr(result['errors']))
    log=(folder/'run.log').read_text(encoding='utf-8-sig')
    rows=old.parse(log,result['human_slot'],result['player'])
    fields=[r for r in rows if r['tag']=='BOSS_FIELD'and r['stage']==16]
    # Qualified input replay faults use the exact same whole-campaign verifier,
    # with unchanged original source/guest/capture hashes and positive control.
    negatives=[]
    if fields:
        kick=next((line for line in log.splitlines()if line.startswith('MK2_NAT_CAMPAIGN_INPUT ')and
                   'button=High_Kick 'in line and int(re.search(r' frame=(\d+)',line)[1])in{r['frame']for r in fields}),None)
        if kick:
            for label,changed in (
                ('missing_actual_highkick',log.replace(kick+'\n','',1)),
                ('wrong_actual_attack',log.replace(kick,kick.replace('button=High_Kick','button=Low_Kick'),1))):
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
        actualShaoHighkickPolicyFields=len(fields),specificActualInputCounterexamples=negatives,
        rawAudioFilesWritten=0,newBuildsOrROMCopies=0,fullPortAcceptance=False)
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
