"""Native body suppression and own laser recoil over complete paired fields."""
import copy,json,re,struct
import verify_native_source_sync as sync
import qualify_morphed_victims_secondary_pairs as prior

def body_gate(rows,killer,ident,side):
    action=next(r for t,r in rows if t=='ACTION')
    wrap=next(r for t,r in rows if t=='WRAP')
    peers=[r for t,r in rows if t=='PEER' and int(r['slot'])==side]
    start=int(action['frame'])
    visible=[r for r in peers if int(r['flags'],16)&0x22!=0x22]
    hidden=[r for r in peers if int(r['flags'],16)&0x22==0x22]
    assert visible and hidden
    first=int(hidden[0]['frame'])
    assert [int(r['frame']) for r in hidden]==list(range(first,int(peers[-1]['frame'])+1))
    assert int(visible[-1]['frame'])==first-1 and first<int(wrap['frame'])
    assert int(hidden[0]['flags'],16)==(int(visible[-1]['flags'],16)|32)&~16
    if killer=='kano':
        group='FE831B40' if ident==17 else 'FE83ED00'
        recoil=[r for r in peers if r['pose']==group]
        assert int(recoil[0]['frame'])-start in (68,69)
        assert first-start==164
        assert all(r['pose']==group for r in peers if int(r['frame'])>=int(recoil[0]['frame']))
    return dict(nativeHiddenBodyAge=first-start,hiddenThroughLastFollowthroughField=True,
        hiddenFieldCount=len(hidden),ownLaserRecoilChecked=killer=='kano')

def main():
    source_sync=sync.verify()
    parent=sync.ROOT/'audit_morphed_victims_secondary_pairs_checked/report.json'
    receipt=json.loads(parent.read_text());assert receipt['passed']
    out=sync.ROOT/'audit_morphed_secondary_body_retirement_checked';assert not out.exists()
    stock=(sync.ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    lo=(0xff838f60-0xff800000)//8
    assert stock[lo:lo+18]==struct.pack('<9H',0xB404,0x0160,0x0BA4,0x0020,0,0x0B84,0x0010,0,0xC008)
    cpp=(sync.ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp').read_text()
    assert 'leg_code({0x4d00}); leg_call(0xff838f60);' in cpp
    assert 'leg_code({0xa30f,0xb7a8,0x0140,0x4d00});leg_call(0xff838f60);' in cpp
    cases={}
    for killer,kid,address in (('kano',17,'FFD86600'),('sonya',18,'FFD7B000')):
        gate=prior.make_gate(killer,kid,address)
        for target,ident in (('kano',17),('sonya',18)):
            for side in (1,2):
                key=f'{killer}_{target}_p{side}'
                folder=sync.ROOT/f'audit_morphed_victim_secondary_{key}_runtime'
                log=folder/'run.log'
                assert sync.sha(log)==receipt['cases'][key]['logSHA256']
                rows=[(l.split()[0].removeprefix('MK2_STOCK_HEAD_V921_'),dict(re.findall(r'(\w+)=([^\s]+)',l))) for l in log.read_text().splitlines() if l.startswith('MK2_STOCK_HEAD_V921_')]
                gate(rows,target,ident,side,[])
                proof=body_gate(rows,killer,ident,side)
                bad=copy.deepcopy(rows)
                last=next(r for t,r in reversed(bad) if t=='PEER' and int(r['slot'])==side)
                last['flags']=f'{int(last["flags"],16)&~32:04X}'
                try: body_gate(bad,killer,ident,side)
                except AssertionError: pass
                else: raise AssertionError('Reappearing hidden corpse accepted')
                cases[key]=dict(proof=proof,visibleCorpseFaultRejected=True,logSHA256=sync.sha(log))
    report=dict(passed=True,cases=cases,parentSHA256=sync.sha(parent),sourceSync=source_sync,
        fullPortAcceptance=False,fullEffectArtAccepted=False,
        scope='Eight actual transformed victims: original hide-mask transition before common completion, body remains suppressed through +120-field followthrough; four Kano laser victims retain own recoil from contact through hide. Does not prove raster, palette/effect choreography, worker retirement, audio or full campaign.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,contexts=8,nativeBodySuppression=True,fullPortAcceptance=False)))

if __name__=='__main__':main()
