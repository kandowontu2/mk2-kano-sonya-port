"""Fresh actual human signature moves in both slots, exact v602 build.

Does not cover misses, blocks, all opponents, interrupts, audio or a campaign.
"""
import hashlib
import json
from pathlib import Path

import verify_native_candidate_v602 as build
import verify_human_special_matrix as positive

ROOT=build.ROOT


def verify():
    inputs={};cases=[]
    for move in positive.SPECS:
        for side in (1,2):
            folder=ROOT/f'audit_v608_positive_{move}_p{side}'
            build.matched(folder,inputs)
            metadata=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
            build.need((metadata['move'],metadata['side'],metadata['air'])==(move,side,False),'Actual declared ground command/slot')
            observer=(folder/'input_sources/mk2ks_human_special_matrix_v2.lua').read_text()
            build.need('write_u16' not in observer and 'write_u32' not in observer,'No guest-state writes')
            proof=positive.verify_log((folder/'run.log').read_text(encoding='utf-8-sig'),move,side,False)
            cases.append(proof)
    # Check the exact source delta, not an assurance that nothing else changed.
    live=ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'
    original=ROOT/'diagnostic_v596_native_pit_assets/base_v545_sources/midtunit_m.cpp'
    source=live.read_text();base=original.read_text()
    begin=source.index('\t// Pit II has a separate twelve-fighter')
    end=source.index('\tif (memcmp(donor + effect_header, "KFX1", 4))',begin)
    build.need(source[:begin]+source[end:]==base,'Only the dedicated Pit data/lookup initialization changed in gameplay driver')
    build.need(hashlib.sha256(original.read_bytes()).hexdigest().upper()==
               '217D08ED8CB6F4D03D1A6F24C3E43555204B9FA7B52B63C43FE8E5421157ED35','Exact preserved old gameplay source')
    for file in (live,original,Path(__file__),ROOT/'tools/verify_native_candidate_v602.py',ROOT/'tools/verify_human_special_matrix.py'):
        inputs[str(file)]=build.digest(file)
    return dict(passed=True,candidate=build.NAME,cases=cases,cases_count=len(cases),source_delta='only_native_Pit_initialization',
                scope='eight_actual_human_signature_moves_both_slots_not_full_outcomes_victims_interrupts_visual_audio_or_campaign',
                fullPortAcceptance=False,inputHashes=inputs)


if __name__=='__main__':print(json.dumps(verify(),indent=2))
