"""Qualify actual3680 P2 progression with the whole original campaign verifier.

Only compiled-build provenance and the declared six PNG sinks are adapted.
All actual native schedule/ID/morph/health/KO/paid-continue/ending checks and
independent boss physical-input replay remain. A loss or time limit cannot
prove a campaign clear. Raster digests do not prove ending-art fidelity.
"""
import argparse,hashlib,json,re,sys,traceback
from pathlib import Path
import run_guarded_p2_campaign_ram_v3744 as capture
import verify_current_campaign_shao_knife_observer_v3526 as knife
import verify_current_campaign_shao_ring_retreat_v3491 as ring

ROOT,need,sha,NAME=capture.ROOT,capture.need,capture.sha,capture.NAME
OUT=ROOT/'audit_v3759_guarded_sonya_p2_bounded_campaign_checked'

def matched(folder,pins):
    meta=json.loads((folder/'result.json').read_text())
    build=json.loads((ROOT/NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    before=json.loads((folder/'input_hashes_before.json').read_text())
    frozen=json.loads((folder/'source_snapshot_paths.json').read_text())
    need(meta['candidate']==NAME and meta['exit_code']==0 and meta['human_slot']==2 and meta['cpu_slot']==1 and
      meta['assistance']=='none'and not meta['cheats_enabled']and meta['snapshot_schema']==2 and
      meta['raw_audio_files_written']==meta['new_builds_or_rom_copies']==meta['rawRasterFilesWritten']==0 and
      before==meta['input_hashes'],'Terminal actual P2 input-only3680 capture, no audio/raster/build copies')
    need(meta['executable_sha256']==build['executable_sha256']=='BF5D90F90E6A254C4BCB63B4C0D3974C08DF9F28A817BD35A6F86FE68ABE6A41'and
      meta['payload_sha256']==build['payload_sha256']=='ED9023949F73BD719F8BC688C69230C68239D7CC140F814C1A4E54A5BF561BC3'and
      all(before.get(str(Path(p).resolve()))==h for p,h in build['input_hashes'].items()),'Exact executable/payload/all compiled inputs')
    for p,h in before.items():
        need(sha(p)==h,'Executed input unchanged');pins[p]=h
        if Path(p).suffix in('.lua','.py','.ps1','.json'):
            dest=Path(frozen[p]).resolve()
            need(dest.is_relative_to(folder.resolve())and sha(dest)==h,'Exact frozen hierarchy source');pins[str(dest)]=h
        if Path(p).suffix=='.lua':
            need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',Path(p).read_text()),'No guest-state/AI/health/CPU assistance')
    wrapper=(ROOT/capture.LUA).read_text()
    need(wrapper.count("source:gsub('screen:snapshot%(', '_campaign_emit(')")==1 and
      "assert(count==6"in wrapper and "assert(load(prefix..adapted"in wrapper and
      not re.search(r':set_value|:clear_value|:write_|\.value\s*=(?!=)',wrapper),'Wrapper changes only six PNG sinks; no controls/game writes')
    driver=(knife if meta['player']=='kano'else ring).source_boundary()
    need(driver.count('screen:snapshot(')==6,'All six original PNG sinks accounted for')
    need(not list(folder.rglob('*.png'))and not list(folder.rglob('*.wav')),'No new raster/PCM files')

def change(text,tag,frame,key,new):
    pattern=rf'^(MK2_NAT_CAMPAIGN_{tag} frame={frame} [^\r\n]*?\b{key}=)([^\s]+)'
    result,count=re.subn(pattern,lambda m:m[1]+str(new),text,count=1,flags=re.M)
    need(count==1 and result!=text,'Non-vacuous actual-row corruption')
    return result

def verify(fighter):
    policy=knife if fighter=='kano'else ring
    folder=ROOT/f'audit_v3745_guarded_{fighter}_natural_p2_campaign'
    need(folder.is_dir()and(folder/'result.json').is_file(),'Existing terminal actual capture required')
    expected=knife.current.expected_current()
    native=policy.make_verifier(expected)
    # Preserve the generated whole3515/3491 algorithm and its declared
    # stage16 input replay; replace only its matched-build provenance handler.
    native.__globals__.update(NAME=NAME,matched=matched)
    positive=native(folder)
    need(positive['passed'],'Whole original actual P2 campaign gate: '+repr(positive['errors']))
    text=(folder/'run.log').read_text();rows=knife.old.parse(text,2,fighter)
    trials=[]
    def reject(label,damaged,error):
        result=native(folder,text_override=damaged)
        need(not result['passed']and any(error in message for message in result['errors']),
          'Specific same-path actual fault rejection '+label)
        restored=native(folder)
        need(restored==positive,'Exact positive restored after every actual fault')
        trials.append(label)
    first=lambda tag:next(r for r in rows if r['tag']==tag)
    r=first('LIVE');reject('proxy_Liu_live_ID',change(text,'LIVE',r['frame'],'human','0:0'),'True live human ID')
    r=first('SELECT_ID');reject('wrong_confirmed_roster',change(text,'SELECT_ID',r['frame'],'roster',0),'selection check retains own true ID')
    r=next(r for r in rows if r['tag']=='HEALTH'and r['pc']==0xff836700 and r['after']<r['before'])
    reject('unoriginal_health_writer',change(text,'HEALTH',r['frame'],'pc','FFF00000'),'exact original writer')
    reject('negative_collision_health',change(text,'HEALTH',r['frame'],'after',-1),'collision never heals')
    r=first('WIN');reject('wrong_winner_table_PC',change(text,'WIN',r['frame'],'pc','FFF00000'),'winner-table call')
    reject('fabricated_win_zero_health',change(text,'WIN',r['frame'],'health','0,0'),'Native winning health')
    r=first('ROM');reject('changed_native_schedule',change(text,'ROM',r['frame'],'ids',r['ids'].replace('18','0',1)),'Original-derived true-ID schedule')
    r=first('SPECIAL');reject('wrong_move_actor_register',change(text,'SPECIAL',r['frame'],'a8','01000000'),'special instruction fetch')
    reject('wrong_native_move_entry_PC',change(text,'SPECIAL',r['frame'],'pc','FFF00000'),'special instruction fetch')
    fields={r['frame']for r in rows if r['tag']=='BOSS_FIELD'}
    attack=next((r for r in rows if r['tag']=='INPUT'and r['frame']in fields and r['button']in('High_Punch','Low_Punch')),None)
    if attack:
        original=next(line for line in text.splitlines()if line.startswith(f"MK2_NAT_CAMPAIGN_INPUT frame={attack['frame']} ")and f"button={attack['button']} "in line)
        reject('missing_actual_boss_attack_input',text.replace(original+'\n','',1),'independently replayed native state')
    if any(r['tag']=='ENDING_COMPLETED'for r in rows):
        r=first('ENDING_COMPLETED')
        reject('missing_own_ending_picture_page',change(text,'ENDING_COMPLETED',r['frame'],'pictures','0,0'),'Both own native picture/story pages')
        reject('wrong_ending_return_roster',change(text,'ENDING_COMPLETED',r['frame'],'roster',f'0,{17 if fighter=="kano"else 18}'),'return to attract roster')
    pins=positive['inputHashes']
    for file in folder.rglob('*'):
        if file.is_file():pins[str(file)]=sha(file)
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).suffix=='.py'and Path(file).resolve().is_relative_to(ROOT/'tools'):pins[str(Path(file).resolve())]=sha(file)
    need(all(sha(p)==h for p,h in pins.items()),'All source/proof bytes unchanged')
    positive.update(actual3680P2WholeCampaignAlgorithmRetained=True,actualRowCounterexamplesRejected=trials,
      endingPixelsAccepted=False,completeCampaignAudioAccepted=False,fullPortAcceptance=False)
    return positive

def run(fighters):
    cases=[verify(fighter)for fighter in fighters]
    return dict(passed=True,cases=cases,currentBothP2NaturalClearAccepted=set(fighters)=={'kano','sonya'}and all(c['unassisted_clear_proven']for c in cases),
      endingPixelsAccepted=False,completeCampaignAudioAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),action='append')
    args=parser.parse_args()
    try:report=run(args.fighter or('kano','sonya'))
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable report');OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    summary={k:v for k,v in report.items()if k!='cases'}
    summary['cases']=[{k:v for k,v in c.items()if k not in('inputHashes','uppercutAssignmentFrames')}for c in report.get('cases',[])]
    print(json.dumps(summary,indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
