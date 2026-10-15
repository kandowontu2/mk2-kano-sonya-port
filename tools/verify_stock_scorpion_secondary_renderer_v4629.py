"""Fresh original-stock row proof; final duplicate row uses DMA Y=A0+1.

Original FF8015B0 increments A0, writes hardware Y, then FF8015D0 restores
A0 before the final DMA at FF801600. Preserve frozen4625 failed assumption.
No field/pixel/physical/callback gate removed; no game or capture changes.
"""
import inspect,json,subprocess,traceback
from pathlib import Path
import verify_stock_scorpion_secondary_renderer_v4625 as previous
ROOT,need,sha,CASE=previous.ROOT,previous.need,previous.sha,previous.CASE
OUT=ROOT/'audit_v4630_stock_kitana_scorpion_secondary_renderer_checked'
source=inspect.getsource(previous.stock_shadow_rows)
before="int(r['a0'],16)==int(d['y'])"
after="((int(r['a0'],16)+(d['pc']=='FF801610'))&511)==int(d['y'])"
need(source.count(before)==1,'Only original final-row hardware Y/register phase correction')
source=source.replace(before,after,1)
namespace=dict(vars(previous))
exec(compile(source,__file__+'::original_final_duplicate_row_register_phase','exec'),namespace)
stock_shadow_rows=namespace['stock_shadow_rows']
scope=dict(vars(previous),__file__=__file__,stock_shadow_rows=stock_shadow_rows)
exec(compile(inspect.getsource(previous.scope['contract']),__file__+'::whole4592_stock_contract','exec'),scope)
contract=scope['contract']
scope.update(contract=contract,stock_shadow_rows=stock_shadow_rows)
exec(compile(inspect.getsource(previous.verify),__file__+'::whole4625_stock_renderer_qualification','exec'),scope)

def verify():
    report=scope['verify']()
    exe=ROOT/'mame-mkp/unidasm.exe';rom=ROOT/'mk2/mk2-maincpu.bin'
    assembly=subprocess.run([str(exe),str(rom),'-arch','tms34010','-skip','0x298','-count','1024','-basepc','0xff8014c0'],
                            capture_output=True,text=True,check=True,creationflags=subprocess.CREATE_NO_WINDOW).stdout
    for token in ('ff801580: 8006','ff801590: 81c3','ff8015b0: 1020','ff8015c0: 8006',
                  'ff8015d0: 1420','ff801600: 81c3','ff801610: 0b09'):
        need(token in assembly,'Original native ordinary/final shadow DMA Y increment/restore source: '+token)
    log=(CASE/'run.log').read_text();native=stock_shadow_rows(log)
    final=next(d for d in native if d['pc']=='FF801610')
    lines=log.splitlines();index=next(i for i,line in enumerate(lines)if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_DMA_REGS ')and
                                     f"event={final['event']} "in line)
    import re
    original=lines[index];a0=int(re.search(r'\ba0=([^\s]+)',original)[1],16)
    lines[index]=re.sub(r'\ba0=[^\s]+',f'a0={a0+1:08X}',original)
    need(lines[index]!=original,'Actual final duplicated-row register phase fault')
    try:stock_shadow_rows('\n'.join(lines)+'\n')
    except ValueError as error:report['actualPipelineAndStockShadowFaultsRejected'].append(dict(label='wrong_actual_final_duplicate_row_A0',rejectedBy=str(error)))
    else:raise ValueError('Accepted actual final duplicate row A0 fault')
    need(stock_shadow_rows(log)==native,'Every unchanged original stock row restored after actual final-row fault')
    for p in (exe,rom,Path(__file__).resolve(),Path(previous.__file__)):
        report['inputHashes'][str(p)]=sha(p)
    report.update(originalFinalDuplicateRowRegisterPhaseSourceProven=True,
                  actualFinalDuplicateRows=sum(d['pc']=='FF801610'for d in native),
                  scope=__doc__)
    need(all(sha(p)==h for p,h in report['inputHashes'].items()),'All source/capture/native/public inputs unchanged')
    return report

if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable corrected original stock row qualification')
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
