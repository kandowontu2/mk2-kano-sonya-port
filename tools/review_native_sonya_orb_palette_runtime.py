"""Preserve earned native successes AND the real winner-time cloud failure.

No build, guest writes, ROM/raw-media copy, or public promotion. All 45
actual native rasters were inspected in RAM; the replay's 15 digests also
equal the original repaired P1 run byte-for-byte. Allocation reuse is not
mistaken for continued ownership or a second retirement.
"""
import gzip
import hashlib
import json
import re
import subprocess
from pathlib import Path
import qualify_native_sonya_orb_palette as source

ROOT=source.ROOT
OUT=ROOT/'audit_native_sonya_orb_palette_runtime_review'
RUNS=('audit_native_sonya_orb_repaired_p1',
      'audit_native_sonya_orb_lifetime_trace_p2',
      'audit_native_sonya_orb_mass_trace_p1')
need,sha=source.need,source.sha

def fields(line):return dict(re.findall(r'(\w+)=([^\s]+)',line))
def rows(text,tag):return [fields(l) for l in text.splitlines() if l.startswith('MK2_ORB_'+tag+' ')]

def mass_contract(text):
    spawned=rows(text,'TASK');clouds=[r for r in spawned if r['kind']=='smoke']
    need(len(clouds)==3 and len({r['job'] for r in clouds})==3,'Three real independent cloud births')
    targets={r['job']:r['actor'] for r in clouds}
    mass=[r for r in rows(text,'MASS') if r['pc']=='FF80E550' and r['known']=='smoke']
    need(len(mass)==3 and {r['target']:r['actor'] for r in mass}==targets,
         'Actual mass-unlink selects every same-allocation cloud exactly once')
    need(all(r['age']=='198' and r['match']=='00000100' and r['mask']=='FFFFFFFF' and
             r['type']=='0100' and r['ip']=='FF83C3D0' and r['active']=='yes' and r['free']=='no'
             for r in mass),'Winner-time exact native100 process deletion while all clouds still animate')
    entries=[r for r in rows(text,'MASS') if r['pc']=='FF80E450' and r['age']=='198' and r['match']=='00000100']
    need(len(entries)==1 and entries[0]['caller']=='FF8204E0', 'Actual native FF8204B0 caller, not inferred from single-process deletion')
    life=rows(text,'LIFETIME')
    before=[r for r in life if r['age']=='197']
    need(len(before)==3 and all(r['active']=='yes' and r['free']=='no' and r['cursor']=='FFD6F8C0' and
         r['actor']==targets[r['job']] for r in before),'All three actual cloud allocations alive immediately before unlink')
    after=[r for r in life if r['age']=='198']
    orphan=[r for r in after if r['actor']==targets[r['job']]]
    reused=[r for r in after if r['actor']!=targets[r['job']]]
    need(len(orphan)==2 and all(r['active']=='no' and r['free']=='yes' and r['cursor']=='FFD6F8C0' for r in orphan) and
         len(reused)==1 and reused[0]['active']=='yes' and reused[0]['free']=='no' and reused[0]['ip']=='FF8413B0',
         'Two real freed cloud tasks plus one reused native text allocation, not three surviving animation tasks')
    return dict(cloudBirths=clouds,actualMassUnlinks=mass,actualWinnerDeletionCaller=entries,
                beforeWinner=before,afterWinner=after,originalCloudAllocationReusedForText=reused,
                cloudCleanupAccepted=False)

def decode(file,address,bits):
    return subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'),str(file),'-arch','tms34010',
        '-basepc',hex(address),'-skip',hex((address-0xff800000)//8),'-count',str(bits),'-norawbytes'],
        text=True,capture_output=True,check=True).stdout

def main():
    need(not OUT.exists() and not source.prior.prior.prior.visual.native.census(),'Fresh evidence; native games actually terminal')
    OUT.mkdir();reviews=[];pins={}
    for name in RUNS:
        folder=ROOT/name;report=json.loads((folder/'report.json').read_text());text=gzip.open(folder/'run.log.gz','rt').read()
        need(report['passed'] and report['transportOnlyAccepted'] and report['nativeExit']==0 and
             report['wholeGuestMatched'] and not report['finisherAccepted'] and
             all(sha(p)==h for p,h in report['inputHashes'].items()), 'Exact actual native test and executed inputs conserved')
        entry=rows(text,'ENTRY');winner=rows(text,'WINNER');stop=rows(text,'STOP');frame=rows(text,'RGB_DIGEST')
        need(len(entry)==len(winner)==len(stop)==1 and entry[0]['gap']=='256' and
             winner[0]['age']=='197' and stop[0]['bones']=='32' and stop[0]['clouds']=='3' and stop[0]['mode']=='3' and
             len(frame)==15 and not rows(text,'OVERRUN'),'Genuinely earned command, native winner/continue, all rasters, no old overrun')
        pal=rows(text,'PALETTE');need(len(pal)==3 and all(r['source']=='FFD7B400' for r in pal),'Actual owned magenta palette, not stale body palette')
        original=(ROOT/'mk3/mk3-maincpu.bin').read_bytes();at=(0xff83f6f0-0xff800000)//8
        colors=','.join(f'{int.from_bytes(original[i:i+2],"little"):04X}' for i in range(at+2,at+66,2))
        need(all(r['active']==colors for r in pal),'All32 actual active colors match original source through every sampled phase')
        cursor=rows(text,'CURSOR');need(cursor and all(r['a9']!='FFD6C0A0' for r in cursor),'Native repaired cursor never consumes known filler slot')
        child=rows(text,'CHILD');need(child and int(child[-1]['age'])<182,'Owned orb child retires before winner')
        cleanup=[r for r in rows(text,'CLEANUP') if r.get('job')==next(r['job'] for r in rows(text,'TASK') if r['kind']=='worker')]
        need({r['kernel'] for r in cleanup}=={'FF83EFD0','FF840450','FF80E0E0'},'Real orb object/palette/cache cleanup reached')
        reviews.append(dict(name=name,physicalSlot=report['side'],actualNativeProcess=report['actualWindowsIdentity'],
             entry=entry,winner=winner,stop=stop,frames=frame,actualNativeFramesVisuallyReviewed=15,
             activePalette=pal,cursorSamples=len(cursor),orbCleanup=cleanup,cloudCleanupAccepted=False))
        for p in (folder/'report.json',folder/'run.log.gz',folder/'executed_sources.json.gz'):pins[str(p)]=sha(p)
    need([r['sha256'] for r in reviews[0]['frames']]==[r['sha256'] for r in reviews[2]['frames']],
         'All15 actual mass trace rasters equal independently inspected first repaired P1 rasters')
    text=gzip.open(ROOT/RUNS[2]/'run.log.gz','rt').read();failure=mass_contract(text)
    faults=[]
    for name,wrong in [('wrong_mask',text.replace('mask=FFFFFFFF target=0107CDC0','mask=FFFFFF00 target=0107CDC0')),
        ('wrong_actual_actor',text.replace('target=0107CDC0 type=0100 actor=01030030','target=0107CDC0 type=0100 actor=010335D0')),
        ('not_freed',text.replace('active=no free=yes','active=yes free=no'))]:
        try:mass_contract(wrong)
        except ValueError as e:faults.append(dict(name=name,rejected=str(e)))
        else:raise ValueError('Invalid allocation/deletion trace accepted: '+name)
    mk2=ROOT/'mk2/mk2-maincpu.bin';mk3=ROOT/'mk3/mk3-maincpu.bin'
    disassembly=dict(nativeWinner=decode(mk2,0xff820340,0x240),
        nativeMaskedDelete=decode(mk2,0xff80e450,0x1d0),
        nativeExactDeleteWrapper=decode(mk2,0xff840020,0x50),
        nativeEffectDispatcher=decode(mk2,0xff9a5b00,0x180),
        nativeCompoundEffect=decode(mk2,0xff9ad600,0x180),
        originalSonyaIndependentBurst=decode(mk3,0xff9aeec0,0x90))
    need('MOVI   100h,A0' in disassembly['nativeWinner'] and 'CALLA  FF840020h' in disassembly['nativeWinner'] and
         'JA     FF80E450h' in disassembly['nativeExactDeleteWrapper'] and
         'MOVE   *A2,*A3,1' in disassembly['nativeMaskedDelete'] and
         'MOVI   201h,A1' in disassembly['nativeEffectDispatcher'] and
         'MOVI   201h,A1' in disassembly['nativeCompoundEffect'] and
         'MOVI   201h,A1' in disassembly['originalSonyaIndependentBurst'], 'Actual native masked deletion and same native201 effect category')
    prior=json.loads((source.OUT/'report.json').read_text())
    for p in (Path(__file__),mk2,mk3,source.OUT/'report.json',ROOT/'PLAY_LATEST_KANO_SONYA.cmd'):pins[str(p)]=sha(p)
    result=dict(passed=True,evidenceReviewAccepted=True,finisherAccepted=False,fullPortAcceptance=False,
        previousGoalTurnClassification='no progress: user-requested status restatement only',
        thisGoalTurnClassification='progress: native P1/P2 cursor/palette/winner cleanup verified; actual native winner-time mass unlink proves three cloud tasks prematurely killed; next correction is native independent effect category201',
        nativeRuns=reviews,totalActualFramesVisuallyReviewed=45,actualFailure=failure,
        actualFaultsRejected=faults,nativeDisassembly=disassembly,
        originalNaturalIntegrationRequirements=prior['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=prior['originalRemainingWorkGroups'],inputHashes=pins,
        goalStatus='active',latestPlayableChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        limitations=['Finite gap256 own Sonya/Kano tests only; finisher still incomplete, including original victim flash and audio.',
           'Clouds freeze through winner/continue; earlier effect tracking mislabels reused allocations as repeated bones.',
           'Long-distance worker lifetime, additional victims, CPU, Kano laser and full release gates remain unaccepted.'])
    (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(passed=True,runs=3,reviewedFrames=45,cloudsActuallyUnlinked=3,finisherAccepted=False)))

if __name__=='__main__':main()
