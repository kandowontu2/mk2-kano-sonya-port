"""Fresh extended native CPU source, paired phases and whole state/health ledgers.

Actual full guest reconstructed independently on candidate2753 and control1836.
Original selected-pair phase invariants retained. Every actual flag/action and
all-mode HP transition source-bound and replayed, without masking signatures,
unfinished pair entries, child effects or round changes. This is not complete
signature-move/child art/audio/CPU/KO/morph acceptance or public promotion.
"""
import hashlib
import json
import re
import struct
import traceback
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly
import native_extended_cpu_pair_contract_v2939 as pair
import verify_current_cpu_round_trace_v1900 as rounds
import verify_current_cpu_overlap_v1911 as overlap
import run_native_cpu_continuation_dispatch_v2936 as dispatch

ROOT=assembly.ROOT
OUT=ROOT/'audit_v2941_native_extended_cpu_checked'
need=assembly.need

def phase_contract_source():
    source=(ROOT/'tools/verify_physical_p2_cpu_pair_v1456.py').read_text()
    part=source[source.index('def _verify_log('):source.index('\n\ndef verify_ordinary_followup')]
    part=part.replace('def _verify_log(log,player):','def verify_pair(log,player,selected_cycle,guest):')
    part=part.replace('    need(not re.search(',"    all_complete=complete\n    complete=[r for r in all_complete if r['cycle']==selected_cycle]\n    need(not re.search(")
    part=part.replace("results[0].get('schema')==8","results[0].get('schema')==9").replace('Schema 8 original pair and first actual follow-up regain required','Schema 9 actual extended CPU match required')
    before="    follow=verify_ordinary_followup(log,entry,done,fields,flags,results[0],need)\n    verify_cpu_flag_ledger(entry,fields,flags,results[0],need)\n    need(results[0]['complete']==end and results[0]['cycles']==len(entries),'Terminal observation declares exact actual completed cycle')"
    after="    follow=dict(kind='not_ordinary_followup_acceptance',accepted=False)\n    # This is the original paired-contact contract, not a substitute for a\n    # later ordinary/signature/KO branch. Whole-stream ledgers are independent.\n    need(results[0]['complete']==all_complete[-1]['frame'] and results[0]['cycles']==len(entries),'Terminal observation declares exact actual final completed cycle')"
    need(before in part,'Original entire paired phase function before scoped API adaptation')
    part=part.replace(before,after)
    actual=Path(pair.__file__).read_text();actual=actual[actual.index('def verify_pair('):]
    need(actual.rstrip()==part.rstrip(),'Every original paired-contact/phase/damage/individual-cleanup invariant retained byte-for-byte')

def health_ledger(log,guest,player):
    begin=rounds.rows(log,'BEGIN');end=rounds.rows(log,'RESULT')
    need(len(begin)==len(end)==1,'One all-mode native match window')
    first,last=begin[0]['frame'],end[0]['frame']
    fields=rounds.rows(log,'FIELD');by={(r['frame'],r['slot']):r for r in fields}
    need(last-first==1800 and len(fields)==len(by)==3602 and set(by)=={(f,s)for f in range(first,last+1)for s in (1,2)},'Every all-mode physical callback, no omitted round or transition fields')
    expected_ids=f'{pair.HUMANS[player]},18'
    for row in [*begin,*fields,*end]:
        need(row['writes']==0 and row['assistance']=='none' and row['ids']==expected_ids and row['stage']==0 and row['schedule']==0xfffa3180,'Actual original-derived Sonya stage-zero tower and unchanged true roster')
        if 'actor'in row and row['mode']==2 and row['states']=='1,0':
            need(row['valid']==1 and row['owner']==row['actor'] and row['id']==(18 if row['slot']==2 else pair.HUMANS[player]),'All live physical slots retain actual native owner/identity')
    stores=rounds.rows(log,'HEALTH')
    for row in stores:
        need(row['writes']==0 and row['assistance']=='none' and row['mask']==65535 and row['at']==(0x010602f0 if row['slot']==1 else 0x01060ec0),'Physical original health writer, full field mask')
        at=(row['pc']-48-0xff800000)//8
        need(0<=at<len(guest)-6 and struct.unpack_from('<3H',guest,at)==tuple(row[f'op{i}']for i in range(3)),'Every actual health store instruction source-bound to whole actual guest')
        ordinary=0<=row['before']<=161 and 0<=row['after']<=161
        sentinel=row['mode']==7 and ((row['pc']==(0xff9dece0 if row['slot']==1 else 0xff9ded10)and(row['before'],row['after'])==(161,65535))or
            (row['pc']==(0xff9def40 if row['slot']==1 else 0xff9def70)and(row['before'],row['after'])==(65535,4)))
        need(ordinary or sentinel,'Only original mode7 fill sentinel, not invalid live health')
        if row['mode']==2 and row['before']>row['after']:need(row['pc']==0xff836700,'Every live collision damage uses original health routine')
    for slot in (1,2):
        grouped={}
        for row in stores:
            if row['slot']==slot:grouped.setdefault(row['frame'],[]).append(row)
        for frame in range(first,last):
            hp=by[frame,slot]['hp']
            for row in grouped.get(frame,[]):
                need(row['before']==hp,'Complete ordered original same-field health chain')
                hp=row['after']
            need(by[frame+1,slot]['hp']==hp,'Every all-mode callback agrees with full original health store history')
    kos=[r for r in stores if r['mode']==2 and r['before']>0 and r['after']==0]
    resets=[r for r in stores if r['mode']==6 and r['after']==161 and r['pc']in (0xff825930,0xff825960)]
    return dict(first=first,last=last,allModePhysicalFields=len(fields),nativeHealthStores=len(stores),earnedKOs=kos,actualRoundResets=resets,roundResetAcceptance=bool(resets)),by

def state_ledgers(log,guest,player,round_by):
    fields=pair.rows(log,'FIELD');flags=pair.flag_rows(log)
    need(fields and len({r['frame']for r in fields})==len(fields),'Unambiguous complete live native state stream')
    known={}
    for row in fields:
        need(row['writes']==0 and row['assistance']=='none' and (row['cpu_slot'],row['human_slot'])==(2,1) and
             (row['id'],row['roster'],row['vid'],row['vroster'],row['state'],row['vstate'],row['mode'])==(18,18,pair.HUMANS[player],pair.HUMANS[player],0,1,2) and
             row['owner']==row['actor'] and row['vowner']==row['vactor'],'True live physical CPU/human roles and ownership')
        for slot,prefix in ((2,''),(1,'v')):
            native=round_by[row['frame'],slot]
            for key in ('actor','main','owner','id','action','floor','vx','vy','gravity','flags','body','trail','hp'):
                need(row[prefix+key]==native[key],'Independent all-mode and live actor/Main/health/state streams agree')
            if row[prefix+'hp']>0:
                need(row[prefix+'floor']==row['stage_floor']-(135 if row[prefix+'id']==18 else 134),'Original living Main floor anchor across every repeated pair/followup')
        known[row['frame']]=row
    for row in flags:
        need(row['writes']==0 and row['assistance']=='none' and row['slot']in (1,2),'Every native state store declares physical scope')
        at=(row['pc']-32-0xff800000)//8
        need(0<=at<len(guest)-4 and struct.unpack_from('<2H',guest,at)==(row['op0'],row['op1']),'Every native state store matches actual original or source-assembled authored instruction')
        need(row['at']==(row['actor']+0x160 if row['kind']=='body'else row['main']+(0x210 if row['kind']=='flags'else 0x1f0)),'Actual store targets its observed owned object/Main field')
    transitions=0
    for slot,prefix in ((2,''),(1,'v')):
        for kind in ('body','flags','action'):
            grouped={}
            for row in flags:
                if row['slot']==slot and row['kind']==kind:grouped.setdefault(row['frame'],[]).append(row)
            for frame,row in known.items():
                if frame+1 not in known:continue
                nextrow=known[frame+1]
                need((row[prefix+'actor'],row[prefix+'main'])==(nextrow[prefix+'actor'],nextrow[prefix+'main']),'No unobserved live Main reuse across native state ledger')
                current=row[prefix+kind]
                for store in grouped.get(frame,[]):
                    need(store['before']==current and (store['actor'],store['main'])==(row[prefix+'actor'],row[prefix+'main']), 'Full ordered physically owned '+kind+' store chain')
                    current=store['after'];transitions+=1
                need(nextrow[prefix+kind]==current,'Every raw live '+kind+' callback matches complete source-bound state history')
    return dict(liveFields=len(fields),sourceBoundStateStores=len(flags),replayedStateStores=transitions,allRawLiveStateChangesSourceBound=True)

def verify():
    pins={};cases={}
    def pin(path,wanted=None):
        path=Path(path);path=(path if path.is_absolute()else ROOT/path).resolve();key=str(path)
        actual=assembly.sha(path)
        need(wanted is None or actual==wanted,'Immutable actual extended CPU input '+key)
        need(key not in pins or pins[key]==actual,'Consistent actual dependency '+key);pins[key]=actual
    phase_contract_source()
    for file,wanted in assembly.source_check().items():pin(file,wanted)
    guest,old,payload,_,_=assembly.expected()
    runner=(ROOT/'tools/run_native_cpu_continuation_guest_v2935.ps1').read_text()
    expected=(ROOT/'tools/run_current_physical_p2_cpu_continuation_v2000.ps1').read_text().replace('$root/mk2ks_physical_p2_cpu_overlap_trace_v1999.lua")',
        '$root/mk2ks_physical_p2_cpu_overlap_trace_v1999.lua","$root/mk2ks_native_cpu_continuation_guest_v2934.lua","$root/mk2/mk2-maincpu.bin")').replace(
        '-autoboot_script "$root/mk2ks_physical_p2_cpu_overlap_trace_v1999.lua"','-autoboot_script "$root/mk2ks_native_cpu_continuation_guest_v2934.lua"')
    need(runner.rstrip()==expected.rstrip(),'Entire physical driver unchanged except read-only whole guest capture')
    for build,player in dispatch.CASES:
        candidate=assembly.NAME if build=='new'else assembly.prior.NAME
        actual_guest=guest if build=='new'else old
        folder=ROOT/f'audit_v2938_native_cpu_continuation_{build}_human_{player}'
        meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
        bp=ROOT/candidate/'build-info.json';info=json.loads(bp.read_text(encoding='utf-8-sig'));pin(bp)
        need(meta['exit_code']==0 and meta['candidate']==candidate and meta['player']==player and meta['assistance']=='none' and
             not meta['cheats_enabled'] and (meta['cpu_slot'],meta['human_slot'])==(2,1) and meta['confirm_age']==264 and
             meta['policy']=='retreat' and meta['boot_frame']==(613 if build=='new'else 604)and
             meta['approach']==('original'if build=='new'else 'guard_until_close')and before==meta['input_hashes'],'Terminal actual cold input-only fixture')
        need(meta['executable_sha256']==info['executable_sha256'] and meta['payload_sha256']==info['payload_sha256'] and
             all(before.get(file)==wanted for file,wanted in info['input_hashes'].items()),'All original compiled and runtime dependencies captured unchanged')
        pin(ROOT/candidate/'mkport_candidate.exe',info['executable_sha256']);pin(ROOT/candidate/'roms/mk2ks/mk2ks.mdata',info['payload_sha256'])
        need((folder/'guest_maincpu.bin').read_bytes()==actual_guest and (ROOT/candidate/'roms/mk2ks/mk2ks.mdata').read_bytes()==payload,'Whole actual guest and payload independently reconstructed')
        for file,wanted in before.items():
            pin(file,wanted)
            if Path(file).suffix in ('.lua','.ps1','.json'):pin(folder/'input_sources'/Path(file).name,wanted)
            if Path(file).suffix=='.lua':need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|:reset\(',Path(file).read_text()),'No state/CPU/health/stage/RNG/register injection')
        log=(folder/'run.log').read_text(encoding='utf-8-sig')
        need(not re.search(r'LUA ERROR|fatal error|stack traceback|access violation',log,re.I),'No emulator/observer error')
        cold=pair.rows_prefix(log,'MK2_P2CPU_COLD_LIVE ');selection=pair.rows_prefix(log,'MK2_P2CPU_SELECT_RESULT ')
        need(len(cold)==len(selection)==1 and cold[0]['cpu_id']==selection[0]['initial_cpu']==18 and
             cold[0]['human_id']==selection[0]['human_id']==pair.HUMANS[player] and selection[0]['checks']==50 and selection[0]['errors']==0,'Actual natural Sonya CPU and true human selected normally')
        health,round_by=health_ledger(log,actual_guest,player)
        ledger=state_ledgers(log,actual_guest,player,round_by)
        completions=pair.rows(log,'COMPLETE');contracts=[]
        for done in completions:contracts.append(pair.verify_pair(log,player,done['cycle'],actual_guest))
        code=overlap.rows(log,'CODE')
        need(len(code)==5,'Every declared whole native code window captured')
        for row in code:
            lo,hi=((row[k]-0xff800000)//8 for k in ('start','stop'))
            words=[int(w,16)for w in row['words'].split(',')]
            need(struct.pack('<'+'H'*len(words),*words)==actual_guest[lo:hi],'All actual cleanup/guard/ready/projectile program words source-bound')
        events=overlap.rows(log,'EVENT');result=overlap.rows(log,'RESULT')
        need(len(result)==1 and result[0]['live_children']==0,'No live tracked projectile left at terminal observation')
        cases[f'{build}_{player}']=dict(case=folder.name,candidate=candidate,player=player,wholeGuestReconstructed=True,
            health=health,stateLedger=ledger,selectedPairContracts=contracts,
            acceptedSelectedPairs=sum(c['passed']for c in contracts),rejectedSelectedPairs=sum(not c['passed']for c in contracts),
            uncompletedOrMixedEntries=pair.rows(log,'INCOMPLETE'),
            moveEntries=[dict(frame=r['frame'],cycle=r['cycle'],kind=r['kind'])for r in events if r['kind']in ('leg','ring','bicycle','square','knife','choke')],
            projectileBirths=overlap.rows(log,'CHILD'),projectileRetirements=overlap.rows(log,'RETIRE'),
            fullSignatureOrChildPhaseAcceptance=False,allCPUAccepted=False)
        for path in folder.rglob('*'):
            if path.is_file():pin(path)
        print(folder.name+': every native state/health transition source-bound; selected pairs accepted='+str(cases[f'{build}_{player}']['acceptedSelectedPairs']),flush=True)
    mirror=cases['new_sonya']
    need(mirror['acceptedSelectedPairs']==3 and mirror['rejectedSelectedPairs']==0 and
         [c['held_fields']for c in mirror['selectedPairContracts']]==[46,46,46] and
         [c['damage']for c in mirror['selectedPairContracts']]==[35,35,35],'Three actual complete Sonya mirror leg pairs, every original phase/handoff retained')
    pin(__file__);pin(ROOT/'tools/run_current_physical_p2_cpu_continuation_v2000.ps1')
    pin(ROOT/'audit_v2937_native_cpu_continuation_dispatch/report.json')
    import sys
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools')and Path(file).suffix=='.py':pin(file)
    for file,wanted in pins.items():need(assembly.sha(file)==wanted,'Actual immutable extended source/capture '+file)
    return dict(passed=True,candidate=assembly.NAME,control=assembly.prior.NAME,cases=cases,
        actualPhysicalFixtures=4,allModePhysicalFields=sum(c['health']['allModePhysicalFields']for c in cases.values()),
        wholeNativeStateAndHealthLedgersAccepted=True,threeActualSonyaMirrorPairsAccepted=True,
        originalPairPhaseInvariantsRetained=True,ordinaryFollowupSubstituted=False,
        fullSignatureOrChildPhaseAcceptance=False,allCPUOrMorphsAccepted=False,allRoundsOrKOAccepted=False,
        gameChanged=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Immutable extended CPU proof')
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in ('inputHashes','cases')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
