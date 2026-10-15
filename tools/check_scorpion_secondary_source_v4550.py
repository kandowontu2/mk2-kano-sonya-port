"""Current source/guest native release path; no retired capture resurrection."""
import hashlib,json,re,struct,subprocess
from pathlib import Path
import run_kintaro_pressure_guard_long_campaign_v4439 as current
ROOT,need,sha,NAME=current.ROOT,current.need,current.sha,current.NAME
OUT=ROOT/'audit_v4551_current_scorpion_secondary_source_checked'
LUA='mk2ks_scorpion_secondary_state_ram_v4534.lua'
CONTROL='mk2ks_stock_scorpion_secondary_inputs_v1210.lua'

def source_boundary():
    wrapper=(ROOT/LUA).read_text();controls=(ROOT/CONTROL).read_text()
    need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|return\s+data|io\.open\([^\n]*["\']w',wrapper+controls),
      'No guest/register/health/AI/identity/palette/RNG/position manipulation or native disk-media sink')
    need(controls.count('screen:snapshot(')==2 and "source:gsub('screen:snapshot%(', '_scorpion_emit(')" in wrapper and
      'assert(count==2' in wrapper and "@entire1210_physical_controls_two_RAM_sinks_only_4534"in wrapper,
      'Whole unchanged physical policy; exactly two RAM-only image sink substitutions')
    need(re.findall(r'io\.open\(([^\n]+)',wrapper)==["'mk2ks_stock_scorpion_secondary_inputs_v1210.lua','r'))"],
      'Only one explicit read-only existing controller dependency')
    need('cpu.PC.value~=entry+16' in wrapper and 'cpu.PC.value~=0xff8296b0' in wrapper and
      'p:read_u16(0x01061b00)~=3'in wrapper and 'vid~=identity'in wrapper and 'id~=10'in wrapper and
      'frame-origin<=960'in wrapper and '>=94'in wrapper,
      'Real original instruction fetches, true physical own/victim IDs, complete native phase window and only host observation deadline')
    guest=current.expected();original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    off=lambda a:(a-0xff800000)//8
    for lo,hi in ((0xff814af0,0xff814b70),(0xff868700,0xff868930),(0xff876b40,0xff876be0),
      (0xff876f70,0xff877420),(0xff8775d0,0xff8779b0),(0xff878420,0xff8784f0),
      (0xff8bbfe0,0xff8bd040),(0xff841d10,0xff841e10)):
        need(guest[off(lo):off(hi)]==original[off(lo):off(hi)],'Every original release/parser/victim/completion instruction: '+hex(lo))
    u32=lambda data,a:struct.unpack_from('<I',data,off(a))[0]
    need(u32(original,0xff814b00)==0xff863020 and u32(original,0xff863020)==0xff863140 and
      u32(original,0xff863190+10*32)==u32(guest,u32(guest,0xff863150)+10*32)==0xff868700 and
      u32(original,0xff8ba390+10*32)==u32(guest,0xff8ba390+10*32)==0xff8bbfe0,
      'Untouched real Scorpion HP-release dispatch and second fatality, never character substitution')
    need(struct.unpack_from('<13H',original,off(0xff878420))==(56,8,8,8,6,0,0,7,7,7,6,0,0),
      'Original native facing-relative Down F F F release history')
    return dict(passed=True,currentGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),
      controlSHA256=sha(ROOT/CONTROL),observerSHA256=sha(ROOT/LUA),retiredCaptureFilesReadOrRecreated=0,
      onlyPhysicalControlsAndReadOnlyNativeEvidence=True,nativeActivationOrArtAccepted=False,fullPortAcceptance=False)

def main():
    need(not OUT.exists(),'Fresh immutable before-boot current Scorpion source proof')
    positive=source_boundary();files=[Path(__file__).resolve(),ROOT/LUA,ROOT/CONTROL,ROOT/'mk2/mk2-maincpu.bin',
      ROOT/NAME/'mkport_candidate.exe',ROOT/NAME/'roms/mk2ks/mk2ks.mdata',ROOT/NAME/'build-info.json',
      ROOT/'tools/run_current_scorpion_secondary_state_v4549.py']
    import ast
    for p in files:
        if p.suffix=='.py':ast.parse(p.read_text(),filename=str(p))
    build=json.loads((ROOT/NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    for p,h in build['input_hashes'].items():need(sha(p)==h,'Every actual compiled input unchanged')
    report=dict(positive,inputHashes={str(p.resolve()):sha(p)for p in files})
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress source evidence before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(positive,indent=2),flush=True)

if __name__=='__main__':main()
