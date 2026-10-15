"""Finite completed Sonya CPU legs; preserve all failed broader gates and raw RAM review.

No entire mixed-move, child, HP-context, native-body-shadow or release pass.
This journal records the exact next missing evidence: real extra actor/Main
ownership at one native damage event per actual Sonya trial.
"""
import hashlib
import json
import re
from pathlib import Path
import native_extended_cpu_pair_contract_v2939 as pair
import capture_native_kano_laser_cpu_leg_repeat_p2 as capture

ROOT,need,sha,base=capture.ROOT,capture.need,capture.sha,capture.base
OUT=ROOT/'audit_native_kano_laser_cpu_leg_diagnostic_review'
FIRST=ROOT/'audit_native_kano_laser_cpu_leg_first_diagnostic_review'
PRESSURE=[998,1174,1288,1816,1850,1880,1884,1888,1892,1944,1963,1993,1997,2001,2005,2019,2541,2571,2575,2579,2583]
GUARD=[998,1174,1288,1816,1914,1944,1948,1952,1956,2275,2305,2309,2313,2317,2369,2415,2537,2567,2571,2575,2579]


def visuals(owner,key,viewed):
    folder,text,images=owner.RAM_CASES[key];report=json.loads((folder/'result.json').read_text())
    need(not report['passed'] and report['nativeExit']==0 and not report['nativeTerminal']['hostDecodeErrors'],
         'Exact rejected but actually terminal native case')
    need([r['frame']for r in report['actualScenes']]==viewed and len(images)==len(viewed),
         'Every original captured raster individually reviewed')
    rows=[]
    for scene in report['actualScenes']:
        image=images[f"ui_{scene['frame']:04d}.png"]
        need(image.shape==(254,400,3),'Exact original unscaled RGB array')
        rows.append(dict(frame=scene['frame'],stage=scene['stage'],sourceRawBGRXSHA256=scene['sha256'],
                         nativeRGBSHA256=hashlib.sha256(image.tobytes()).hexdigest().upper(),individuallyViewed=True,
                         diagnosticOnly=True,fullGameplayAccepted=False))
    return folder,text,report,rows


def mutate(text,prefix,key,value,predicate):
    target=next(line for line in text.splitlines()if line.startswith(prefix+' ')and predicate(dict(re.findall(r'(\w+)=([^\s]+)',line))))
    changed=re.sub(r'(?<!\w)'+key+r'=[^\s]+',key+'='+str(value),target,count=1)
    need(changed!=target,'Actual typed-leg fault changes native observation')
    return text.replace(target,changed,1)


def run(actual,guarded):
    need(not OUT.exists() and not base.identity.census(),'Fresh journal of same actual terminal processes only')
    import verify_native_cpu_ring_v2971 as original_source
    original_source.phase_contract_source()
    pins={};cases=[];faults=[]
    for owner,key,viewed in ((actual,actual.KEY,PRESSURE),(guarded,guarded.KEY,GUARD)):
        folder,text,report,review=visuals(owner,key,viewed)
        need(all(sha(p)==h for p,h in report['inputHashes'].items()),'Every actual native input conserved')
        complete=pair.rows(text,'COMPLETE');need(len(complete)==1,'Exactly one actual full uninterrupted leg in this failed repeated trial')
        cycle=complete[0]['cycle'];proof=pair.verify_pair(text,'sonya',cycle,actual.guest)
        need(proof['passed'] and proof['held_fields']==46 and proof['damage']==35,'Entire unmodified original selected leg phases, damage and both owning ready handoffs')
        remove=lambda prefix,predicate:text.replace(next(line+'\n'for line in text.splitlines()if line.startswith(prefix+' ')and predicate(dict(re.findall(r'(\w+)=([^\s]+)',line)))),'',1)
        in_cycle=lambda r:r.get('cycle')==str(cycle)
        trials=[
            ('native_step_missing',remove('MK2_CPU_PAIR_EVENT',lambda r:in_cycle(r)and r['kind']=='step')),
            ('native_action_missing',remove('MK2_CPU_PAIR_ENTRY',in_cycle)),
            ('native_victim_ready_missing',remove('MK2_CPU_PAIR_VICTIM_REGAIN',in_cycle)),
            ('native_own_ready_busy',mutate(text,'MK2_CPU_PAIR_OWN_REGAIN','flags','00000010',in_cycle)),
            ('held_victim_pose_wrong',mutate(text,'MK2_CPU_PAIR_FIELD','vpose','00000000',lambda r:in_cycle(r)and r['vaction']=='273')),
            ('held_victim_offset_wrong',mutate(text,'MK2_CPU_PAIR_FIELD','vxpos','999',lambda r:in_cycle(r)and r['vaction']=='273')),
            ('native_damage_request_wrong',mutate(text,'MK2_CPU_PAIR_EVENT','a10','00000022',lambda r:in_cycle(r)and r['kind']=='damage')),
            ('native_paired_HP_store_wrong',mutate(text,'MK2_CPU_PAIR_HEALTH','after','1',lambda r:in_cycle(r)and r['before']!=r['after']and proof['start']<=int(r['frame'])<=proof['complete']))]
        for label,changed in trials:
            checked=pair.verify_pair(changed,'sonya',cycle,actual.guest)
            need(not checked['passed'] and checked['errors'],'Actual original typed-leg fault rejected: '+label)
            faults.append(dict(case=key,fault=label,rejectedBy=checked['errors']))
        need(pair.verify_pair(text,'sonya',cycle,actual.guest)==proof,'Entire original selected-leg positive restored')
        fields=pair.rows(text,'FIELD');by={r['frame']:r for r in fields}
        pending=[dict(frame=h['frame'],physicalSlot=h['slot'],before=h['before'],after=h['after'],
                      executingActor=hex(h['a8']),executingMain=hex(h['a13']),
                      actorMainOwnershipProven=False)
                 for h in pair.rows(text,'HEALTH')if h['a8']not in(by[h['frame']]['actor'],by[h['frame']]['vactor'])or
                 h['a13']not in(by[h['frame']]['main'],by[h['frame']]['vmain'])]
        need(len(pending)==1 and pending[0]['executingActor']=='0x1032d90' and pending[0]['executingMain']=='0x106d400',
             'Exact observed extra actor/Main gap, not arbitrary aliases accepted')
        cases.append(dict(key=key,selectedOriginalCompleteLeg=proof,extraDamageContextsPending=pending,
                          reviewedOriginalRasters=review,wholeRepeatedTrialStillRejected=True,
                          allHPContextsAccepted=False,allBodyShadowFieldsAccepted=False))
        pins.update(report['inputHashes'])
        for p in folder.rglob('*'):
            if p.is_file():pins[str(p.resolve())]=sha(p)
    for p in (Path(__file__),Path(pair.__file__),Path(original_source.__file__),ROOT/'tools/verify_physical_p2_cpu_pair_v1456.py',
              ROOT/'tools/verify_restart_pair.py',ROOT/'tools/verify_p2_campaign.py',
              ROOT/'audit_native_kano_laser_cpu_leg_owned_trace_checked/failure.json',
              ROOT/'audit_native_kano_laser_cpu_leg_render_inventory_checked/failure.json',
              actual.OUT/'failure.json',guarded.OUT/'failure.json'):
        pins[str(p.resolve())]=sha(p)
    need(len(faults)==16 and all(sha(p)==h for p,h in pins.items()),'All actual typed faults and conserved evidence')
    OUT.mkdir();base.save(OUT/'report.json',dict(passed=True,candidate=actual.native.NAME,cases=cases,inputHashes=pins,
        selectedOriginalCompletedLegs=2,actualTypedLegFaultsRejected=faults,individuallyReviewedOriginalRasters=42,
        wholeRepeatedTrialsStillRejected=True,extraDamageActorMainContextsPending=True,allHPContextsAccepted=False,
        allBodyShadowFieldsAccepted=False,allMixedMovesAccepted=False,fullAudioAcceptance=False,fullPortAcceptance=False,
        publicPlayableChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active',
        nextAction='Add original read-only all-cycle child allocation/fields/contact/retirement and guard observers; verify the exact extra native actor/Main ownership before accepting the mixed gameplay/HP/render trace. Keep all stronger rejections.',scope=__doc__))
    print('Two complete original CPU Sonya legs, 16 typed faults and 42 original visual frames verified; broader gates remain rejected.',flush=True)


def first_case(actual):
    need(not FIRST.exists(),'Fresh first-trial diagnostic review')
    key='leg_cpu_sonya_p1_human_kano_p2'
    folder,text,report,review=visuals(actual,key,[997,1013,1287,1815])
    cold=pair.rows_prefix(text,'MK2_P1CPU_COLD_LIVE ')
    need(len(cold)==1 and cold[0]['cpu_id']==3 and not pair.rows(text,'ENTRY'),'Actually selected Baraka, not a claimed CPU Sonya trial')
    pins=dict(report['inputHashes'])
    for p in (Path(__file__),folder/'result.json',folder/'run.log.gz',folder/'native_terminal.json'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'First actual diagnostic sources immutable')
    FIRST.mkdir();base.save(FIRST/'report.json',dict(passed=True,diagnosticOnly=True,actualCPU=3,CPUGrabAccepted=False,
        reviewedOriginalRasters=review,inputHashes=pins,fullPortAcceptance=False,publicPlayableChanged=False,newBuilds=0,newRawMedia=0,goalStatus='active'))
    print('Four original Baraka diagnostic rasters reviewed; no CPU Sonya gameplay acceptance.',flush=True)
