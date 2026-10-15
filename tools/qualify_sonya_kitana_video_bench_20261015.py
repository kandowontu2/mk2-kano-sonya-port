"""Require two real same-paid Kitana wins and native next-match admission."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parent.parent

def load(path):
    text=path.read_text();assert 'LUA ERROR' not in text and len(text)<20*1024**2
    return [(line.split()[0].removeprefix('MK2_NAT_CAMPAIGN_'),dict(re.findall(r'(\w+)=([^\s]+)',line))) for line in text.splitlines() if line.startswith('MK2_NAT_CAMPAIGN_')]

def gate(rows):
    advances=[r for t,r in rows if t=='FIGHT' and r['stage']=='10']
    assert advances,'No actual next match'
    advance=advances[0];assert advance['human']=='18:18' and advance['cpu']=='5:5'
    selection=advance['selection'];stop=int(advance['frame'])
    starts=[r for t,r in rows if t=='FIGHT' and r['stage']=='9' and r['selection']==selection and int(r['frame'])<stop]
    assert starts and all(r['human']=='18:18' and r['cpu']=='4:4' for r in starts)
    start=int(starts[-1]['frame'])
    window=[(t,r) for t,r in rows if start<=int(r['frame'])<=stop]
    assert not any(t in ('LOSS','SELECT') for t,r in window),'Intervening paid continue'
    wins=[r for t,r in window if t=='WIN' and r['stage']=='9' and r['slot']=='2']
    assert len(wins)==2 and int(wins[1]['frame'])-int(wins[0]['frame'])>100,'Two actual rounds'
    assert not any(t=='WIN' and r['stage']=='9' and r['slot']=='1' for t,r in window),'Opponent round win in required two-win window'
    for win in wins:
        assert win['id']=='18' and win['pc']=='FF8296B0'
        enemy,own=map(int,win['health'].split(','));assert 0<=enemy<own<=161
        if enemy:
            assert any(t=='STATE' and r['mode']=='5' and r['winner']=='2' and r['health']==win['health'] and int(win['frame'])<=int(r['frame'])<=int(win['frame'])+2 for t,r in window),'Native timeout winner context'
    legs=[r for t,r in window if t=='SPECIAL' and r['move']=='leg' and r['stage']=='9']
    assert legs and all(r['entry']=='FFF80800' and r['actor']==r['a8'] and r['main']==r['a13'] and r['id']==r['roster']=='18' for r in legs)
    assert all(r['writes']=='0' and r['assistance']=='none' for t,r in rows)
    return dict(selection=selection,kitanaFight=starts[-1],ownRoundWins=wins,nextMileenaFight=advance,ownedLegEntries=len(legs),fullCampaign=False)

def main():
    pa=argparse.ArgumentParser();pa.add_argument('case',nargs='?',default='video_sonya_kitana_leg_bench_20261015');a=pa.parse_args()
    assert re.fullmatch(r'[a-z0-9_]+',a.case)
    folder=ROOT/a.case;out=folder/'qualification.json';assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text());assert terminal['exitCode']==0 and not terminal['limits']
    assert not (folder/'stderr.log').read_text().strip()
    rows=load(folder/'run.log');proof=gate(rows)
    faults=[]
    for kind in ('missing_win','continued','proxy','wrong_winner'):
        bad=copy.deepcopy(rows)
        if kind=='missing_win':bad.pop(next(i for i,(t,r) in enumerate(bad) if t=='WIN' and r['frame']==proof['ownRoundWins'][0]['frame']))
        elif kind=='continued':bad.append(('LOSS',dict(proof['ownRoundWins'][0])))
        elif kind=='proxy':next(r for t,r in bad if t=='FIGHT' and r['frame']==proof['nextMileenaFight']['frame'])['human']='1:1'
        else:next(r for t,r in bad if t=='WIN' and r['frame']==proof['ownRoundWins'][0]['frame'])['slot']='1'
        try:gate(bad)
        except AssertionError:faults.append(kind)
        else:raise AssertionError('False proof admitted: '+kind)
    report=dict(passed=True,proof=proof,terminal=terminal,faultsRejected=faults,logSHA256=hashlib.sha256((folder/'run.log').read_bytes()).hexdigest().upper(),scope='Kitana native paid two-round win and next-Mileena admission only, not entire campaign or video')
    out.write_text(json.dumps(report,indent=2));print(json.dumps(proof))

if __name__=='__main__':main()
