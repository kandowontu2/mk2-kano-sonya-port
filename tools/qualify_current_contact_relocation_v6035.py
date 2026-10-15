"""Whole6033 matrix; independently bind the actual extended native reaction table.

Preserve the failed unchanged-operand assumption. The native collision kernel
has one intended four-byte table relocation for real IDs17/18, not altered
collision/block/health logic. Check that exact relocation and every other byte.
"""
import inspect,json,traceback
from pathlib import Path
import qualify_current_close_contacts_v6033 as earlier
ROOT,need,sha=earlier.ROOT,earlier.need,earlier.sha
OUT=ROOT/'audit_v6036_current_native_contact_relocation_checked'

def run():
 failed=earlier.OUT/'report.json';failure=json.loads(failed.read_text())
 need(not failure['passed']and 'Whole original native body/shadow/collision/block/health/guard kernel unchanged'in failure['error'],
      'Actual original-operand assumption failure retained without rewriting any capture')
 source=inspect.getsource(earlier.run)
 before=" original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()"
 after=""" original=bytearray((ROOT/'mk2/mk2-maincpu.bin').read_bytes())
 operand=(0xff835de0-0xff800000)//8;outer=0xfc900
 compiled=ROOT/current.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
 text=compiled.read_text()
 need('constexpr unsigned outer = 0xfc900;'in text and 'unsigned const operand = rom_offset(0xff835de0);'in text and
      'write32(operand, 0xff800000U + outer * 8);'in text,
      'Actual frozen compiled reaction-table relocation constants and operand')
 need(struct.unpack_from('<I',original,operand)[0]==0xff8d2bd0 and
      struct.unpack_from('<I',guest,operand)[0]==0xff800000+outer*8 and
      guest[outer:outer+17*4]==original[(0xff8d2bd0-0xff800000)//8:(0xff8d2bd0-0xff800000)//8+17*4]and
      struct.unpack_from('<II',guest,outer+17*4)==(0xff800000+0xfca00*8,0xff800000+0xfcb00*8),
      'Every original outer roster row unchanged and both actual appended IDs use separate own native reaction roots')
 struct.pack_into('<I',original,operand,0xff800000+outer*8)
 pins[str(compiled)]=sha(compiled)"""
 need(source.count(before)==1,'One independently explained original reaction relocation');source=source.replace(before,after,1)
 scope=dict(earlier.run.__globals__,OUT=OUT,__file__=__file__)
 exec(compile(source,__file__+'::whole_contact_body_shadow_matrix_exact_relocation','exec'),scope)
 report=scope['run']()
 for p in(failed,Path(earlier.__file__).resolve()):report['inputHashes'][str(p)]=sha(p)
 report.update(wholeNativeCollisionKernelExactExceptSourceQualifiedTableRelocation=True,
               nativeBlockHealthAndGuardKernelsByteExact=True,retainedOriginalOperandAssumptionFailure=str(failed))
 return report

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable complete native contact qualification')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualSemanticFaultsRejected','cases')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
