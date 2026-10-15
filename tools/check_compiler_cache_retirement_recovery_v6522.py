"""Read-only recovery receipt after actual cache deletion/post-delete report failure.

Do not rerun deletion, modify the executed cleanup source or recreate a cache
to manufacture a byte count. Actual historical reclaimed bytes are unknown.
"""
import json,subprocess
from pathlib import Path
import native_projectile_identifiers_context_v6509 as candidate
ROOT,need,sha=candidate.ROOT,candidate.need,candidate.sha
OUT=ROOT/'audit_v6523_compiler_cache_retirement_recovery_checked'

def main():
 need(not OUT.exists(),'Fresh recovery receipt; no previous evidence overwrite')
 cache=ROOT/'mame-mkp/build/mingw-gcc';failed=ROOT/'audit_v6517_generated_compiler_cache_retired'
 source=ROOT/'tools/retire_generated_compiler_cache_v6516.ps1'
 need(not cache.exists() and failed.is_dir() and not list(failed.iterdir()),
      'Actual exact cache absent and original reporting directory empty')
 t=source.read_text();need(t.index('Remove-Item -LiteralPath $mk2Cache -Recurse -Force')<t.index('Measure-Object logicalBytes -Sum') and
      '$mk2Rows+= [ordered]@{' in t,'Preserved executed deletion before failing OrderedDictionary property aggregation')
 candidate.expected();meta=json.loads((ROOT/candidate.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
 restore=json.loads((ROOT/candidate.NAME/'restoration.json').read_text(encoding='utf-8-sig'))
 pins=dict(meta['input_hashes']);pins.update(restore['restored_actual_preexisting_files'])
 for p in (source,Path(__file__),Path(candidate.__file__),ROOT/candidate.NAME/'mkport_candidate.exe',
           ROOT/candidate.NAME/'roms/mk2ks/mk2ks.mdata',ROOT/candidate.NAME/'build-info.json',ROOT/candidate.NAME/'restoration.json',
           ROOT/'PLAY_MK2_KANO_SONYA.cmd',ROOT/'PLAY_CURRENT_V5219_CHECKED.cmd',ROOT/'tools/check_current_playtest_v5975.ps1',
           ROOT/candidate.old.NAME/'mkport_candidate.exe',ROOT/candidate.old.NAME/'build-info.json',
           ROOT/candidate.old.NAME/'roms/mk2ks/mk2ks.mdata'):
  pins[str(p.resolve())]=sha(p)
 need(sha(ROOT/candidate.old.NAME/'mkport_candidate.exe')==candidate.old.EXE_SHA and
      all(sha(p)==h for p,h in pins.items()),'Actual retained candidate, prior playable, compiled inputs and dirty restoration intact')
 report=dict(passed=True,scope=__doc__,exactAbsentTarget=str(cache.resolve()),
             deletionRepeated=False,additionalFilesRemoved=0,cacheRecreated=False,
             originalCleanupScript=str(source),originalReportProduced=False,
             preservedReportingFailure=dict(provenance='Prior terminal tool output; original process has exited, aggregation rows were not persisted.',
              scriptExitCode=1,message='Measure-Object : The property "logicalBytes" cannot be found in the input for any objects.',
              phase='After exact cache removal and retained hash verification, before JSON report creation'),
             reclaimedLogicalBytes=None,reclaimedAllocatedBytes=None,
             noHistoricalByteCountInvented=True,retainedCompiledInputsAndDirtyFilesVerified=True,
             recovery='Regenerate reproducible objects/archives with tools/build_native_projectile_identifiers_v6507.ps1. User sources and playable artifacts were not targeted.',
             inputHashes=pins,publicPlayableChanged=False,fullPortAcceptance=False)
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,
      'Hash-preserving exact recovery receipt compression')
 print(json.dumps(dict(passed=True,cacheAbsent=True,retainedInputsIntact=True,reclaimedBytes=None,additionalFilesRemoved=0)),flush=True)

if __name__=='__main__':main()
