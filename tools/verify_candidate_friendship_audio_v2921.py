"""Candidate2753 full captured Friendship PCM/tails/overlap, both human slots.

Cold physical inputs and earned wins only. Reuse unchanged v791 fidelity
thresholds and v2672 actual PCM counterexamples. Whole guest/payload must match
independent source assembly. Original hardware-only DCS references are an audio
oracle, never substituted for native gameplay. No universal finisher acceptance.
"""
import copy
import json
import re
import struct
import traceback
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly
import verify_current_friendship_audio_v2672 as audio
from run_candidate_friendship_audio_dispatch_v2918 import leaf

ROOT=assembly.ROOT
OUT=ROOT/'audit_v2922_candidate_friendship_audio_checked'
need=assembly.need
scene=audio.scene
native=audio.native

def verify():
    pins={};cases={};negatives={};variants=set()
    def pin(path,wanted=None):
        path=Path(path)
        path=(path if path.is_absolute() else ROOT/path).resolve()
        key=str(path)
        if key in pins:
            need(wanted is None or pins[key]==wanted,'Consistent immutable audio dependency '+key)
            return
        actual=assembly.sha(path)
        need(wanted is None or actual==wanted,'Unchanged actual audio dependency '+key)
        pins[key]=actual
    for file,wanted in assembly.source_check().items():pin(file,wanted)
    guest,old,payload,ends,ranges=assembly.expected()
    buildpath=ROOT/assembly.NAME/'build-info.json';pin(buildpath)
    build=json.loads(buildpath.read_text(encoding='utf-8-sig'))
    need(build['name']==assembly.NAME and build['expected_guest_sha256']=='65CE02355CD6B2830F4635FF1B8D55C1D0D22BA22E37ECF17B820DF26DA020E7','Exact isolated candidate')
    pin(ROOT/assembly.NAME/'mkport_candidate.exe','F7CE88667B33BA8AB7316F3C254B3B75A7A23ACA8C78524BB08B6E6055B90650')
    pin(ROOT/assembly.NAME/'roms/mk2ks/mk2ks.mdata',build['payload_sha256'])
    need((ROOT/assembly.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()==payload,'Independent whole payload reconstruction')
    for file,wanted in build['input_hashes'].items():pin(file,wanted)
    stockpath=ROOT/'mk2/mk2-maincpu.bin';pin(stockpath,'45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23')
    stock=stockpath.read_bytes();off=lambda a:(a-0xff800000)//8
    need(guest[0xf98a0:0xf98a0+68]==stock[off(0xff880a70):off(0xff880a70)+68] and
         guest[0xf98f0:0xf98f0+68]==stock[off(0xff880d90):off(0xff880d90)+68],'All seventeen original Friendship command/action rows retained')
    oldrunner=(ROOT/'tools/run_current_friendship_v2650.ps1').read_text()
    newrunner=(ROOT/'tools/run_candidate_friendship_audio_v2917.ps1').read_text()
    need(newrunner==oldrunner.replace(assembly.prior.NAME,assembly.NAME),'Only runner candidate changed; no physical/timing/cheat switches changed')
    for name,wanted in (
        ('mk2ks_native_friendship_probe_v784.lua','7B8F9CB538175410B93AF1D98783A25878A9E28A1CB7E94066F0F4EB1D553450'),
        ('mk2ks_native_friendship_audio_v790.lua','8D461B5BC7C100C207E1C7F0082747CE77B5A11274FFBACBE48477E05679DA73'),
        ('tools/verify_native_friendship_dispatch_v778.py','F2AC088DBAE1C228820D1501E89E1F8E4B09798C9409AAB7CF74A1FE65A69139')):pin(ROOT/name,wanted)
    for name in ('mk2ks_current_friendship_wins_v2651.lua','mk2ks_native_friendship_audio_v790.lua','mk2ks_native_friendship_probe_v784.lua'):
        pin(ROOT/name)
        need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',(ROOT/name).read_text()),'Physical buttons and read-only observers only')
    templates,assets=audio.original_templates(pin)
    def matched(fighter,side,command,quiet):
        folder=ROOT/leaf(fighter,side,command,quiet)
        result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        before=json.loads((folder/'inputs_before.json').read_text(encoding='utf-8-sig'))
        need(result['exit_code']==0 and result['candidate']==assembly.NAME and result['winner']==fighter and
             result['side']==side and result['command_case']==command and result['samples_enabled']==(not quiet) and
             result['guest_writes']==0 and result['assistance']=='none' and
             result['executable_sha256']==build['executable_sha256'] and result['payload_sha256']==build['payload_sha256'] and
             result['input_hashes']==before,'Terminal matched candidate physical capture '+folder.name)
        need(all(before.get(p)==h for p,h in build['input_hashes'].items()),'Every compiled input tracked unchanged')
        for file,wanted in before.items():
            pin(file,wanted)
            if Path(file).suffix in ('.lua','.ps1','.json'):pin(folder/'input_sources'/Path(file).name,wanted)
        need((folder/'guest_maincpu.bin').read_bytes()==guest,'Complete actual native guest independently source reconstructed')
        pin(folder/'native_mix.wav',result['mix_sha256'])
        for name in ('result.json','inputs_before.json','guest_maincpu.bin','run.log'):pin(folder/name)
        need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|exception at',(folder/'run.log').read_text(encoding='utf-8-sig'),re.I),'No observer/runtime errors')
        return folder,scene.previous.parse(folder/'run.log')
    for fighter in ('kano','sonya'):
        for side in (1,2):
            key=f'{fighter}_p{side}'
            positive,rows=matched(fighter,side,'positive',False)
            quiet,quiet_rows=matched(fighter,side,'positive',True)
            audio.baselines.exact(rows,quiet_rows)
            control=scene.check(rows,fighter,side)
            need(scene.check(quiet_rows,fighter,side)==control,'Unchanged actual silent-control native scene')
            baseline_units=[]
            for tag in ('WIN','DAMAGE','AUDIO'):
                changed=copy.deepcopy(quiet_rows);at=next(i for i,(t,r)in enumerate(changed)if t==tag)
                if tag=='WIN':changed.pop(at)
                elif tag=='DAMAGE':changed[at][1]['after']=str(int(changed[at][1]['after'])-1)
                else:changed[at][1]['frame']=str(int(changed[at][1]['frame'])+1)
                need(changed!=quiet_rows,'Nonvacuous actual baseline mutation')
                baseline_units.append(audio.reject(lambda:audio.baselines.exact(rows,changed),'baseline_'+tag,('Every actual physical input',)))
            chronology=native.runtime(rows,fighter,side,'positive')
            a=native.audio(positive/'native_mix.wav');b=native.audio(quiet/'native_mix.wav')
            need(a.shape==b.shape,'Exact paired full PCM duration')
            delta=a-b;cues=scene.previous.select(rows,'AUDIO')
            others=[(round(float(v['seconds'])*48000),native.existing_sample(ROOT,int(v['command'],16)))for v in scene.previous.select(rows,'VOICE')]
            groups=[];first_data=None;step=1 if fighter=='kano'else 3
            for first in range(0,len(cues),step):
                group=cues[first:first+step]
                commands=[0x6e if fighter=='kano'else(0xa5,0xaa,0xaf,0x96)[(int(c['command'],16)-0x6aa0)//5]for c in group]
                starts=[round(float(c['seconds'])*48000)for c in group];clips=[templates[c]for c in commands]
                fit=native.fit_overlap(delta,starts,clips,others)
                groups.append(dict(firstCue=first,commands=commands,startsPCM=starts,**fit));variants.update(commands)
                if first_data is None:first_data=(starts,clips,fit)
            pcm=audio.pcm_counterexamples(delta,*first_data[:2],others,first_data[2],templates,fighter)
            changed=copy.deepcopy(rows);at=next(i for i,(t,r)in enumerate(changed)if t=='AUDIO');changed[at][1]['id']='1'
            cue_units=[audio.reject(lambda:native.runtime(changed,fighter,side,'positive'),'proxy_audio_owner',('Audio belongs to wrong actor/task',))]
            changed=copy.deepcopy(rows)
            if fighter=='kano':
                changed[at][1]['frame']=str(int(changed[at][1]['frame'])+1);label='Pop is not at the native burst phase'
            else:
                changed[at][1]['command']=f"{int(changed[at][1]['command'],16)+1:04X}";label='Not original first-free independent voice allocation'
            cue_units.append(audio.reject(lambda:native.runtime(changed,fighter,side,'positive'),'incorrect_native_cue', (label,)))
            audio.baselines.exact(rows,quiet_rows)
            need(native.runtime(rows,fighter,side,'positive')==chronology,'Final unchanged actual native cue/voice control')
            cases[key]=dict(**chronology,audibleGroups=groups,PCMCorruptions=pcm,cueCorruptions=cue_units,
                baselineCorruptions=baseline_units,wholeNativeRecords=len(rows),existingAnnouncementEvents=len(others),
                nativeScene=control,finalUnmodifiedControlPassed=True)
            for command in ('wrong_command','punch_used'):
                folder,negative_rows=matched(fighter,side,command,False)
                restriction=audio.restrictions.check(negative_rows,fighter,side,command)
                negative=native.runtime(negative_rows,fighter,side,command)
                changed=copy.deepcopy(negative_rows)
                # Actual extra AUDIO cue must be rejected even if all native input/history stays valid.
                changed.append(('AUDIO',copy.deepcopy(cues[0])))
                unwanted=audio.reject(lambda:native.runtime(changed,fighter,side,command),'spurious_restricted_audio',('Friendship sound on rejected/ordinary gameplay',))
                need(audio.restrictions.check(negative_rows,fighter,side,command)==restriction and
                     native.runtime(negative_rows,fighter,side,command)==negative,'Final untouched physical restriction control')
                negatives[f'{fighter}_{command}_p{side}']=dict(**negative,nativeScene=restriction,audioCorruptions=[unwanted],finalUnmodifiedControlPassed=True)
            print(key+': full original waveform/tail/overlap and physical restrictions passed',flush=True)
    need(variants=={0x6e,0xa5,0xaa,0xaf,0x96},'Every original Friendship PCM variant exercised by actual native RNG')
    pin(ROOT/'mame-mkp/src/devices/sound/samples.cpp');pin(__file__)
    pin(ROOT/'tools/run_candidate_friendship_audio_v2917.ps1');pin(ROOT/'tools/run_current_friendship_v2650.ps1')
    pin(ROOT/'audit_v2919_candidate_friendship_audio_dispatch/report.json')
    scene.launch.module_pins(pins)
    for file,wanted in pins.items():need(assembly.sha(file)==wanted,'Final immutable dependency '+file)
    return dict(passed=True,candidate=assembly.NAME,cases=cases,physicalRestrictions=negatives,originalAssets=assets,
        actualPhysicalCaptures=16,audibleCues=sum(c['cues']for c in cases.values()),audibleGroups=sum(len(c['audibleGroups'])for c in cases.values()),
        actualAudioCounterexamplesRejected=sum(len(c['PCMCorruptions'])+len(c['cueCorruptions'])+len(c['baselineCorruptions'])for c in cases.values())+len(negatives),
        originalPCMAndAudibleOverlapAccepted=True,all20OriginalCluckChannelsReconstructed=True,
        currentWholeGuestAndPayloadReconstructed=True,samplesSettingNeverChangedGameplay=True,
        originalPhysicalStrategyUnchanged=True,inputHashes=pins,gameChanged=False,
        completeSceneRasterShadowAudioAccepted=False,allCPUOrMorphsAccepted=False,fullFinisherAcceptance=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Immutable fresh candidate audio proof')
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in ('inputHashes','cases','physicalRestrictions','originalAssets')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
