"""Earned native rejection, no false positive stage action or proxy identity."""
import argparse,copy,json
import verify_native_source_sync as sync
from qualify_current_native_tomb_case import load

def gate(rows,fighter,side,label):
    own=17 if fighter=='kano' else 18;victim=35-own;arena=0 if label=='arena0' else 1
    case={'wrong':'wrong_command','far':'far','arena0':'positive'}[label]
    assert all(r['writes']=='0' and r['assistance']=='none' and r['side']==str(side) and r['winner']==fighter for records in rows.values() for r in records)
    boot=rows['BOOT'][0];assert boot['own_id']==str(own) and boot['victim_id']==str(victim) and boot['command_case']==case and boot['target_arena']==str(arena)
    assert [(r['match'],r['arena'],r['ids']) for r in rows['MATCH']]==[(str(i+1),str(i),f'{own},{victim}') for i in range(arena+1)]
    assert len(rows['WINDOW'])==arena+1
    for window in rows['WINDOW']:
        hits=[r for r in rows['DAMAGE'] if r['match']==window['match']]
        assert sum(int(r['before'])-int(r['after']) for r in hits)==322
        assert all(r['pc']=='FF836700' and 0<=int(r['after'])<int(r['before'])<=161 for r in hits)
        groups=[];chain=[]
        for hit in hits:
            chain.append(hit)
            if hit['after']=='0':groups.append(chain);chain=[]
        assert len(groups)==2 and not chain
        assert all(g[0]['before']=='161' and g[-1]['after']=='0' and all(a['after']==b['before'] for a,b in zip(g,g[1:])) for g in groups)
    command=rows['COMMAND'][0];begin=int(command['frame']);assert command['arena']==str(arena)
    assert int(command['gap'])>=130 if label=='far' else 60<=int(command['gap'])<=65
    assert not rows.get('FIELD') and not any(r['entry'] in ('FF8BDDE0','FF8BDFE0') for r in rows['ENTRY'])
    parser='FFFAA200' if own==17 else 'FFFAA400'
    event=next(r for r in rows['ENTRY'] if r['entry']==parser and int(r['frame'])>=begin+40)
    assert event['id']==str(own) and int(event['frame'])==begin+42
    addresses={'FF876D20','FF876E50','FF876E80','FF876F40','FF877000','FF877120','FF8771F0','FF877270','FF877280','FF877300','FF877350','FF8773A0','FF877420'}
    branch=[r for r in rows['ENTRY'] if r['frame']==event['frame'] and r['a8']==event['a8'] and r['entry'] in addresses]
    expected={'wrong':['FF876D20','FF876E50','FF877420'],'far':['FF876D20','FF876E50','FF876E80','FF876F40','FF877420'],'arena0':['FF876D20','FF877420']}[label]
    assert [r['entry'] for r in branch]==expected and all(r['id']==str(own) for r in branch)
    if label=='far':assert int(branch[-1]['a3'],16)>72
    end=rows['REJECT_END'][0];assert end['mode']=='3' and end['arena']==str(arena+1) and int(end['frame'])==begin+1100
    result=rows['RESULT'][0];assert result['action']==result['action_arena']=='-1' and result['damage']=='322' and result['kos']=='2'
    return dict(nativeRejectionBranch=expected,earnedMatches=arena+1,commandFrame=begin,nextArena=arena+1)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('fighter',choices=['kano','sonya']);parser.add_argument('side',type=int,choices=[1,2]);parser.add_argument('label',choices=['wrong','far','arena0']);args=parser.parse_args()
    source=sync.verify();name=f'{args.fighter}_p{args.side}_{args.label}'
    folder=sync.ROOT/f'audit_current_native_stage_reject_{name}_runtime';out=sync.ROOT/f'audit_current_native_stage_reject_{name}_checked';assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text());assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['elapsedSeconds']<=90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_native_tomb_preparation/stage.lua')
    assert not (folder/'stderr.log').read_text().strip() and not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
    rows=load(folder/'run.log');proof=gate(rows,args.fighter,args.side,args.label)
    bad=copy.deepcopy(rows);bad['ENTRY'].append(dict(bad['ENTRY'][-1],entry='FF8BDFE0'))
    try:gate(bad,args.fighter,args.side,args.label)
    except AssertionError:pass
    else:raise AssertionError('False action accepted')
    report=dict(passed=True,sourceSync=source,terminal=terminal,rejection=proof,falseStageActionRejected=True,logSHA256=sync.sha(folder/'run.log'),fullPortAcceptance=False,
        scope='Current earned full-health native matches and exact history/range/arena rejection branch; no stage action and clean next-arena return. Not all roles/commands/arenas, DeadPool acid finisher, raster/audio or release acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,case=name,rejection=proof)))

if __name__=='__main__':main()
