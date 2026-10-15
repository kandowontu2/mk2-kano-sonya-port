"""Bounded actual second-page counterexample, read-only cold-policy source."""
import ast,json,re,subprocess
from pathlib import Path
import qualify_ending_latch_probe_source_v4606 as old
ROOT,need,sha=old.ROOT,old.need,old.sha
LUA='mk2ks_kano_ending_clear_beam_probe_ram_v4669.lua'
OUT=ROOT/'audit_v4672_ending_clear_beam_source_checked'
TRANSITIVE_LUA=old.TRANSITIVE_LUA+(LUA,)

def source_boundary():
    old.source_boundary();wrapper=(ROOT/LUA).read_text()
    need(wrapper.count('io.open(')==1 and "io.open('mk2ks_kano_ending_latch_probe_ram_v4599.lua','rb')"in wrapper and
         "assert(load(source,'@whole4599_cold_policy_second_page_beam_RAM_only_4669','t',_ENV))()"in wrapper,
         'Complete existing read-only probe/controller load, no new physical inputs')
    need(not re.search(r':write_\w+\s*\(|write_u\d+\s*\(|\.value\s*=(?!=)|load_?state|set_value|clear_value|return\s+data|snapshot\(',wrapper),
         'No guest/control/register/identity/health/AI/RNG/position/palette writes or native raster disk sink')
    for before,after in(
      ('frame-origin<1095 or frame-origin>1145','frame-origin<1877 or frame-origin>1897'),
      ('frame-origin>=1095 and frame-origin<=1145','frame-origin>=1877 and frame-origin<=1897'),
      ('frame-origin<1100 or frame-origin>1140','frame-origin<1877 or frame-origin>1897'),
      ('assert(#taps==3)','assert(#taps==4)')):
        need(f"once('{before}','{after}')"in wrapper,'Exact bounded phase adapter '+before)
    for token in ('p:install_write_tap(0,0x001fffff','frame-origin<1877 or frame-origin>1897',
                  'p:read_u16(0xc00001d0)','p:read_u16(0xc00001e0)','bucket.count=bucket.count+1',
                  "log('CPU_BUCKET'","log('CPU_TOTAL'",'buckets={}')):
        need(token in wrapper,'Complete read-only actual beam/address/PC/data/mask/count observation '+token)
    failed=ROOT/'audit_v4649_kano_p2_ending_display_actual_metadata_ram'
    meta=json.loads((failed/'result.json').read_text())
    need(meta['exit_code']==0 and meta['observedEndingRGBFields']==3040 and meta['exactContinuousEndingFields']==1887 and
         len(meta['endingModelErrors'])==1 and 'frame=58183 'in meta['endingModelErrors'][0]['line'],
         'Actual late counterexample and earlier1887 exact fields preserved; whole ending remains unaccepted')
    guest=old.original.expected();rom=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    a,b=(0xff80f400-0xff800000)//8,(0xff80f600-0xff800000)//8
    need(guest[a:b]==rom[a:b],'Whole actual original CPU clear routine unchanged, not a port hook')
    return dict(passed=True,nativeRasterCauseAccepted=False,fullEndingRendererVideoAccepted=False,fullPortAcceptance=False)

def main():
    need(not OUT.exists(),'Fresh immutable before-boot clear/beam source')
    source_boundary()
    import run_ending_clear_beam_probe_ram_v4670 as capture
    generated=capture.collector()
    need('errors'in generated.__code__.co_varnames and 'probe_records'in generated.__code__.co_varnames and
         'current'not in generated.__code__.co_varnames and 'current_comparison'in generated.__code__.co_varnames and
         generated.__globals__['LUA']==LUA,'Actual generated cold-control/diagnostic scopes bound before boot')
    files=[Path(__file__).resolve(),Path(capture.__file__).resolve(),Path(capture.previous.__file__).resolve(),Path(old.__file__).resolve(),
           ROOT/'audit_v4649_kano_p2_ending_display_actual_metadata_ram/result.json',ROOT/'audit_v4650_kano_p2_ending_display_actual_metadata_checked/report.json']
    files.extend(ROOT/p for p in TRANSITIVE_LUA)
    for p in files:
        if p.suffix=='.py':ast.parse(p.read_text(),filename=str(p))
    report=dict(passed=True,inputHashes={str(p.resolve()):sha(p)for p in files},actualPriorFailedFrame=58183,
                sameOriginalColdCampaignAndWholeGuest=True,wholeOriginalCPUClearRoutineUnchanged=True,
                observationFields=21,rawMediaFilesWritten=0,nativeRasterCauseAccepted=False,fullEndingRendererVideoAccepted=False,fullPortAcceptance=False)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)

if __name__=='__main__':main()
