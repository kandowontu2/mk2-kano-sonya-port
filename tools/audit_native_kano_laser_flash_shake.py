"""Whole original/native burst white flash and screen-Y shake ABI.

The packedC0012 starts18alternating12pixel shake steps, not a white flash.
The real source flash is6fields; native stock burn flash is2fields. Preserve
that difference and require an independent source-timed auxiliary worker.
"""
import hashlib
import json
import struct
import subprocess
import traceback
from pathlib import Path

ROOT=Path(r'C:\Users\kando\Documents\Codex\2026-08-29\i-ha\work\mk2port')
OUT=ROOT/'audit_native_kano_laser_flash_shake_abi'

def need(value,message):
    if not value:raise ValueError(message)

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()

def part(blob,start,end):return blob[(start-0xff800000)//8:(end-0xff800000)//8]

def changed(blob,words=(),longs=()):
    result=bytearray(blob)
    for at,value in words:struct.pack_into('<H',result,at,value)
    for at,value in longs:struct.pack_into('<I',result,at,value)
    return bytes(result)

def disasm(path,start,end):
    result=subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'),str(path),'-arch','tms34010','-basepc',f'{start:X}',
        '-skip',str((start-0xff800000)//8),'-count',str(end-start)],capture_output=True,text=True)
    need(result.returncode==0,'Exact complete helper disassembly terminal')
    return result.stdout

def main():
    need(not OUT.exists(),'Fresh immutable complete helper audit');OUT.mkdir()
    try:
        original_path=ROOT/'mk3/mk3-maincpu.bin';native_path=ROOT/'mk2/mk2-maincpu.bin'
        original=original_path.read_bytes();native=native_path.read_bytes()
        flash_original=part(original,0xffaa2880,0xffaa2a20);flash_native=part(native,0xff9e2160,0xff9e2300)
        need(len(flash_original)==len(flash_native)==52 and
             changed(flash_native,words=((26,6),),longs=((2,0x105d7e0),(14,0x105d7e0),(20,0xff95c060),
                (30,0xff926960),(36,0x105d7e0),(42,0xff95c080)))==flash_original,
             'Whole source/native white-flash coroutine52bytes, only globals/callees and actual6vs2field duration differ')
        for a,b in ((0xff95c060,0xff83a4c0),(0xff95c080,0xff83a4e0)):
            # Both entries share one real10byte native/source control body.
            pass
        control_original=part(original,0xff95c060,0xff95c0d0);control_native=part(native,0xff83a4c0,0xff83a530)
        need(len(control_original)==len(control_native)==14 and changed(control_native,longs=((8,0x105d820),))==control_original,
             'Complete real native palette-control disable/enable entries and shared restore body')
        create_original=part(original,0xffaa2a20,0xffaa2b20);create_native=part(native,0xff9e1290,0xff9e1390)
        need(len(create_original)==len(create_native)==32 and changed(create_native,longs=((16,0xffaa2b20),(22,0xff95fec0)))==create_original,
             'Whole source/native shake constructor, same packed count/amplitude, exact103class replacement ABI')
        worker_original=part(original,0xffaa2b20,0xffaa2c30);worker_native=part(native,0xff9e1390,0xff9e14a0)
        need(len(worker_original)==len(worker_native)==34 and changed(worker_native,words=((0,0x05a6),(8,0x0586)),
             longs=((2,0x105d8a0),(10,0x105d8a0),(20,0xff926960),(30,0xff926ac0)))==worker_original,
             'Whole native/source shake worker, explicit actualWORDvsDWORD global access difference, same3field loop and retirement')
        guard_path=ROOT/'audit_native_kano_laser_velocity_source/report.json';guard=json.loads(guard_path.read_text())
        need(guard['passed'] and guard['sourceOnlyAccepted'] and all(sha(p)==h for p,h in guard['inputHashes'].items()),
             'Current corrected full source conserved')
        paths=[Path(__file__),original_path,native_path,ROOT/'mame-mkp/unidasm.exe',guard_path,ROOT/'PLAY_LATEST_KANO_SONYA.cmd']
        report=dict(passed=True,completeFlashShakeABIReviewed=True,nativeRuntimeAccepted=False,fullPortAcceptance=False,
            whiteFlash=dict(originalEntry='FFAA2880',nativeStockEntry='FF9E2160',completeBytes=52,originalFields=6,nativeStockFields=2,
                nativeBackgroundWord='0105D070',originalBackgroundWord='0105D7E0',nativePaletteDisable='FF83A4C0',nativePaletteEnable='FF83A4E0',
                nativePaletteControlWord='0105D0B0',backgroundRestoration='Save actual background WORD in scheduler-preservedA9, setFFFF, restore after six fields; re-enable actual native palette control.',
                coroutineReturn='MMFM A12,A7;EXGPC A7. Use actual private continuation, not ordinary CALLA.',
                originalDisassembly=disasm(original_path,0xffaa2880,0xffaa2a20),nativeDisassembly=disasm(native_path,0xff9e2160,0xff9e2300)),
            screenShake=dict(originalConstructor='FFAA2A20',nativeConstructor='FF9E1290',originalWorker='FFAA2B20',nativeWorker='FF9E1390',
                packedRecipe='000C0012',amplitudePixels=12,alternatingSteps=18,stepFields=3,totalFields=54,
                nativeYGlobal='0105D130',nativeGlobalAccessBits=32,originalGlobalAccessBits=16,
                nativeClass=0x103,nativeClassReplacementConstructor='FF840070',nativeRetirement='FF80DE20',
                constructorDisassembly=disasm(native_path,0xff9e1290,0xff9e1390),workerDisassembly=disasm(native_path,0xff9e1390,0xff9e14a0),
                caution='Preserve actual native32bit global ABI. Even18steps restore full value; verify actual background motion/native-camera handoff and neighbor state in runtime.'),
            originalNaturalIntegrationRequirements=guard['originalNaturalIntegrationRequirements'],originalRemainingWorkGroups=guard['originalRemainingWorkGroups'],
            goalStatus='active',inputHashes={str(p.resolve()):sha(p) for p in paths},newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,latestPlayableChanged=False,
            limitations=['ABI audit only, no new action binding or native flash acceptance.',
                'Source flash timing requires six fields, not direct use of native two-field helper.',
                'Independent source-timed worker must not delay actual196winner or hold globalSP across yield.',
                'Sound, roster victims/CPU/fallback/scene reset/rejoin and full14+6acceptance remain.'])
        need(len(report['originalNaturalIntegrationRequirements'])==14 and len(report['originalRemainingWorkGroups'])==6,'Full original scope retained')
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(dict(passed=True,wholeFlashBytes=52,sourceFlashFields=6,nativeStockFlashFields=2,wholeShakeBytes=34,shakeFields=54,nativeRuntimeAccepted=False)))
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc());raise

if __name__=='__main__':main()
