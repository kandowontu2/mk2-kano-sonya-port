"""Current3836 Kano P2 cold tower using unchanged original accepted inputs.

Reuse whole4439 collector with only actual role/policy/path/preflight changes.
All initialized guest bytes and native RGB in RAM. No new builds/raw media.
An actual terminal observation is not full campaign, ending-art/audio acceptance.
"""
import inspect,json,subprocess,traceback
from pathlib import Path
import run_kintaro_pressure_guard_long_campaign_v4439 as previous
import qualify_kano_current_p2_campaign_source_v4482 as source
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
NAME=previous.NAME
LUA=source.LUA
FOLDER=ROOT/'audit_v4485_kano_current_p2_campaign_ram'
OUT=ROOT/'audit_v4486_kano_current_p2_campaign_observed'

def collector():
    text=inspect.getsource(previous.capture)
    changes=[("need(fighter=='sonya','Actual unfinished Sonya P2 context only')",
              "need(fighter=='kano','Current missing Kano P2 context only')"),
             ('audit_v4438_kintaro_pressure_guard_long_source_preflight/report.json',str(source.OUT.relative_to(ROOT))+'/report.json'),
             ("folder=ROOT/f'audit_v4440_{fighter}_kintaro_pressure_guard_long_p2_campaign'","folder=FOLDER"),
             ("MK2KS_CAMPAIGN_STRATEGY='guard_punish'","MK2KS_CAMPAIGN_STRATEGY='zoning'")]
    for before,after in changes:
        need(text.count(before)==1,'Unique role/policy/path-only full collector adaptation: '+before)
        text=text.replace(before,after,1)
    scope=dict(vars(previous));scope.update(__file__=__file__,source=source,LUA=LUA,FOLDER=FOLDER)
    exec(compile(text,__file__+'::entire4439_collector_original_Kano_inputs','exec'),scope)
    return scope['capture']

def main():
    need(not FOLDER.exists() and not OUT.exists(),'Fresh cold native capture, never restart an executed leaf')
    folder,headers,images=collector()('kano')
    rows=previous.knife.old.parse((folder/'run.log').read_text(),2,'kano')
    report=dict(passed=True,candidate=NAME,capture=str(folder),
                stages=[r['stage'] for r in rows if r['tag']=='STAGE'],
                endingStarts=sum(r['tag']=='ENDING_START' for r in rows),
                endingCompletions=sum(r['tag']=='ENDING_COMPLETED' for r in rows),
                actualNativeFrameCallbacks=len(headers),fullIndependentCampaignVerificationPending=True,
                fullEndingPixelsAudioAccepted=False,newBuildsOrROMCopies=0,rawRasterAudioVRAMROMFilesWritten=0,
                fullPortAcceptance=False,scope=__doc__)
    return report

if __name__=='__main__':
    try:report=main()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable actual observation report');OUT.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,
         'Observation proof compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)
    raise SystemExit(0 if report['passed'] else 1)
