"""Actual loaded story text, original headers, stock rows and own photo slots."""
import copy,json,re
import verify_native_source_sync as sync

def gate(rows,stories):
    scripts=[r for t,r in rows if t=='ENDING_SCRIPT']
    photos=[r for t,r in rows if t=='ENDING_PHOTO']
    assert len(scripts)==10 and len(photos)==4
    for fighter in (0,1):
        for page in (0,1):
            own=[r for r in scripts if r['id']==str(17+fighter) and r['page']==str(page)]
            assert [int(r['segment']) for r in own]==list(range(3 if page==0 else 2))
            for row in own:
                segment=int(row['segment']);index=fighter*5+(0 if page==0 else 3)+segment
                assert bytes.fromhex(row['texthex']).decode('ascii')==stories[index]
                assert int(row['ptr'],16)==0xff800000+(0xf4c00+index*0xc0)*8
                assert row['header_exact']=='true' and row['frame']=='600'
            photo=next(r for r in photos if r['id']==str(17+fighter) and r['page']==str(page))
            assert int(photo['row'])==50+fighter*2+page
            assert 0x07100000<=int(photo['ptr'],16)<0x07200000
    assert len({r['ptr'] for r in photos})==4
    stock=[r for t,r in rows if t=='ENDING_STOCK'];assert len(stock)==1
    assert stock[0]['preserved_pointers']=='72' and stock[0]['own_headers']=='10' and stock[0]['page2_terminators']=='2'
    return dict(storyScripts=10,originalLayoutHeaders=10,stockPointersPreserved=72,ownPhotos=4,page2NullTerminators=2)

def main():
    source=sync.verify()
    folder=sync.ROOT/'audit_current_ending_asset_tables_runtime'
    out=sync.ROOT/'audit_current_ending_asset_tables_checked';assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['elapsedSeconds']<=90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_ending_asset_tables_preparation/attract.lua')
    assert not (folder/'stderr.log').read_text().strip()
    assert not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
    text=(folder/'run.log').read_text();assert 'LUA ERROR' not in text
    rows=[(l.split()[0].removeprefix('MK2_LIGHT_ATTRACT_'),dict(re.findall(r'(\w+)=([^\s]+)',l))) for l in text.splitlines() if l.startswith('MK2_LIGHT_ATTRACT_')]
    assert all(r['writes']=='0' and r['assistance']=='none' for t,r in rows)
    assert [r['frame'] for t,r in rows if t=='INPUT']==['300','301','302','303']
    assert [r['frame'] for t,r in rows if t=='RESULT']==['700']
    cpp=sync.ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'
    section=cpp.read_text().split('char const *const ending_story[2][5] = {',1)[1].split('\n\t};',1)[0]
    stories=[json.loads(s) for s in re.findall(r'"(?:\\.|[^"\\])*"',section)];assert len(stories)==10
    proof=gate(rows,stories)
    bad=copy.deepcopy(rows);next(r for t,r in bad if t=='ENDING_SCRIPT' and r['id']=='18')['texthex']='4C4955204B414E47'
    try:gate(bad,stories)
    except AssertionError:pass
    else:raise AssertionError('Wrong own ending story accepted')
    report=dict(passed=True,sourceSync=source,terminal=terminal,loadedEndingTables=proof,
                wrongStoryRejected=True,logSHA256=sync.sha(folder/'run.log'),
                endingCampaignReached=False,endingPixelsAccepted=False,fullPortAcceptance=False,
                scope='Current loaded ending asset tables only: exact ten own story strings and independent script slots, original24byte headers, all72stock pointers unchanged, four own photo slots and two null page2 terminators. No natural current boss clear/ending execution, decoded pictures, text layout, audio or release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,loadedOwnEndingAssetTables=True,endingCampaignReached=False)))

if __name__=='__main__':main()
