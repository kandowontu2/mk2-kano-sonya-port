"""Small scalar differences only; never accept missing draw records."""
import collections,json
import qualify_bounded_kung_lao_split_pixels as previous
import verify_native_source_sync as sync

def main():
    proof=json.loads((sync.ROOT/'audit_bounded_kung_lao_split_all_descriptors_checked/report.json').read_text())
    results={}
    for fighter,ident in [('sonya',18),('kano',17)]:
        sources={r['source'] for r in proof['descriptors'][str(ident)]}
        folder=sync.ROOT/f'audit_bounded_{fighter}_p1_kung_lao_split_all_pixels_runtime'
        expected=previous.fifo_at(folder,sources,ident)
        groups=previous.previous.summaries_at(folder)
        actual=collections.Counter((int(r['frame']),r['source'],int(r['width']),int(r['height']),int(r['x']),int(r['y']),int(r['command'],16)) for r in groups['IDLE_OPAQUE'])
        missing=expected-actual;extra=actual-expected
        results[fighter]=dict(expected=sum(expected.values()),actual=sum(actual.values()),missing=list(missing.items())[:8],extra=list(extra.items())[:8],missingDraws=sum(missing.values()),extraDraws=sum(extra.values()))
    print(json.dumps(results))

if __name__=='__main__':main()
