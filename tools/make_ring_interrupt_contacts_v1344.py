"""Unmodified actual full frames for pink charge, interruption and close retry."""
import json,math
from pathlib import Path
from PIL import Image,ImageDraw
import verify_ring_native_lookup_v1342 as current
ROOT=current.ROOT;OUT=ROOT/'audit_v1344_ring_interrupt_contacts'
assert not OUT.exists();OUT.mkdir();cases={}
for side in(1,2):
    proof_path=ROOT/f'audit_v1346_ring_interrupt_p{side}_render_checked/report.json'
    proof=json.loads(proof_path.read_text());assert proof['passed']and proof['candidate']==current.CANDIDATE
    folder=ROOT/f'audit_v1341_ring_interrupt_p{side}';records={r['frame']:r for r in proof['replayed']['records']};state=proof['state']
    selected={}
    def add(frame,label):
        assert frame in records;selected.setdefault(frame,[]).append(label)
    for age in(1,4,7,10):add(state['first_entry']+age,'first charge '+str(age))
    for age in(0,1,2,4,8):add(state['hit']+age,'uppercut reaction '+str(age))
    for phase,rows in proof['nativePhaseOrder'].items():
        for row in rows:add(row['first']+1,phase+':'+f'{row["pose"]:08X}')
    for age in(1,2,4):add(proof['retirement']['frame']+age,'native cleanup '+str(age))
    for frame in sorted(records)[-3:]:add(frame,'ordinary follow-up')
    entries=[];sheets=[];ordered=sorted(selected.items())
    for page in range(math.ceil(len(ordered)/20)):
        section=ordered[page*20:(page+1)*20];sheet=Image.new('RGB',(1600,math.ceil(len(section)/4)*282),(24,24,24));draw=ImageDraw.Draw(sheet)
        for n,(frame,labels)in enumerate(section):
            path=folder/'snap'/records[frame]['file'];im=Image.open(path).convert('RGB');assert im.size==(400,254)
            x,y=n%4*400,n//4*282;sheet.paste(im,(x,y+28));draw.text((x+4,y+2),f'P{side} ring interrupt/retry field {frame}',fill='white');draw.text((x+4,y+14),' / '.join(labels),fill='white')
            entries.append(dict(frame=frame,labels=labels,file=str(path),sha256=current.digest(path),page=page))
        path=OUT/f'ring_interrupt_p{side}_{page+1}.png';sheet.save(path);sheets.append(dict(file=str(path),sha256=current.digest(path)))
    cases[str(side)]=dict(proof=str(proof_path),proofSHA256=current.digest(proof_path),entries=entries,sheets=sheets)
(OUT/'report.json').write_text(json.dumps(dict(candidate=current.CANDIDATE,cases=cases,fullImagesNotCropped=True,productionArtChanged=False,manualReviewPending=True),indent=2)+'\n')
print('Actual ring interruption/close retry contacts generated; manual review pending',flush=True)
