"""Original Sonya second finisher input, derived from original native code.

Source-only reference. It explicitly uses MK3 Run and therefore cannot just
be copied as a player command into five-button MKII. No port changes here.
"""
import gzip
import json
import struct
import subprocess
from pathlib import Path
import audit_native_secondary_finisher_reference as reference
import capture_native_secondary_kano_reference as transport

ROOT = reference.ROOT
OUT = ROOT/'audit_native_sonya_secondary_input'


def inspect(program, instructions):
    need = reference.need
    pointer = lambda a: reference.pointer(program,a)
    word = lambda a: struct.unpack_from('<H',program,reference.art.stock_file(a))[0]
    table = pointer(0xff977bd0+7*32)
    need(table == 0xff978a30 and pointer(table+32) == 0xff97a090,
         'Actual original Down event7 and Sonya1 roster handler')
    expected = {
        0xff817e20:'MOVI   7h,A0',
        0xff97a090:'MOVI   FF98A4A0h,A14',
        0xff97a0c0:'JR     FF991F70h',
        0xff9923b0:'MOVI   40020h,A0',
        0xff9923e0:'MOVI   402000h,A1',
        0xff992410:'CALLR  FF97F0E0h',
        0xff97f160:'CMP    A2,A0',
        0xff97f170:'JRNE   FF97F1A0h',
        0xff992450:'MOVI   D0h,A5',
        0xff992470:'MOVI   140h,A6',
        0xff992490:'JR     FF993160h',
        0xff993160:'CALLA  FF822890h',
        0xff993190:'CMP    A5,A3',
        0xff9931a0:'JRC    FF993B00h',
        0xff9931c0:'CMP    A6,A3',
        0xff9931d0:'JRHI   FF993B00h',
        0xff9931f0:'JR     FF993760h',
        0xff993790:'CMPI   3h,A4',
        0xff998810:'MOVI   FF998A50h,A0',
        0xff9ae120:'MOVK   2h,A9',
        0xff9ae130:'CALLA  FFA5EF10h',
        0xff9ae1f0:'MOVK   4h,A9',
        0xff9ae200:'CALLA  FFA5EF10h',
    }
    for at, text in expected.items():
        need(instructions.get(at) == text, f'Actual original Sonya input/effect instruction {at:08X}')
    record = 0xff98a4a0
    need(pointer(record) == 0x40020 and pointer(record+32) == 0x402000 and
         word(record+64) == 2 and pointer(record+80) == 0xff9923b0 and
         pointer(record+112) == 0xff9987e0,
         'Actual original Run+Block masks, typed fatality gate and second selector')
    histories = [[word(record+160+facing*96+index*16)for index in range(6)]
                 for facing in range(2)]
    need(word(record+144) == 48 and histories == [[7,8,6,6,0,0],[7,9,6,6,0,0]],
         'Actual original 48tick facing-relative Up/Up/Back/Down history')
    need(pointer(0xff998a50+32) == 0xff9ae0b0,
         'Actual original Sonya1 second performer independently owns special4')
    return dict(originalIdentity=1, finalEvent=7, eventName='Down', table=f'{table:08X}',
                handler='FF97A090', record=f'{record:08X}',
                commandChronological=['Up','Up','Back','Down'],
                originalRequiredHeldButtons=['Block','Run'],
                bothFacingHistories=histories, timeoutNativeTicks=48,
                separationMinimum=208,separationMaximum=320,requiredFinishFlag=3,
                originalAction='FF9AE0B0',performerAnimationIndex=2,effectAnimationIndex=4,
                verifiedInstructions={f'{at:08X}':text for at,text in expected.items()})


def main():
    reference.need(not OUT.exists() and not transport.census() and not reference.native.census(),
                   'Fresh original Sonya source reference with no native game live')
    reference.need(reference.sha(reference.MK3) ==
        '1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651',
        'Exact authoritative original native program')
    original = reference.MK3.read_bytes()
    run = subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'),str(reference.MK3),
        '-arch','tms34010','-basepc','0xff800000','-norawbytes'],
        capture_output=True,text=True,check=True)
    instructions = {int(line.split(':',1)[0],16):line.split(':',1)[1].strip()
                    for line in run.stdout.splitlines()}
    mapping = inspect(original,instructions)
    faults = []
    for name, at in [('Down_table',0xff977bd0+7*32),('Sonya_handler',0xff978a50),
        ('Run_Block_mask',0xff98a4a0),('typed_gate',0xff98a4f0),
        ('second_selector',0xff98a510),('timeout',0xff98a530),
        ('right_history',0xff98a540),('left_history',0xff98a5a0),
        ('Sonya_second_performer',0xff998a70)]:
        wrong = bytearray(original);wrong[reference.art.stock_file(at)] ^= 1
        try:inspect(bytes(wrong),instructions)
        except ValueError as error:faults.append(dict(name=name,rejected=str(error)))
        else:raise ValueError('Original Sonya source fault admitted: '+name)
    source_reference = ROOT/'audit_native_secondary_finisher_reference/report.json'
    scope = json.loads(source_reference.read_text())
    paths = [Path(__file__),Path(reference.__file__),reference.MK3,source_reference,
        ROOT/'mame-mkp/unidasm.exe',ROOT/'audit_native_kano_laser_reference_checked/report.json',
        reference.SOURCE,ROOT/reference.current.NAME/'mkport_candidate.exe',reference.PAYLOAD,
        ROOT/'PLAY_LATEST_KANO_SONYA.cmd']
    pins = {str(p.resolve()):reference.sha(p)for p in paths}
    report = dict(passed=True,sourceInputAccepted=True,originalRuntimeAccepted=False,
        portSecondFatalityImplemented=False,fullPortAcceptance=False,originalInput=mapping,
        faultRejections=faults,inputHashes=pins,
        originalNaturalIntegrationRequirements=scope['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=scope['originalRemainingWorkGroups'],
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        gameSourceChanged=False,latestPlayableChanged=False,goalStatus='active',
        limitations=['This is original source grammar, not a physically executed Sonya second fatality.',
                     'MKII has no Run button; port command must be deliberately adapted to its native five-button input.',
                     'The existing original special2/special4 graphics are imported, but effects/victim/timing/audio/cleanup remain unproved.'],
        nextAction='Physically earn the original Sonya win; at208..320 native separation, hold original Block/Run while Up/Up/Back/Down and observe only passive actual action/effect/victim state.')
    reference.need(len(report['originalNaturalIntegrationRequirements'])==14 and
        len(report['originalRemainingWorkGroups'])==6,'Full14+6 requirements conserved')
    reference.need(all(reference.sha(p)==h for p,h in pins.items()),'Current playable and actual source conserved')
    OUT.mkdir()
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    with gzip.open(OUT/'executed_sources.json.gz','wt',encoding='utf-8')as stream:
        json.dump({str(Path(__file__).resolve()):dict(sha256=reference.sha(__file__),source=Path(__file__).read_text())},stream)
    print(json.dumps(dict(passed=True,originalInput=mapping,rejectedFaults=len(faults),portSecondFatalityImplemented=False)))


if __name__=='__main__':main()
