"""Retain old full clears, explicitly bound unchanged components and transfer limits."""
import hashlib,json
import verify_native_source_sync as sync
sync.verify()
out=sync.ROOT/'audit_current_historical_campaign_transfer'
assert not out.exists()
matrix_path=sync.ROOT/'audit_v5698_current_campaign_four_case_matrix_checked/report.json'
matrix=json.loads(matrix_path.read_text())
assert matrix['passed'] and matrix['actualNativeFourCaseBossOwnEndingAttractMatrixAccepted']
old_path=sync.ROOT/'diagnostic_v5219_current_payload_rom_metadata/input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
current_path=sync.ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'
assert sync.sha(old_path)=='37E02771B1F20CF17D0D619F83033F5FE37FE5B62DCD9519F60872763BE0E57A'
old=old_path.read_text();current=current_path.read_text()
def segment(source,start,end):
    return source[source.index(start):source.index(end,source.index(start))]
story_start='char const *const ending_story[2][5] = {'
old_story=segment(old,story_start,'\n\t};')
new_story=segment(current,story_start,'\n\t};')
assert old_story==new_story
pairs=['write16(rom_offset(0xff844700), 0x0270);','write16(rom_offset(0xff8448a0), 0x0270);',
       'write16(rom_offset(0xff844720), 0x0170);','write16(rom_offset(0xff844970), 0x0170);',
       'write16(rom_offset(0xff844740), 0x0190);','write16(rom_offset(0xff844ab0), 0x0190);',
       'write16(rom_offset(0xff844760), 0x01b0);','write16(rom_offset(0xff844b40), 0x01b0);']
assert all(line in old and line in current for line in pairs)
assert 'std::copy_n(rom + rom_offset(0xff8f48f0), 40 * 4, rom + ending_picture_table);' in old
assert 'std::copy_n(rom + rom_offset(0xff8f48f0), 41 * 4, rom + ending_picture_table);' in current
assert 'constexpr unsigned ai_variety_router = 0xf7800;' in current and 'constexpr unsigned ai_variety_router = 0xf7800;' not in old
cases=[]
for case in matrix['cases']:
    assert case['actualOwnEndingCompletions']==1 and case['actualBossRoundWins']>=4 and case['actualNativeExit']==0
    path=sync.ROOT/('audit_v5235_'+case['fighter']+'_corrected_p1_campaign_checked/report.json' if case['physicalSlot']==1 else
                   ('audit_v5624_current_kano_p2_campaign_checked/report.json' if case['fighter']=='kano' else 'audit_v5691_verified_subzero_sonya_p2_campaign_checked/report.json'))
    expected=next(value for name,value in matrix['inputHashes'].items() if name.replace('\\','/').lower()==str(path).replace('\\','/').lower())
    assert sync.sha(path)==expected
    cases.append(dict(fighter=case['fighter'],slot=case['physicalSlot'],ownRoundWins=case['actualOwnRoundWins'],
        paidLosses=case['actualContinueLosses'],proofSHA256=expected,fullEndingPixelsAccepted=case['fullEndingPixelsAccepted']))
report=dict(historicalFourCampaignReceiptsPreserved=True,cases=cases,
    unchangedOwnStoryStrings=True,unchangedPairedEndingContinuationPatches=pairs,
    currentPreservesAdditionalStockPictureRow=True,currentAddsCpuVarietyRouter=True,
    oldExecutableSHA256=matrix['executableSHA256'],oldGuestSHA256=matrix['guestSHA256'],
    currentExecutableSHA256=sync.sha(sync.BUILD/'mkport_candidate.exe'),
    oldSourceSHA256=sync.sha(old_path),currentSourceSHA256=sync.sha(current_path),
    matrixSHA256=sync.sha(matrix_path),
    currentFullCampaignAccepted=False,currentEndingRenderingAccepted=False,fullPortAccepted=False,
    scope='Historical receipts and selected exact source components only. Expanded CPU gameplay and other source changes prevent automatic whole-build campaign transfer. Old art/audio gaps remain gaps; no old recorder/controller executed.')
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(dict(historicalCases=len(cases),ownStoriesUnchanged=True,currentCpuRoutingChanged=True,currentCampaignAccepted=False)))
