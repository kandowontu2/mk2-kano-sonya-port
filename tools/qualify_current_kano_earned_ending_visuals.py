"""Four actually reviewed native frames; no full audio/cinematic acceptance."""
import json,re,struct
import verify_native_source_sync as sync
sync.verify()
root=sync.ROOT;case=root/'audit_current_kano_earned_ending_visuals_runtime'
out=root/'audit_current_kano_earned_ending_visuals_checked';assert not out.exists()
def records(path):
    lines=path.read_text().splitlines();assert not any('LUA ERROR' in s for s in lines)
    return [s for s in lines if s.startswith('MK2_NAT_CAMPAIGN_')]
actual=records(case/'run.log');prior=records(root/'audit_current_kano_p2_shao_backjump_charge_counter_runtime/run.log')
assert [s for s in actual if not s.startswith('MK2_NAT_CAMPAIGN_ENDING_VISUAL_SAVED ')]==prior
captures=[dict(re.findall(r'(\w+)=([^\s]+)',s)) for s in actual if s.startswith('MK2_NAT_CAMPAIGN_ENDING_VISUAL_SAVED ')]
expected={'ending_page1.png':73800,'ending_page2.png':74700,'ending_return.png':75180,'after_ending.png':75400}
assert len(captures)==4 and {r['name']:int(r['frame']) for r in captures}==expected
files=list((case/'snap').rglob('*.png'));assert {p.name for p in files}==set(expected)
assert sum(p.stat().st_size for p in files)<=512*1024
for p in files:
    data=p.read_bytes();assert data[:8]==b'\x89PNG\r\n\x1a\n'
    assert struct.unpack('>II',data[16:24])==(400,254)
terminal=json.loads((case/'terminal.json').read_text(encoding='utf-8-sig'))
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert not (case/'stderr.log').read_text().strip()
report=dict(provenEarnedCampaignNativeRecordsExactlyPreserved=True,reviewedNativeFrames=4,
    totalPNGBytes=sum(p.stat().st_size for p in files),captures=captures,
    finiteVisualReview='Both Kano story pages show own photographs and readable MK2-style text in native gray panels, without selection portraits/cursors/lifebars. Return frames show native arena/demo imagery. Page2 has a narrow top black strip; original-stock pixel comparison was not rerun here.',
    frameHashes={p.name:sync.sha(p) for p in files},terminal=terminal,logSHA256=sync.sha(case/'run.log'),
    entireEndingPixelSequenceAccepted=False,endingAudioAccepted=False,postEndingFreshJoinAccepted=False,fullPortAccepted=False)
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
