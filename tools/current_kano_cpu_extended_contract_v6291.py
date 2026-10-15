"""Whole native state/HP and actual Kano AI choices; move-phase acceptance separate.

Source-exact identity/table context adaptation of the qualified original1800
field ledgers and native RNG contract. Do not promote this to full move art,
shadow, audio, contacts or the old two-knives/two-chokes scenario.
"""
import inspect
import verify_current_existing_cpu_leg_choices_v6274 as original
import verify_current_kano_cpu_overlap_v1963 as knife
need=original.need


def bind(function,changes):
 text=inspect.getsource(function)
 for before,after in changes.items():
  need(text.count(before)==1,'Only actual native Kano identity/table context: '+before)
  text=text.replace(before,after,1)
 scope=dict(function.__globals__);exec(compile(text,__file__+'::'+function.__name__,'exec'),scope)
 return scope[function.__name__]


health=bind(original.stream.health_ledger,{
 "expected_ids=f'{pair.HUMANS[player]},18'":"expected_ids=f'{pair.HUMANS[player]},17'",
 'row[\'schedule\']==0xfffa3180':"row['schedule']==0xfffa3000",
 "(18 if row['slot']==2 else pair.HUMANS[player])":"(17 if row['slot']==2 else pair.HUMANS[player])"})
state=bind(original.stream.state_ledgers,{
 "==(18,pair.HUMANS[player])":"==(17,pair.HUMANS[player])",
 "==(18,18,pair.HUMANS[player],pair.HUMANS[player],0,1,2)":"==(17,17,pair.HUMANS[player],pair.HUMANS[player],0,1,2)"})
choices=bind(original.choice_gate,{
 "0xfffbc200":"0xfffbc000","0xfffbc220":"0xfffbc020","0xfffbc250":"0xfffbc050",
 "0xfffbc280":"0xfffbc080","0xfffbc2b0":"0xfffbc0b0","0xfffbc2c0":"0xfffbc0c0",
 "0xfffbc2f0":"0xfffbc0f0","0xfffbc320":"0xfffbc120",
 "ring=":"knife=","square=":"ball=","bicycle=":"blade=",
 "==18 and":"==17 and","==0xfffa3180":"==0xfffa3000",
 "expected=['entry','first_call','first_result','bicycle'];chosen='bicycle'":"expected=['entry','first_call','first_result','blade'];chosen='blade'",
 "chosen='square'if n(events[4],'carry')else'ring'":"chosen='ball'if n(events[4],'carry')else'knife'"})


def verify(text,guest):
 hp,by=health(text,guest,'kano');stores=state(text,guest,'kano',by)
 native=choices(original.choice_rows(text),guest)
 cold=original.pair.rows_prefix(text,'MK2_P2CPU_COLD_LIVE ')
 selection=original.pair.rows_prefix(text,'MK2_P2CPU_SELECT_RESULT ')
 need(len(cold)==len(selection)==1 and cold[0]['cpu_id']==cold[0]['human_id']==17
      and selection[0]['initial_cpu']==selection[0]['human_id']==17
      and selection[0]['errors']==0 and selection[0]['checks']==50,
      'Actual current cold selection, no CPU or human proxies')
 try: old=knife.verify(text,guest)
 except (AssertionError,ValueError,KeyError,IndexError)as error:
  old=dict(passed=False,error=repr(error),scope='unchanged original two-choke/two-knife scenario, not a generic long-match gate')
 return dict(passed=True,wholeNativeHealthLedger=hp,wholeNativeStateLedger=stores,nativeChoices=native,
             originalKnifeScenario=old,fullMovePhaseAcceptance=False,artShadowAudioAcceptance=False,
             fullPortAcceptance=False,scope=__doc__)
