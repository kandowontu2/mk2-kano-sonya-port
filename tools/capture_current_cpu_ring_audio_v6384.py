"""Same current native full-hit Ring trajectory, complete RAM-only audio.

Preserve6213's entire terminal-first native transport and DAC/ROM fault gates.
Keep original5779 observers and5789 native float32/resampler/source-winner
prediction; no fits, raw files, guest writes, forced moves or build copies.
"""
import argparse,code,gzip,inspect,json,re,sys,traceback
from pathlib import Path
import capture_current_subzero_audio_v6213 as original
import capture_current_cpu_ring_render_v6377 as physical
import current_tomb_winner_mix_fault_model_v5789 as mix
import capture_current_cmd_specials_v6261 as process_tools
ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_v6385_current_cpu_ring_audio_ram'
PARENT=ROOT/'audit_v6382_current_cpu_ring_render_checked/report.json'
SCOPE_PARENT=ROOT/'audit_v6311_current_kano_cpu_blade_knife_checked/report.json'
LUA='mk2ks_current_cpu_ring_audio_v6383.lua'
CHAIN=(LUA,'mk2ks_current_cpu_ring_render_ram_v6375.lua','mk2ks_native_tomb_ram_v3624.lua',
 *physical.CHAIN[:4],'mk2ks_current_tomb_winner_mix_observer_v5779.lua')
SCOPE=None


def state(text,fighter,side,guest):
 need(fighter=='sonya' and side==2,'Actual native Sonya CPU, physical slot2')
 with gzip.open(physical.FOLDER/'run.log.gz','rt',encoding='utf-8')as file:reference=file.read()
 prefixes=('MK2_CPU_PAIR_','MK2_P2CPU_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_','MK2_RING_PAIR_')
 rows=lambda value:[s for s in value.splitlines()if s.startswith(prefixes)]
 need(rows(text)==rows(reference),'Entire original physical/AI/RNG/HP/state/child/guard chronology unchanged')
 result=physical.full_phase(text,guest)
 marks=mix.rows(text,'MK2_MAUDIO_BEGIN');ends=mix.rows(text,'MK2_MAUDIO_RESULT')
 timeline=result['ring']['acceptedRings'][0]
 need(len(marks)==len(ends)==1 and marks[0]['frame']==marks[0]['origin']==str(timeline['start'])=='2077' and
      marks[0]['id']=='18' and ends[0]['frame']=='3623' and ends[0]['origin']=='2077',
      'Actual true CPU Ring origin and unchanged complete physical terminal')
 channels=mix.rows(text,'MK2_MAUDIO_CHANNEL')
 need(len(channels)==639*14 and {(int(r['frame']),int(r['channel']))for r in channels}==
      {(f,c)for f in range(2078,2717)for c in range(14)},'All14 native channels at every complete observed video field')
 for row in channels:
  need(row['writes']==row['loop']==row['paused']=='0','Passive unpaused nonlooping native channels')
  if row['channel']!='0':need(row['length']=='0' and float(row['pos'])==0,'No unmodeled imported audio source')
 need(all(r['sample']=='4294967295' and float(r['pos'])>=int(r['length'])for r in channels if r['frame']=='2716'),
      'Every imported source retired; native completed length/position retained')
 pcm=mix.rows(text,'MK2_BBAUDIO_PCM_DIGEST')
 need(pcm and all(r['bytes']=='3840' and 2077<=int(r['frame'])<=2716 for r in pcm) and
      int(pcm[0]['frame'])<=2078 and int(pcm[-1]['frame'])>=2715 and
      all(abs(float(b['seconds'])-float(a['seconds'])-.02)<1e-9 for a,b in zip(pcm,pcm[1:])),
      'Entire consecutive50Hz sound window, no first/last callback or tail trimming')
 return dict(fullOriginalPhaseContract=result,wholeOriginalTrajectoryRows=len(rows(text)),
             nativeAudioOrigin=marks[0],nativeAudioTerminal=ends[0],channelRows=len(channels),completePCMCallbacks=len(pcm))


def dac_models(callbacks):
 need(500<callbacks<650,'Whole original639-field Ring audio window')
 source=inspect.getsource(original.dac_models).replace('1600<callbacks<2100','500<callbacks<650',1)
 scope=dict(original.dac_models.__globals__)
 exec(compile(source,__file__+'::whole_native_DAC_ring_window','exec'),scope)
 return scope['dac_models'](callbacks)


def prepare():
 source=inspect.getsource(original.run)
 def replace(before,after):
  nonlocal source
  need(source.count(before)==1,'One complete original collector adaptation '+before[:65])
  source=source.replace(before,after,1)
 replace('audit_v6214_current_subzero_{fighter}_p{side}_native_audio','audit_v6385_current_cpu_ring_audio_ram')
 replace('gfx=current.expected_gfx()',"gfx=b''")
 replace("parent=json.loads(PARENT.read_text());need(parent['passed']and len(parent['remaining'])==5,'Full current scope preserved')",
         "parent=json.loads(PARENT.read_text());full_scope=json.loads(SCOPE_PARENT.read_text());need(parent['passed']and full_scope['passed']and len(full_scope['remaining'])==5,'Full current scope preserved');remaining=full_scope['remaining']")
 first=source.index(' files=[ROOT/leaf for leaf in (LUA,');last=source.index(' controller=',first)
 source=source[:first]+' files=[ROOT/leaf for leaf in CHAIN]\n'+source[last:]
 replace('Path(__file__),Path(current.__file__),Path(model.__file__),',
         'Path(__file__),Path(original.__file__),Path(physical.__file__),Path(mix.__file__),SCOPE_PARENT,Path(current.__file__),Path(model.__file__),')
 replace('expected,_=model.expected_region(pins)',
         "expected,_=model.expected_region(pins)\n for module in tuple(sys.modules.values()):\n  file=getattr(module,'__file__',None)\n  if file and Path(file).resolve().is_relative_to(ROOT/'tools'):pins[str(Path(file).resolve())]=sha(file)\n pins[str(physical.FOLDER/'run.log.gz')]=sha(physical.FOLDER/'run.log.gz')")
 replace("env.update(MK2KS_TEST_FIGHTER=fighter,MK2KS_CAMPAIGN_SIDE=str(side),MK2KS_STOCK_KILLER='subzero',\n            MK2KS_STOCK_COMMAND='ffd_hk',MK2KS_STOCK_GAP='168')",
         "env.update(MK2KS_TEST_FIGHTER='kano',MK2KS_TEST_BOOT_FRAME='613',MK2KS_CPU_PAIR_CONFIRM_AGE='264',MK2KS_CPU_PAIR_APPROACH='original',MK2KS_CPU_CONTINUATION_POLICY='retreat')")
 replace("'-nosamples'","'-samples'");replace("'-str','130'","'-snapsize','400x254','-str','95'")
 replace("('MK2_MAUDIO_GUEST','MK2_EARNED_SUBZERO_GUEST')","('MK2_MAUDIO_GUEST','MK2_KNIFE_RAM_GUEST')")
 replace("tag=='MK2_EARNED_SUBZERO_RGB'","tag=='MK2_KNIFE_RAM_RGB'")
 replace("need(seen_guest==2 and seen_gfx==1 and len(raw_proofs)==4,'Whole driver plus audio guest and four native transitions')",
         "need(seen_guest==2 and seen_gfx==0 and len(raw_proofs)==104,'Whole physical/audio guest and all104 original native scene callbacks')")
 # Immediately retain the fully drained native RAM carrier, even if any later
 # host state/predictor fails. A failure never requires another native replay.
 replace("with gzip.open(folder/'run.log.gz','rt')as reader:text=reader.read()",
         "with gzip.open(folder/'run.log.gz','rt')as reader:text=reader.read()\n globals()['LAST_CAPTURE']=dict(locals())")
 first=source.index(" rows=[dict(fields(line),tag=line.split()[0])");last=source.index(' gate,fault,gate_sha=',first)
 source=source[:first]+" native=state(text,fighter,side,guest)\n end=[native]\n"+source[last:]
 replace('waveform=model.predict_waveform(dac_chunks,dac_headers,pcm)',
         "waveform=mix.predict_mix(dac_chunks,dac_headers,pcm,text,fighter,pins)")
 replace("remaining=parent['remaining']","remaining=remaining")
 replace('nativeNextCPUMatch=end[0]','nativeCPUFullRingHitSequence=end[0]')
 replace('nativeDCSWaveformAccepted=True,samplesEnabled=False,importedVictimMixAccepted=False,',
         'nativeDCSWaveformAccepted=True,samplesEnabled=True,importedVictimMixAccepted=False,sourceWinnerMixAccepted=True,')
 scope=dict(original.run.__globals__,__file__=__file__,original=original,physical=physical,mix=mix,sys=sys,
            LUA=LUA,PARENT=PARENT,SCOPE_PARENT=SCOPE_PARENT,CHAIN=CHAIN,state=state,dac_models=dac_models)
 exec(compile(source,__file__+'::whole6213_terminal_first_current_CPU_ring_audio','exec'),scope)
 return scope


def main(preflight=False):
 global SCOPE
 parent=json.loads(PARENT.read_text())
 need(parent['passed'] and all(sha(p)==h for p,h in parent['inputHashes'].items()),'Complete current Ring renderer proof unchanged')
 need(not OUT.exists() and not process_tools.census(),'Fresh job, empty actual native process census')
 SCOPE=prepare()
 if preflight:
  with gzip.open(physical.FOLDER/'run.log.gz','rt',encoding='utf-8')as file:text=file.read()
  result=physical.full_phase(text,original.current.expected())
  need(result['ring']['acceptedRings'][0]==parent['phase'],'Source guest and exact already qualified full-hit Ring phase')
  print(json.dumps(dict(preflightPassed=True,nativeBoots=0,wholeCollectorCompiled=True)),flush=True);return
 return SCOPE['run']('sonya',2)


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');parser.add_argument('--hold',action='store_true');args=parser.parse_args()
 try:main(args.preflight)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if OUT.exists():original.save(OUT/'failure.json',failure)
  print(json.dumps(failure,indent=2),flush=True)
  if args.hold and SCOPE and 'LAST_CAPTURE'in SCOPE:
   code.interact(banner='Same native process terminal; actual PCM/DAC retained in RAM, no native rerun.',
                local=dict(capture=SCOPE['LAST_CAPTURE'],module=__import__(__name__),mix=mix))
  raise SystemExit(1)
