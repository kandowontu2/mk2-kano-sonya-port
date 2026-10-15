"""Verify whole original/native victim position/flip/offset helper mappings.

Local ROM source evidence only. Never infer a victim ID swap or classify
an opaque original body flag as gravity without proving its native use.
"""
import hashlib
import json
import re
import struct
import subprocess
from pathlib import Path

import qualify_native_kano_laser_button_gate as gate
import qualify_native_kano_laser_button_gate_bound as accepted

ROOT=gate.ROOT
OUT=ROOT/'audit_native_kano_laser_victim_position'
need,sha=gate.need,gate.sha


def instructions(file,start,end):
    run=subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'),str(file),'-arch','tms34010',
        '-basepc',hex(start),'-skip',hex((start-0xff800000)//8),'-count',str(end-start),'-norawbytes'],
        capture_output=True,text=True,check=True)
    return [line.split(':',1)[1].strip() for line in run.stdout.splitlines()]


def inspect_mapping(original,native,old_file,new_file):
    mappings=[]
    helpers=[('copy full fixed-point XY and match facing',0xff965da0,0xff966080,0xff83ce60,0xff83d140),
        ('flip actual body and redraw its own current composite',0xff965750,0xff965810,0xff83b470,0xff83b530),
        ('apply facing-relative signed pixel offset',0xff965c00,0xff965d30,0xff83cc20,0xff83cd50)]
    for label,old_first,old_last,new_first,new_last in helpers:
        old=instructions(old_file,old_first,old_last);new=instructions(new_file,new_first,new_last)
        def translate(match):
            value=int(match.group(1),16)
            if old_first<=value<old_last:value+=new_first-old_first
            else:value={0xff965750:0xff83b470,0xff963200:0xff838790}.get(value,value)
            return f'{value:X}h'
        need([re.sub(r'\b([0-9A-F]+)h',translate,line) for line in old]==new,
             'Whole actual original/native helper mapping, not a prefix')
        need(new[-1]=='RETS' or label.startswith('flip'),'Whole helper terminal boundary')
        mappings.append(dict(operation=label,original=f'{old_first:08X}',native=f'{new_first:08X}',
            fullOriginalInstructions=old,fullNativeInstructions=new))
    wrapper=instructions(old_file,0xff9618e0,0xff9619b0)
    need(wrapper==['MMTM   SP,A0,A8','MOVE   *A13(140h),A0,1','XOR    A0,A8','XOR    A8,A0',
        'XOR    A0,A8','CALLA  FF965DA0h','MMFM   SP,A0,A8','RETS'],
        'Victim main140 is true performer; swap only local argument registers, never fighter IDs')
    table=(0xff9b6970-0xff800000)//8
    offsets=struct.unpack_from('<4h',original,table)
    need(offsets==(-184,0,-184,0),'Original real Kano/Sonya victim offsets, not guessed short beam range')
    need(struct.unpack_from('<3H',original,(0xff9599f0-0xff800000)//8)==(0x0bae,0x400,0),
         'Original victim flag400 is an actual source operation')
    return dict(fullHelperMappings=mappings,originalPositionWrapper=wrapper,
        sourceAddedVictimOffsets=dict(Kano=[-184,0],Sonya=[-184,0]),
        nativeFixedPointXYCopy=True,nativeFacingAndRedraw=True,
        identityWritesInMappedHelpers=False,
        originalFlag400Meaning='Not classified by this audit; no proved native equivalent. Do not label it stop-gravity.',
        remaining='Select each true victim own hurt composite, prove stock pose/anchors and flag semantics, then implement full reaction.')


def main():
    need(not OUT.exists() and not gate.prior.phases.visual.native.census(),'Fresh audit, no live native games')
    receipt=json.loads((accepted.OUT/'report.json').read_text())
    need(receipt['passed'] and all(sha(p)==h for p,h in receipt['inputHashes'].items()),'Latest gate/source and all accepted inputs conserved')
    old=ROOT/'mk3/mk3-maincpu.bin';new=ROOT/'mk2/mk2-maincpu.bin'
    need(sha(old)=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651' and
         sha(new)=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23',
         'Exact original authoritative ROM programs')
    result=inspect_mapping(old.read_bytes(),new.read_bytes(),old,new)
    paths=[Path(__file__),old,new,ROOT/'mame-mkp/unidasm.exe',accepted.OUT/'report.json',
           ROOT/'PLAY_LATEST_KANO_SONYA.cmd']
    pins={str(p.resolve()):sha(p) for p in paths}
    report=dict(passed=True,sourceReferenceAccepted=True,nativeRuntimeAccepted=False,fullPortAcceptance=False,
        contract=result,originalNaturalIntegrationRequirements=receipt['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=receipt['originalRemainingWorkGroups'],inputHashes=pins,
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,latestPlayableChanged=False,goalStatus='active')
    need(len(report['originalNaturalIntegrationRequirements'])==14 and len(report['originalRemainingWorkGroups'])==6,
         'Full14+6 original scope retained')
    need(all(sha(p)==h for p,h in pins.items()),'Whole original programs/public launcher conserved')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,fullNativeHelperMappings=len(result['fullHelperMappings']),nativeRuntimeAccepted=False)))


if __name__=='__main__':main()
