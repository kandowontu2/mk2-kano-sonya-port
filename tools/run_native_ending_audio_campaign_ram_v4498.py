"""New natural final-KO/ending/attract native PCM windows, original controls.

Whole4439 guest/raster/manifest/terminal collector retained. Only role-specific
existing policy, additional read-only observer and RAM PCM sink adapt. Native
samples-on/off comparisons do not imply an independent stock DCS reference.
"""
import concurrent.futures,hashlib,inspect,json,re,subprocess,traceback
from pathlib import Path
import numpy as np
import run_kintaro_pressure_guard_long_campaign_v4439 as original
import qualify_native_ending_audio_source_v4501 as source
ROOT,need,sha,NAME=original.ROOT,original.need,original.sha,original.NAME
OUT=ROOT/'audit_v4500_native_ending_audio_observed'

def collector(fighter,enabled):
    text=inspect.getsource(original.capture)
    changes=[("need(fighter=='sonya','Actual unfinished Sonya P2 context only')",
              "need(fighter in ('kano','sonya'),'Both actual accepted P2 policies only')"),
             ('source.source_boundary()','source.source_boundary(fighter)'),
             ('audit_v4438_kintaro_pressure_guard_long_source_preflight/report.json',str(source.OUT.relative_to(ROOT))+'/report.json'),
             ("folder=ROOT/f'audit_v4440_{fighter}_kintaro_pressure_guard_long_p2_campaign'",
              "folder=ROOT/f'audit_v4499_{fighter}_p2_ending_audio_{suffix}'"),
             ("MK2KS_CAMPAIGN_STRATEGY='guard_punish'","MK2KS_CAMPAIGN_STRATEGY='zoning'if fighter=='kano'else'guard_punish'"),
             ("'-artpath',str(ROOT/'artwork'),'-samples'","'-artpath',str(ROOT/'artwork'),'-samples'if enabled else'-nosamples'"),
             ('headers=[];images={};stream=hashlib.sha256();byte_count=0;guest_sha=None',
              'headers=[];images={};stream=hashlib.sha256();byte_count=0;guest_sha=None;audio_headers=[];audio_chunks=[]'),
             ("if line.startswith('MK2_CAMPAIGN_GUEST_RAM '):",'''if line.startswith('MK2_EAUDIO_PCM '):
                    h=dict(re.findall(r'(\\w+)=([^\\s]+)',line));raw=bytes.fromhex(h.pop('hex'))
                    need(len(raw)==int(h['bytes']) and len(raw)%4==0,'Complete actual native stereo PCM update, no tolerance')
                    h['sha256']=hashlib.sha256(raw).hexdigest().upper();audio_headers.append(h);audio_chunks.append(raw)
                    log.write('MK2_EAUDIO_PCM_DIGEST '+' '.join(f'{k}={v}'for k,v in h.items())+'\\n')
                elif line.startswith('MK2_CAMPAIGN_GUEST_RAM '):'''),
             ('nativeFrameStreamSHA256=stream.hexdigest().upper(),passed=False',
              "nativeFrameStreamSHA256=stream.hexdigest().upper(),samples_enabled=enabled,mixedPCMUpdates=len(audio_headers),mixedPCMBytesVerifiedInRAM=sum(map(len,audio_chunks)),mixedPCMSHA256=hashlib.sha256(b''.join(audio_chunks)).hexdigest().upper(),passed=False"),
             ('return folder,headers,images',"return folder,headers,images,audio_headers,np.frombuffer(b''.join(audio_chunks),dtype='<i2').reshape(-1,2).copy()")]
    for before,after in changes:
        need(text.count(before)==1,'Only declared whole collector role/policy/observer/RAM sink changes: '+before)
        text=text.replace(before,after,1)
    # Preserve all compiled-input/source snapshots; explicitly include the
    # native sound implementation whose output is being observed.
    before='    files.update(ROOT/p for p in source.TRANSITIVE_LUA)'
    need(text.count(before)==1,'All existing transitive source snapshots retained')
    text=text.replace(before,before+"\n    files.update(ROOT/p for p in ('mame-mkp/src/mame/shared/dcs.cpp','mame-mkp/src/emu/sound.cpp','mame-mkp/src/devices/sound/samples.cpp','mame-mkp/src/frontend/mame/luaengine.cpp'))",1)
    scope=dict(vars(original),__file__=__file__,source=source,LUA=source.LUA[fighter],enabled=enabled,
               suffix='samples'if enabled else'nosamples')
    exec(compile(text,__file__+'::entire4439_native_PCM_sinks_only','exec'),scope)
    return scope['capture']

def rows(text,tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)',s)) for s in text.splitlines() if s.startswith('MK2_EAUDIO_'+tag+' ')]

def pair(fighter):
    observed=[]
    for enabled in (True,False):
        folder,images_headers,images,audio_headers,pcm=collector(fighter,enabled)(fighter)
        need(audio_headers and len(pcm)>0,'Actual native ending audio, never a missing/empty transport')
        observed.append((folder,audio_headers,pcm))
    (folder,headers,a),(baseline,old_headers,b)=observed
    text=(folder/'run.log').read_text();old=(baseline/'run.log').read_text()
    references={'kano':ROOT/'audit_v4485_kano_current_p2_campaign_ram',
                'sonya':ROOT/'audit_v4440_sonya_kintaro_pressure_guard_long_p2_campaign'}
    native=lambda t:[s for s in t.splitlines() if s.startswith(('MK2_NAT_CAMPAIGN_','MK2_MILEENA_CAMPAIGN_','MK2_BOSS_KNIFE_','MK2_CAMPAIGN_GUEST_RAM_DIGEST ','MK2_CAMPAIGN_RAM_FRAME_DIGEST '))]
    need(native(text)==native(old)==native((references[fighter]/'run.log').read_text()),
         'Every original native physical input/health/selection/move/boss/ending/guest/RGB event unchanged, not a new tower-clear claim')
    timeline=lambda hs:[{k:v for k,v in h.items() if k!='sha256'} for h in hs]
    need(timeline(headers)==timeline(old_headers) and a.shape==b.shape,'Every actual native audio update clock and stereo sample count equal')
    equal=bool(np.array_equal(a,b))
    inventories={tag:rows(text,tag)==rows(old,tag) for tag in ('WINDOW','BEGIN','WINNER','ATTRACT','FIELD','ROUTE','QUEUE','PACKET','SOUND','DELIVERY','CHANNEL','RESULT')}
    meta=json.loads((folder/'result.json').read_text());base_meta=json.loads((baseline/'result.json').read_text())
    need(meta['exit_code']==base_meta['exit_code']==0,'Both new sound observations actually terminal')
    pins={str(references[fighter]/'run.log'):sha(references[fighter]/'run.log')}
    for leaf in (folder,baseline):
        result=json.loads((leaf/'result.json').read_text())
        for p,h in result['input_hashes'].items():need(p not in pins or pins[p]==h,'Identical immutable actual paired inputs');pins[p]=h
        for p in leaf.rglob('*'):
            if p.is_file():pins[str(p)]=sha(p)
    return dict(fighter=fighter,physicalSlot=2,capture=str(folder),baseline=str(baseline),
                actualNativePCMExactlyEqual=equal,nativeInventoriesEqual=inventories,
                differingStereoFrames=int(np.count_nonzero(np.any(a!=b,axis=1))),
                fullNativePCMFrames=len(a),actualNativePCMUpdates=len(headers),
                actualNativePCMSHA256=meta['mixedPCMSHA256'],actualBaselinePCMSHA256=base_meta['mixedPCMSHA256'],
                nonzeroNativePCMSamples=int(np.count_nonzero(a)),
                originalCompleteNativeCampaignAndGuestRGBEventsExactlyUnchanged=True,
                rawNativeAudioRasterVRAMROMFilesWritten=0,inputHashes=pins,
                independentStockDCSWaveformReferenceAccepted=False,fullEndingTransitionRasterAccepted=False,fullPortAcceptance=False)

def main():
    need(not OUT.exists(),'Fresh immutable new ending audio observation')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        cases=list(pool.map(pair,('kano','sonya')))
    need(all(all(c['nativeInventoriesEqual'].values()) for c in cases),'Every complete native sound/state inventory exactly equals paired baseline')
    need(all(c['actualNativePCMExactlyEqual'] and c['nonzeroNativePCMSamples']>0 for c in cases),
         'Full actually non-silent native ending PCM has no phantom imported contribution')
    pins={str(Path(__file__).resolve()):sha(__file__)}
    for case in cases:
        for p,h in case['inputHashes'].items():need(p not in pins or pins[p]==h,'All original shared inputs consistent');pins[p]=h
    need(all(sha(p)==h for p,h in pins.items()),'Every actual input/source/proof byte unchanged')
    return dict(passed=True,candidate=NAME,cases=cases,inputHashes=pins,actualPairedCaptures=4,
                newEndingNativePCMWindowObservationsAccepted=True,independentStockDCSWaveformReferenceAccepted=False,
                allEndingAudioFidelityAccepted=False,fullEndingTransitionRasterAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=main()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable new observation report');OUT.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed proof before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes','cases')},indent=2),flush=True)
    if report['passed']:print(json.dumps([{k:v for k,v in c.items() if k!='inputHashes'} for c in report['cases']],indent=2),flush=True)
    raise SystemExit(0 if report['passed'] else 1)
