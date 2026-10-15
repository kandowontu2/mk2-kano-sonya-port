"""Verify observer repair without claiming hit-during-private-cue coverage."""
import hashlib,json,re
from pathlib import Path
import verify_native_source_sync as sync
ROOT=sync.ROOT
BASE=ROOT/'audit_bounded_native_uppercut_retained_tap_runtime'
OLD=ROOT/'audit_bounded_native_uppercut_boot608_runtime'
RX=re.compile(r'(\w+)=([^\s]+)')
def scan(folder):
    digest=hashlib.sha256();cues=[];active=set();hits=[];last_hp=None;retained=0;fields=0
    with (folder/'run.log').open() as stream:
        for line in stream:
            assert len(line)<1048576 and '[LUA ERROR]' not in line
            tag=line.split(' ',1)[0].strip();r=dict(RX.findall(line))
            if tag in ('MK2_BOUNDED_FIELD','MK2_VOICE_OWNER','MK2_P2CPU_SELECT_RESULT'):
                digest.update(line.encode())
            if tag=='MK2_BOUNDED_CUE':cues.append(r)
            if tag=='MK2_BOUNDED_TAP_TERMINAL':retained+=int(r['retained'])
            if tag=='MK2_VOICE_OWNER' and r['slot']=='2' and r['actor']!='00000000':active.add(int(r['frame']))
            if tag=='MK2_BOUNDED_FIELD':
                fields+=1;hp=int(r['hp2']);frame=int(r['frame'])
                assert r['p1id']=='17' and r['p2id']=='18' and r['writes']=='0'
                if last_hp is not None and 0<last_hp<=166 and hp<last_hp:hits.append(frame)
                last_hp=hp
    return dict(digest=digest.hexdigest(),cues=cues,active=active,hits=hits,retained=retained,fields=fields)
def main():
    pins=sync.verify();terminal=json.loads((BASE/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    before,after=scan(OLD),scan(BASE)
    assert before['digest']==after['digest'],'Observer repair must not alter actual scalar gameplay/owner trace'
    assert after['retained']==1 and len(after['cues'])==2
    assert [r['word'] for r in after['cues']]==['6B01','6B02']
    assert {r['frame'] for r in after['cues']}=={'2934'}
    assert after['active']==before['active'] and len(after['active'])==77
    overlaps=[f for f in after['hits'] if f in after['active'] or f-1 in after['active']]
    assert not overlaps
    report=dict(observerRepairVerified=True,privateInterruptionAccepted=False,
        nativeExit=terminal['exitCode'],peakWorkingSetBytes=terminal['peakWorkingSetBytes'],
        identicalScalarGameplayAndOwners=True,scalarFields=after['fields'],
        actualLaunchCommands=after['cues'],activeOwnerFrames=len(after['active']),
        incomingDamageFrames=after['hits'],damageDuringObservedVoiceFrames=overlaps,
        fullGoalComplete=False,sourceSync=pins,
        hashes={str(p):sync.sha(p) for p in (BASE/'run.log',OLD/'run.log',Path(__file__))})
    target=BASE/'observer_check.json';assert not target.exists()
    target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('sourceSync','hashes')}))
if __name__=='__main__':main()
