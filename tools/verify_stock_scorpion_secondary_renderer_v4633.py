"""Actual stock shadow register semantics: A1 is command post-skip shift.

Original FF801430/450/460 derives A1=(command>>10)&3, not DMA height.
Retain the source-proven final duplicate-row Y=A0+1 and entire stock window.
Frozen failed assumptions remain untouched; game/capture pixels unchanged.
"""
import inspect,json,re,subprocess,traceback
from pathlib import Path
import verify_stock_scorpion_secondary_renderer_v4625 as base
import verify_stock_scorpion_secondary_renderer_v4629 as final_row
ROOT,need,sha,CASE=base.ROOT,base.need,base.sha,base.CASE
OUT=ROOT/'audit_v4634_stock_kitana_scorpion_secondary_renderer_checked'
source=inspect.getsource(base.stock_shadow_rows)
for before,after in [("int(r['a0'],16)==int(d['y'])","((int(r['a0'],16)+(d['pc']=='FF801610'))&511)==int(d['y'])"),
                     ("r['a1']=='00000001'","int(r['a1'],16)==((int(d['command'],16)>>10)&3)")]:
    need(source.count(before)==1,'Only declared original shadow register interpretation: '+before)
    source=source.replace(before,after,1)
namespace=dict(vars(base))
exec(compile(source,__file__+'::source_exact_stock_shadow_register_semantics','exec'),namespace)
stock_shadow_rows=namespace['stock_shadow_rows']
scope=dict(vars(base),__file__=__file__,stock_shadow_rows=stock_shadow_rows)
exec(compile(base.text,__file__+'::entire_declared_stock_contract','exec'),scope)
need(scope['contract'].__globals__['stock_shadow_rows']is stock_shadow_rows,
     'Actual complete generated stock contract uses source-qualified register semantics')
exec(compile(inspect.getsource(base.verify),__file__+'::whole4625_stock_verify','exec'),scope)
proof_scope=dict(vars(final_row),__file__=__file__,scope=scope,stock_shadow_rows=stock_shadow_rows)
exec(compile(inspect.getsource(final_row.verify),__file__+'::whole_native_final_row_proof','exec'),proof_scope)

def verify():
    report=proof_scope['verify']()
    exe=ROOT/'mame-mkp/unidasm.exe';rom=ROOT/'mk2/mk2-maincpu.bin'
    assembly=subprocess.run([str(exe),str(rom),'-arch','tms34010','-skip','0x286','-count','64','-basepc','0xff801430'],
                            capture_output=True,text=True,check=True,creationflags=subprocess.CREATE_NO_WINDOW).stdout
    for token in ('ff801430: 4dc1','ff801450: 2681','ff801460: 2c41'):
        need(token in assembly,'Actual original command-bit post-skip A1 source derivation: '+token)
    log=(CASE/'run.log').read_text();positive=stock_shadow_rows(log);d=positive[0]
    lines=log.splitlines();index=next(i for i,line in enumerate(lines)if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_DMA_REGS ')and
                                     f"event={d['event']} "in line)
    before=lines[index];a1=int(re.search(r'\ba1=([^\s]+)',before)[1],16)
    lines[index]=re.sub(r'\ba1=[^\s]+',f'a1={a1^1:08X}',before)
    need(lines[index]!=before,'Actual command-bit post-skip register fault')
    try:stock_shadow_rows('\n'.join(lines)+'\n')
    except ValueError as error:report['actualPipelineAndStockShadowFaultsRejected'].append(dict(label='wrong_actual_command_postskip_A1',rejectedBy=str(error)))
    else:raise ValueError('Accepted actual command post-skip A1 fault')
    need(stock_shadow_rows(log)==positive,'Every untouched original stock row positive restored after A1 fault')
    for p in (Path(__file__).resolve(),Path(base.__file__),Path(final_row.__file__)):
        report['inputHashes'][str(p)]=sha(p)
    report.update(originalCommandPostSkipRegisterSourceProven=True,explicitWholeGeneratedStockContractSourceBinding=True,
                  scope=__doc__)
    need(all(sha(p)==h for p,h in report['inputHashes'].items()),'Every original/current source/capture/public byte unchanged')
    return report

if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable original stock register qualification')
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
