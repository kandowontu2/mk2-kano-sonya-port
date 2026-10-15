"""Actual original packet call/return origins, full prior gates retained.

One physical Kano-P1 run, two additional passive taps. No game edits/builds,
no raw guest/media files. Direct packet semantics and full waveforms remain
unaccepted until the newly observed actual original callers are decoded.
"""
import datetime, json, re, struct, subprocess, traceback
from pathlib import Path
from PIL import Image
import qualify_current_baraka_announcer_v5571 as announcer

capture, prior = announcer.capture, announcer.prior
ROOT, need, sha = announcer.ROOT, announcer.need, announcer.sha
PARENT = ROOT / 'audit_v5575_current_baraka_announcer_matrix_progress/progress.json'
BASE = ROOT / 'audit_v5578_current_baraka_packet_origin_ram'
OUT = ROOT / 'audit_v5579_current_baraka_packet_origin_progress'
LUA = ROOT / 'mk2ks_current_baraka_packet_origin_v5576.lua'
COMPLETED = []
capture.capture.__globals__.update(BASE=BASE,LUA=LUA,COMPLETED=COMPLETED)


def rows(log, tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)', s)) for s in log.splitlines() if s.startswith('MK2_PORIGIN_' + tag + ' ')]


def gate(log, guest):
    ann = announcer.gate(log, guest)
    entries, ends = rows(log,'ENTRY'), rows(log,'END')
    packets, writes, delivery = (capture.rows(log,t) for t in ('PACKET','SOUND','DELIVERY'))
    keys = ('frame','seconds','entry','a1','a3','a4','a8','a13')
    tuples = lambda rs:[tuple(r[k] for k in keys) for r in rs]
    need(tuples(entries) == tuples(packets) and [int(r['serial']) for r in entries] == list(range(1,len(entries)+1))
         and len(ends) == len(entries) > 20, 'Every original actual packet independently entry-inventoried and completed')
    stock = (ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for first,last in ((0xffa13ba0,0xffa13e70),):
        need(guest[prior.off(first):prior.off(last)] == stock[prior.off(first):prior.off(last)],
             'Entire original packet save/mute/bytes/ack/restore/return program')
    need(len(writes) == 2*len(entries), 'Every actually unmuted native packet has exactly two original port writes')
    selected = {r['packet']['seconds'] for r in ann['delivered']}
    records = []
    for i,e in enumerate(entries):
        completion = [r for r in ends if r['serial'] == e['serial']]
        need(len(completion) == 1 and completion[0]['entry'] == 'FFA13DD0'
             and all(completion[0][k] == e[k] for k in ('frame','a1','a3','a4','a8','a13','sp','return_pc','mute'))
             and float(e['seconds']) < float(completion[0]['seconds']),
             'Actual packet owner/task/caller/stack/full saved registers restored at genuine native RETS')
        need(e['mute'] == '0000' and e['writes'] == '0' and e['assistance'] == 'none',
             'Real unmuted native packet; observer never writes or assists')
        first,last = float(e['seconds']),float(completion[0]['seconds'])
        ports = writes[2*i:2*i+2]
        word = int(e['a3'],16)
        need(0 <= word <= 65535 and all(first < float(w['seconds']) < last for w in ports)
             and all(all(w[k] == e[k] for k in ('frame','a8','a13')) and w['mask'] == 'FFFF' for w in ports)
             and [w['pc'] for w in ports] == ['FFA13C90','FFA13D60']
             and [int(w['word'],16)&255 for w in ports] == [word>>8,word&255],
             'Every full native packet, including direct controls, exact high/low bytes and actual original writer/context')
        consumed = []
        for j,w in enumerate(ports):
            index = 2*i+j
            deadline = float(writes[index+1]['seconds']) if index+1 < len(writes) else float(w['seconds'])+.1
            hits = [d for d in delivery if float(w['seconds']) <= float(d['seconds']) < deadline
                    and int(d['word'],16) == int(w['word'],16)&255]
            need(hits, 'Every actual original packet byte read by native ADSP before next port write')
            consumed.append(hits[0])
        pc = int(e['return_pc'],16)
        need(0xff800030 <= pc <= 0xfffffe00 and pc%16 == 0, 'Actual original packet caller is an aligned guest-ROM address')
        offset = prior.off(pc-48)
        need(guest[offset:offset+22] == stock[offset:offset+22], 'Actual packet caller instruction/continuation bytes remain whole original source')
        a,b,c = struct.unpack_from('<3H',guest,offset)
        if a == 0x0d5f:
            instruction = dict(kind='CALLA',target=f'{b|(c<<16):08X}')
        elif b == 0x0d3f:
            displacement = struct.unpack('<h',struct.pack('<H',c))[0]
            instruction = dict(kind='CALLR',target=f'{(pc+displacement*16)&0xffffffff:08X}')
        else:
            instruction = dict(kind='unclassified original stack continuation',target=None)
        records.append(dict(actualEntry=e,actualCompletion=completion[0],actualPorts=ports,actualDSPReads=consumed,
                            originalCallerInstruction=instruction,priorityPath=e['seconds'] in selected))
    terminal = rows(log,'RESULT')
    need(len(terminal) == 1 and terminal[0]['frame'] == '5198' and terminal[0]['calls'] == str(len(entries))
         and terminal[0]['pending'] == '0', 'All actual packet entries genuinely retired at native5198 terminal')
    direct = [r for r in records if not r['priorityPath']]
    need(len(direct) == ann['directPacketProgramsOutsidePriorityPath'] == 4,
         'Complete real four direct packet observations; not inferred from packet value or sound')
    return dict(passed=True,actualPacketCalls=len(entries),allObservedPacketsCompleteAndDelivered=True,
        actualPackets=records,actualDirectPackets=direct,retainedQualifiedDualDispatcher=ann,
        allDirectPacketSourceSemanticsAccepted=False,sourceQualifiedNativeDCSWaveformAccepted=False,fullPortAcceptance=False)


def faults(log, guest):
    positive = gate(log,guest)
    record = positive['actualDirectPackets'][0]
    cases = []

    def change(label,tag,row,key,value):
        line = next(s for s in log.splitlines() if s.startswith(tag+' ') and dict(re.findall(r'(\w+)=([^\s]+)',s)) == row)
        damaged,n = re.subn(r'(?<!\w)'+key+r'=[^\s]+',key+'='+value,line)
        need(n == 1 and damaged != line, 'Effective actual direct-packet record fault')
        cases.append((label,log.replace(line,damaged,1)))

    e,end = record['actualEntry'],record['actualCompletion']
    change('wrong actual packet caller','MK2_PORIGIN_ENTRY',e,'return_pc','00000000')
    change('wrong actual packet word','MK2_PORIGIN_ENTRY',e,'a3','00000001')
    change('foreign actual packet actor','MK2_PORIGIN_ENTRY',e,'a8','01000000')
    change('foreign actual packet task','MK2_PORIGIN_ENTRY',e,'a13','01000000')
    change('packet stack not restored','MK2_PORIGIN_END',end,'sp','01000000')
    change('packet caller not restored','MK2_PORIGIN_END',end,'return_pc','00000000')
    change('wrong packet native return instruction','MK2_PORIGIN_END',end,'entry','FFA13DE0')
    change('direct packet byte corrupted','MK2_MAUDIO_SOUND',record['actualPorts'][0],'word','0001')
    final = rows(log,'RESULT')[0]
    change('actual native pending packet at terminal','MK2_PORIGIN_RESULT',final,'pending','1')
    line = next(s for s in log.splitlines() if s.startswith('MK2_PORIGIN_END ') and dict(re.findall(r'(\w+)=([^\s]+)',s)) == end)
    cases.append(('one actual direct packet completion omitted',log.replace(line+'\n','',1)))
    rejected = []
    for label,bad in cases:
        need(bad != log, 'Actual direct packet record changed')
        try:gate(bad,guest)
        except ValueError as error:rejected.append(dict(label=label,rejectedBy=str(error)))
        else:raise ValueError('Accepted actual packet origin fault: '+label)
    need(gate(log,guest) == positive, 'Whole positive packet-origin/return/delivery gate restored after actual faults')
    return rejected


def run():
    guest = capture.original.model.current.expected()
    parent = json.loads(PARENT.read_text())
    need(parent['passed'] and parent['goalStatus'] == 'active'
         and parent['allNormalBarakaVictimsAndSlotsObservedAnnouncerPriorityDeliveryAccepted'],
         'Completed actual both-victim/slot announcer proof and complete original remaining scope retained')
    pins = dict(parent['newInputHashes'])
    for p in (PARENT,Path(__file__),LUA,Path(announcer.__file__),Path(announcer.observed.__file__)):
        pins[str(p.resolve())] = sha(p)
    need(all(sha(p) == h for p,h in pins.items()), 'All current/public/source/evidence exact before one original physical boot')
    payload = (ROOT/capture.original.model.current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    reference,gfx = capture.original.model.source_art(guest,payload,pins)
    image = capture.original.transport.source_graphics(payload,pins)
    record = capture.capture(('kano',1),guest,payload,gfx,reference,pins,image,True)
    meta,log,folder = record['final'],record['log'],record['folder']
    positive = gate(log,guest)
    rejected = faults(log,guest)
    ann_faults = announcer.faults(log,guest)
    priority_faults = announcer.observed.qualified.faults(log,guest)
    coverage = prior.phase.coverage(log,meta)
    voice = prior.routes.gate(log,guest,'kano',1)
    old = json.loads((ROOT/'audit_v5567_current_baraka_announcer_ram/kano_p1_samples/result.json').read_text())
    need(meta['actualDisplayHeaders'] == old['actualDisplayHeaders']
         and meta['actualMixedPCMSHA256'] == old['actualMixedPCMSHA256']
         and meta['actualPCMUpdates'] == old['actualPCMUpdates'] and meta['actualPCMBytes'] == old['actualPCMBytes'],
         'Every125 native whole raster and full joined actual PCM unchanged by passive packet stack/return observers')
    pngs,compacted = [],[]
    for p in sorted(folder.rglob('*')):
        if not p.is_file():continue
        need(p.suffix.lower() not in ('.bin','.wav','.rgb','.pcm'), 'No requested raw guest/GFX/raster/audio files')
        if p.suffix.lower() == '.png':
            with Image.open(p) as im:
                need(p == folder/'snap/mk2ks/0000.png' and im.size == (400,254), 'Only original automatic native timed-exit PNG')
            pngs.append(dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)))
        if p.suffix.lower() in ('.log','.json','.cfg','.txt'):
            before = sha(p);cp = subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True)
            need(cp.returncode == 0 and sha(p) == before, 'Sealed native logs truly force-LZX compressed, all bytes unchanged')
            compacted.append(str(p))
        pins[str(p.resolve())] = sha(p)
    need(len(pngs) == 1 and all(sha(p) == h for p,h in pins.items()), 'One native timed PNG and exact source/current/public/evidence pins')
    return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
        remaining=parent['remaining'],parentAdditiveJournal=str(PARENT),previousGoalTurnClassification=parent['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: actual original every-packet entry/caller/stack/return independently recorded, complete direct control packets and priority packets high/low/ADSP delivered;10new actual packet-origin faults plus12announcer/22priority faults, original full native physical/art/source voice/timer/RGB/PCM nonperturbance retained; exact direct original callers now available for semantic source decoding',
        actualPacketOrigins=positive,effectiveActualPacketOriginFaults=rejected,retainedActualAnnouncerFaults=ann_faults,
        retainedActualPriorityFaults=priority_faults,actualTimerCoverage=coverage,actualSourceVoiceEffectRoutes=voice,
        nativeCaptureResult=str(folder/'result.json'),persistentNativeAutomaticExitPNGs=pngs,
        persistentNativeAutomaticPNGBytes=sum(p['bytes'] for p in pngs),terminalTextFilesForceLZXCompacted=len(compacted),
        newNativeBoots=1,newBuilds=0,newDeletedFiles=0,publicPlayableChanged=False,refreshedReleaseZIP=False,
        requestedRawGuestGFXVRAMRGBPCMFilesWritten=0,allDirectPacketSourceSemanticsAccepted=False,
        sourceQualifiedNativeDCSWaveformAccepted=False,completeBarakaFinisherAudioAccepted=False,fullPortAcceptance=False,
        newInputHashes=pins,nextAction='Decode actual four original direct packet caller targets and control-word semantics from stock source; qualify source counterexamples without replay, then extend contexts and original waveform/all remaining requirement groups.')


if __name__ == '__main__':
    need(not OUT.exists() and not BASE.exists(), 'Fresh immutable actual native packet-origin capture')
    try:report=run()
    except Exception as error:
        report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completedNativeCaptures=COMPLETED,
                    goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();capture.save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items() if k not in ('remaining','newInputHashes','actualPacketOrigins',
        'effectiveActualPacketOriginFaults','retainedActualAnnouncerFaults','retainedActualPriorityFaults',
        'actualTimerCoverage','actualSourceVoiceEffectRoutes','completedNativeCaptures')},indent=2),flush=True)
    raise SystemExit(0 if report['passed'] else 1)
