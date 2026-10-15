"""Original MK2 signed byte-header shadow scanner for one real stock raw sprite.

This is not the body-DMA raw-pixel decoder. The unchanged native shadow
routine unconditionally scans headers even on stock descriptors without
compression bit0x80. Its signed width-minus-skips can move backward. All
source addresses are independently bounded against the whole compiled ROM,
never fitted to observed DMA rows. Imported sprites remain compressed only.
"""
import hashlib,json,subprocess
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5316_original_stock_raw_shadow_scanner_source_checked'
STOCK_SHA='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'
def qualify():
    guest=current.expected();stockpath=ROOT/'mk2/mk2-maincpu.bin';stock=stockpath.read_bytes()
    need(sha(stockpath)==STOCK_SHA,'Complete original MK2 CPU ROM unchanged')
    lo,hi=(0xff801070-0xff800000)//8,(0xff8017a0-0xff800000)//8
    need(guest[lo:hi]==stock[lo:hi],'Entire original native eligibility/projection/copy/header scanner unchanged')
    exe=ROOT/'mame-mkp/unidasm.exe'
    result=subprocess.run([str(exe),str(stockpath),'-arch','tms34010','-skip','0x286',
      '-count','880','-basepc','0xff801430'],capture_output=True,text=True,
      creationflags=subprocess.CREATE_NO_WINDOW)
    need(result.returncode==0 and not result.stderr,'Actual original ROM disassembly success')
    required=(
      'ff801430: 4dc1','ff801440: 4dc4','ff801450: 2681','ff801460: 2c41',
      'ff801470: 26c4','ff801480: 2c44','ff801490: 0bae 8008 0000',
      'ff801590: 81c3','ff8015a0: 3935','ff801600: 81c3','ff801610: 0b09 0070',
      'ff801670: 1893','ff801680: 0548','ff801690: 9548','ff8016a0: 4d0d',
      'ff8016b0: 278d','ff8016c0: 2c8d','ff8016d0: 628d','ff8016e0: 2f88',
      'ff8016f0: 6228','ff801700: 410d','ff801710: 4d68','ff801720: 45a8',
      'ff801730: 2428','ff801740: 410a','ff801750: 2428','ff801760: 410a',
      'ff801770: 3df3','ff801780: 0570','ff801790: c0d5')
    need(all(result.stdout.count(line)==1 for line in required),
      'Every exact original exponent/header/nibble/signed subtract/2plus4bit advance/DSJS/duplicate-tail instruction')
    baseline=ROOT/'audit_v2699_current_friendship_shadow_stock_comparison_checked/report.json'
    old=json.loads(baseline.read_text())
    need(old['passed']and old['onlyOriginalScannerSemanticsAndSourceAddressingCorrected']and
      all(sha(p)==h for p,h in old['inputHashes'].items()if p in (
        str(exe),str(stockpath),str(ROOT/'tools/verify_current_friendship_shadow_inventory_v2696.py'),
        str(ROOT/'tools/compare_current_friendship_shadow_stock_v2698.py'))),
      'Previously independent original whole-ROM unconditional signed scanner source qualification unchanged')
    return dict(passed=True,sourceOnly=True,currentOriginalShadowKernelByteExact=True,
      originalUnconditionalHeaderAndSignedWidthAdvanceQualified=True,
      originalScannerDisassembly=result.stdout,originalKernelSHA256=hashlib.sha256(stock[lo:hi]).hexdigest().upper(),
      inputHashes={str(p.resolve()):sha(p)for p in (Path(__file__),Path(current.__file__),exe,stockpath,baseline,
        ROOT/'tools/verify_current_friendship_shadow_inventory_v2696.py',
        ROOT/'tools/compare_current_friendship_shadow_stock_v2698.py')},
      actualCapturedRawShadowRowsNotYetAccepted=True,gameChanged=False,rawMediaFilesWritten=0,
      fullArtAcceptance=False,fullPortAcceptance=False)
def stock_raw_starts(graphic,width,height,command,gfx,proof):
    need(graphic==0x0251f2dc and width==10 and height==48 and command in (0x6000,0x6010),
      'Only exact independently owned original Sub-Zero10x48 raw reaction sprite; no generic raw/imported admission')
    need(proof['streamFormat']=='stockRaw6'and not proof['compressedRowStreamVerified']and
      proof['actualRowStarts']==proof['actualRowHeaders']==[]and proof['usedBits']==0,
      'Raw body stream remains explicitly raw, never relabeled compressed')
    bit=graphic;starts=[]
    for _ in range(height):
        need(0<=bit and bit+8<=len(gfx)*8,'Original unconditional scanner header inside entire independent ROM')
        starts.append(bit)
        header=(int.from_bytes(gfx[bit//8:bit//8+2],'little')>>(bit%8))&255
        pre=(header&15)<<((command>>8)&3);post=(header>>4)<<((command>>10)&3)
        bit=(bit+8+6*(width-pre-post))&0xffffffff
        need(0<=bit<=len(gfx)*8,'Original signed scanner pointer remains inside entire independent source ROM')
    return starts
if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable original-source scanner qualification')
    report=qualify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','originalScannerDisassembly')},indent=2),flush=True)
