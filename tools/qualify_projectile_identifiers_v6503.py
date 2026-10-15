"""Source-only repair of two missed native packed-identifier tables.

The actual failed native records remain failures. Expected RAM is constructed
independently; no compiled/runtime/public-fix acceptance is claimed here.
"""
import gzip,hashlib,json,re,struct,subprocess
from pathlib import Path
import current_payload_metadata_context_v5229 as current
from capture_current_continue_v6479 import rows
ROOT,need,sha=current.ROOT,current.need,current.sha
SOURCE=ROOT/'source_v6502_native_projectile_identifiers/midtunit_m.cpp'
PRIOR=ROOT/current.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
OUT=ROOT/'audit_v6504_projectile_identifiers_source_checked'
MARKER='\t// The cooperative scheduler saves A7..A12, not ordinary SP call frames.'
BLOCK='''\t// These native lookups are packed 16-bit identifiers, not callbacks. The
\t// task table has sixteen rows and the render-group table twelve. Appended
\t// IDs previously read executable words: Sonya P1 received B700h, whose
\t// high bit exempts it from challenger cleanup. Its linked polling task was
\t// retired, then impact cleanup asserted while removing that stale pointer.
\t// Keep every real stock row. Added projectiles use ordinary P1/P2 task
\t// families and independent, non-persistent render-group identifiers.
\tconstexpr unsigned projectile_task_ids = 0xfd700, projectile_group_ids = 0xfd750;
\tfor (unsigned at = projectile_task_ids; at < 0xfd800; at++)
\t\tif (rom[at] != 0xff) fatalerror("MK2KS: projectile identifier storage occupied");
\tif (read16(rom_offset(0xff8b5d20)) != 0x09e0 ||
\t\tread32(rom_offset(0xff8b5d30)) != 0xff8b5fc0 ||
\t\tread16(rom_offset(0xff8b6570)) != 0x09e0 ||
\t\tread32(rom_offset(0xff8b6580)) != 0xff8b66a0)
\t\tfatalerror("MK2KS: unsupported projectile identifier lookup layout");
\tstd::copy_n(rom + rom_offset(0xff8b5fc0), 16 * 4, rom + projectile_task_ids);
\tstd::copy_n(rom + rom_offset(0xff8b66a0), 12 * 4, rom + projectile_group_ids);
\tfor (unsigned id = 16; id < 19; id++)
\t\twrite32(projectile_task_ids + id * 4, 0x08000700);
\tfor (unsigned id = 12; id < 17; id++)
\t\twrite32(projectile_group_ids + id * 4, 0);
\twrite32(projectile_group_ids + 17 * 4, 0x07030703);
\twrite32(projectile_group_ids + 18 * 4, 0x07040704);
\twrite32(rom_offset(0xff8b5d30), native_address(projectile_task_ids));
\twrite32(rom_offset(0xff8b6580), native_address(projectile_group_ids));
'''

def offset(a):return (a-0xff800000)//8
def address(b):return 0xff800000+b*8
def expected_guest(base):
 need(base[0xfd700:0xfd800]==b'\xff'*256,'Whole actually unused initialized pool')
 need(struct.unpack_from('<I',base,offset(0xff8b5d30))[0]==0xff8b5fc0 and
      struct.unpack_from('<I',base,offset(0xff8b6580))[0]==0xff8b66a0,'Two actual old lookup operands')
 g=bytearray(base)
 g[0xfd700:0xfd740]=base[offset(0xff8b5fc0):offset(0xff8b5fc0)+64]
 g[0xfd750:0xfd780]=base[offset(0xff8b66a0):offset(0xff8b66a0)+48]
 for i in range(16,19):struct.pack_into('<I',g,0xfd700+i*4,0x08000700)
 for i in range(12,17):struct.pack_into('<I',g,0xfd750+i*4,0)
 struct.pack_into('<2I',g,0xfd750+17*4,0x07030703,0x07040704)
 struct.pack_into('<I',g,offset(0xff8b5d30),address(0xfd700))
 struct.pack_into('<I',g,offset(0xff8b6580),address(0xfd750))
 return bytes(g)

def check(text):
 old=PRIOR.read_text()
 need(old.count(MARKER)==1 and text==old.replace(MARKER,BLOCK+MARKER,1),
      'Only exact reviewed packed-ID extension; every other gameplay/art/audio/source byte preserved')
 return True

def main():
 need(not OUT.exists(),'Fresh immutable source diagnosis/qualifier')
 base=current.expected();check(SOURCE.read_text());fresh=expected_guest(base)
 paths=[SOURCE,PRIOR,Path(__file__),Path(current.__file__),ROOT/'mk2/mk2-maincpu.bin']
 captures=[];texts=[]
 for version,label in ((6492,'current_challenger'),(6495,'current_challenger_overlap'),
                       (6498,'current_challenger_ancestry'),(6501,'current_challenger_cleanup')):
  folder=ROOT/f'audit_v{version}_{label}_sonya_p2_ram'
  report=json.loads((folder/'report.json').read_text())
  need(not report['passed'] and report['nativeExit']==0 and not report['observationErrors'] and
       not(folder/'stderr.log').read_text().strip() and len(report['actualGuestGFXProofs'])==2,
       'Actual failed gameplay run naturally terminal, complete current memory and clean observer')
  need(all(sha(p)==h for p,h in report['inputHashes'].items()),'Every actual failed-run source intact')
  with gzip.open(folder/'run.log.gz','rt')as f:t=f.read()
  texts.append(t);paths.extend([folder/'report.json',folder/'run.log.gz',folder/'stderr.log',folder/'native_identity.json'])
  captures.append(dict(report=str(folder/'report.json'),nativeExit=0,passed=False))
 for tag in ('MK2_JR_INPUT','MK2_JR_HEALTH','MK2_CR_FIELD'):
  selected=lambda t:[l for l in t.splitlines() if l.startswith(tag+' ')]
  need(all(selected(t)==selected(texts[0]) for t in texts[1:]),'All four complete physical/health/actor callback chronologies byte-identical '+tag)
 entries=rows(texts[-1],'MK2_JC_ENTRY')
 error=next(q for q in entries if q['at']=='FFA1D860')
 cleanup=next(q for q in entries if q['at']=='FF80E0E0')
 need(error['frame']==cleanup['frame']=='2158' and cleanup['mode']=='14' and cleanup['a0']=='0106DAF0' and
      cleanup['a13']=='01070490' and cleanup['stack'].startswith('FF8B6870,') and
      error['stack'].startswith('FF80E1B0,00000000,01070590,FF8B6870,'),'Actual original projectile retirement -> missing-list-task assertion stack')
 tasks=rows(texts[-1],'MK2_JC_TASK')
 before=[q for q in tasks if q['frame']=='2156' and q['entry']=='FF83F520']
 after=[q for q in tasks if q['frame']=='2158' and q['entry']=='FF80E0E0']
 need(any(q['task']=='0106DAF0' for q in before) and not any(q['task']=='0106DAF0' for q in after),'Actual linked task retired by native join bulk cleanup')
 child=next(q for q in before if q['task']=='01070490');survivor=next(q for q in after if q['task']=='01070490')
 need(child['words'].split(',')[1]=='0003B700' and survivor['words'].split(',')[1]=='0000B700','Actual bogus high-bit child survives native join cleanup')
 old_task=struct.unpack_from('<I',base,offset(0xff8b5fc0)+18*4)[0]
 need(old_task==0x0040b700 and old_task&65535==0xb700,'Actual Sonya P1 lookup reads MOVE instruction bytes as B700 task identifier')
 spans=[(0xfd700,0xfd74c),(0xfd750,0xfd79c),(offset(0xff8b5d30),offset(0xff8b5d30)+4),(offset(0xff8b6580),offset(0xff8b6580)+4)]
 changes=[i for i,(a,b)in enumerate(zip(base,fresh))if a!=b]
 need(all(any(a<=i<b for a,b in spans)for i in changes),'Every changed expected guest byte belongs to two data tables/two pointer operands')
 for table,count,origin in ((0xfd700,16,0xff8b5fc0),(0xfd750,12,0xff8b66a0)):
  need(fresh[table:table+count*4]==base[offset(origin):offset(origin)+count*4],'Every actual stock packed identifier row preserved')
 faults=[];text=SOURCE.read_text()
 for label,a,b in [('retain_overread','16 * 4','19 * 4'),('preserve_bogus_highbit','0x08000700','0x0800b700'),
                   ('wrong_pool','0xfd700','0xfc700'),('wrong_sonya_group','0x07040704','0xf0b504'),
                   ('unrelated_edit',MARKER,MARKER+' unrelated')]:
  bad=text.replace(a,b,1);need(bad!=text,'Effective actual staged-source fault')
  try:check(bad)
  except ValueError as e:faults.append(dict(kind=label,rejectedBy=str(e)))
  else:raise ValueError('Faulty source accepted '+label)
  check(text)
 report=dict(passed=True,scope=__doc__,stagedSource=str(SOURCE),stagedSourceSHA256=sha(SOURCE),
  priorCandidate=current.NAME,expectedGuestSHA256=hashlib.sha256(fresh).hexdigest().upper(),
  expectedGuestChangedBytes=len(changes),expectedChangedSpans=spans,actualPreservedFailedRuns=captures,
  actualNativeRootCause='Unextended packed projectile task IDs read executable bytes; Sonya P1 B700 survives native join purge while linked task retires, then original FF8B6820 cleanup asserts in FF80E0E0 list scan.',
  physicalHealthAndActorChronologiesIdenticalAcrossFourFailures=True,sourceNegativeFaults=faults,
  inputHashes={str(p.resolve()):sha(p)for p in paths},newBuilds=0,newROMCopies=0,newRawMedia=0,
  compiledFixAccepted=False,nativeFixAccepted=False,publicPlayableChanged=False,fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 for p in [SOURCE,Path(__file__),OUT/'report.json']:
  h=sha(p);need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Hash-preserving exact-file compression')
 print(json.dumps({k:report[k]for k in ('passed','expectedGuestSHA256','expectedGuestChangedBytes','nativeFixAccepted')}),flush=True)

if __name__=='__main__':main()
