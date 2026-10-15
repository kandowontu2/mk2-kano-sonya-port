"""Exact input-only Shao Knife/retreat and read-only observer delta."""
import json,re
from pathlib import Path
import verify_current_campaign_shao_guarded_highkick_v3461 as base
ROOT=base.ROOT;need=base.need;sha=base.sha
DRIVER='mk2ks_natural_campaign_shao_knife_retreat_v3510.lua'
BASELINE='mk2ks_natural_campaign_shao_lowkick_v3406.lua'
RUNNER='tools/run_current_campaign_shao_knife_retreat_v3511.ps1'
OBSERVER='mk2ks_campaign_shao_knife_observer_v3508.lua'
LOAD="dofile('"+OBSERVER+"')\n"
DECLARED="""    if stage==16 then
     -- Genuine Kano D,B,HP command, with ordinary retreat at close range.
     -- Native code decides activation, projectile collision and boss damage.
     boss_walk_last_x=nil
     if projectile_start and frame-projectile_start<64 then
      local age=frame-projectile_start
      if age>=2 and age<5 then press('Down')end
      if age>=7 and age<10 then press(projectile_direction)end
      if age>=8 and age<12 then press('High Punch')end
      if age>=15 then press('Down');press('Block')end
     elseif height>8 then
      if frame-boss_last_jump<48 then press(boss_jump_direction)end
      if frame%6<3 then press('High Kick')end
     elseif gap<140 then
      projectile_start=nil
      if frame-boss_last_jump>=40 then
       boss_last_jump=frame;boss_jump_direction=back
       decision('shao_knife_retreat_jump_attempt',back)
       press('Up');press(back)
      elseif frame-boss_last_jump<4 then
       press('Up');press(boss_jump_direction)
      else press('Down');press('Block')end
     else
      projectile_start=frame;projectile_direction=back
      decision('shao_knife_command_attempt',back)
     end
"""
SOURCE_ERROR='Only declared stage16 buttons/labels differ; all original ordinary/Kintaro/ID/state/health/win/ending observers exact'
DECLARED_ERROR='Exact genuine physical D,B,HP and retreat schedule; no game or register writes'
def observer_boundary():
    before=(ROOT/'mk2ks_campaign_shao_ring_observer_v3499.lua').read_text()
    expected=before.replace('-- Optional read-only companion to a future frozen cold campaign driver.\n-- This file is NOT loaded by the already running v3485 campaign.',
       '-- Read-only companion to the frozen v3510 Kano cold campaign driver.')
    for a,b in (('Ring','Knife'),('MK2_BOSS_RING','MK2_BOSS_KNIFE'),("=='sonya'","=='kano'"),('==18','==17'),
       ('0xffffb400','0xffffb000'),('0xfffc4800','0xfffc3800'),('0xfffc5c00','0xfffc5800'),('0xfffc7000','0xfffc6000')):
        expected=expected.replace(a,b)
    actual=(ROOT/OBSERVER).read_text()
    need(actual==expected,'Entire read-only observer differs only in declared Kano identity/entry/labels; no controls or guest writes')
    need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|:set_value|:clear_value',actual),
       'Observer cannot supply physical controls or game state')
    return actual
def source_boundary():
    before=(ROOT/BASELINE).read_text();after=(ROOT/DRIVER).read_text()
    observer_boundary()
    need(after.endswith(LOAD) and after.count(LOAD)==1,'Only one declared observer load after all original driver callbacks')
    controls=after[:-len(LOAD)]
    proof=json.loads((ROOT/'audit_v3412_current_kano_natural_lowkick_campaign_checked/report.json').read_text())
    hashes={str(Path(k).resolve()).casefold():v for k,v in proof['inputHashes'].items()}
    need(proof['passed'] and hashes[str((ROOT/BASELINE).resolve()).casefold()]==sha(ROOT/BASELINE),'Accepted complete original input driver bound')
    start='    if stage==16 then\n';stop='    elseif quiet then\n'
    need(before.count(start)==controls.count(start)==before.count(stop)==controls.count(stop)==1,'Unique stage16 input branch')
    a=before.index(start);b=before.index(stop,a);c=controls.index(start);d=controls.index(stop,c)
    restored=(controls[:c]+before[a:b]+controls[d:]).replace('shao_knife_retreat','shao_crouch_lowkick')
    need(restored==before,SOURCE_ERROR);need(controls[c:d]==DECLARED,DECLARED_ERROR)
    need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',after),'No guest writes or state injection')
    return after
def runner_boundary():
    after=(ROOT/RUNNER).read_text()
    observer_path=',"$root/'+OBSERVER+'"'
    need(after.count(observer_path)==1,'Exactly one read-only observer tracked and snapshotted')
    restored=after.replace(observer_path,'').replace(BASELINE,base.DRIVER).replace(DRIVER,
       'mk2ks_natural_campaign_shao_ring_retreat_v3485.lua').replace('shao_knife_retreat','shao_ring_retreat')
    need(restored==(ROOT/'tools/run_current_campaign_shao_ring_retreat_v3486.ps1').read_text(),
       'Entire runner unchanged apart from exact policy/driver/baseline and tracked observer')
    need('-nocheat' in after and '-wavwrite'not in after and 'snapshot_schema=2'in after,'Cold native run, compressed hierarchy, no WAV/build copies')
    return after
