"""Exact cold controls; strictly read-only failed-switch hardware probe."""
import ast,json,re,subprocess
from pathlib import Path
import qualify_kano_current_p2_campaign_source_v4482 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_v4601_ending_latch_probe_source_checked'
LUA='mk2ks_kano_ending_latch_probe_ram_v4599.lua'
TRANSITIVE_LUA=original.TRANSITIVE_LUA+(LUA,'mk2ks_native_tomb_ram_v3624.lua')
def source_boundary():
    original.source_boundary();text=(ROOT/LUA).read_text()
    need(text.startswith("-- Exact accepted cold controls; observe the previously failed switch only.\ndofile('mk2ks_kano_current_p2_campaign_ram_v4472.lua')\n"),
      'Whole previously accepted native cold physical policy unchanged')
    need(text.count('dofile(')==1 and not re.search(r':write_\w+\s*\(|write_u\d+\s*\(|\.value\s*=(?!=)|load_?state|set_value|clear_value|return\s+data|snapshot\(',text),
      'No native/control/register/identity/health/AI/palette/RNG mutation or native media sink')
    for token in ('cpu.PC.value~=0xff8296b0','cpu.PC.value~=0xff836700','mask~=0xffff','p:read_u16(at)<=0',
      'wins~=1','p:read_u16(0x01061b00)==2','roster==17','p:read_u32(0x01060220)==0','p:read_u32(0x01060df0)==0',
      'frame-origin<1100','frame-origin>1140','0xc00001e0','0xc00001d0','0xc0000060'):
        need(token in text,'Original own ending/earned KO and actual hardware failed-window observation: '+token)
    need(re.findall(r'io.open\(([^\n]+)',text)==["'mk2ks_native_tomb_ram_v3624.lua','r'))"],
      'One existing read-only RAM transport dependency')
    return dict(passed=True,fullVideoAcceptance=False,fullPortAcceptance=False)
def main():
    need(not OUT.exists(),'Fresh immutable source qualification')
    source_boundary()
    import run_ending_latch_probe_ram_v4602 as capture
    generated=capture.collector();need('errors'in generated.__code__.co_varnames and 'probe_records'in generated.__code__.co_varnames,
      'Original stderr handle and diagnostic records remain separate')
    files=[Path(__file__).resolve(),Path(capture.__file__),Path(original.__file__),ROOT/'tools/current_tomb_ram_model_v3642.py']+[ROOT/p for p in TRANSITIVE_LUA]
    for p in files:
        if p.suffix=='.py':ast.parse(p.read_text(),filename=str(p))
    report=dict(passed=True,inputHashes={str(p.resolve()):sha(p)for p in files},
      actualNativeRasterSwitchCauseEstablished=False,fullVideoAcceptance=False,fullPortAcceptance=False)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
if __name__=='__main__':main()
