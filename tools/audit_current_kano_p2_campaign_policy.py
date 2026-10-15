"""Bind current scalar driver to historically executed unchanged input policy."""
import gzip,json,re
import verify_native_source_sync as sync
sync.verify()
out=sync.ROOT/'audit_current_kano_p2_campaign_policy'
assert not out.exists()
matrix=json.loads((sync.ROOT/'audit_v5698_current_campaign_four_case_matrix_checked/report.json').read_text())
original=sync.ROOT/'mk2ks_natural_campaign_shao_knife_retreat_v3510.lua'
expected_hash=next(value for name,value in matrix['inputHashes'].items() if name.replace('\\','/').lower()==str(original).replace('\\','/').lower())
assert sync.sha(original)==expected_hash
source=original.read_text()
sink="  local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)\n  local file=assert(io.open(assert(os.getenv('MK2KS_CAMPAIGN_OUT'))..'/guest_maincpu.bin','wb'));file:write(raw);file:close()"
assert source.count(sink)==1 and source.count('screen:snapshot(')==6
source=source.replace(sink,"  log('NO_RAW_DUMP','guest_memory_read_and_file_sink_omitted=true')")
source="local function discard_snapshot(...)end\n"+source.replace('screen:snapshot(','discard_snapshot(')
marker='emu.register_frame(function()\n';assert source.count(marker)==1
source=source.replace(marker,marker+" if frame>=12000 then log('HOST_BOUND','maximum_fields=12000 full_campaign_acceptance=false');manager.machine:exit();return end\n")
source=source.replace("dofile('mk2ks_campaign_shao_knife_observer_v3508.lua')",'-- Kano-only read-only observer omitted; core physical policy unchanged.')
current=sync.ROOT/'audit_bounded_campaign_progress_core_preparation/core.lua'
assert source==current.read_text()
old_events={}
old_log=sync.ROOT/'audit_v5622_current_kano_p2_campaign/run.log.gz'
with gzip.open(old_log,'rt',encoding='utf-8') as stream:
    for line in stream:
        if line.startswith('MK2_NAT_CAMPAIGN_'):
            tag=line.split()[0][17:]
            if tag in ('BOOT','FIGHT','STAGE'):
                row=dict(re.findall(r'(\w+)=([^\s]+)',line));old_events.setdefault(tag,[]).append(row)
                if tag=='STAGE':break
current_events={}
with (sync.ROOT/'audit_bounded_campaign_progress_core_kano_p2_runtime/run.log').open() as stream:
    for line in stream:
        if line.startswith('MK2_NAT_CAMPAIGN_'):
            tag=line.split()[0][17:]
            if tag in ('BOOT','FIGHT','STAGE'):
                row=dict(re.findall(r'(\w+)=([^\s]+)',line));current_events.setdefault(tag,[]).append(row)
                if tag=='STAGE':break
assert old_events['BOOT'][0]['boot']==current_events['BOOT'][0]['boot']=='600'
assert old_events['BOOT'][0]['strategy']==current_events['BOOT'][0]['strategy']=='zoning'
old_schedule=old_events['STAGE'][0]['schedule'];new_schedule=current_events['STAGE'][0]['schedule']
assert old_schedule=='FFFA3780' and new_schedule=='FFFA3180'
out.mkdir();report=dict(originalPhysicalPolicyHashVerified=True,currentPhysicalPolicyUnchanged=True,
    onlyDeclaredMediaSinksBoundAndPassiveCompanionChanged=True,
    historicalOpening=old_events,currentOpening=current_events,naturalLadderChoiceDiffers=True,
    originalControllerSHA256=expected_hash,currentScalarControllerSHA256=sync.sha(current),
    oldRecorderExecuted=False,forcedScheduleUsed=False,currentFullCampaignAccepted=False,fullPortAccepted=False,
    conclusion='Current bounded run does not repeat the old full-clear opponent sequence. Same physical zoning policy and boot timing are preserved; different observed schedule and build require fresh earned campaign proof, not forced ladder/RNG or automatic old-clear transfer.')
(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(dict(policyUnchanged=True,oldSchedule=old_schedule,currentSchedule=new_schedule)))
