"""Native ground-damage/actual-input partition, never attack causality."""
import collections,json,subprocess
from pathlib import Path
import verify_shang_jump_retry_prefix_v4306 as native
ROOT,need,sha=native.ROOT,native.need,native.sha
OUT=ROOT/'audit_v4423_sonya_kintaro_ground_damage'

def main():
    need(not OUT.exists(),'Fresh actual native ground-damage evidence')
    proofpath=ROOT/'audit_v4309_shang_jump_retry_whole_campaign_checked/report.json'
    proof=json.loads(proofpath.read_text());need(proof['passed'] and proof['case']['passed'] and
      proof['case']['actualWholeCampaignGrammarRetained'],'Original full native campaign required')
    rows=native.parse((native.FOLDER/'run.log').read_text())
    fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD' and r['stage']=='15'}
    inputs=collections.defaultdict(list)
    for r in rows:
        if r['tag']=='INPUT':inputs[r['frame']].append(r['button'])
    damage=[];by_input=collections.Counter();by_stance=collections.Counter();by_cpu=collections.Counter()
    for r in rows:
        if r['tag']!='HEALTH' or r['slot']!='2' or r['frame'] not in fields or int(r['before'])<=int(r['after']):continue
        f=fields[r['frame']]
        need(r['pc']=='FF836700' and r['at']=='01060EC0' and 0<=int(r['after'])<int(r['before'])<=161 and
          f['human_id']=='18' and f['cpu_id']=='12' and f['writes']=='0' and f['assistance']=='none',
          'Actual original collision health store, native Sonya18/Kintaro12')
        amount=int(r['before'])-int(r['after']);ground=int(f['height'])<=8
        if ground:
            keys=tuple(inputs[r['frame']]);by_input[','.join(keys) or 'none']+=amount
            by_stance[f['human_action']]+=amount;by_cpu[f['cpu_action']]+=amount
        damage.append(dict(frame=r['frame'],healthBefore=int(r['before']),healthAfter=int(r['after']),damage=amount,
          sampledGrounded=ground,sameFieldActualButtons=inputs[r['frame']],sampledHumanAction=int(f['human_action']),
          sampledCPUAction=int(f['cpu_action']),sampledGap=int(f['gap']),nativeHealthStore=r,
          sampledFlags=f['flags'],sampledBody=f['body']))
    need(damage and by_input,'Actual ground damage events, not a guessed control weakness')
    guarded=[f for f in fields.values() if 'Block' in inputs[f['frame']]]
    sampled_blocks=[f for f in fields.values() if int(f['human_action']) in (0x700,0x701)]
    paths=[Path(__file__).resolve(),Path(native.__file__).resolve(),proofpath,native.FOLDER/'run.log',native.FOLDER/'result.json']
    return dict(passed=True,actualHumanCollisionDamageEvents=damage,
      sampledGroundedDamage=sum(r['damage'] for r in damage if r['sampledGrounded']),
      sampledAirborneDamage=sum(r['damage'] for r in damage if not r['sampledGrounded']),
      groundDamageByActualSameFieldInput=dict(by_input),groundDamageBySampledHumanAction=dict(by_stance),
      groundDamageBySampledCPUAction=dict(by_cpu),actualBlockInputFields=len(guarded),
      sampledNativeBlockActionFields=len(sampled_blocks),
      sampledNativeBlockBodies=dict(collections.Counter(f['body'] for f in sampled_blocks)),
      inputAndSampledActionsNotCausalAttackAttribution=True,alternativeGuardPolicyExercised=False,
      naturalTowerClearAccepted=False,nativeFloorShadowArtAudioAccepted=False,fullPortAcceptance=False,
      inputHashes={str(p):sha(p) for p in paths},scope=__doc__)

if __name__=='__main__':
    report=main();OUT.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('actualHumanCollisionDamageEvents','inputHashes')},indent=2),flush=True)
