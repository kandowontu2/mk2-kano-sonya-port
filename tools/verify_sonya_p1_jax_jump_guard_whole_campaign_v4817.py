"""Whole4803/4787 campaign grammar plus actual Jax physical/native callbacks.

Preserves every original later-context, guest, true-ID, health/winner, paid
continue, boss and ending/300-attract gate. No incomplete run is called clear.
"""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
text=(ROOT/'tools/verify_sonya_p1_kitana_guard_whole_campaign_v4803.py').read_text()
changes=[
 ('run_sonya_p1_kitana_guard_ram_v4794','run_sonya_p1_jax_jump_guard_ram_v4808'),
 ('qualify_sonya_p1_kitana_guard_source_v4795','qualify_sonya_p1_jax_jump_guard_source_v4809'),
 ('audit_v4797_{fighter}_p1_kitana_guard_ram','audit_v4811_{fighter}_p1_jax_jump_guard_ram'),
 ('audit_v4798_{fighter}_p1_kitana_guard_observed','audit_v4812_{fighter}_p1_jax_jump_guard_observed'),
 ('audit_v4798_{args.fighter}_p1_kitana_guard_observed','audit_v4812_{args.fighter}_p1_jax_jump_guard_observed'),
 ('audit_v4804_{args.fighter}_p1_kitana_guard_whole_campaign_checked','audit_v4818_{args.fighter}_p1_jax_jump_guard_whole_campaign_checked'),
 ('import verify_sonya_p1_kitana_guard_prefix_v4799 as kitana_inputs',
  'import verify_sonya_p1_kitana_guard_prefix_v4799 as kitana_inputs\\nimport verify_sonya_p1_jax_jump_guard_prefix_v4813 as jax_inputs')]
for before,after in changes:
    assert text.count(before)==1,before
    text=text.replace(before,after,1)
before="            result['actualWholeKitanaInputReplay']=actual\n"
after=before+"""            result['actualWholeJaxInputReplay']=jax_inputs.make_replay()(text)
            result['actualWholeJaxNativeCallbacks']=jax_inputs.callbacks(text,kano.expected_current()[0])
"""
assert text.count(before)==1
text=text.replace(before,after,1)
before="    prefix_path=kitana_inputs.OUT/'report.json';prefix=json.loads(prefix_path.read_text())\n"
after=before+"""    jax_prefix_path=jax_inputs.OUT/'report.json';jax_prefix=json.loads(jax_prefix_path.read_text())
    need(jax_prefix['passed'] and jax_prefix['prefixProofOnly'] and len(jax_prefix['actualRowAndCallbackFaultsRejected'])==13,
         'Actual separate complete Jax prefix and all13physical/native callback faults retained')
    with (folder/'run.log').open('rb') as stream:actual_jax_prefix=stream.read(jax_prefix['nativeLogPrefixBytes'])
    need(hashlib.sha256(actual_jax_prefix).hexdigest().upper()==jax_prefix['nativeLogPrefixSHA256'],
         'Executed original Jax prefix retained byte-for-byte through actual whole native terminal')
"""
assert text.count(before)==1
text=text.replace(before,after,1)
before="Path(kitana_inputs.__file__).resolve(),prefix_path"
after=before+",Path(jax_inputs.__file__).resolve(),jax_prefix_path"
assert text.count(before)==1
text=text.replace(before,after,1)
before='all11ActualKitanaPrefixFaultsRetained=True,'
assert text.count(before)==1
text=text.replace(before,before+'all13ActualJaxPrefixFaultsRetained=True,',1)
exec(compile(text,__file__+'::whole4803_plus_complete_Jax_controls_and_native_ground_jump_callbacks','exec'),globals())
