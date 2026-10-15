"""Full native ladder/boss/own-ending gate before recording the controller."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parent.parent
RX=re.compile(r'(\w+)=([^\s]+)')

def gate(rows):
    def tagged(tag):return [r for t,r in rows if t==tag]
    assert all(r['writes']=='0' and r['assistance']=='none' for t,r in rows)
    result=tagged('RESULT');assert len(result)==1
    r=result[0];assert int(r['ending'])>0 and int(r['ending_completed'])>int(r['ending'])
    fights=tagged('FIGHT');assert {int(x['stage']) for x in fights}==set(range(13))|{14,15,16}
    assert all(x['human']=='18:18' for x in fights)
    assert {x['page'] for x in tagged('PICTURE')}=={'1','2'} and {x['page'] for x in tagged('TEXT')}=={'1','2'}
    assert len(tagged('ENDING_START'))==1 and len(tagged('ENDING_COMPLETED'))==1
    e=tagged('ENDING_START')[0]
    assert e['stage']=='16' and e['winner']=='2' and e['roster']=='18' and e['actors']=='00000000,00000000'
    hp=list(map(int,e['health'].split(',')));assert hp[0]==0 and 0<hp[1]<=161
    ending=int(e['frame']);assert ending==int(r['ending'])
    assert int(tagged('ENDING_COMPLETED')[0]['frame'])==int(r['ending_completed'])
    assert int(r['frame'])>=int(r['ending_completed'])+300
    own=[x for x in tagged('WIN') if x['slot']=='2']
    for stage in (15,16):
        wins=[x for x in own if x['stage']==str(stage) and int(x['frame'])<ending]
        # Native final Shao encounter requires one winning round; Kintaro
        # requires two. The completed Kano recording independently confirms
        # this chronology. The earned own-ending entry is mandatory as well.
        assert len(wins)>=(2 if stage==15 else 1) and all(x['id']=='18' and x['pc']=='FF8296B0' and x['health'].split(',')[0]=='0' and int(x['health'].split(',')[1])>0 for x in wins)
    assert not tagged('HOST_BOUND')
    return dict(fullNativeCampaignAndOwnEnding=True,endingFrame=ending,completedFrame=int(r['ending_completed']),stopFrame=int(r['frame']),selections=int(r['selections']),paidLosses=int(r['losses']),entireStageSet=sorted({int(x['stage']) for x in fights}),ownEndingPages=[1,2],videoStillRequired=True)

def main():
    pa=argparse.ArgumentParser();pa.add_argument('case',nargs='?',default='video_sonya_complete_bench_20261015');a=pa.parse_args()
    assert re.fullmatch('[a-z0-9_]+',a.case)
    out=ROOT/a.case;receipt=out/'qualification.json';assert not receipt.exists()
    terminal=json.loads((out/'terminal.json').read_text());assert terminal['exitCode']==0 and not terminal['limits']
    launch=json.loads((out/'launch.json').read_text());lua=Path(launch['command'][-1])
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
    assert sha(lua)==launch['luaSHA256'] and launch['executableSHA256']=='EBDFEB6CCA3617308F1448A4A0F6778E3E787420CACF3D11E9B4F40358C87F6A'
    assert not (out/'stderr.log').read_text().strip()
    text=(out/'run.log').read_text();rows=[(s.split()[0].removeprefix('MK2_NAT_CAMPAIGN_'),dict(RX.findall(s))) for s in text.splitlines() if s.startswith('MK2_NAT_CAMPAIGN_')]
    proof=gate(rows);faults=[]
    for kind in ('no_shao','proxy','missing_picture','missing_stage','no_kintaro','bad_ending_health'):
        bad=copy.deepcopy(rows)
        if kind=='no_shao':bad=[(t,r) for t,r in bad if not(t=='WIN' and r['stage']=='16')]
        elif kind=='proxy':next(r for t,r in bad if t=='FIGHT')['human']='1:1'
        elif kind=='missing_picture':bad=[(t,r) for t,r in bad if not(t=='PICTURE' and r['page']=='2')]
        elif kind=='missing_stage':bad=[(t,r) for t,r in bad if not(t=='FIGHT' and r['stage']=='14')]
        elif kind=='no_kintaro':bad=[(t,r) for t,r in bad if not(t=='WIN' and r['stage']=='15')]
        else:next(r for t,r in bad if t=='ENDING_START')['health']='100,0'
        try:gate(bad)
        except AssertionError:faults.append(kind)
        else:raise AssertionError('Missing completion proof accepted: '+kind)
    receipt.write_text(json.dumps(dict(passed=True,proof=proof,faultsRejected=faults,terminal=terminal,sourceSHA256=sha(lua),logSHA256=sha(out/'run.log'),videoRecorded=False),indent=2))
    print(json.dumps(proof))

if __name__=='__main__':main()
