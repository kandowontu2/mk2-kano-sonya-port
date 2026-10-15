"""Native all-mode physical publications and inherited CPU RGB transport tag.

The original round reset temporarily clears both published actors. Bind all
3606 observations to the independent whole round ledger, including its null
actor fields, rather than requiring a fighting actor during native teardown.
The executed6670 all-mode assertion failure remains false. The CPU observer
also publishes MK2_KNIFE_RAM_RGB_DIGEST, not the inherited finisher tag.
"""
import inspect
import finish_kano_cpu_launch_audio_v6670 as original
ROOT,need,sha=original.ROOT,original.need,original.sha


def bindings(text):
 rows=original.model.original.rows(text,'MK2_MAUDIO_BINDING')
 by={(int(r['frame']),int(r['slot'])):r for r in rows}
 need(len(rows)==len(by)==1803*2 and set(by)=={(f,s)for f in range(1813,3616)for s in(1,2)},
      'Every complete physical binding field through natural terminal')
 physical=original.motion.state.knife.overlap.round_model.rows(text,'FIELD')
 rounds={(r['frame'],r['slot']):r for r in physical}
 null=[]
 for key,row in by.items():
  frame,slot=key
  need(row['writes']=='0'and row['assistance']=='none'and row['roster']=='17','Every actual audio physical binding passive and true roster')
  actor,main,owner=(int(row[k],16)for k in('actor','main','owner'))
  if key in rounds:
   native=rounds[key]
   need((actor,main)==(native['actor'],native['main'])and native['ids']=='17,17',
        'Every audio actor/Main publication agrees with independently checked complete native round ledger')
   if not native['valid']:
    previous=by[frame-1,slot]
    need(native['mode']==6 and native['hp']==161 and actor==0 and row['id']=='-1'and
         main==int(previous['main'],16)and owner==int(previous['owner'],16),
         'Native mode6 reset clears publication, retaining its actual Main owner; no fighting actor fabricated')
    null.append(dict(frame=frame,slot=slot,main=row['main'],retainedOwner=row['owner']))
    continue
   need(owner==native['owner']and int(row['id'])==native['id'],'Every valid physical source owner and identity matches whole native ledger')
  need(actor==owner and row['id']=='17','All actual published living actors retain their true owned Kano identity')
 return dict(passed=True,completePhysicalFields=len(rows),nativeNullActorResetFields=null,
             allModeRecordsBoundWithoutDiscard=True,fullOwnerInterruptionAcceptance=False)

code=inspect.getsource(original.finish)
before="""need(len(binding)==1803*2 and {(int(r['frame']),int(r['slot']))for r in binding}==
      {(f,s)for f in range(1813,3616)for s in(1,2)}and
      all(r['actor']==r['owner']and r['id']==r['roster']=='17'and r['writes']=='0'and r['assistance']=='none'for r in binding),
      'Every true owned physical role through native entry, damage, KO, reset and natural terminal')"""
need(code.count(before)==1,'Only erroneous always-fighting-actor assumption replaced by whole native all-mode bindings')
code=code.replace(before,'physical_bindings=bindings(text)',1)
before='completePhysicalBindingFields=len(binding),allNativeRGBCallbackDigests=rgb'
need(code.count(before)==1,'Publish complete independently bound transient-null native fields')
code=code.replace(before,'completePhysicalBindingFields=len(binding),physicalBindingProof=physical_bindings,allNativeRGBCallbackDigests=rgb',1)
before="'MK2_EARNED_SUBZERO_RGB_DIGEST'"
need(code.count(before)==1,'Exact inherited CPU observer RGB digest inventory key')
code=code.replace(before,"'MK2_KNIFE_RAM_RGB_DIGEST'",1)
before='Path(__file__),Path(model.__file__)'
need(code.count(before)==1,'Pin original executed finisher and explicit tag rejection')
code=code.replace(before,"Path(__file__),Path(original.__file__),ROOT/'audit_v6673_cpu_callback_tag_rejection/failure.json',Path(model.__file__)",1)
scope=dict(original.__dict__,__file__=__file__,original=original,bindings=bindings)
exec(compile(code,__file__+'::whole_same_terminal_audio_actual_RGB_tag','exec'),scope)
finish=scope['finish']
