"""Keep actual terminal evidence; do not credit missing stale taps as no cast."""
import gzip,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def seal(captures):
    for fighter,c in captures.items():
        folder=ROOT/f'audit_native_block_freeze_setup_checked_{fighter}_p2'
        out=folder/'inconclusive_observer_receipt.json'
        assert not out.exists()
        terminal=json.loads((folder/'native_terminal.json').read_text())
        assert terminal['nativeExit']==c['meta']['nativeExit']==0
        fields=[dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in c['text'].splitlines() if line.startswith('MK2_NORMAL_FREEZE_FIELD ')]
        assert len(fields)==701 and len(c['images'])==4
        assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()==h for p,h in c['meta']['inputHashes'].items())
        receipt=dict(passed=False,transportPassed=True,blockingAccepted=False,launchAbsenceProven=False,
                     reason='Observer used stale FF86BB80/FF86BAB0 instead of actual FF86F9D0/FF8A5900 launch/setup sites.',
                     nativeExit=0,fieldCount=701,actualVictimIDs=sorted({r['victim_id'] for r in fields}),
                     actualVictimActions=sorted({r['action'] for r in fields}),
                     actualVictimHP=sorted({int(r['hp']) for r in fields}),
                     ramImageDigests=[hashlib.sha256(i.tobytes()).hexdigest().upper() for i in c['images']],
                     inputHashes=c['meta']['inputHashes'],fullPortAcceptance=False,newBuilds=0,newROMCopies=0)
        out.write_text(json.dumps(receipt,indent=2)+'\n')
    return dict(preserved=list(captures),blockingAccepted=False)
