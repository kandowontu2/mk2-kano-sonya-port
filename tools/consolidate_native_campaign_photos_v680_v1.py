"""Freeze current bounded native campaign and original-photo record evidence."""
import hashlib
import json
import re
from pathlib import Path
from verify_natural_campaign_v680_v2 import verify

ROOT=Path(__file__).resolve().parents[1]


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024),b''):h.update(block)
    return h.hexdigest().upper()


def need(ok,label):
    if not ok:raise ValueError(label)


if __name__=='__main__':
    out=ROOT/'audit_v707_native_campaign_photos_checked_inputs'
    need(not out.exists(),'Do not overwrite evidence')
    campaign=ROOT/'audit_v706_native_tower_kano_p1'
    report=verify(campaign)
    need(report['passed'] and not report['unassisted_clear_proven'] and
         report['stages_reached']==list(range(13))+[14,15],'Actual bounded current progression, not an invented clear')
    inputs={}
    for folder in (campaign,ROOT/'audit_v702_current_ending_records',ROOT/'audit_v702_current_battle_records'):
        result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        need(result['exit_code']==0,'Terminal native capture')
        for name,sha in result['input_hashes'].items():
            need(digest(Path(name))==sha,'Verified current input changed: '+name)
            inputs[name]=sha
        if folder!=campaign:need(result['passed'] and result['writes']==0 and not result['cheats_enabled'],'Read-only original photo result')
    for path,count in ((campaign/'regressions_v1.log',16),
                       (ROOT/'audit_v702_original_photo_oracle/decoder_tests.log',16)):
        text=path.read_text(encoding='utf-8-sig')
        need(re.search(rf'Ran {count} tests in [\d.]+s\s+OK\s*$',text) and 'FAILED' not in text,'Terminal regression log: '+str(path))
    # Pin the prior consolidated manifest by hash as a reference. Its 20,507
    # underlying files were checked in that checkpoint, not rechecked here.
    prior=ROOT/'audit_v704_finish_slots_checked_inputs/verification.json'
    prior_report=json.loads(prior.read_text())
    need(prior_report['passed'] and not prior_report['fullPortAcceptance'],'Prior bounded both-slot checkpoint')
    inputs[str(prior)]=digest(prior)
    folders=('audit_v697_reactive_kano_p1','audit_v697_reactive_sonya_p2',
             'audit_v698_reactive_kano_p1','audit_v698_reactive_sonya_p2',
             'audit_v699_zoning_kano_p1','audit_v699_zoning_sonya_p2',
             'audit_v700_zoning_long_kano_p1','audit_v700_zoning_leg_sonya_p2',
             'audit_v701_current_ending_records','audit_v701_current_battle_records',
             'audit_v702_original_photo_oracle','audit_v702_current_ending_records',
             'audit_v702_current_battle_records','audit_v703_native_tower_kano_p1',
             'audit_v705_native_tower_sonya_p2','audit_v706_native_tower_kano_p1')
    for folder in folders:
        need((ROOT/folder/'result.json').is_file() or folder=='audit_v702_original_photo_oracle','All attempts terminal and inventoried')
        for path in (ROOT/folder).rglob('*'):
            if path.is_file():inputs[str(path)]=digest(path)
    for pattern in ('mk2ks_natural_campaign_probe_v2[5-9].lua','mk2ks_natural_campaign_probe_v30.lua'):
        for path in ROOT.glob(pattern):inputs[str(path)]=digest(path)
    for path in (ROOT/'tools').iterdir():
        if path.is_file() and(path.name.startswith(('verify_natural_campaign_v680_',
          'test_natural_campaign_v680_','consolidate_native_campaign_photos_v680_',
          'run_native_ending_picture_probe_v680_')) or re.fullmatch(r'run_natural_campaign_probe_v(?:2[5-9]|30)\.ps1',path.name)):
            inputs[str(path)]=digest(path)
    for name in ('STATUS_2026-10-02_NATIVE_TOWER_AND_PHOTOS.md','tools/test_native_ending_photos.py',
                 'tools/native_picture_reference.cpp','tools/build_native_ending_reference.py',
                 'tools/decode_native_picture.py','tools/upgrade_ksui_previews.py',
                 'mame-mkp/src/mame/midway/mk2ks_native_picture.h'):
        path=ROOT/name;inputs[str(path)]=digest(path)
    out.mkdir()
    result=dict(passed=True,candidate='diagnostic_v680_native_pit_initial_cache',
                campaign=report,ending_record_pixels=107064,battle_record_pixels=43608,
                decoder_regressions=16,campaign_regressions=16,
                prior_checkpoint_manifest=digest(prior),prior_underlying_files_rechecked_here=False,
                gameplay_changed=False,release_promoted=False,fullPortAcceptance=False,
                unassisted_clear_proven=False,inputHashes=inputs,
                scope='Original photo records and genuine Kano progression to Kintaro; not boss clear, full endings/audio or full port')
    (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='inputHashes'},indent=2))
    print('Pinned inputs:',len(inputs))
