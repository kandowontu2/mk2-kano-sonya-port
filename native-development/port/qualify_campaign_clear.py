"""Earned final-boss result; deliberately not an ending-render certificate."""
import csv
import hashlib
import json
import re
from pathlib import Path
import subprocess
import sys

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'

def earned_clear(rows,target):
    candidates=[(i,r) for i,r in enumerate(rows) if
        r['mode']=='11' and r['winner']=='1' and r['p1match']=='2' and
        r['p1selected']==r['p1char']==str(target) and
        r['p2selected']==r['p2char']=='13' and r['p2hp']=='0' and int(r['p1hp'])>0]
    assert candidates, 'No own-ID native final-boss two-win result'
    index,result=candidates[0]
    assert index and rows[index-1]['mode']=='2'
    context=(result['attempt'],result['map'])
    fight=[r for r in rows[:index] if (r['attempt'],r['map'])==context and r['p2char']=='13']
    first=[r for r in fight if r['mode']=='5' and r['winner']=='1' and
           r['p1match']=='1' and r['p2hp']=='0' and int(r['p1hp'])>0 and
           r['p1char']==r['p1selected']==str(target)]
    assert first, 'Missing first native winning round in same paid attempt'
    first=first[-1]
    assert first['round']!=result['round']
    second=[r for r in fight if int(r['frame'])>int(first['frame']) and r['mode']=='2']
    assert second and second[0]['p1hp']==second[0]['p2hp']=='161'
    assert second[0]['p1match']=='1' and second[0]['round']==result['round']
    assert all(r['p1char']==r['p1selected']==str(target) for r in second)
    assert rows[index-1]['p2hp']=='0' and int(rows[index-1]['p1hp'])>0
    attract=next((r for r in rows[index+1:] if r['mode']=='1'),None)
    assert attract and int(attract['frame'])>int(result['frame'])
    assert all(r['mode']=='11' for r in rows[index:int(rows.index(attract))])
    return dict(firstWinningRoundFrame=int(first['frame']),
                finalBossClearFrame=int(result['frame']),attempt=int(result['attempt']),
                playerHealthAtClear=int(result['p1hp']),cpuRoundWins=int(result['p2match']),
                attractReturnFrame=int(attract['frame']))

def qualify(name):
    run=BASE/name
    # Re-run the full current-ROM/frozen-input/identity/progression audit.
    subprocess.run([sys.executable,str(PORT/'audit_campaign_run.py'),name],
                   check=True,capture_output=True,
                   creationflags=(subprocess.CREATE_NO_WINDOW|subprocess.BELOW_NORMAL_PRIORITY_CLASS) if sys.platform=='win32' else 0)
    audit=json.loads((run/'CAMPAIGN_AUDIT.json').read_text())
    assert audit['actor'] in (17,18) and audit['currentFullROMVerified']
    defeated=audit['naturallyDefeatedOpponents']
    assert {x['opponent'] for x in defeated}==set(range(12))|{12,17,18}
    rows=list(csv.DictReader((run/'campaign.csv').open()))
    result=earned_clear(rows,audit['actor'])
    src=BASE/'mk2-rebuild-main/srcp'
    main=(src/'MAIN.ASM').read_text()
    equates=(src/'MAINEQU.ASM').read_text()
    assert re.search(r'(?im)^gs_gameover\s+\.set\s+00bh\b',equates)
    assert re.search(r'(?im)^ft_final_boss\s+\.set\s+13\s*$',equates)
    gate=main.split('\nresults_retp\n',1)[1].split('\npf_entered',1)[0]
    for instruction in ('cmpi\t2,a2','cmpi\tft_final_boss,a1','jreq\tgame_finished',
                        'movi\tgs_gameover,a0','jsrp\tcongrats','jruc\tending_gover_entry'):
        assert instruction in gate
    report=dict(scope='Earned native final-boss clear and gameover-to-attract flow',
                actor=audit['actor'],nativeCampaignClearVerified=True,
                ownEndingRenderingVerified=False,castChoreographyVerified=False,
                creditsRenderingVerified=False,fullPortVerified=False,**result)
    pins=[run/n for n in ('CAMPAIGN_AUDIT.json','execution.json','autoboot.lua','campaign.csv')]
    pins += [src/n for n in ('MAIN.ASM','MAINEQU.ASM','MK2P.MAP')]
    pins += [Path(__file__),PORT/'audit_campaign_run.py',PORT/'campaign_budget.py']
    report['pins']={str(p):hashlib.sha256(p.read_bytes()).hexdigest().upper() for p in pins}
    (run/'CAMPAIGN_CLEAR_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    return {k:v for k,v in report.items() if k!='pins'}

if __name__=='__main__':
    print(json.dumps(qualify(sys.argv[1]),indent=2))
