"""Finite inspected stock corner sheets; placement variation, not universal parity."""
import json
from pathlib import Path
import verify_native_source_sync as sync

def main():
    out=sync.ROOT/'audit_bounded_jax_arm_stock_corner_review_bound';assert not out.exists()
    path=sync.ROOT/'audit_v6157_current_jax_arms_stock_profiles_checked/report.json'
    prior=json.loads(path.read_text());assert prior['passed'] and prior['actualStockContexts']==6 and prior['actualAddedCharacterContexts']==0
    results={}
    for fighter,version in [('kitana',6147),('jax',6161)]:
        for side in (1,2):
            assert any(c['fighter']==fighter and c['side']==side for c in prior['cases'])
            folder=sync.ROOT/f'audit_v{version}_current_jax_arms_stock_{fighter}_p{side}_corner_ram'
            png=folder/'review'/f'actual-stock-{fighter}-p{side}-native-corner-review.png'
            assert sync.sha(png)==prior['inputHashes'][str(png)]
            results[f'{fighter}P{side}']=dict(reviewPath=str(png),reviewSha256=sync.sha(png),stockReferenceOnly=True,
                visualObservation='Stock Kitana remains mostly onscreen in sampled victim poses.' if fighter=='kitana' else 'Stock Jax victim poses extend partly offscreen in sampled phases, in both slots.')
    report=dict(passed=True,results=results,historicalProofSha256=sync.sha(path),checkerSha256=sync.sha(Path(__file__)),sourceSync=sync.verify(),
        finiteStockPlacementVariationObserved=True,currentAddedPositionEquivalenceAccepted=False,universalCornerPlacementAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,reviewedStockContexts=4,universalCornerPlacementAccepted=False)))

if __name__=='__main__':main()
