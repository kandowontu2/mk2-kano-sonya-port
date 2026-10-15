"""In-memory corruptions only; never edit gameplay logs or rendered evidence."""
import json,re,struct
import verify_native_arm_rip_v1051 as proof
OUT=proof.ROOT/'audit_v1053_arm_rip_proof_units'
if OUT.exists():raise ValueError('Preserve evidence')
texts={case:(proof.ROOT/case/'run.log').read_text(encoding='utf-8-sig') for case in proof.CASES}
baseline=proof.verify(texts,False);assert baseline['passed'],baseline['errors']
case=proof.CASES[0];text=texts[case];checks=[]
def run(name,changed,reason):
 assert changed!=text
 fixture=dict(texts);fixture[case]=changed
 result=proof.verify(fixture,False)
 assert not result['passed'] and any(reason in error for error in result['errors']),(name,result['errors'])
 checks.append({'name':name,'rejected':True,'expectedReason':reason})
body=next(line for line in text.splitlines() if '_QUEUE ' in line and 'source=0FA' in line and 'id=17 ' in line)
run('proxy body identity',text.replace(body,body.replace('id=17 ','id=1 '),1),'True victim body')
run('floating body actor',text.replace(body,body.replace('floor=82 ','floor=81 '),1),'Own actor floor')
row=next(line for line in text.splitlines() if '_TABLE_RETURN ' in line and 'table=FFFDD280 ' in line)
run('wrong native victim offset',text.replace(row,row.replace('value=0005FF70','value=FFFBFF70'),1),'True-ID native table 1')
wrap=next(line for line in text.splitlines() if '_WRAP ' in line)
run('skipped native timing',text.replace(wrap,wrap.replace('age=147','age=146'),1),'Native completion timing')
comparison=next(line for line in text.splitlines() if '_COMPARE ' in line and 'table=FF879BE0 ' in line)
run('incorrect physical button history',text.replace(comparison,comparison.replace('actual=2','actual=0'),1),'Original button parser')
dma=next(line for line in text.splitlines() if '_DMA ' in line and 'source=0FA' in line)
width=re.search(r'width=(\d+)',dma)
run('wrong actual raster dimensions',text.replace(dma,dma[:width.start(1)]+str(int(width[1])+1)+dma[width.end(1):],1),'Actual dimensions')
guest,_,_=proof.reconstruct()
old=(proof.ROOT/'audit_v1046_jax_kano_p1_owned_arms/guest_maincpu.bin').read_bytes()
diff=[i for i,(a,b) in enumerate(zip(old,guest)) if a!=b]
assert diff==[0xfba92,0xfba93]
assert old[0xfba92:0xfba94]==b'\x00\xd0' and guest[0xfba92:0xfba94]==b'\xb0\x57'
checks.append({'name':'actual first candidate with adjacent operand contamination','rejected':True,'wrongGuestBytes':[hex(i) for i in diff]})
OUT.mkdir();data={'passed':True,'checks':checks,'checksCount':len(checks),
 'evidenceFilesModified':False,'fullPortAccepted':False}
(OUT/'unit-results.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data,indent=2))
