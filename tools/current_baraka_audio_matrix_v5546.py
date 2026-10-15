"""Extend qualified current Baraka audio to both victims and physical slots.

Reuse immutable actual Kano-P1 evidence; six new native recordings only.
Whole original physical/raster/PCM/packet gate, source-owned voice/effect
gate and full actual route faults remain; timer coverage is exact50Hz.
No game changes, new builds, raw media files or public promotion.
"""
import concurrent.futures,datetime,inspect,json,textwrap,traceback
from pathlib import Path
import current_baraka_audio_capture_v5533 as capture
import qualify_current_baraka_audio_phase_v5542 as phase
import verify_current_baraka_audio_routes_v5544 as source_model

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
PARENT=ROOT/'audit_v5545_current_baraka_audio_routes_qualified/progress.json'
BASE=ROOT/'audit_v5547_current_baraka_audio_matrix_ram'
OUT=ROOT/'audit_v5548_current_baraka_audio_matrix_progress'
LUA=ROOT/'mk2ks_current_baraka_audio_ram_v5536.lua'
COMPLETED=[]
capture.capture.__globals__.update(BASE=BASE,LUA=LUA,COMPLETED=COMPLETED)
source=inspect.getsource(capture.paired_observation)
before="""    need(int(hs[0]['frame'])in(origin,origin+1)and int(hs[-1]['frame'])==origin+749,
         'Whole original audio window through749fields, not truncated at animation completion')"""
after="    phase.coverage(a['log'],a['final']);phase.coverage(b['log'],b['final'])"
need(source.count(before)==1,'Only incorrect final-video-field assumption replaced by complete original50Hz timer coverage')
source=source.replace(before,after,1)
scope=dict(capture.__dict__,phase=phase)
exec(compile(source,__file__+'.entire5533_RAM_PCM_physical_and_all_native_packet_gate_exact_timer_coverage','exec'),scope)
paired=scope['paired_observation']

fault_source=inspect.getsource(source_model.prior.run)
first="        positive=gate(log,guest,'kano',1);faults=[]"
last="        cases.append(dict(suffix=suffix"
need(fault_source.count(first)==fault_source.count(last)==1,'Entire actual native route/source/packet fault suite boundaries')
body=textwrap.dedent(fault_source[fault_source.index(first):fault_source.index(last)])
need(body.count("gate(log,guest,'kano',1)")==2 and body.count("gate(log.replace(line,changed,1),guest,'kano',1)")==1,
     'Actual positive/fault/positive restoration, no hidden native context adaptation')
body=body.replace("gate(log,guest,'kano',1)",'gate(log,guest,fighter,side)')
body=body.replace("gate(log.replace(line,changed,1),guest,'kano',1)",'gate(log.replace(line,changed,1),guest,fighter,side)')
before="positive['actualNativeDeathVoice'][1],'entry','FFA123B0'"
after="positive['actualNativeDeathVoice'][1],'entry',('FFA122D0'if fighter=='sonya'else'FFA123B0')"
need(body.count(before)==1,'Effective opposite native gender branch for the actual true victim')
body=body.replace(before,after,1)
function='def actual_route_faults(log,guest,fighter,side):\n'+textwrap.indent(body,'    ')+'    return positive,faults\n'
fault_scope=dict(source_model.prior.__dict__,gate=source_model.gate)
exec(compile(function,__file__+'.entire5540_effective_actual_native_route_faults_both_true_victims_slots','exec'),fault_scope)
actual_route_faults=fault_scope['actual_route_faults']


def case(spec,guest,payload,gfx,reference,pins,image):
    fighter,side=spec
    a=capture.capture(spec,guest,payload,gfx,reference,pins,image,True)
    b=capture.capture(spec,guest,payload,gfx,reference,pins,image,False)
    observed=paired(a,b,fighter,side)
    routes=[]
    for suffix,record in(('samples',a),('nosamples',b)):
        positive,faults=actual_route_faults(record['log'],guest,fighter,side)
        need(len(faults)==10,'All actual source/voice/owner/table/queue/packet/port faults retained')
        routes.append(dict(suffix=suffix,routes=positive,effectiveActualRouteFaults=faults))
    result=dict(passed=True,fighter=fighter,side=side,samplesResult=str(a['folder']/'result.json'),
        nosamplesResult=str(b['folder']/'result.json'),pairedNativeAudio=observed,sourceBoundVoiceEffectRoutes=routes,
        entireOriginalPhysicalAndExactFourteenPartRasterGatesRetained=True,
        allNativeQueueSuppressionCausesAccepted=False,sourceQualifiedNativeDCSWaveformAccepted=False,fullPortAcceptance=False)
    capture.save(BASE/f'{fighter}_p{side}_paired.json',result)
    print(f'{fighter} P{side} entire actual native physical/raster/PCM/packet/source-owned death voice/blade and20route faults passed',flush=True)
    return result


def run():
    guest=capture.original.model.current.expected();parent=json.loads(PARENT.read_text())
    need(parent['passed']and parent['goalStatus']=='active'and parent['effectiveActualRouteFaults']==20,
         'Actual first current paired audio/source evidence and complete original scope retained')
    pins=dict(parent['newInputHashes']);pins[str(PARENT)]=sha(PARENT)
    for p in(Path(__file__),Path(phase.__file__),Path(source_model.__file__),Path(source_model.prior.__file__),LUA):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Exact current/public/source/asset/retained evidence before six native recordings')
    payload=(ROOT/capture.original.model.current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    reference,gfx=capture.original.model.source_art(guest,payload,pins)
    image=capture.original.transport.source_graphics(payload,pins)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:
        cases=list(pool.map(lambda spec:case(spec,guest,payload,gfx,reference,pins,image),[('kano',2),('sonya',1),('sonya',2)]))
    for p in BASE.rglob('*'):
        if p.is_file():pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Exact current/public/source/evidence unchanged after entire extended native matrix')
    return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
        remaining=parent['remaining'],parentAdditiveJournal=str(PARENT),previousGoalTurnClassification=parent['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: actual current both normal victims/both physical slots Baraka full native PCM/physical/exact14-part art/true voice gender/player/blade/table/selected queue/packet/port/ADSP matrix with original actual source faults; reused immutable first Kano-P1 pair and recorded remaining six native runs',
        retainedKanoP1Evidence=str(PARENT),cases=cases,allNormalVictimSlotsNativeBarakaVoiceEffectAndPacketDeliveryAccepted=True,
        newNativeBoots=6,reusedPriorAcceptedNativeBoots=2,newBuilds=0,newDeletedFiles=0,publicPlayableChanged=False,
        refreshedReleaseZIP=False,requestedRawGuestGFXVRAMRGBPCMFilesWritten=0,
        allNativeQueueSuppressionCausesAccepted=False,sourceQualifiedNativeDCSWaveformAccepted=False,
        completeBarakaFinisherAudioAccepted=False,fullPortAcceptance=False,newInputHashes=pins,
        nextAction='Account all six native terminal screenshots/text and qualify original DCS waveforms and omitted native queue branches; continue original full finisher/arena/CPU/campaign/UI requirements.')


if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable extended current native audio matrix')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completedNativeCaptures=COMPLETED,
        goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();capture.save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','completedNativeCaptures','remaining','newInputHashes')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
