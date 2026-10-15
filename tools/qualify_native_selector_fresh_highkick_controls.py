"""Exact ordinary High Kick control policy; record missing target coverage."""
import inspect
import json
from pathlib import Path
import qualify_native_selector_fresh_lowkick_controls as prior

OUT=prior.sync.ROOT/'audit_native_selector_fresh_highkick_controls_checked'
CAPTURE=prior.sync.ROOT/'audit_native_selector_fresh_highkick_owners_capture_checked/report.json'
scope=dict(vars(prior),OUT=OUT,CAPTURE=CAPTURE,__file__=__file__)
for function in (prior.gate,prior.execute):
    source=inspect.getsource(function)
    source=source.replace('LOWKICK_INPUT','HIGHKICK_INPUT').replace('LOWKICK_BIND','HIGHKICK_BIND').replace('walk_lowkick','walk_highkick')
    exec(compile(source,__file__+'::original_full_policy_highkick_field','exec'),scope)


def main(prepared):
    report=scope['execute'](prepared)
    text=prepared.RAM_CASES[prepared.SCOPE['KEY']][1]
    markers=[r for r in prior.ledger.rows(text,'MK2_MAUDIO_SOUND') if r['word'] in ('6B00','6B01','6B02')]
    owners=prior.ledger.rows(text,'MK2_VOICE_OWNER')
    choices=[r for r in prior.ledger.rows(text,'MK2_SONYA_CHOICE_EVENT') if r['kind'] in ('ring','square','bicycle','leg')]
    damages=[r for r in prior.ledger.rows(text,'MK2_CPU_ROUND_HEALTH') if r['slot']=='2'
             and int(r['after'])<int(r['before']) and int(r['before'])<=161]
    prior.sync.need(not markers and len(owners)==13850 and all(r['actor']=='00000000' for r in owners)
                    and [(r['frame'],r['kind']) for r in choices]==[('1817','ring'),('2538','ring')]
                    and not damages,'Actual target context absent; no imagined private voice/hit coverage')
    coverage=dict(actualNativeIdentity=report['actualNativeIdentity'],actualCPUChoices=choices,
                  savedOwnerSnapshots=len(owners),nonzeroSavedOwners=0,privateCueLaunches=0,
                  incomingCPUHealthDamageStores=0,privateVoiceInterruptionCovered=False,
                  wholeControlPolicyPassed=True,fullPortAcceptance=False,
                  consequence='Preserve clean actual control run; required voice-interruption context remains open. Do not replay this same policy as acceptance.')
    (OUT/'missing_target_context.json').write_text(json.dumps(coverage,indent=2)+'\n')
    return report,coverage
