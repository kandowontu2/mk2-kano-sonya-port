"""Actual earned Portal/Toasty admission; random misses never count as success."""
import copy
import json
import re
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_sonya_natural_smoke_runtime'
out=sync.ROOT/'audit_current_sonya_natural_smoke_checked'
assert not out.exists()
terminal=json.loads((folder/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_sonya_natural_smoke_preparation/stage.lua')
assert not (folder/'stderr.log').read_text().strip()
def load(path):
    text=path.read_text();assert 'LUA ERROR' not in text
    rows={}
    for line in text.splitlines():
        if line.startswith('MK2_STAGE_'):
            rows.setdefault(line.split()[0][10:],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    return rows
rows=load(folder/'run.log')
old=load(sync.ROOT/'audit_current_stock_pit_initialized_selector_sonya_p1_kitana_runtime/run.log')
for tag in set(rows)|set(old):
    if tag!='BOOT' and not tag.startswith('SECRET_'):
        assert [r for r in rows.get(tag,[]) if int(r['frame'])<17948]==[
            r for r in old.get(tag,[]) if int(r['frame'])<17948],tag
def gate(records):
    assert all(r['writes']=='0' and r['assistance']=='none' and r['side']=='1' and r['winner']=='sonya'
               for group in records.values() for r in group)
    matches=records['MATCH']
    assert [(r['match'],r['arena'],r['ids']) for r in matches]==[
        (str(i+1),str(i%9),'18,4') for i in range(len(matches))]
    for window in records.get('WINDOW',[]):
        damage=[r for r in records['DAMAGE'] if r['match']==window['match']]
        assert sum(int(r['before'])-int(r['after']) for r in damage)==322
        assert sum(r['after']=='0' for r in damage)==2
        assert all(r['pc']=='FF836700' and int(r['before'])>int(r['after']) for r in damage)
        assert window['kos']=='2' and window['damage']=='322'
    proof=dict(earnedMatches=len(matches),earnedTwoWinWindows=len(records.get('WINDOW',[])),
               portalAdmissions=sum(r['arena']=='7' for r in matches),
               actualToastyEvents=len(records.get('SECRET_TOASTY',[])),
               actualSecretAccepted=False,completeSameRoundControls=False)
    accepts=records.get('SECRET_ACCEPT',[])
    if not accepts:return proof
    assert len(accepts)==1
    accept=accepts[0];at=int(accept['frame'])
    assert accept['pc']=='FFA1A470' and accept['arena']=='7' and accept['secretID']=='14' and accept['taskSide']=='0'
    assert int(accept['in0'],16)&2==0 and (int(accept['tick'])-int(accept['toastTick']))%65536<=64
    toast=[r for r in records['SECRET_TOASTY'] if int(r['frame'])<=at][-1]
    assert toast['pc']=='FFA0BAF0' and toast['tick']==accept['toastTick']
    for button in ('Down','Start'):
        assert any(r['slot']=='1' and r['button']==button and at-1<=int(r['frame'])<=at for r in records['INPUT'])
    fights=records.get('SECRET_FIGHT',[])
    assert len(fights)==1 and fights[0]['human']=='18' and fights[0]['cpu']=='14' and fights[0]['arena']=='9'
    assert int(fights[0]['frame'])>at
    live=[r for r in records['SECRET_FIELD'] if int(r['frame'])>=int(fights[0]['frame']) and r['mode']=='2']
    assert live
    for r in live:
        assert r['ids']==r['rosters']=='18,14' and r['states']=='1,0' and r['arena']=='9'
        assert r['actors']==r['owners'] and all(0x01000000<=int(v,16)<0x01100000 for v in r['actors'].split(',')+r['mains'].split(','))
    proof.update(actualSecretAccepted=True,acceptance=accept,secretFight=fights[0],liveSecretFields=len(live))
    complete=records.get('SECRET_COMPLETE',[])
    if not complete:return proof
    assert len(complete)==1
    finish=complete[0];epoch=int(finish['epoch']);last=int(finish['frame'])
    final=[r for r in live if epoch<=int(r['frame'])<=last]
    assert [int(r['frame']) for r in final]==list(range(epoch,last+1))
    assert all(all(0<int(h)<=161 for h in r['hp'].split(',')) for r in final)
    responses=[next(r for r in reversed(records['SECRET_'+tag]) if int(r['frame'])>=epoch)
               for tag in ('WALK','JUMP','PUNCH','RECOVER')]
    assert epoch<=int(responses[0]['frame'])<int(responses[1]['frame'])<int(responses[2]['frame'])<int(responses[3]['frame'])
    assert abs(int(responses[0]['x'])-int(responses[0]['from']))>=4
    assert int(responses[1]['y'])<int(responses[1]['floor'])
    assert final[int(responses[2]['frame'])-epoch]['actions'].split(',')[0]=='257'
    assert int(finish['recovered'])==int(responses[3]['frame']) and last-int(finish['recovered'])>=180
    proof.update(completeSameRoundControls=True,complete=finish,responses=responses)
    return proof
proof=gate(rows)
bad=copy.deepcopy(rows);bad['MATCH'][0]['ids']='1,4'
try:gate(bad)
except AssertionError:pass
else:raise AssertionError('Proxy selection accepted')
bad=copy.deepcopy(rows);bad['DAMAGE'].pop(0)
try:gate(bad)
except AssertionError:pass
else:raise AssertionError('Unearned arena progression accepted')
out.mkdir()
(out/'report.json').write_text(json.dumps(dict(finiteObservationPassed=True,
    priorPhysicalPrefixUnchangedThrough=17947,proof=proof,proxyAndUnearnedDamageFaultsRejected=True,
    terminal=terminal,logSHA256=sync.sha(folder/'run.log'),secretVisualAudioAccepted=False,
    completeSecretTeardownAccepted=False,lateWatchdogResetFixed=False,fullPortAccepted=False),indent=2))
print(json.dumps(proof))
