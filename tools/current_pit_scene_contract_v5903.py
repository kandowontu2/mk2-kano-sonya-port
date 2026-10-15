"""Whole2107 native Pit constructor/phase/FIFO/cache/exit/cue gates in RAM.

Source bindings and exact complete raster run online, not via synthetic paths.
All31original actual movie corruptions plus physical earned12faults reject.
Normal original physical shadows and actual cinematic palette stay distinct.
"""
import hashlib,inspect,struct
from collections import defaultdict
from types import SimpleNamespace
import current_cross_pit_earned_state_v5893 as native
import verify_current_native_pit_matrix_v2107 as original
import test_current_native_pit_matrix_v2136 as faults_original
import run_current_tomb_ram_matrix_v3648 as continuous
need,ROOT=original.need,original.ROOT

def source_graphics(payload,pins):
 image=bytearray(continuous.source_graphics(payload,pins))
 header,start,dest=0x130000,0x134000,0x1e80000
 need(payload[header:header+4]==b'KPT2','Declared native Pit graphics payload')
 source,count,destination=struct.unpack_from('<III',payload,header+4)
 need((source,destination)==(start,dest) and 0<count<=len(payload)-source and
      destination+count<=len(image),'Entire bounded source-native Pit graphics upload')
 image[dest:dest+count]=payload[source:source+count]
 return bytes(image)

# Preserve every original native movie invariant. Only the observation source
# is the actual online RAM scene, rather than a retired raw-file capture.
whole=inspect.getsource(original.verify)
first=whole.index(" begins,results,ends,physical=")
last=whole.index(" print('Current native Pit full movie")
native_source='def native_gate(scene,log,guest,payload,fighter,side,ids):\n'
native_source+=" identity=17 if fighter=='kano'else 18;victim=35-identity\n groups=scene.groups\n state=native.check_log(log,fighter,side,6,guest=guest)\n original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()\n"
code_first=whole.index(" original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()")
code_last=whole.index(' image=bytearray(',code_first)
native_source+=whole[code_first:code_last].replace(" original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()\n",'',1)
native_source+=whole[first:last]
native_source+=" return dict(passed=True,nativeState=state,movie=dict(enter=enter,impact=impact,nextScreen=end,physicalPointerRetirement=normal_end,actualActor=a,actualMain=m,actualID=victim,originalNativeMode9Exit=movie_exit,actualMovieAddressRepurposed=cleared,fallingGroups=20,impactGroups=1,initialPreloads=1,staticInitializerBranches=branches,observedPreservedRegisters=7),sampledFrames=len(expected),sourceBoundProjections=len(queues),nativeCommands=commands,originalVictimVoiceGroup=voice,actualMoviePoses=sorted(poses[4]),originalShakeChanges=changes)\n"
scope=dict(vars(original),native=native)
exec(compile(native_source,__file__+'::whole2107_native_movie_contract','exec'),scope)
native_gate=scope['native_gate']
NATIVE_SOURCE_SHA256=hashlib.sha256(native_source.encode()).hexdigest().upper()

fault_source=inspect.getsource(faults_original.run)
first=fault_source.index(" movie=proof['movie'];")
last=fault_source.index(" print(case+' all31specificcorruptions")
fault_source='def movie_faults(scene,log,guest,payload,fighter,side,ids,proof):\n'+\
 " groups=scene.groups;case=fighter+str(side);model=SimpleNamespace(need=need)\n tests=[]\n"+\
 " def copied():return defaultdict(list,{tag:[dict(r)for r in rows]for tag,rows in groups.items()})\n"+\
 " def run_copy(g):return native_gate(SimpleNamespace(groups=g),log,guest,payload,fighter,side,ids)\n"+\
 " def reject(name,change,wanted):\n  g=copied();change(g)\n  try:run_copy(g)\n  except ValueError as error:\n   need(wanted in str(error),'Unexpected movie fault rejection '+name+': '+str(error))\n   tests.append(dict(name=name,rejected=True,validation=str(error)))\n  else:raise ValueError('Corrupted actual movie accepted '+name)\n"+\
 fault_source[first:last]+" need(native_gate(scene,log,guest,payload,fighter,side,ids)==proof,'Unmodified whole native movie positive restoration')\n return tests\n"
fault_scope=dict(vars(original),need=need,native_gate=native_gate,SimpleNamespace=SimpleNamespace)
exec(compile(fault_source,__file__+'::whole2136_actual31movie_faults','exec'),fault_scope)
movie_faults=fault_scope['movie_faults']
FAULT_SOURCE_SHA256=hashlib.sha256(fault_source.encode()).hexdigest().upper()

def scene_contract(scene,log,guest,payload,fighter,side,reference,ids):
 proof=native_gate(scene,log,guest,payload,fighter,side,ids)
 with __import__('gzip').open(reference/'run.log.gz','rt')as reader:previous=reader.read()
 physical=('MK2_STAGE_BOOT ','MK2_STAGE_INPUT ','MK2_STAGE_DAMAGE ','MK2_STAGE_MATCH ',
           'MK2_STAGE_SELECT ','MK2_STAGE_SELECT_ID ','MK2_STAGE_WINDOW ','MK2_STAGE_COMMAND ','MK2_STAGE_RESULT ')
 need([s for s in log.splitlines()if s.startswith(physical)]==
      [s for s in previous.splitlines()if s.startswith(physical)],
      'Entire independent enabled-audio physical paid selection/health/KO/action/cleanup trajectory')
 groups=scene.groups;movie=proof['movie'];enter,clear=movie['enter'],movie['actualMovieAddressRepurposed']
 expected=list(range(groups['FLOOR_BEGIN'][0]['origin']+1,movie['nextScreen']+31))
 need([r['frame']for r in scene.records]==expected and scene.pre_count==len(groups['FLOOR_PRE_FRAME']) and
      scene.flip_count==len(groups['FLOOR_LATCH']) and scene.loads==scene.fills>0 and
      not scene.events and not scene.raw and not scene.rgb and len(scene.counterexamples)==2,
      'Every one-base continuous CPU/DMA/shift/VRAM/palette/RGB field and actual pixel faults retained')
 visible=set();draws=defaultdict(set)
 queue={(q['frame'],q['cursor']):q for q in groups['FLOOR_QUEUE']}
 for d in groups['FLOOR_QUEUE_DISPATCH']:
  q=queue[d['queue_frame'],d['cursor']]
  if q['slot']==4:draws[d['frame']].add(q['pose'])
 for r in scene.records:
  if r['body']['4']['pixels']>100:visible.update(draws[r['frame']-1])
 need(visible==set(proof['actualMoviePoses']) and len(visible)==6,
      'All six actual own cinematic poses are visibly scanned out, not metadata-only')
 anchors={17:134,18:135}
 for t in groups['FLOOR_QUEUE_TRANSFORM']:
  q=queue[t['frame'],t['cursor']]
  if q['slot'] in (1,2):need(t['floor']==q['floor']==t['stageY']-anchors[q['id']],
                             'Physical own native ground anchor remains aligned before cinematic retirement')
 from unittest.mock import patch
 with patch.object(continuous.shadow,'data',return_value=(groups,scene.buffers,None,None,scene.owners)):
  shadows=continuous.shadow.inspect(None)
 need(shadows['rowStreamVerified'] and not shadows['failures'] and not shadows['oversized_rows'] and
      set(map(tuple,shadows['identities']))=={(s,ids[s-1])for s in (1,2)},
      'All actual own compressed physical floor-shadow rows and identities retained')
 faults=movie_faults(scene,log,guest,payload,fighter,side,ids,proof)
 earned=native.actual_faults(log,fighter,side,guest)
 need(len(faults)==31 and len(earned)==12,'Entire actual native movie31 and full earned12 counterexamples')
 proof.update(nativeShadowCopies=shadows['checked_copies'],actualMovieFaultsRejected=faults,
              actualEarnedFaultsRejected=earned,visibleMoviePoses=sorted(visible),
              exactRGBPixels=len(expected)*400*254,oneInitialBaseOnly=True,laterTargetsNeverUsedAsAnchors=True)
 return proof
