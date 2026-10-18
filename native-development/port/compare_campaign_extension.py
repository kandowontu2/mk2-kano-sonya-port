"""Exact common trace for an observation-limit extension, not outcome proof."""
import csv
import hashlib
import io
import json
from pathlib import Path
import sys

def verify_profiles(first,second,end):
    old,new=first['testArguments'],second['testArguments']
    assert '--campaign-full' in old and '--campaign-full' in new
    assert end['reason']=='field-budget'
    if '--campaign-ending-window' in old:
        assert '--campaign-finale-window' not in old and '--campaign-finale-window' in new
        assert old==[value for value in new if value!='--campaign-finale-window']
        assert end['frame']=='150000'
        return dict(extensionType='150000-to-180000-fields')
    if '--campaign-extended' not in old:
        assert '--campaign-extended' in new
        assert old==[value for value in new if value!='--campaign-extended']
        assert end['frame']=='90000'
        return dict(extensionType='90000-to-120000-fields')
    assert '--campaign-ending-window' not in old and '--campaign-ending-window' in new
    assert '--campaign-extended' in new and end['frame']=='120000'
    def cap(args):
        limits=[int(arg.split('=',1)[1]) for arg in args if arg.startswith('--campaign-continues=')]
        assert len(limits)==1
        limit=limits[0]
        assert 0<=limit<=(32 if '--campaign-extra-continues' in args else 20)
        return limit
    old_cap,new_cap=cap(old),cap(new)
    assert old_cap<=new_cap
    def strategy(args):
        return [arg for arg in args if arg not in ('--campaign-ending-window','--campaign-extra-continues')
                and not arg.startswith('--campaign-continues=')]
    assert strategy(old)==strategy(new), 'Physical strategy changed'
    return dict(extensionType='120000-to-150000-fields',previousContinueLimit=old_cap,
                newContinueLimit=new_cap,paidContinueBudgetChanged=old_cap!=new_cap)


def compare(previous,extended):
    assert previous and extended and previous[0]==extended[0], 'Columns changed'
    assert len(extended)>len(previous), 'No extended observations'
    assert extended[:len(previous)]==previous, 'Earlier trace changed'
    old=list(csv.DictReader(io.StringIO(''.join(previous))))
    new=list(csv.DictReader(io.StringIO(''.join(extended))))
    assert old and new and int(new[-1]['frame'])>int(old[-1]['frame'])
    return dict(identicalPreviousDataRows=len(old),identicalThroughFrame=int(old[-1]['frame']),
                prefixSHA256=hashlib.sha256(''.join(previous).encode()).hexdigest().upper(),
                extendedThroughFrame=int(new[-1]['frame']),extendedOutcomeVerified=False)

if __name__=='__main__':
    base=Path(__file__).resolve().parent.parent/'baseline'
    assert len(sys.argv)==3
    folders=[base/name for name in sys.argv[1:]]
    receipts=[]
    for folder in folders:
        receipt=json.loads((folder/'execution.json').read_text())
        assert receipt['exitCode']==0 and not receipt['timedOut']
        assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
        assert receipt['controllerSHA256']==hashlib.sha256((folder/'autoboot.lua').read_bytes()).hexdigest().upper()
        receipts.append(receipt)
    first,second=receipts
    assert first['replacementChips']==second['replacementChips']
    assert first['emulatorSHA256']==second['emulatorSHA256']
    end=dict(line.split('=',1) for line in (folders[0]/'campaign_end.txt').read_text().splitlines())
    profile=verify_profiles(first,second,end)
    report=compare(*[(folder/'campaign.csv').read_text().splitlines(keepends=True) for folder in folders])
    report.update(profile)
    report['runs']=[folder.name for folder in folders]
    paths=[p for folder in folders for p in (folder/'campaign.csv',folder/'execution.json',folder/'autoboot.lua')]
    paths.append(Path(__file__))
    report['pins']={str(p):hashlib.sha256(p.read_bytes()).hexdigest().upper() for p in paths}
    (folders[1]/'CAMPAIGN_EXTENSION_COMPARISON.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items() if key!='pins'}))
