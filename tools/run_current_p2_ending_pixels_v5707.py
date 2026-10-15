"""Whole source-qualified current P2 ending renderer; raw buffers RAM only.

Retain5266's complete collector/model/export/error gates; bind the actually
qualified P2 controllers, full original P2 model and new read-only observer.
"""
import argparse,inspect,json,traceback
from pathlib import Path
from types import SimpleNamespace
import run_p1_ending_deferred_pixels_v5266 as previous
import qualify_current_p2_ending_source_v5705 as source
import run_current_kano_p2_campaign_v5621 as kano
import run_verified_subzero_sonya_p2_campaign_v5688 as sonya
import ending_raster_cpu_cycle_model_v4740 as model
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
current=previous.current


def collector(fighter):
 factory=inspect.getsource(previous.collector)
 changes=[('audit_v5264_','audit_v5708_'),('current_p1_ending_pixels','current_p2_ending_pixels'),
  ('code=inspect.getsource(ref.capture)','code=ref.capture_source()\n declared_physical_source=code'),
  ('scene=model.Model(guest,payload,graphics,(17 if fighter==\'kano\'else 18,13))',
   'scene=model.Model(guest,payload,graphics,(13,17 if fighter==\'kano\'else 18))'),
  ('scope=dict(vars(ref),__file__=__file__','scope=dict(vars(ref.original),__file__=__file__'),
  ('model=model,current=current,fighter=fighter)','model=model,current=current,fighter=fighter,declared_physical_source=declared_physical_source)')]
 for before,after in changes:
  need(factory.count(before)==1,'Whole complete collector P2 context/namespace adaptation '+before)
  factory=factory.replace(before,after,1)
 policies=SimpleNamespace(kano=kano,sonya=sonya,metadata_clean=sonya.qualify_payload_metadata_warning)
 scope=dict(vars(previous),__file__=__file__,policies=policies,source=source,model=model)
 exec(compile(factory,__file__+'::entire_RAM_collector_current_P2_controls','exec'),scope)
 return scope['collector'](fighter)


def run(fighter):
 source.observer_source()
 if fighter=='kano':
  boundary=kano.boundary.source_boundary()
  need(boundary['passed']and boundary['physicalInputsExactlyUnchanged']and boundary['physicalSlot']==2,
   'Same genuine complete qualified Kano P2 controls')
 else:sonya.source_boundary()
 result,scene,graphics=collector(fighter)()
 # The completed buffers were compared in the live whole renderer; export
 # only scalar counters/digests. A single native shutdown clock seed is not
 # accepted as pixels and is audited by the separate hardware terminal gate.
 folder=ROOT/f'audit_v5708_{fighter}_current_p2_ending_pixels'
 path=folder/'ending_live_model_terminal.json'
 need(not path.exists(),'Immutable actually completed live renderer export')
 export=dict(actualCompletedFieldRecords=len(scene.records),actualRemainingRGBTargets=len(scene.rgb),
  actualRemainingEvents=[(tag,{k:v for k,v in row.items()if k!='data'})for tag,row in scene.events],
  actualBases=len(scene.groups['FLOOR_BASE']),actualActorOwnerClassifications=len(scene.groups['FLOOR_OWNER']),
  actualQueues=len(scene.groups['FLOOR_QUEUE']),actualPaletteClassifications=scene.palette_checks,
  actualPixelFaultsRejected=scene.counterexamples,actualModelErrors=result['endingModelErrors'],
  inputHashes={str(Path(p).resolve()):h for p,h in graphics.items()},
  completedNativeCapture=True,fullEndingPixelsAccepted=False,fullPortAcceptance=False)
 path.write_text(json.dumps(export,indent=2)+'\n')
 need(result['passed']and result['nativeExit']==0 and not result['endingModelErrors'],
  'Every actual native transport/model/pixel error remains fatal; never accepted by an exporter alone')
 print(json.dumps(dict(fighter=fighter,physicalSlot=2,actualCompletedFieldRecords=len(scene.records),
  actualNativePixelFaultsRejected=len(scene.counterexamples),fullEndingPixelsAccepted=False,
  independentHardwareTerminalAndPageGatesPending=True,fullPortAcceptance=False),indent=2),flush=True)


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 args=parser.parse_args();run(args.fighter)
