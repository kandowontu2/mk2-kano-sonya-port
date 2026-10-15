"""Native cue ownership/timing/voice holds only; NOT audible output proof."""
import json
from qualify_bounded_current_friendships import fields, validate
import verify_native_source_sync as sync

sync.verify()
out=sync.ROOT/'audit_bounded_friendship_audio_dispatch_checked'
assert not out.exists()
reports=[]
for fighter in ('kano','sonya'):
    for side in (1,2):
        case=sync.ROOT/f'audit_bounded_friendship_audio_dispatch_{fighter}_p{side}_runtime'
        terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert terminal['peakWorkingSetBytes']<=320*1024**2
        assert not (case/'stderr.log').read_text().strip()
        text=(case/'run.log').read_text()
        controller='\n'.join(line for line in text.splitlines() if not line.startswith(('MK2_FRIEND_AUDIO','MK2_FRIEND_VOICE')))
        result=validate(controller,fighter,side)
        baseline=(sync.ROOT/f'audit_bounded_current_friendship_{fighter}_p{side}_runtime/run.log').read_text()
        assert [line for line in controller.splitlines() if line.startswith('MK2_FRIEND_')]==[line for line in baseline.splitlines() if line.startswith('MK2_FRIEND_')]
        cues=[fields(line) for line in text.splitlines() if line.startswith('MK2_FRIEND_AUDIO')]
        poses=[fields(line) for line in controller.splitlines() if line.startswith('MK2_FRIEND_POSE')]
        actor,main=poses[0]['actor'],poses[0]['main']
        own=17 if fighter=='kano' else 18
        assert cues and all(int(c['id'])==own and c['actor']==actor and c['main']==main and c['writes']=='0' for c in cues)
        action=int(result['action'])
        voices=[];variants=[]
        if fighter=='kano':
            assert len(cues)==1 and cues[0]['command']=='6AB4' and int(cues[0]['frame'])-action==183
            assert cues[0]['pose']=='FE9D2590'
        else:
            tail=[p for p in poses if int(p['age'])>=83]
            expected=[int(p['frame']) for i,p in enumerate(tail) if i%14 in (2,4,6)]
            assert [int(c['frame']) for c in cues]==expected and len(cues)>=9
            timers=[0]*5;last=action
            for c in cues:
                frame=int(c['frame']);timers=[max(0,t-(frame-last)) for t in timers];last=frame
                command=int(c['command'],16)
                assert 0x6aa0<=command<=0x6ab3
                variant,voice=divmod(command-0x6aa0,5)
                assert voice==timers.index(0)
                timers[voice]=(16,23,20,18)[variant]
                assert [int(n) for n in c['timers'].split(',')]==timers
                voices.append(voice);variants.append(variant)
            assert max(voices)>=2
        reports.append({'fighter':fighter,'side':side,'cueCount':len(cues),'variants':variants,'voices':voices,'logSha256':sync.sha(case/'run.log'),'terminal':terminal})
out.mkdir()
(out/'report.json').write_text(json.dumps({'nativeDispatchPassed':True,'audibleWaveformAcceptance':False,'releaseAcceptance':False,'cases':reports},indent=2))
print('PASS: current native pop/cluck timing, true ownership and overlapping first-free voices; audible output unverified')
