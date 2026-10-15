"""Full4787 natural campaign grammar plus actual separate Kitana input replay.

Every original source/guest/selection/schedule/morph/special/health/winner/
continue/boss/ending/300-attract boundary remains. Supplemental per-field
Kitana replay cannot replace any missing later context or ending evidence.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
text=(ROOT/'tools/verify_current_p1_whole_campaign_v4787.py').read_text()
changes=[
 ('import run_current_p1_campaign_ram_v4782 as capture','import run_sonya_p1_kitana_guard_ram_v4794 as capture'),
 ('import qualify_current_p1_campaign_source_v4783 as boundary','import qualify_sonya_p1_kitana_guard_source_v4795 as boundary\nimport verify_sonya_p1_kitana_guard_prefix_v4799 as kitana_inputs'),
 ('audit_v4785_{fighter}_current_p1_campaign_ram','audit_v4797_{fighter}_p1_kitana_guard_ram'),
 ('audit_v4786_{fighter}_current_p1_campaign_observed','audit_v4798_{fighter}_p1_kitana_guard_observed'),
 ('audit_v4786_{args.fighter}_current_p1_campaign_observed','audit_v4798_{args.fighter}_p1_kitana_guard_observed'),
 ('audit_v4788_{args.fighter}_current_p1_whole_campaign_checked','audit_v4804_{args.fighter}_p1_kitana_guard_whole_campaign_checked'),
 ("choices=('kano','sonya')","choices=('sonya',)")]
for before,after in changes:
    assert text.count(before)==1,before
    text=text.replace(before,after,1)
before="    return native\n\ndef run(fighter):"
after="""    original_native=native
    def native(folder,text_override=None):
        result=original_native(folder,text_override=text_override)
        text=(folder/'run.log').read_text() if text_override is None else text_override
        try:
            actual=kitana_inputs.make_replay()(text)
            need(actual['actualNativeLegActivations']>0,'Real owned Kitana-context leg task, not intended commands')
            result['actualWholeKitanaInputReplay']=actual
        except ValueError as error:
            result['passed']=False;result['errors'].append(str(error))
        return result
    return native

def run(fighter):"""
assert text.count(before)==1
text=text.replace(before,after,1)
before="    native=make_native(fighter);positive=native(folder)\n"
after=before+"""    prefix_path=kitana_inputs.OUT/'report.json';prefix=json.loads(prefix_path.read_text())
    need(prefix['passed'] and prefix['prefixProofOnly'] and len(prefix['actualRowFaultsRejected'])==11,
         'Actual original separate Kitana prefix and all11state/input faults retained')
    with (folder/'run.log').open('rb') as stream:actual_prefix=stream.read(prefix['nativeLogPrefixBytes'])
    need(hashlib.sha256(actual_prefix).hexdigest().upper()==prefix['nativeLogPrefixSHA256'],
         'Executed Kitana prefix retained byte-for-byte in actual whole terminal native capture')
"""
assert text.count(before)==1
text=text.replace(before,after,1)
before="             boundary.OUT/'report.json']:pins[str(p.resolve())]=sha(p)"
after="             boundary.OUT/'report.json',Path(kitana_inputs.__file__).resolve(),prefix_path]:pins[str(p.resolve())]=sha(p)"
assert text.count(before)==1
text=text.replace(before,after,1)
before="      originalWholeCampaignGrammarRetained=True,actualNaturalP1TowerOwnEndingAttractAccepted=positive['unassisted_clear_proven'],"
after="      originalWholeCampaignGrammarRetained=True,all11ActualKitanaPrefixFaultsRetained=True,actualNaturalP1TowerOwnEndingAttractAccepted=positive['unassisted_clear_proven'],"
assert text.count(before)==1
text=text.replace(before,after,1)
exec(compile(text,__file__+'::full4787_plus_complete_actual_Kitana_replay','exec'),globals())
