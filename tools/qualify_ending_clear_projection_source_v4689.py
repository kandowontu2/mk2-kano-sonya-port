"""Actual beam-ledger source and original TMS/T-unit partial-update semantics."""
import ast,copy,json,re,subprocess
from pathlib import Path
import qualify_ending_clear_beam_source_v4680 as prior
import ending_clear_beam_projection_v4688 as projection
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
LUA=prior.LUA
OUT=ROOT/'audit_v4690_ending_clear_projection_source_checked'
TRANSITIVE_LUA=prior.TRANSITIVE_LUA

def source_boundary():
    prior.source_boundary()
    r=json.loads((ROOT/'audit_v4684_kano_ending_clear_beam_probe_observed/report.json').read_text())
    need(r['passed']and r['everyOriginalColdNativeEventAndRGBUnchanged']and r['actualDiagnosticFields']==21,
         'Actual read-only probe source proven non-invasive for full cold policy and58RGB')
    failed=r['records'][10];b=[x for x in r['actualCPUBuckets']if x['frame']=='58183']
    projection.validate(failed['native'],b)
    need(failed['hardwareDerivedStart']['mismatchedPixels']==84 and failed['hardwareDerivedStart']['firstMismatch']==[0,356],
         'Actual84pixel end-VRAM mismatch retained, no tolerance or raster admission yet')
    source=ROOT/'mame-mkp/src/devices/cpu/tms34010/tms34010.cpp';code=source.read_text()
    partial=code.index('screen().update_partial(vcount);');advance=code.index('dpyadr = ((dpyadr & 0xfffc) - (IOREG(REG_DPYCTL) & 0x03fc))')
    need(partial<advance and 'SMART_IOREG(VCOUNT) = vcount;'in code and 'params->rowaddr = dpyadr >> 4;'in code,
         'Original visible partial update before DPYADR decrement; actual bucket samples post-row hardware')
    unit=(ROOT/'mame-mkp/src/mame/midway/midtunit_v.cpp').read_text()
    for token in('offset *= 2;','m_local_videoram[offset] = (data & 0xff) | ((m_dma_register[DMA_PALETTE] & 0xff) << 8);',
                  'm_local_videoram[offset + 1] = ((data >> 8) & 0xff) | (m_dma_register[DMA_PALETTE] & 0xff00);',
                  'src[coladdr++ & 0x1ff] & 0x7fff;'):
        need(token in unit,'Original paired CPU pixels and source indexed scanline read '+token)
    screen=(ROOT/'mame-mkp/src/emu/screen.cpp').read_text()
    need('void screen_device::pixels(u32 *buffer)'in screen and '*buffer++ = palette[*src++];'in screen,
         'Actual Lua pixels convert indexed scanline surface using current palette, not latest VRAM')
    return dict(passed=True,actualBeamBuckets=len(b),actualEndVRAMMismatchPixels=84,nativeProjectionAcceptance=False,fullEndingRendererVideoAccepted=False)

def main():
    need(not OUT.exists(),'Fresh immutable preboot beam projection source')
    positive=source_boundary()
    import run_ending_clear_projection_ram_v4687 as capture
    generated=capture.collector()
    need('prior_raw'in generated.__code__.co_varnames and 'cpu_buckets'in generated.__code__.co_varnames and
         'errors'in generated.__code__.co_varnames and generated.__globals__['projection'].__file__==projection.__file__ and
         generated.__globals__['LUA']==LUA,'Actual full collector previous-field/beam/PCM-free RAM and correct module/Lua binding')
    r=json.loads((ROOT/'audit_v4684_kano_ending_clear_beam_probe_observed/report.json').read_text())
    native=r['records'][10]['native'];b=[x for x in r['actualCPUBuckets']if x['frame']=='58183'];faults=[]
    for label,key,value in(('wrong_beam','beam','18'),('wrong_DP YADR'.replace(' ',''),'dpyadr','0000'),
                           ('wrong_mask','mask','00FF'),('wrong_count','count','1'),('foreign_instruction','pc','FFF00000')):
        bad=copy.deepcopy(b);bad[0][key]=value
        need(bad!=b,'Non-vacuous actual beam fault')
        try:projection.validate(native,bad)
        except ValueError as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Actual beam fault accepted '+label)
        projection.validate(native,b)
    files=[Path(__file__).resolve(),Path(capture.__file__).resolve(),Path(projection.__file__).resolve(),Path(prior.__file__).resolve(),
           Path(capture.previous.__file__).resolve(),ROOT/'audit_v4684_kano_ending_clear_beam_probe_observed/report.json',
           ROOT/'mame-mkp/src/devices/cpu/tms34010/tms34010.cpp',ROOT/'mame-mkp/src/mame/midway/midtunit_v.cpp',ROOT/'mame-mkp/src/emu/screen.cpp']
    files.extend(ROOT/p for p in TRANSITIVE_LUA)
    for p in files:
        if p.suffix=='.py':ast.parse(p.read_text(),filename=str(p))
    report=dict(positive,actualBeamLedgerFaultsRejected=faults,inputHashes={str(p.resolve()):sha(p)for p in files},
                rawMediaFilesWritten=0,fullPortAcceptance=False)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)

if __name__=='__main__':main()
