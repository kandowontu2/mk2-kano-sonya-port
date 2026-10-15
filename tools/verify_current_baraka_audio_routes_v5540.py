"""Source-bound current Baraka native death voice and blade effect delivery.

Qualify actual first paired observation without booting again. All original
physical/exact pixels remain separate required evidence. This does not claim
unobserved queue suppression, all victims, or source-qualified DCS waveforms.
"""
import datetime,json,re,struct,subprocess,traceback
from pathlib import Path
import current_baraka_audio_capture_v5533 as capture

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
PARENT=ROOT/'audit_v5531_current_baraka_qualified_progress/progress.json'
OBSERVED=ROOT/'audit_v5543_current_baraka_audio_phase_qualified/progress.json'
BASE=ROOT/'audit_v5538_current_baraka_audio_ram'
OUT=ROOT/'audit_v5541_current_baraka_audio_routes_progress'
rows=capture.rows
off=lambda address:(address-0xff800000)//8


def gate(log,guest,fighter,side):
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();identity=17 if fighter=='kano'else 18
    for first,last in((0xff8cb4a0,0xff8cb940),(0xffa0ef20,0xffa10ee0),(0xffa12070,0xffa122a0),
                       (0xffa122d0,0xffa12430),(0xffa12530,0xffa13df0)):
        need(guest[off(first):off(last)]==stock[off(first):off(last)],
             'Entire original native Baraka/voice/command-table/priority/packet-store source exact')
    need(struct.unpack_from('<HI',guest,off(0xffa12070))==(0x09e1,0x45464748),
         'Original whole native decapitation death-voice tuple')
    need(struct.unpack_from('<HI',guest,off(0xffa122a0))==(0xc080,0xff800000+(0xfe000+2*0x20)*8)
         and struct.unpack_from('<12H',guest,0xfe040)==
         (0x0b42,0xffef,0xca06,0x0b42,0xffed,0xca03,0xc080,0x22d0,0xffa1,0xc080,0x23b0,0xffa1),
         'Actual current native Sonya female extension preserves original Jade/male continuations')
    # MOVI44,A0 / CALLA native command dispatcher: independently original
    # instructions, not a command inferred from heard or emitted PCM.
    need(struct.unpack_from('<5H',guest,off(0xff8cb680))==(0x09c0,0x0044,0x0d5f,0x2530,0xffa1),
         'Original Baraka fixed blade effect callsite and command44')
    action=[r for tag,r in capture.original.model.original.records(log,'MK2_STOCK_HEAD_V921')if tag=='ACTION']
    need(len(action)==1,'One actual original physical Baraka fatality action');action=action[0]
    begin=rows(log,'BEGIN');need(len(begin)==1 and begin[0]['id']=='3'and begin[0]['a8']==action['actor']
         and begin[0]['a13']==action['main']and begin[0]['frame']==action['frame'],
         'Actual audio origin belongs to original Baraka winner task')
    voice=[r for r in rows(log,'ROUTE')if r['return_pc']=='FF842C50'and r['a8']==action['victim_actor']]
    gender='FFA123B0'if identity==18 else'FFA122D0';command=0x48 if identity==18 else(0x45 if side==1 else 0x46)
    need([r['entry']for r in voice]==['FFA12220',gender,'FFA123D0','FFA12530']and
         all(r['id']==str(identity)and r['a8']==r['owner']==action['victim_actor']and r['a13']==action['victim_main']for r in voice),
         'Entire actual true-victim decapitation death/gender/RNG/native command route')
    need(voice[0]['a0']==voice[1]['a0']==voice[2]['a0']=='00000001'and voice[0]['a1']==voice[1]['a1']=='45464748'
         and int(voice[2]['a1'],16)==int(voice[3]['a0'],16)==command,
         'Whole original packed native death tuple and exact true player/gender byte, one-choice RNG range')
    blades=[r for r in rows(log,'ROUTE')if r['entry']=='FFA12530'and r['return_pc']=='FF8CB6D0']
    need(len(blades)==1 and int(blades[0]['a0'],16)==0x44 and blades[0]['id']=='3'
         and blades[0]['a8']==blades[0]['owner']==action['actor']and blades[0]['a13']==action['main'],
         'Exact original fixed blade call belongs to native Baraka winner')
    calls=[r for r in rows(log,'ROUTE')if r['entry']=='FFA12530'];queues=rows(log,'QUEUE')
    packets=rows(log,'PACKET');writes=rows(log,'SOUND');deliveries=rows(log,'DELIVERY')
    qualified=[];unqualified_suppression=[]
    for i,call in enumerate(calls):
        start=float(call['seconds']);end=float(calls[i+1]['seconds'])if i+1<len(calls)else start+.1
        selected=[q for q in queues if start<=float(q['seconds'])<end and
                  all(q[k]==call[k]for k in('a8','a13','frame'))]
        need(len(selected)<=1,'One actual native queue branch per command call')
        code=int(call['a0'],16);table=0xffa0ef20+code*32
        if not selected:
            unqualified_suppression.append(dict(command=code,call=call,suppressionCauseAccepted=False));continue
        need(0xffa0ef20<=table<0xffa10ee0,'Selected native queue has an actual original command record')
        header,base=struct.unpack_from('<HH',guest,off(table));queue=selected[0]
        slot={'FFA12A10':0,'FFA12A80':1,'FFA12B00':2}.get(queue['entry'])
        need(slot is not None and int(queue['a1'],16)==header>>8 and int(queue['a4'],16)==header&255
             and int(queue['a3'],16)==base and all(queue[k]==call[k]for k in('a8','a13','frame')),
             'Actual selected priority/duration/base packet registers match full original table record and owner')
        after=[p for p in packets if float(queue['seconds'])<=float(p['seconds'])<end]
        need(len(after)==1,'Actual selected native queue reaches one complete packet');packet=after[0]
        word=base+slot
        need(int(packet['a3'],16)==word and all(packet[k]==call[k]for k in('a8','a13','frame')),
             'Actual original priority-slot increment and full native packet ownership')
        port=[w for w in writes if float(packet['seconds'])<=float(w['seconds'])<end]
        need(len(port)==2 and [w['pc']for w in port]==['FFA13C90','FFA13D60']and
             tuple(int(w['word'],16)&255 for w in port)==(word>>8,word&255)and
             all(w['mask']=='FFFF'and all(w[k]==call[k]for k in('a8','a13','frame'))for w in port),
             'Actual source-table/queue-slot/packet native high and low bytes reach original port writers')
        for n,w in enumerate(port):
            lo=float(w['seconds']);hi=float(port[n+1]['seconds'])if n==0 else min(end,lo+.1)
            need(any(lo<=float(d['seconds'])<hi and int(d['word'],16)==int(w['word'],16)&255 for d in deliveries),
                 'Both original source-bound packet bytes actually consumed by ADSP')
        qualified.append(dict(command=code,table=f'{table:08X}',originalHeader=f'{header:04X}',originalBase=f'{base:04X}',
            actualSlot=slot,actualPacket=f'{word:04X}',call=call,queue=queue,packet=packet,port=port))
    need(any(q['call']==voice[-1]for q in qualified)and any(q['call']==blades[0]for q in qualified),
         'Own native death voice and original blade effect both fully source-bound through ADSP')
    return dict(passed=True,fighter=fighter,side=side,identity=identity,actualNativeDeathVoice=voice,
        actualNativeBladeEffect=blades[0],sourceBoundActuallySelectedCommands=qualified,
        unqualifiedNativeQueueSuppressions=unqualified_suppression,trueVictimPainGenderAndFixedSourceCommandsAccepted=True,
        allNativeQueueSuppressionCausesAccepted=False,sourceQualifiedNativeDCSWaveformAccepted=False,
        completeBarakaFinisherAudioAccepted=False,fullPortAcceptance=False)


def run():
    parent=json.loads(PARENT.read_text());observation=json.loads(OBSERVED.read_text());guest=capture.original.model.current.expected()
    need(parent['passed']and parent['goalStatus']=='active'and observation['passed']and observation['goalStatus']=='active'
         and observation['remaining']==parent['remaining']and observation['newNativeBoots']==2,
         'Preserve actual paired physical/pixel/full-RAM PCM observation and full original scope')
    pins=dict(observation['newInputHashes'])
    for p in(PARENT,OBSERVED,Path(__file__)):pins[str(p.resolve())]=sha(p)
    cases=[];pngs=[];compacted=[]
    for suffix in('samples','nosamples'):
        folder=BASE/f'kano_p1_{suffix}';meta=json.loads((folder/'result.json').read_text());log=(folder/'run.log').read_text()
        need(meta['passed']and meta['process']['exit_code']==0 and meta['samplesEnabled']==(suffix=='samples')
             and meta['process']['candidate']==capture.original.model.current.NAME and len(meta['actualDisplayHeaders'])==125
             and len(meta['actualNativeHeadBodyPixelsAndScanout']['parts'])==14 and meta['actualPCMBytes']>0,
             'Actual correct current paired context passed entire physical/pixel and PCM recording gates')
        need(all(sha(p)==h for p,h in meta['process']['input_hashes'].items()),'Actual executed immutable inputs unchanged')
        positive=gate(log,guest,'kano',1);faults=[]
        targets=[('foreign native death owner','ROUTE',positive['actualNativeDeathVoice'][0],'id','1'),
                 ('wrong native death gender branch','ROUTE',positive['actualNativeDeathVoice'][1],'entry','FFA123B0'),
                 ('wrong original packed death tuple','ROUTE',positive['actualNativeDeathVoice'][0],'a1','32343638'),
                 ('wrong native death byte','ROUTE',positive['actualNativeDeathVoice'][2],'a1','00000032'),
                 ('proxy original blade actor','ROUTE',positive['actualNativeBladeEffect'],'id','17')]
        fixed=next(q for q in positive['sourceBoundActuallySelectedCommands']if q['call']==positive['actualNativeBladeEffect'])
        targets.extend((('wrong actual table priority','QUEUE',fixed['queue'],'a1','00000000'),
                        ('wrong native base packet','QUEUE',fixed['queue'],'a3','00000000'),
                        ('wrong slot dispatch packet','PACKET',fixed['packet'],'a3','00000000'),
                        ('wrong native port byte','SOUND',fixed['port'][0],'word','00FF'),
                        ('wrong native port owner','SOUND',fixed['port'][0],'a8','01000000')))
        for label,tag,target,key,value in targets:
            line=next(s for s in log.splitlines()if s.startswith('MK2_MAUDIO_'+tag+' ')and
                      dict(re.findall(r'(\w+)=([^\s]+)',s))==target)
            changed,count=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
            need(count==1 and changed!=line,'Effective actual source/owner/packet fault')
            try:gate(log.replace(line,changed,1),guest,'kano',1)
            except ValueError as error:faults.append(dict(label=label,rejectedBy=str(error)))
            else:raise ValueError('Accepted actual native Baraka source/route fault '+label)
        need(gate(log,guest,'kano',1)==positive,'Entire exact positive restored after every actual route fault')
        cases.append(dict(suffix=suffix,result=str(folder/'result.json'),nativePID=meta['process']['nativePID'],routes=positive,faults=faults))
        for p in folder.rglob('*'):
            if not p.is_file():continue
            need(p.suffix.lower()not in('.bin','.wav','.rgb','.pcm'),'No raw requested buffers persisted')
            if p.suffix.lower()=='.png':
                need(p.relative_to(folder).as_posix()=='snap/mk2ks/0000.png','Only accounted native timed-exit PNG')
                pngs.append(dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)))
            if p.suffix.lower()in('.log','.json','.cfg'):
                before=sha(p);cp=subprocess.run(['compact.exe','/C','/EXE:LZX','/I','/Q',str(p)],capture_output=True)
                need(cp.returncode==0 and sha(p)==before,'Retained terminal text losslessly compressed');compacted.append(str(p))
            pins[str(p.resolve())]=sha(p)
    failed_folder=ROOT/'audit_v5534_current_baraka_audio_ram/kano_p1_samples'
    failed_terminal=json.loads((failed_folder/'terminal.json').read_text())
    need(failed_terminal['exit_code']==3 and failed_terminal['nativePID']==123100 and
         "attempt to call a nil value (global 'read')"in(failed_folder/'stderr.log').read_text()
         and not list(failed_folder.rglob('*.png')),
         'Preserve and accurately account original pre-game harness failure, not native gameplay or an exit screenshot')
    for p in failed_folder.rglob('*'):
        if not p.is_file():continue
        need(p.suffix.lower()not in('.bin','.wav','.rgb','.pcm'),'No requested raw buffer in failed harness boot')
        before=sha(p);cp=subprocess.run(['compact.exe','/C','/EXE:LZX','/I','/Q',str(p)],capture_output=True)
        need(cp.returncode==0 and sha(p)==before,'Preserved failed harness evidence losslessly compressed')
        compacted.append(str(p));pins[str(p.resolve())]=sha(p)
    need(len(pngs)==2 and all(sha(p)==h for p,h in pins.items()),'All paired automatic PNGs accounted and current/public/evidence unchanged')
    return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',remaining=parent['remaining'],
        parentAdditiveJournal=str(PARENT),previousGoalTurnClassification=parent['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: actual current Kano-P1 Baraka samples-on/off whole PCM/guest/palette/125 whole frames each exactly equal; full original physical and14 exact head/body scanouts each retained; independently original voice tuple/true gender/player death route/fixed blade call and every selected command record/priority slot/packet/port/ADSP bound,20 actual route faults; retained native text compacted',
        cases=cases,pairedObservation=str(OBSERVED),effectiveActualRouteFaults=20,persistentNativeAutomaticExitPNGs=pngs,
        terminalTextFilesLosslesslyCompacted=len(compacted),actualNativeBootsSinceParentThisTurn=3,
        acceptedPhysicalNativeRuns=2,preservedFailedHarnessNativeRuns=1,preservedFailedHarnessNativePID=123100,
        preservedFailedHarnessNativeExitCode=3,newNativeBootsForQualifier=0,newBuilds=0,newDeletedFiles=0,
        publicPlayableChanged=False,refreshedReleaseZIP=False,allVictimSlotsAudioAccepted=False,
        completeBarakaFinisherAudioAccepted=False,allNativeQueueSuppressionCausesAccepted=False,
        sourceQualifiedNativeDCSWaveformAccepted=False,fullPortAcceptance=False,newInputHashes=pins,
        nextAction='Carry actual current source-bound Baraka audio gate into Sonya and both slots; independently verify suppressed branches and original DCS waveforms, while retaining all original remaining requirements.')


if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable actual source-bound Baraka audio journal')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();capture.save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','remaining','newInputHashes','persistentNativeAutomaticExitPNGs')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
