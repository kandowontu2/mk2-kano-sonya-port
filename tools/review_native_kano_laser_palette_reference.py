"""Actual original laser victim ramp, resolved by continuous native fields.

All27 real RGB frames inspected in RAM. This accepts original reference
evidence only, never the port finisher or its audio implementation.
"""
import gzip
import json
import re
import struct
from pathlib import Path
import capture_native_kano_laser_palette_trace as host

ROOT=host.ROOT
OUT=ROOT/'audit_native_kano_laser_palette_reference_review'
need,sha=host.reference.need,host.reference.sha

def rows(text,tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in text.splitlines()
            if line.startswith('MK3_SECONDARY_'+tag+' ')]

def ramp(color,intensity):
    return (min(31,(color>>10&31)+intensity)<<10)|(max(0,(color>>5&31)-intensity)<<5)|max(0,(color&31)-intensity)

def palette_contract(text,program):
    fields=[r for r in rows(text,'PALETTE_FIELD') if r['side']=='2']
    need(len(fields)==150 and [int(r['age']) for r in fields]==list(range(1,151)),
         'Actual victim colors continuously sampled, not only when its pose changes')
    at=(0xffc96790-0xff800000)//8
    count=struct.unpack_from('<H',program,at)[0]
    need(count==64,'Actual original victim palette has64colors')
    colors=struct.unpack_from('<64H',program,at+2)
    table=struct.unpack_from('<12H',program,(0xff9b6200-0xff800000)//8)
    need(table==(1,2,4,6,8,10,12,14,16,18,20,0xffff),'Original finite native red intensity table')
    levels=table[:-1];codes=rows(text,'RAMP_CODE')
    constructor=[r for r in codes if r['at']=='FF92B890']
    need(len(constructor)==1 and constructor[0]['age']=='68' and constructor[0]['a0']=='00000606' and
         constructor[0]['a5']=='00000006' and constructor[0]['a10']=='00000001' and constructor[0]['a11']=='FF9B6200',
         'Actual victim palette constructor begins at laser contact68, cadence6/method1/source table')
    tasks=[r for r in codes if r['at']=='FF92BB80']
    need(len(tasks)==11 and [int(r['age']) for r in tasks]==[68+6*i for i in range(11)] and
         len({r['a13'] for r in tasks})==1 and all(r['a1']=='FFC96790' and r['a9']=='00000600' for r in tasks) and
         [r['a11'] for r in tasks]==[f'{0xff9b6200+i*16:08X}' for i in range(11)],
         'One original palette worker consumes every source intensity once at6field cadence')
    queue=[r for r in codes if r['at']=='FF925320' and r['a1']=='00000600']
    need(len(queue)==11 and [int(r['age']) for r in queue]==[68+6*i for i in range(11)] and
         all(r['a0']==f'{int(tasks[0]["a13"],16)+0x110:08X}' for r in queue),'Actual finite native transfer queue owns worker scratch palette')
    for r in fields:
        age=int(r['age']);intensity=0 if age<70 else levels[min(10,(age-70)//6)]
        observed=tuple(int(c,16) for c in r['colors'].split(','))
        need(r['bank']=='0600' and observed==tuple(ramp(c,intensity) for c in colors),
             'Every actual victim color equals original red-clamp/green-blue-subtract source arithmetic')
    writes=rows(text,'RAMP_WRITE')
    need(len(writes)==11*64,'All64hardware colors transferred for every11original intensity levels')
    for i,intensity in enumerate(levels):
        own=[r for r in writes if int(r['age'])==69+6*i]
        need(len(own)==64 and sorted(int(r['pen']) for r in own)==list(range(64)) and
             all(r['bank']=='0600' and r['mask']=='FFFF' and int(r['data'],16)==ramp(colors[int(r['pen'])],intensity) for r in own),
             'Every native hardware write is the exact next-field palette transfer, not an inferred appearance')
    return dict(victimConstructor=constructor[0],worker=tasks[0]['a13'],sourcePalette='FFC96790',
                sourceColors=64,sourceIntensityTable=list(table),contactAge=68,hardwareWriteAges=[69+6*i for i in range(11)],
                firstContinuousSampleWithRedAge=70,lastIntensitySampleAge=130,continuousVictimFields=150,
                exactHardwareWrites=704,sourceArithmetic='red+=intensity clamp31; green/blue-=intensity floor0',
                paletteWorkerSteps=tasks)

def main():
    need(not OUT.exists() and not host.reference.census() and not host.reference.process.census(),
         'Fresh independent reference review; all actual native games terminal')
    folder=ROOT/'audit_native_kano_laser_palette_trace'
    report=json.loads((folder/'report.json').read_text());text=gzip.open(folder/'run.log.gz','rt').read()
    need(report['passed'] and report['nativeExit']==0 and report['originalWholeGuestMatched'] and
         all(sha(p)==h for p,h in report['inputHashes'].items()),'Actual original whole program and executed source inputs preserved')
    program=(ROOT/'mk3/mk3-maincpu.bin').read_bytes();contract=palette_contract(text,program)
    entry=rows(text,'OWN_ENTRY');stop=rows(text,'STOP');frames=rows(text,'RGB_DIGEST')
    need(len(entry)==len(stop)==1 and entry[0]['ids']=='0,1' and entry[0]['hp']=='166,0' and
         stop[0]['zeros']=='2' and stop[0]['own_action_observed']=='1' and len(frames)==27,
         'Two physically earned rounds, real original actor identities, same native handle terminal, all27RGBframes')
    faults=[]
    for name,wrong in [('early_contact_ramp',text.replace('age=68 at=FF92B890','age=20 at=FF92B890')),
        ('wrong_worker_palette',text.replace('a1=FFC96790','a1=FFC967A0')),
        ('wrong_hardware_color',text.replace('pen=0 data=0400','pen=0 data=0000'))]:
        try:palette_contract(wrong,program)
        except ValueError as error:faults.append(dict(name=name,rejected=str(error)))
        else:raise ValueError('Incorrect original ramp evidence accepted: '+name)
    paths=[Path(__file__),folder/'report.json',folder/'run.log.gz',folder/'executed_sources.json.gz',ROOT/'mk3/mk3-maincpu.bin']
    OUT.mkdir()
    result=dict(passed=True,originalLaserVictimRampReferenceAccepted=True,portImplementationAccepted=False,
        fullPortAcceptance=False,actualWindowsIdentity=report['actualWindowsIdentity'],originalOwnEntry=entry[0],
        nativeStop=stop[0],nativePaletteContract=contract,actualRGBFrames=frames,actualFramesVisuallyReviewed=27,
        visualObservation='Victim stays ordinary through laser startup; becomes increasingly red after hit, then native bone/grey-cloud burst. Own laser retires and original continue appears.',
        resolvedDiscrepancy='Previous pose-change observer sampled unchanged colors through68 and stopped sampling the unchanged victim pose during its later ramp. Constructor starts68, not20.',
        rejectedFaults=faults,inputHashes={str(p.resolve()):sha(p) for p in paths},goalStatus='active',
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,latestPlayableChanged=False,
        limitations=['Original Kano versus original Sonya reference only. Native port choreography, victim bodies, palette ownership and audio still require implementation/verification.'])
    (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(passed=True,contactAge=68,colorsChecked=150*64,hardwareWrites=704,reviewedFrames=27,portAccepted=False)))

if __name__=='__main__':main()
