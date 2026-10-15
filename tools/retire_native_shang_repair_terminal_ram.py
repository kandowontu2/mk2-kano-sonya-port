"""Release already qualified original terminal campaign RAM, never a live game."""
import json
import os
from pathlib import Path
import qualify_native_shang_repair_terminal_sampled as checked

def retire(ram):
    need,sha,root=checked.original.need,checked.original.sha,checked.ROOT
    out=root/'audit_native_shang_repair_terminal_ram_retirement'
    need(not out.exists() and os.getpid()==30848 and os.getppid()==35304 and
         ram['process'].poll()==0 and not checked.original.census.census(),
         'Exact original retained host; actual native terminal and no native emulator live')
    proof_path=checked.OUT/'report.json'
    proof=json.loads(proof_path.read_text())
    need(proof==ram['terminalRecoveryReport'] and proof['passed'] and
         proof['finiteSonyaNormalShrinkingCrashAndOrdinaryRecoveryAccepted'] and
         all(sha(p)==h for p,h in proof['inputHashes'].items()),
         'Actual entire original terminal chronology/window/route/raster evidence qualified and unchanged')
    text_bytes=len(ram['capture']['text'])
    images=len(ram['capture']['images'])
    need(text_bytes==531553099 and images==45,'Exact original bounded RAM ownership')
    native_identity=ram['identity']
    # Console failure diagnostics may also reference the captured objects;
    # normal host exit immediately after this releases all of those references.
    ram.clear()
    report=dict(passed=True,qualifiedReceiptSHA256=sha(proof_path),
        originalNativeIdentity=native_identity,nativeExit=0,hostPID=os.getpid(),
        hostParentPID=os.getppid(),releasedChronologyBytes=text_bytes,releasedRasterCount=images,
        RAMDictionaryCleared=True,normalHostExitRequired=True,newNativeBoots=0,
        newROMCopies=0,newRawMedia=0,publicPlayableChanged=False,fullPortAcceptance=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,releasedChronologyBytes=text_bytes,releasedRasterCount=images)),flush=True)
    return report
