"""Exact input-only Shao Ring/retreat delta; no native-game changes."""
import json,re
from pathlib import Path
import verify_current_campaign_shao_guarded_highkick_v3461 as base
ROOT=base.ROOT;need=base.need;sha=base.sha
DRIVER='mk2ks_natural_campaign_shao_ring_retreat_v3485.lua'
BASELINE=base.DRIVER
RUNNER='tools/run_current_campaign_shao_ring_retreat_v3486.ps1'
DECLARED="""    if stage==16 then
     -- Genuine Sonya D,F,LP command, with ordinary retreat at close range.
     -- Native code decides activation, projectile collision and boss damage.
     boss_walk_last_x=nil
     if projectile_start and frame-projectile_start<64 then
      local age=frame-projectile_start
      if age>=2 and age<5 then press('Down')end
      if age>=7 and age<10 then press(projectile_direction)end
      if age>=8 and age<12 then press('Low Punch')end
      if age>=15 then press('Down');press('Block')end
     elseif height>8 then
      if frame-boss_last_jump<48 then press(boss_jump_direction)end
      if frame%6<3 then press('High Kick')end
     elseif gap<140 then
      projectile_start=nil
      if frame-boss_last_jump>=40 then
       boss_last_jump=frame;boss_jump_direction=back
       decision('shao_ring_retreat_jump_attempt',back)
       press('Up');press(back)
      elseif frame-boss_last_jump<4 then
       press('Up');press(boss_jump_direction)
      else press('Down');press('Block')end
     else
      projectile_start=frame;projectile_direction=forward
      decision('shao_ring_command_attempt',forward)
     end
"""
SOURCE_ERROR='Only declared stage16 buttons/labels differ; all original ordinary/Kintaro/ID/state/health/win/ending observers exact'
DECLARED_ERROR='Exact genuine physical D,F,LP and retreat schedule; no game or register writes'
def source_boundary():
    before=(ROOT/BASELINE).read_text();after=(ROOT/DRIVER).read_text()
    proof=json.loads((ROOT/'audit_v3474_current_sonya_guarded_highkick_campaign_checked/report.json').read_text())
    hashes={str(Path(k).resolve()).casefold():v for k,v in proof['inputHashes'].items()}
    need(proof['passed'] and hashes[str((ROOT/BASELINE).resolve()).casefold()]==sha(ROOT/BASELINE),'Accepted complete original input driver bound')
    start='    if stage==16 then\n';stop='    elseif quiet then\n'
    need(before.count(start)==after.count(start)==before.count(stop)==after.count(stop)==1,'Unique stage16 input branch')
    a=before.index(start);b=before.index(stop,a);c=after.index(start);d=after.index(stop,c)
    restored=(after[:c]+before[a:b]+after[d:]).replace('shao_ring_retreat','shao_guarded_highkick')
    need(restored==before,SOURCE_ERROR);need(after[c:d]==DECLARED,DECLARED_ERROR)
    need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',after),'No guest writes or state injection')
    return after
def runner_boundary():
    after=(ROOT/RUNNER).read_text()
    restored=after.replace(BASELINE,base.BASELINE).replace(DRIVER,BASELINE).replace('shao_ring_retreat','shao_guarded_highkick')
    need(restored==(ROOT/base.RUNNER).read_text(),'Entire runner unchanged apart from exact policy/driver/baseline paths')
    need('-nocheat' in after and '-wavwrite'not in after and 'snapshot_schema=2'in after,'Cold native run, compressed hierarchy, no WAV/build copies')
    return after
