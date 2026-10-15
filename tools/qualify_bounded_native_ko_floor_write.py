"""Direct native KO floor-write proof; no graphical sole-height acceptance."""
import copy,json,struct
from pathlib import Path
import check_bounded_native_retained_tap as prior
ROOT=prior.ROOT
BASE=ROOT/'audit_bounded_native_floor_writes_runtime'
def gate(rows,fields,stock_words):
    assert stock_words==(0xb5a0,0x200,0xbe0,0xfff7,0xb00d,0x200)
    candidates=[r for r in rows if r['slot']=='1' and r['hp']=='0']
    assert len(candidates)==1
    r=candidates[0]
    assert (r['id'],r['action'],r['before'],r['data'],r['mask'],r['pc'],r['a0'],r['op0'],r['op1'])==(
        '17','050A','82','004A','FFFF','FFA0DD40','0000004A','B00D','0200')
    assert r['a13']==r['main'] and r['stage_floor']=='216'
    frame=int(r['frame']);following=next(x for x in fields if int(x['frame'])==frame+1)
    assert (following['p1id'],following['hp1'],following['action1'],following['floor1'])==('17','0','050A','74')
    return dict(frame=frame,slot=1,trueId=17,nativePC=r['pc'],beforeFloor=82,afterFloor=74,
        originalStockInstructionOperandsMatch=True,physicalFloorWriteAndNextFieldAgree=True)
def main():
    out=BASE/'ko_floor_write_check.json';assert not out.exists()
    terminal=json.loads((BASE/'terminal.json').read_text());assert terminal['exitCode']==0 and not terminal['limitReason']
    assert prior.scan(BASE)['digest']==prior.scan(ROOT/'audit_bounded_native_close_counter_runtime')['digest']
    rows=[];fields=[]
    with (BASE/'run.log').open() as stream:
        for line in stream:
            assert len(line)<1048576 and '[LUA ERROR]' not in line
            if line.startswith('MK2_BOUNDED_FLOOR_WRITE '):rows.append(dict(prior.RX.findall(line)))
            elif line.startswith('MK2_BOUNDED_FIELD '):fields.append(dict(prior.RX.findall(line)))
    assert len(rows)<2000 and len(fields)<=1800
    stock=ROOT/'mk2/mk2-maincpu.bin'
    with stock.open('rb') as rom:
        rom.seek((0xffa0dce0-0xff800000)//8);words=struct.unpack('<6H',rom.read(12))
    positive=gate(rows,fields,words);faults=[]
    for key,value in (('pc','FFA0DD50'),('data','004B'),('a13','0106A380'),('id','18'),('op0','B00C')):
        bad=copy.deepcopy(rows);next(r for r in bad if r['slot']=='1' and r['hp']=='0')[key]=value
        try:gate(bad,fields,words)
        except AssertionError:faults.append(key)
        else:raise AssertionError('Floor counterexample admitted '+key)
    assert gate(rows,fields,words)==positive
    report=dict(passed=True,nativeExit=0,peakWorkingSetBytes=terminal['peakWorkingSetBytes'],
        actualNativeKO=positive,rejectedFaults=faults,identicalGameplayAndVoiceTrace=True,
        graphicSoleParityAccepted=False,allReactionStatesAccepted=False,fullGoalComplete=False,
        sourceSync=prior.sync.verify(),
        hashes={str(p):prior.sync.sha(p) for p in (BASE/'run.log',stock,Path(__file__))})
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,actualNativeKO=positive,rejectedFaults=faults)))
if __name__=='__main__':main()
