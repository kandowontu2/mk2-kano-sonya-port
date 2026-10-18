"""Require current recovery-verifier code and every recorded evidence pin."""
import hashlib
from pathlib import Path

PORT=Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def verify(folder,proof,verifier=None):
    verifier=verifier or PORT/'qualify_finisher_rejoin.py'
    pins=proof['evidenceSHA256']
    required=(folder/'execution.json',folder/'autoboot.lua',verifier)
    assert all(str(path) in pins for path in required),'Missing mandatory recovery evidence'
    assert proof['verifierSHA256']==sha(verifier),'Stale recovery verifier'
    for name,digest in pins.items():
        assert sha(Path(name))==digest,('Stale recovery evidence',name)
