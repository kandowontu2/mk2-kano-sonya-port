"""Full unchanged actual frames for current close defense/UI/ground/blood review."""
import json,math
from PIL import Image,ImageDraw
import verify_ring_native_lookup_v1342 as current
ROOT=current.ROOT;OUT=ROOT/'audit_v1390_current_regression_contacts'
assert not OUT.exists();OUT.mkdir();cases={}
def sheet_case(key,entries,proofs):
    checked=[];sheets=[]
    for page in range(math.ceil(len(entries)/20)):
        section=entries[page*20:(page+1)*20]
        sheet=Image.new('RGB',(1600,math.ceil(len(section)/4)*282),(24,24,24));draw=ImageDraw.Draw(sheet)
        for n,(path,label)in enumerate(section):
            picture=Image.open(path).convert('RGB');assert picture.size==(400,254)
            x,y=n%4*400,n//4*282;sheet.paste(picture,(x,y+28));draw.text((x+4,y+5),label,fill='white')
            checked.append(dict(file=str(path),label=label,sha256=current.digest(path)))
        path=OUT/f'{key}_{page+1}.png';sheet.save(path);sheets.append(dict(file=str(path),sha256=current.digest(path)))
    cases[key]=dict(proofs=[dict(file=str(p),sha256=current.digest(p))for p in proofs],entries=checked,sheets=sheets)
for side in(1,2):
    for scenario in('block','miss'):
        path=ROOT/f'audit_v{1360 if scenario=="block"else 1374}_ring_close_{scenario}_p{side}_render_checked/report.json'
        proof=json.loads(path.read_text());assert proof['passed']and proof['candidate']==current.CANDIDATE
        folder=ROOT/f'audit_v1359_ring_close_{scenario}_p{side}';records={r['frame']:r for r in proof['replayed']['records']}
        selected={}
        def add(frame,label):
            assert frame in records;selected.setdefault(frame,[]).append(label)
        for age in(1,4,7,10,13):add(proof['state']['entry']+age,'release '+str(age))
        for phase,rows in proof['nativePhaseOrder'].items():
            if phase!='body':
                for r in rows:add(r['first']+1,phase+':'+f'{r["pose"]:08X}')
        for age in(1,2,4):add(proof['retirement']['frame']+age,'native cleanup '+str(age))
        for frame in sorted(records)[-2:]:add(frame,'ordinary follow-up')
        sheet_case(f'ring_{scenario}_p{side}',[(folder/'snap'/records[f]['file'],f'P{side} {scenario} {f}: '+','.join(labels))for f,labels in sorted(selected.items())],[path])
ui_path=ROOT/'audit_v1368_current_ui_flow_checked/report.json';ui=json.loads(ui_path.read_text());assert ui['passed']
entries=[]
for key,case in ui['cases'].items():
    folder=ROOT/f'audit_v1367_ui_{key}/snap'
    files={int(p.stem.split('_')[-1]):p for p in folder.glob('ui_*.png')}
    available=sorted(files)
    for target,label in((case['exit']-120,'hover/blink'),(case['exit']-112,'hover/blink'),(case['exit']-2,'last CSS'),(case['exit'],'exit'),(case['exit']+2,'ladder cleanup'),(case['live']+4,'first match')):
        # Keep the actual nearest recorded field explicit; never relabel it
        # as an unobserved target or substitute a different image silently.
        frame=min(available,key=lambda f:abs(f-target))
        entries.append((files[frame],f'{key} {label}: actual {frame}'))
sheet_case('ui',entries,[ui_path])
ground_path=ROOT/'audit_v1373_current_ground_shadow_checked/report.json';ground=json.loads(ground_path.read_text());assert ground['passed']
entries=[]
for key,case in ground['cases'].items():
    records=case['presentation']['records'];idle=records[0]
    airborne=next(r for r in records if not r['body'][str(case['side'])]['grounded'])
    for record,label in((idle,'idle soles/shadow'),(airborne,'airborne shadow')):
        entries.append((ROOT/f'audit_v1372_ground_shadow_{key}/snap/ground_{record["frame"]}.png',f'{key} {label} {record["frame"]}'))
sheet_case('ground',entries,[ground_path])
entries=[];proofs=[]
for side in(1,2):
    proof_path=ROOT/f'audit_v1388_blade_native_gore_p{side}_checked/report.json';proof=json.loads(proof_path.read_text());assert proof['passed'];proofs.append(proof_path)
    for prefix,label in((f'audit_v1383_blade_native_p{side}','current'),(f'audit_v1387_blade_native_prior_p{side}','prior')):
        entries.append((ROOT/prefix/'snap/special_recovered.png',f'P{side} blade {label}: original native blood'))
sheet_case('blade_blood',entries,proofs)
(OUT/'report.json').write_text(json.dumps(dict(candidate=current.CANDIDATE,cases=cases,fullImagesNotCropped=True,productionArtChanged=False,manualReviewPending=True),indent=2)+'\n')
print('Current full-frame contacts generated; manual review pending',flush=True)
