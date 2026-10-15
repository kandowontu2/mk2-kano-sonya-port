"""Complete same-RAM proof with actual nonvacuous, slot-neutral faults.

Preserve the earlier executed fixed-word rejection; do not rerun a game.
Use an actual bit change in the chosen native packet/port/DSP record.
"""
import qualify_launch_fireball_interruption as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
source=previous.source
for before,after in [
 ('audit_launch_fireball_interruption_checked_','audit_launch_fireball_faults_checked_'),
 ("('wrong native projectile parent','parentActor','010350A0')","('wrong native projectile parent','parentActor','01000000')"),
 ("('wrong native projectile victim task','victimMain','0106A370')","('wrong native projectile victim task','victimMain','01000000')"),
 ("reject('native packet '+tag,tag,key,value,dict(frame=r['frame']),lambda c:packet_gate(c['text']))",
  "reject('native packet '+tag,tag,key,format(int(r[key],16)^1,'04X'),dict(frame=r['frame'],**{key:r[key]}),lambda c:packet_gate(c['text']))"),
 ('Path(__file__),Path(original.__file__)',"Path(__file__),Path(previous.__file__),ROOT/'audit_launch_fireball_fault_adapter_rejection/failure.json',Path(original.__file__)"),
]:
 need(source.count(before)==1,'Only vacuous/non-slot-neutral fault or exact source pin changed');source=source.replace(before,after,1)
scope=dict(previous.scope,__file__=__file__,previous=previous)
exec(compile(source,__file__+'::whole_same_RAM_source_proof_actual_changed_record_faults','exec'),scope)
qualify=scope['qualify']
