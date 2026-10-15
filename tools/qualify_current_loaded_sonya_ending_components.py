"""Genuine loaded Sonya ending registrations/text/headers, not a forced or earned ending."""
import copy,json,re
import verify_native_source_sync as sync
sync.verify();root=sync.ROOT
prep=root/'audit_current_loaded_sonya_ending_components_preparation';case=root/'audit_current_loaded_sonya_ending_components_runtime'
out=root/'audit_current_loaded_sonya_ending_components_checked';assert not out.exists()
assert sync.sha(prep/'expected.json')=='91006D04C915D62D413FA7A32E777D2E68DEEF2AAB302BEE01C964E95DAAA08F'
expected=json.loads((prep/'expected.json').read_text())
lines=(case/'run.log').read_text().splitlines();assert not any('LUA ERROR' in s for s in lines)
rows=[(s.split()[0],dict(re.findall(r'(\w+)=([^\s]+)',s))) for s in lines if s.startswith('MK2_ENDING_')]
def gate(records):
 text=[r for t,r in records if t=='MK2_ENDING_TEXT'];pictures=[r for t,r in records if t=='MK2_ENDING_PICTURE']
 assert len(text)==5 and len(pictures)==2
 for e in expected['texts']:
  r=next(r for r in text if int(r['page'])==e['page'] and int(r['segment'])==e['segment'])
  assert int(r['pointer'],16)==e['pointer'] and r['header']==e['headerHex'] and r['text']==e['textHex']
 for e in expected['pictures']:
  r=next(r for r in pictures if int(r['index'])==e['index'])
  assert int(r['pointer'],16)==e['pointer']
  for key in ('width','height','planes','palette'):assert int(r[key])==e[key]
 for tag,key in (('MK2_ENDING_OPERAND','operands'),('MK2_ENDING_CONTINUATION','continuations')):
  actual={r['at']:int(r['value'],16) for t,r in records if t==tag};assert actual==expected[key]
 null=[r for t,r in records if t=='MK2_ENDING_NULL'];assert len(null)==1 and int(null[0]['at'],16)==expected['secondPageNull']['at'] and int(null[0]['value'],16)==0
 done=[r for t,r in records if t=='MK2_ENDING_COMPONENT_DONE'];assert len(done)==1 and done[0]['fields']=='3' and done[0]['inputs']=='0'
 assert all(r['writes']=='0' and r['assistance']=='none' for t,r in records)
gate(rows);faults=[]
def change(records,tag,key,value):next(r for t,r in records if t==tag)[key]=value
for name,tag,key,value in (
 ('wrong_Sonya_text_pointer','MK2_ENDING_TEXT','pointer','FFFA7E20'),
 ('wrong_native_text_header','MK2_ENDING_TEXT','header','00000000'),
 ('wrong_story_bytes','MK2_ENDING_TEXT','text','00'),
 ('wrong_own_picture_pointer','MK2_ENDING_PICTURE','pointer','07100000'),
 ('wrong_picture_geometry','MK2_ENDING_PICTURE','width','80'),
 ('wrong_native_continuation','MK2_ENDING_CONTINUATION','value','0310'),
 ('wrong_text_operand','MK2_ENDING_OPERAND','value','FF8F5550'),
 ('wrong_page2_null','MK2_ENDING_NULL','value','FFFA7E00'),
):
 bad=copy.deepcopy(rows);change(bad,tag,key,value)
 try:gate(bad)
 except AssertionError:faults.append(name)
 else:raise AssertionError('Loaded component fault accepted:'+name)
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['observerSha256']=='119CFC21ED92B76D1E91F0172E4FD0A9B3C220D1B1701719EA68112BECFBA8C4'
assert not (case/'stderr.log').read_text().strip()
report=dict(currentLoadedSonyaEndingTextPictureHeaderContinuationComponentsAccepted=True,
 historicalUnchangedEndingComponentTransferSupported=True,loadedTextSegments=5,loadedPictureHeaders=2,loadedOperands=3,loadedContinuationWords=8,
 exactFiveNativeHeadersAndStoriesMatched=True,loadedSecondPageNullMatched=True,rejectedFaults=faults,
 inputFreeFields=3,forcedEnding=False,earnedCurrentSonyaEndingAccepted=False,fullEndingPixelsAccepted=False,fullAudioAccepted=False,fullPortAccepted=False,
 terminal=terminal,actualRecords=rows,logSHA256=sync.sha(case/'run.log'),sourceComponentProofSHA256=expected['sourceComponentProofSHA256'],expectedSHA256=sync.sha(prep/'expected.json'),
 scope='Current loaded ending registrations/native text headers/story bytes/two image geometry headers/eight paired continuation patch words. Historical earned Sonya cases remain evidence for unchanged components; not whole changed-game campaign, complete pixels, credits race or heardaudio.')
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ('currentLoadedSonyaEndingTextPictureHeaderContinuationComponentsAccepted','rejectedFaults','terminal','logSHA256')}))
