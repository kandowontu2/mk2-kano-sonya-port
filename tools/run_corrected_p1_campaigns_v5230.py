"""Fresh complete corrected-build P1 campaigns, unchanged physical policies."""
import argparse,concurrent.futures,inspect,re,zlib,hashlib
import current_payload_metadata_context_v5229 as current
import run_current_kano_p1_campaign_v5195 as kano
import run_extended_sonya_p1_campaign_v5207 as sonya
ROOT,need,sha=current.ROOT,current.need,current.sha

def metadata_clean(errors,proof):
 source=ROOT/current.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
 need(sha(source)=='17FCD9D7C5D862FEB03487828364AC4126D9B0C7AB437DAEBD94F760DA11C0DE',
  'Actual corrected compiled declaration source')
 declarations=re.findall(r'ROM_LOAD\( "mk2ks\.mdata", 0x000000, 0x200000, CRC\(([a-f0-9]+)\) SHA1\(([a-f0-9]+)\) \)',source.read_text())
 payload=(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 need(declarations==[(f'{zlib.crc32(payload):08x}',hashlib.sha1(payload).hexdigest())]and
  proof and proof['sha256']==current.GUEST_SHA and proof['everyActualByteComparedInRAM']and
  errors=='','Actual current payload metadata/full native guest; no warnings ignored')
 return dict(metadataMatchesPayload=True,nativeStderrEmpty=True,testCandidateWarningQualified=False,
  releaseMetadataCorrectionStillRequired=False,compiledCRC=declarations[0][0],compiledSHA1=declarations[0][1])

def run(fighter):
 ref=kano if fighter=='kano'else sonya
 out=ROOT/f'audit_v5231_{fighter}_corrected_p1_campaign'
 code=inspect.getsource(ref.capture)
 scope=dict(vars(ref),__file__=__file__,native=current,OUT=out,
  qualify_payload_metadata_warning=metadata_clean)
 exec(compile(code,__file__+'::whole_source_unchanged_'+fighter,'exec'),scope)
 return scope['capture']()

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya','both'),default='both')
 args=parser.parse_args()
 if args.fighter=='both':
  with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:list(pool.map(run,('kano','sonya')))
 else:run(args.fighter)
