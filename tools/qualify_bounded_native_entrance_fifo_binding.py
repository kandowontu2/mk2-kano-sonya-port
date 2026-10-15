"""Complete sparse FIFO-to-DMA census, including temporary entrance palette."""
import json
import qualify_bounded_native_sole_fifo_binding as old
BASE=old.ROOT/'audit_bounded_native_entrance_dma_runtime'
def main():
    out=BASE/'entrance_fifo_check.json';assert not out.exists()
    terminal=json.loads((BASE/'terminal.json').read_text());assert terminal['exitCode']==0 and not terminal['limitReason']
    tags=('MK2_BOUNDED_SOLE_FIFO','MK2_BOUNDED_SOLE_DMA','MK2_BOUNDED_SOLE_UNMATCHED','MK2_BOUNDED_STANCE_PART')
    data={k:[] for k in tags};entrance=[]
    with (BASE/'run.log').open() as stream:
        for line in stream:
            assert len(line)<1048576 and '[LUA ERROR]' not in line
            tag=line.split(' ',1)[0].strip();r=dict(old.RX.findall(line))
            if tag in data:data[tag].append(r)
            elif tag=='MK2_BOUNDED_ENTRANCE_DMA':entrance.append(r)
    assert len(entrance)==4
    added=[]
    for r in entrance:
        if any(d['frame']==r['frame'] and d['source']==r['source'] for d in data['MK2_BOUNDED_SOLE_DMA']):continue
        q=[q for q in data['MK2_BOUNDED_SOLE_FIFO'] if q['frame']==r['frame'] and q['source']==r['source']]
        assert len(q)==1 and q[0]['slot']=='2' and q[0]['id']=='18'
        assert r['raw_palette']=='0606' and r['bank']=='0600'
        d=dict(r,slot=q[0]['slot'],id=q[0]['id'])
        data['MK2_BOUNDED_SOLE_UNMATCHED'].append(d);added.append(d)
    assert [r['source'] for r in added]==['108E07BC','108E2696']
    positive=old.gate(data)
    report=dict(passed=True,nativeExit=0,peakWorkingSetBytes=terminal['peakWorkingSetBytes'],
        allThirtySparsePublishedCopiesBound=positive['allObservedBodyCopiesBound']==30,
        temporaryEntrancePaletteBank='0600',entranceOwnershipFromActualFIFO=True,
        graphicalStandingSoleParityAccepted=False,fullGoalComplete=False,
        sourceSync=old.sync.verify(),logSha256=old.sync.sha(BASE/'run.log'))
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('sourceSync','logSha256')}))
if __name__=='__main__':main()
