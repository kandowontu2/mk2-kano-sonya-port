"""Fresh journal correction; retain executed4915 and malformed prior prompt log."""
from pathlib import Path
prior=Path(__file__).with_name('save_earned_subzero_matrix_progress_v4915.py')
text=prior.read_text()
before="prompts=json.loads((ROOT/'art_native_subzero_v4888/generation-prompts.json').read_text())"
after="""original_prompts=(ROOT/'art_native_subzero_v4888/generation-prompts.json').read_text()
 corrected_prompts=ROOT/'art_native_subzero_v4888/generation-prompts_v4917.json'
 need(original_prompts.startswith('+{') and corrected_prompts.read_text()==original_prompts[1:], 'Exact single stray-leading-plus removal in fresh prompt record')
 prompts=json.loads(corrected_prompts.read_text());pin(corrected_prompts);pin(prior)
""".rstrip()
assert text.count(before)==1
text=text.replace(before,after,1).replace('audit_v4916_earned_subzero_matrix_progress','audit_v4919_earned_subzero_matrix_progress',1)
before="builtInImageGeneration=True,selectedMasterOnly=True,nativeEncoded=False,nativeAccepted=False)"
after="builtInImageGeneration=True,selectedMasterOnly=True,nativeEncoded=False,nativeAccepted=False, correctedPrompts=str(corrected_prompts), priorPromptLogHasStrayLeadingPlus=True)"
assert text.count(before)==1
text=text.replace(before,after,1)
exec(compile(text,str(Path(__file__).resolve())+'::corrected_journal4915','exec'),globals())
