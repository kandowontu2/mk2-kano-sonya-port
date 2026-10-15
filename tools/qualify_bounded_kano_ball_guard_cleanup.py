"""Reuse full retirement predicates for actual Kano hit and slot clocks."""
import inspect,json,re,copy
from pathlib import Path
import verify_native_source_sync as sync
import qualify_bounded_twohuman_square_rise_cleanup as previous

def main():
    gate=inspect.getsource(previous.gate)
    gate=gate.replace('def gate(rows,side,length):','def gate(rows,side,length):\n    stopped=2318 if side==1 else 2319')
    for before,after in {
        "('18' if int(r['slot'])==side else '17')":"('17' if int(r['slot'])==side else '18')",
        "cues[0]['value']=='6B00'":"cues[0]['value']=='6B03'",
        "'1381'":"'1459'","'1387'":"'1461'",'>=1388':'>=1462','<1388':'<1462',
        "hits=rows['HEALTH']":"hits=[r for r in rows['HEALTH'] if int(r['slot'])==side]",
        "r['id']=='18'":"r['id']=='17'","r['pos']=='5464.00000000'":"Decimal(r['pos'])==stopped",
        '0<5464<length':'0<stopped<length','stoppedSample=5464,unplayedSamples=length-5464':'stoppedSample=stopped,unplayedSamples=length-stopped',
        "Decimal(h['seconds'])+Decimal('1.5')":"Decimal(cues[0]['seconds'])+Decimal(length)/48000",
    }.items():
        assert before in gate;gate=gate.replace(before,after)
    namespace=dict(previous.__dict__);exec(compile(gate,__file__+'::kano_retirement','exec'),namespace)
    out=sync.ROOT/'audit_bounded_kano_ball_guard_cleanup_checked';assert not out.exists();results={}
    for side in (1,2):
        folder=sync.ROOT/f'audit_bounded_kano_ball_p{side}_guard_counter_runtime'
        t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip();rows={}
        with (folder/'run.log').open() as stream:
            for line in stream:
                assert '[LUA ERROR]' not in line
                if line.startswith('MK2_HSPECIAL_'):
                    tag=line.split(' ',1)[0].removeprefix('MK2_HSPECIAL_');r=dict(re.findall(r'(\w+)=([^\s]+)',line));rows.setdefault(tag,[]).append(r)
                    assert r['writes']=='0' and r['assistance']=='none'
        assert len(rows['HEALTH'])==2
        blocked=[r for r in rows['HEALTH'] if int(r['slot'])==3-side]
        assert len(blocked)==1 and blocked[0]['before']=='161' and blocked[0]['after']=='155'
        positive=namespace['gate'](rows,side,55465);faults=[]
        for label in ('lingering_owner','advancing_playback'):
            bad=copy.deepcopy(rows)
            if label=='lingering_owner':next(r for r in bad['VOICE_OWNER'] if int(r['slot'])==side and int(r['frame'])>=1462)['id']='17'
            else:next(r for r in bad['VOICE_CHANNEL'] if int(r['channel'])==10+(side-1)*2 and int(r['frame'])>=1462)['pos']=str((2318 if side==1 else 2319)+1)
            try:namespace['gate'](bad,side,55465)
            except AssertionError:faults.append(label)
            else:raise AssertionError('Retirement fault accepted')
        results[f'p{side}']=dict(**positive,rejectedFaults=faults,initialBlockedDamage=6,terminal=t,logSHA256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),mixedOutputAccepted=False,heardQualityAccepted=False,fullGoalComplete=False,checkerSHA256=sync.sha(Path(__file__)))
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
