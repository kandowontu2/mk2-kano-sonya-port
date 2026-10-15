"""Retain the real finite native demo miss; never label muted roll as audible."""
import gzip
import json
import re
import subprocess
from pathlib import Path
import native_ai_response_context as current
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha

def rows(text,tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in text.splitlines() if line.startswith(tag+' ')]

def main():
    folder=ROOT/'audit_native_attract_audible_kano'
    output=folder/'finite_native_attempt.json'
    need(not output.exists() and not native.census(),'Original actual native job fully terminal, fresh immutable attempt record')
    report=json.loads((folder/'report.json').read_text())
    with gzip.open(folder/'run.log.gz','rt',encoding='utf-8') as f:text=f.read()
    need(report['passed'] and report['requestedConfigurationAccepted'] and report['nativeTerminal']['nativeExit']==0 and
        not report['nativeTerminal']['hostDecodeErrors'],'Actual normal native terminal and correct physical timing')
    need([(int(r['frame']),r['value']) for r in rows(text,'MK2_ATTRACT_INPUT')]==
        [(f,'1') for f in range(480,484)]+[(484,'0')],'Exact four ordinary High Punch fields and release')
    need(not rows(text,'MK2_ATTRACT_RESET') and not rows(text,'MK2_ATTRACT_ERROR_ENTRY'),
        'No actual native reset or executed error throughout the complete attempt')
    sounds=rows(text,'MK2_ATTRACT_SOUND')
    rolls=[r for r in sounds if r['word']=='6B03']
    need(len(rolls)==1 and rolls[0]['mode']=='1' and rolls[0]['mute']=='1' and rolls[0]['pc']=='FFFFDEC0' and
        rolls[0]['p2_roster']==rolls[0]['p2_id']=='17' and rolls[0]['p2_action']=='523' and
        rolls[0]['p2_actor']==rolls[0]['p2_owner']==rolls[0]['a8'] and rolls[0]['p2_main']==rolls[0]['a13'],
        'Actual true Kano17 CPU roll occurs only under original native mute policy')
    channels=rows(text,'MK2_TOMB_MIX_CHANNEL')
    roll_sources=[r for r in channels if int(r['frame'])>=int(rolls[0]['frame']) and int(r['channel']) in (10,11,12,13)]
    need(roll_sources and all(r['sample']=='4294967295' and r['length']=='0' and float(r['position'])==0 and
        r['bits']=='0000000000000000' and r['loop']==r['paused']==r['writes']=='0' for r in roll_sources),
        'All actual muted startup sources remain completely inactive through the captured roll window')
    guest=current.expected()
    digest=rows(text,'MK2_ATTRACT_GUEST_DIGEST')
    need(len(digest)==1 and digest[0]['sha256']==__import__('hashlib').sha256(guest).hexdigest().upper(),
        'Whole original actual compiled guest identity unchanged')
    need(all(sha(path)==value for path,value in report['inputHashes'].items()),'Every actual native/controller input intact')
    result=dict(passed=False,audibleKanoAttractRollAccepted=False,transportOnlyAccepted=True,
        reason='Native Kano roll was reached only after the stock attract sequence muted demo sound; no unmuted Kano roll occurred.',
        nativeTerminal=report['nativeTerminal'],actualRoll=rolls[0],mutedSourceStatesChecked=len(roll_sources),
        actualOwnDemoAdmissions=rows(text,'MK2_ATTRACT_DEMO_OWNER'),actualPhysicalInputs=report['actualPhysicalInputs'],
        result=rows(text,'MK2_ATTRACT_RESULT'),fullPortAcceptance=False,goalStatus='active',
        previousGoalTurnClassification='progress: current four-case selection/ladder/match and full sixteen-case special matrix qualified',
        thisGoalTurnClassification='progress: one real different-opponent native demo route finished, muted Kano roll suppression checked; audible path remains unproved',
        rawAudioQualification=False,hostRAMReleased=True,
        hostObservationLimit='Host was launched without a PTY; its InteractiveConsole received EOF after native termination. PCM/DAC remain digest-only in the log, not retained audio carriers.',
        nextAction='Use a fresh ordinary physical timing variant and an explicitly retained PTY host; never replay this completed attempt or count its muted roll as audible.',
        inputHashes={**report['inputHashes'],str(folder/'report.json'):sha(folder/'report.json'),
            str(folder/'run.log.gz'):sha(folder/'run.log.gz'),str(Path(__file__).resolve()):sha(__file__)},
        newNativeBoots=1,newBuilds=0,newROMCopies=0,newRawAudioCopies=0,newZIPs=0)
    output.write_text(json.dumps(result,indent=2)+'\n')
    storage=[]
    for path in [p for p in folder.rglob('*') if p.is_file()]:
        need(path.resolve().is_relative_to(ROOT) and not path.is_symlink(),'Exact bounded proof leaf')
        digest=sha(path)
        subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],check=True,capture_output=True)
        need(sha(path)==digest,'Actual native attempt evidence unchanged by compression')
        storage.append(dict(path=str(path),sha256=digest,allocatedBytes=allocated(path)))
    (folder/'storage_receipt.json').write_text(json.dumps(dict(passed=True,exactFiles=storage,newBuilds=0,newROMCopies=0),indent=2)+'\n')
    print(json.dumps(dict(audibleKanoAccepted=False,nativeExit=0,mutedSourceStates=len(roll_sources),
        allocatedEvidenceBytes=sum(r['allocatedBytes'] for r in storage))),flush=True)

if __name__=='__main__':main()
