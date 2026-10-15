"""P1 stock/added shatter native DMA and paired entire mixed PCM; finite scope only."""
import copy,json,re,struct,subprocess
from pathlib import Path
import native_subzero_body_context_v4932 as native
import verify_earned_subzero_offset_matrix_v4913 as parser

ROOT,need,sha=native.ROOT,native.need,native.sha
OUT=ROOT/'audit_v4980_native_subzero_reference_pcm_checked'

def verify_pair(a,b,rows,guest,identity):
 need(a['sampleRate']==b['sampleRate']==48000 and a['channels']==b['channels']==2
      and a['bytesPerChannelSample']==b['bytesPerChannelSample']==2 and a['profile']=='samples'and b['profile']=='nosamples',
      'Actual paired full stereo48k PCM API, not stem estimates')
 need(a['updates']==b['updates']and a['wholePCMSHA256']==b['wholePCMSHA256']and a['totalBytes']==b['totalBytes']==1359360,
      'Every actual update and concatenated complete mixed PCM identical across sample profiles')
 updates=a['updates'];need(len(updates)==354 and [r['index']for r in updates]==list(range(1,355)),
      'Every actual consecutive sound callback retained')
 for r in updates:need(r['bytes']==3840 and 0<=r['peak']<=32768 and r['energy']>=0 and len(r['sha256'])==64,'Actual complete20ms PCM buffers')
 need(all(abs(float(y['seconds'])-float(x['seconds'])-.02)<1e-9 for x,y in zip(updates,updates[1:]))
      and sum(r['peak']>0 for r in updates)==353,'Native50Hz audio cadence and actual nonsilence')
 def pick(tag):
  q=[r for r in rows if r['tag']=='MK2_EARNED_SUBZERO_'+tag];need(len(q)==1,'Actual unique '+tag);return q[0]
 deep,fracture,end=(pick(t)for t in('DEEP_TASK','FRACTURE_ENTRY','LIFECYCLE_END'))
 need(updates[0]['frame']==int(deep['frame'])and updates[-1]['frame']==int(end['frame'])
      and int(end['frame'])==int(end['wrap'])+180 and int(end['pcm_updates'])==354,
      'Complete actual native freeze through win+180 audio interval')
 sound=pick('SOUND_CALL');need(sound['a0']=='000000D8'and sound['frame']==fracture['frame'],'Actual original fractureD8 sound source')
 need(a['rawPCMOrWAVFilesWritten']==b['rawPCMOrWAVFilesWritten']==0,'No raw audio on disk')
 dmas=[r for r in rows if r['tag']=='MK2_EARNED_SUBZERO_DMA']
 groups={'BODY_LOOKUP':0xffd62600,'LEGS_LOOKUP':0xffd62a00}
 actual=[]
 for tag,table in groups.items():
  lookup=pick(tag);need(int(lookup['a9'],16)==identity*32,'True native identity body index')
  group=struct.unpack_from('<I',guest,(table+identity*32-0xff800000)//8)[0]
  desc=[]
  for i in range(3):
   p=struct.unpack_from('<I',guest,(group+i*32-0xff800000)//8)[0]
   if p==0:break
   d=struct.unpack_from('<4hIH',guest,(p-0xff800000)//8);desc.append(d)
  need(len(desc)==(3 if tag=='BODY_LOOKUP'else2),'Original native3part whole/2part legs topology')
  scene=int(deep['frame'])+100 if tag=='BODY_LOOKUP'else int(end['wrap'])+150
  for width,height,x,y,gfx,flags in desc:
   matches=[r for r in dmas if int(r['frame'])==scene and int(r['source'],16)==gfx]
   need(len(matches)==1 and matches[0]['width']==str(width)and matches[0]['height']==str(height)
        and matches[0]['palette']=='0404'and int(matches[0]['command'],16)&15==2
        and int(matches[0]['command'],16)&0x7fc0==flags&0x7fc0,
        'Every actual native cold-body DMA bound to guest descriptor; zero pixels skipped')
   actual.append(matches[0])
 return dict(identity=identity,side=1,pairedPCMUpdates=354,pairedCompletePCMBytes=1359360,
             wholePCMSHA256=a['wholePCMSHA256'],actualNativeBodyDMA=actual,actualZeroPixelTransparencyProven=True,
             externalSamplesDoNotAlterThisEntireMixedPCMWindow=True,fullAudioAcceptance=False,fullArtAcceptance=False)

def main():
 need(not OUT.exists(),'Fresh independent finite reference proof')
 guest=native.expected();pins={};cases=[];faults=[]
 for fighter,identity in(('kitana',4),('kano',17),('sonya',18)):
  folders=[ROOT/f'audit_v4967_subzero_{fighter}_p1_samples_reference',ROOT/f'audit_v4976_subzero_{fighter}_p1_nosamples_reference']
  reports=[ROOT/f'audit_v4968_subzero_{fighter}_p1_samples_reference_observed/report.json',ROOT/f'audit_v4977_subzero_{fighter}_p1_nosamples_reference_observed/report.json']
  audio=[];logs=[];rgbs=[]
  for folder,path in zip(folders,reports):
   report=json.loads(path.read_text());meta=json.loads((folder/'result.json').read_text())
   need(report['passed']and report['nativeExit']==0 and not report['fullPortAcceptance'],'Actual native terminal reference case')
   g=json.loads((folder/'guest_memory_proof.json').read_text());need(g['everyActualByteComparedInRAM']and g['sha256']==native.GUEST_SHA and g['executableSHA256']==native.EXE_SHA,'Entire actual guest and exact binary bound')
   audio.append(json.loads((folder/'pcm_memory_proof.json').read_text()));logs.append((folder/'run.log').read_text());rgbs.append(json.loads((folder/'rgb_memory_proofs.json').read_text()))
   need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',logs[-1]+(folder/'stderr.log').read_text(),re.I),'Actual transport and all callbacks clean')
   pins.update(meta['inputHashes'])
   for p in[path,*[p for p in folder.rglob('*')if p.is_file()]]:pins[str(p.resolve())]=sha(p)
  rows=parser.parse(logs[0]);need(rows==parser.parse(logs[1])and rgbs[0]==rgbs[1],
      'Every actual native event/DMA and all three entire RGB fields identical across profiles')
  positive=verify_pair(*audio,rows,guest,identity);cases.append(dict(fighter=fighter,**positive))
  for label,mutate in(('altered_PCM',lambda x:x['updates'][120].update(sha256='0'*64)),
                       ('missing_PCM',lambda x:x['updates'].pop(120)),
                       ('wrong_audio_cadence',lambda x:x['updates'][120].update(seconds='0')),
                       ('altered_whole_PCM',lambda x:x.update(wholePCMSHA256='0'*64))):
   altered=copy.deepcopy(audio[1]);mutate(altered)
   try:verify_pair(audio[0],altered,rows,guest,identity)
   except ValueError as e:faults.append(dict(case=fighter,fault=label,rejectedBy=str(e)))
   else:raise ValueError('Counterexample admitted '+label)
  altered=copy.deepcopy(rows);target=next(r for r in altered if r['tag']=='MK2_EARNED_SUBZERO_DMA'and r in positive['actualNativeBodyDMA']);target['command']=f"{int(target['command'],16)|1:04X}"
  try:verify_pair(*audio,altered,guest,identity)
  except ValueError as e:faults.append(dict(case=fighter,fault='opaque_zero_blit',rejectedBy=str(e)))
  else:raise ValueError('Opaque zero-blit admitted')
 for p in(Path(__file__),Path(native.__file__),Path(parser.__file__)):pins[str(p.resolve())]=sha(p)
 need(len(cases)==3 and len(faults)==15 and all(sha(p)==h for p,h in pins.items()),'Actual finite matrix and every immutable input')
 result=dict(passed=True,candidate=native.NAME,cases=cases,alteredRecordFaultsRejected=faults,inputHashes=pins,
  actualPairedPCMContexts=3,actualTotalPairedPCMBytes=4078080,fullAudioAcceptance=False,fullArtAcceptance=False,
  fullPortAcceptance=False,allFourAddedVictimSlotsAccepted=False,
  actualArtCounterexample='Native DMA transparently skips zero pixels. The rectangular part cut leaves floating hand remnants and a flat waist, unlike stock Kitana/Liu shaped ice edges. Dedicated semantic lower-body art is required, not a compression change.')
 OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress evidence')
 (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(passed=True,cases=[{k:v for k,v in c.items()if k!='actualNativeBodyDMA'}for c in cases],negativeFaults=len(faults),fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
