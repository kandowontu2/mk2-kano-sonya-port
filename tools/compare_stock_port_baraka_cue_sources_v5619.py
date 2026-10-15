"""Every captured Baraka general cue: original producer and native variants.

Do not fit or compare whole-game waveform timing across different actors.
Retain stock/current DAC waveform qualifications and all packet/voice gates.
Bind every observed producer to original code: frame-stream input, literal
blade/head/floor cues, and packed three-choice original random gore helper.
"""
import datetime
import json
import re
import struct
import subprocess
import traceback
from pathlib import Path
import capture_original_mk2_qualified_waveform_v5616 as reference

ROOT,need,sha=reference.ROOT,reference.need,reference.sha
PARENT=reference.OUT/'progress.json'
PORT=ROOT/'audit_v5601_current_native_dac_matrix_progress/progress.json'
OUT=ROOT/'audit_v5620_stock_port_baraka_cue_sources_qualified'
direct=reference.original.direct
rows=reference.original.rows
off=lambda address:(address-0xff800000)//8


def producer(row,guest,stock):
    code=int(row['command'],16);caller=int(row['caller'],16)
    need(code==int(row['a0'],16),'Actual producer command and native entry register identical')
    def exact(address,words,label):
        raw=struct.pack('<'+'H'*len(words),*words);at=off(address)
        need(guest[at:at+len(raw)]==stock[at:at+len(raw)]==raw,'Entire original '+label+' producer program source exact')
    if caller==0xff83be30:
        exact(0xff83bdf0,(0x9720,0x0d5f,0x2530,0xffa1),'animation stream read/postincrement/CALLA')
        need(code in (0x0a13,0x42),'Captured Baraka stream values match original control; not an arbitrary extra cue')
        kind='original animation-stream marker' if code==0x0a13 else 'original animation-stream effect42'
    elif caller==0xff842c50:
        need(code in (0x45,0x46,0x48),'Captured true-victim voice is native male/female selector, never Liu-specific47')
        kind='original true-victim death voice'
    elif caller==0xff8cb6d0:
        exact(caller-80,(0x09c0,0x0044,0x0d5f,0x2530,0xffa1),'literal Baraka blade44/CALLA')
        need(code==0x44,'Actual blade command comes from original literal44')
        kind='original literal blade44'
    elif caller in (0xffa17760,0xffa178c0,0xffa17a10,0xff9adc00):
        expected=0xc4 if caller==0xff9adc00 else 0x1f
        exact(caller-80,(0x09c0,expected,0x0d5f,0x2530,0xffa1),'literal native head/floor cue/CALLA')
        need(code==expected,'Actual head/floor command equals its original literal producer')
        kind='original floor-particle cueC4' if expected==0xc4 else 'original head cue1F'
    elif caller==0xff9ad190:
        exact(caller-32,(0x0d3f,0x037b),'gore CALLR to packed random helper')
        need((caller+0x037b*16)&0xffffffff==0xff9b0940,'Original signed CALLR really targets observed packed helper')
        exact(0xff9b0940,(0x09e0,0x0073,0x0003,0xc080,0x2180,0xffa1),'packed base73/count3 and original random-dispatch jump')
        exact(0xffa12180,(0x4c01,0x2e00,0x0521,0x0d5f,0xeae0,0xff80,0x1420,0x4020,0xc032),
              'packed count/base extraction, native RNG call, decrement/add and original dispatcher jump')
        need(guest[off(0xff80eae0):off(0xff80f000)]==stock[off(0xff80eae0):off(0xff80f000)],
             'Whole original RNG source window unchanged; no forced random state or substitute generator')
        need(code in (0x73,0x74,0x75) and row['a1']=='00000073',
             'Actual original three-choice random gore command and retained native base73')
        kind='original three-choice random gore cue'
    else:
        raise ValueError('Unexplained captured original general producer caller '+row['caller'])
    if code==0x0a13:
        need(row['header']==row['base']=='0000','Original out-of-table animation marker not relabeled as delivered audio')
    else:
        address=0xffa0ef20+code*32
        header,base=struct.unpack_from('<HH',stock,off(address))
        need(row['table']==f'{address:08X}' and int(row['header'],16)==header and int(row['base'],16)==base,
             'Every producer reaches its whole original priority/duration/base command record')
    return dict(kind=kind,command=code,actualCaller=row['caller'],actualEntry=row)


def gate(log,guest,stock):
    calls=rows(log,'MK2_BPRIO_CALL')
    proved=[producer(r,guest,stock) for r in calls]
    original_families=['original animation-stream marker','original true-victim death voice','original literal blade44',
        'original animation-stream effect42','original head cue1F','original head cue1F',
        'original floor-particle cueC4','original floor-particle cueC4','original head cue1F']
    need(len(proved)==17 and [r['kind'] for r in proved]==original_families+['original three-choice random gore cue']*8,
         'All17 actual general calls accounted, including suppressed markers and all eight random descendants; no ignored extra cue')
    return dict(passed=True,actualGeneralCalls=len(calls),producers=proved,
                wholeGameWaveformIdentityRequired=False,wholeGameWaveformEqualityClaimed=False)


def faults(log,guest,stock):
    positive=gate(log,guest,stock);rejected=[]
    source_targets=((0xff83bdf0,'animation stream input instruction'),(0xff8cb680,'fixed blade literal'),
        (0xffa17710,'first head literal'),(0xffa17870,'second head literal'),(0xffa179c0,'third head literal'),
        (0xff9adbb0,'floor literal'),(0xff9ad170,'actual random-helper CALLR'),
        (0xff9b0960,'packed random count3'),(0xffa12190,'packed random count extraction'),
        (0xffa121e0,'native RNG decrement'),(0xff80eae0,'original RNG source'))
    for address,label in source_targets:
        bad=bytearray(guest);bad[off(address)]^=1
        try:gate(log,bytes(bad),stock)
        except ValueError as error:rejected.append(dict(label=label,rejectedBy=str(error),kind='verifier RAM source only'))
        else:raise ValueError('Accepted corrupted original cue producer source')
    original=next(s for s in log.splitlines() if s.startswith('MK2_BPRIO_CALL ') and 'caller=FF9AD190' in s)
    for code in (0x72,0x76):
        bad=re.sub(r'(?<!\w)(command|a0)=[^\s]+',lambda m:m[1]+f'={code:08X}',original)
        need(bad!=original,'Effective actual native cue record corruption')
        try:gate(log.replace(original,bad,1),guest,stock)
        except ValueError as error:rejected.append(dict(label=f'actual random selector outside original73..75: {code:02X}',rejectedBy=str(error),kind='actual captured record copy'))
        else:raise ValueError('Accepted out-of-range native random gore cue')
    need(gate(log,guest,stock)==positive,'Whole actual producer positive restored after thirteen effective source/record faults')
    return rejected


def run():
    parent,port=(json.loads(p.read_text()) for p in (PARENT,PORT))
    need(parent['passed'] and parent['sourceQualifiedOriginalMixedWaveformAccepted'] and port['passed']
         and parent['remaining']==port['remaining'] and len(parent['remaining'])==5,
         'Actual qualified stock and four-context current waveform proof retained; all original remaining groups intact')
    pins=dict(parent['newInputHashes']);pins.update(port['newInputHashes'])
    for p in (PARENT,PORT,Path(__file__),Path(reference.__file__)):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'All immutable stock/current/public inputs exact before no-replay source comparison')
    stock=reference.original.STOCK.read_bytes()
    current=reference.original.clock.original.capture.original.model.current.expected()
    specs=[('original_cage',1,reference.FOLDER,stock),
        ('kano',1,ROOT/'audit_v5597_current_native_dac_clock_ram/kano_p1_samples',current),
        ('kano',2,ROOT/'audit_v5600_current_native_dac_matrix_ram/kano_p2_samples',current),
        ('sonya',1,ROOT/'audit_v5600_current_native_dac_matrix_ram/sonya_p1_samples',current),
        ('sonya',2,ROOT/'audit_v5600_current_native_dac_matrix_ram/sonya_p2_samples',current)]
    results=[]
    for name,side,folder,guest in specs:
        log=(folder/'run.log').read_text();meta=json.loads((folder/'result.json').read_text())
        need(meta['passed'] and 'MK2_STOCK_HEAD_V921_RESULT frame=5198' in log
             and not (folder/'stderr.log').read_text(),'Same genuinely completed native physical run, not a synthetic trace')
        proved=gate(log,guest,stock);rejected=faults(log,guest,stock)
        if name!='original_cage':
            voices=direct.observed.prior.routes.gate(log,guest,name,side)
            packets=direct.gate(log,guest)
        else:
            voices=parent['originalPacketQualification']['proof']['actualWholePacketOriginProof']['retainedQualifiedDualDispatcher']
            packets=reference.qualified.previous.scope['packet_gate'](log,guest)['proof']
        need(packets['passed'] and len(rejected)==13,'Full actual packet/queue/priority/port/ADSP gate plus every new producer fault')
        for p in (folder/'run.log',folder/'result.json',folder/'terminal.json',folder/'stderr.log'):
            pins[str(p.resolve())]=sha(p)
        results.append(dict(fighter=name,side=side,nativeCaptureResult=str(folder/'result.json'),
            originalCueProducerProof=proved,effectiveProducerFaults=rejected,retainedWholePacketProof=packets,
            retainedTrueVoiceOrStockDispatcherProof=voices))
    need(all(sha(p)==h for p,h in pins.items()),'Every unchanged stock/current/public/source/evidence byte exact after qualification')
    return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
        remaining=parent['remaining'],parentAdditiveJournal=str(PARENT),retainedPortWaveformJournal=str(PORT),
        previousGoalTurnClassification=parent['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: all85 actual original/current general sound calls across original Cage and both added victims/both slots source-accounted; native frame input, fixed blade/head/floor producers and complete packed3-choice/RNG/dispatcher source independently bound.65new effective producer source/record faults retained with whole actual true-victim voice/priority/packet/full-word/return/ADSP and qualified stock/current DAC waveform proofs. Natural voice, suppression, geometry-field and RNG differences explicitly not whole-waveform equality or fitted away.',
        cases=results,actualGeneralProducerCalls=85,effectiveActualProducerFaults=65,
        allCapturedGeneralCueProducersSourceAccounted=True,sourceQualifiedOriginalMixedWaveformAccepted=True,
        completeBarakaFinisherAudioAccepted=False,allOtherBranchVictimStageAudioAccepted=False,
        wholeGameWaveformEqualityClaimed=False,fullPortAcceptance=False,
        newNativeBoots=0,newBuilds=0,newDeletedFiles=0,requestedRawGuestGFXVRAMRGBPCMFilesWritten=0,
        publicPlayableChanged=False,refreshedReleaseZIP=False,newInputHashes=pins,
        nextAction='Advance original female stock control and remaining native victim/stage/audio cases as needed; retain completed source-owned observed Baraka cue/voice/priority/packet/DAC/mixer proof and move forward on all original move/shadow/CPU/finisher/morph/secret/cinematic/campaign/UI/cleanup/release requirements. No whole-game waveform equality or timing/gain fit is a substitute for source ownership.')


if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable complete stock/current native producer comparison')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();reference.original.save(OUT/'progress.json',report)
    paths=[Path(__file__),OUT/'progress.json'];frozen={str(p):sha(p) for p in paths}
    done=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',*[str(p) for p in paths]],capture_output=True)
    need(done.returncode==0 and all(sha(p)==h for p,h in frozen.items()),'New source and evidence losslessly compressed')
    print(json.dumps({k:report[k] for k in ('passed','error','actualGeneralProducerCalls','effectiveActualProducerFaults') if k in report},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
