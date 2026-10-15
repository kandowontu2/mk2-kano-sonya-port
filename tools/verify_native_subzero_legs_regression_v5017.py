"""Independent cross-candidate physical/RGB regression and P1 native vocal/entire PCM proof."""
import copy,json,re,struct,subprocess
from pathlib import Path
import native_subzero_legs_context_v4993 as native
import verify_earned_subzero_offset_matrix_v4913 as parser
import verify_native_subzero_reference_pcm_v4981 as audio_gate
import verify_native_subzero_legs_matrix_v5004 as sequence

ROOT,need,sha=native.ROOT,native.need,native.sha
OUT=ROOT/'audit_v5018_native_subzero_legs_regression_checked'

def normalize(rows):
 return [{k:(v.replace('FFD62900','FFD63400').replace('FFD62960','FFD63460')if isinstance(v,str)else v)
          for k,v in row.items()}for row in rows if '_DIGEST'not in row['tag']]

def vocal(guest,rows,identity):
 branch='FEMALE_VOCAL'if identity==18 else'MALE_VOCAL'
 wanted=0x48 if identity==18 else0x45
 events=[r for r in rows if r['tag']=='MK2_EARNED_SUBZERO_'+branch]
 calls=[r for r in rows if r['tag']=='MK2_EARNED_SUBZERO_VOICE_DISPATCH']
 need(len(events)==len(calls)==1,'Actual unique native victim gender branch/voice dispatch')
 expected_pc=0xffa123b0 if identity==18 else0xffa12360
 for event,entry in((events[0],expected_pc),(calls[0],0xffa12420)):
  need(int(event['entry'],16)==entry and int(event['pc'],16)==entry+16 and event['mask']=='FFFF'
       and int(event['value'],16)==struct.unpack_from('<H',guest,(entry-0xff800000)//8)[0],
       'Actual voice branch opcode/PC/mask bound to complete initialized guest')
  need(event['actor']==event['owner']=='01034E90'and event['id']==event['identity']==str(identity)
       and event['side']=='1'and event['action']=='0408'and event['frame']=='3317'
       and event['palette']=='0404'and event['writes']=='0'and event['assistance']=='none',
       'Actual native branch belongs to true owned shatter victim')
 need(events[0]['a1']=='45464748'and int(calls[0]['a0'],16)==int(calls[0]['a1'],16)==wanted,
      'Correct native45 male/48 female byte selected from original packed voice choices')
 opposite='MALE_VOCAL'if identity==18 else'FEMALE_VOCAL'
 need(not any(r['tag']=='MK2_EARNED_SUBZERO_'+opposite for r in rows),'No opposite gender branch in this actual interval')
 return dict(identity=identity,side=1,branch=branch,voiceByte=f'{wanted:02X}',events=events+calls,
             directSoundPrimitiveDeliveryObserved=False,fullVoiceAudioAcceptance=False)

def main():
 need(not OUT.exists(),'Fresh cross-candidate proof')
 guest=native.expected();pins={};cross=[];audio=[];faults=[]
 def pin(p,h=None):
  p=Path(p).resolve();actual=sha(p);need(h is None or actual==h,'Exact actual input hash')
  need(str(p)not in pins or pins[str(p)]==actual,'Consistent immutable input');pins[str(p)]=actual
 checked=ROOT/'audit_v5005_native_subzero_legs_matrix_checked/report.json';matrix=json.loads(checked.read_text())
 need(matrix['passed']and len(matrix['cases'])==4 and not matrix['fullPortAcceptance'],'Real four-slot native instance matrix')
 pin(checked)
 for p,h in matrix['inputHashes'].items():pin(p,h)
 for fighter,identity in(('kano',17),('sonya',18)):
  for side in(1,2):
   old=ROOT/f'audit_v4953_subzero_{fighter}_p{side}_lifecycle';new=ROOT/f'audit_v5002_subzero_{fighter}_p{side}_lifecycle'
   old_report=ROOT/f'audit_v4954_subzero_{fighter}_p{side}_lifecycle_observed/report.json'
   report=json.loads(old_report.read_text());need(report['passed']and report['nativeExit']==0,'Actual prior native terminal baseline')
   before,after=(parser.parse((p/'run.log').read_text())for p in(old,new))
   a,b=normalize(before),normalize(after);need(a==b,'Every actual native/physical row identical except explicitly replaced two-leg group pointer')
   initial,final=(json.loads((p/'rgb_memory_proofs.json').read_text())for p in(old,new))
   need(len(initial)==len(final)==4 and [r['frame']for r in initial]==[r['frame']for r in final],
        'All four actual scene times preserved, no lifecycle change')
   need(initial[0]==final[0]and initial[3]==final[3]and initial[1]['sha256']!=final[1]['sha256']
        and initial[2]['sha256']!=final[2]['sha256'],'Only actual post-fracture art scenes differ; whole freeze and fresh CPU scene identical')
   cross.append(dict(fighter=fighter,side=side,actualPhysicalNativeRowsCompared=len(a),
       onlyNormalizedValues={'FFD62900':'FFD63400','FFD62960':'FFD63460'},initialFreezeAndNextMatchEntireRGBIdentical=True,
       onlyFractureAndParkedLegsRGBChanged=True,fullPortAcceptance=False))
   for p in[old_report,*[p for p in old.rglob('*')if p.is_file()]]:pin(p)
   for p,h in json.loads((old/'result.json').read_text())['inputHashes'].items():pin(p,h)
  folder=ROOT/f'audit_v5014_subzero_{fighter}_p1_nosamples_reference'
  observed=ROOT/f'audit_v5015_subzero_{fighter}_p1_nosamples_reference_observed/report.json'
  report=json.loads(observed.read_text());need(report['passed']and report['nativeExit']==0,'Actual consumed mixed PCM native case')
  rows=parser.parse((folder/'run.log').read_text());actual=json.loads((folder/'pcm_memory_proof.json').read_text())
  baseline=ROOT/f'audit_v4967_subzero_{fighter}_p1_samples_reference/pcm_memory_proof.json'
  older_off=ROOT/f'audit_v4976_subzero_{fighter}_p1_nosamples_reference/pcm_memory_proof.json'
  before=json.loads(baseline.read_text());off=json.loads(older_off.read_text())
  need(before['updates']==off['updates']and before['wholePCMSHA256']==off['wholePCMSHA256'],
       'Previously qualified samples-on/off baseline remains exact')
  positive=audio_gate.verify_pair(before,actual,rows,guest,identity);voice=vocal(guest,rows,identity)
  expected_rgb=json.loads((ROOT/f'audit_v5002_subzero_{fighter}_p1_lifecycle/rgb_memory_proofs.json').read_text())[:3]
  need(json.loads((folder/'rgb_memory_proofs.json').read_text())==expected_rgb,'Read-only DMA/PCM/vocal observation preserves all actual shatter RGB fields')
  positive.update(fighter=fighter,nativeGenderAndDispatch=voice,currentNoSamplesMatchesBothPriorProfiles=True)
  audio.append(positive)
  for label,tag,key,value in(('wrong_gender','FEMALE_VOCAL'if identity==18 else'MALE_VOCAL','id','1'),
                              ('wrong_voice_byte','VOICE_DISPATCH','a0','00000047'),
                              ('wrong_vocal_opcode','VOICE_DISPATCH','value','0000')):
   changed=copy.deepcopy(rows);target=next(r for r in changed if r['tag']=='MK2_EARNED_SUBZERO_'+tag);target[key]=value
   try:vocal(guest,changed,identity)
   except ValueError as e:faults.append(dict(case=fighter,fault=label,rejectedBy=str(e)))
   else:raise ValueError('Altered native voice record admitted')
  changed=copy.deepcopy(actual);changed['updates'][100]['sha256']='0'*64
  try:audio_gate.verify_pair(before,changed,rows,guest,identity)
  except ValueError as e:faults.append(dict(case=fighter,fault='changed_current_PCM',rejectedBy=str(e)))
  else:raise ValueError('Changed actual PCM admitted')
  for p in[baseline,older_off,observed,*[p for p in folder.rglob('*')if p.is_file()]]:pin(p)
  for p,h in json.loads((folder/'result.json').read_text())['inputHashes'].items():pin(p,h)
 # A repeat cold boot exists only because initial UI output was truncated, not because native evidence failed.
 folder=ROOT/'audit_v5008_subzero_kano_p1_lifecycle';observed=ROOT/'audit_v5009_subzero_kano_p1_lifecycle_observed/report.json'
 repeat=json.loads(observed.read_text());need(repeat['passed']and repeat['nativeExit']==0,'Actual repeated terminal native review')
 rows=parser.parse((folder/'run.log').read_text());scenes=json.loads((folder/'rgb_memory_proofs.json').read_text())
 sequence.verify(guest,rows,(folder/'run.log').read_text(),17,1,scenes)
 need(scenes==json.loads((ROOT/'audit_v5002_subzero_kano_p1_lifecycle/rgb_memory_proofs.json').read_text()),'Every actual repeated full scene identical, all four successfully viewed in RAM')
 for p in[observed,*[p for p in folder.rglob('*')if p.is_file()]]:pin(p)
 for p,h in json.loads((folder/'result.json').read_text())['inputHashes'].items():pin(p,h)
 for p in(Path(__file__),Path(native.__file__),Path(parser.__file__),Path(audio_gate.__file__),Path(sequence.__file__)):pin(p)
 need(len(cross)==4 and len(audio)==2 and len(faults)==8 and all(sha(p)==h for p,h in pins.items()),'Actual finite matrix/counterexamples and immutable evidence')
 result=dict(passed=True,crossCandidateCases=cross,currentMixedPCMAndVocalCases=audio,actualFaultsRejected=faults,
  executableSHA256=native.EXE_SHA,guestSHA256=native.GUEST_SHA,inputHashes=pins,
  actualAddedVictimSlotCasesCompared=4,actualCurrentPCMContexts=2,allNativeLegCasesViewed=True,
  actualRepeatedKanoP1ReviewEntireRGBIdentical=True,
  fullArtAcceptance=False,fullAudioAcceptance=False,normalHealthFreezeAccepted=False,
  nativeFloorShadowCoverageAccepted=False,fullPortAcceptance=False,publicBuildPromoted=False)
 OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress exact finite cross-proof')
 (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(passed=True,crossCandidateCases=4,actualNativePhysicalRows=sum(c['actualPhysicalNativeRowsCompared']for c in cross),
       currentPCMContexts=2,nativeVocalBytes=[r['nativeGenderAndDispatch']['voiceByte']for r in audio],
       negativeFaults=8,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
