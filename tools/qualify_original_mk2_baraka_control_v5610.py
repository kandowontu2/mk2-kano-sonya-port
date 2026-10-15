"""Qualify completed genuine stock control without replay or raw buffers.

Preserve both failures. The actual original BBBB parser chooses its direction
history, not a slot-specific constant. Original name dispatch indexes its
stock ID/name table, not the import trampoline or a literal MOVI9. All old
packet/priority/queue/return/full-port/ADSP algorithms remain intact.
"""
import datetime
import inspect
import json
import re
import struct
import subprocess
import traceback
from pathlib import Path
import capture_original_mk2_native_tables_v5607 as capture

original = capture.original
direct = original.direct
ROOT, need, sha = original.ROOT, original.need, original.sha
FOLDER = capture.FOLDER
FAILURE = capture.OUT / 'progress.json'
OUT = ROOT / 'audit_v5611_original_mk2_baraka_control_qualified'

source = inspect.getsource(original.physical)
before = """    need(any(r['button'] == 'High_Punch' and int(r['slot']) == 2 and start-15 <= int(r['frame']) <= start for r in inputs)
         and any(r['button'] == 'Block' and int(r['slot']) == 2 and start-40 <= int(r['frame']) <= start for r in inputs)
         and any(r['table'] == 'FF87A9A0' for r in records('PARSER')),
         'Original P2 Baraka physical Block/BBBB/HP native parser, never injected action')"""
after = """    approach = records('APPROACH')
    need(len(approach) == 1 and 60 <= int(approach[0]['gap']) <= 68,
         'Actual original finisher distance reached using controller movement')
    a = int(approach[0]['frame'])
    need(start == a+44, 'Actual four eight-field Back pulses followed by three HP fields')
    actual = lambda button: [int(r['frame']) for r in inputs if r['slot']=='2' and r['button']==button and a+10 <= int(r['frame']) <= start]
    need(actual('Block') == list(range(a+10,a+42))
         and actual('Right') == [a+10+i*8+j for i in range(4) for j in range(3)]
         and actual('High_Punch') == [a+42,a+43,a+44],
         'All32 actual Block fields, four physical three-field Right/Back pulses and final HP, no action injection')
    parser = [r for r in records('PARSER') if r['frame']==action['frame'] and r['table']=='FF87A980']
    need(len(parser)==1 and parser[0]['actor']==action['actor'] and parser[0]['a0']=='00000063'
         and parser[0]['a1']=='0000600C', 'Actual winner executes original direction-qualified finisher parser')
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    need(struct.unpack_from('<12H',stock,(0xff87a980-0xff800000)//8)==(56,7,7,7,7,0,0,8,8,8,8,0),
         'Entire original BBBB timing/header/four Right-history words and terminator source exact')
    comparisons=[r for r in records('COMPARE') if r['frame']==action['frame'] and int(r['table'],16) in range(0xff87aa00,0xff87aa40,16)]
    need(len(comparisons)==4 and [int(r['table'],16) for r in comparisons]==list(range(0xff87aa00,0xff87aa40,16))
         and all(r['wanted']==r['actual']=='8' for r in comparisons)
         and [int(r['tick']) for r in comparisons]==[int(comparisons[0]['tick'])-8*i for i in range(4)],
         'All four source-qualified direction history comparisons match genuine Back pulses at exact eight-tick spacing')"""
need(source.count(before) == 1, 'Preserve whole physical gate; replace only incorrect slot-specific parser assumption')
physical_source = source.replace(before, after, 1)
scope = dict(original.__dict__)
exec(compile(physical_source, __file__+'.entire5603_original_physical_gate_actual_native_command_history', 'exec'), scope)
physical = scope['physical']


def stock_reference(guest, stock, name, address, call):
    need(0xff800000 <= address <= 0xfffffe00, 'Original reference address in original guest ROM')
    at = direct.prior.off(address)
    need(guest[at:at+16] == stock[at:at+16], 'Actual stock caller/script remains whole original source')
    if name == 'caller' and address == 0xff820a50:
        wanted = (0x4c09,0x2480,0x0b20,0x24a0,0xff82,0x8400,0xca03,0x0d5f,0x2430,0xffa1)
        names = (6,7,8,9,10,11,12,13,14,15,16,17,53,0,18,90,19)
        need(struct.unpack_from('<10H',guest,direct.prior.off(0xff8209b0)) == wanted
             and struct.unpack_from('<17H',guest,direct.prior.off(0xff8224a0)) == names,
             'Entire original ID shift/name-table lookup/zero branch/CALLA and all17 native ID/name entries')
        need(call['command'] == call['a0'] == '00000009' and names[3] == 9
             and [i for i,n in enumerate(names) if n == 9] == [3],
             'Actual announcer selector9 maps uniquely to original Baraka3 via executed original lookup program')
    else:
        direct.observed.announcer.reference(guest, stock, name, address, call)


def packet_gate(log, guest):
    # Rebuild the whole original gate; change only its caller-source check.
    observed = direct.observed.announcer.observed
    source = inspect.getsource(observed.gate)
    before = """                need(0xff800000 <= address <= 0xfffffe00
                     and guest[prior.off(address):prior.off(address)+16] == stock[prior.off(address):prior.off(address)+16],
                     'Actual native announcer script/caller remains original source bytes')"""
    need(source.count(before) == 1, 'Whole original dual-dispatcher proof with exact original name lookup source')
    source = source.replace(before, '                stock_reference(guest, stock, name, address, call)', 1)
    scope = dict(observed.__dict__, stock_reference=stock_reference)
    exec(compile(source, __file__+'.entire5566_original_announcer_gate_complete_stock_name_lookup', 'exec'), scope)
    announcer = direct.observed.announcer
    old_gate = announcer.gate
    try:
        announcer.gate = scope['gate']
        positive = direct.gate(log, guest)
        rejected = direct.faults(log, guest)
    finally:
        announcer.gate = old_gate
    return dict(passed=True, proof=positive, effectiveFaults=rejected,
                stockNameLookupActualIndexUniquelyInferredFromOriginalTable=True,
                stockNameLookupA9RegisterDirectlyObserved=False)


def physical_faults(log):
    positive = physical(log); faults = []
    tests = (
        ('wrong original victim identity', 'ids=3,2', 'ids=3,1'),
        ('wrong original collision writer', 'pc=FF836700', 'pc=FF838860'),
        ('wrong native wrap age', 'age=174 actor=', 'age=175 actor='),
        ('wrong original parser mask', 'table=FF87A980 a0=00000063 a1=0000600C', 'table=FF87A980 a0=00000063 a1=00000000'),
        ('wrong actual native history', 'wanted=8 actual=8 tick=797 table=FF87AA00', 'wanted=8 actual=4 tick=797 table=FF87AA00'),
        ('wrong actual eight-tick history spacing', 'wanted=8 actual=8 tick=789 table=FF87AA10', 'wanted=8 actual=8 tick=790 table=FF87AA10'),
    )
    for label, old, new in tests:
        need(old in log and old != new, 'Effective actual stock physical fault')
        try:
            physical(log.replace(old,new,1))
        except ValueError as error:
            faults.append(dict(label=label,rejectedBy=str(error)))
        else:
            raise ValueError('Accepted actual stock physical counterexample: '+label)
    for button in ('Block','Right','High_Punch'):
        line = next(s for s in log.splitlines() if s.startswith('MK2_STOCK_HEAD_V921_INPUT frame=3130 ')
                    and 'button=Block' in s) if button=='Block' else next(s for s in log.splitlines()
                    if s.startswith('MK2_STOCK_HEAD_V921_INPUT frame='+('3125' if button=='Right' else '3133')+' ')
                    and 'button='+button in s)
        try:
            physical(log.replace(line+'\n','',1))
        except ValueError as error:
            faults.append(dict(label='one genuine '+button+' field omitted', rejectedBy=str(error)))
        else:
            raise ValueError('Accepted omitted genuine stock controller field')
    need(physical(log) == positive, 'Whole positive native physical proof restored after nine effective faults')
    return faults


def run():
    parent = json.loads(original.PARENT.read_text())
    failed = json.loads(FAILURE.read_text())
    need(parent['passed'] and parent['goalStatus']=='active' and not failed['passed']
         and failed['error']=="ValueError('Original P2 Baraka physical Block/BBBB/HP native parser, never injected action')",
         'Actual full port proof and completed original native run with preserved incorrect verifier assumption')
    terminal = json.loads((FOLDER/'terminal.json').read_text())
    process = json.loads((FOLDER/'process.json').read_text())
    log = (FOLDER/'run.log').read_text()
    need(terminal['exit_code']==0 and terminal['nativePID']==process['pid'] and process['command'][1]=='mk2'
         and not (FOLDER/'stderr.log').read_text() and 'Average speed:' in log,
         'Same original native run genuinely finished without any script error')
    pins = json.loads((FOLDER/'input_hashes_before.json').read_text())
    for p in (Path(__file__), FAILURE, original.PARENT, Path(capture.__file__),
              ROOT/'mame-mkp/unidasm.exe', ROOT/'mame-mkp/src/tools/unidasm.cpp'):
        pins[str(p.resolve())] = sha(p)
    stock = original.STOCK.read_bytes()
    expected, source_roms = original.rom.expected_region(pins)
    need(all(sha(p)==h for p,h in pins.items()), 'Every original/current/public/source input stable before qualification')
    state = physical(log); rejected = physical_faults(log)
    packets = packet_gate(log, stock)
    need(len(rejected)==9 and len(packets['effectiveFaults'])==12,
         'Nine actual native physical and twelve original direct/source/full-word faults all effective')
    chunks = original.rows(log,'MK2_NATIVE_DCS_ROM_DIGEST')
    guest = original.rows(log,'MK2_MAUDIO_GUEST_DIGEST')
    need(len(guest)==1 and guest[0]['sha256']==sha(original.STOCK) and len(chunks)==384,
         'Executed whole-byte original guest comparison and both complete native sound ROM transports retained')
    for phase in ('startup','terminal'):
        selected = [r for r in chunks if r['phase']==phase]
        need([int(r['offset']) for r in selected]==list(range(0,0xc00000,65536))
             and all(r['sha256']==original.digest(expected[int(r['offset']):int(r['offset'])+65536]) for r in selected),
             'All192 actual successful source-compared chunk digests rechecked per original startup/terminal region')
    pcm, dac = (original.rows(log, prefix) for prefix in ('MK2_BBAUDIO_PCM_DIGEST','MK2_NATIVE_DAC_RAM_DIGEST'))
    need(len(pcm)==len(dac)==685 and all(p['frame']==d['frame'] and p['seconds']==d['seconds']
         and p['bytes']=='3840' and d['consumed']=='625' for p,d in zip(pcm,dac)),
         'All685 stock DAC and PCM transports really occurred; raw normalization/waveform gate was not reached')
    for p in sorted(FOLDER.rglob('*')):
        if p.is_file(): pins[str(p.resolve())] = sha(p)
    need(all(sha(p)==h for p,h in pins.items()), 'Original and port/public immutable sources/evidence unchanged after no-replay qualification')
    return dict(passed=True, observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(), goalStatus='active',
        remaining=parent['remaining'], parentAdditiveJournal=str(original.PARENT),
        preservedOriginalNavigationFailure=str(capture.FAILURE), preservedOriginalSlotParserAssumptionFailure=str(FAILURE),
        previousGoalTurnClassification='no progress: acknowledgement and read-only cleanup status did not change implementation or qualification',
        thisGoalTurnClassification='progress: genuine original stock Cage2/Baraka3 earns two rounds and original fatality; physical direction history/source/input/health/retirement accepted with9actual faults, entire original dynamic name table/lookup and full dispatcher/packet/port/ADSP/return source accepted with12faults without replay; whole stock guest and both sound ROM checkpoints exact. Full stock mixed-waveform comparison remains unexecuted because earlier verifier failed before that gate.',
        originalNativeTerminal=terminal, retainedNativeProcess=str(FOLDER/'process.json'), originalPhysicalProof=state,
        effectiveOriginalPhysicalFaults=rejected, originalPacketQualification=packets, originalSourceROMs=source_roms,
        retainedExecutedWholeGuestSourceComparisonSHA256=guest[0]['sha256'],
        retainedExecutedWholeSoundROMSourceComparisonSHA256=original.digest(expected),
        completeOriginalSoundROMChunkDigestsRechecked=384, originalPCMCallbacksObserved=685,
        originalPCMBytesObserved=sum(int(r['bytes']) for r in pcm), originalDACCallbacksObserved=685,
        originalWaveformReferenceCaptureObserved=True, sourceQualifiedOriginalMixedWaveformAccepted=False,
        portWaveformEqualsOriginalGameplayReferenceAccepted=False, completeBarakaFinisherAudioAccepted=False,
        fullPortAcceptance=False, newNativeBoots=0, nativeBootsSincePortFrontier=2, newBuilds=0, newDeletedFiles=0,
        requestedRawGuestGFXVRAMRGBPCMFilesWritten=0, publicPlayableChanged=False, refreshedReleaseZIP=False,
        persistentNativeAutomaticExitPNGs=[*json.loads(capture.FAILURE.read_text())['persistentNativeAutomaticExitPNGs'],*failed['persistentNativeAutomaticExitPNGs']],
        newInputHashes=pins,
        nextAction='Fresh complete original stock RAM capture using the now-qualified direction-history physical and original dynamic-name source gates; qualify actual native DAC normalization and source-clock waveform before disposing of buffers, then compare source-owned corresponding original/port phases and advance all original stage/move/finisher/CPU/campaign/UI/cleanup/release groups.')


if __name__=='__main__':
    need(not OUT.exists(), 'Fresh immutable original native source/control qualification')
    try:
        report=run()
    except Exception as error:
        report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir()
    original.save(OUT/'progress.json',report)
    before=sha(OUT/'progress.json')
    done=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(OUT/'progress.json'),__file__],capture_output=True)
    need(done.returncode==0 and sha(OUT/'progress.json')==before, 'Source and evidence losslessly compressed')
    print(json.dumps({k:report[k] for k in ('passed','error','originalNativeTerminal','originalPCMCallbacksObserved',
        'sourceQualifiedOriginalMixedWaveformAccepted') if k in report},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
