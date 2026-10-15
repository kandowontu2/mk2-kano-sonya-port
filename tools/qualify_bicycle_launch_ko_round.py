"""Whole same-terminal Bicycle KO/reset, projectile, body and source audio."""
import inspect,json
from pathlib import Path
import qualify_sonya_launch_ko_round as square
import qualify_sonya_launch_ko_round_v2 as square2
import launch_fireball_interruption_model as projectile
ROOT,need,sha=square.ROOT,square.need,square.sha
rows=square.rows

source=square.source
for before,after in (
 ('limit=5 if side==1 else 7;points=40 if side==1 else 26', 'limit=8;points=22'),
 ("ids={side:'18',3-side:'8'}", "ids={side:'18',3-side:'1'}"),
 ('floor_source.subzero_floor(guest)','projectile.stock_floor(guest,1)'),
 ('Every exact native40HP uppercut or26HP jump kick, including final KO saturation','Every exact original22HP fireball contact, including native lethal saturation'),
):
 need(source.count(before)==1,'Exact native Bicycle/Liu/22HP boundary adaptation');source=source.replace(before,after,1)
scope=dict(vars(square),projectile=projectile)
exec(compile(source,__file__+'::whole_native_health_KO_reset_rearm_physical_contract','exec'),scope)
physical=scope['physical']

def body_publication(text,guest,by):
 source=inspect.getsource(square.prior.body_publication)
 need(source.count('ids={1:17,2:17}')==1,'Whole native descriptor/clip/FIFO contract')
 side=int(square.prior.one(text,'MK2_HSPECIAL_RESULT')['side'])
 scope=dict(vars(square.prior),body_ids={side:18,3-side:1})
 exec(compile(source.replace('ids={1:17,2:17}','ids=body_ids'),__file__+'::whole_native_Sonya_Liu_body_publication','exec'),scope)
 return scope['body_publication'](text,guest,by)

def projectile_gate(c):
 source=inspect.getsource(projectile.projectile_gate)
 for before,after in (("'MK2_HSPECIAL_FIELD'","'MK2_KO_FIELD'"),
  ("int(r['after'])<int(r['before'])", "r['pc']=='FF836700' and int(r['after'])<int(r['before'])"),
  ('len(contacts)==len(health)==2','len(contacts)==len(health)==9')):
  need(source.count(before)==1,'Whole original nine projectile collision/contact/health branch contract');source=source.replace(before,after,1)
 scope=dict(vars(projectile));exec(compile(source,__file__+'::whole_original_native_projectile_branches_through_KO','exec'),scope)
 return scope['projectile_gate'](c)

def source_events(c,pins):
 original=square.prior.mirror.old
 source=original.source
 source=source[source.index('def source_events(carrier,pins):'):source.index('\ndef predict(carrier,pins):')]
 for before,after in (
  ("int(r['after'])<int(r['before'])", "r['pc']=='FF836700'and int(r['after'])<int(r['before'])"),
  ("len(health)==2", "len(health)==9"),
  ("len(events)==(4 if carrier['move']=='bicycle'else 2)", "len(events)==18 and carrier['move']=='bicycle'"),
 ):
  need(source.count(before)==1,'Complete original two-channel interrupted timer/stream source operations');source=source.replace(before,after,1)
 scope=dict(vars(original));exec(compile(source,__file__+'::whole_native_nine_Bicycle_launch_and_cry_sources','exec'),scope)
 events=scope['source_events'](c,pins)
 fields={(int(r['frame']),int(r['slot'])):r for r in rows(c['text'],'MK2_KO_FIELD')}
 for e in events:
  e['slot']=c['side'];e['incoming']=next(r for r in rows(c['text'],'MK2_INTERRUPT_HEALTH') if r['pc']=='FF836700'and int(r['slot'])==c['side']and int(e['marker']['frame'])<int(r['frame'])<int(e['marker']['frame'])+120)
  field=fields[int(e['marker']['frame']),c['side']];marker=e['marker']
  need(marker['mask']=='FFFF'and marker['a8']==field['actor']==field['owner']and marker['a13']==field['main']and field['id']==field['roster']=='18'and
       marker['pc']==('FFF9A4C0'if marker['word']=='6B01'else'FFF9A690'), 'Every actual true18 Bicycle launch/cry native opcode and actor/Main owner')
 return events

def owners(c,events):
 original=square.prior.mirror
 source=inspect.getsource(original.owners)
 source=source.replace("rows(text,'MK2_HSPECIAL_FIELD')","rows(text,'MK2_KO_FIELD')").replace("r['id']=='17'","r['id']=='18'")
 source=source.replace("e['slot']==slot and", "e['slot']==slot and e['sample_id']==14 and",1)
 before="  if int(r['channel'])in(11,13):need(r['length']=='0'and r['position']=='0'and r['sample']=='4294967295','Unused aux channels stay genuinely idle')"
 need(source.count(before)==1,'Whole original source-channel lifetime gate')
 source=source.replace(before,"  if int(r['channel'])not in(10+2*(carrier['side']-1),11+2*(carrier['side']-1)):need(r['length']=='0'and r['position']=='0'and r['sample']=='4294967295','Both actual opponent source channels remain genuinely idle')",1)
 cached={}
 def inventory(text,tag):
  if tag not in cached:cached[tag]=rows(text,tag)
  return cached[tag]
 scope=dict(vars(original),rows=inventory)
 exec(compile(source,__file__+'::whole_nine_Bicycle_owners_both_actual_source_stop_clocks','exec'),scope)
 return scope['owners'](c,events)

def packet_gate(text):
 source=inspect.getsource(square.prior.mirror.qualifier.packet_gate)
 need(source.count('len(launches)in(2,4)')==1,'Whole native sound packet/delivery grammar')
 source=source.replace('len(launches)in(2,4)','len(launches)==18')
 scope=dict(vars(square.prior.mirror.qualifier));exec(compile(source,__file__+'::whole_DCS_delivery_eighteen_Bicycle_sources','exec'),scope)
 return scope['packet_gate'](text)

def qualify(c):
 out=ROOT/f"audit_bicycle_launch_ko_round_checked_p{c['side']}";need(not out.exists(),'Fresh same-terminal proof')
 need(c['report']['passed']and c['terminal']['nativeExit']==0 and not c['decodeErrors'],'Authoritative native normal terminal')
 pins=dict(c['pins']);need(all(sha(p)==h for p,h in pins.items()),'Whole executed source/candidate unchanged')
 state,by=physical(c['text'],c['guest']);inputs=square.prior.mirror.delivery.delivered(c['text'])
 body=body_publication(c['text'],c['guest'],by);contacts=projectile_gate(c);events=source_events(c,pins);owned=owners(c,events)
 waveform=square2.predict(c,events,pins);need(waveform['passed'],'Every complete native Bicycle launch/cry/DCS PCM sample')
 gate,fault=square.prior.mirror.qualifier.source_audio.dac_models(len(c['pcmHeaders']))
 dac=dict(positive=gate(c['dac'],c['dacHeaders'],c['pcmHeaders']),faults=fault(c['dac'],c['dacHeaders'],c['pcmHeaders']))
 rg,rf=square.prior.mirror.qualifier.source_audio.host.models.rom_models(c['expectedROM'])
 rom=dict(positive=[rg(bytes(c['rom'][p]),p)for p in c['rom']],faults=[v for p in c['rom']for v in rf(bytes(c['rom'][p]),p)])
 packets=packet_gate(c['text'])
 for path in (Path(__file__),Path(square.__file__),Path(square2.__file__),Path(projectile.__file__),ROOT/'mk2/mk2-maincpu.bin',*c['folder'].rglob('*')):
  if path.is_file():pins[str(path.resolve())]=sha(path)
 need(all(sha(p)==h for p,h in pins.items()),'All source and evidence preserved')
 report=dict(passed=True,candidate=square.prior.mirror.old.current.NAME,nativeTerminal=c['terminal'],physicalKOResetRearm=state,
  wholeNativeInputDelivery=inputs,sampledNativeBodyDescriptorClipFIFO=body,completeNativeProjectileBranches=contacts,
  completeIndependentOwnership=owned,completeSourceWaveform=waveform,sourceDAC=dac,wholeSoundROM=rom,completeNativeDCSDelivery=packets,
  inputHashes=pins,fullRasterAcceptance=False,allKOResetMorphCoverageAccepted=False,fullPortAcceptance=False,goalStatus='active',newNativeBoots=0,newBuilds=0,newRawMedia=0)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(passed=True,side=c['side'],physicalFields=state['continuousPhysicalFields'],stereoFrames=waveform['comparedStereoFrames'])),flush=True)
 return report
