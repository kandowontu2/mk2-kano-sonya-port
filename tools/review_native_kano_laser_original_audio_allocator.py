"""Full original sound helper/table audit and actual five-slot state replay.

This accepts only the earned original reference, not port audio or PCM.
Packet offsets derive from source channel allocation, not fabricated variants.
Every observed slot (priority, remaining ticks, continuation) is replayed at
every captured helper/timer entry. All other sound packets remain visible.
"""
import gzip
import json
import struct
import subprocess
import traceback
from collections import Counter
from decimal import Decimal
from pathlib import Path
import review_native_kano_laser_burst as burst

ROOT=burst.ROOT
OUT=ROOT/'audit_native_kano_laser_original_audio_allocator_review'
need,sha=burst.need,burst.sha
FOLDER=ROOT/'audit_native_kano_laser_original_audio_allocator'


def rows(text,tag):return burst.rows(text,tag,True)


def parse_slots(row):
    result=[tuple(int(x,16) for x in part.split(',')) for part in row['slots'].split(';')]
    need(len(result)==5 and all(len(x)==3 for x in result),'Whole actual five-slot priority/time/continuation state')
    return result


def choose(record,flag,slots):
    flags=record&0xffff;command=record>>16
    priority=flags>>8;duration=flags&255
    if not flags:return None
    category=priority>>4
    if category==3 and any(p==priority for p,t,c in slots):return None
    if category==4:
        if priority==0x41 and flag!=1:priority=0x42
        existing=next((i for i,(p,t,c) in enumerate(slots) if p==priority),None)
        if existing is not None:return existing,priority,duration,command+existing
    free=next((i for i,(p,t,c) in enumerate(slots) if p==0),None)
    selected=free if free is not None else min(range(5),key=lambda i:slots[i][0])
    if free is None and slots[selected][0]>priority:return None
    return selected,priority,duration,command+selected


def packets(text):
    result=[];source=rows(text,'SOUND')
    need(len(source)%2==0,'Entire original high/low sound packet chronology')
    for high,low in zip(source[::2],source[1::2]):
        need(high['pc']=='FFAA88B0' and low['pc']=='FFAA8920' and high['frame']==low['frame'] and
             high['mask']==low['mask']=='FFFF' and Decimal(high['seconds'])<Decimal(low['seconds']),
             'Real original high then low store sequence, not guessed byte ordering')
        result.append(dict(frame=high['frame'],seconds=high['seconds'],
            command=(int(high['byte'],16)<<8)|int(low['byte'],16)))
    return result


def contract(text):
    entry=rows(text,'OWN_ENTRY');stop=rows(text,'STOP')
    need(len(entry)==len(stop)==1 and entry[0]['ids']=='0,1' and entry[0]['hp']=='166,0' and
         stop[0]['zeros']=='2' and stop[0]['own_action_observed']=='1','Actual physically earned original laser')
    start=int(entry[0]['frame']);code=rows(text,'AUDIO_CODE')
    need(code and all(r['writes']=='0' and r['assistance']=='none' for r in code),'Passive real original code taps only')
    state=[(0,0,0)]*5;pending=None;allocations=[];timer=[];checked=0;packet_rows=packets(text)
    records=[]
    for row in code:
        actual=parse_slots(row)
        need(actual==state,'Every actual sound-helper priority/time/continuation state matches complete semantic replay')
        checked+=5;at=row['at']
        if at=='FFAA6E00':
            need(pending is None,'Previous actual allocator choice dispatched or rejected')
            record=int(row['record'],16);choice=choose(record,int(row['flag']),state)
            records.append(dict(age=int(row['age']),record=f'{record:08X}',actor=row['actor'],job=row['job']))
            if choice is not None:pending=dict(row=row,record=record,choice=choice)
        elif at=='FFAA7900':
            need(pending is not None,'Real assignment follows an admitted source record')
            slot,priority,duration,command=pending['choice'];source=pending['row']
            need(row['job']==source['job'] and row['actor']==source['actor'] and row['age']==source['age'] and
                 int(row['a5'],16)==0x010b8ba0+slot*64 and int(row['a2'],16)==0x010b8bb0+slot*64 and
                 int(row['a1'],16)==priority and int(row['a4'],16)==duration and int(row['a3'],16)==command,
                 'Real source-selected slot, packet base+slot, exact priority, full low-byte duration')
            state[slot]=(priority,duration,state[slot][2])
            allocations.append(dict(age=int(row['age']),seconds=row['seconds'],slot=slot,record=f'{pending["record"]:08X}',
                priority=priority,durationTicks=duration,command=f'{command:04X}',actor=row['actor'],job=row['job'],
                oldSlots=actual,newSlots=list(state)))
        elif at=='FFAA87C0' and pending is not None:
            slot,priority,duration,command=pending['choice'];source=pending['row']
            need(row['job']==source['job'] and row['actor']==source['actor'] and int(row['a3'],16)==command and
                 state[slot][:2]==(priority,duration),'Actual admitted record reaches original packet writer with allocated state')
            candidates=[r for r in packet_rows if r['frame']==row['frame'] and
                        r['command']==command and Decimal(r['seconds'])>Decimal(row['seconds']) and
                        Decimal(r['seconds'])-Decimal(row['seconds'])<Decimal('.0001')]
            need(len(candidates)==1,'Real allocated command appears exactly once at corresponding actual DCS high/low stores')
            pending=None
        elif at=='FFAA80D0':
            timer.append(row)
            next_state=[]
            for priority,duration,stream in state:
                need(stream==0,'This earned trace uses no unmodeled continuation stream')
                after=max(0,duration-1)
                next_state.append((0 if duration==1 else priority,after,0))
            state=next_state
    need(pending is None and len(allocations)==len(records)==39,'All39 actual record allocations and dispatches, not only five selected cues')
    counts=Counter(int(r['age']) for r in timer)
    need(set(counts)==set(range(1,301)) and len(timer)==301 and counts[7]==2 and
         all(counts[age]==1 for age in range(1,301) if age!=7),
         'All301 actual timer invocations, including genuine duplicate during empty-slot age7')
    want=[(20,'03525038',0,'0352',0x50,56),(68,'276A504C',1,'276B',0x50,76),
        (68,'081B41CB',2,'081D',0x42,203),(164,'01405066',0,'0140',0x50,102),
        (164,'01455063',1,'0146',0x50,99)]
    need([(r['age'],r['record'],r['slot'],r['command'],r['priority'],r['durationTicks']) for r in allocations[:5]]==want,
         'All five laser-specific own/victim/burst cues mapped to exact true original allocations')
    calls=[r for r in code if r['at'] in ('FFAA8CA0','FFAA4C80','FFAA6D00') and int(r['age'])<=164]
    need([(r['age'],r['at'],r['id'],int(r['a0'],16)) for r in calls]==
         [('20','FFAA8CA0','0',5),('68','FFAA8CA0','0',6),('68','FFAA4C80','1',9),
          ('164','FFAA6D00','1',0),('164','FFAA6D00','1',1)],
         'True own/victim/universal source call families and cue numbers, no proxy or forced sound')
    random=[r for r in code if r['at']=='FFAA6C00' and int(r['age'])<=164]
    need(len(random)==1 and random[0]['age']=='68' and random[0]['a0']=='00000001' and random[0]['a1']=='FFAA5090',
         'Victimcue9 has exactly one source record, though real RNG helper still executes')
    return dict(checkedSlotTriples=checked,actualRecordAllocations=allocations,actualRecords=records,
        sourceTimerInvocations=301,sourceTimerThroughAge=300,sourceLaserCues=allocations[:5],
        fullOriginalSoundPackets=packet_rows,streamContinuationsObserved=False,
        nativeHigherPriorityAllSlotsRejectionObserved=False,portAudioAccepted=False)


def section(blob,start,end):return blob[(start-0xff800000)//8:(end-0xff800000)//8]


def disasm(path,start,end):
    job=subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'),str(path),'-arch','tms34010','-basepc',f'{start:X}',
        '-skip',str((start-0xff800000)//8),'-count',str(end-start)],capture_output=True,text=True)
    need(job.returncode==0,'Whole source helper disassembly terminal')
    return job.stdout


def main():
    need(not OUT.exists(),'Fresh original audio review; no overwritten prior evidence');OUT.mkdir()
    try:
        record=json.loads((FOLDER/'report.json').read_text())
        need(record['passed'] and record['nativeExit']==0 and record['originalWholeGuestMatched'] and not record['errors'] and
             all(sha(p)==h for p,h in record['inputHashes'].items()),'Same actual original native game terminal; full guest and executed inputs conserved')
        text=gzip.open(FOLDER/'run.log.gz','rt').read();result=contract(text)
        old_folder=ROOT/'audit_native_kano_laser_original_burst_pipeline'
        old=gzip.open(old_folder/'run.log.gz','rt').read()
        need(rows(text,'RGB_DIGEST')==rows(old,'RGB_DIGEST') and len(rows(text,'RGB_DIGEST'))==36,
             'All36 actual whole rasters exactly match the already individually viewed original burst reference')
        rom_path=ROOT/'mk3/mk3-maincpu.bin';rom=rom_path.read_bytes()
        roots=struct.unpack('<19I',section(rom,0xffaa8f70,0xffaa91d0))
        need(roots[0]==0xffaa91d0,'Actual Kano own sound-table root')
        own=[struct.unpack('<I',section(rom,roots[0]+cue*32,roots[0]+(cue+1)*32))[0] for cue in (5,6)]
        need(own==[0x03525038,0x276a504c],'Whole actual own cue5/6 DWORD records')
        universal=struct.unpack('<2I',section(rom,0xffaa3a60,0xffaa3aa0))
        need(universal==(0x01405066,0x01455063),'Actual two whole universal bone-burst sound records')
        groups=struct.unpack('<19h',section(rom,0xffaa6120,0xffaa6250))
        need(groups==(3,0,3,2,4,1,0,5,5,4,1,7,3,6,5,-1,8,4,4),'Whole real nineteen-character voice-group mapping')
        cue9=struct.unpack('<I',section(rom,0xffaa4f40+9*32,0xffaa4f40+10*32))[0]
        count=struct.unpack('<H',section(rom,cue9,cue9+16))[0]
        voices=struct.unpack('<9I',section(rom,cue9+16,cue9+16+9*32))
        need(cue9==0xffaa5080 and count==1 and voices[0]==0x081b41cb and voices[3]==0x17bb41c1,
             'Whole nine voice-group records; one choice per group, no inferred low-bit variation count')
        helpers=[('victim_voice',0xffaa4c80,0xffaa4f40),('random_choice',0xffaa6c00,0xffaa6d00),
            ('universal_and_full_allocator',0xffaa6d00,0xffaa7a20),('complete_timer',0xffaa80d0,0xffaa87c0),
            ('packet_write_and_handshake',0xffaa87c0,0xffaa8a00),('own_voice',0xffaa8ca0,0xffaa8d70),
            ('actual_rng_range',0xff927780,0xff927810)]
        reviewed=[]
        for name,start,end in helpers:
            blob=section(rom,start,end)
            reviewed.append(dict(name=name,start=f'{start:08X}',endExclusive=f'{end:08X}',completeBytes=len(blob),
                bytesHex=blob.hex().upper(),disassembly=disasm(rom_path,start,end)))
        faults=[]
        for name,old_value,new in [('wrong_record','record=03525038','record=03525039'),
            ('wrong_priority','a1=00000042 a2=010B8C30','a1=00000041 a2=010B8C30'),
            ('wrong_channel_command','a3=0000276B','a3=0000276A'),
            ('truncated_duration','a4=000000CB','a4=00000003'),
            ('wrong_choice_count','a0=00000001 a1=FFAA5090','a0=00000003 a1=FFAA5090'),
            ('wrong_live_slot_timer','slots=0050,0008,00000000','slots=0050,0007,00000000')]:
            need(old_value in text,'Concrete actual sound negative-control boundary '+name)
            try:contract(text.replace(old_value,new,1))
            except ValueError as error:faults.append(dict(name=name,rejected=str(error)))
            else:raise ValueError('Sound fault admitted '+name)
        scope_path=ROOT/'audit_native_kano_laser_burst_scheduler_phase_review/report.json';scope=json.loads(scope_path.read_text())
        paths=[Path(__file__),Path(burst.__file__),rom_path,ROOT/'mame-mkp/unidasm.exe',FOLDER/'report.json',FOLDER/'run.log.gz',
            FOLDER/'executed_sources.json.gz',old_folder/'report.json',old_folder/'run.log.gz',scope_path,
            ROOT/'source_native_kano_laser_burst/midtunit_m.cpp',ROOT/'source_native_kano_laser_burst/midtunit.cpp',ROOT/'PLAY_LATEST_KANO_SONYA.cmd']
        report=dict(passed=True,earnedOriginalSoundAllocatorReplayAccepted=True,sourceSoundTablesReviewed=True,
            portAudioAccepted=False,fullFinisherAccepted=False,fullPortAcceptance=False,runtimeReference=result,
            ownCueRecords=[f'{r:08X}' for r in own],universalBurstRecords=[f'{r:08X}' for r in universal],
            originalVoiceGroups=list(groups),victimCue9Records=[f'{r:08X}' for r in voices],victimCue9ChoicesPerGroup=count,
            completeSourceHelpers=reviewed,negativeFaultsRejected=faults,
            implementationRequirements=['Use full priority/time flags:50/56,50/76,41-or42/voice duration,50/102,50/99; low bits are not variation counts.',
                'Preserve five independent source sound slots and derive packet offset from slot, not a hardcoded observed packet.',
                'Source true actor flag chooses victim priority41 versus42; cue9 RNG executes despite one record.',
                'Import complete original PCM sources and verify native sample clocks, full tails, priorities and scene ownership; do not trim/fabricate waveforms.',
                'Native MK2 original DCS byte stores remain untouched; new script markers must not alias stock bytes.',
                'Bone impact cues and later native announcements must coexist, not be removed to isolate a passing laser mix.'],
            limitations=['Sound-none passive packet/state trace is not audible PCM or port audio acceptance.',
                'Only one earned original actor pair/arena; other voice groups source-mapped, not earned runtime cases.',
                'No real all-slots-higher-priority rejection or nonzero continuation stream in this trace.',
                'Whole rasters match viewed earlier trial; no new raw media saved.',
                'All original14requirements and6remaining groups remain; public build unchanged.'],
            originalNaturalIntegrationRequirements=scope['originalNaturalIntegrationRequirements'],
            originalRemainingWorkGroups=scope['originalRemainingWorkGroups'],goalStatus='active',previousGoalTurnClassification='progress',
            inputHashes={str(p.resolve()):sha(p) for p in paths},newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,latestPlayableChanged=False)
        need(len(report['originalNaturalIntegrationRequirements'])==14 and len(report['originalRemainingWorkGroups'])==6,'Full natural-integration scope retained')
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(dict(passed=True,actualAllocatorRecords=39,actualTimerInvocations=301,actualSlotTriples=result['checkedSlotTriples'],
            sourceLaserCues=5,negativeFaultsRejected=len(faults),portAudioAccepted=False)))
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc());raise


if __name__=='__main__':main()
