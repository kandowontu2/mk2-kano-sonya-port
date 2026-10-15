"""Actual saved voice-owner fields, only quiet EOF in rejected-input run49084.

Read existing compressed metadata; never enter the retained Python console or
start another game. Failed Low Kick inputs are NOT accepted as gameplay. Clip
EOF/60Hz owner retirement clocks are derived from port times and original WAV
headers, not chosen from observed owner transitions. Full scope stays active.
"""
import copy,gzip,hashlib,json,re,subprocess,traceback,wave
from collections import Counter
from decimal import Decimal
from pathlib import Path
import verify_native_source_sync as sync

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'audit_native_selector_sonya_voice_owner_eof_checked'
BASE=ROOT/'audit_native_selector_sonya_cpu_lowkick_owners_ram/ordinary_Kano_walk_lowkick_native_Sonya_CPU_actual_voice_owners'
CAPTURE=ROOT/'audit_native_selector_sonya_cpu_lowkick_owners_capture_checked/failure.json'
need,sha=sync.need,sync.sha
ATTO=10**18; PERIOD60=ATTO//60; PERIOD48=(ATTO+48000-1)//48000
RX=re.compile(r'(\w+)=([^\s]+)')
FIELDS=('actor','main','health','id','mode')
SIZES=dict(actor=4,main=4,health=2,id=2,mode=2)
FILES={0x6b00:'sonya_square_launch.wav',0x6b01:'sonya_bicycle_launch.wav',0x6b02:'sonya_bicycle_cry.wav'}
PCS={'6B00':'FFFFCAC0','6B01':'FFF9A4C0','6B02':'FFF9A520'}


def read():
    prefixes=('MK2_VOICE_OWNER_ITEM ','MK2_VOICE_OWNER ','MK2_MAUDIO_SOUND ',
              'MK2_CPU_ROUND_FIELD ','MK2_CPU_ROUND_HEALTH ')
    result={p.strip():[] for p in prefixes}
    with gzip.open(BASE/'run.log.gz','rt',encoding='utf-8') as stream:
        for line in stream:
            if line.startswith(prefixes):result[line.split()[0]].append(dict(RX.findall(line)))
    return result


def at(seconds):return int(Decimal(seconds)*ATTO)
def clock(t,up):
    seconds,fraction=divmod(t,ATTO)
    return seconds*48000+(fraction+(PERIOD48-1 if up else 0))//PERIOD48


def gate(data,lengths):
    items=data['MK2_VOICE_OWNER_ITEM']; owners=data['MK2_VOICE_OWNER']
    need(len(items)==5 and {r['field'] for r in items}==set(FIELDS), 'Every actual saved owner descriptor unique/present')
    for r in items:
        name=r['field']
        need(r==dict(field=name,name='0/m_mk2ks_battle_'+name,bytes=str(SIZES[name]),count='2',writes='0',assistance='none'),
             'Actual registered two-player saved array layout and read-only descriptor')
    need(len(owners)==13850,'Every real saved-field snapshot, no missing or duplicate owner row')
    need([int(r['serial']) for r in owners]==[s for s in range(1,6926) for _ in range(2)],
         'Original owner observer chronology retained in full')
    phases=Counter(); previous=-1
    for n in range(0,len(owners),2):
        left,right=owners[n:n+2]
        need(left['slot']=='1' and right['slot']=='2' and
             all(left[k]==right[k] for k in ('serial','phase','frame','seconds')),
             'Both physical slots observed together, not swapped or reconstructed')
        t=at(left['seconds']);need(t>=previous,'Actual observation clocks nondecreasing');previous=t
        need(left['phase'] in ('frame','sound','stop') and
             all(r['writes']=='0' and r['assistance']=='none' for r in (left,right)),
             'Every observer phase read-only');phases[left['phase']]+=1
    need(dict(phases)==dict(frame=3618,sound=3306,stop=1),'Entire real frame/sound/terminal observation inventory')
    need([int(r['frame']) for r in owners[::2] if r['phase']=='frame']==list(range(1,3619)),
         'Every cold/native/UI callback, including real last frame')
    sound=[r for r in owners[::2] if r['phase']=='sound']
    need([at(r['seconds']) for r in sound]==[n*ATTO//50 for n in range(1,3307)],
         'Every original50Hz sound callback clock, without a fitted phase')
    markers=[r for r in data['MK2_MAUDIO_SOUND'] if r['word'] in ('6B00','6B01','6B02','6B03')]
    need([r['word'] for r in markers]==['6B00','6B01','6B02'],'All actual quiet CPU launches, including both Bicycle cues')
    for r in markers:
        need((r['pc'],r['a8'],r['a13'],r['mask'],r['writes'],r['assistance'])==
             (PCS[r['word']],'010350A0','0106BF30','FFFF','0','none'),
             'Actual typed Sonya source port instructions/actor/Main, not inferred route')
    starts=[markers[0],markers[1]]; episodes=[]
    for i,start in enumerate(starts):
        cues=[start] if i==0 else markers[1:]
        onset=at(start['seconds']); n=1
        while True:
            tick=onset+n*PERIOD60
            # All actual sources are48kHz, so repeated-double pos+=1 is exact.
            # playing(main) runs first; aux is only queried after main EOF.
            ended=[clock(tick,False)-clock(at(c['seconds']),True)>=lengths[int(c['word'],16)] for c in cues]
            if all(ended):break
            n+=1;need(n<200,'Finite native nonlooping source ends')
        episodes.append(dict(onset=onset,retired=tick,timerTicks=n,
                             markers=[r['word'] for r in cues]))
    rounds=data['MK2_CPU_ROUND_FIELD']
    actual={int(r['frame']):r for r in rounds if r['slot']=='2'}
    need(len(actual)==1801 and set(actual)==set(range(1818,3619)), 'Complete actual CPU state/health callbacks')
    for episode in episodes:
        active_frames=[int(r['frame']) for r in owners if r['slot']=='2' and
                       episode['onset']<=at(r['seconds'])<episode['retired']]
        need(active_frames and all((actual[f]['actor'],actual[f]['main'],actual[f]['owner'],actual[f]['id'],actual[f]['hp'],actual[f]['mode'])==
             ('010350A0','0106BF30','010350A0','18','161','2') for f in active_frames),
             'Actual quiet owner identity/health/mode unchanged during each real clip')
        changes=[r for r in data['MK2_CPU_ROUND_HEALTH'] if r['slot']=='2' and
                 min(active_frames)<=int(r['frame'])<=max(active_frames)]
        need(not changes,'No unobserved incoming-health retirement relabeled EOF')
    zero=('00000000','00000000','0','0','0'); active=('010350A0','0106BF30','161','18','2')
    count=0; boundaries=[]
    for r in owners:
        owned=r['slot']=='2' and any(e['onset']<=at(r['seconds'])<e['retired'] for e in episodes)
        need(tuple(r[k] for k in FIELDS)==(active if owned else zero),
             'All five actual saved fields equal independently timed source ownership/retirement')
        count+=owned
    for e in episodes:
        rows=[r for r in owners if r['slot']=='2']
        last=next(r for r in reversed(rows) if at(r['seconds'])<e['retired'] and at(r['seconds'])>=e['onset'])
        first=next(r for r in rows if at(r['seconds'])>=e['retired'])
        boundaries.append(dict(**e,lastActualOwnedSnapshot=last,firstActualZeroSnapshot=first))
    need(count==246 and all(tuple(r[k] for k in FIELDS)==zero for r in owners[-2:]),
         'Actual finite active snapshots and both full terminal owner arrays zero')
    return dict(passed=True,actualSavedOwnerSnapshots=len(owners),actualActiveOwnerSnapshots=count,
        observedPhases=dict(phases),sourceDerivedRetirements=boundaries,
        allRecordedQuietEOFOwnerFieldsAccepted=True,allOwnerLifetimeTransitionsAccepted=False,
        hitKOResetMorphOwnerCleanupAccepted=False,physicalLowkickGameplayAccepted=False,fullPortAcceptance=False)


def execute():
    need(not OUT.exists(),'Fresh immutable finite EOF ownership proof')
    proof=json.loads(CAPTURE.read_text()); terminal=json.loads((BASE/'result.json').read_text())
    identity=proof['actualNativeIdentity']
    need(not proof['passed'] and proof['nativeExit']==terminal['nativeExit']==0 and identity['ProcessId']==49084 and
         identity['ParentProcessId']==38752 and identity['createdUnix']==1791786145.2510834,
         'Original actual rejected-input run retained; no transport failure promoted')
    errors=(BASE/'stderr.log').read_text(); marker="attempt to index a nil value (field 'P1 Low Kick')"
    need(errors.count(marker)==14 and '[LUA ERROR]' in errors,'Exact actual missing-input errors preserved and excluded from gameplay acceptance')
    need(sync.verify()['passed'],'Whole current15 compiled sources and fixed public/private endpoints')
    pins=dict(proof['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'All original full source/native pins intact')
    data=read();lengths={}
    for code,name in FILES.items():
        path=ROOT/'samples/mk2ks'/name
        with wave.open(str(path),'rb') as clip:
            need((clip.getnchannels(),clip.getsampwidth(),clip.getframerate(),clip.getcomptype())==(1,2,48000,'NONE'),
                 'Whole original mono signed16 source at native48kHz'); lengths[code]=clip.getnframes()
        pins[str(path)]=sha(path)
    need(lengths=={0x6b00:45512,0x6b01:40720,0x6b02:66523},'Actual qualified original source lengths, no timing fit')
    source=ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'
    need(sha(source)=='A32C860194808831589A7D06F47A564708162B723391801EC5A310113767ACDD',
         'Whole actual compiled owner binding/timer/stop source')
    text=source.read_text()
    for name in FIELDS:
        need('save_item(NAME(m_mk2ks_battle_'+name+'));' in text and
             'm_mk2ks_battle_'+name+'[slot] = 0;' in text,
             'Actual saved field registration and full owner cleanup')
    need('else if (!m_mk2ks_voices->playing(10 + slot * 2) && !m_mk2ks_voices->playing(11 + slot * 2))' in text and
         'm_mk2ks_battle_audio_timer->adjust(attotime::from_hz(60), 0, attotime::from_hz(60));' in text and
         'mk2ks_battle_audio_stop(slot, "finished");' in text,
         'Exact source60Hz short-circuit EOF owner retirement, no invented reason')
    positive=gate(data,lengths); faults=[]
    for field,value in zip(FIELDS,('01000000','01000000','160','17','1')):
        bad=copy.deepcopy(data); row=next(r for r in bad['MK2_VOICE_OWNER'] if r['actor']=='010350A0')
        row[field]=value
        try:gate(bad,lengths)
        except AssertionError as error:faults.append(dict(kind='owned_'+field,rejectedBy=str(error)))
        else:raise AssertionError('Actual owner field fault admitted: '+field)
    for label,change in (
        ('missing_real_snapshot',lambda d:d['MK2_VOICE_OWNER'].pop()),
        ('duplicate_real_snapshot',lambda d:d['MK2_VOICE_OWNER'].append(copy.deepcopy(d['MK2_VOICE_OWNER'][-1]))),
        ('wrong_saved_layout',lambda d:d['MK2_VOICE_OWNER_ITEM'][0].update(bytes='4')),
        ('wrong_launch_owner',lambda d:next(r for r in d['MK2_MAUDIO_SOUND'] if r['word']=='6B00').update(a8='01000000')),
        ('wrong_native_launch_clock',lambda d:next(r for r in d['MK2_MAUDIO_SOUND'] if r['word']=='6B00').update(seconds='35.000000000000')),
        ('early_owner_clear',lambda d:next(r for r in d['MK2_VOICE_OWNER'] if r['actor']=='010350A0').update(actor='00000000',main='00000000',health='0',id='0',mode='0')),
        ('terminal_dangling_id',lambda d:d['MK2_VOICE_OWNER'][-1].update(id='18'))):
        bad=copy.deepcopy(data);change(bad)
        try:gate(bad,lengths)
        except AssertionError as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise AssertionError('Actual owner chronology fault admitted: '+label)
    bad_lengths=dict(lengths);bad_lengths[0x6b00]+=4800
    try:gate(data,bad_lengths)
    except AssertionError as error:faults.append(dict(kind='wrong_actual_source_length',rejectedBy=str(error)))
    else:raise AssertionError('Actual source EOF duration fault admitted')
    need(gate(data,lengths)==positive,'Whole unmodified actual owner observation history restored')
    for p in (Path(__file__),CAPTURE,BASE/'run.log.gz',BASE/'result.json',BASE/'process.json',BASE/'stderr.log',source,
              ROOT/'mame-mkp/src/devices/sound/samples.cpp',ROOT/'mk2ks_native_selector_sonya_cpu_lowkick_owners.lua'):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'No executed source/actual failure rewritten');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'Whole original/new evidence input hashes intact')
    result=dict(passed=True,goalStatus='active',actualNativeIdentity=identity,nativeExit=0,
        recordedQuietEOFOwnership=positive,effectiveFaultsRejected=faults,inputHashes=pins,
        originalInputFailurePreserved=True,actualOriginalLuaErrors=14,requirements=proof['requirements'],
        remainingGroups=proof['remainingGroups'],physicalLowkickGameplayAccepted=False,
        allOwnerLifetimeTransitionsAccepted=False,fullPortAcceptance=False,publicPlayableChanged=False,
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(passed=True,snapshots=13850,sourceDerivedEOFs=2,effectiveFaults=len(faults),
        physicalLowkickGameplayAccepted=False,fullPortAcceptance=False)),flush=True)
    return result


if __name__=='__main__':
    try:execute()
    except Exception as error:
        need(not OUT.exists(),'Preserve actual finite owner proof rejection')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
