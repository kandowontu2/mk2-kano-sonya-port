"""Unchanged accepted controller roles plus a strictly read-only ending observer."""
import json,re,subprocess
from pathlib import Path
import qualify_kano_current_p2_campaign_source_v4482 as kano
import qualify_kintaro_pressure_guard_long_source_v4437 as sonya
ROOT,need,sha=kano.ROOT,kano.need,kano.sha
OBSERVER='mk2ks_native_ending_audio_observer_ram_v4495.lua'
LUA={'kano':'mk2ks_kano_ending_audio_campaign_ram_v4496.lua','sonya':'mk2ks_sonya_ending_audio_campaign_ram_v4497.lua'}
OUT=ROOT/'audit_v4502_native_ending_audio_source_preflight'
TRANSITIVE_LUA=tuple(sorted(set(kano.TRANSITIVE_LUA+sonya.TRANSITIVE_LUA+tuple(LUA.values())+(OBSERVER,))))

def source_boundary(fighter):
    need(fighter in LUA,'Only both original real character/slot contexts')
    parent=kano if fighter=='kano' else sonya
    proof=parent.source_boundary()
    expected='-- Existing accepted controller unchanged; only a new read-only sound observer.\n'+\
             f"dofile('{parent.LUA}')\ndofile('{OBSERVER}')\n"
    need((ROOT/LUA[fighter]).read_text()==expected,'Exact declared existing controller and one additional observer')
    text=(ROOT/OBSERVER).read_text()
    need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|set_value|clear_value|return\s+data|io\.open|snapshot\(|machine:exit',text),
         'Observer cannot provide controls/guest/health/IDs/AI/positions/palette/RNG/audio files or exits')
    need(not re.search(r'dofile\(|loadfile\(|\bload\(',text),'No hidden observer dependencies or delegated code')
    need('cpu.PC.value~=0xff836700' in text and 'cpu.PC.value~=0xff8296b0' in text and
         'cpu.PC.value~=at+16' in text and "dsp.spaces.data:install_read_tap(0x3400,0x37ff" in text and
         "manager.machine.sound:get_samples()" in text and "for n=0,13 do" in text,
         'Actual original collision/winner/fetch/DSP provenance, complete mixed PCM and all14 sample states')
    return dict(passed=True,fighter=fighter,physicalSlot=2,controller=parent.LUA,
                originalControllerProof=proof,observerSHA256=sha(ROOT/OBSERVER),physicalInputsExactlyUnchanged=True,
                nativeWindowChosenByActualOriginalFinalCollision=True,nativeWindowNeverSuppliesVictory=True,
                rawNativePCMGuestRGBRemainRAMOnly=True,endingAudioAcceptance=False,fullPortAcceptance=False)

if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable source preflight before new native windows')
    contexts=[source_boundary(f) for f in ('kano','sonya')]
    files=[Path(__file__).resolve(),Path(kano.__file__).resolve(),Path(sonya.__file__).resolve(),
           ROOT/'tools/run_native_ending_audio_campaign_ram_v4498.py',
           ROOT/'audit_v4488_kano_current_p2_whole_campaign_checked/report.json',
           ROOT/'audit_v4443_kintaro_pressure_guard_long_whole_campaign_checked/report.json']+[ROOT/p for p in TRANSITIVE_LUA]
    for p in files[4:6]:need(json.loads(p.read_text())['passed'],'Already qualified native full tower, not an assumed cold outcome')
    report=dict(passed=True,contexts=contexts,inputHashes={str(p.resolve()):sha(p) for p in files},fullPortAcceptance=False)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,
                    'New source proof compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='inputHashes'},indent=2),flush=True)
