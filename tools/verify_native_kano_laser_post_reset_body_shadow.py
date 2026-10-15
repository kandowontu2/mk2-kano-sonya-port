"""All actual next-round body/shadow calls, same native control capture.

Whole original composite/FIFO/ROM-stream/projection/DMA contract retained.
The window is every actual resumed draw before the pre-render native exit.
Action-setter fields are proved by the actual store ledger, not relabeled
button markers or guessed routine entries. No visual/PCM/full-port inference.
"""
import copy
import inspect
import json
import traceback
from collections import defaultdict
from pathlib import Path
import verify_native_kano_laser_post_reset_controls_bound as controls
import verify_native_kano_laser_post_reset_controls_complete_fields as strict

ROOT,need,once,base,sha=controls.ROOT,controls.need,controls.once,controls.base,controls.sha
OUT=ROOT/'audit_native_kano_laser_post_reset_body_shadow_checked'


def load(actual):
    b,images=controls.load(actual)
    proof=json.loads((strict.OUT/'report.json').read_text())
    need(proof['passed']and len(proof['actualSemanticFaultsRejected'])==21 and
         all(sha(p)==h for p,h in proof['inputHashes'].items()),'Whole strict actual response/HP/native-store fault suite remains unchanged')
    state=proof['actualControls'];stores=proof['nativeControlStoreProvenance']
    first,last=state['round']['actualNativeResume'],state['round']['last']
    frames=set(range(first,last));rows=defaultdict(list)
    for tag in ('MK2_HPHASE_POST_FIELD','MK2_HPHASE_CANDIDATE','MK2_HPHASE_QUEUE',
                'MK2_HPHASE_SHADOW_BEGIN','MK2_HPHASE_PROJECTION','MK2_HPHASE_SHADOW_DMA'):
        rows[tag]=[r for r in b['rows'][tag]if int(r['frame'])in frames]
    need({(int(r['frame']),int(r['slot']))for r in rows['MK2_HPHASE_POST_FIELD']}=={(f,s)for f in frames for s in (1,2)}and
         len(rows['MK2_HPHASE_POST_FIELD'])==len(frames)*2,'Both actual complete post-reset draw fields; no fabricated terminal draw')
    b['rows']=rows
    used={f"{base.shadow.num(r,'graphic'):08X}_{r['width']}_{r['height']}_{base.shadow.num(r,'command'):04X}"
          for r in rows['MK2_HPHASE_PROJECTION']}
    all_streams=json.loads((b['folder']/'shadow_stream_memory_proofs.json').read_text())
    need(len({r['stream']for r in all_streams})==len(all_streams),'All actual captured static stream identities unique')
    b['streams']=[r for r in all_streams if r['stream']in used]
    need({r['stream']for r in b['streams']}==used,'Every and only actual next-round projected ROM stream retained')
    events=state['actualControls']
    flags=controls.mutation.pair.flag_rows(b['cpuLog'])
    setters=[r for r in flags if r['slot']==1 and r['kind']=='action'and r['after']==257 and
             events['jump']<r['frame']<events['punch']]
    need(len(setters)==1 and setters[0]['a8']==stores['owners']['1'][0]and setters[0]['a13']==stores['owners']['1'][1],
         'Exactly one actual own-Main native punch setter preceding the observed punch response')
    entries={stores['jumpNativeSetter']['frame'],setters[0]['frame']}
    need(entries<=frames,'Actual jump/punch setters lie in the full native draw window')
    return b,proof,entries,images


def binding(proof,entries):
    shadow=base.shadow
    source=inspect.getsource(shadow.check)
    start=source.index(' # The older physical/ownership/health checker')
    end=source.index(" fields=rows['MK2_HPHASE_POST_FIELD']",start)
    source=once(source,source[start:end]," state=qualified_state\n entry_frames=actual_setter_frames\n")
    source=once(source,"ids={side:identity,3-side:4}","ids={1:18,2:18}")
    source=once(source,"actualRoutineEntryFrames=sorted(entry_frames),entryBodyPublicationProven=True",
                "actualNativeActionSetterFrames=sorted(entry_frames),nativeActionSetterBodyPublicationProven=True")
    scope=dict(vars(shadow),qualified_state=proof['actualControls'],actual_setter_frames=entries)
    exec(compile(source,__file__+'::whole_original_complete_body_FIFO_ROM_projection_DMA_gate_next_round','exec'),scope)
    return scope['check']


def run(actual):
    need(not OUT.exists()and not base.identity.census(),'Same actual terminal gameplay; no native replay')
    b,proof,entries,images=load(actual);check=binding(proof,entries)
    positive=check(b,actual.guest,actual.payload,actual.gfx32)
    faults=[]
    mutations=[('native_action_setter_body_source_wrong','MK2_HPHASE_CANDIDATE','source','00000000'),
        ('shadow_owner','MK2_HPHASE_SHADOW_BEGIN','owner','01000000'),
        ('shadow_ineligible','MK2_HPHASE_SHADOW_BEGIN','body','0002'),
        ('projection_shift','MK2_HPHASE_PROJECTION','dx','999'),
        ('wrong_native_camera','MK2_HPHASE_PROJECTION','b4','00000000'),
        ('wrong_native_floor','MK2_HPHASE_PROJECTION','floor','999'),
        ('wrong_shadow_x','MK2_HPHASE_SHADOW_DMA','x','999'),
        ('wrong_shadow_pen','MK2_HPHASE_SHADOW_DMA','color','0101'),
        ('wrong_shadow_source','MK2_HPHASE_SHADOW_DMA','source','00000001')]
    for label,tag,key,value in mutations:
        changed=dict(b,rows=defaultdict(list,b['rows']))
        changed['rows'][tag]=[dict(r)for r in b['rows'][tag]]
        index=next(i for i,r in enumerate(changed['rows'][tag])if int(r['frame'])in entries)if label=='native_action_setter_body_source_wrong'else 0
        need(changed['rows'][tag][index][key]!=value,'Each native body/shadow fault genuinely changes actual evidence')
        changed['rows'][tag][index][key]=value
        try:check(changed,actual.guest,actual.payload,actual.gfx32)
        except(ValueError,AssertionError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual post-reset body/shadow fault accepted: '+label)
    for label in ('actual_rom_stream_wrong','packed_row_start_wrong'):
        changed=dict(b,streams=copy.deepcopy(b['streams']))
        if label=='actual_rom_stream_wrong':changed['streams'][0]['sha256']='0'*64
        else:changed['streams'][0]['actualRowStarts'][1]+=1
        try:check(changed,actual.guest,actual.payload,actual.gfx32)
        except(ValueError,AssertionError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Actual post-reset ROM stream fault accepted: '+label)
    # Entire composites and eligibility calls must reject omission, too.
    for tag in ('MK2_HPHASE_POST_FIELD','MK2_HPHASE_CANDIDATE','MK2_HPHASE_QUEUE',
                'MK2_HPHASE_SHADOW_BEGIN','MK2_HPHASE_PROJECTION','MK2_HPHASE_SHADOW_DMA'):
        changed=dict(b,rows=defaultdict(list,b['rows']));changed['rows'][tag]=b['rows'][tag][1:]
        try:check(changed,actual.guest,actual.payload,actual.gfx32)
        except(ValueError,AssertionError)as error:faults.append(dict(fault='missing_actual_'+tag,rejectedBy=str(error)))
        else:raise ValueError('Actual post-reset record omission accepted: '+tag)
    need(len(faults)==17 and check(b,actual.guest,actual.payload,actual.gfx32)==positive,
         'All original eleven plus six actual record-omission faults reject; whole positive restores')
    pins=dict(proof['inputHashes'])
    for p in (Path(__file__),Path(strict.__file__),Path(controls.__file__),Path(base.shadow.__file__),
              strict.OUT/'report.json',controls.OUT/'report.json',b['folder']/'shadow_stream_memory_proofs.json'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every actual executed source, compiled input and immutable proof preserved')
    OUT.mkdir();base.save(OUT/'report.json',dict(passed=True,candidate=b['report']['candidate'],actualPostResetBodyShadow=positive,
        actualSemanticFaultsRejected=faults,inputHashes=pins,gameplayReplayed=False,actualNativeRastersStillInRAM=len(images),
        fullPostResetRasterAcceptance=False,fullAudioAcceptance=False,allCPUContextsAccepted=False,fullPortAcceptance=False,
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False,goalStatus='active'))
    print(json.dumps(dict(passed=True,fields=positive['actualContiguousActorFields'],bodyParts=positive['actualNativeBodyCandidates'],
                         shadowCopies=positive['actualSourceBoundShadowCopies'],faults=len(faults),fullPortAcceptance=False)),flush=True)


def execute(actual):
    try:run(actual)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual post-reset body/shadow failure');OUT.mkdir()
        base.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False))
        print(json.dumps(dict(passed=False,error=repr(error))),flush=True)
