"""Current naturally chosen CPU blade/knife audio, RAM-only source prediction.

Keep the entire terminal-first6213 native collector. Scope only changes the
physical driver, passive observation window and enabled winner source mix.
The exact already-qualified chronology must match; no native state injection.
Retain RAM on a host failure with --hold, never restart an observed job.
"""
import argparse,code,gzip,inspect,json,sys,traceback
from pathlib import Path
import capture_current_subzero_audio_v6213 as original
import verify_current_cpu_blade_allocation_v6333 as phase
import current_tomb_winner_mix_fault_model_v5789 as mix
import capture_current_cmd_specials_v6261 as process_tools
ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_v6364_current_cpu_blade_knife_audio_ram'
PARENT=ROOT/'audit_v6359_current_cpu_effect_render_checked/report.json'
LUA='mk2ks_current_cpu_blade_knife_audio_v6362.lua'
SCOPE=None
CHAIN=(LUA,'mk2ks_current_cpu_blade_allocation_v6340.lua',
 'mk2ks_current_kano_cpu_extended_ram_v6290.lua','mk2ks_blade_allocation_v2892.lua',
 'mk2ks_physical_p2_cpu_continuation_v3300.lua','mk2ks_physical_p2_cpu_round_trace_v1940.lua',
 'mk2ks_physical_p2_cpu_overlap_trace_v1942.lua','mk2ks_physical_p2_cpu_knife_trace_v1955.lua',
 'mk2ks_physical_p2_cpu_choice_trace_v3303.lua','mk2ks_current_tomb_winner_mix_observer_v5779.lua')


def state(text,fighter,side,guest):
 need(fighter=='kano' and side==2,'Actual native CPU Kano physical slot, no substitute')
 with gzip.open(ROOT/'audit_v6342_current_cpu_blade_allocation_ram/run.log.gz','rt',encoding='utf-8')as file:reference=file.read()
 prefixes=('MK2_CPU_PAIR_','MK2_P2CPU_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_',
           'MK2_KNIFE_PAIR_','MK2_CPU_CHOICE_','MK2_BLADE_ALLOC_')
 rows=lambda value:[s for s in value.splitlines()if s.startswith(prefixes)]
 need(rows(text)==rows(reference),'Every original physical/AI/RNG/HP/state/pool row identical')
 result=phase.phase_gate()(text,guest)
 marks=mix.rows(text,'MK2_MAUDIO_BEGIN');ends=mix.rows(text,'MK2_MAUDIO_RESULT')
 need(len(marks)==len(ends)==1 and marks[0]['frame']==marks[0]['origin']=='1871' and
      marks[0]['id']=='17' and marks[0]['a8']=='010350A0' and marks[0]['a13']=='0106A370' and
      ends[0]['frame']=='3615' and ends[0]['origin']=='1871',
      'Actual owned CPU blade origin and full unchanged physical terminal')
 channels=mix.rows(text,'MK2_MAUDIO_CHANNEL')
 need(len(channels)==640*14 and len({(r['frame'],r['channel'])for r in channels})==640*14 and
      {int(r['frame'])for r in channels}==set(range(1871,2511)),
      'Every actual channel at every consecutive observed field')
 for row in channels:
  need(row['writes']==row['loop']==row['paused']=='0','Passive unpaused nonlooping original channels')
  if row['channel']!='0':need(row['length']=='0' and float(row['pos'])==0,'No unmodeled imported audio source')
 need(all(r['length']=='0'for r in channels if r['frame']=='2510'),
      'All imported channels inactive after knife cleanup')
 return dict(fullOriginalPhaseContract=result,wholeOriginalTrajectoryRows=len(rows(text)),
             nativeAudioOrigin=marks[0],nativeAudioTerminal=ends[0],channelRows=len(channels))


def dac_models(callbacks):
 source=inspect.getsource(original.dac_models)
 need(source.count('1600<callbacks<2100')==1,'Only native observation-duration admission changes')
 source=source.replace('1600<callbacks<2100','500<callbacks<650',1)
 scope=dict(original.dac_models.__globals__)
 exec(compile(source,__file__+'::whole_native_DAC_CPU_window','exec'),scope)
 return scope['dac_models'](callbacks)


def prepare():
 source=inspect.getsource(original.run)
 def replace(before,after):
  nonlocal source
  need(source.count(before)==1,'One complete original collector adaptation '+before[:65])
  source=source.replace(before,after,1)
 replace('audit_v6214_current_subzero_{fighter}_p{side}_native_audio','audit_v6364_current_cpu_blade_knife_audio_ram')
 replace('gfx=current.expected_gfx()',"gfx=b''")
 first=source.index(' files=[ROOT/leaf for leaf in (LUA,');last=source.index(' controller=',first)
 source=source[:first]+' files=[ROOT/leaf for leaf in CHAIN]\n'+source[last:]
 replace('Path(__file__),Path(current.__file__),Path(model.__file__),',
         'Path(__file__),Path(original.__file__),Path(phase.__file__),Path(mix.__file__),Path(current.__file__),Path(model.__file__),')
 replace('expected,_=model.expected_region(pins)',
         "expected,_=model.expected_region(pins)\n for module in tuple(sys.modules.values()):\n  file=getattr(module,'__file__',None)\n  if file and Path(file).resolve().is_relative_to(ROOT/'tools'):pins[str(Path(file).resolve())]=sha(file)\n pins[str(ROOT/'audit_v6342_current_cpu_blade_allocation_ram/run.log.gz')]=sha(ROOT/'audit_v6342_current_cpu_blade_allocation_ram/run.log.gz')")
 replace("env.update(MK2KS_TEST_FIGHTER=fighter,MK2KS_CAMPAIGN_SIDE=str(side),MK2KS_STOCK_KILLER='subzero',\n            MK2KS_STOCK_COMMAND='ffd_hk',MK2KS_STOCK_GAP='168')",
         "env.update(MK2KS_TEST_FIGHTER='kano',MK2KS_TEST_BOOT_FRAME='605',MK2KS_CPU_PAIR_CONFIRM_AGE='265',MK2KS_CPU_PAIR_APPROACH='guard_until_close',MK2KS_CPU_CONTINUATION_POLICY='retreat')")
 replace("'-nosamples'","'-samples'")
 replace("'-str','130'","'-str','95'")
 replace("('MK2_MAUDIO_GUEST','MK2_EARNED_SUBZERO_GUEST')","('MK2_MAUDIO_GUEST','MK2_KNIFE_RAM_GUEST')")
 replace("tag=='MK2_EARNED_SUBZERO_RGB'","tag=='MK2_KNIFE_RAM_RGB'")
 replace("need(seen_guest==2 and seen_gfx==1 and len(raw_proofs)==4,'Whole driver plus audio guest and four native transitions')",
         "need(seen_guest==2 and seen_gfx==0 and len(raw_proofs)==42,'Whole original physical/audio guest and unchanged hashed scene callbacks')")
 first=source.index(" rows=[dict(fields(line),tag=line.split()[0])");last=source.index(' gate,fault,gate_sha=',first)
 source=source[:first]+" native=state(text,fighter,side,guest)\n end=[native]\n"+source[last:]
 replace('waveform=model.predict_waveform(dac_chunks,dac_headers,pcm)',
         "globals()['LAST_CAPTURE']=dict(locals())\n waveform=mix.predict_mix(dac_chunks,dac_headers,pcm,text,fighter,pins)")
 replace('nativeNextCPUMatch=end[0]','nativeCPUBladeKnifeSequence=end[0]')
 replace('nativeDCSWaveformAccepted=True,samplesEnabled=False,importedVictimMixAccepted=False,',
         'nativeDCSWaveformAccepted=True,samplesEnabled=True,importedVictimMixAccepted=False,sourceWinnerMixAccepted=True,')
 replace("('passed','fighter','physicalSlot','comparedStereoFrames','nativeDCSWaveformAccepted','samplesEnabled','fullPortAcceptance')",
         "('passed','fighter','physicalSlot','comparedStereoFrames','nativeDCSWaveformAccepted','sourceWinnerMixAccepted','samplesEnabled','fullPortAcceptance')")
 scope=dict(original.run.__globals__,__file__=__file__,original=original,phase=phase,mix=mix,sys=sys,
            LUA=LUA,PARENT=PARENT,CHAIN=CHAIN,state=state,dac_models=dac_models)
 exec(compile(source,__file__+'::whole6213_current_CPU_blade_knife_audio','exec'),scope)
 return scope


def main(preflight=False):
 global SCOPE
 parent=json.loads(PARENT.read_text())
 need(parent['passed'] and all(sha(p)==h for p,h in parent['inputHashes'].items()),'Current complete renderer qualification unchanged')
 need(not OUT.exists(),'No overwrite or relaunch of actual audio job')
 need(not process_tools.census(),'Actual native emulator process census empty')
 SCOPE=prepare()
 if preflight:
  print(json.dumps(dict(preflightPassed=True,nativeBoots=0,wholeCollectorCompiled=True)),flush=True);return
 return SCOPE['run']('kano',2)


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');parser.add_argument('--hold',action='store_true');args=parser.parse_args()
 try:main(args.preflight)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if OUT.exists():original.save(OUT/'failure.json',failure)
  print(json.dumps(failure,indent=2),flush=True)
  if args.hold and SCOPE and 'LAST_CAPTURE'in SCOPE:
   code.interact(banner='Native terminal; actual PCM/DAC retained in RAM, no native rerun.',
                local=dict(capture=SCOPE['LAST_CAPTURE'],module=__import__(__name__),mix=mix))
  raise SystemExit(1)
