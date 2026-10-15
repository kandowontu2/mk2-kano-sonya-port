"""Paired native crossover counterexample, not a collision-fidelity pass."""
import json
import re
from pathlib import Path
import verify_native_candidate_v517 as build
import verify_human_special_negative_v4 as port
import verify_original_ball_v1 as donor
from verify_ko_round_floor_shadows import need,digest,rgb

ROOT=build.ROOT

def details(log):
    output=[]
    hexkeys={'actor','main','pose','victim','victim_main','victim_pose','victim_min','victim_max','attack_min','attack_max','pc'}
    for line in log.splitlines():
        if not line.startswith('MK2_BALL_DETAIL '):continue
        row=dict(re.findall(r'(\w+)=([^\s]+)',line))
        # The v1 observer's list/victim_list labels actually read opponent
        # Main pointers. They are deliberately excluded, not interpreted as
        # animation-list provenance or used to justify a geometry change.
        for k in list(row):
            if k in {'list','victim_list','victim_flags','victim_body'}:del row[k]
            else:row[k]=int(row[k],16 if k in hexkeys else 10)
        output.append(row)
    return output

def rectangle(value):return value&65535,value>>16

def overlap(row):
    ax,ay=rectangle(row['attack_min']);bx,by=rectangle(row['attack_max'])
    vx,vy=rectangle(row['victim_min']);wx,wy=rectangle(row['victim_max'])
    return dict(horizontal=min(bx,wx)-max(ax,vx),vertical=min(by,wy)-max(ay,vy))

def inspect():
    inputs={};cases=[]
    for side in (1,2):
        folder=ROOT/f'audit_v540_cannonball_pose_p{side}_liu'
        base=ROOT/f'audit_v518_cannonball_duck_p{side}_liu_kang'
        build.matched(folder,inputs);build.matched(base,inputs)
        log=(folder/'run.log').read_text(encoding='utf-8-sig')
        before=(base/'run.log').read_text(encoding='utf-8-sig')
        need([l for l in log.splitlines() if l.startswith('MK2_HSPECIAL_')]==
             [l for l in before.splitlines() if l.startswith('MK2_HSPECIAL_')],
             'Every original real input, paired field, action, rectangle and health event unchanged by detail observer')
        metadata=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        for name in ('mk2ks_cannonball_geometry_probe_v1.lua','mk2ks_human_special_negative_v9.lua'):
            source=folder/'input_sources'/name
            need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',source.read_text()),'Read-only geometry observer')
            inputs[str(source)]=digest(source)
        geo=port.rows(log,'GEOMETRY');own=details(log)
        need(len(own)==len(geo) and [r['frame'] for r in own]==[r['frame'] for r in geo], 'Every actual comparison has one detail record')
        snaps=[dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in log.splitlines() if line.startswith('MK2_BALL_DETAIL_SNAPSHOT ')]
        need([int(r['comparison']) for r in snaps]==[r['frame'] for r in own] and
             all(int(r['callback'])==int(r['comparison'])+1 and r['writes']=='0' for r in snaps), 'Actual next-callback screenshot association')
        for g,r in zip(geo,own):
            need(r['side']==side and r['writes']==0 and r['pc']==0xff835b80 and
                 all(r[k]==g[k] for k in ('actor','main','victim_min','victim_max','attack_min','attack_max','x','y','floor')) and
                 r['victim']==g['victim_actor'] and r['victim_main']==g['victim_main'] and
                 r['victim_y']==r['victim_floor'], 'Actual owned collision instruction and grounded ducking victim')
        for s in snaps:
            path=folder/'snap'/s['file'];need(rgb(path).shape==(254,400,3),'Actual native-size callback image');inputs[str(path)]=digest(path)
        result=port.rows(log,'RESULT')[0]
        hit=[r for r in port.rows(log,'HEALTH') if result['entry']<=r['frame']<=result['recovered']]
        if side==1:
            try:port.verify_log(log,'ball',side,'miss','liu_kang')
            except ValueError as error:need(str(error)=='Own special contact damage (excludes initial ordinary charged kick)','Only retained contact counterexample, no hidden failed phase')
            else:raise ValueError('Counterexample must not be silently counted as a passing miss')
            need(len(hit)==1 and hit[0]['before']-hit[0]['after']==24 and hit[0]['pc']==0xff836700 and hit[0]['frame']==geo[-1]['frame'],'Actual native 24-damage contact agrees with last comparison')
        else:
            port.verify_log(log,'ball',side,'miss','liu_kang');need(not hit,'Actual mirrored miss')
        turn=next(r for r in own if r['victim_pose']!=own[0]['victim_pose'])
        need(turn['victim_pose']==0xff9236d0 and own[0]['victim_pose']==0xff923580,'Actual native crouching turn pose change')
        cross=overlap(turn)
        need(cross==({'horizontal':9,'vertical':1} if side==1 else {'horizontal':-1,'vertical':1}),'Exact observed crossover distinction, not a fitted hitbox change')
        cases.append(dict(side=side,comparisons=len(geo),nativeDamage=24 if side==1 else 0,turnFrame=turn['frame'],turnPose='FF9236D0',crossover=cross,
                          observerAnimationListClaim=False,snapshots=len(snaps)))
        for p in folder.rglob('*'):
            if p.is_file():inputs[str(p)]=digest(p)
    ref=ROOT/'audit_v505_original_ball_liu_kang_duck'
    metadata=json.loads((ref/'result.json').read_text(encoding='utf-8-sig'))
    need(metadata['exit_code']==0 and metadata['game']=='mk3' and metadata['cheats'] is False and metadata['assistance']=='none','Actual original unassisted reference')
    need(metadata['input_hashes']==json.loads((ref/'input_hashes_before.json').read_text(encoding='utf-8-sig')),'Original launch manifests agree')
    for filename,sha in metadata['input_hashes'].items():need(digest(filename)==sha,'Original reference input unchanged');inputs[filename]=sha
    log=(ref/'run.log').read_text(encoding='utf-8-sig');original=donor.verify_log(log,'liu_kang','duck')
    g=donor.rows(log,'GEOMETRY');turn=next(r for r in g if rectangle(r['victim_min'])[1]!=rectangle(g[0]['victim_min'])[1])
    original.update(firstRaisedBoundsFrame=turn['frame'],crossover=overlap(turn))
    for p in (ref/'run.log',ref/'result.json',ref/'input_hashes_before.json'):inputs[str(p)]=digest(p)
    return dict(diagnosticVerified=True,collisionFixed=False,fullPortAcceptance=False,cases=cases,originalReference=original,
                scope='Exact current paired real-input crossover and native-size next-callback images; v1 mislabeled list fields excluded. Original P1 donor reference misses after horizontal separation. Does not prove all duck phases, donor mirrored cases, all roster geometry or a corrected attack plane.',inputHashes=inputs)

if __name__=='__main__':print(json.dumps(inspect(),indent=2))
