"""Correct receipt prose assertion; retain executed6675 rejection unchanged.

The storage document affirmatively says no additional build was created.
The original assertion accidentally required that exact phrase be absent.
All actual runtime proofs, protected pins and storage checks are unchanged.
"""
import inspect
import journal_kano_cpu_launch_v6675 as original
need=original.need
code=inspect.getsource(original.main)
for before,after in[("'No additional build'not in docs['WORKSPACE_CLEANUP_CURRENT.md']",
                     "'No additional build'in docs['WORKSPACE_CLEANUP_CURRENT.md']"),
                    ('6663<=version(p)<=6674','6663<=version(p)<=6678'),
                    ('6663<=version(p)<=6675','6663<=version(p)<=6677')]:
 need(code.count(before)==1,'Exact document assertion or bounded current evidence range correction')
 code=code.replace(before,after,1)
scope=dict(original.__dict__,__file__=__file__)
exec(compile(code,__file__+'::whole_journal_correct_document_assertion','exec'),scope)
if __name__=='__main__':scope['main']()
