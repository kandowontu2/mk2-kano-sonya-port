"""Finite current/historical boss-tail and ending-context source conservation."""
import json,hashlib,copy
import verify_native_source_sync as sync
sync.verify();root=sync.ROOT
current=root/'mame-mkp/src/mame/midway/midtunit_m.cpp'
historical=root/'diagnostic_v5219_current_payload_rom_metadata/input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
a=current.read_text();b=historical.read_text()
anchors={
 'ending_context_fields':('// The added ladder fights make the one-player scene task', '/* Initial/alternate palettes'),
 'damage_and_native_boss_AI_callbacks':('// Canonical roster IDs also select damage scaling.', '/* The two post-Shao-Kahn story pages'),
 'six_native_ladders_boss_tails':('// six ROM schedules. Retain each original ordering and boss tail,', 'init_mk2ks_native_selector();'),
}
sections={}
for name,(start,end)in anchors.items():
    def extract(text):
        lo=text.index(start);return text[lo:text.index(end,lo)]
    x,y=extract(a),extract(b);assert x==y,name
    sections[name]=dict(normalizedSourceExact=True,characters=len(x),SHA256=hashlib.sha256(x.encode()).hexdigest(),source=x)
def gate(values):
    assert values==sections
    ladder=values['six_native_ladders_boss_tails']['source']
    assert 'tail < 5'in ladder and '(13 + tail)'in ladder and 'old_regular != 11'in ladder
    ending=values['ending_context_fields']['source'];assert all(x in ending for x in ['0x0270','0x0170','0x0190','0x01b0'])
gate(sections);faults=[]
for name in sections:
    bad=copy.deepcopy(sections);bad[name]['source']+=' changed'
    try:gate(bad)
    except AssertionError:faults.append(name)
    else:raise AssertionError('Changed dependency admitted')
matrix=root/'audit_v5698_current_campaign_four_case_matrix_checked/report.json'
accepted=json.loads(matrix.read_text());assert accepted['passed']and accepted['candidate']=='diagnostic_v5219_current_payload_rom_metadata'and accepted['actualNativeFourCaseBossOwnEndingAttractMatrixAccepted']
out=root/'audit_current_campaign_transition_dependencies_checked';assert not out.exists();out.mkdir()
report=dict(passed=True,historicalFourEarnedCampaignBossEndingAttractProofRetained=True,historicalMatrixSHA256=sync.sha(matrix),finiteConservedSections=sections,effectiveFaultsRejected=faults,currentSourceSHA256=sync.sha(current),historicalSourceSHA256=sync.sha(historical),wholeGuestEqual=False,wholeCurrentFourCampaignAcceptance=False,loadedAllBossTransitionOperandsChecked=False,scope='Exact finite source construction for six schedule originalboss tails, damage scaling/stockbossAI callbacks and paired endingcontext field relocation is conserved. These do not establish all laterpatched guest dependencies/runtime trajectories, wholecurrentearnedfourcampaign or unsampledloadedboss transition operands. CurrentK2earnedfullending separatelyproven; K1/S1Kintaro/S2Kitana coveragefrontiers are bot evidence limits, not observed brokenboss transition/roster/ending.',actualChangedFiniteDependency='Within these three relevant sections NONE; laterselector/CPU special/morph/finisher/audio additions elsewhere differ. Ownending asset decoder/table41 vs40 change and currentloadedSonyaending dependencies are separatelyqualified, not reset here.',nextConcreteScope='Avoid replay solelyforbossdifficulty. Close specific remainingloadedtransition/secretteardown dependency and finalrelease combined heardaudio/visual plusmatchingupdatedZIP; currentopposite-slotwholeearnedendings remain unproven aswholebuild despite retainedfinite historical evidence.',fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2));print(out)
