"""Replay accepted genuine cases on the exact new candidate; require equality.

Freshly revalidate original scoped proofs, then bind current cases to exact
unchanged physical/native observations, all hardware graphics/palettes and
all actual presented PNGs. Guest changes are restricted to intended head
descriptors proved independently by verify_rolling_heads_v1010.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
from PIL import Image
import verify_rolling_heads_v1010 as heads
import verify_native_torso_art_v980 as cage
import verify_native_inflation_art_v989 as kitana
import verify_native_death_grounding_v990 as reptile

ROOT=heads.ROOT
GROUPS=(
    (1005,979,'cage','rolling_head_regression','owned_torso','MK2_STOCK_HEAD_V921','MK2_CAGE_TORSO_V979',185),
    (1006,987,'kitana','rolling_head_regression','owned_inflation','MK2_STOCK_HEAD_V921','MK2_INFLATION_ART_V938',276),
    (1008,988,'','rolling_head_regression','native_death_grounding','MK2_REPTILE_V879','MK2_DEATH_ART_V897',187))


def rows(text,prefix):
    # Preserve the full source line, not a lossy dictionary whose duplicate
    # field names could hide a mismatched scenario or physical identity.
    return re.findall(r'^'+re.escape(prefix)+r'_.*$',text,re.M)


def verify(fresh_baselines=True):
    errors=[];pins={};cases={}
    def need(ok,message):
        if not ok:errors.append(message)
    if fresh_baselines:
        for name,module in (('Cage',cage),('Kitana',kitana),('Reptile',reptile)):
            proof=module.verify();need(proof['passed'],'Fresh authoritative baseline '+name)
            pins.update(proof.get('inputHashes',{}))
    guest,_=heads.verify_payload()
    for version,previous,killer,suffix,old_suffix,driver,observer,wrap_age in GROUPS:
        prefix=killer+'_' if killer else ''
        for name in ('kano','sonya'):
            for side in (1,2):
                current=f'audit_v{version}_{prefix}{name}_p{side}_{suffix}'
                older=f'audit_v{previous}_{prefix}{name}_p{side}_{old_suffix}'
                directory=ROOT/current;baseline=ROOT/older
                result=json.loads((directory/'result.json').read_text(encoding='utf-8-sig'))
                need(result['candidate']==heads.CANDIDATE and result['executable_sha256']==heads.EXE and result['payload_sha256']==heads.PAYLOAD,
                     current+': exact current candidate')
                need(result['exit_code']==0 and result['player']==name and result['victim_slot']==side and result['winner_slot']==3-side and
                     result['seconds']==95 and result['assistance']=='none' and result['cheats_enabled'] is False,
                     current+': terminal genuine physical-only scenario')
                for filename,wanted in result['input_hashes'].items():
                    path=Path(filename);need(path.is_file() and heads.digest(path)==wanted,'Frozen current input changed: '+filename);pins[filename]=wanted
                text=(directory/'run.log').read_text(encoding='utf-8-sig')
                old=(baseline/'run.log').read_text(encoding='utf-8-sig')
                need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|exception at',text,re.I),current+': no runtime errors')
                for tag in (driver,observer):
                    wanted=rows(old,tag);actual=rows(text,tag)
                    need(bool(wanted) and actual==wanted,current+': all genuine native '+tag+' observations unchanged')
                need((directory/'guest_maincpu.bin').read_bytes()==guest,current+': whole guest only intended rotating-head descriptors changed')
                blobs={p.name:p for p in directory.glob('*.bin') if p.name!='guest_maincpu.bin'}
                previous_blobs={p.name:p for p in baseline.glob('*.bin') if p.name!='guest_maincpu.bin'}
                need(set(blobs)==set(previous_blobs),current+': same observed initialized graphics/hardware palette set')
                for filename,path in blobs.items():
                    original=previous_blobs.get(filename)
                    need(original is not None and path.read_bytes()==original.read_bytes(),current+': actual unchanged graphics/palette '+filename)
                    pins[str(path)]=heads.digest(path)
                pictures={p.name:p for p in (directory/'snap').glob('*.png')}
                old_pictures={p.name:p for p in (baseline/'snap').glob('*.png')}
                # Cage's observer also saves the winner's unmodified poses;
                # retain those additional actual pictures, not only67 scoped
                # victim/periodic pictures counted by its previous verifier.
                need(len(pictures)>=(31 if killer=='' else 67) and set(pictures)==set(old_pictures),current+': complete unchanged native snapshot chronology')
                for filename,path in pictures.items():
                    original=old_pictures.get(filename)
                    need(original is not None and Image.open(path).size==(400,254) and path.read_bytes()==original.read_bytes(),
                         current+': actual presented PNG byte-identical '+filename)
                    pins[str(path)]=heads.digest(path)
                for filename in ('run.log','result.json','guest_maincpu.bin'):
                    path=directory/filename;pins[str(path)]=heads.digest(path)
                cases[current]=dict(previousAcceptedCase=older,unchangedNativeWrapAge=wrap_age,
                                    actualIdenticalPNGs=len(pictures),identicalGraphicsAndPaletteDumps=len(blobs),
                                    physicalInputsAndAllNativeObservationsIdentical=True)
    need(len(cases)==12,'All three established actions, both real victims and physical slots')
    return dict(passed=not errors,errors=sorted(set(errors)),cases=cases,inputHashes=pins,
                normalDeadPoolCageKitanaReptileRegressionsAccepted=not errors,
                selectedActualPNGs=sum(c['actualIdenticalPNGs'] for c in cases.values()),
                priorControlledAlternateDiagnosticTransferredAsNaturalAcceptance=False,
                alternateCostumesAccepted=False,allArenasAccepted=False,allStockFatalitiesAccepted=False,fullPortAccepted=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    if args.output.exists():raise ValueError('Preserve current replay evidence')
    report=verify();args.output.mkdir();(args.output/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='inputHashes'},indent=2))
    raise SystemExit(0 if report['passed'] else 1)
