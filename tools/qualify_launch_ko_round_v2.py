"""Native noncombat branch stops the surviving roll when the round is won.

Use the unique original60Hz tick between actual physical/owner snapshots;
never infer the stop from PCM, fit a clock, or assume EOF through a KO.
"""
import inspect,json
from decimal import Decimal
from pathlib import Path
import qualify_launch_ko_round as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
rows=previous.rows

def events(carrier,pins):
 events=previous.events(carrier,pins);fields=rows(carrier['text'],'MK2_KO_FIELD');owners=rows(carrier['text'],'MK2_INTERRUPT_OWNER')
 ko=int(previous.one(carrier['text'],'MK2_HSPECIAL_KO')['frame'])
 event=next(e for e in events if e['slot']==2 and ko-20<int(e['marker']['frame'])<ko)
 by={int(v['frame']):v for v in fields if v['slot']=='2'}
 at=next(f for f in sorted(by)if f>ko and by[f]['mode']!='2');before,after=by[at-1],by[at]
 need(before['mode']=='2'and after['mode']=='5'and all(v['hp']=='161'and v['actor']==v['owner']==event['marker']['a8']and v['main']==event['marker']['a13']and v['id']=='17'for v in(before,after)),
      'Actual surviving unchanged owner/full health reaches original winner/noncombat mode')
 clock=previous.mirror.old.audio;period=clock.ATTO//60;origin=event['sharedTimerOrigin'];left=int(Decimal(before['seconds'])*clock.ATTO);right=int(Decimal(after['seconds'])*clock.ATTO)
 ticks=[origin+n*period for n in range(1,100)if left<origin+n*period<=right]
 need(len(ticks)==1,'Exactly one source60Hz guard tick in actual mode/ownership boundary, no fitted interval')
 stop=ticks[0];owner={(int(v['frame']),int(v['slot'])):v for v in owners}
 need(owner[at-1,2]['actor']==event['marker']['a8']and owner[at,2]['actor']==owner[at,2]['main']=='00000000'and
      owner[at,2]['id']==owner[at,2]['health']=='0','Actual owner retirement brackets that unique noncombat guard tick')
 update=max([int(Decimal(h['seconds'])*clock.ATTO)for h in carrier['pcmHeaders']if int(Decimal(h['seconds'])*clock.ATTO)<stop]+[stop-period])
 cutoff=clock.sample_clock(str(Decimal(update)/clock.ATTO),True);generated=cutoff-event['start']
 need(0<generated<len(event['sample']),'Actual noncombat stop is a finite partial roll source, not EOF')
 event.update(stopAttoseconds=stop,lastStreamUpdateAttoseconds=update,generatedBeforeStop=generated,noncombatModeBoundaryFrame=at,
              stopReason='source-exact noncombat guard with unique actual physical/ownership bracket')
 states={(int(v['frame']),int(v['channel'])):v for v in rows(carrier['text'],'MK2_INTERRUPT_CHANNEL')}
 state=states[at,event['channel']]
 need(state['sample']=='4294967295'and float(state['position'])==event['positions'][generated-1],'Actual survivor channel stopped at independently calculated native cache prefix')
 return events

source=inspect.getsource(previous.qualify)
source=source.replace("out=ROOT/f\"audit_launch_ko_round_checked_p{carrier['side']}\"","out=ROOT/f\"audit_launch_ko_round_v2_checked_p{carrier['side']}\"")
source=source.replace('Path(__file__),Path(mirror.__file__)','Path(__file__),Path(original_adapter.__file__),Path(mirror.__file__)')
scope=dict(vars(previous),__file__=__file__,events=events,original_adapter=previous)
exec(compile(source,__file__+'::whole_original_KO_reset_audio_with_noncombat_branch','exec'),scope)
qualify=scope['qualify']

def preserve_rejection(carrier):
 out=ROOT/'audit_launch_ko_round_p2_eof_model_rejection';need(not out.exists(),'Exact failed old EOF-only model remains rejected')
 event=[e for e in previous.events(carrier,{})if e['slot']==2 and int(e['marker']['frame'])<int(previous.one(carrier['text'],'MK2_HSPECIAL_KO')['frame'])][-1]
 owner=next(v for v in rows(carrier['text'],'MK2_INTERRUPT_OWNER')if v['slot']=='2'and v['actor']=='00000000'and int(event['marker']['frame'])<int(v['frame'])and
            int(Decimal(v['seconds'])*previous.winner.ATTO)<event['stopAttoseconds'])
 report=dict(passed=False,nativeTerminal=carrier['terminal'],oldModelFailure='Every source-owned actor/Main/ID/HP until independent stop',
             actualEarlyRetirement=owner,oldIncorrectAssumption='Unhit surviving roll always keeps its full EOF tail, even after native combat mode ends',
             actualNativeGameFailure=False,originalModelUnchanged=True,inputHashes={str(Path(previous.__file__)):sha(previous.__file__)},
             fullPortAcceptance=False,newNativeBoots=0)
 out.mkdir();(out/'failure.json').write_text(json.dumps(report,indent=2)+'\n')
