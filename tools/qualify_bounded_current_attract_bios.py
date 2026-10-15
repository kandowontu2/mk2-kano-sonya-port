"""Actual natural bio rotation and character-owned name/story/picture selection."""
import copy,json,re
import verify_native_source_sync as sync

def gate(rows):
    def tagged(tag):return [r for t,r in rows if t==tag]
    rotation=[r for r in tagged('COUNTER') if r['pc']=='FF84A460']
    assert [int(r['id']) for r in rotation]==[9,10,11,17,18,0]
    proofs={}
    for ident,expected,picture in ((17,(0xfff9c380,0xfffb9800,0xfffba000),54),(18,(0xfff9c580,0xfffba800,0xfffb3980),55)):
        counter=next(r for r in rotation if int(r['id'])==ident)
        reads=[r for r in tagged('BIO_READ') if int(r['id'])==ident]
        first=0xff800000+(0xf3780+ident*12)*8
        assert len(reads)==6 and [int(r['at'],16) for r in reads]==[first+i*16 for i in range(6)]
        assert all(r['frame']==counter['frame'] and r['counter']==str(ident) and r['mask']=='FFFF' for r in reads)
        assert [r['pc'] for r in reads]==['FF84A620']*2+['FF84A630']*2+['FF84A640']*2
        pointers=tuple(int(reads[i]['data'],16)|(int(reads[i+1]['data'],16)<<16) for i in (0,2,4))
        assert pointers==expected
        pictures=[r for r in tagged('PICTURE') if int(r['row'])==picture]
        assert len(pictures)==1 and pictures[0]['frame']==counter['frame'] and pictures[0]['pc']=='FF8447E0'
        proofs[str(ident)]=dict(frame=int(counter['frame']),nativePointers=[f'{p:08X}' for p in pointers],nativePictureRow=picture)
    assert [r['frame'] for r in tagged('INPUT')]==['300','301','302','303']
    assert len(tagged('FIELD'))==400 and tagged('RESULT')[0]['frame']=='24000'
    return proofs

def main():
    source_sync=sync.verify()
    out=sync.ROOT/'audit_bounded_current_attract_bios_checked';assert not out.exists()
    folder=sync.ROOT/'audit_bounded_current_attract_long_runtime'
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_bounded_current_attract_long_preparation/attract.lua')
    assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['elapsedSeconds']<=90 and terminal['logBytes']<=10*1024*1024
    assert not (folder/'stderr.log').read_text().strip() and not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
    text=(folder/'run.log').read_text();assert 'LUA ERROR' not in text
    rows=[(l.split()[0].removeprefix('MK2_LIGHT_ATTRACT_'),dict(re.findall(r'(\w+)=([^\s]+)',l))) for l in text.splitlines() if l.startswith('MK2_LIGHT_ATTRACT_')]
    assert all(r['writes']=='0' and r['assistance']=='none' for t,r in rows)
    proofs=gate(rows)
    bad=copy.deepcopy(rows);next(r for t,r in bad if t=='BIO_READ' and r['id']=='18')['data']='0000'
    try:gate(bad)
    except AssertionError:pass
    else:raise AssertionError('Wrong native Sonya bio name pointer accepted')
    report=dict(passed=True,sourceSync=source_sync,terminal=terminal,bios=proofs,wrongNamePointerRejected=True,
        logSHA256=sync.sha(folder/'run.log'),fullBioVisualAudioAccepted=False,fullPortAcceptance=False,
        scope='Cold natural attract, only four ordinary boot HP inputs: true17/18 biography rotation, all three own native name/story pointers and picture54/55 selection, then original0 wrap. No full picture/text raster/audio/demo combat or release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,naturalKanoSonyaBios=True,fullPortAcceptance=False)))

if __name__=='__main__':main()
