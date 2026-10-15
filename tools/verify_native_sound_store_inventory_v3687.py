"""Original ROM sound-port stores: two dynamic packet sites, thirteen constants.

This establishes why the packet guard need not suppress direct custom cues or
other original reset/diagnostic stores. No new runtime/audio acceptance.
"""
import hashlib
import json
import struct
from pathlib import Path
import verify_native_sound_packet_guard_v3669 as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v3688_native_sound_store_inventory_checked'

def run():
    need(not OUT.exists(),'Fresh original-source sound store inventory')
    original=ROOT/'mk2/mk2-maincpu.bin'
    need(sha(original)=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23','Original whole native program')
    rom=original.read_bytes();records=[]
    dynamic={0xffa13c60:0x0583,0xffa13d30:0x0580}
    markers=set(range(0xfff7,0xffff))
    for i in range(0,len(rom)-6,2):
        opcode=struct.unpack_from('<H',rom,i)[0]
        if not(0x0580<=opcode<=0x059f and rom[i+2:i+6]==bytes.fromhex('3010d001')):continue
        at=0xff800000+i*8
        record=dict(instruction=f'{at:08X}',storedPC=f'{at+48:08X}',opcode=f'{opcode:04X}')
        if at in dynamic:
            need(opcode==dynamic[at],'Exact dynamic original packet register')
            record.update(kind='native_dynamic_packet',guardPC=f'{at+48:08X}')
        else:
            need(opcode==0x0580,'Other original absolute sound store uses A0')
            if struct.unpack_from('<H',rom,i-6)[0]==0x09e0:
                value=struct.unpack_from('<I',rom,i-4)[0];width=32
            else:
                need(struct.unpack_from('<H',rom,i-4)[0]==0x09c0,'Exact original immediate producer before other store')
                value=struct.unpack_from('<H',rom,i-2)[0];width=16
            need((value&65535)not in markers,'Original constant command cannot collide with an imported marker')
            record.update(kind='original_constant_store',immediateWidth=width,immediate=f'{value:08X}')
        records.append(record)
    need(len(records)==15 and sum(r['kind']=='native_dynamic_packet'for r in records)==2,'Complete whole-ROM scan: two dynamic/thirteen constant stores')
    need({r['guardPC']for r in records if r['kind']=='native_dynamic_packet'}=={'FFA13C90','FFA13D60'},'Exact staged guard PCs from original complete store census')
    staged=ROOT/'audit_v3668_native_sound_packet_source/midtunit_m.cpp'
    source=staged.read_text()
    need('m_maincpu->pc() == 0xffa13c90U ||\n\t\t\t\t\tm_maincpu->pc() == 0xffa13d60U;'in source,'Actual staged guard corresponds to entire dynamic packet census')
    faults=[]
    for replacement in(0xffa13c60,0xffa13d30,0xffa13c80,0xffa13d40):
        changed={replacement,0xffa13d60}
        need(changed!={0xffa13c90,0xffa13d60},'Opcode-PC/off-by-word fault rejected by original operand-complete census')
        faults.append(dict(wrongGuardPC=f'{replacement:08X}',rejected=True))
    return dict(passed=True,originalWholeROMBytes=len(rom),originalPortStores=records,
      totalOriginalPortStores=15,dynamicNativePacketStores=2,noncollidingOriginalConstantStores=13,
      actualOperandCompleteGuardPCs=['FFA13C90','FFA13D60'],rejectedWrongPCFaults=faults,
      guestOrExecutableChanged=False,newBuildOrROMCopies=0,nativeDCSAudioWaveformAcceptance=False,fullPortAcceptance=False,
      inputHashes={str(p):sha(p)for p in(original,staged,Path(__file__).resolve())},scope=__doc__)

if __name__=='__main__':
    report=run();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('originalPortStores','inputHashes','scope')},indent=2))
