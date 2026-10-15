"""Short-lived streamed saved metadata; no recorder, whole log or raw media RAM."""
import copy,ctypes,gzip,inspect,json,re,traceback,wave
from pathlib import Path
import qualify_native_selector_sonya_voice_owner_eof as prior
import verify_native_source_sync as sync

ROOT=sync.ROOT
OUT=ROOT/'audit_saved_square_owner_eof_streamed_checked'
BASE=ROOT/'audit_native_selector_lowkick_after_host_exit_scoped_ram/fresh_host_Kano_actual_IN2_lowkick_natural_Sonya_CPU_saved_owners'
CAPTURE=ROOT/'audit_native_selector_lowkick_after_host_exit_bound_capture_checked/report.json'
MAX_MEMORY=128*1024*1024


def peak():
    class Counters(ctypes.Structure):
        _fields_=[('cb',ctypes.c_uint32),('faults',ctypes.c_uint32)]+[(k,ctypes.c_size_t) for k in
            ('peakWorking','working','peakPaged','paged','peakNonpaged','nonpaged','pagefile','peakPagefile')]
    c=Counters();c.cb=ctypes.sizeof(c)
    ctypes.windll.kernel32.GetCurrentProcess.restype=ctypes.c_void_p
    ctypes.windll.psapi.GetProcessMemoryInfo.argtypes=(ctypes.c_void_p,ctypes.POINTER(Counters),ctypes.c_uint32)
    assert ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.windll.kernel32.GetCurrentProcess(),ctypes.byref(c),c.cb)
    assert c.peakWorking<MAX_MEMORY,'Short-lived metadata check exceeded128MiB budget'
    return c.peakWorking


def boundary(data,actual,frame):
    if actual[frame]['mode']=='2':return '2'
    prior.need(frame==2571 and actual[frame]['mode']=='7' and actual[frame+1]['mode']=='2','Only actual within-frame7->2 boundary')
    taps=[r for r in data['MK2_SONYA_CHOICE_EVENT'] if r['frame']=='2571' and r['kind']=='square']
    prior.need(len(taps)==1 and tuple(taps[0][k] for k in
        ('mode','pc','opcode','actor','main','owner','id','roster','state','human_state'))==
        ('2','FFFBC300','C080','010350A0','0106BF30','010350A0','18','18','0','1'), 'Actual instruction-time Square owner and next physical field')
    return taps[0]['mode']


def binding():
    source=inspect.getsource(prior.gate)
    for old,new in (
        ("['6B00','6B01','6B02']","['6B00']"),
        ('starts=[markers[0],markers[1]]','starts=[markers[0]]'),
        ('need(count==246 and','need(count>0 and'),
        ("actual[f]['id'],actual[f]['hp'],actual[f]['mode'])==","actual[f]['id'],actual[f]['hp'],boundary(data,actual,f))=="),
    ):
        prior.need(source.count(old)==1,'Only actual cue inventory/mode boundary differs');source=source.replace(old,new,1)
    scope=dict(vars(prior),boundary=boundary)
    exec(compile(source,__file__+'::whole_original_owner_clock_gate','exec'),scope)
    return scope['gate']


def main():
    prior.need(not OUT.exists(),'Fresh immutable streamed proof')
    proof=json.loads(CAPTURE.read_text()); pins=dict(proof['inputHashes'])
    prior.need(proof['passed'] and proof['actualNativeIdentity']['ProcessId']==21456 and proof['nativeExit']==0,'Actual saved completed capture')
    prior.need(all(sync.sha(p)==h for p,h in pins.items()),'All whole recorded source/capture inputs unchanged')
    tags=('MK2_VOICE_OWNER_ITEM','MK2_VOICE_OWNER','MK2_MAUDIO_SOUND','MK2_CPU_ROUND_FIELD','MK2_CPU_ROUND_HEALTH','MK2_SONYA_CHOICE_EVENT')
    data={t:[] for t in tags}
    with gzip.open(BASE/'run.log.gz','rt',encoding='utf8') as stream:
        while True:
            line=stream.readline(1024*1024+1)
            if not line:break
            prior.need(len(line)<=1024*1024,'Bounded streamed line')
            tag=line.split(' ',1)[0]
            if tag in data:data[tag].append(dict(prior.RX.findall(line)))
    peak();clip=ROOT/'samples/mk2ks/sonya_square_launch.wav'
    with wave.open(str(clip),'rb') as audio:
        prior.need((audio.getnchannels(),audio.getsampwidth(),audio.getframerate(),audio.getnframes())==(1,2,48000,45512),'Whole original Square source header')
    lengths={0x6b00:45512};gate=binding();positive=gate(data,lengths);faults=[]
    for field,value in zip(prior.FIELDS,('01000000','01000000','160','17','1')):
        bad=copy.deepcopy(data);next(r for r in bad['MK2_VOICE_OWNER'] if r['actor']=='010350A0')[field]=value
        try:gate(bad,lengths)
        except AssertionError as error:faults.append(dict(field=field,rejected=str(error)))
        else:raise AssertionError('Owner field fault admitted')
        del bad;peak()
    prior.need(gate(data,lengths)==positive,'Whole unmodified owner positive restored')
    for p in (Path(__file__),Path(prior.__file__),CAPTURE,clip,BASE/'run.log.gz'):
        pins[str(p.resolve())]=sync.sha(p)
    prior.need(all(sync.sha(p)==h for p,h in pins.items()),'All complete pins remain intact')
    report=dict(passed=True,actualNativeIdentity=proof['actualNativeIdentity'],recordedQuietEOFOwnership=positive,
        ownerFieldFaults=faults,inputHashes=pins,peakWorkingSetBytes=peak(),memoryBudgetBytes=MAX_MEMORY,
        fullPortAcceptance=False,privateVoiceInterruptionAccepted=False,newRecorders=0,newGames=0,newRawMediaFiles=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,owners=positive['actualSavedOwnerSnapshots'],peakMemoryMiB=round(peak()/1024**2,1))),flush=True)


if __name__=='__main__':
    try:main()
    except BaseException:
        OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=traceback.format_exc()),indent=2)+'\n');raise
