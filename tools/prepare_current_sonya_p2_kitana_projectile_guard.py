"""UNEXECUTED Kitana9-only observed-launch guard then genuinely ready ring."""
import json,re
import verify_native_source_sync as sync
sync.verify();root=sync.ROOT
base=root/'audit_current_sonya_p2_kitana_ring_spacing_preparation'
out=root/'audit_current_sonya_p2_kitana_projectile_guard_preparation';assert not out.exists()
original=(base/'campaign.lua').read_text()
start=original.index("   elseif fighter=='sonya' and side==2 and other.roster==4 and stage==9 then")
end=original.index("   elseif fighter=='sonya' and side==2 and other.roster==11 and stage==8 then",start+1)
old=original[start:end];new=old
before="if not krs_last or frame-krs_last~=1 then krs_ring=nil;krs_dir=nil;krs_jump=-1000;krs_jumpdir=nil end"
assert new.count(before)==1
new=new.replace(before,before.replace(' end',';kgs_until=-1000;kgs_retry=-1000 end'))
before="    if krs_ring and frame-krs_ring<64 and(frame-krs_ring<12 or gap>=150)then"
assert new.count(before)==1
new=new.replace(before,"""    if other.action==8 then kgs_until=frame+40 end
    if frame<kgs_until then
     krs_ring=nil;press('Down');press('Block')
    elseif krs_ring and frame-krs_ring<64 and(frame-krs_ring<12 or gap>=150)then""")
before="    else\n     krs_ring=frame;krs_dir=forward"
assert new.count(before)==1
new=new.replace(before,"""    elseif human.y==human.floor and(human.action==0 or human.action==771 or human.action==770 or human.action==772 or human.action==1792 or human.action==1793)
     and(other.action==0 or other.action==771 or other.action==770 or other.action==772)and other.flags&0x18==0 and frame-kgs_retry>=64 then
     krs_ring=frame;krs_dir=forward;kgs_retry=frame""")
last="    end\n";assert new.endswith(last)
new=new[:-len(last)]+"    else press('Down');press('Block')end\n"
globals='local kgs_until,kgs_retry=-1000,-1000\n'
source=globals+original[:start]+new+original[end:]
def conservation(candidate):
    assert candidate.startswith(globals) and candidate.count(new)==1
    assert candidate[len(globals):].replace(new,old,1)==original
    assert 'if other.action==8 then kgs_until=frame+40 end' in new
    assert "krs_ring=nil;press('Down');press('Block')" in new and 'frame-kgs_retry>=64' in new
    assert ':write_' not in candidate and ':snapshot(' not in candidate
conservation(source);faults=[]
for label,bad in [('lost actual CPU8 guard',source.replace('if other.action==8 then','if other.action==9 then',1)),('changed earlier Jax ground jump40',source.replace('jgl_until=frame+40','jgl_until=frame+41',1)),('lost native human-ready gate',source.replace('human.y==human.floor and(human.action==0','human.y==human.floor and(human.action==4',1))]:
    try:conservation(bad)
    except AssertionError:faults.append(label)
    else:raise AssertionError('Source fault admitted')
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_kitana_ring_spacing_runtime','audit_current_sonya_p2_kitana_projectile_guard_runtime')
(out/'run.ps1').write_text(runner)
checked=root/'audit_current_sonya_p2_kitana_ring_spacing_checked/report.json';r=json.loads(checked.read_text())
setter=[x for x in r['actualCPUActionSetterRecords'] if x['frame'] in ('104518','104544','104571')]
hit=next(x for x in r['actualHPWriterContext'] if x['frame']=='104545' and x['victim_slot']=='2')
assert hit['writer230']==hit['cpu_actor'] and int(hit['before'])-int(hit['after'])==32
report=dict(prepared=True,emulatorLaunched=False,runtimeAcceptance=False,fullPortAcceptance=False,proposedConservedPrefix=104518,
            solePhysicalChange='Kitana9 only: observed CPUaction8 extends40field physical crouchguard and cancels pending ring chord; afterward require actual human grounded-ready and CPUidle/recovered before ring,64fieldretry. Other stage controls and passive observers retained.',
            actualFirstCPUSetterRecoverySequence=setter,actualFirstCPUCreated32HPHit=hit,
            unsupportedClaim='The40field guard is a physical policy inferred from the first26fieldlaunch+27fieldrecovery/current contact; it is not proof every projectile has passed, no chip, allmovesclassified, or automatic historical winning-strategy transfer.',
            effectiveSourceFaultsRejected=faults,luaSHA256=sync.sha(lua),evidenceSHA256=sync.sha(checked),
            limits=dict(wallSeconds=180,memoryMiB=320,textMiB=10,media=False,guestWrites=False))
(out/'preparation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(prepared=True,emulatorLaunched=False,luaSHA256=sync.sha(lua),faults=len(faults))))
