"""Actual stock controls and finite timing variation, not universal parity."""
import inspect,json,re
from pathlib import Path
import qualify_bounded_jax_clap_finisher as p1
import qualify_bounded_p2_jax_clap_control as p2
from qualify_bounded_stock_head_body_footprints import PREFIX
import verify_native_source_sync as sync

def main():
    out=sync.ROOT/'audit_bounded_stock_kiss_timing_checked';assert not out.exists()
    added_path=sync.ROOT/'audit_bounded_kitana_kiss_voice_choice_checked/report.json'
    added=json.loads(added_path.read_text());assert added['passed'];results={}
    for side in (1,2):
        for fighter,ident in [('kitana',4),('liu_kang',1)]:
            folder=sync.ROOT/f'audit_bounded_stock_{fighter}_p{side}_kiss_voice_runtime'
            t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None
            assert not (folder/'stderr.log').read_text().strip();rows=[];branches=[];cues=[]
            with (folder/'run.log').open() as stream:
                for line in stream:
                    assert '[LUA ERROR]' not in line
                    r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                    if line.startswith('MK2_STOCK_HEAD_V921_'):
                        m=PREFIX.match(line);assert m and (m[3],m[4],m[5],m[6],m[7])==(fighter,str(side),'kitana','0','none')
                        rows.append((m[1],r))
                    elif line.startswith('MK2_FINISHER_AUDIO_BRANCH '):branches.append(r)
                    elif line.startswith('MK2_VOICE_SELECTOR_CUE '):cues.append(r)
            source=inspect.getsource(p1.gate) if side==1 else p2.source
            assert source.count("a['address']=='FF8C7820'")==1
            source=source.replace("a['address']=='FF8C7820'","a['address']=='FF8CC650'")
            assert source.count("x['own'].split(':')[-1]=='11'")==1
            source=source.replace("x['own'].split(':')[-1]=='11'","x['own'].split(':')[-1]=='4'")
            if side==2:source=source.replace("int(w['frame'])-int(a['frame'])==188","int(w['frame'])-int(a['frame'])==276")
            namespace={};exec(compile(source,__file__+'::earned_stock_control','exec'),namespace)
            physical=namespace['gate'](rows,ident) if side==1 else namespace['gate'](rows,[],ident)
            a=next(r for tag,r in rows if tag=='ACTION');w=next(r for tag,r in rows if tag=='WRAP')
            assert len(branches)==1;b=branches[0]
            age=188 if fighter=='kitana' and side==1 else 179+side
            assert int(b['age'])==age and int(b['frame'])==int(a['frame'])+age
            assert int(b['victim_id'])==int(b['a2'],16)==ident and b['hp']=='0'
            assert b['a8']==b['victim_actor']==a['victim_actor'] and b['a13']==b['victim_main']==a['victim_main']
            assert b['route']==('female' if ident==4 else 'male')
            assert b['pc']==('FFA123C0' if ident==4 else 'FFA122E0')
            effect=[r for r in cues if r['cue'] in ('A3','A5','A4')]
            assert [r['cue'] for r in effect]==['A3','A5','A4']
            offsets=[int(r['frame'])-int(b['frame']) for r in effect];assert offsets==[32,32,172]
            assert int(w['frame'])-int(b['frame'])==(96 if side==1 else 95)
            for added_fighter in ('sonya','kano'):
                key=f'{added_fighter}P{side}'
                path=sync.ROOT/f'audit_bounded_{added_fighter}_p{side}_kitana_kiss_voice_priority_runtime/run.log'
                assert sync.sha(path)==added['results'][key]['logSha256']
                assert added['results'][key]['voiceAge']==179+side
            results[f'{fighter}P{side}']=dict(actualStockVictim=fighter,trueID=ident,stockReferenceOnly=True,
                physical=physical,voiceAge=age,wrapAge=int(w['frame'])-int(a['frame']),
                effectOffsetsAfterVoice=offsets,addedVoiceAgeDelta=age-(179+side),terminal=t,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        addedProofSha256=sync.sha(added_path),finiteStockLiuSlotTimingParityAccepted=True,
        universalStockTimingParityAccepted=False,stockKitanaP1EightFieldVariationObserved=True,
        variationCauseVerified=False,heardAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,cases={k:{a:r[a] for a in ('voiceAge','wrapAge','addedVoiceAgeDelta')} for k,r in results.items()})))

if __name__=='__main__':main()
