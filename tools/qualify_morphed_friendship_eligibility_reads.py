"""Original gate prefix plus actual native own-slot punch-counter reads."""
import json,struct
import verify_native_source_sync as sync
import qualify_bounded_current_friendships as parsing
import qualify_bounded_morphed_friendships as previous

def rows(text,tag):
    return [parsing.fields(line) for line in text.splitlines() if line.startswith('MK2_FRIEND_'+tag+' ')]

def gate(text,side,stock):
    previous.validate(text,'sonya',side)
    words=rows(text,'ORIGINAL_GATE_WORD')
    addresses=list(range(0xff880770,0xff880890+1,16))
    assert [int(r['at'],16) for r in words]==addresses
    for r in words:
        offset=(int(r['at'],16)-0xff800000)//8
        assert int(r['word'],16)==struct.unpack_from('<H',stock,offset)[0]
    window=rows(text,'WINDOW')[0]
    counters=[int(v) for v in window['lp_counters'].split(',')]
    native=rows(text,'ELIGIBILITY_READ')
    assert len(native)==2
    actor=next(r for r in rows(text,'MORPH_STORE') if r['id']=='18')['actor']
    hp,lp=native
    assert hp['frame']==lp['frame'] and int(hp['frame'])>int(window['frame'])
    assert all(r['pc']=='FF880A60' and r['mask']=='0000FFFF' and r['a8']==actor for r in native)
    assert int(hp['at'],16)==0x01061e40+(side-1)*16 and hp['data']=='0000'
    assert int(lp['at'],16)==0x01061e60+(side-1)*16 and int(lp['data'],16)==counters[side-1]>0
    return dict(originalGatePrefixWords=len(words),nativeEligibilityReadPC=hp['pc'],
        actualOwnLowPunchCounter=counters[side-1],actualHighPunchCounter=0,
        nativeReadFrame=int(hp['frame']),friendshipActionAbsent=True)

if __name__=='__main__':
    source_sync=sync.verify()
    out=sync.ROOT/'audit_morphed_friendship_eligibility_reads_checked';assert not out.exists()
    stock=sync.ROOT/'mk2/mk2-maincpu.bin'
    original=stock.read_bytes();assert len(original)==1048576
    lua=sync.ROOT/'audit_morphed_friendship_eligibility_reads_preparation/friendships.lua'
    results={}
    for side in(1,2):
        folder=sync.ROOT/f'audit_morphed_friendship_eligibility_sonya_p{side}_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['observerSha256']==sync.sha(lua)
        assert not (folder/'stderr.log').read_text().strip()
        assert not any(p.suffix.lower() in('.png','.bin','.wav') for p in folder.rglob('*'))
        text=(folder/'run.log').read_text();assert 'LUA ERROR' not in text
        proof=gate(text,side,original)
        baseline=sync.ROOT/f'audit_bounded_morphed_friendship_followthrough_sonya_p{side}_runtime/run.log'
        keep=lambda value:[line for line in value.splitlines() if line.startswith('MK2_FRIEND_') and not line.startswith(('MK2_FRIEND_ELIGIBILITY_READ ','MK2_FRIEND_ORIGINAL_GATE_WORD '))]
        assert keep(text)==keep(baseline.read_text())
        record=rows(text,'ELIGIBILITY_READ')[-1]
        needle='at='+record['at']+' data='+record['data']
        assert text.count(needle)==1
        broken=text.replace(needle,'at='+record['at']+' data=0000')
        try:gate(broken,side,original)
        except AssertionError:pass
        else:raise AssertionError('Masked actual nonzero LP eligibility read accepted')
        results[str(side)]=dict(proof=proof,terminal=terminal,logSHA256=sync.sha(folder/'run.log'),
            baselineSHA256=sync.sha(baseline),entirePhysicalTraceUnchanged=True,maskedCounterReadRejected=True)
    report=dict(passed=True,results=results,sourceSync=source_sync,stockROMSHA256=sync.sha(stock),
        fullPortAcceptance=False,scope='Both physical slots: Sonya actual morph/earned-round input traces unchanged; nineteen running native gate-prefix words match original ROM, original routine PC FF880A60 reads own zero HP/nonzero LP, friendship does not activate. Not complete routine byte comparison, heard audio, babality, whole CPU/campaign/port acceptance. No command or counter changes.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,contexts=2,nativePunchCounterReadsVerified=True,fullPortAcceptance=False)))
