"""Metadata-only ROM declaration repair against actual immutable current payload."""
import hashlib,json,re,traceback,zlib
from pathlib import Path
import native_subzero_legs_context_v4993 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
SOURCE=ROOT/'source_v5215_current_payload_rom_metadata/midtunit.cpp'
OUT=ROOT/'audit_v5217_current_payload_rom_metadata_source_checked'

def check(text):
 prior=ROOT/current.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
 need(sha(prior)=='0094EAE7DC9D3AF85474F720A16054BCFA5DF654751E8DA9C3D105588E674363','Actual compiled current source')
 payloadpath=ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata';payload=payloadpath.read_bytes()
 need(sha(payloadpath)==current.PAYLOAD_SHA and len(payload)==0x200000,'Actual immutable payload')
 pattern=r'ROM_LOAD\( "mk2ks\.mdata", 0x000000, 0x200000, CRC\(([a-f0-9]{8})\) SHA1\(([a-f0-9]{40})\) \)'
 old=prior.read_text();old_entries=list(re.finditer(pattern,old));fresh=list(re.finditer(pattern,text))
 need(len(old_entries)==len(fresh)==1,'Exactly one old/new actual payload declaration')
 crc=f'{zlib.crc32(payload):08x}';digest=hashlib.sha1(payload).hexdigest()
 need(fresh[0].groups()==(crc,digest),'Actual payload CRC32/SHA1 exactly match new declaration')
 expected=old[:old_entries[0].start()]+fresh[0].group()+old[old_entries[0].end():]
 need(text==expected,'Only actual payload CRC/SHA1 declaration changes; every unrelated source byte retained')
 need(old_entries[0].groups()!=fresh[0].groups(),'Real stale metadata discrepancy corrected')
 return dict(priorDeclaration=old_entries[0].group(),correctedDeclaration=fresh[0].group(),
  actualPayloadCRC32=crc,actualPayloadSHA1=digest,actualPayloadSHA256=current.PAYLOAD_SHA,
  actualPayloadBytes=len(payload),onlyDeclaredCRCAndSHA1Changed=True)

def main():
 need(not OUT.exists(),'Fresh immutable source qualifier')
 text=SOURCE.read_text();proof=check(text);faults=[]
 for label,bad in [
  ('old_actual_checksum',text.replace(proof['correctedDeclaration'],proof['priorDeclaration'],1)),
  ('foreign_crc',text.replace('CRC('+proof['actualPayloadCRC32']+')','CRC(00000000)',1)),
  ('foreign_sha1',text.replace('SHA1('+proof['actualPayloadSHA1']+')','SHA1('+'0'*40+')',1)),
  ('unrelated_source_change',text+'// unrelated\n'),
  ('duplicate_payload_declaration',text+proof['correctedDeclaration']+'\n')]:
  try:check(bad)
  except ValueError as error:faults.append(dict(kind=label,rejectedBy=str(error)))
  else:raise ValueError('Actual metadata-only source fault admitted '+label)
 need(check(text)==proof,'Entire actual source positive restored')
 guest=current.expected()
 need(hashlib.sha256(guest).hexdigest().upper()==current.GUEST_SHA,'Same independently reconstructed initialized guest')
 campaignpath=ROOT/'audit_v5200_current_kano_p1_whole_campaign_checked/report.json'
 campaign=json.loads(campaignpath.read_text())
 need(campaign['passed']and campaign['actualNaturalCurrentKanoP1BossesOwnEndingAttractAccepted']and
  all(sha(p)==h for p,h in campaign['inputHashes'].items()),'Actually qualified current gameplay/ending source and immutable proof')
 paths=[SOURCE,Path(__file__).resolve(),ROOT/current.NAME/'build-info.json',
  ROOT/current.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit.cpp',
  ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata',campaignpath]
 pins={str(p.resolve()):sha(p)for p in paths}
 report=dict(passed=True,stagedSource=str(SOURCE),stagedSourceSHA256=sha(SOURCE),
  expectedGuestSHA256=current.GUEST_SHA,sourceNegativeFaults=faults,metadata=proof,inputHashes=pins,
  compiledFixAccepted=False,nativeStartupWithoutWarningAccepted=False,gameDataChanged=False,
  initializedGuestChangesExpected=0,publicPlayableChanged=False,newBuilds=0,fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
