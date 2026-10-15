"""Complete actual sealed six-recording comparison, no additional boot.

5548 stopped before paired_observation because its call omitted the unused
guest argument. Preserve that failure. Every raw buffer was fully consumed,
validated and SHA256-bound by the actual capture; compare those authentic
whole-buffer records instead of pretending the discarded RAM still exists.
Retain original physical/pixel proofs and all packet/channel/timer criteria.
"""
import copy,datetime,json,re,traceback
from pathlib import Path
import current_baraka_audio_matrix_v5546 as matrix

ROOT,need,sha=matrix.ROOT,matrix.need,matrix.sha
PARENT=matrix.PARENT
FAILED=matrix.OUT/'progress.json'
BASE=matrix.BASE
OUT=ROOT/'audit_v5553_current_baraka_audio_records_progress'
rows=matrix.capture.rows


def gate(log,old,a,b,fighter,side):
    need(a['passed']and b['passed']and a['samplesEnabled']and not b['samplesEnabled'],
         'Actual correctly enabled/disabled native recordings passed original complete capture gates')
    for meta in(a,b):
        p=meta['process']
        need(p['player']==fighter and p['victim_slot']==side and p['winner_slot']==3-side
             and p['exit_code']==0 and p['candidate']==matrix.capture.original.model.current.NAME
             and p['executable_sha256']==matrix.capture.original.model.current.EXE_SHA
             and p['payload_sha256']==matrix.capture.original.model.current.PAYLOAD_SHA
             and p['killer']=='baraka'and p['command']=='bbbb_hp'and p['target_gap']==64
             and p['assistance']=='none'and not p['cheats_enabled']and p['entireOriginal921PhysicalControllerRetained']
             and meta['allRequestedGuestMediaBuffersRAMOnly']and len(meta['effectiveActualNativeRecordFaults'])==15
             and meta['actualNativeHeadBodyPixelsAndScanout']['everyEmittedOwnedHeadBodyAndLegitimateForegroundPixelExact'],
             'Each actual complete current true-ID/slot/controller/physical/raster execution context retained')
    selected=lambda s:[line for line in s.splitlines()if line.startswith(
        ('MK2_STOCK_HEAD_V921_','MK2_ROLLING_HEAD_V1003_','MK2_CURRENT_BARAKA_SCENE_'))]
    need(selected(log)==selected(old),'Whole original physical/parser/palette/FIFO/ordered display chronology on/off exact')
    streams=lambda s:[line for line in s.splitlines()if line.startswith('MK2_CURRENT_BARAKA_RAM_')]
    need(streams(log)and streams(log)==streams(old)and
         a['actualDisplayHeaders']==b['actualDisplayHeaders']and len(a['actualDisplayHeaders'])==125,
         'Every actual full RAM guest/GFX/palette/VRAM/RGB buffer digest and all125 whole displayed frames on/off exact')
    chunks=matrix.phase.pcm_rows(log);baseline=matrix.phase.pcm_rows(old)
    need(chunks==baseline and len(chunks)==a['actualPCMUpdates']==b['actualPCMUpdates']
         and sum(int(c['bytes'])for c in chunks)==a['actualPCMBytes']==b['actualPCMBytes']
         and a['actualMixedPCMSHA256']==b['actualMixedPCMSHA256'],
         'Every actual native PCM interval and whole joined in-RAM waveform byte hash on/off exact')
    matrix.phase.coverage(log,a);matrix.phase.coverage(old,b)
    for tag in('BEGIN','ROUTE','QUEUE','PACKET','SOUND','DELIVERY','RESULT'):
        need(rows(log,tag)==rows(old,tag),'Every actual native audio '+tag+' chronology on/off exact')
    begin=rows(log,'BEGIN');end=rows(log,'RESULT')
    actions=[r for tag,r in matrix.capture.original.model.original.records(log,'MK2_STOCK_HEAD_V921')if tag=='ACTION']
    need(len(begin)==len(end)==len(actions)==1,'One actual original physical/action/audio origin/terminal')
    action=actions[0];origin=int(begin[0]['origin'])
    need(begin[0]['id']=='3'and begin[0]['a8']==action['actor']and begin[0]['a13']==action['main']
         and begin[0]['frame']==action['frame']and end[0]['origin']==str(origin)and end[0]['frame']=='5198',
         'Audio origin and normal terminal belong to the genuine original Baraka winner task')
    channels=rows(log,'CHANNEL');disabled=rows(old,'CHANNEL')
    without_retained=lambda values:[{k:v for k,v in r.items()if k not in('length','pos')}for r in values]
    need(without_retained(channels)==without_retained(disabled)and all(r['length']=='0'and float(r['pos'])==0 for r in disabled),
         'All14 native imported channels idle on/off; disabled channels never obtain retained sample data')
    writes=rows(log,'SOUND');packets=rows(log,'PACKET');deliveries=rows(log,'DELIVERY')
    need(packets and len(writes)==2*len(packets)and [w['pc']for w in writes]==['FFA13C90','FFA13D60']*len(packets),
         'All native packets use exact original high/low port writer ordering')
    matched=[]
    for i,packet in enumerate(packets):
        high,low=writes[2*i:2*i+2];word=int(packet['a3'],16)
        need(0<=word<=65535 and tuple(int(w['word'],16)&255 for w in(high,low))==(word>>8,word&255)
             and float(packet['seconds'])<float(high['seconds'])<float(low['seconds'])
             and all(w['mask']=='FFFF'and all(w[k]==packet[k]for k in('a8','a13','frame'))for w in(high,low)),
             'Every whole actual native packet/actor/task reaches exact original two port bytes')
    for i,w in enumerate(writes):
        start=float(w['seconds']);end=float(writes[i+1]['seconds'])if i+1<len(writes)else start+.1
        hits=[d for d in deliveries if start<=float(d['seconds'])<end and int(d['word'],16)==int(w['word'],16)&255]
        need(hits,'Every actual native port byte consumed by ADSP before the following write')
        matched.append(dict(write=w,dspRead=hits[0]))
    return dict(passed=True,fighter=fighter,side=side,origin=origin,terminal=5198,
        fullNativePCMOnOffExactlyEqual=True,comparisonTransport='Authentic actual whole-buffer SHA256 and native chronological records; no fabricated or restored RAM',
        pairedWholeFramesExact=125,completeNativePCMUpdates=len(chunks),completeNativeStereoFrames=a['actualPCMBytes']//4,
        nativePortBytesDelivered=len(matched),actualDeliveredBytes=matched,
        allOriginalPhysicalAndExactPixelGatesRetained=True,allNativeQueueSuppressionCausesAccepted=False,
        sourceQualifiedNativeDCSWaveformAccepted=False,completeBarakaFinisherAudioAccepted=False,fullPortAcceptance=False)


def faults(log,old,a,b,fighter,side):
    positive=gate(log,old,a,b,fighter,side);out=[]
    def reject(label,left=log,right=old,ameta=a,bmeta=b):
        try:gate(left,right,ameta,bmeta,fighter,side)
        except ValueError as error:out.append(dict(label=label,rejectedBy=str(error)))
        else:raise ValueError('Accepted actual native paired-record counterexample '+label)
        need(gate(log,old,a,b,fighter,side)==positive,'Complete actual record positive restored after counterexample')
    def replace(tag,key,value):
        line=next(s for s in log.splitlines()if s.startswith('MK2_MAUDIO_'+tag+' '))
        changed,count=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(count==1 and changed!=line,'Effective actual paired native row mutation')
        return log.replace(line,changed,1),old.replace(line,changed,1)
    for label,tag,key,value in(('foreign original audio actor','BEGIN','a8','01000000'),
                              ('non-native packet writer','SOUND','pc','FFF00000'),
                              ('foreign native packet owner','PACKET','a8','01000000'),
                              ('wrong native port byte','SOUND','word','FFF7'),
                              ('looping imported channel','CHANNEL','loop','1')):
        left,right=replace(tag,key,value);reject(label,left,right)
    line=next(s for s in log.splitlines()if s.startswith('MK2_MAUDIO_CHANNEL '))
    reject('missing actual imported channel field',log.replace(line+'\n','',1),old.replace(line+'\n','',1))
    writes=rows(log,'SOUND');start=float(writes[0]['seconds']);end=float(writes[1]['seconds'])
    def omit(value):
        return '\n'.join(s for s in value.splitlines()if not(s.startswith('MK2_MAUDIO_DELIVERY ')and
            start<=float(dict(re.findall(r'(\w+)=([^\s]+)',s))['seconds'])<end))+'\n'
    reject('missing actual ADSP consumption',omit(log),omit(old))
    line=next(s for s in log.splitlines()if s.startswith('MK2_BBAUDIO_PCM_DIGEST '))
    reject('one actual native PCM interval differs',log.replace(line,re.sub(r'sha256=\S+','sha256='+'0'*64,line),1))
    damaged=copy.deepcopy(a);damaged['actualMixedPCMSHA256']='0'*64
    reject('whole joined native PCM differs',ameta=damaged)
    damaged=copy.deepcopy(a);damaged['actualDisplayHeaders'][0]['sha256']='0'*64
    reject('one whole actual displayed frame differs',ameta=damaged)
    need(len(out)==10,'All10 actual complete paired-record counterexamples rejected')
    return positive,out


def run():
    guest=matrix.capture.original.model.current.expected();parent=json.loads(PARENT.read_text());failed=json.loads(FAILED.read_text())
    need(parent['passed']and parent['goalStatus']=='active'and not failed['passed']and
         failed['error']=="TypeError(\"paired_observation() missing 1 required positional argument: 'guest'\")"
         and len(failed['completedNativeCaptures'])==6,'All six actual successful native captures retained; only unused comparison argument was missing')
    pins=dict(parent['newInputHashes']);pins[str(PARENT)]=sha(PARENT);pins[str(FAILED)]=sha(FAILED)
    cases=[]
    for fighter,side in(('kano',2),('sonya',1),('sonya',2)):
        folders=[BASE/f'{fighter}_p{side}_{suffix}'for suffix in('samples','nosamples')]
        metas=[json.loads((folder/'result.json').read_text())for folder in folders]
        logs=[(folder/'run.log').read_text()for folder in folders]
        for meta in metas:
            need(all(sha(p)==h for p,h in meta['process']['input_hashes'].items()),'Every actual execution input remains immutable')
            pins.update(meta['process']['input_hashes'])
        observed,paired_faults=faults(*logs,*metas,fighter,side);route_records=[]
        for suffix,log in zip(('samples','nosamples'),logs):
            positive,actual_faults=matrix.actual_route_faults(log,guest,fighter,side)
            need(len(actual_faults)==10,'Entire original actual source/voice/gender/queue/packet/port faults retained')
            route_records.append(dict(suffix=suffix,routes=positive,effectiveActualRouteFaults=actual_faults))
        cases.append(dict(passed=True,fighter=fighter,side=side,samplesResult=str(folders[0]/'result.json'),
            nosamplesResult=str(folders[1]/'result.json'),pairedNativeAudio=observed,effectiveActualPairedRecordFaults=paired_faults,
            sourceBoundVoiceEffectRoutes=route_records,entireOriginalPhysicalAndExactFourteenPartRasterGatesRetained=True,
            sourceQualifiedNativeDCSWaveformAccepted=False,fullPortAcceptance=False))
    for p in(Path(__file__),ROOT/'tools/inspect_current_baraka_audio_packets_v5551.py'):
        pins[str(p.resolve())]=sha(p)
    for p in BASE.rglob('*'):
        if p.is_file():pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Exact current/public/controller/source/evidence hashes unchanged')
    return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',remaining=parent['remaining'],
        parentAdditiveJournal=str(PARENT),previousGoalTurnClassification=parent['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: qualify all six actually completed remaining normal Baraka victim/slot recordings without replay; authentic whole-buffer hashes and full original physical/raster/timer/channel/packet/ADSP chronology,30 actual paired-record and60 actual source/gender/queue/port faults; preserve missing-unused-argument harness failure',
        cases=cases,retainedKanoP1Evidence=str(PARENT),newNativeBoots=6,newNativeBootsForQualifier=0,reusedPriorAcceptedNativeBoots=2,
        allNormalVictimSlotsNativeBarakaVoiceEffectAndPacketDeliveryAccepted=True,effectiveActualPairedRecordFaults=30,
        effectiveActualSourceRouteFaults=60,newBuilds=0,newDeletedFiles=0,publicPlayableChanged=False,refreshedReleaseZIP=False,
        requestedRawGuestGFXVRAMRGBPCMFilesWritten=0,allNativeQueueSuppressionCausesAccepted=False,
        sourceQualifiedNativeDCSWaveformAccepted=False,completeBarakaFinisherAudioAccepted=False,fullPortAcceptance=False,newInputHashes=pins,
        nextAction='Account and compact all eight native terminal records/automatic PNGs, then original DCS waveform/suppression fidelity and all other original remaining requirement groups.')


if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable authentic captured-record comparison')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir()
    if report['passed']:
        for case in report['cases']:matrix.capture.save(OUT/f"{case['fighter']}_p{case['side']}_paired.json",case)
    matrix.capture.save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','remaining','newInputHashes')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
