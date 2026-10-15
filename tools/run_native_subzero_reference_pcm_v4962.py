"""Stock/added actual earned references, exact mixed PCM digest per update, RAM-only."""
from pathlib import Path
prior=Path(__file__).with_name('run_native_subzero_shatter_lifecycle_v4944.py')
text=prior.read_text()
for before,after in(
 ("LUA='mk2ks_native_subzero_shatter_lifecycle_v4943.lua'","LUA='mk2ks_native_subzero_reference_pcm_v4961.lua'"),
 ('def capture(fighter,side):','def capture(fighter,side,profile):'),
 ("audit_v4945_subzero_{fighter}_p{side}_lifecycle","audit_v4963_subzero_{fighter}_p{side}_{profile}_reference"),
 ("audit_v4946_subzero_{args.fighter}_p{args.side}_lifecycle_observed","audit_v4964_subzero_{args.fighter}_p{args.side}_{args.profile}_reference_observed"),
 ("(LUA,'mk2ks_native_subzero_shatter_probe_v4939.lua',\n  'mk2ks_native_subzero_body_probe_v4933.lua','mk2ks_stock_fatality_v1021.lua')",
  "(LUA,'mk2ks_native_subzero_body_probe_v4933.lua','mk2ks_stock_fatality_v1021.lua')"),
 ('[*controllers,Path(__file__),Path(native.__file__)','[*controllers,prior,Path(__file__),Path(native.__file__),ROOT/\'mame-mkp/src/frontend/mame/luaengine.cpp\''),
 ("'-samples','-samplerate'","('-samples'if profile=='samples'else'-nosamples'),'-samplerate'"),
 ('guestproof=gfxproof=None;scenes=[]','guestproof=gfxproof=None;scenes=[];pcm=[];pcm_hash=hashlib.sha256();pcm_bytes=0'),
 ("if line.startswith(('MK2_EARNED_SUBZERO_GUEST '","""if line.startswith('MK2_EARNED_SUBZERO_PCM '):
     import array
     fields=dict(re.findall(r'(\\w+)=([^\\s]+)',line));raw=bytes.fromhex(fields.pop('hex'))
     need(len(raw)==int(fields['bytes'])and len(raw)%4==0 and int(fields['index'])==len(pcm)+1,'Every actual stereo PCM update in RAM')
     values=array.array('h',raw)
     peak=max((abs(v)for v in values),default=0);energy=sum(v*v for v in values)
     pcm_hash.update(raw);pcm_bytes+=len(raw)
     record=dict(frame=int(fields['frame']),index=int(fields['index']),seconds=fields['seconds'],bytes=len(raw),
                 sha256=hashlib.sha256(raw).hexdigest().upper(),peak=peak,energy=energy)
     pcm.append(record)
     log.write('MK2_EARNED_SUBZERO_PCM_DIGEST '+' '.join(str(k)+'='+str(v)for k,v in record.items())+'\\n')
    elif line.startswith(('MK2_EARNED_SUBZERO_GUEST '"""),
 ("log=(folder/'run.log').read_text();err=(folder/'stderr.log').read_text()", """audio=dict(profile=profile,sampleRate=48000,channels=2,bytesPerChannelSample=2,
  updates=pcm,totalBytes=pcm_bytes,wholePCMSHA256=pcm_hash.hexdigest().upper(),rawPCMOrWAVFilesWritten=0)
 (folder/'pcm_memory_proof.json').write_text(json.dumps(audio,indent=2)+'\\n')
 log=(folder/'run.log').read_text();err=(folder/'stderr.log').read_text()"""),
 ("actualScenes=scenes,inputHashes=pins,fullPortAcceptance=False","actualScenes=scenes,actualPCM=dict(profile=profile,updates=len(pcm),totalBytes=pcm_bytes,wholePCMSHA256=audio['wholePCMSHA256'],nonzeroUpdates=sum(r['peak']>0 for r in pcm)),inputHashes=pins,fullPortAcceptance=False"),
 ("need(len(scenes)==4,'Actual freeze, fracture, victory and subsequent scene')","need(len(scenes)==3 and len(pcm)>100 and any(r['peak']>0 for r in pcm),'Actual freeze/fracture/victory and nonzero complete mixed PCM interval')"),
 ("choices=('kano','sonya')","choices=('kano','sonya','kitana','liu_kang')"),
 ('args=parser.parse_args()',"parser.add_argument('--profile',required=True,choices=('samples','nosamples'));args=parser.parse_args()"),
 ('report=capture(args.fighter,args.side)','report=capture(args.fighter,args.side,args.profile)'),
):
 assert text.count(before)==1,before
 text=text.replace(before,after,1)
exec(compile(text,str(Path(__file__).resolve())+'::native_reference_mixed_pcm','exec'),globals())
