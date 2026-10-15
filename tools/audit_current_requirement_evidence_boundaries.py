"""Revalidate saved requirement inventory without promoting historical claims."""
import json
from pathlib import Path
import verify_native_source_sync as sync

def main():
    source_sync=sync.verify()
    parent=sync.ROOT/'audit_v6133_current_kung_lao_native_scene_progress/progress.json'
    historical=json.loads(parent.read_text())
    out=sync.ROOT/'audit_current_requirement_evidence_boundaries'
    assert not out.exists()
    inventory=[]
    for item in historical['requirementAudit']:
        evidence=[]
        for reference in item.get('evidence',[]):
            path=Path(reference['path'])
            actual=sync.sha(path) if path.is_file() else None
            evidence.append(dict(path=str(path),expectedSHA256=reference['sha256'],
                actualSHA256=actual,bytesStillMatch=actual==reference['sha256']))
        inventory.append(dict(requirement=item['requirement'],historicalStatus=item['status'],
            historicalEvidence=evidence,currentFullScopeCompletionProven=False,
            boundary='Hash equality preserves historical bytes, not current runtime coverage or lost recording availability.'))
    latest=[]
    for name in ('kung_lao_split_dcs_delivery','kung_lao_split_pcm_terminal_field',
                 'kitana_kiss_dcs_delivery','kitana_kiss_pcm_digest'):
        path=sync.ROOT/f'audit_bounded_{name}_checked/report.json'
        report=json.loads(path.read_text());assert report['passed']
        cases={}
        for key,case in report['results'].items():
            pins={}
            if 'logSha256' in case:
                fighter,side=key[:-2],key[-1]
                log=sync.ROOT/f'audit_bounded_{fighter}_p{side}_{name}_runtime/run.log'
                pins[str(log)]=sync.sha(log)==case['logSha256']
            else:
                fighter,side=key[:-2],key[-1]
                prefix='kung_lao_split' if name.startswith('kung_lao') else 'kitana_kiss'
                for label,expected in case['logHashes'].items():
                    log=sync.ROOT/f'audit_bounded_{fighter}_p{side}_{prefix}_pcm_{label}_runtime/run.log'
                    pins[str(log)]=sync.sha(log)==expected
            assert pins and all(pins.values())
            cases[key]=pins
        latest.append(dict(path=str(path),sha256=sync.sha(path),actualRuntimeLogPinsVerified=cases,
            scope='Finite native command delivery or paired mixed-output consistency; not heard-quality/full integration.'))
    report=dict(passed=True,sourceSync=source_sync,parentSHA256=sync.sha(parent),
        originalRequirementAudit=inventory,originalRemainingGroups=historical['remaining'],
        recentBoundedEvidence=latest,fullGoalComplete=False,goalStatus='active',
        nextPriority='Bounded real move interruption and imported channel ownership/retirement; lost dense recording is not evidence.',
        checkerSHA256=sync.sha(Path(__file__)))
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,requirements=len(inventory),historicalPinMismatches=sum(not e['bytesStillMatch'] for i in inventory for e in i['historicalEvidence']),recentProofs=len(latest),fullGoalComplete=False)))

if __name__=='__main__':main()
