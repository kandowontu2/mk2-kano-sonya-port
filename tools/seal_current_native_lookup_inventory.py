"""Retain current direct-immediate lookup inspection, distinct from runtime."""
import hashlib
import json
import subprocess
from pathlib import Path
import inspect_current_native_lookup_tables as inspection
import native_ai_response_full_context as current

def main():
    out = current.ROOT/'audit_native_current_lookup_inventory'
    current.need(not out.exists(), 'Fresh bounded static inspection receipt')
    rows = inspection.inspect()
    current.need(len(rows)==28 and all(row['relocated'] for row in rows),
        'All actual unchanged direct calls with adjacent long immediate table operands use extended tables')
    stock = current.ROOT/'mk2/mk2-maincpu.bin'
    current.need(current.sha(stock)=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23',
        'Entire original source for disassembly')
    paths = [Path(__file__),Path(inspection.__file__),Path(inspection.disasm.__file__),
        current.ROOT/'mame-mkp/unidasm.exe',stock,Path(current.__file__),
        current.ROOT/current.NAME/'mkport_candidate.exe',current.ROOT/current.NAME/'build-info.json']
    pins = {str(path.resolve()):current.sha(path) for path in paths}
    report = dict(passed=True, staticInventoryOnly=True, candidate=current.NAME,
        executableSHA256=current.EXE_SHA, guestSHA256=current.GUEST_SHA,
        actualUnreplacedImmediateLookupSites=len(rows), directImmediateTables=rows,
        obsoleteStockVictoryCallExcluded=True,
        limit='Only unchanged direct CALLA live-ID lookup sites with adjacent literal MOVI table operands. Dynamic/register-passed tables and runtime reachability are not proved by this inventory.',
        runtimeAcceptance=False, fullPortAcceptance=False, goalStatus='active',
        inputHashes=pins,newNativeBoots=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0)
    out.mkdir()
    path=out/'report.json'
    path.write_text(json.dumps(report,indent=2)+'\n')
    before=hashlib.sha256(path.read_bytes()).hexdigest()
    subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True,check=True)
    current.need(hashlib.sha256(path.read_bytes()).hexdigest()==before,'Lossless bounded static evidence retention')
    print(json.dumps(dict(passed=True,staticInventoryOnly=True,currentDirectImmediateSites=len(rows),
        runtimeAcceptance=False,newBuilds=0)),flush=True)

if __name__=='__main__':
    main()
