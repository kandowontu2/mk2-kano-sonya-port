"""Merge eight bounded current CPU displayed grabs with full current evidence."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def need(ok,label):
    if not ok:raise ValueError(label)


def main():
    out=ROOT/'audit_v841_current_cpu_display_checkpoint'
    need(not out.exists(),'Refusing to overwrite evidence')
    inputs={};reports={}
    def track(path,wanted=None):
        path=Path(path).resolve();sha=hashlib.sha256(path.read_bytes()).hexdigest().upper()
        need(wanted is None or sha==wanted,'Pinned input changed: '+str(path))
        need(str(path)not in inputs or inputs[str(path)]==sha,'Inconsistent evidence hash')
        inputs[str(path)]=sha
    track(__file__)
    names=('audit_v837_current_cpu_pair_checkpoint','audit_v839_current_cpu_ordinary_leg_checked',
           'audit_v840_current_cpu_ordinary_leg_units')
    for name in names:
        path=ROOT/name/'verification.json';track(path);proof=json.loads(path.read_text());reports[name]=proof
        need(proof['fullPortAcceptance']is False,'Do not promote whole-port scope')
        for path,wanted in proof.get('checked_inputs',proof.get('inputHashes',{})).items():track(path,wanted)
    prior,current,units=(reports[name]for name in names)
    need(current['passed']and len(current['cases'])==3 and not current['CPU_acceptance'],'Three bounded displayed leg paths')
    for name,case in current['cases'].items():
        need(name.startswith('audit_v838_')and case['passed']and case['paired']['passed'],'Actual current captures pass')
        need(case['paired']['target']=='sonya'and case['paired']['native_followup']['kind']=='ordinary',
             'Genuine CPU Sonya leg and ordinary continuation')
        need(all(r['vram_mismatches']==r['displayed_mismatches']==0 for r in case['records']),
             'Every retained native pass and scanout exact')
    need(units['passed']and units['methods']==22 and units['baseline_cases']==3,'Current ordinary leg checker methods')
    path=ROOT/names[2]/'unit-tests.log';track(path);text=path.read_text()
    need('Ran 22 tests'in text and text.rstrip().endswith('OK'),'Actual successful test log')
    frames=prior['sampledFrames']+sum(c['sampled_frames']for c in current['cases'].values())
    pixels=prior['exactDisplayedPixels']+sum(c['exact_screen_pixels']for c in current['cases'].values())
    bodies=prior['exactBodyPixels']+sum(c['exact_body_pixels']for c in current['cases'].values())
    fields=prior['pairedFields']+sum(c['paired']['paired_fields']for c in current['cases'].values())
    need((frames,pixels,bodies,fields)==(687,69799200,3955761,882),'Actual aggregate current evidence')
    report={**{k:value for k,value in prior.items()if k not in('checked_inputs','checked_input_count')},
            'checked_inputs':inputs,'checked_input_count':len(inputs),'currentCpuDisplayedGrabCases':8,
            'sampledFrames':frames,'exactDisplayedPixels':pixels,'exactBodyPixels':bodies,'pairedFields':fields,
            'newCheckerUnitMethods':81,
            'limits':['eight actual current P1 CPU choke/leg paths: five ordinary and three square follow-ups',
                      '687 sampled passes, not unsampled rendering or complete inter-pass cleanup',
                      'no current CPU bicycle follow-up claim; historical failed expectation retained',
                      'not all CPU moves/victims/slots/interruptions/KO/art/audio or full-port acceptance']}
    out.mkdir();(out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k]for k in('checked_input_count','currentCpuDisplayedGrabCases','sampledFrames',
                                       'exactDisplayedPixels','newCheckerUnitMethods','fullPortAcceptance')},indent=2))


if __name__=='__main__':main()
