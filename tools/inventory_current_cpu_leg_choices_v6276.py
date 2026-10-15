"""Current bounded CPU inventory: accepted pairs and actual mixed-case rejection.

Do not relabel the third leg->Square continuation as an accepted standalone
pair or a game bug. Keep the entire original verifier and its rejection.
Qualify the first two true legs, all-mode state/health, and native RNG choices.
"""
import inspect,json,traceback
from pathlib import Path
import verify_current_existing_cpu_leg_choices_v6274 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v6277_current_cpu_leg_choice_inventory'

def gate(text,guest):
 health,by=prior.stream.health_ledger(text,guest,'kano');state=prior.stream.state_ledgers(text,guest,'kano',by)
 complete=prior.pair.rows(text,'COMPLETE');need(len(complete)==3,'Three observed completed CPU pair records, not three accepted contracts')
 legs=[prior.pair.verify_pair(text,'kano',r['cycle'],guest)for r in complete]
 need(all(r['passed']and r['target']=='sonya'and r['damage']==35 and r['held_fields']==46 for r in legs[:2]),'First two entire original native leg choreography/physics/cleanup contracts')
 rejection={'Continuous real original action-store instruction/register/ownership ledger','Original follow-up is either unchanged-state native setup or exact walking-to-attack publication'}
 third=legs[2];need(not third['passed']and set(third['errors'])==rejection,'Retain actual third mixed-case rejection; no new paired fault may be hidden')
 choices=prior.choice_gate(prior.choice_rows(text),guest);need({r['move']for r in choices}=={'ring','square','bicycle'},'All three actual native Sonya traveling RNG branches')
 square=next(r for r in choices if r['move']=='square')
 need(third['own_handoff']<square['frame']<third['victim_handoff']and any(r['frame']==square['frame']and r['before']==0x303 and r['after']==0x207 and r['pc']=='0xff877bc0'for r in third['native_followup_actions']),'Actual compound Square starts after owning cleanup but before victim recovery; original verifier stays rejected')
 return dict(wholeNativeHealthLedger=health,wholeNativeStateLedger=state,originalLegContracts=legs,acceptedStandaloneLegCycles=2,rejectedMixedLegSquareCycles=1,nativeChoices=choices,compoundLegToSquareAccepted=False)

def main():
 failed=prior.OUT/'failure.json';need(failed.exists()and not json.loads(failed.read_text())['passed'],'Keep original attempted six-leg qualification failure')
 source=inspect.getsource(prior.main)
 changes={
  'PARENT,actual,baseline,Path(__file__).resolve(),Path(pair.__file__),Path(stream.__file__),Path(phase_source.__file__),Path(current.__file__)':
   'PARENT,actual,baseline,failed,Path(prior.__file__),Path(__file__).resolve(),Path(pair.__file__),Path(stream.__file__),Path(phase_source.__file__),Path(current.__file__)',
  'actualCurrentCompletedCPULegCycles=6':'actualCurrentCompletedCPULegCycles=4,actualCurrentRejectedMixedLegSquareCycles=2,compoundLegToSquareAccepted=False',
  'actualExistingCPULegCycles=6':'actualExistingCPULegCycles=4,rejectedMixedLegSquareCycles=2',
  'current frozen table/AI/ladder inventory plus existing current actual CPU leg and all three natural choice branches independently requalified; no repeated native games':
   'current frozen table/AI/ladder inventory plus four existing true complete CPU legs and all three actual Sonya native RNG branches independently requalified; two original mixed-case rejections retained; no repeated native games',
  'Current Kano traveling CPU routes and remaining branch-specific fidelity, reusing already complete UI/campaign/ending/Friendship evidence':
   'Validate actual compound CPU leg-to-Square continuation, retaining original standalone rejections; then current Kano traveling CPU routes and remaining fidelity, without repeating complete UI/campaign/ending/Friendship checks',
 }
 for before,after in changes.items():need(source.count(before)==1,'Exact truthful inventory scope/pin change '+before[:95]);source=source.replace(before,after,1)
 scope=dict(prior.main.__globals__,__file__=__file__,OUT=OUT,prior=prior,failed=failed,gate=gate)
 exec(compile(source,__file__+'::whole_original_existing_trace_checks_with_mixed_rejection_retained','exec'),scope);scope['main']()

if __name__=='__main__':
 try:main()
 except Exception as error:
  OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n');raise
