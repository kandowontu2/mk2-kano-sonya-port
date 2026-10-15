"""Actual current original three-slot priority/suppression decisions.

One real Kano-P1 run, whole qualified physical/art/PCM capture retained.
Compare every observed dispatcher call to immutable original ROM/TMS borrow
semantics and real pre-call mute/header/slot state. No injected sound words,
proxies, state writes, new builds or raw buffer files.
"""
import datetime,json,re,struct,traceback
from pathlib import Path
import current_baraka_audio_capture_v5533 as capture
import verify_current_baraka_audio_routes_v5544 as routes
import qualify_current_baraka_audio_phase_v5542 as phase

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
PARENT=ROOT/'audit_v5550_current_baraka_audio_matrix_qualified/progress.json'
BASE=ROOT/'audit_v5556_current_baraka_priority_ram'
OUT=ROOT/'audit_v5557_current_baraka_priority_progress'
LUA=ROOT/'mk2ks_current_baraka_priority_ram_v5554.lua'
COMPLETED=[]
capture.capture.__globals__.update(BASE=BASE,LUA=LUA,COMPLETED=COMPLETED)
off=lambda address:(address-0xff800000)//8


def rows(log,tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)',s))for s in log.splitlines()if s.startswith('MK2_BPRIO_'+tag+' ')]


def decision(call,guest):
    code=int(call['command'],16);table=(0xffa0ef20+((code<<5)&0xffffffff))&0xffffffff
    need(call['entry']=='FFA12530'and int(call['a0'],16)==code and int(call['table'],16)==table,
         'Actual original command register and32-bit native table address exact')
    if int(call['mute'],16):return dict(kind='muted',end='FFA13DE0',slot=None)
    if table>=0xffa10ee0:return dict(kind='outside original command table',end='FFA12B90',slot=None)
    need(table>=0xffa0ef20,'No unsupported unsigned-underflow native command table')
    header,base=struct.unpack_from('<HH',guest,off(table))
    need(int(call['header'],16)==header and int(call['base'],16)==base,'Whole actual command header/base packet source exact')
    if not header:return dict(kind='empty original command',end='FFA12B90',slot=None)
    need(not header&0x8000,'Do not relabel complex native player-specific dispatch as a simple priority slot')
    priority=header>>8;current=[int(call[f'priority{i}'],16)for i in range(3)]
    slot=None
    if priority==0x71:slot=next((i for i,p in enumerate(current)if p==0x71),None)
    if slot is None:slot=next((i for i,p in enumerate(current)if p==0),None)
    # Native CMP A0,A1 computes requested-current; SET_C_SUB records unsigned
    # borrow(current>requested). JRNC accepts requested>=current, in slot order.
    if slot is None:slot=next((i for i,p in enumerate(current)if priority>=p),None)
    if slot is None:return dict(kind='all native slots higher priority',end='FFA129D0',slot=None,priority=priority,current=current)
    return dict(kind='original selected priority slot',end='FFA12B90',slot=slot,priority=priority,
        duration=header&255,base=base,packet=base+slot,current=current)


def gate(log,guest):
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for first,last in((0xffa0ef20,0xffa10ee0),(0xffa12530,0xffa12bd0)):
        need(guest[off(first):off(last)]==stock[off(first):off(last)],'Entire original command table and priority selection/return code')
    calls=rows(log,'CALL');ends=rows(log,'END');queues=rows(log,'QUEUE');results=[]
    need([int(c['serial'])for c in calls]==list(range(1,len(calls)+1))and len(ends)==len(calls)>10,
         'Every actual original dispatcher call has an ordered serial and observed completion')
    for call in calls:
        serial=call['serial'];end=[e for e in ends if e['serial']==serial];queue=[q for q in queues if q['serial']==serial]
        need(len(end)==1 and all(end[0][k]==call[k]for k in('a8','a13')),'Actual native command decision owner/task completes')
        expected=decision(call,guest);need(end[0]['entry']==expected['end'],'Actual native suppression/selection terminal branch source exact')
        if expected['slot']is None:
            need(not queue and end[0]['queued']=='00000000','Correct native suppression never creates a priority queue')
        else:
            entry=('FFA12A10','FFA12A80','FFA12B00')[expected['slot']]
            need(len(queue)==1 and queue[0]['entry']==end[0]['queued']==entry
                 and all(queue[0][k]==call[k]for k in('a8','a13','frame'))
                 and int(queue[0]['a1'],16)==expected['priority']and int(queue[0]['a4'],16)==expected['duration']
                 and int(queue[0]['a3'],16)==expected['base'],
                 'Actual selected original slot/priority/duration/base registers agree with complete pre-call snapshot')
        results.append(dict(actualCall=call,actualCompletion=end[0],expectedOriginalDecision=expected))
    terminal=rows(log,'RESULT')
    need(len(terminal)==1 and terminal[0]['frame']=='5198'and terminal[0]['calls']==str(len(calls))and terminal[0]['pending']=='0',
         'All actual command calls retired at real native5198 terminal')
    need(any(r['expectedOriginalDecision']['kind']=='all native slots higher priority'for r in results)
         and any(r['expectedOriginalDecision']['kind']=='outside original command table'for r in results),
         'Actual blocked-head-cue and out-of-table pose-marker branches really exercised')
    return dict(passed=True,calls=results,actualCalls=len(calls),suppressedCalls=sum(r['expectedOriginalDecision']['slot']is None for r in results),
        nativeDirectUnboundQueueRows=len(rows(log,'UNBOUND_QUEUE')),allCapturedOriginalDispatcherDecisionsAccepted=True,
        allNativeDirectMusicOrComplexDispatchAccepted=False,allVictimSlotsAccepted=False,sourceQualifiedNativeDCSWaveformAccepted=False,
        completeBarakaFinisherAudioAccepted=False,fullPortAcceptance=False)


def run():
    guest=capture.original.model.current.expected();parent=json.loads(PARENT.read_text())
    need(parent['passed']and parent['goalStatus']=='active','Complete original both-victim/slot audio frontier retained')
    pins=dict(parent['newInputHashes']);pins[str(PARENT)]=sha(PARENT)
    ops=ROOT/'mame-mkp/src/devices/cpu/tms34010/34010ops.hxx';source=ops.read_text()
    need('int32_t r = *rd - *rs;'in source and '#define SET_C_SUB(a,b)        SET_C_LOG((uint32_t)(b) > (uint32_t)(a))'in source,
         'Original TMS destination-source CMP and unsigned borrow carry semantics')
    for p in(Path(__file__),LUA,ops):pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All current/public/source/evidence stable before one physical native capture')
    payload=(ROOT/capture.original.model.current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    reference,gfx=capture.original.model.source_art(guest,payload,pins);image=capture.original.transport.source_graphics(payload,pins)
    record=capture.capture(('kano',1),guest,payload,gfx,reference,pins,image,True)
    positive=gate(record['log'],guest);phase.coverage(record['log'],record['final']);routes.gate(record['log'],guest,'kano',1)
    old=json.loads((ROOT/'audit_v5538_current_baraka_audio_ram/kano_p1_samples/result.json').read_text())
    need(record['final']['actualDisplayHeaders']==old['actualDisplayHeaders']and
         record['final']['actualMixedPCMSHA256']==old['actualMixedPCMSHA256']and record['final']['actualPCMBytes']==old['actualPCMBytes'],
         'Every original125 whole raster and complete native audio unchanged by additional passive priority snapshots')
    return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',remaining=parent['remaining'],
        parentAdditiveJournal=str(PARENT),previousGoalTurnClassification=parent['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: actual original dispatcher priority/empty/out-of-table/occupied-slot decisions from read-only pre-call mute/header/three-priority-slot snapshots; original ROM and TMS borrow semantics independently bind selection or suppression; one real current Kano-P1 Baraka capture retains whole physical/raster/PCM/source voice gates and exact old125-frame/whole-audio nonperturbance',
        actualPriority=positive,nativeCaptureResult=str(record['folder']/'result.json'),newNativeBoots=1,newBuilds=0,newDeletedFiles=0,
        publicPlayableChanged=False,refreshedReleaseZIP=False,requestedRawGuestGFXVRAMRGBPCMFilesWritten=0,
        allNativeQueueSuppressionCausesAccepted=False,sourceQualifiedNativeDCSWaveformAccepted=False,
        completeBarakaFinisherAudioAccepted=False,fullPortAcceptance=False,newInputHashes=pins,
        nextAction='Fault-test actual priority/owner/terminal snapshots and account native timed-exit PNG; extend original direct/complex dispatch and both victims/slots, original waveform fidelity, then all remaining original requirement groups.')


if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable native priority/suppression evidence')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completedNativeCaptures=COMPLETED,
        goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();capture.save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items()if k not in('actualPriority','completedNativeCaptures','remaining','newInputHashes')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
