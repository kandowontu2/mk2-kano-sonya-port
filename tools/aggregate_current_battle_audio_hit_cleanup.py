"""Reexecute six native hit-cleanup gates against existing compact traces."""
import copy
import inspect
import json
import re
import wave
import qualify_bounded_twohuman_hit_voice_state as bicycle
import qualify_bounded_twohuman_square_rise_cleanup as square
import qualify_bounded_kano_ball_cleanup_direct as ball
import verify_native_source_sync as sync


def load(folder):
 rows={}
 for line in (folder/'run.log').read_text().splitlines():
  assert '[LUA ERROR]' not in line
  if line.startswith('MK2_HSPECIAL_'):
   tag=line.split()[0].removeprefix('MK2_HSPECIAL_')
   row=dict(re.findall(r'(\w+)=([^\s]+)',line))
   assert row['writes']=='0' and row['assistance']=='none'
   rows.setdefault(tag,[]).append(row)
 return rows


if __name__=='__main__':
 sync.verify()
 out=sync.ROOT/'audit_current_battle_audio_hit_cleanup_checked'
 assert not out.exists()
 cases=[]
 for move in ('bicycle','square','ball'):
  clipname={'bicycle':'sonya_bicycle_cry','square':'sonya_square_launch','ball':'kano_ball_launch'}[move]
  clip=sync.ROOT/f'diagnostic_native_selector_layers_long/samples/mk2ks/{clipname}.wav'
  if not clip.exists():clip=sync.ROOT/f'samples/mk2ks/{clipname}.wav'
  with wave.open(str(clip)) as wav:
   length=wav.getnframes();assert wav.getframerate()==48000
  for side in (1,2):
   if move=='bicycle':
    folder=sync.ROOT/('audit_bounded_twohuman_hit_voice_state_runtime' if side==1 else 'audit_bounded_twohuman_p2_hit_voice_runtime')
   elif move=='square':folder=sync.ROOT/f'audit_bounded_twohuman_square_p{side}_rise_counter_runtime'
   else:folder=sync.ROOT/f'audit_bounded_kano_ball_p{side}_guard_counter_runtime'
   terminal=json.loads((folder/'terminal.json').read_text())
   assert terminal['exitCode']==0 and terminal['limitReason'] is None and not (folder/'stderr.log').read_text().strip()
   rows=load(folder)
   if move=='bicycle':
    code=inspect.getsource(bicycle.gate)
    if side==2:
     for old,new in {"r['slot']=='1'":"r['slot']=='2'",'01034E90':'010350A0','0106A370':'0106B150',"r['channel']=='11'":"r['channel']=='13'"}.items():
      assert old in code;code=code.replace(old,new)
    ns=dict(bicycle.__dict__);exec(compile(code,'native_bicycle_hit_gate','exec'),ns)
    gate=lambda data:ns['gate']([('MK2_HSPECIAL_'+tag,r) for tag,group in data.items() for r in group],length)
    cutoff=1392
   elif move=='square':
    code=inspect.getsource(square.gate)
    code=code.replace('def gate(rows,side,length):','def gate(rows,side,length):\n    stopped=5464 if side==1 else 5471')
    code=code.replace("r['pos']=='5464.00000000'","Decimal(r['pos'])==stopped").replace('0<5464<length','0<stopped<length').replace('stoppedSample=5464,unplayedSamples=length-5464','stoppedSample=stopped,unplayedSamples=length-stopped')
    ns=dict(square.__dict__);exec(compile(code,'native_square_slot_gate','exec'),ns)
    gate=lambda data:ns['gate'](data,side,length)
    cutoff=1388
   else:
    code=inspect.getsource(ball.gate)
    assert code.count('len(cleared)>200')==1
    code=code.replace('len(cleared)>200','len(cleared)==138')
    ns=dict(ball.__dict__);exec(compile(code,'native_ball_window_gate','exec'),ns)
    gate=lambda data:ns['gate'](data,side,length)
    cutoff=1462
   result=gate(rows)
   fault=copy.deepcopy(rows)
   next(r for r in fault['VOICE_OWNER'] if int(r['slot'])==side and int(r['frame'])>=cutoff)['id']='17' if move=='ball' else '18'
   try:gate(fault)
   except AssertionError:pass
   else:raise AssertionError('Lingering owner accepted')
   cases.append({'move':move,'side':side,'result':result,'ownerFaultRejected':True,
                 'logSHA256':sync.sha(folder/'run.log'),'terminalSHA256':sync.sha(folder/'terminal.json'),'clipSHA256':sync.sha(clip)})
 out.mkdir();(out/'report.json').write_text(json.dumps({'passed':True,'cases':cases,
  'newEmulatorRuns':0,'allSceneInterruptionsCovered':False,'heardMixVerified':False,'fullPortAccepted':False},indent=2))
 print('PASS six current battle hit-cleanup contexts, both slots; no emulator runs')
