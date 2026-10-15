"""Unedited actual current UI captures, with diagnostic captions only."""
import json
from PIL import Image,ImageDraw
import verify_current_ui_flow_v1271 as current
ROOT=current.ROOT;OUT=ROOT/'audit_v1274_current_ui_contacts';assert not OUT.exists();OUT.mkdir();cases={}
for fighter in ('kano','sonya'):
    for side in (1,2):
        key=f'{fighter}_p{side}';folder=ROOT/f'audit_v1270_ui_{key}';log=(folder/'run.log').read_text(encoding='utf-8-sig')
        rows=current.model.records(log,'SNAP');n=current.model.n
        selected=[r for r in rows if r['scene']=='select'and 54<=n(r,'age')<=70]
        settled=next(r for r in rows if r['scene']=='select'and 78<=n(r,'age')<=94)
        transition=[r for r in rows if r['scene']=='transition']
        fight=next(r for r in rows if r['scene']=='fight'and n(r,'age')>=60)
        # Both blink phases, stock neighbor, first transition, ladder and match.
        chosen=[selected[0],selected[1],settled,transition[0],transition[len(transition)//2],fight]
        sheet=Image.new('RGB',(1200,556),(25,25,25));draw=ImageDraw.Draw(sheet);entries=[]
        for i,row in enumerate(chosen):
            path=folder/'snap'/row['file'];image=Image.open(path).convert('RGB');assert image.size==(400,254)
            x,y=(i%3)*400,(i//3)*278;sheet.paste(image,(x,y+24));draw.text((x+4,y+5),f'{key} {row["scene"]} age {row["age"]}',fill='white')
            entries.append(dict(file=str(path),sha256=current.current.digest(path),scene=row['scene'],age=n(row,'age'),frame=n(row,'frame')))
        path=OUT/f'{key}.png';sheet.save(path);cases[key]=dict(sheet=str(path),sha256=current.current.digest(path),entries=entries)
(OUT/'report.json').write_text(json.dumps(dict(candidate=current.current.CANDIDATE,cases=cases,productionArtChanged=False,manualReviewPending=True),indent=2)+'\n')
print('Four sheets with24 actual current CSS/transition/ladder/match images',flush=True)
