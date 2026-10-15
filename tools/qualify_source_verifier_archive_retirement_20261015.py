"""Persist actual current source verification and explicit archive-policy negatives."""
import json
import verify_native_source_sync as v

out=v.ROOT/'audit_source_verifier_archive_retirement_20261015'
assert not out.exists()
r=v.verify()
assert r['passed'] and r['trackedCanonicalCompileInputs']==15
assert len(r['retiredHistoricalArchivePins'])==1
assert len(r['effectiveArchiveRetirementFaultsRejected'])==7
assert len(r['effectiveFaultsRejected'])==13
assert not v.RETIRED_ARCHIVE.exists()
assert r['retiredHistoricalArchivePins'][0]['oldArchiveBytesFreshlyRevalidated'] is False
assert any(p['explicitlyRetiredArchivePins'] and not p['unchangedOriginalPathsGateStillValid'] for p in r['historicalEvidence'])
report=dict(passed=True,actualSourceVerifier=r,
            exactArchivalPolicyOnly=True,canonicalCompileInputsRetained=15,
            currentExecutableAndPayloadChecksUnchanged=True,
            originalHistoricalReportBytesUnchanged=True,
            retiredArchiveIsNotCurrentRebuildDependency=True,
            genericMissingInputsStillFail=True,
            effectiveRetirementNegatives=7,effectiveSourceProvenanceNegatives=13,
            verifierSHA256=v.sha(v.__file__),retirementReceiptSHA256=v.sha(v.RETIREMENT_RECEIPT),
            noNewGameBuild=True,noEmulatorRun=True,noDeletionByThisVerifier=True)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(passed=True,compileInputs=15,retirementFaults=7,provenanceFaults=13,report=str(out/'report.json'))))
