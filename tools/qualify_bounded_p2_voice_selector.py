"""Native role-byte selection explains P2 Kano command; RNG count is one."""
import copy,json,re
from pathlib import Path
import qualify_bounded_p2_stock_head_finisher as scope
import qualify_bounded_stock_head_finisher as control
import verify_native_source_sync as sync

def gate(steps,cue,fighter,stock):
    ident=18 if fighter=='sonya' else 17
    assert [r['entry'] for r in steps]==['FFA12220','FFA123D0','FFA12400','FFA12530']
    assert all(r['age']=='58' and r['frame']=='3113' and r['role']=='2' and int(r['victim_id'])==ident
        and r['a8']=='010350A0' and r['a13']=='0106B150' for r in steps)
    count=int(steps[0]['a0'],16);packed=int(steps[0]['a1'],16)
    assert count==1 and packed==0x45464748
    base=(packed&255) if fighter=='sonya' else (packed>>16)&255
    assert int(steps[1]['a1'],16)==int(steps[2]['a1'],16)==int(steps[3]['a1'],16)==base
    assert int(steps[1]['a0'],16)==count and int(steps[2]['a0'],16)==1
    assert int(steps[3]['a0'],16)==base and int(cue['cue'],16)==base
    import struct
    off=lambda pc:(pc-0xff800000)//8
    header,packet=struct.unpack_from('<HH',stock,off(0xffa0ef20)+base*4)
    assert int(cue['header'],16)==header and int(cue['packet'],16)==packet
    return dict(trueID=ident,physicalRole=2,packedVoice=f'{packed:08X}',selectedCue=f'{base:02X}',
        stockTableCommand=f'{packet:04X}',randomVariantCount=count)

def main():
    out=sync.ROOT/'audit_bounded_p2_voice_selector_checked';assert not out.exists()
    proof=json.loads((sync.ROOT/'audit_bounded_p2_stock_head_control_checked/report.json').read_text())
    assert proof['passed'];stock=(sync.ROOT/'mk2/mk2-maincpu.bin').read_bytes();results={}
    off=lambda pc:(pc-0xff800000)//8
    for fighter,ident in (('sonya',18),('kano',17)):
        folder=sync.ROOT/f'audit_bounded_p2_{fighter}_voice_selector_runtime'
        baseline=sync.ROOT/f'audit_bounded_p2_{fighter}_stock_head_finisher_runtime'
        assert sync.sha(baseline/'run.log')==proof['results'][fighter]['logSha256']
        terminal=json.loads((folder/'terminal.json').read_text());assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        def read(folder):
            states=[];groups={}
            with (folder/'run.log').open() as stream:
                for line in stream:
                    assert '[LUA ERROR]' not in line
                    r=dict(re.findall(r'(\w+)=([^\s]+)',line))
                    if line.startswith('MK2_STOCK_HEAD_V921_'):
                        m=scope.PREFIX.match(line);assert m and m[3]==fighter and m[4]=='2'
                        states.append((m[1],r))
                    elif line.startswith('MK2_VOICE_SELECTOR_'):groups.setdefault(line.split(' ',1)[0],[]).append(r)
            return states,groups
        states,groups=read(folder);old,_=read(baseline);assert states==old
        control.gate(states,fighter,ident)
        source=groups['MK2_VOICE_SELECTOR_SOURCE'];assert len(source)==1
        assert bytes.fromhex(source[0]['hex'])==stock[off(0xffa122d0):off(0xffa12430)]
        steps=groups['MK2_VOICE_SELECTOR_STEP'];cues=groups['MK2_VOICE_SELECTOR_CUE'];assert len(cues)==1
        positive=gate(steps,cues[0],fighter,stock)
        bad=copy.deepcopy(steps);bad[1]['a1']='00000000'
        try:gate(bad,cues[0],fighter,stock)
        except AssertionError:pass
        else:raise AssertionError('Wrong byte accepted')
        results[fighter]=dict(**positive,terminal=terminal,logSha256=sync.sha(folder/'run.log'),wrongSelectedByteRejected=True)
    report=dict(passed=True,results=results,sourceSync=sync.verify(),stockSha256=sync.sha(sync.ROOT/'mk2/mk2-maincpu.bin'),
        checkerSha256=sync.sha(Path(__file__)),heardAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
