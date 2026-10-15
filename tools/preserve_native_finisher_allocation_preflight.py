"""Preserve rejected source-only allocation; it was never compiled or run."""
import gzip,json
from pathlib import Path
import native_ai_response_context as native
ROOT,need,sha=native.ROOT,native.need,native.sha
if __name__=='__main__':
    folder=ROOT/'audit_native_cpu_finisher_allocation_preflight_failure'
    need(not folder.exists(),'Fresh rejected preflight archive')
    paths=[ROOT/'tools/qualify_native_cpu_finisher_dispatch_source.py',
           ROOT/'source_native_cpu_finisher_dispatch/midtunit_m.cpp']
    sources={str(p):dict(sha256=sha(p),text=p.read_text())for p in paths}
    guest=native.expected()
    need(guest[0xf3a00:0xf3a4c]!=b'\xff'*76,'Actual initialized Bicycle tick overlaps rejected table allocation')
    need(guest[0xf4320:0xf43b8]==b'\xff'*152,'Both replacement tables fit whole genuinely erased span')
    folder.mkdir()
    with gzip.open(folder/'rejected_uncompiled_sources.json.gz','wt',encoding='utf-8')as stream:json.dump(sources,stream)
    (folder/'report.json').write_text(json.dumps(dict(passed=False,sourcePreflightRejected=True,
        reason='Proposed F39F4/F3A40 tables overlap existing Sonya Bicycle tick beginning F3A00.',
        proposedReplacementByteSpan='F4320-F43B8',wholeReplacementSpanErased=True,
        gameBuildsProduced=0,nativeRunsOfRejectedProposal=0,publicBuildChanged=False,
        fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
    print('Rejected source allocation frozen; zero builds/runs; verified replacement152-byte span.')
