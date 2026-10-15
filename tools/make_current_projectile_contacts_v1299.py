"""Contact sheets of unchanged actual phase coverage and cleanup-tail captures."""
import json,math
from pathlib import Path
from PIL import Image,ImageDraw
import verify_human_projectile_display_v1293 as hit
ROOT=hit.ROOT;OUT=ROOT/'audit_v1299_current_projectile_contacts'
assert not OUT.exists();OUT.mkdir();cases={}
for move in('knife','ring'):
    for side in(1,2):
        for scenario in('hit','block','miss'):
            suffix=f'{move}_p{side}'if scenario=='hit'else f'{move}_{scenario}_p{side}'
            proof_path=ROOT/f'audit_v{1293 if scenario=="hit"else 1297}_projectile_{suffix}_render_checked/report.json'
            proof=json.loads(proof_path.read_text());assert proof['passed']and proof['candidate']==hit.current.CANDIDATE
            folder=ROOT/f'audit_v{1291 if scenario=="hit"else 1296}_projectile_{suffix}'
            records={r['frame']:r for r in proof['replayed']['records']};selected={};seen=set()
            for phase,rows in proof['nativePhaseOrder'].items():
                for row in rows:
                    if (phase,row['pose'])in seen:continue
                    seen.add((phase,row['pose']));frame=row['first']+1
                    assert frame in records,'Each actually observed distinct phase group has a full replayed capture'
                    selected.setdefault(frame,[]).append(phase+':'+f'{row["pose"]:08X}')
            retirement=proof['retirement']['frame']
            for frame in sorted(records):
                if retirement<frame<=retirement+5:selected.setdefault(frame,[]).append('cleanup tail')
            for frame in sorted(records)[-3:]:selected.setdefault(frame,[]).append('ordinary follow-up')
            entries=[];sheets=[];ordered=sorted(selected.items())
            for page in range(math.ceil(len(ordered)/20)):
                section=ordered[page*20:(page+1)*20]
                sheet=Image.new('RGB',(1600,math.ceil(len(section)/4)*282),(24,24,24));draw=ImageDraw.Draw(sheet)
                for n,(frame,labels)in enumerate(section):
                    path=folder/'snap'/records[frame]['file'];im=Image.open(path).convert('RGB');assert im.size==(400,254)
                    x,y=n%4*400,n//4*282;sheet.paste(im,(x,y+28))
                    draw.text((x+4,y+2),f'{suffix} {scenario} field {frame}',fill='white')
                    draw.text((x+4,y+14),' / '.join(labels),fill='white')
                    entries.append(dict(frame=frame,labels=labels,file=str(path),sha256=hit.current.digest(path),page=page))
                path=OUT/f'{suffix}_{scenario}_{page+1}.png';sheet.save(path);sheets.append(dict(file=str(path),sha256=hit.current.digest(path)))
            cases[suffix+'/'+scenario]=dict(proof=str(proof_path),proofSHA256=hit.current.digest(proof_path),sheets=sheets,entries=entries)
(OUT/'report.json').write_text(json.dumps(dict(candidate=hit.current.CANDIDATE,cases=cases,
    allExecutedDistinctPhaseGroupsIncluded=True,fullImagesNotCropped=True,productionArtChanged=False,manualReviewPending=True),indent=2)+'\n')
print('Actual phase and cleanup contact sheets created; manual review pending',flush=True)
