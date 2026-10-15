"""Whole5925 native schedule and14 faults, stable evidence restoration.

Preserve its actual final equality failure. The observation timestamp changes
on each validation call; compare all evidence unchanged, excluding only that
host timestamp. No native rerun or data/source/shadow/font gate is relaxed.
"""
import inspect
from qualify_stock_pit_shadow_schedule_v5925 import *
import qualify_stock_pit_shadow_schedule_v5925 as previous
OUT=ROOT/'audit_v5928_original_stock_pit_shadow_schedule_checked'
FAILURE=ROOT/'audit_v5926_original_stock_pit_shadow_schedule_checked/report.json'

def stable(value):return {k:v for k,v in value.items()if k!='observedUTC'}

source=inspect.getsource(previous.run)
old="schedule(text,stock,pins,0,sha(STOCK),guest)==positive"
need(source.count(old)==1,'Only generated host observation timestamp excluded from full restoration comparison')
source=source.replace(old,"stable(schedule(text,stock,pins,0,sha(STOCK),guest))==stable(positive)",1)
old=" for p in (Path(__file__),Path(captured.__file__),Path(previous.__file__),FAILED,ROOT/'mk2_stock_pit_shadow_inventory_v5916.lua',"
need(source.count(old)==1,'Whole original schedule dependencies retained plus actual failed qualifier')
source=source.replace(old," for p in (Path(__file__),Path(captured.__file__),Path(previous.previous.__file__),FAILED,FAILURE,Path(previous.__file__),ROOT/'mk2_stock_pit_shadow_inventory_v5916.lua',",1)
scope=dict(globals(),__file__=__file__,stable=stable)
exec(compile(source,__file__+'::whole5925_stable_source_native_restoration','exec'),scope)
run=scope['run'];run.source=source

if __name__=='__main__':
 failure=json.loads(FAILURE.read_text())
 need(not failure['passed']and failure['error']=="ValueError('All14 actual schedule/source faults reject and complete positive restores')",'Preserve whole actual5925final host-timestamp equality failure')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();save(OUT/'report.json',report)
 for p in (Path(__file__),OUT/'report.json'):
  before=sha(p);done=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True)
  need(done.returncode==0 and sha(p)==before,'Lossless bounded qualified original text')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','remaining','sourceNativeCommand','sourceNativeNonFloorFontDraws','effectiveActualScheduleFaultsRejected')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
