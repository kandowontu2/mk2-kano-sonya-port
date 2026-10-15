"""Preserve finite secret/arena results and release retained test RAM.

No random misses are relabelled as successful secret encounters. Current
source equivalence and actual runtime results are kept separate.
"""
import gzip
import hashlib
import json
import re
import subprocess
from pathlib import Path
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated

ROOT = Path(__file__).resolve().parents[1]
KANO = 'audit_natural_smoke_route_kano_p1_native_toasty_decision'
SONYA = ('audit_natural_smoke_route_sonya_p2_native_toasty_rearmed_controls',
         'audit_natural_smoke_route_sonya_p1_native_toasty_final_round_controls')
OUT = ROOT/'audit_native_secret_progress_storage'


def need(value,message):
    if not value:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def visual(c):
    need(c['side'] == 1 and c['fighter'] == 'sonya' and c['terminal']['nativeExit'] == 0,
         'Actual terminal Sonya first-slot capture')
    headers = []
    for i in (16,54):
        frame = c['rgbFrames'][i]
        need(frame['header']['stage'] == 'portal_match.png' and
             hashlib.sha256(frame['pixels']).hexdigest().upper() == frame['header']['sha256'],
             'Whole actually viewed native Portal frame')
        headers.append(frame['header'])
    path = c['folder']/'finite_portal_visual_review.json'
    need(not path.exists(), 'Fresh finite visual receipt')
    result = dict(passed=True, actuallyViewedNativeFrames=headers,
                  observation='First and third Portal admissions show real Sonya/Kano bodies, matching names and floor shadows; no selector portraits or poses persist.',
                  allSceneVisualAcceptance=False, secretEncounterAccepted=False,
                  newRawMedia=0)
    path.write_text(json.dumps(result,indent=2)+'\n')
    return result


def misses(folder,side):
    with gzip.open(folder/'run.log.gz','rt',encoding='utf-8') as f:
        lines = f.read().splitlines()
    get = lambda line: dict(re.findall(r'(\w+)=([^\s]+)',line))
    decisions = [get(l) for l in lines if l.startswith('MK2_STAGE_TOASTY_DECISION ')]
    products = [r for r in decisions if r['entry'] == 'FF8DF120']
    frames = {int(r['frame']) for r in products}
    fields = {(int(r['frame']),int(r['slot'])):r for l in lines
              if l.startswith('MK2_STAGE_SECRET_FIELD ') and (r:=get(l)) and int(r['frame']) in frames}
    need(products and not any(l.startswith(('MK2_STAGE_TOASTY ','MK2_STAGE_SECRET_ACCEPT ')) for l in lines),
         'Actual finite Sonya attempts have no popup or accepted secret entry')
    observed = []
    for r in products:
        f, value = int(r['frame']),int(r['a0'],16)
        args = [a for a in decisions if a['entry']=='FF8DF0F0' and a['task']==r['task'] and a['frame']==r['frame']]
        need(len(args)==1 and args[0]['a0']=='00000028' and r['pc']=='FF8DF130' and
             40 <= value < 1000 and r['states']=='1,1' and r['actor']==fields[f,3-side]['actor'],
             'Actual original threshold40 native RNG miss belongs to the real opposite actor')
        need(fields[f,side]['id']==fields[f,side]['roster']=='18' and fields[f,3-side]['id']==fields[f,3-side]['roster']=='17',
             'Native random attempt retains real Sonya/Kano roles')
        observed.append(dict(frame=f,nativeRandomValue=value,originalTask=r['task'],actualPopup=False))
    return observed


def main():
    need(not OUT.exists() and not native.census(), 'Actual native jobs terminal, fresh bounded journal')
    kano = json.loads((ROOT/KANO/'native_secret_decisions_and_faults.json').read_text())
    need(kano['passed'] and len(kano['actualFaultsRejected'])==14 and
         len(kano['viewedNativeFrameHeaders'])==4, 'Actual Kano native secret entry and controls proof retained')
    exposurepath = ROOT/'audit_native_voice_priority_exposure/report.json'
    exposure = json.loads(exposurepath.read_text())
    need(exposure['passed'] and exposure['nativeQueueAllInputSourceEquivalence'] and
         len(exposure['actualSourceFaultsRejected'])==4 and not exposure['suppressionAndSpecial71RuntimeCoverage'],
         'Source equivalence does not relabel unobserved stock branch runtime coverage')
    cases, files = [], set()
    for name in (KANO,*SONYA):
        folder = ROOT/name
        transport = json.loads((folder/'report.json').read_text())
        terminal = transport['nativeTerminal']
        need(transport['passed'] and terminal['nativeExit']==0 and not terminal['hostDecodeErrors'], 'Actual clean native terminal')
        handle = native.k.OpenProcess(0x1000,False,terminal['actualWindowsIdentity']['ParentProcessId'])
        if handle:
            native.k.CloseHandle(handle)
            raise ValueError('Retained native test RAM host still live')
        with gzip.open(folder/'executed_sources.json.gz','rt',encoding='utf-8') as f:
            executed = json.load(f)
        for path,digest in transport['inputHashes'].items():
            if path in executed:
                need(digest==executed[path]['sha256']==hashlib.sha256(executed[path]['text'].encode()).hexdigest().upper(),
                     'Original whole executed text archived before later test edits')
            else:
                need(sha(path)==digest, 'Exact unchanged native/reference input')
        files.update(p for p in folder.rglob('*') if p.is_file())
        if name in SONYA:
            case = json.loads((folder/'arena_rotation_contract.json').read_text())
            need(case['passed'] and not case['actualSecretFightAccepted'] and len(case['actualFaultsRejected'])==7,
                 'Full finite Sonya physical/HP/ownership arena gate, never secret acceptance')
            side = case['physicalSlot']
            case = dict(fighter='sonya',side=side,nativeMatches=case['nativeMatches'],
                        earnedTwoWinWindows=case['earnedTwoWinWindows'],portalMatches=case['nativePortalMatches'],
                        wholePhysicalAndHealthLedger=case['wholePhysicalAndHealthLedger'],
                        actualFaultsRejected=7,nativeToastyMisses=misses(folder,side),
                        secretEncounterAccepted=False)
            cases.append(case)
    viewedpath = ROOT/SONYA[1]/'finite_portal_visual_review.json'
    viewed = json.loads(viewedpath.read_text())
    need(viewed['passed'] and len(viewed['actuallyViewedNativeFrames'])==2, 'Actual finite Sonya Portal visual review retained')
    files.update((exposurepath,ROOT/'tools/audit_native_voice_priority_exposure.py',Path(__file__).resolve()))
    targets = []
    for path in sorted(files):
        need(path.resolve().is_relative_to(ROOT) and not path.is_symlink() and
             path.suffix.lower() not in ('.exe','.mdata','.zip','.wav','.png','.bin','.pcm','.rgb'), 'Exact bounded evidence leaves only')
        digest,before = sha(path),allocated(path)
        subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True,check=True)
        need(sha(path)==digest, 'All retained evidence losslessly compressed')
        targets.append(dict(path=str(path),sha256=digest,beforeAllocatedBytes=before,allocatedBytes=allocated(path)))
    need(len([p for p in ROOT.iterdir() if p.is_dir() and (p/'mkport_candidate.exe').is_file()])==16 and
         'PLAY_CURRENT_V6508_CHECKED.cmd' in (ROOT/'PLAY_MK2_KANO_SONYA.cmd').read_text(), 'Compiled folders and public launcher unchanged')
    result = dict(passed=True,goalStatus='active',fullPortAcceptance=False,
                  previousGoalTurnClassification='no progress: user acknowledgement only',
                  thisGoalTurnClassification='progress: two terminal Sonya slot rotations checked with whole HP/identity/physical ledgers and fourteen corruption checks; native random misses distinguished from game failure; current native cue/queue source exposure resolved with four source mutations',
                  actualKanoSecretEntryAccepted=True,actualKanoSecretFaultsRejected=14,
                  actualSonyaResults=cases,actualSonyaMatches=sum(c['nativeMatches'] for c in cases),
                  actualSonyaSecretEntryAccepted=False,
                  compiledCandidate='diagnostic_v6640_kano_ball_launch',publicCandidate='PLAY_CURRENT_V6508_CHECKED.cmd',
                  unchangedNativeQueueSourceProof=str(exposurepath),
                  allRAMHostsReleased=True,selectedFiles=len(files),
                  allocatedBytes=sum(t['allocatedBytes'] for t in targets),exactCompressedTargets=targets,
                  remaining=['Actual Sonya secret admission/control verification; native random misses are not softlocks.',
                             'Concrete added-actor finisher/victim/cinematic ownership and teardown gaps, distinguished from unchanged stock queue branches.',
                             'Final combined current-candidate UI/gameplay/audio regression and matching runnable CMD/release ZIP.'],
                  originalObjectivePreserved=True,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0)
    OUT.mkdir()
    (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('passed','actualSonyaMatches','actualSonyaSecretEntryAccepted','allRAMHostsReleased','allocatedBytes','selectedFiles')}))


if __name__=='__main__':
    main()
