"""Six fresh native crouching-turn roll diagnostics, not contact-fidelity approval.

Correlates actual comparator registers with independent owning pose/cache records,
unchanged stock ROM turn art, native hit/miss/rebound and ordinary controls.
Never reclassifies a contact as an accepted duck miss or supplies guest state.
"""
from __future__ import annotations
import json
import re
import struct
from pathlib import Path

import verify_native_candidate_v545 as build
import verify_human_special_negative_v6 as native
from verify_ko_round_floor_shadows import need,digest,rgb

ROOT=build.ROOT
HEX={'pc','actor','main','owner','cache','pose','action','facing','flags','body','palette',
     'source','command','victim','victim_main','victim_min','victim_max','attack_min','attack_max'}

def rows(log,tag):
    out=[]
    for line in log.splitlines():
        if not line.startswith('MK2_BALL_V2_'+tag+' '):continue
        pairs=re.findall(r'(\w+)=([^\s]+)',line)
        need(len({k for k,v in pairs})==len(pairs),'Unambiguous pose/cache observer fields')
        out.append({k:v if k in ('role','phase','file')else int(v,16 if k in HEX else 10)for k,v in pairs})
    return out

def xy(word):return native.rect(word)

def overlap(g):
    ax,ay=xy(g['attack_min']);bx,by=xy(g['attack_max'])
    vx,vy=xy(g['victim_min']);wx,wy=xy(g['victim_max'])
    return dict(horizontal=min(bx,wx)-max(ax,vx),vertical=min(by,wy)-max(ay,vy))

def components(program,pose,base,facing):
    at=(pose-base)//8;result=[]
    for index in range(8):
        ptr=struct.unpack_from('<I',program,at+index*4)[0]
        if ptr==0:return result
        need(base<=ptr<=0xffffffff and ptr&15==0,'Typed own ROM composite component')
        w,h,dx,dy,source,command=struct.unpack_from('<HHhhIH',program,(ptr-base)//8)
        if facing&0x10:dx=w-dx
        if facing&0x20:dy=h-dy
        result.append(dict(part=index,width=w,height=h,dx=dx,dy=dy,source=source,command=(command&~0x30)|(facing&0x30)))
    raise ValueError('Unterminated native composite')

def inspect_log(log,prior,side,victim,original,payload):
    need([l for l in log.splitlines()if l.startswith('MK2_HSPECIAL_')]==
         [l for l in prior.splitlines()if l.startswith('MK2_HSPECIAL_')],
         'All original real inputs, paired callbacks, geometry, health and recovery unchanged by observer')
    contact=not(victim=='raiden'and side==2)
    proof=native.verify_log(log,'ball',side,'miss',victim,duck_contact=contact)
    native.verify_repel(log,side)
    if contact:proof.update(native.verify_rebound(log,side,False))
    geometry,actors,parts,snaps=(rows(log,t)for t in ('GEOMETRY','ACTOR','PART','SNAPSHOT'))
    base=native.rows(log,'GEOMETRY')
    need(len(geometry)==len(base)and [g['frame']for g in geometry]==[g['frame']for g in base],
         'Every real comparison has one independent geometry/pose/cache observation')
    need(len(actors)==len(geometry)*2 and len({(a['frame'],a['role'])for a in actors})==len(actors),
         'Both actual display owners are recorded at every comparison')
    need(len(snaps)==len(geometry)and [s['comparison']for s in snaps]==[g['frame']for g in geometry]and
         all(s['frame']==s['comparison']+1 and s['phase']=='done'and s['writes']==0 and s['file']==f"ball_comparison_{s['comparison']:04d}.png"for s in snaps),
         'Actual next-frame-done raster association, not an instruction-time screenshot claim')
    fields={(f['frame'],f['slot']):f for f in native.rows(log,'FIELD')}
    actor_map={(a['frame'],a['role']):a for a in actors}
    ident=native.VICTIMS[victim]
    root=struct.unpack_from('<I',original,0x20c2a+ident*4)[0]
    turn_script=struct.unpack_from('<I',original,(root+10*32-0xff800000)//8)[0]
    turn_groups=struct.unpack_from('<2I',original,(turn_script-0xff800000)//8)
    raised=[]
    for g,b in zip(geometry,base):
        need(g['side']==side and g['pc']==0xff835b80 and g['bounds']==1 and g['writes']==0 and
             all(g[k]==b[k]for k in ('actor','main','victim_main','victim_min','victim_max','attack_min','attack_max'))and g['victim']==b['victim_actor'],
             'Independent actual CMPXY register and owner crosscheck')
        for role,n in (('own',side),('victim',3-side)):
            a=actor_map[g['frame'],role];field=fields[g['frame'],n]
            need(a['side']==side and a['writes']==0 and a['id']==(17 if role=='own'else ident)and
                 a['owner']==a['actor']and all(a[k]==field[k]for k in ('actor','main','y','floor','action'))and
                 a['cache']==(0x0105ed30 if n==1 else 0x0105f230)and a['flags']==field['flags']and a['body']==field['body'],
                 'True actor/Main/cache/flags/body labels agree with actual owning callbacks')
            # Callback occurs before the native ten-pixel roll integration.
            # Compare the actual instruction-time X to the independent native
            # GEOMETRY observer AND that exact integration, not a stale field.
            need(a['x']==b['x']==field['x']+(10 if side==1 else -10)if role=='own'else a['x']==field['x'],
                 'Actual comparison X agrees with independent geometry and native integration')
            observed=[p for p in parts if p['frame']==g['frame']and p['role']==role]
            descriptors=components(payload if role=='own'else original,a['pose'],0xfe800000 if role=='own'else 0xff800000,a['facing'])
            need(len(observed)==len(descriptors)and all(p['side']==side and p['writes']==0 and all(p[k]==v for k,v in descriptor.items())for p,descriptor in zip(observed,descriptors)),
                 'Every true cached sprite component equals its actual ROM pose descriptor')
            need(a['facing']&0x20==0,'No unintended actor/cache Y flip')
        v=actor_map[g['frame'],'victim']
        need(v['action']==0x302 and v['y']==v['floor'],'Actual grounded native crouch during every comparison')
        if v['pose']in turn_groups:raised.append(dict(frame=g['frame'],pose=f"{v['pose']:08X}",**overlap(g)))
    need(bool(raised),'Real original stock crouching-turn dispatch, not inferred only from held Down')
    result=native.rows(log,'RESULT')[0]
    health=[h for h in native.rows(log,'HEALTH')if result['entry']<=h['frame']<=result['recovered']]
    if contact:
        last=geometry[-1];v=actor_map[last['frame'],'victim']
        need(v['pose']==turn_groups[0]and len(health)==1 and health[0]['frame']==last['frame'],
             'Actual first original crouching-turn pose coincides with the native health store')
        need(overlap(last)==dict(horizontal=(9 if victim=='raiden'else 12)if side==1 else 2,vertical=6 if victim=='raiden'else 1),
             'Exact retained native contact overlap, not an adjusted plane or categorical immunity')
    else:
        need(not health and len(geometry)==20 and all(g['horizontal']<=0 or g['vertical']<=0 for g in raised),
             'Mirrored Raiden turn has a real separating axis, not a skipped collision callback')
    proof.update(comparisons=len(geometry),snapshots=len(snaps),firstRaised=raised[0],lastComparison=overlap(geometry[-1]),
                 lastVictimPose=f"{actor_map[geometry[-1]['frame'],'victim']['pose']:08X}",
                 contactFidelityAccepted=False,planeCorrectionClaim=False,
                 scope='Exact native crouching-turn contact/miss, actual ROM/cache poses, complete rebound/controls; not port/donor contact-fidelity approval')
    return proof

def inspect():
    inputs={};cases=[]
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    payload=(ROOT/build.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
    need(digest(ROOT/'mk2/mk2-maincpu.bin')=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23','Exact original stock animation/comparator program')
    need(struct.unpack_from('<6H',original,(0xff835b70-0xff800000)//8)==(0xe4a2,0xc92e,0xcd2d,0xe483,0xc42b,0xc22a),'Original shared-edge rejecting CMPXY branch sequence')
    inputs[str(ROOT/'mk2/mk2-maincpu.bin')]=digest(ROOT/'mk2/mk2-maincpu.bin')
    for victim in ('kitana','mileena','raiden'):
        for side in (1,2):
            folder=ROOT/f'audit_v574_roll_pose_p{side}_{victim}'
            prior=ROOT/f'audit_v547_cannonball_duck_p{side}_{victim}'
            build.matched(folder,inputs);build.matched(prior,inputs)
            observer=folder/'input_sources/mk2ks_cannonball_geometry_probe_v2.lua'
            need(not re.search(r':write_|\.value\s*=(?!=)|load_?state',observer.read_text()),'Read-only pose/cache observer')
            proof=inspect_log((folder/'run.log').read_text(encoding='utf-8-sig'),(prior/'run.log').read_text(encoding='utf-8-sig'),side,victim,original,payload)
            for s in rows((folder/'run.log').read_text(encoding='utf-8-sig'),'SNAPSHOT'):
                image=folder/'snap'/s['file'];need(rgb(image).shape==(254,400,3),'Actual native-size next-frame raster')
            proof.update(capture=folder.name,victim=victim);cases.append(proof)
            for path in folder.rglob('*'):
                if path.is_file():inputs[str(path)]=digest(path)
    return dict(diagnosticVerified=True,contactFidelityAccepted=False,planeCorrectionClaim=False,fullPortAcceptance=False,cases=cases,
                observedNativeContacts=5,observedNativeMisses=1,pairedCallbackRecords=sum(c['fields']for c in cases),
                scope='Six fresh unassisted v545 current-build roll crossover diagnostics, unchanged real inputs versus v547. True cached/ROM stock crouching-turn poses explain five native24 hits; opposite Raiden misses through separation. No roll fix or universal duck-miss/contact-fidelity claim.',inputHashes=inputs)

if __name__=='__main__':print(json.dumps(inspect(),indent=2))
