"""Collect portable, finite release evidence; never approve a release implicitly."""
import hashlib
import json
from pathlib import Path
from inspect_normal_runtime import PORT, BASE


def digest(path):
    checksum = hashlib.sha256()
    with Path(path).open('rb') as source:
        for block in iter(lambda: source.read(65536), b''):
            checksum.update(block)
    return checksum.hexdigest().upper()


def require_report(data, required=(), count=None):
    for key in required:
        if data.get(key) is not True:
            raise ValueError('Required evidence is not true: ' + key)
    if count is not None and len(data.get('cases', [])) != count:
        raise ValueError('Unexpected finite case count')


def main():
    reports = {}

    def add(label, path, required=(), count=None):
        path = Path(path)
        data = json.loads(path.read_text())
        require_report(data, required, count)
        reports[label] = dict(file=path.name, SHA256=digest(path), evidence=data)
        return data

    add('normalContact', PORT/'NORMAL_CONTACT_ACCEPTANCE_2219.json',
        ['all136FiniteContactCellsPassed'])
    add('specials', PORT/'SPECIAL_MATRIX_QUALIFICATION.json',
        ['allSixteenFiniteCasesPassed', 'currentAll26ROMsVerified'], 16)
    add('lethals', PORT/'LETHAL_ROSTER_ACCEPTANCE_2219.json',
        ['allExpectedCasesQualified'], 112)
    add('friendshipBabality', PORT/'NONLETHAL_MATRIX_QUALIFICATION.json',
        ['allEightPositiveCasesPassed', 'currentAll26ROMsVerified'], 8)
    add('negativeEligibility', PORT/'NEGATIVE_NONLETHAL_MATRIX_QUALIFICATION.json',
        ['allEightPunchIneligibleCasesPassed', 'currentAll26ROMsVerified'], 8)
    add('stages', PORT/'STAGE_POSITIVE_MATRIX_QUALIFICATION.json',
        ['allEightPositiveCasesPassed', 'allFourMissingChordCasesPassed',
         'allFourOwnPairPitCasesPassed', 'currentAll26ROMsVerified'])
    add('morphLethals', PORT/'MORPH_FINISHER_REJOIN_MATRIX_QUALIFICATION.json',
        ['allEightCasesPassed', 'allActual26ROMsVerified'], 8)
    add('morphMoves', PORT/'MORPH_MOVE_RELEASE_QUALIFICATION.json', count=14)
    add('morphArt', PORT/'MORPH_ART_TRACE_QUALIFICATION.json',
        ['forwardAndReversePoseOrderVerified', 'nativeFourFieldCadenceVerified',
         'entryGroundingMeasuredCorrect', 'reverseGroundingMeasuredCorrect'], 2)
    add('selectionP1', PORT/'SELECTION_UI_2219_QUALIFICATION.json', count=2)
    add('selectionP2', PORT/'SELECTION_P2_2219_QUALIFICATION.json', count=2)
    add('floorShadows', PORT/'SHADOW_BANK_QUALIFICATION.json',
        ['nonBankControlBitsPreserved', 'sourceRestoresSystemControlAfterEachByte',
         'capturedFloorShadowsVisuallyReviewed', 'currentFourCaptureShadowPixelRegressionVerified'])
    add('movelist', PORT/'MOVELIST_COMMAND_QUALIFICATION.json',
        ['laserButtonHistoryMatched', 'friendshipButtonHistoryMatched',
         'nativeNoPunchSourceGatesVerified', 'trueIdentityMorphSourceDispatchVerified'])
    add('rebuild', PORT/'REBUILT_ROM_SET_QUALIFICATION.json',
        ['programCleanRebuildByteIdentical', 'soundCleanRebuildByteIdentical',
         'addedGraphicsChainRebuiltByteIdentical', 'allRebuiltROMBytesMatchRuntimeInput'])
    for actor, run in [('kano', 'stock_wolf_2219_kano_continuous_short_route'),
                       ('sonya', 'stock_wolf_2219_sonya_campaign_stream')]:
        add(actor+'Campaign', BASE/run/'CAMPAIGN_CLEAR_QUALIFICATION.json',
            ['nativeCampaignClearVerified'])
        add(actor+'Video', PORT/('generated_'+actor+'_campaign_2219')/'CAMPAIGN_VIDEO.json',
            ['earnedFullCampaignClearVerified'])
    out = PORT/'development_patches'
    # Module count is an integer, not a boolean evidence gate.
    package = add('sourcePackage', out/'PACKAGE_QUALIFICATION.json',
        ['packageFileHashesVerified', 'noCompleteROMsOrEmulatorIncluded',
         'sourceDiffAppliedAndMatchedCurrent'])
    assert package['ownASMModulesMatched'] == 59 and package['changedOriginalFiles'] == 40
    source_zip = out/'MK2KS_NATIVE_DEVELOPMENT_IPS.zip'
    assert digest(source_zip) == package['packageSHA256']
    media = []
    for relative, expected in [
        ('generated_kano_campaign_2219/MKII_KANO_CAMPAIGN_NATIVE.mp4',
         'BD21C6BB5A1F09B2B6F6BAABF1DEE1EF65105CB402225A70330CE33073658394'),
        ('generated_sonya_campaign_2219/MKII_SONYA_CAMPAIGN_NATIVE.mp4',
         '23C5309D7892059644062814441891B8EF84B67F436EB3F197356F70C0ED6FEE'),
        ('generated_showcases_2219_streamcopy/MKII_KANO_MOVES.mp4',
         '45954A09C2BE89C60C5FCFF529EE4287D8E51043F3EDC747963BA53E504A315E'),
        ('generated_showcases_2219_streamcopy/MKII_SONYA_MOVES.mp4',
         'DEB15FED56822783784067ECAF39019C52D172B49B9B9D2F646734CCB769C1DB')]:
        path = PORT/relative
        assert digest(path) == expected, relative
        media.append(dict(file=path.name, bytes=path.stat().st_size, SHA256=expected))
    report = dict(format='MK2KS-NATIVE-RELEASE-EVIDENCE-1',
        scope='Finite native stock-MAME verification record; packaging approval is separate',
        customDriver=False, gameMemoryWritesForCampaignClear=False,
        releaseApproved=False, finalPlayerPackageVerified=False,
        sourcePackageSHA256=digest(source_zip), reports=reports, media=media,
        limitations=['Not a T-unit PCB drop-in: targets stock mk3 Wolf hardware definition',
                     'Not an exhaustive proof of every input, victim, arena or interruption',
                     'Sparse visual review is not subjective every-frame audiovisual approval',
                     'Interactive Windows renderer not opened during background-only testing'])
    target = PORT/'NATIVE_RELEASE_EVIDENCE_CANDIDATE.json'
    target.write_text(json.dumps(report, indent=2)+'\n')
    print('Collected', len(reports), 'reports and', len(media), 'verified media assets;',
          target.stat().st_size, 'bytes; release approval remains separate')


if __name__ == '__main__':
    main()
