"""Correct an unverified flash inference using source and actual original trace.

No source mutation, game, build, raw media or public promotion. The three
observed victim palette phases do not imply a visible palette flash: the
first color/bank change coincides with the original transparent victim.
FF9591E0 starts native camera tracking, not a palette animation process.
"""
import gzip
import json
import re
from pathlib import Path
import review_native_sonya_orb_palette_runtime as runtime

ROOT=runtime.ROOT
OUT=ROOT/'audit_native_sonya_orb_victim_palette_role'
need,sha=runtime.need,runtime.sha

def check(text):
    def rows(tag):return [runtime.fields(l) for l in text.splitlines() if l.startswith('MK3_SECONDARY_'+tag+' ')]
    palette=[r for r in rows('PALETTE_FIELD') if r['side']=='2']
    phases=rows('FIELD')
    need(len(palette)==len(phases)==451,'All451 actual original victim fields and whole palette observations')
    need(all(r['actor']=='010396C0' and r['bank']=='0700' and r['colors']==palette[0]['colors'] for r in palette[:168]),
         'Actual visible original Kano victim has one unchanged palette through initial stance, spin and crouch')
    changes=[r for i,r in enumerate(palette) if i==0 or r['colors']!=palette[i-1]['colors']]
    need([int(r['age']) for r in changes]==[1,169,170],'Actual palette changes only at or after transparent victim handoff')
    need(all(r['poses'].split(',')[1]=='FF840280' for r in phases[168:]) and
         phases[168]['bank'].split(',')[1]=='0808','Original victim has transparent group when palette bank changes and is later reused')
    return dict(visibleOriginalVictimUnchangedFields=168,
        actualPaletteChanges=[{k:r[k] for k in ('age','actor','bank')} for r in changes],
        victimPaletteFlashBeforeTransparentHandoffObserved=False,
        interpretation='Do not add an invented victim flash. Preserve the visible true-victim palette, correct hidden-victim teardown and separate effect palette ownership.')

def main():
    need(not OUT.exists(),'Fresh source/actual-reference interpretation evidence')
    OUT.mkdir()
    original=ROOT/'audit_native_secondary_sonya_source_distance'
    accepted=ROOT/'audit_native_sonya_orb_reference_checked/report.json'
    report=json.loads(accepted.read_text())
    need(report['passed'] and report['originalFiniteActionReferenceAccepted'] and
         all(sha(p)==h for p,h in report['inputHashes'].items()),'Original finite native source-distance reference unchanged')
    text=gzip.open(original/'run.log.gz','rt').read();result=check(text)
    mk3=ROOT/'mk3/mk3-maincpu.bin'
    assembly={f'{a:08X}':runtime.decode(mk3,a,n) for a,n in
        ((0xff9591e0,0x180),(0xff90c020,0x510),(0xff9ae4e0,0x90))}
    need('MOVI   FF90C020h,A7' in assembly['FF9591E0'] and
         'MOVI   FF9591E0h,A0' in assembly['FF9AE4E0'] and
         'MOVE   A0,@105D890h,1' in assembly['FF90C020'] and
         'MOVI   FF90BBF0h,A5' in assembly['FF90C020'],
         'Actual call chain starts actor-position-based native camera tracking, not palette effect animation')
    wrong=text.replace('age=118 side=2 actor=010396C0 bank=0700','age=118 side=2 actor=010396C0 bank=0800')
    try:check(wrong)
    except ValueError as error:fault=str(error)
    else:raise ValueError('Invented visible victim palette change admitted')
    pins={str(p):sha(p) for p in (Path(__file__),accepted,original/'run.log.gz',mk3)}
    result.update(passed=True,sourceAndReferenceInterpretationAccepted=True,nativeDisassembly=assembly,
        actualWrongVisiblePaletteFaultRejected=fault,inputHashes=pins,
        originalNaturalIntegrationRequirements=report['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=report['originalRemainingWorkGroups'],fullPortAcceptance=False,
        latestPlayableChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active',
        limitations=['Only actual original Sonya versus Kano reference. Broader port victim palettes, camera/arena placement and audio remain unaccepted.'])
    (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(passed=True,visibleVictimPaletteConservedFields=168,inventedFlashRejected=True)))

if __name__=='__main__':main()
