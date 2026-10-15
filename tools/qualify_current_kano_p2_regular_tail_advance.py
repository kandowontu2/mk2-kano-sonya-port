"""Same-attempt native tail clears plus canonical stock-ID name correction."""
import copy,json,re
import check_campaign_stage_chronology as chronology
import verify_native_source_sync as sync
sync.verify()
case=sync.ROOT/'audit_current_kano_p2_campaign_render_skip_runtime'
out=sync.ROOT/'audit_current_kano_p2_regular_tail_advance_checked'
assert not out.exists()
prior=json.loads((sync.ROOT/'audit_current_kano_p2_campaign_render_skip_checked/report.json').read_text())
assert prior['finiteEvidenceVerified'] and prior['logSHA256']==sync.sha(case/'run.log')
source=(sync.ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp').read_text()
table=source.split('constexpr int16_t leg_stock_xy[12][5][2] = {',1)[1].split('\n\t};',1)[0]
names=re.findall(r'// ([^\n]+)',table)
assert names==['Kung Lao','Liu Kang','Cage','Baraka','Kitana','Mileena','Shang Tsung','Raiden','Sub-Zero','Reptile','Scorpion','Jax']
rows=chronology.load(case/'run.log')
def gate(records):
    proofs=[]
    for stage,start,winframes,nxt,nextstage,cpu,nextcpu in [(11,50932,['51543','52567'],53087,12,10,7),(12,53087,['54662','55824'],56386,14,7,6)]:
        fight=next(r for r in records['FIGHT'] if int(r['frame'])==start)
        assert fight['human']=='17:17' and fight['cpu']==f'{cpu}:{cpu}' and int(fight['stage'])==stage
        wins=[r for r in records['WIN'] if int(r['stage'])==stage and r['slot']=='2' and start<int(r['frame'])<nxt]
        assert [r['frame'] for r in wins]==winframes
        assert all(r['id']=='17' and r['entry']=='FFFEFA20' and r['pc']=='FF8296B0' and r['health'].split(',')[0]=='0' and int(r['health'].split(',')[1])>0 for r in wins)
        assert not any(start<int(r['frame'])<nxt for r in records['LOSS'])
        successor=next(r for r in records['FIGHT'] if int(r['frame'])==nxt)
        assert int(successor['stage'])==nextstage and successor['human']=='17:17' and successor['cpu']==f'{nextcpu}:{nextcpu}'
        proofs.append(dict(stage=stage,nativeOpponentID=cpu,nativeOpponentName=names[cpu],ownWins=wins,nextFight=successor,nextOpponentName=names[nextcpu]))
    return proofs
proof=gate(rows)
for fault in ('wrongwinner','paidloss'):
    bad=copy.deepcopy(rows)
    if fault=='wrongwinner':next(r for r in bad['WIN'] if r['frame']=='55824')['slot']='1'
    else:bad['LOSS'].append(dict(frame='55000'))
    try:gate(bad)
    except AssertionError:pass
    else:raise AssertionError('False clear accepted: '+fault)
out.mkdir();report=dict(passed=True,proof=proof,canonicalStockNames=names,
    historicalTestNameLabelsCorrected=True,wrongWinnerFaultRejected=True,interveningPaidLossFaultRejected=True,
    fullCampaignAccepted=False,fullPortAccepted=False,logSHA256=sync.sha(case/'run.log'))
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
