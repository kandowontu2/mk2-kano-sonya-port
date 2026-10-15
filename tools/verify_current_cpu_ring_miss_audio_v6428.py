"""Whole native missed-Ring cue/voice/packet/channel retirement qualification.

Keep full exact RAM waveform/DAC/ROM proof and original packet/ADSP/repeated
double clock gates. A real miss has release5 but no hit/impact audio path.
"""
import argparse,gzip,json,re,struct,subprocess
from pathlib import Path
import capture_current_cpu_ring_miss_audio_v6426 as capture
import verify_current_cpu_ring_audio_v6386 as original

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
CASE=capture.OUT
OUT=ROOT/'audit_v6429_current_cpu_ring_miss_audio_checked'
MIX=original.capture.mix


def cue_gate(text,guest):
 physical=capture.original.physical
 phase=physical.miss.phase
 events=phase.overlap.rows(text,'EVENT');parent=next(r for r in events if r['kind']=='ring')
 child=phase.overlap.rows(text,'CHILD')[0];dead=phase.overlap.rows(text,'RETIRE')[0]
 begin=MIX.rows(text,'MK2_MAUDIO_BEGIN');routes=MIX.rows(text,'MK2_MAUDIO_ROUTE')
 need(len(begin)==1 and begin[0]['frame']==begin[0]['origin']==str(parent['frame'])=='1879' and begin[0]['id']=='18' and
      int(begin[0]['a8'],16)==parent['a8']==parent['main_owner'] and int(begin[0]['a13'],16)==parent['a13'],
      'One source audio origin at actual native true-Sonya missed-Ring owner')
 release=[r for r in routes if r['return_pc']=='FFFC48F0']
 need(len(release)==1 and release[0]['frame']=='1879' and release[0]['entry']=='FFA12530' and release[0]['a0']=='00000005' and
      release[0]['id']=='18' and int(release[0]['a8'],16)==int(release[0]['owner'],16)==parent['a8'] and
      int(release[0]['a13'],16)==parent['a13'] and release[0]['writes']=='0' and release[0]['assistance']=='none',
      'Exactly one real source release5, native Sonya18/physical Main, never proxy')
 offset=lambda at:(at-0xff800000)//8
 need(guest[offset(0xfffc48f0-96):offset(0xfffc48f0)]==struct.pack('<6H',0x09e0,5,0,0x0d5f,0x2530,0xffa1),
      'Whole authored release MOVI/CALLA literal')
 need(not[r for r in routes if r['return_pc']=='FF8B0010'],'Actual missed Ring has no impact62/63 dispatch')
 need(not[r for r in routes if r['return_pc']=='FF8DE600' and parent['frame']<=int(r['frame'])<=dead['frame']],
      'Miss child has no Ring-hit victim voice branch')
 need(not[r for r in routes if int(r['a8'],16)==child['a8'] and parent['frame']<=int(r['frame'])<=dead['frame']],
      'No hidden child-owned sound producer inside native missed-projectile lifetime')
 stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 # The qualified port changes one impact-align CALLA target, not the
 # original hit/miss audio producers. Bind that authored target exactly and
 # require every other byte of this complete original source window.
 native=bytearray(stock[offset(0xff8aff00):offset(0xff8b00c0)])
 at=offset(0xff8b00a0)-offset(0xff8aff00)
 need(struct.unpack_from('<I',native,at)[0]==0xff842010,'Actual original alignment CALLA target')
 struct.pack_into('<I',native,at,0xfffc2800)
 need(guest[offset(0xff8aff00):offset(0xff8b00c0)]==bytes(native),
      'Whole original projectile hit/miss source with only exact previously qualified native alignment target')
 compiled=ROOT/'diagnostic_v5219_current_payload_rom_metadata/input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
 need('constexpr unsigned impact_align = 0xf8500, impact_offset = 0xf8600;'in compiled.read_text() and
      'write32(rom_offset(0xff8b00a0), native_address(impact_align));'in compiled.read_text() and
      0xff800000+0xf8500*8==0xfffc2800,
      'Compiled source explicitly authors this one native alignment pointer')
 for lo,hi in((0xff8b69b0,0xff8b6ac0),(0xff8de000,0xff8de700),(0xffa12530,0xffa13ed0)):
  need(guest[offset(lo):offset(hi)]==stock[offset(lo):offset(hi)],'Whole original projectile hit/miss/voice/queue/packet source unchanged')
 female=bytes.fromhex('02b5f001420bfbff14ca420bfaff11ca80c00002ffff420bfeff08caa2b52000420bfeff01ca0125012d05c00126012d02c00127012d5f0de0ea80ff2014204010c0')
 need(guest[offset(0xffa12220):offset(0xffa12430)]==female,'Whole already-qualified native gender/Main-role/packed selector extension')
 physical_fields=phase.rounds.rows(text,'FIELD')
 by={(r['frame'],r['slot']):r for r in physical_fields}
 voices=[]
 for index,row in enumerate(routes):
  if row['entry']!='FFA12220':continue
  identity=int(row['id']);need(identity in(17,18),'Actual added-character voice identity, never Liu proxy')
  slot=1 if identity==17 else 2
  actual=by[int(row['frame']),slot]
  need(int(row['a8'],16)==int(row['owner'],16)==actual['actor'] and int(row['a13'],16)==actual['main'],
       'Every actual victim voice belongs to original physical actor/Main')
  chain=routes[index:index+4]
  selector='FFA122D0'if identity==17 else'FFA123B0'
  need([r['entry']for r in chain]==['FFA12220',selector,'FFA123D0','FFA12530'] and
       all(r['frame']==row['frame'] and r['return_pc']==row['return_pc'] and r['id']==row['id'] and
           r['a8']==r['owner']==row['a8'] and r['a13']==row['a13'] and r['writes']=='0' and r['assistance']=='none'for r in chain),
       'Complete actual native male/female voice dispatch chain')
  count=int(row['a0'],16);role=slot if identity==17 else 18
  base=(int(row['a1'],16)>>(24 if identity==17 else 0))&255
  need(chain[1]['a0']==row['a0'] and chain[1]['a1']==row['a1'] and int(chain[1]['a2'],16)==identity and
       int(chain[2]['a2'],16)==int(chain[3]['a2'],16)==role and
       int(chain[2]['a1'],16)==int(chain[3]['a1'],16)==base and base<=int(chain[3]['a0'],16)<base+count,
       'Every packed voice uses original male physical role or true native Sonya female byte, no name-only proxy')
  voices.append(dict(frame=int(row['frame']),identity=identity,role=role,base=base,count=count,caller=row['return_pc']))
 need(voices,'Positive actual native victim voice paths exercised inside full window')
 return dict(performerIdentity=18,victimIdentity=17,releaseCues=1,impactCues=0,ringHitVictimGrunts=0,
             actualParent=parent['a8'],actualChild=child['a8'],releaseFrame=1879,retirementFrame=dead['frame'],
             completeNativeVictimVoiceChains=voices)


def main(preflight=False):
 need(not OUT.exists() and not capture.original.prior.process_tools.census(),'Fresh independent proof; naturally terminal, no replay')
 report=json.loads((CASE/'report.json').read_text());waveform=json.loads((CASE/'waveform.json').read_text())
 terminal=json.loads((CASE/'native_terminal.json').read_text())
 need(report['passed'] and terminal['nativeExit']==0 and not terminal['hostDecodeErrors'] and report['samplesEnabled'] and
      report['sourceWinnerMixAccepted'] and report['nativeDCSWaveformAccepted'] and waveform['passed'] and
      waveform['differentChannelSamples']==0 and waveform['actualSHA256']==waveform['predictedSHA256'] and
      all(sha(p)==h for p,h in report['inputHashes'].items()),'Entire actual current native DAC/PCM/winner/whole ROM proof intact')
 with gzip.open(CASE/'run.log.gz','rt',encoding='utf-8')as file:text=file.read()
 guest=capture.original.prior.original.current.expected()
 physical=capture.original.state(text,'sonya',2,guest)
 headers=MIX.rows(text,'MK2_BBAUDIO_PCM_DIGEST')
 need(headers==report['pcmHeaders'] and MIX.rows(text,'MK2_NATIVE_DAC_RAM_DIGEST')==report['dacHeaders'],
      'All actual retained callback digests bind complete RAM source waveform')
 cue=cue_gate(text,guest);delivery=original.packet_gate(text);channels=original.channel_gate(text,waveform,headers)
 if preflight:
  print(json.dumps(dict(preflightPassed=True,stereoFrames=waveform['comparedStereoFrames'],cue=cue,delivery=delivery,channels=channels)),flush=True);return
 faults=[]
 def alter(tag,key,value,where):
  line=next(s for s in text.splitlines()if s.startswith(tag+' ')and where in s)
  bad,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
  need(n==1 and bad!=line,'Actual nonvacuous miss-audio field mutation');return text.replace(line,bad,1)
 for label,tag,key,value,where,gate in [
  ('wrong release command','MK2_MAUDIO_ROUTE','a0','00000006','return_pc=FFFC48F0',lambda t:cue_gate(t,guest)),
  ('proxy performer','MK2_MAUDIO_BEGIN','id','1','origin=1879',lambda t:cue_gate(t,guest)),
  ('child given release voice','MK2_MAUDIO_ROUTE','a8',format(cue['actualChild'],'08X'),'return_pc=FFFC48F0',lambda t:cue_gate(t,guest)),
  ('false miss impact caller','MK2_MAUDIO_ROUTE','return_pc','FF8B0010','return_pc=FFFC48F0',lambda t:cue_gate(t,guest)),
  ('wrong actual male voice selector','MK2_MAUDIO_ROUTE','a2','00000001','entry=FFA122D0',lambda t:cue_gate(t,guest)),
  ('wrong native full packet','MK2_MAUDIO_PACKET','a3','00010000','',original.packet_gate),
  ('missing actual port prefix','MK2_MAUDIO_SOUND','word','0000','pc=FFA13C90',original.packet_gate),
  ('wrong native DSP delivery','MK2_MAUDIO_DELIVERY','word','FFFF','',original.packet_gate),
  ('wrong winner identity','MK2_MAUDIO_SOUND','word','FFFE','pc=FFFB7140',original.packet_gate),
  ('wrong exact double position','MK2_TOMB_MIX_CHANNEL','bits','000000000000F03F','channel=0',lambda t:original.channel_gate(t,waveform,headers)),
  ('looped retired winner','MK2_TOMB_MIX_CHANNEL','loop','1','channel=0',lambda t:original.channel_gate(t,waveform,headers)),
 ]:
  try:gate(alter(tag,key,value,where))
  except(ValueError,KeyError,AssertionError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Actual missed-Ring audio fault accepted '+label)
 need(cue_gate(text,guest)==cue and original.packet_gate(text)==delivery and original.channel_gate(text,waveform,headers)==channels,
      'Entire original native audio positive restored after all actual faults')
 failed=capture.original.OUT
 failure=json.loads((failed/'native_terminal.json').read_text())
 need(failure['nativeExit']==3 and 'attempt to call a nil value'in(failed/'stderr.log').read_text(),'Actual original startup rejection remains distinct from accepted current run')
 need(not any(p.suffix.lower()in('.png','.wav','.bin','.exe','.zip')for p in CASE.rglob('*')if p.is_file()),
      'All native snapshots remain in RAM; no scratch image or raw media retained')
 pins=dict(report['inputHashes'])
 for p in(CASE/'report.json',CASE/'waveform.json',CASE/'run.log.gz',CASE/'native_terminal.json',Path(__file__),
          Path(original.__file__),failed/'native_terminal.json',failed/'failure.json',failed/'stderr.log',ROOT/'samples/mk2ks/kano_select.wav'):
  pins[str(p.resolve())]=sha(p)
 result=dict(passed=True,currentCPUMissedRingSourceAudioAccepted=True,nativeTerminal=terminal,wholeNativePhysicalPhase=physical,
  cueProvenance=cue,nativeDelivery=delivery,wholePreciseWinnerClockAndRetirement=channels,completeStereoFrames=waveform['comparedStereoFrames'],
  wholePCMSHA256=waveform['actualSHA256'],actualAudioFaultsRejected=faults,inputHashes=pins,remaining=report['remaining'],
  preservedFailedStartup=str(failed),newNativeBoots=0,newBuilds=0,newRawMedia=0,fullPortAcceptance=False,goalStatus='active')
 OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(result,indent=2)+'\n');h=sha(path)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==h,
      'Exact complete finite audio result losslessly compressed')
 print(json.dumps(dict(passed=True,stereoFrames=result['completeStereoFrames'],nativePackets=delivery['packets'],actualFaults=len(faults))),flush=True)


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');args=parser.parse_args();main(args.preflight)
