"""Original direct packet source and full16-bit port words; no replay.

Whole5577 origin/return/ADSP plus prior physical/art/voice/announcer proofs
retained. Independently encode complete reset and conditional finisher-wrap
programs; bind real caller and flags, not merely a matching packet value.
"""
import copy, datetime, json, re, struct, subprocess, traceback
from pathlib import Path
import current_baraka_packet_origin_capture_v5577 as observed

ROOT, need, sha = observed.ROOT, observed.need, observed.sha
prior, capture = observed.prior, observed.capture
PARENT = observed.OUT/'progress.json'
OUT = ROOT/'audit_v5581_current_baraka_direct_packets_qualified'


def direct_source(entry, guest):
    pc = int(entry['return_pc'],16)
    stock = (ROOT/'mk2/mk2-maincpu.bin').read_bytes()

    def exact(address,words,label):
        raw = struct.pack('<' + 'H'*len(words),*words);at = prior.off(address)
        need(guest[at:at+len(raw)] == stock[at:at+len(raw)] == raw, 'Entire original '+label+' program source exact')

    if pc == 0xffa13070:
        exact(0xffa13020,(0x098f,0xc000,0x5663,0x0d3f,0x00b3,0x0d3f,0x0003,0x09af,0x0003,0x0960,
             0x5600,0x09e1,0x8100,0x010b,0x9001,0x0b61,0x7dff,0xfef4,0xcbfb,0x0960),
             'reset packet plus four-slot clearing')
        expected,kind = 0,'native reset packet and original slot-reset routine'
    elif pc in (0xff8cdc10,0xff82cb70):
        expected = 0x34 if pc == 0xff8cdc10 else 0x38
        exact(pc-80,(0x09c3,expected,0x0d5f,0x3ba0,0xffa1),'literal direct packet setter/CALLA')
        if pc == 0xff8cdc10:
            exact(0xff8cdb70,(0x09c0,0x0002,0x0d5f,0xdcc0,0xff80),'two-field native delay before packet34')
        kind = 'native delayed direct packet34' if expected == 0x34 else 'native continuation direct packet38'
    elif pc == 0xff8cdd90:
        exact(0xff8cdc40,(0x05a1,0x19c0,0x0106,0x09c0,0xffff,0x0580,0x19c0,0x0106,
             0x0b41,0xfff8,0xca0a,0x09c3,0x0035,0x0b41,0xfffa,0xcb02,0x09c3,0x003f,
             0x0d5f,0x3ba0,0xffa1,0x0960),'finisher-end flag7 skip/flag5 packet3F/otherwise35')
        flag = int(entry['a1'],16)
        need(flag != 7,'Original flag7 returns without creating a direct packet')
        expected = 0x3f if flag == 5 else 0x35
        kind = 'native finisher-end flag-dependent direct packet'
    else:
        raise ValueError('Unexplained original direct packet source caller '+entry['return_pc'])
    need(int(entry['a3'],16) == expected,'Actual direct packet word equals complete original caller program and actual branch flags')
    return dict(passed=True,kind=kind,originalCaller=f'{pc:08X}',originalExpectedPacket=f'{expected:04X}',actualEntry=entry)


def gate(log,guest):
    # Semantic checks run on actual source-entry records before generic packet
    # checks; same low byte is insufficient when original ADDI addsFF00.
    selected = {r['packet']['seconds'] for r in observed.announcer.gate(log,guest)['delivered']}
    direct_entries = [r for r in observed.rows(log,'ENTRY') if r['seconds'] not in selected]
    source = [direct_source(e,guest) for e in direct_entries]
    need(len(source) == 4 and [r['originalCaller'] for r in source] == ['FFA13070','FF8CDC10','FF8CDD90','FF82CB70'],
         'All actual direct caller programs, in complete native order; no guessed or ignored packets')
    need(int(direct_entries[1]['frame']) == int(direct_entries[0]['frame'])+2
         and all(direct_entries[0][k] == direct_entries[1][k] for k in ('a8','a13')),
         'Actual reset and delayed34 are the same native task exactly two original fields apart')
    positive = observed.gate(log,guest)
    for record in positive['actualPackets']:
        word = int(record['actualEntry']['a3'],16)
        need([int(w['word'],16) for w in record['actualPorts']] == [0xff00|(word>>8),0xff00|(word&255)],
             'Every full16-bit original port word, includingFF00 prefix, source-exact; not just matching low byte')
    return dict(passed=True,actualPacketCalls=positive['actualPacketCalls'],actualDirectPacketSources=source,
        allCapturedOriginalPacketsSourceBoundAndDelivered=True,actualWholePacketOriginProof=positive,
        allOtherVictimSlotsAccepted=False,allNativeBranchCombinationsAccepted=False,
        fullOriginalDCSWaveformAccepted=False,fullPortAcceptance=False)


def faults(log,guest):
    positive = gate(log,guest);sources = positive['actualDirectPacketSources']
    source_faults = []
    for row,key,value,label in ((sources[0],'a3','00000001','reset does not send zero'),
                                (sources[1],'return_pc','FF82CB70','34 falsely attributed to38 setter'),
                                (sources[2],'a1','00000005','flag5 must choose3F, not35'),
                                (sources[2],'a1','00000007','flag7 must not send a packet'),
                                (sources[2],'a3','0000003F','normal branch falsely sends3F'),
                                (sources[3],'a3','00000034','continuation falsely sends34')):
        changed = dict(row['actualEntry']);need(changed[key] != value,'Effective source-entry counterexample')
        changed[key] = value
        try:direct_source(changed,guest)
        except ValueError as error:source_faults.append(dict(label=label,rejectedBy=str(error)))
        else:raise ValueError('Accepted actual-entry source prediction fault')
    for address,label in ((0xffa13040,'reset CLR A3 corrupted'),(0xff8cdbc0,'literal34 setter corrupted'),
                           (0xff8cdcc0,'flag7 comparison corrupted'),(0xff8cdd40,'flag5 packet3F setter corrupted'),
                           (0xff82cb20,'literal38 setter corrupted')):
        bad = bytearray(guest);bad[prior.off(address)] ^= 1
        try:gate(log,bytes(bad))
        except ValueError as error:source_faults.append(dict(label=label,rejectedBy=str(error),kind='independent source bytes in verifier RAM only'))
        else:raise ValueError('Accepted original direct program source corruption')
    actual = positive['actualWholePacketOriginProof']['actualDirectPackets'][0]['actualPorts'][0]
    line = next(s for s in log.splitlines() if s.startswith('MK2_MAUDIO_SOUND ') and dict(re.findall(r'(\w+)=([^\s]+)',s)) == actual)
    low = int(actual['word'],16)&255
    changed,n = re.subn(r'(?<!\w)word=[^\s]+',f'word={low:04X}',line)
    need(n == 1 and changed != line,'Actual packet port prefix corrupted while low byte stays exactly unchanged')
    try:gate(log.replace(line,changed,1),guest)
    except ValueError as error:source_faults.append(dict(label='full16-bit port prefix corrupted with unchanged low byte',rejectedBy=str(error),kind='effective actual port record'))
    else:raise ValueError('Accepted non-native port prefix despite identical low byte')
    need(gate(log,guest) == positive,'Whole complete native/source/prefix/return/delivery positive restored after faults')
    return source_faults


def run():
    guest = capture.original.model.current.expected();parent = json.loads(PARENT.read_text())
    need(parent['passed'] and parent['goalStatus'] == 'active'
         and parent['actualPacketOrigins']['allObservedPacketsCompleteAndDelivered'],
         'Preserve actual completed packet-origin capture and full original remaining scope')
    pins = dict(parent['newInputHashes'])
    for p in (PARENT,Path(__file__),Path(observed.__file__),observed.LUA,ROOT/'mame-mkp/unidasm.exe'):
        pins[str(p.resolve())] = sha(p)
    need(all(sha(p) == h for p,h in pins.items()), 'All immutable current/public/source/native capture inputs exact before qualification')
    folder = Path(parent['nativeCaptureResult']).parent
    meta = json.loads((folder/'result.json').read_text());terminal = json.loads((folder/'terminal.json').read_text())
    log = (folder/'run.log').read_text()
    need(meta['passed'] and terminal == meta['process'] and terminal['exit_code'] == 0
         and 'MK2_STOCK_HEAD_V921_RESULT frame=5198' in log and 'Average speed:' in log
         and not (folder/'stderr.log').read_text(), 'Actual native capture terminal0 and5198, not an observation timeout')
    positive = gate(log,guest);rejected = faults(log,guest)
    need(len(rejected) == 12 and observed.gate(log,guest) == parent['actualPacketOrigins'],
         'All twelve new effective source/branch/prefix faults; entire previously executed packet proof unchanged')
    need(all(sha(p) == h for p,h in pins.items()), 'Every actual source/capture/current/public byte unchanged after qualification')
    return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',
        remaining=parent['remaining'],parentAdditiveJournal=str(PARENT),previousGoalTurnClassification=parent['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: actual four direct reset/delay34/flag-dependent35-or3F/continuation38 callers bound to complete original programs and real branch flags, exactly two native reset-delay fields; all actual native port words verified full16-bitFF00 prefix rather than low byte alone;12source/branch/prefix faults rejected without replay; complete prior physical/art/packet/announcer/priority/timer/voice/RGB/PCM proof retained',
        actualOriginalDirectPacketSources=positive,effectiveDirectSourceBranchAndPortFaults=rejected,
        retainedNativeCaptureResult=parent['nativeCaptureResult'],newNativeBoots=0,newBuilds=0,newDeletedFiles=0,
        publicPlayableChanged=False,refreshedReleaseZIP=False,requestedRawGuestGFXVRAMRGBPCMFilesWritten=0,
        allCapturedKanoP1NormalBarakaDirectPacketSourceSemanticsAccepted=True,
        allDirectPacketsAllContextsAccepted=False,sourceQualifiedNativeDCSWaveformAccepted=False,
        completeBarakaFinisherAudioAccepted=False,fullPortAcceptance=False,newInputHashes=pins,
        nextAction='Extend actual original direct packet source/branch/full-word/return delivery to both victims and slots, then independently qualify full original DCS waveform and continue all original remaining requirement groups.')


if __name__ == '__main__':
    need(not OUT.exists(),'Fresh immutable direct packet source qualification')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();capture.save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items() if k not in ('remaining','newInputHashes','actualOriginalDirectPacketSources',
        'effectiveDirectSourceBranchAndPortFaults')},indent=2),flush=True)
    raise SystemExit(0 if report['passed'] else 1)
