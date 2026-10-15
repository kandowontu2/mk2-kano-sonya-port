"""Source-qualified current native-packet/sample-marker collision and staged fix.

This is a staged source regression, NOT a newly compiled executable/runtime
acceptance. Failed audio gates remain failed and their captures immutable.
"""
import hashlib
import json
import re
import struct
from pathlib import Path
import map_current_native_feature_coverage_v3590 as current
import run_current_tomb_audio_ram_v3661 as audio

ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v3670_native_sound_packet_guard_checked'
STAGED=ROOT/'audit_v3668_native_sound_packet_source/midtunit_m.cpp'
ORIGINAL=ROOT/'diagnostic_v3172_native_morph_shadow/input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'

def run():
    need(not OUT.exists(),'Fresh staged regression report')
    need(sha(ORIGINAL)=='F509CC18D5C9CA4152508E52FEBA23B93A1B6C4085986E498F02C53E5BE7EABA','Actual compiled source unchanged')
    original=ORIGINAL.read_text();staged=STAGED.read_text()
    comment='''\t\t\t\t// Native MKII packets sign-extend both their high and low bytes.
\t\t\t\t// FFF7..FFFE are therefore valid native packet bytes, not globally
\t\t\t\t// reserved imported cues. Only the character scripts' direct port
\t\t\t\t// writes may use those markers; both original packet-store sites
\t\t\t\t// must continue to reach DCS unchanged, including attract mode.
\t\t\t\tbool const native_packet = m_maincpu->pc() == 0xffa13c90U ||
\t\t\t\t\tm_maincpu->pc() == 0xffa13d60U;
'''
    expected=original.replace('\t\t\tcase SOUND_DCS:\n','\t\t\tcase SOUND_DCS:\n'+comment)
    conditions=('(data == 0xfff8 || data == 0xfff7)','(data == 0xfffa || data == 0xfff9)','data >= 0xfffb && data <= 0xfffe')
    for condition in conditions:
        needle='if (m_mk2ks_voices && '+condition+')'
        need(expected.count(needle)==1,'Exact original imported routing branch')
        expected=expected.replace(needle,'if (m_mk2ks_voices && !native_packet && '+condition+')')
    need(staged==expected,'Whole staged source differs only in native packet guard and three FF-marker predicates')
    guest=current.current.expected_current()[0];rom=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    offset=lambda at:(at-0xff800000)//8
    need(guest[offset(0xffa13ba0):offset(0xffa13de0)]==rom[offset(0xffa13ba0):offset(0xffa13de0)],'Entire original native packet transmitter unchanged')
    for at,opcode in ((0xffa13c60,0x0583),(0xffa13d30,0x0580)):
        need(struct.unpack_from('<HHH',guest,offset(at))==(opcode,0x1030,0x01d0),'Actual original native absolute sound-port store')
    # The stored program counter has consumed the store's extension words.
    native_pcs={0xffa13c90,0xffa13d60}
    markers=set(range(0xfff7,0xffff))
    original_route=lambda word:word in markers
    fixed_route=lambda word,pc:word in markers and pc not in native_pcs
    need(all(not fixed_route(word,pc)for pc in native_pcs for word in range(65536)),'All 131072 native full-word inputs remain DCS packets')
    need(all(fixed_route(word,0xfffb7140)==original_route(word)for word in range(65536)),'Every direct custom word retains its previous routing')
    folder=ROOT/'audit_v3666_current_kano_tomb_audio_p1_samples'
    baseline=ROOT/'audit_v3666_current_kano_tomb_audio_p1_nosamples'
    meta=json.loads((folder/'result.json').read_text());oldmeta=json.loads((baseline/'result.json').read_text())
    need(meta['exit_code']==oldmeta['exit_code']==0 and meta['candidate']==current.NAME,'Both actual current captures terminal, without importing their failed acceptance')
    for terminal in (meta,oldmeta):
        need(all(sha(p)==h for p,h in terminal['input_hashes'].items()),'Every actual captured source input unchanged')
    log=(folder/'run.log').read_text();oldlog=(baseline/'run.log').read_text()
    need(audio.rows(log,'SOUND')==audio.rows(oldlog,'SOUND'),'Same native sound calls with/without imported samples')
    result=[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in log.splitlines()if line.startswith('MK2_STAGE_RESULT ')]
    need(len(result)==1 and result[0]['action']=='8173','Actual native Tomb action context')
    collisions=[r for r in audio.rows(log,'SOUND')if int(r['word'],16)in markers and int(r['pc'],16)in native_pcs]
    need(collisions,'Actual observed native packet collision, not hypothetical metadata')
    channels=audio.rows(log,'CHANNEL');evidence=[]
    for packet in collisions:
        word=int(packet['word'],16);frame=int(packet['frame'])
        need(original_route(word)and not fixed_route(word,int(packet['pc'],16)),'Staged guard repairs actual bad branch')
        if word==0xfff8:
            started=[r for r in channels if int(r['frame'])==frame+1 and r['channel']=='2']
            need(len(started)==1 and started[0]['sample']=='6'and float(started[0]['pos'])<2000,'Actual native F8 packet wrongly starts imported Sonya fire')
            evidence.append(dict(nativePacket=packet,wrongImportedSample=started[0]))
    need(evidence,'Verified physical imported fire-channel transition')
    # Correct the rejected verifier expectation from original packed voice code,
    # not by accepting an arbitrary observed command or altering the game.
    need(struct.unpack_from('<HHH',rom,offset(0xffa11fe0))==(0x09e1,0x3638,0x3234)and
         struct.unpack_from('<HH',rom,offset(0xffa123b0))==(0x2701,0x2d01),'Original female selector isolates packed low byte 38h')
    scream=[r for r in audio.rows(log,'ROUTE')if r['entry']=='FFA11FD0']
    need(len(scream)==1 and scream[0]['id']=='18'and scream[0]['owner']==scream[0]['a8'],'Actual owned Sonya victim, true ID18')
    chosen=[r for r in audio.rows(log,'ROUTE')if r['frame']==scream[0]['frame']and r['entry']=='FFA12530']
    need(len(chosen)==1 and int(chosen[0]['a0'],16)in(0x38,0x39),'Actual original female random scream range')
    pins={str(p):sha(p)for p in (Path(__file__).resolve(),ORIGINAL,STAGED,ROOT/'mk2/mk2-maincpu.bin',
      ROOT/'tools/run_current_tomb_audio_ram_v3661.py',ROOT/'tools/run_current_tomb_audio_ram_v3665.py',
      ROOT/'mk2ks_current_tomb_audio_ram_v3660.lua',ROOT/'mk2ks_current_tomb_audio_ram_v3664.lua',
      ROOT/'audit_v3663_current_tomb_audio_routing_checked/report.json',ROOT/'audit_v3667_current_tomb_audio_routing_checked/report.json')}
    for terminal in(meta,oldmeta):pins.update(terminal['input_hashes'])
    for leaf in(folder,baseline):
        for path in leaf.rglob('*'):
            if path.is_file():pins[str(path)]=sha(path)
    return dict(passed=True,candidate=current.NAME,stagedSource=str(STAGED),stagedSourceSHA256=sha(STAGED),
      actualNativePacketCollisions=collisions,actualWrongImportedFireTransitions=evidence,
      exhaustiveNativePacketWords=131072,exhaustiveDirectWordComparisons=65536,
      sourceQualifiedFemaleScream=dict(packed=0x32343638,range=[0x38,0x39],actual=chosen[0]),
      rejectedVerifierExpectationsPreserved=True,stagedFixRequiresCompilationAndRuntimeRegression=True,
      nativeDCSStageOrVictimWaveformFidelityAccepted=False,fullPortAcceptance=False,
      publicBuildChanged=False,newExecutableROMRasterOrAudioCopies=0,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    report=run();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','scope','actualNativePacketCollisions')},indent=2))
