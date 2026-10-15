"""Bounded lossless compaction of four retained terminal boss captures, no deletion."""
import json,subprocess
from pathlib import Path
import compact_current_tomb_logs_v3654 as storage
import run_kintaro_backward_escape_campaign_v4323 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v4333_frozen_boss_audio_compaction'
NAMES=('audit_v2611_current_kano_p1_shao_walking_retreat_campaign',
       'audit_v2611_current_sonya_p1_shao_walking_retreat_campaign',
       'audit_v2633_current_kano_p1_shao_cooldown_retreat_campaign',
       'audit_v2633_current_sonya_p1_shao_cooldown_retreat_campaign')

def exact(path):
    path=Path(path)
    need(path.is_absolute() and path.parent.parent==ROOT and path.parent.name in NAMES and path.name=='native_mix.wav',
         'Only explicitly named original frozen audio files')
    for p in (path,*path.parents):
        if p==ROOT:break
        need(not p.lstat().st_file_attributes&0x400,'No reparse target/ancestor')
    need(path.is_file() and path.stat().st_nlink==1,'Regular unshared file, no hardlink mutation')
    return path

def main():
    need(not OUT.exists(),'Fresh immutable storage report')
    literals=' -or '.join("$_.CommandLine -like '*"+name+"*'" for name in NAMES)
    q=subprocess.run(['powershell.exe','-NoProfile','-Command',
      'Get-CimInstance Win32_Process -Filter "Name=\'mkport_candidate.exe\' OR Name=\'mkport.exe\' OR Name=\'mame.exe\' OR Name=\'hbmame.exe\'" | Where-Object { '+literals+' } | Select-Object ProcessId,Name | ConvertTo-Json -Compress'],capture_output=True,text=True)
    need(q.returncode==0 and not q.stdout.strip(),'No native process owns any selected frozen capture')
    keep=(ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd',ROOT/'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe',
      ROOT/current.NAME/'mkport_candidate.exe',ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata',ROOT/'mame-mkp/mkport.exe',
      ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp',ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip')
    pins={str(p.resolve()):sha(p) for p in keep}
    pins[str(Path(__file__).resolve())]=sha(__file__)
    pins[str(Path(storage.__file__).resolve())]=sha(storage.__file__)
    rows=[]
    for name in NAMES:
        result=ROOT/name/'result.json'
        need(json.loads(result.read_text(encoding='utf-8-sig'))['exit_code']==0,'Actual old capture terminal0')
        pins[str(result)]=sha(result)
        p=exact(ROOT/name/'native_mix.wav');s=p.stat()
        rows.append(dict(path=str(p),logicalBytes=s.st_size,mtimeNS=s.st_mtime_ns,
                         sha256=sha(p),allocatedBefore=storage.allocated(p)))
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Report compressed before writing')
    (OUT/'plan.json').write_text(json.dumps(dict(targets=rows,inputHashes=pins,deletedFiles=0),indent=2)+'\n')
    done=[];sample_saved=None
    for row in rows:
        if sample_saved==0:break
        p=exact(row['path']);s=p.stat()
        need(s.st_size==row['logicalBytes'] and s.st_mtime_ns==row['mtimeNS'] and
             storage.allocated(p)==row['allocatedBefore'] and sha(p)==row['sha256'],'Exact inventory still frozen before mutation')
        process=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/I','/Q',str(p)],capture_output=True)
        after=storage.allocated(p);s=p.stat()
        need(process.returncode==0 and sha(p)==row['sha256'] and s.st_size==row['logicalBytes'] and
             s.st_mtime_ns==row['mtimeNS'] and after<=row['allocatedBefore'],
             'Every original byte, path, size and timestamp preserved with no allocated growth')
        actual=dict(row,allocatedAfter=after,reclaimed=row['allocatedBefore']-after)
        done.append(actual);sample_saved=actual['reclaimed']
        print(json.dumps(dict(path=str(p),allocatedBefore=row['allocatedBefore'],allocatedAfter=after,reclaimed=actual['reclaimed'])),flush=True)
    need(all(sha(p)==h for p,h in pins.items()),'All protected current/public/native/game bytes unchanged')
    for row in rows:need(sha(row['path'])==row['sha256'],'All selected original evidence preserved, including skipped files')
    report=dict(passed=True,targets=rows,verifiedFiles=done,inputHashes=pins,
      reclaimedAllocatedBytes=sum(r['reclaimed'] for r in done),deletedFiles=0,newNativeMediaCopies=0,
      actualTerminalAndReparseHardlinkChecks=True,originalPathsBytesSizesTimestampsPreserved=True,
      alreadyCompactZeroGainSampleStopsFurtherWrites=True,fullPortAcceptance=False,scope=__doc__,
      recovery='Native lossless filesystem compression; files remain readable in place. compact /U /EXE reverses it.')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes','targets','verifiedFiles')},indent=2),flush=True)

if __name__=='__main__':main()
