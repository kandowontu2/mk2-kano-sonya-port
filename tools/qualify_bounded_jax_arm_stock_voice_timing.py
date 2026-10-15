"""Genuine stock Kitana confirms the same slot-dependent arm voice timestamp."""
import inspect,json,re
from pathlib import Path
import qualify_bounded_jax_clap_finisher as p1
import qualify_bounded_p2_jax_clap_control as p2
from qualify_bounded_jax_arms_draw_census import states
import verify_native_source_sync as sync

def main():
    out=sync.ROOT/'audit_bounded_jax_arm_stock_voice_timing_checked';assert not out.exists();results={}
    for side in (1,2):
        folder=sync.ROOT/f'audit_bounded_stock_kitana_p{side}_jax_arm_voice_runtime'
        terminal=json.loads((folder/'terminal.json').read_text());assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
        rows=states(folder,'kitana',side)
        source=inspect.getsource(p1.gate) if side==1 else p2.source
        source=source.replace("a['address']=='FF8C7820' and a['variant']=='1'","a['address']=='FF8BE240' and a['variant']=='2'")
        if side==2:source=source.replace("int(w['frame'])-int(a['frame'])==188","int(w['frame'])-int(a['frame'])==147")
        namespace={};exec(compile(source,__file__+'::stock_reference_control','exec'),namespace)
        physical=namespace['gate'](rows,4) if side==1 else namespace['gate'](rows,[],4)
        action=next(r for tag,r in rows if tag=='ACTION');wrap=next(r for tag,r in rows if tag=='WRAP')
        assert int(wrap['frame'])-int(action['frame'])==147
        branches=[]
        with (folder/'run.log').open() as stream:
            for line in stream:
                if line.startswith('MK2_FINISHER_AUDIO_BRANCH '):branches.append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
        assert len(branches)==1;b=branches[0];age=103+side
        assert int(b['age'])==age and int(b['frame'])==int(action['frame'])+age
        assert b['victim_id']=='4' and b['a2']=='00000004' and b['hp']=='0' and b['route']=='female' and b['pc']=='FFA123C0'
        assert b['a8']==b['victim_actor']==action['victim_actor'] and b['a13']==b['victim_main']==action['victim_main']
        added_name='audit_bounded_jax_arms_voice_priority_p1_checked' if side==1 else 'audit_bounded_p2_jax_arms_voice_observed_checked'
        added_path=sync.ROOT/added_name/'report.json';added=json.loads(added_path.read_text());assert added['passed']
        for fighter in ('sonya','kano'):
            runtime=sync.ROOT/f'audit_bounded_{fighter}_p{side}_jax_arms_voice_priority_runtime'
            assert sync.sha(runtime/'run.log')==added['results'][fighter]['logSha256'] and added['results'][fighter]['voiceAge']==age
        results[f'P{side}']=dict(actualStockVictim='kitana',trueID=4,stockReferenceOnly=True,stockVoiceAge=age,addedVoiceAgesMatch=True,physical=physical,branch=b,terminal=terminal,logSha256=sync.sha(folder/'run.log'),addedProofSha256=sync.sha(added_path))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),finiteSlotVoiceTimingParityAccepted=True,allTimingContextsAccepted=False,heardAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,stockVoiceAges={key:r['stockVoiceAge'] for key,r in results.items()},addedVoiceAgesMatch=True)))

if __name__=='__main__':main()
