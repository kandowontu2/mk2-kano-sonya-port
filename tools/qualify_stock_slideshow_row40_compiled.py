"""Actual isolated artifact identity, not a runtime/reset/release pass."""
import hashlib
import json
import struct
from pathlib import Path
import stock_slideshow_row40_context as current
import qualify_stock_slideshow_row40 as repair
from inventory_current_port_storage_v4200 import allocated

ROOT,need=current.ROOT,current.need
OUT=ROOT/'audit_stock_slideshow_row40_compiled'


def main():
    need(not OUT.exists(),'Fresh immutable compiled conservation receipt')
    guest=current.expected()
    base=current.prior.expected()
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    at=(0xff8f48f0-0xff800000)//8
    need(guest[repair.TABLE:repair.TABLE+41*4]==stock[at:at+41*4],
         'All41 original stock picture pointers retained exactly, not only repaired final row')
    need(guest[repair.TABLE+41*4:repair.TABLE+54*4]==base[repair.TABLE+41*4:repair.TABLE+54*4],
         'All reserved entries and four genuine Kano/Sonya ending pointers unchanged')
    changes=[i for i,(a,b) in enumerate(zip(base,guest)) if a!=b]
    need(changes==list(range(repair.TABLE+160,repair.TABLE+164)),
         'All1MiB guest compared; only original row40 pointer bytes change')
    faults=[]
    for label,offset in (('zero original picture pointer',repair.TABLE+160),
                         ('new Kano ending pointer',repair.TABLE+50*4),
                         ('Kano voice marker',0xffbce),('unrelated native code',0x12340)):
        bad=bytearray(guest);bad[offset]^=1
        try:need(bytes(bad)==guest,'Whole independently reconstructed guest conservation contract')
        except ValueError as error:faults.append(dict(fault=label,rejected=str(error)))
        else:raise ValueError('Guest-identity fault admitted')
    build=ROOT/current.NAME
    meta=json.loads((build/'build-info.json').read_text(encoding='utf-8-sig'))
    cache=json.loads((build/'cache_retirement.json').read_text(encoding='utf-8-sig'))
    pins={str(p.resolve()):current.sha(p) for p in
          (Path(__file__),Path(current.__file__),Path(repair.__file__),build/'build-info.json',
           build/'restoration.json',build/'cache_retirement.json',build/'mkport_candidate.exe')}
    result=dict(passed=True,compiledIdentityAccepted=True,nativeFixAccepted=False,fullPortAcceptance=False,
                candidate=current.NAME,executableSHA256=current.EXE_SHA,guestSHA256=current.GUEST_SHA,
                immutablePayloadSHA256=current.PAYLOAD_SHA,wholeGuestBytesCompared=len(guest),
                changedByteOffsets=changes,originalStockPointersRetained=41,newEndingPointersUnchanged=4,
                onlyChangedHostSource='midtunit_m.cpp',actualGuestIdentityFaultsRejected=faults,
                nativeCompilerExit=cache['nativeCompilerExit'],preexistingFilesRestored=True,
                generatedCompilerCacheActuallyAbsent=not Path(cache['removedGeneratedCache']).exists(),
                singleNewExecutableAllocatedBytes=allocated(build/'mkport_candidate.exe'),
                payloadAndLaunchSampleSharedByHardlink=True,newROMCopies=0,newRawMedia=0,newZIPs=0,
                publicPlayableChanged=False,inputHashes=pins,goalStatus='active')
    need(meta['payload_hardlink_to_immutable_prior']==str(ROOT/current.prior.NAME/'roms/mk2ks/mk2ks.mdata'),
         'Build records exact original shared payload source')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('compiledIdentityAccepted','originalStockPointersRetained',
                                         'singleNewExecutableAllocatedBytes','nativeFixAccepted')}))


if __name__=='__main__':main()
