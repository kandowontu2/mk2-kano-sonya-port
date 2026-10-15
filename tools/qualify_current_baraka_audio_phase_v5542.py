"""Actual original50Hz audio callback coverage, no additional boot.

5539 already executed direct whole RAM/PCM equality before its incorrect
last-video-field assertion. Sound updates are 50Hz, not one per video field.
Keep its failure; independently derive every expected tick and video label
from the real749-field channel chronology and actual native timer source.
"""
import datetime,decimal,json,subprocess,traceback
from pathlib import Path
import current_baraka_audio_capture_v5533 as capture

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
PARENT=ROOT/'audit_v5531_current_baraka_qualified_progress/progress.json'
FAILED=ROOT/'audit_v5539_current_baraka_audio_observation/progress.json'
BASE=ROOT/'audit_v5538_current_baraka_audio_ram'
OUT=ROOT/'audit_v5543_current_baraka_audio_phase_qualified'
D=decimal.Decimal
rows=capture.rows


def pcm_rows(log):
    return [dict(capture.re.findall(r'(\w+)=([^\s]+)',s))for s in log.splitlines()
            if s.startswith('MK2_BBAUDIO_PCM_DIGEST ')]


def coverage(log,meta):
    begin=rows(log,'BEGIN');need(len(begin)==1,'Actual native audio origin');origin=int(begin[0]['origin'])
    channels=rows(log,'CHANNEL')
    need(len(channels)==14*749 and {(int(r['frame']),int(r['channel']))for r in channels}==
         {(f,n)for f in range(origin+1,origin+750)for n in range(14)},'Every actual original749-field/14-channel callback')
    for n in range(14):
        own=[r for r in channels if int(r['channel'])==n]
        need(all(int(r['sample'])==0xffffffff and r['paused']==r['loop']=='0'for r in own)
             and len({(r['length'],r['pos'])for r in own})==1,'All imported channels idle and retained metadata unchanged')
    fields=[r for r in channels if r['channel']=='0'];times=[D(r['seconds'])for r in fields]
    intervals={b-a for a,b in zip(times,times[1:])};need(len(intervals)==1,'Exact native video-field callback period')
    period=next(iter(intervals));need(period>0,'Positive actual video period')
    start=D(begin[0]['seconds']);end=times[-1]+period
    first=int((start*50).to_integral_value(rounding=decimal.ROUND_CEILING))
    last=int((end*50).to_integral_value(rounding=decimal.ROUND_CEILING))-1
    chunks=pcm_rows(log);expected=[D(t)/50 for t in range(first,last+1)]
    need([D(h['seconds'])for h in chunks]==expected,'Every original50Hz sound update inside actual observer window, none missing or extra')
    for h,t in zip(chunks,expected):
        video=origin+sum(at<=t for at in times)
        need(int(h['frame'])==video and int(h['bytes'])==3840,'Exact actual video label and48kHz/20ms signed16 stereo buffer')
    need(len(chunks)==meta['actualPCMUpdates']and sum(int(h['bytes'])for h in chunks)==meta['actualPCMBytes'],
         'Complete actual PCM update/byte counts match full joined in-RAM capture')
    return dict(passed=True,origin=origin,originalVideoFields=749,actualSoundUpdateFrequency=50,
        completeActualSoundCallbacks=len(chunks),completeActualPCMBytes=meta['actualPCMBytes'],
        firstActualSoundSeconds=str(expected[0]),lastActualSoundSeconds=str(expected[-1]),
        nativeWindowEndExclusive=str(end),everyExpectedAudioTickAndVideoLabelExact=True)


def run():
    capture.original.model.current.expected();parent=json.loads(PARENT.read_text());failure=json.loads(FAILED.read_text())
    need(parent['passed']and parent['goalStatus']=='active'and not failure['passed']and
         failure['error']=="ValueError('Whole original audio window through749fields, not truncated at animation completion')"
         and 'paired_observation'in failure['traceback'],'Preserve actual post-equality last-video-field verifier counterexample')
    sound=ROOT/'mame-mkp/src/emu/sound.cpp';header=ROOT/'mame-mkp/src/emu/sound.h';lua=ROOT/'mame-mkp/src/frontend/mame/luaengine.cpp'
    need('static constexpr int STREAMS_UPDATE_FREQUENCY = 50;'in header.read_text()
         and 'm_update_timer->adjust(STREAMS_UPDATE_ATTOTIME, 0, STREAMS_UPDATE_ATTOTIME);'in sound.read_text()
         and 'attotime::from_hz(STREAMS_UPDATE_FREQUENCY)'in sound.read_text()
         and 'execute_function("LUA_ON_SOUND_UPDATE");'in lua.read_text(),
         'Original native sound timer cadence and actual Lua sound-update callback source')
    src=(ROOT/'tools/current_baraka_audio_capture_v5533.py').read_text()
    need(src.index("need(np.array_equal(a['pcm'],b['pcm'])")<src.index('Whole original audio window through749fields'),
         'Actual direct whole PCM equality executed before preserved failing phase assumption')
    cases=[];logs=[];metas=[];pins=dict(parent['newInputHashes']);pngs=[];compacted=[]
    for suffix in('samples','nosamples'):
        folder=BASE/f'kano_p1_{suffix}';meta=json.loads((folder/'result.json').read_text());log=(folder/'run.log').read_text()
        need(meta['passed']and meta['process']['exit_code']==0 and meta['samplesEnabled']==(suffix=='samples')
             and meta['process']['player']=='kano'and meta['process']['victim_slot']==1
             and meta['process']['candidate']==capture.original.model.current.NAME
             and meta['process']['assistance']=='none'and not meta['process']['cheats_enabled']
             and len(meta['actualNativeHeadBodyPixelsAndScanout']['parts'])==14 and len(meta['actualDisplayHeaders'])==125,
             'Both actual current native processes passed whole original physical and exact rendered14-part gates')
        need(all(sha(p)==h for p,h in meta['process']['input_hashes'].items()),'Every actual pinned executed input unchanged')
        pins.update(meta['process']['input_hashes']);positive=coverage(log,meta);faults=[]
        chunk=next(s for s in log.splitlines()if s.startswith('MK2_BBAUDIO_PCM_DIGEST '))
        damaged=capture.re.sub(r'frame=\d+', 'frame=0',chunk,count=1)
        for label,bad in(('one actual sound callback omitted',log.replace(chunk+'\n','',1)),
                          ('one actual sound callback assigned wrong video field',log.replace(chunk,damaged,1))):
            try:coverage(bad,meta)
            except ValueError as error:faults.append(dict(label=label,rejectedBy=str(error)))
            else:raise ValueError('Accepted actual50Hz sound callback fault '+label)
        need(coverage(log,meta)==positive,'Complete actual positive restored after sound callback faults')
        cases.append(dict(suffix=suffix,nativePID=meta['process']['nativePID'],coverage=positive,faults=faults));logs.append(log);metas.append(meta)
        for p in folder.rglob('*'):
            if not p.is_file():continue
            need(p.suffix.lower()not in('.bin','.wav','.rgb','.pcm'),'All requested native raw media remain in RAM')
            if p.suffix.lower()=='.png':
                need(p.relative_to(folder).as_posix()=='snap/mk2ks/0000.png','Only accounted native timed-exit PNG')
                pngs.append(dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)))
            if p.suffix.lower()in('.log','.json','.cfg'):
                before=sha(p);cp=subprocess.run(['compact.exe','/C','/EXE:LZX','/I','/Q',str(p)],capture_output=True)
                need(cp.returncode==0 and sha(p)==before,'Terminal evidence losslessly compacted');compacted.append(str(p))
            pins[str(p.resolve())]=sha(p)
    need(pcm_rows(logs[0])==pcm_rows(logs[1])and metas[0]['actualMixedPCMSHA256']==metas[1]['actualMixedPCMSHA256']
         and metas[0]['actualPCMBytes']==metas[1]['actualPCMBytes'],'Every actual native PCM interval and joined in-RAM waveform hash on/off exact')
    need(metas[0]['actualDisplayHeaders']==metas[1]['actualDisplayHeaders'],'Every actual whole125-frame native RGB raster on/off exact')
    selected=lambda t:[s for s in t.splitlines()if s.startswith(('MK2_STOCK_HEAD_V921_','MK2_ROLLING_HEAD_V1003_','MK2_CURRENT_BARAKA_SCENE_'))]
    need(selected(logs[0])==selected(logs[1]),'Whole actual physical/controller/owned art/palette/FIFO/display chronology identical')
    for tag in('BEGIN','ROUTE','QUEUE','PACKET','SOUND','DELIVERY','RESULT'):
        need(rows(logs[0],tag)==rows(logs[1],tag),'Complete actual native audio '+tag+' chronology on/off identical')
    for p in(PARENT,FAILED,Path(__file__),sound,header,lua,ROOT/'mk2ks_current_baraka_audio_ram_v5532.lua',
              ROOT/'mk2ks_current_baraka_audio_ram_v5536.lua',ROOT/'tools/current_baraka_audio_capture_v5533.py',
              ROOT/'tools/current_baraka_audio_capture_v5537.py',ROOT/'audit_v5535_current_baraka_audio_observation/progress.json'):
        pins[str(p.resolve())]=sha(p)
    need(len(pngs)==2 and all(sha(p)==h for p,h in pins.items()),'Exact current/public/source/evidence stable and native exit PNGs accounted')
    return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',remaining=parent['remaining'],
        parentAdditiveJournal=str(PARENT),preservedPhaseAssumptionFailure=str(FAILED),
        thisGoalTurnClassification='progress: two actual current Kano-P1 Baraka complete physical/14-head-body exact raster runs; actual whole RAM/PCM equality already executed before preserved phase-assumption failure; native original50Hz timer/749video-field observer coverage independently exact,685full updates each,4actual phase faults, no restart or discarded buffers; retained paired text compressed',
        cases=cases,allActualPCMUpdatesOnOffExact=True,actualJoinedNativePCMHashOnOffEqual=True,
        actualWholeDisplayedFrameCallbacks=250,effectiveActualAudioPhaseFaults=4,persistentNativeAutomaticExitPNGs=pngs,
        terminalTextFilesLosslesslyCompacted=len(compacted),newNativeBoots=2,newNativeBootsForQualifier=0,
        newBuilds=0,newDeletedFiles=0,publicPlayableChanged=False,refreshedReleaseZIP=False,
        allVictimSlotsAudioAccepted=False,completeBarakaFinisherAudioAccepted=False,fullPortAcceptance=False,newInputHashes=pins,
        nextAction='Qualify actual own-death voice/gender/player and original blade/selected packet source against retained logs; extend both victims/slots and independently original DCS waveform/suppressed-branch fidelity. Preserve full objective.')


if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable completed actual native50Hz audio qualification')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();capture.save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','remaining','newInputHashes','persistentNativeAutomaticExitPNGs')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
