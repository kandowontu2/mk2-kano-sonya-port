"""Same complete review, remove both duplicate own native cleanup witnesses.

The actual CPU Main executes its body cleanup twice in the same handoff.
The original pair gate requires a real witness and correctly still finds
the second after one is changed. Preserve the earlier incomplete negative;
test missing handoff witnesses, without weakening the actual pair contract.
The separate continuous-store gate already qualifies every actual store.
"""
import inspect
import traceback
import seal_native_kano_laser_post_reset_controls_review as prior

ROOT,need,sha,base=prior.ROOT,prior.need,prior.sha,prior.base
OUT=ROOT/'audit_native_kano_laser_post_reset_controls_complete_review'


def run(actual):
    once=prior.bodies.prior.once
    source=inspect.getsource(prior.run)
    source=once(source,"    cycle=lambda r:r['cycle']=='4'\n",
        """    cycle=lambda r:r['cycle']=='4'
    def remove_all(tag,predicate):
        removed=[s for s in text.splitlines()if s.startswith(tag+' ')and predicate(dict(base.re.findall(r'(\\w+)=([^\\s]+)',s)))]
        need(len(removed)==2,'Both actual same-field own-Main body-cleanup witnesses present')
        return '\\n'.join(s for s in text.splitlines()if s not in removed)+'\\n'
""")
    source=once(source,
        "('next_round_actual_own_cleanup_store_wrong',mutate('MK2_CPU_PAIR_FLAG','after','FFFF',lambda r:cycle(r)and r['kind']=='body'and r['pc']=='FF83EEB0'))",
        "('next_round_actual_own_cleanup_witnesses_missing',remove_all('MK2_CPU_PAIR_FLAG',lambda r:cycle(r)and r['slot']=='2'and r['kind']=='body'and r['pc']=='FF83EEB0'and int(r['frame'])==cpu['own_handoff']))")
    source=once(source,'for p in (Path(__file__),Path(controls.__file__),',
                "for p in (Path(__file__),Path(prior.__file__),prior.OUT/'failure.json',Path(controls.__file__),")
    scope=dict(vars(prior),prior=prior,OUT=OUT,__file__=__file__)
    exec(compile(source,__file__+'::whole_actual_review_faults_both_native_cleanup_witnesses','exec'),scope)
    scope['run'](actual)


def execute(actual):
    try:run(actual)
    except Exception as error:
        need(not OUT.exists(),'Preserve exact same-capture complete review failure');OUT.mkdir()
        base.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False))
        print(prior.json.dumps(dict(passed=False,error=repr(error))),flush=True)
