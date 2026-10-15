"""Before-boot unchanged native controls and complete read-only render extension."""
import ast,hashlib,json,re,subprocess
from pathlib import Path
import check_scorpion_secondary_source_v4550 as original
ROOT,need,sha,NAME,current=original.ROOT,original.need,original.sha,original.NAME,original.current
OUT=ROOT/'audit_v4567_scorpion_secondary_scene_source_checked'
LUA='mk2ks_scorpion_secondary_native_scene_ram_v4558.lua'
CONTROL=original.CONTROL
PAIRS=[
 ("dofile('mk2ks_stock_extended_earned_ram_v3958.lua')","dofile('mk2ks_scorpion_secondary_state_ram_v4534.lua')"),
 ("local move='jax_arms'","local move='scorpion_secondary'"),
 ('local action_entry=0xff8be240','local action_entry=0xff8bbfe0'),
 ('a.id==11 and victim.id==identity','a.id==10 and victim.id==identity'),
 ('MK2_JAX_ARMS_NATIVE_SCENE_WRAPPER','MK2_SCORPION_SECONDARY_NATIVE_SCENE_WRAPPER'),
 ('@mk2ks_native_tomb_display_v2062_Jax_arms_window_RAM_sinks','@mk2ks_native_tomb_display_v2062_Scorpion_secondary_window_RAM_sinks')]
TOKEN=r'''"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*' '''.strip()

def observer_source(text):
    actions=[tuple(ast.literal_eval(t) for t in m.groups()) for m in
             re.finditer(r'\bonce\(\s*('+TOKEN+r')\s*,\s*('+TOKEN+r')\s*\)',text)]
    need(actions==PAIRS,'Exactly six declared original Scorpion-role substitutions; no control policy changes')
    source=(ROOT/'mk2ks_jax_arms_native_scene_ram_v4073.lua').read_text()
    for before,after in actions:
        need(source.count(before)==1,'Unique whole original role boundary');source=source.replace(before,after,1)
    need(not re.search(r':write_\w+\s*\(|write_u\d+\s*\(|\.value\s*=(?!=)|load_?state|set_value|clear_value|return\s+data',text+source),
         'No guest/register/identity/AI/health/palette/RNG/position writes or invented positive events')
    need("dofile('mk2ks_scorpion_secondary_state_ram_v4534.lua')"in source and
         'cpu.PC.value==address+16' in source and 'a.id==10 and victim.id==identity' in source and
         'a.owner==a.actor and victim.owner==victim.actor' in source and
         "p:read_u16(side==1 and 0x010602f0 or 0x01060ec0)==0"in source,
         'Actual owned native Scorpion10 activation and true physical defeated victim')
    return source

def source_boundary():
    control=original.source_boundary();source=observer_source((ROOT/LUA).read_text())
    need(sha(ROOT/'mk2ks_jax_arms_native_scene_ram_v4073.lua')==
         json.loads((ROOT/'audit_v4557_secondary_state_video_full_scope_checkpoint/checkpoint.json').read_text())['inputHashes'][str(ROOT/'mk2ks_jax_arms_native_scene_ram_v4073.lua')],
         'Exact inherited entire original renderer wrapper unchanged')
    return dict(passed=True,originalNativeControlAndGuestProof=control,
      executedRoleWrapperSHA256=hashlib.sha256(source.encode()).hexdigest().upper(),
      nativeArtRendererOrAudioAccepted=False,fullPortAcceptance=False)

def main():
    need(not OUT.exists(),'Fresh before-boot scene proof')
    positive=source_boundary();actual=(ROOT/LUA).read_text();faults=[]
    for label,before,after in [('proxy_attacker','a.id==10 and victim.id==identity','a.id==1 and victim.id==identity'),
      ('wrong_native_action','local action_entry=0xff8bbfe0','local action_entry=0xff8bc000'),
      ('changed_controller','mk2ks_scorpion_secondary_state_ram_v4534.lua','mk2ks_stock_fatality_v1021.lua'),
      ('guest_write',"assert(not source:find(':write_',1,true))","p:write_u16(0x01060e50,1)\nassert(not source:find(':write_',1,true))")]:
        changed=actual.replace(before,after,1);need(changed!=actual,'Non-vacuous actual source fault')
        try:observer_source(changed)
        except ValueError as error:faults.append(dict(label=label,rejectedBy=str(error)))
        else:raise ValueError('Accepted source fault: '+label)
    observer_source(actual)
    import run_scorpion_secondary_native_scene_v4562 as capture
    generated=capture.collector();need('errors'in generated.__code__.co_varnames and 'scene_errors'in generated.__code__.co_varnames,
      'Original stderr handle and model error list are separate generated locals')
    files=[Path(__file__).resolve(),Path(capture.__file__),ROOT/LUA,ROOT/CONTROL,ROOT/original.LUA,
      Path(original.__file__),ROOT/'mk2ks_jax_arms_native_scene_ram_v4073.lua',ROOT/'mk2ks_arm_palette_trace_v1073.lua',
      ROOT/'mk2ks_native_tomb_display_v2062.lua',ROOT/'tools/scorpion_secondary_native_scene_model_v4559.py',
      ROOT/'tools/current_tomb_ram_model_v3642.py',ROOT/'tools/run_jax_arms_native_scene_v4074.py',
      ROOT/'audit_v4555_current_scorpion_secondary_state_checked/report.json']
    # Bind every local Python module actually imported for source/model/graphics.
    import sys
    for module in list(sys.modules.values()):
        path=getattr(module,'__file__',None)
        if path and Path(path).resolve().is_relative_to(ROOT/'tools'):files.append(Path(path).resolve())
    files=list(dict.fromkeys(files))
    for p in files:
        if p.suffix=='.py':ast.parse(p.read_text(),filename=str(p))
    report=dict(positive,actualSourceFaultsRejected=faults,
      generatedStderrAndSceneErrorLocalsDistinct=True,
      priorPreflightFailure=dict(source=str(ROOT/'tools/qualify_scorpion_secondary_scene_source_v4560.py'),
        nativeJobsLaunched=False,condition='The scanner matched the literal forbidden-token string in an existing assert, not a native write.',
        correction='Require an actual named write-call shape; the explicit inserted guest-write counterexample must still reject.'),
      inputHashes={str(p.resolve()):sha(p)for p in files})
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)

if __name__=='__main__':main()
