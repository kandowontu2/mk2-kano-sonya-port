"""Bind new native CPU/campaign evidence without narrowing whole-port success."""
import hashlib,json,re
from pathlib import Path
import verify_active_launch_timer_v1520 as source
ROOT=source.ROOT;OUT=ROOT/'audit_v1558_native_cpu_campaign_checkpoint'

def verify():
    pins={}
    def pin(path,wanted=None):
        path=Path(path);key=str(path.resolve())
        if key not in pins:pins[key]=source.sha(path)
        assert wanted is None or pins[key]==wanted,'Changed current evidence '+key
    previous=ROOT/'audit_v1541_active_launch_checkpoint/checkpoint.json'
    pin(previous,'4EF39615409AEA259C276A542F9566BC2EB370193193A3BC89273DA187436F85')
    old=json.loads(previous.read_text());assert not old['fullPortAccepted']
    names=('audit_v1542_native_rng_timing','audit_v1545_native_rng_checked',
           'audit_v1547_current_sonya_campaign_checked','audit_v1547_current_kano_campaign_checked',
           'audit_v1551_cross_stomp_campaign_checked','audit_v1551_projectile_campaign_checked',
           'audit_v1556_interleaved_kano_display_checked','audit_v1557_interleaved_kano_counterexamples')
    reports={};data={}
    for name in names:
        path=ROOT/name/'report.json';r=json.loads(path.read_text(encoding='utf-8-sig'));assert r['passed'];pin(path)
        for p,h in r.get('inputHashes',{}).items():pin(p,h)
        reports[name]=dict(passed=True,sha256=source.sha(path));data[name]=r
    native=data['audit_v1556_interleaved_kano_display_checked']
    assert native['sampledNativeScanouts']==119 and native['completeBothPhysicalStateLedgers']
    assert native['chokeDamage']==32 and native['earlyBladeDamage']==26 and not native['uninterruptedFixtureAccepted']
    counters=data['audit_v1557_interleaved_kano_counterexamples'];assert len(counters['rejected'])==6 and counters['actualCaptureUnmodified']
    rng=data['audit_v1545_native_rng_checked'];assert rng['actualNativeRNGTimingDifferenceObserved']
    for name in names:
        r=data[name]
        if 'campaign_checked' in name:assert r['bounded_campaign_evidence_proven'] and not r['unassisted_clear_proven']
    failed=ROOT/'audit_v1555_interleaved_kano_state_checked/report.json'
    assert not json.loads(failed.read_text())['passed'];pin(failed)
    for name in('audit_v1552_current_kano_cpu_cage','audit_v1552_current_kano_cpu_cage_confirm96',
                'audit_v1554_cpu_cage_boot602','audit_v1554_cpu_cage_boot603','audit_v1554_cpu_cage_boot604'):
        launch=json.loads((ROOT/name/'result.json').read_text(encoding='utf-8-sig'))
        assert launch['exit_code']==0 and launch['candidate']==source.NAME and launch['assistance']=='none' and not launch['cheats_enabled']
    for folder in ROOT.iterdir():
        m=re.match(r'^audit_v(\d+)_',folder.name)
        if folder.is_dir() and m and 1542<=int(m[1])<=1557:
            for p in folder.rglob('*'):
                if p.is_file():pin(p)
    for folder in(ROOT,ROOT/'tools'):
        for p in folder.iterdir():
            m=re.search(r'_v(\d+)\.(lua|ps1|py)$',p.name)
            if p.is_file() and m and 1542<=int(m[1])<=1558:pin(p)
    canonical={
        'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
        'mame-mkp/src/mame/midway/midtunit.cpp':'07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
        'mame-mkp/src/mame/midway/midtunit.h':'256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644',
        'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891'}
    for p,h in canonical.items():pin(ROOT/p,h)
    pin(ROOT/source.NAME/'mkport_candidate.exe',source.EXE_SHA)
    pin(ROOT/'PLAY_CURRENT_V1517_TEST_BUILD.cmd');pin(ROOT/'STATUS_2026-10-03_V1517_NATIVE_CPU_CAMPAIGN.md');pin(__file__)
    return dict(candidate=source.NAME,currentTestLauncher='PLAY_CURRENT_V1517_TEST_BUILD.cmd',
                previousCheckpoint=str(previous),previousCheckpointSHA256=source.sha(previous),
                previousPinsBoundByManifest=len(old['inputHashes']),previousPinsIndividuallyRehashedThisCheckpoint=False,
                freshReports=reports,currentKanoCPUInterleavedContactAccepted=True,newExactNativeScanouts=119,
                realChokeDamage=32,realEarlyBladeDamage=26,bothPhysicalFlagStateLedgersExact=True,
                counterexamplesRejected=6,oldUninterruptedFixtureNotRelabelled=True,
                nativeRNGFirstHardwareTimingDivergenceProven=True,allLaterAIBranchesExplained=False,
                additionalKanoBossCampaignsChecked=2,fullCampaignAccepted=False,fullAIRepertoireAccepted=False,
                allMoveAudioAndChoreographyAccepted=False,allArenaGroundShadowAccepted=False,
                canonicalSourcesAndInstalledExeRestored=True,playableGameChangedThisWork=False,
                furtherOldBuildsRemovedThisWork=False,allOldBuildFoldersDeleted=False,releaseZIPUpdated=False,
                fullPortAccepted=False,inputHashes=pins)

if __name__=='__main__':
    assert not OUT.exists(),'Never overwrite evidence'
    report=verify();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(freshPins=len(report['inputHashes']),newExactNativeScanouts=119,fullPortAccepted=False)),flush=True)
