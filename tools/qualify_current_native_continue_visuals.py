"""Reexecute earned-continue gates and exact full scalar baselines for four images."""
import json
import check_campaign_stage_chronology as chronology
import qualify_current_native_continue_roles as roles
import verify_native_source_sync as sync
sync.verify()
out=sync.ROOT/'audit_current_native_continue_visuals_checked';assert not out.exists()
cases=[];total=0
for fighter in ('kano','sonya'):
 for side in (1,2):
  folder=sync.ROOT/f'audit_current_native_continue_visual_{fighter}_p{side}_runtime'
  terminal=json.loads((folder/'terminal.json').read_text())
  assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
  rows=chronology.load(folder/'run.log')
  result=roles.gate(rows,fighter,side)
  baseline=chronology.load(sync.ROOT/f'audit_current_native_continue_{fighter}_p{side}_runtime/run.log')
  assert {k:v for k,v in rows.items() if k!='CONTINUE_VISUAL'}==baseline
  assert len(rows['CONTINUE_VISUAL'])==1 and rows['CONTINUE_VISUAL'][0]['age']=='30'
  pictures=list((folder/'snap').glob('*.png'));assert len(pictures)==1
  image=pictures[0];assert image.stat().st_size<=128*1024
  total+=image.stat().st_size
  result.update(scalarBaselineExact=True,imageSHA256=sync.sha(image),imageBytes=image.stat().st_size,
                logSHA256=sync.sha(folder/'run.log'))
  cases.append(result)
assert total<=512*1024
out.mkdir();(out/'report.json').write_text(json.dumps({'passed':True,'cases':cases,'totalImageBytes':total,
 'continuousVisualAudioAccepted':False,'fullPortAccepted':False},indent=2))
print(json.dumps({'passed':True,'cases':4,'totalImageBytes':total}))
