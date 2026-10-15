"""Only source/asset/independent guest construction acceptance, not runtime.

One source-authored launch marker is inserted in the same native roll action.
Exactly four internal pointers relocate by96bits; the complete original roll
instructions and all other guest bytes remain unchanged. Audio ownership binds
the published real actor/Main/ID/action and is finite, physical-slot isolated.
"""
import hashlib,json,struct,subprocess
from pathlib import Path
import native_projectile_identifiers_context_v6509 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
STAGE=ROOT/'source_v6636_kano_ball_launch';OUT=ROOT/'audit_v6638_kano_ball_launch_source_checked'
OLD=ROOT/prior.NAME/'input_sources/mame-mkp/src/mame/midway'
M_EDITS={
 '\tsave_item(NAME(m_mk2ks_battle_health));':'\tsave_item(NAME(m_mk2ks_battle_health));\n\tsave_item(NAME(m_mk2ks_battle_id));',
 '\tball_call(0xff877ba0);\n\tball_call(0xff838d00);':
 '\tball_call(0xff877ba0);\n\t// Original MK3 Kano voice group4: typed record0208503Dh, command0208h.\n\t// The independently captured donor sample preserves its hardware latency\n\t// and complete tail; only the real owning fighter can request this cue.\n\tball_movi(0, 0x6b03); ball_code({0x0580, 0x1030, 0x01d0});\n\tball_call(0xff838d00);',
 '\tm_mk2ks_battle_health[slot] = 0;':'\tm_mk2ks_battle_health[slot] = 0;\n\tm_mk2ks_battle_id[slot] = 0;',
 'read32(main + 0xc0) != actor || space.read_word(actor + 0x1f0) != 18)':
 'read32(main + 0xc0) != actor || space.read_word(actor + 0x1f0) != m_mk2ks_battle_id[slot])',
 'data >= 0x6b00 && data <= 0x6b02':'data >= 0x6b00 && data <= 0x6b03',
 '\t\t\t\tif (m_mk2ks_voices && data >= 0x6b00 && data <= 0x6b03)\n\t\t\t\t{':
 '\t\t\t\tif (m_mk2ks_voices && data >= 0x6b00 && data <= 0x6b03)\n\t\t\t\t{\n\t\t\t\t\tuint16_t const launch_id = (data == 0x6b03) ? 17 : 18;\n\t\t\t\t\tuint16_t const launch_action = (data == 0x6b03) ? 0x20b : ((data == 0x6b00) ? 0x207 : 0x204);',
 'read32(main + 0xc0) != actor || space.read_word(actor + 0x1f0) != 18 ||\n\t\t\t\t\t\t\tspace.read_word(main + 0x1f0) != ((data == 0x6b00) ? 0x207 : 0x204))':
 'read32(main + 0xc0) != actor || space.read_word(actor + 0x1f0) != launch_id ||\n\t\t\t\t\t\t\tspace.read_word(main + 0x1f0) != launch_action)',
 '\t\t\t\t\t\tm_mk2ks_battle_health[slot] = space.read_word(health[slot]);':
 '\t\t\t\t\t\tm_mk2ks_battle_health[slot] = space.read_word(health[slot]);\n\t\t\t\t\t\tm_mk2ks_battle_id[slot] = launch_id;',
 'actor=%08X main=%08X id=18 pc=%08X seconds=%.12f\\n",\n\t\t\t\t\t\t\tdata, sample, channel, slot + 1, actor, main, m_maincpu->pc()':
 'actor=%08X main=%08X id=%u pc=%08X seconds=%.12f\\n",\n\t\t\t\t\t\t\tdata, sample, channel, slot + 1, actor, main, launch_id, m_maincpu->pc()',
}
def edited(text,edits):
 for a,b in edits.items():need(text.count(a)==1,'Exact single reviewed source edit '+a[:70]);text=text.replace(a,b,1)
 return text
def expected_sources():
 return {
  'midtunit_m.cpp':edited((OLD/'midtunit_m.cpp').read_text(),M_EDITS),
  'midtunit.cpp':edited((OLD/'midtunit.cpp').read_text(),{'"sonya_square_launch", "sonya_bicycle_launch", "sonya_bicycle_cry", nullptr':'"sonya_square_launch", "sonya_bicycle_launch", "sonya_bicycle_cry", "kano_ball_launch", nullptr'}),
  'midtunit.h':edited((OLD/'midtunit.h').read_text(),{'Independent, finite original Sonya launch voices.':'Independent, finite original Kano/Sonya launch voices.',
    '\tuint16_t m_mk2ks_battle_health[2] = {};':'\tuint16_t m_mk2ks_battle_health[2] = {};\n\tuint16_t m_mk2ks_battle_id[2] = {};'}),
 }
def check_source():
 for name,text in expected_sources().items():need((STAGE/name).read_text()==text,'Every source byte outside exact reviewed changes preserved '+name)
 return True
def expected_guest(base):
 lo,hi=0xffbc0,0xffd80;ball=base[lo:hi]
 need(ball[:12]==bytes.fromhex('e1090b0200005f0da07b87ff')and ball[290:]==b'\xff'*158,'Complete old native roll layout and spare capacity')
 insertion=struct.pack('<6H',0x09e0,0x6b03,0,0x0580,0x1030,0x01d0)
 new=bytearray(ball[:12]+insertion+ball[12:290]+b'\xff'*146)
 expected=[(116,0xc380,0xffffe250),(134,0xc880,0xffffe350),(148,0xcb80,0xffffe0b0),(206,0xca80,0xffffe4c0)]
 discovered=[]
 for pos in range(2,287,2):
  target=struct.unpack_from('<I',ball,pos)[0]
  if 0xffffde00<=target<0xffffec00:discovered.append((pos,struct.unpack_from('<H',ball,pos-2)[0],target))
 need(discovered==expected,'All4 typed native internal branches, not a loose binary relocation scan')
 for pos,opcode,target in expected:struct.pack_into('<I',new,pos+12,target+96)
 rebuilt=bytearray(new[:12]+new[24:302]+b'\xff'*158)
 for pos,opcode,target in expected:struct.pack_into('<I',rebuilt,pos,target)
 need(bytes(rebuilt)==ball,'Every old action instruction and original target reconstructed exactly after removing only the new marker')
 guest=bytearray(base);guest[lo:hi]=new
 need(guest[:lo]==base[:lo]and guest[hi:]==base[hi:],'All other1MiB native guest bytes unchanged')
 return bytes(guest)

def main():
 need(not OUT.exists(),'New immutable source-only guard')
 check_source();base=prior.expected();guest=expected_guest(base)
 donor=json.loads((ROOT/'audit_v6635_kano_launch_native48k/asset_report.json').read_text())
 need(donor['passed']and donor['hardwareOnlyNotGameplayAcceptance']and not donor['fullPortAcceptance']and
  donor['command']==0x208 and donor['nativeChannelVariants']==5 and donor['allVariantsExactlyEqual']and
  all(sha(p)==h for p,h in donor['inputHashes'].items()),'All6 actual native48k donor jobs and source/sample pins intact')
 source_rom=(ROOT/'mk3/mk3-maincpu.bin').read_bytes();off=lambda a:(a-0xff800000)//8
 need(struct.unpack_from('<I',source_rom,off(0xffaa8f70))[0]==0xffaa91d0 and
  struct.unpack_from('<I',source_rom,off(0xffaa91d0)+4*4)[0]==0x0208503d,
  'Original real Kano0 voice group4 typed record, command0208h (not Sonya/shared grunt)')
 for directory in ['audit_v6623_donor_ball_startup_source','audit_v6626_donor_ball_startup_helpers','audit_v6629_donor_ball_voice_kernel']:
  r=json.loads((ROOT/directory/'report.json').read_text())
  need(r['passed']and r['wholeNativeROM']['everyActualByteComparedInRAM']and
       r['wholeNativeROM']['sha256']==sha(ROOT/'mk3/mk3-maincpu.bin')and all(sha(p)==h for p,h in r['inputHashes'].items()),
       'Native whole donor ROM and actual startup/helper/voice disassembly bound')
 faults=[]
 def reject(label,changed):
  try:need(changed==guest,'Whole exact source-derived one-marker guest/branch contract')
  except ValueError as error:faults.append(dict(kind=label,rejectedBy=str(error)))
  else:raise ValueError('Source guest fault admitted '+label)
 for label,at in [('wrong marker',0xffbce),('wrong hardware address',0xffbd6),('old startup target',0xffbc0+128),('old contact target',0xffbc0+146),
                  ('old loop target',0xffbc0+160),('old rebound target',0xffbc0+218),('unrelated guest edit',0x12340)]:
  bad=bytearray(guest);bad[at]^=1;reject(label,bytes(bad))
 paths=[Path(__file__),*list(STAGE.glob('*')),ROOT/'audit_v6635_kano_launch_native48k/asset_report.json',
  ROOT/'audit_v6635_kano_launch_native48k/kano_ball_launch.wav',ROOT/'mk3/mk3-maincpu.bin',Path(prior.__file__),
  *[ROOT/d/'report.json'for d in ['audit_v6623_donor_ball_startup_source','audit_v6626_donor_ball_startup_helpers','audit_v6629_donor_ball_voice_kernel']]]
 pins={str(p.resolve()):sha(p)for p in paths if p.is_file()}
 result=dict(passed=True,sourceOnlyAccepted=True,compiledFixAccepted=False,nativeFixAccepted=False,publicBuildPromoted=False,fullPortAcceptance=False,
  stagedSourceDirectory=str(STAGE),stagedSourceHashes={name:sha(STAGE/name)for name in expected_sources()},
  priorCandidate=prior.NAME,priorExecutableSHA256=prior.EXE_SHA,priorGuestSHA256=prior.GUEST_SHA,
  expectedGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),expectedGuestChangedBytes=sum(a!=b for a,b in zip(base,guest)),
  guestChangeRange=[0xffbc0,0xffd80],insertedNativeWords=[0x09e0,0x6b03,0,0x0580,0x1030,0x01d0],all4InternalBranchTargetsRelocated=True,
  donorCommand=0x208,donorAsset=donor['stagedAsset'],donorAssetSHA256=donor['assetSHA256'],donorFirstPCMDelaySeconds=donor['firstPCMDelaySeconds'],
  sourceNegativeFaults=faults,inputHashes=pins,newBuilds=0,newROMCopies=0,goalStatus='active')
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(result,indent=2)+'\n')
 for p in [*list(STAGE.glob('*')),OUT/'report.json']:
  if p.is_file():
   h=sha(p);subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True,check=True);need(sha(p)==h,'Lossless exact staged source/proof compression')
 print(json.dumps({k:result[k]for k in ('passed','sourceOnlyAccepted','nativeFixAccepted','expectedGuestSHA256','expectedGuestChangedBytes','donorCommand')}),flush=True)
if __name__=='__main__':main()
