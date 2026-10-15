"""Freeze the real throw fix, failed checks and current playable handoff."""
import json,hashlib,sys
from pathlib import Path
import verify_native_ground_throw_source_v1598 as source
import verify_native_ground_throw_humans_v1606 as human
import verify_native_ground_throw_campaign_v1612 as campaign
ROOT=source.ROOT
OUT=ROOT/'audit_v1618_native_ground_throw_checkpoint'
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb')as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest().upper()
def freeze():
    pins={}
    def pin(p,wanted=None):
        p=Path(p);key=str(p.resolve())
        if key not in pins:pins[key]=sha(p)
        assert wanted is None or wanted==pins[key],'Changed checkpoint input '+key
    accepted={}
    for name in('audit_v1598_native_ground_throw_source_checked','audit_v1606_native_ground_throw_humans_checked',
                'audit_v1612_ground_throw_campaign_checked','audit_v1614_ground_throw_arena_checked',
                'audit_v1615_native_cpu_ground_throw_checked','audit_v1617_ground_throw_launcher_checked'):
        path=ROOT/name/'report.json';report=json.loads(path.read_text(encoding='utf-8-sig'))
        assert report['passed'];pin(path)
        if 'candidate'in report:assert report['candidate']==source.NAME
        for p,h in report.get('inputHashes',{}).items():pin(p,h)
        accepted[name]=dict(reportSHA=pins[str(path.resolve())],passed=True,
                           scope=report.get('scope'),fullPortAcceptance=False)
    prior=ROOT/'audit_v1584_native_arena_context_checkpoint/checkpoint.json'
    pin(prior,'925E0D34BCCD6957B1A7F1A25F0A0889F0D8E399796E5E78AFDD5A7D2A609EC6')
    for name in('audit_v1594_native_ground_throw_collision','audit_v1600_sonya_ground_throw_p1',
                 'audit_v1600_kano_ground_throw_p2','audit_v1602_sonya_ground_throw_p1',
                 'audit_v1602_sonya_ground_throw_p2','audit_v1602_kano_ground_throw_p1',
                 'audit_v1602_kano_ground_throw_p2','audit_v1604_kano_p2_throw_cpu_campaign',
                 'audit_v1605_native_ground_throw_humans_checked','audit_v1610_ground_throw_campaign_checked',
                 'audit_v1611_ground_throw_arena_checked','audit_v1613_ground_throw_arena_checked'):
        for p in(ROOT/name).rglob('*'):
            if p.is_file():pin(p)
    for name in('inspect_native_ground_throw_collision_v1594.py','build_native_ground_throw_v1596.ps1',
                 'verify_native_ground_throw_source_v1598.py','run_human_ground_throw_v1599.ps1',
                 'run_human_ground_throw_v1601.ps1','verify_native_ground_throw_humans_v1603.py',
                 'verify_native_ground_throw_humans_v1605.py','verify_native_ground_throw_humans_v1606.py',
                 'verify_native_ground_throw_campaign_v1607.py','verify_native_ground_throw_arena_v1608.py',
                 'verify_native_ground_throw_campaign_v1610.py','verify_native_ground_throw_arena_v1611.py',
                 'verify_native_ground_throw_campaign_v1612.py','verify_native_ground_throw_arena_v1613.py',
                 'verify_native_ground_throw_arena_v1614.py','verify_native_cpu_ground_throw_v1615.py',
                 'check_ground_throw_playtest_v1616.ps1','test_ground_throw_launcher_v1617.ps1'):
        pin(ROOT/'tools'/name)
    for module in tuple(sys.modules.values()):
        value=getattr(module,'__file__',None)
        if value:
            p=Path(value).resolve()
            if p.is_relative_to(ROOT/'tools')and p.suffix=='.py':pin(p)
    for name in('PLAY_CURRENT_V1517_TEST_BUILD.cmd','PLAY_CURRENT_V1597_TEST_BUILD.cmd',
                 'mk2ks_human_ground_throw_v1599.lua','mk2ks_human_ground_throw_v1601.lua'):
        pin(ROOT/name)
    restored={'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891',
              'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
              'mame-mkp/src/mame/midway/midtunit.cpp':'07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
              'mame-mkp/src/mame/midway/midtunit.h':'256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644'}
    for p,h in restored.items():pin(ROOT/p,h)
    pin(__file__)
    return dict(goalStatus='active',objective='Once again, the goal is clear: THey need to appear as a natural part of the game in all aspects.',
      previousGoalTurnClassification='progress: final Kano P1 nine-arena checker completed successfully',
      thisGoalTurnClassification='progress: diagnosed, source-built and runtime-tested a real ordinary throw/fatality index collision',
      currentCandidate=source.NAME,currentCMD='PLAY_CURRENT_V1597_TEST_BUILD.cmd',
      executableSHA='9D2E9849CA3A98AA06018DB2EF3EE65397A5C9EC95C466CFD999C9091237B695',
      payloadSHA='5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D',
      initializedGuestSHA='1B79ACA01355CC0AEAC1B59FB39031F947EC05D2F08A9B68C578D8580289E01F',
      knownDefect='Native ordinary throw selected main[42 + attacker ID]; Sonya ID18 selected headless main60 while opponent was alive',
      implementation='Only native ordinary throw animation index dispatch changes for true attacker IDs17/18. Actual victim ID/root owns main43; fatality rows, body assets, timing, damage, palettes and audio unchanged.',
      changedGuestBytes=54,currentHumanThrowsBothSlots=True,currentCPUThrowStateAndROMPoses=True,
      currentFullRasterSamples=60,currentArenasSampled=[0,1,2,3],currentNativeShadowRowCopies=38753,
      currentExactCoordinatePublications=2565,campaignReachedStages=[0,1,2,3],nativeOwnRoundWins=8,
      currentUnassistedCampaignClear=False,allNineBothCharactersBothSlots=False,
      current52SpecialCaseRegressionRerun=False,allMovePhaseFloorAccepted=False,
      launcherOrdinaryBootPassed=True,userControlsCopiedWithoutOverwritingPriorControls=True,
      priorCanonicalSourceAndExecutableRestored=True,liveWorkProcesses=[],
      failedCapturesAndCheckersRetained=True,mislabeledV1613ReportRetainedNotAccepted=True,
      oldCaptureEvidenceChanged=False,newReleaseZIPCreated=False,cleanupPerformedThisTurn=False,
      remaining=['Full current special-move and CPU repertoire/opponent regression',
        'Actual P2 square-wave incoming-hit audio interruption',
        'All-nine-arena both-character both-slot and full move-phase floor/shadow coverage',
        'All finishers, victims, morphs, boss/campaign clear, endings, secrets and cinematics',
        'Obsolete build cleanup and final release ZIP'],
      acceptedReports=accepted,inputHashes=pins,fullPortAcceptance=False)
if __name__=='__main__':
    assert not OUT.exists(),'Never overwrite a checkpoint'
    report=freeze();OUT.mkdir();(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(saved=str(OUT/'checkpoint.json'),pins=len(report['inputHashes']),candidate=report['currentCandidate'],goalStatus=report['goalStatus'],fullPortAcceptance=False),indent=2))
