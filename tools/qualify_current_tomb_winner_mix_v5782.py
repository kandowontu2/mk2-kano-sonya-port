"""Whole current held Tomb controller plus passive exact winner clocks/gains."""
import ast,inspect,json,re
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import qualify_current_tomb_source_audio_v5752 as previous
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5783_current_tomb_winner_mix_source_checked'
EXTRA="-- Additional passive exact sample-clock/gain snapshots at actual sound callbacks.\nlocal mix_frame,mix_channels,mix_items,mix_serial=0,{},{},0\nlocal function mix_bind(tag)\n local device=assert(manager.machine.devices[tag])\n for name,index in pairs(device.items)do\n  local channel,field=name:match('^(%x+)/chan%.(.+)$')\n  if tag==':mk2ksvoices'and channel then\n   channel=tonumber(channel,16);mix_channels[channel]=mix_channels[channel]or{}\n   mix_channels[channel][field]=emu.item(index)\n  end\n  if name:match('/m_gain$')or name:match('/m_user_gain$')then\n   local item=emu.item(index);assert(item.size==4 and item.count==1)\n   mix_items[#mix_items+1]={device=tag,name=name,item=item}\n  end\n end\nend\nemu.register_frame(function()\n mix_frame=mix_frame+1\n if mix_frame==1 then\n  mix_bind(':mk2ksvoices');mix_bind(':mk2ksvoice')\n  for channel=0,13 do\n   local c=assert(mix_channels[channel])\n   assert(c.source_num and c.source_len and c.pos and c.loop and c.paused)\n  end\n  table.sort(mix_items,function(a,b)return a.device..a.name<b.device..b.name end)\n  for i,entry in ipairs(mix_items)do\n   print(string.format('MK2_TOMB_MIX_ITEM frame=%d index=%d device=%s name=%s bytes=4 count=1 writes=0 assistance=none',\n    mix_frame,i,entry.device,entry.name))\n  end\n end\nend)\nemu.register_sound_update(function()\n if not active()then return end\n mix_serial=mix_serial+1\n for channel=0,13 do\n  local c=mix_channels[channel]\n  local raw=c.pos:read_block(0,8);assert(#raw==8)\n  print(string.format('MK2_TOMB_MIX_CHANNEL frame=%d seconds=%.12f index=%d channel=%d sample=%d length=%d position=%.17g bits=%s loop=%d paused=%d writes=0 assistance=none',\n   mix_frame,emu.time(),mix_serial,channel,c.source_num:read(0),c.source_len:read(0),string.unpack('<d',raw),\n   raw:gsub('.',function(value)return string.format('%02X',value:byte())end),c.loop:read(0),c.paused:read(0)))\n end\n for i,entry in ipairs(mix_items)do\n  print(string.format('MK2_TOMB_MIX_GAIN frame=%d seconds=%.12f index=%d item=%d bits=%08X writes=0 assistance=none',\n   mix_frame,emu.time(),mix_serial,i,entry.item:read(0)))\n end\nend)\n"


def run():
 current.expected();previous.observer_source()
 parentpath=ROOT/'audit_v5777_current_tomb_native_audio_progress/progress.json'
 parent=json.loads(parentpath.read_text())
 need(parent['passed']and parent['actualCurrentBothSlotsHeldAndPressedNativeTombSoundAccepted']and
  parent['goalStatus']=='active'and len(parent['remaining'])==5,'Whole current held/pressed/ending proofs and original full goal retained')
 pins=dict(parent['newInputHashes']);pins[str(parentpath)]=sha(parentpath)
 need(all(sha(p)==h for p,h in pins.items()),'All authoritative whole current/physical/native/model evidence intact')
 import run_current_tomb_winner_mix_v5781 as host
 import run_current_tomb_source_audio_v5749 as oldhost
 observer=(ROOT/host.OBSERVER).read_text()
 need(observer==(ROOT/previous.OBSERVER).read_text().rstrip()+'\n'+EXTRA,
  'Entire original15tap/PCM/14videochannel/nativeDAC/wholeROM observer retained plus read-only precise callback item snapshots')
 need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|set_value|clear_value|load_?state|io\.open|dofile\(|\bload\(|snapshot\(|machine:exit|return\s+data|force_update|flush\(',observer),
  'Every added sample/gain observation passive; no actor/health/IDs/RNG/input/cursor/audio writes or flush')
 campaign=previous.CAMPAIGN.replace('-- Original true-ID earned matches and facing commands; passive audio only.',
  '-- Whole original earned held Tomb campaign; passive full enabled audio.').replace(previous.OBSERVER,host.OBSERVER)
 need((ROOT/host.LUA).read_text()==campaign,'Whole genuine two-earned-match controller/window/deadline, only passive observer target')
 fn,digest=host.collector();oldfn,_=oldhost.collector()
 need(fn.source==oldfn.source.replace('audit_v5754_current_tomb_source_audio_','audit_v5784_current_tomb_winner_mix_').replace(
  oldhost.LUA,host.LUA)and fn.__globals__['NAME']==current.NAME and fn.__globals__['model']is host.model and
  fn.__globals__['source'].__file__==__file__ and fn.__globals__['OBSERVER']==host.OBSERVER,
  'Whole canonical bounded cold RAM/gzip capture unchanged except output and observer target; enable original samples parameter at callsite')
 need("fn(fighter,side,True,guest)"in Path(host.__file__).read_text(),'Actual enabled native+winner game capture, not disabled samples mislabeled')
 float_fn=host.model.float_model()
 code=inspect.getsource(host.model.native.predict_waveform)
 code=code.replace('def predict_waveform(chunks,headers,pcm):','def native_float(chunks,headers):',1).replace(
  'def convert(value):return int(max(-1.0,min(1.0,float(value)))*32767.0)',
  'def convert(value):return np.float32(value)',1)
 code=code[:code.index("    guessed=np.asarray(predicted,dtype='<i2')")]+ "    return np.asarray(predicted,dtype='<f4'),clocks\n"
 need(float_fn.source==code,'Entire qualified native resampler/cache/source-clock loop retained unquantized, only final output delayed until speaker sum')
 compiled=ROOT/current.NAME/'input_sources/mame-mkp/src/mame/midway'
 config=(compiled/'midtunit.cpp').read_text();dispatch=(compiled/'midtunit_m.cpp').read_text()
 need('m_mk2ks_voices->set_channels(14);'in config and
  'm_mk2ks_voices->add_route(ALL_OUTPUTS, "mk2ksvoice", 0.70);'in config and
  'm_mk2ks_voices->set_volume(0, 0.30f);'in dispatch and
  'unsigned const sample = (data == 0xfffc) ? 0 : (data == 0xfffb) ? 1 : (data == 0xfffe) ? 2 : 3;'in dispatch,
  'Exact compiled separate center speaker/14channels/.70route/.30output and winner2/3 dispatch')
 samples=ROOT/'mame-mkp/src/devices/sound/samples.cpp';text=samples.read_text()
 for fragment in ('chan.stream->update();','chan.pos = 0;','chan.curfreq = sample.frequency;',
  'sample[(ipos + 1) % chan.source_len]','chan.pos += step;','buffer.fill(0, sampindex);','SAMPLE_RATE_OUTPUT_ADAPTIVE'):
  need(fragment in text,'Original authoritative sample start/clock/interpolation/terminal operation '+fragment)
 for fighter in ('kano','sonya'):host.model.read_winner(fighter,pins)
 for p in (Path(__file__),Path(host.__file__),Path(host.model.__file__),ROOT/host.LUA,ROOT/host.OBSERVER,
  compiled/'midtunit.cpp',compiled/'midtunit_m.cpp',samples,
  ROOT/'mame-mkp/src/emu/sound.cpp',ROOT/'mame-mkp/src/emu/sound.h',
  ROOT/'mame-mkp/src/emu/disound.cpp',ROOT/'mame-mkp/src/emu/speaker.cpp'):
  if p.suffix=='.py':ast.parse(p.read_text())
  pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All original/current complete source inputs stable before enabled boot')
 return dict(passed=True,sourceOnly=True,inputHashes=pins,transportSourceSHA256=digest,
  wholeNativeFloatCarrierSHA256=__import__('hashlib').sha256(float_fn.source.encode()).hexdigest().upper(),
  actualEnabledTombWinnerWaveformAccepted=False,completeStageVictimAudioAccepted=False,fullPortAcceptance=False,
  newBuilds=0,rawMediaWritten=0)


if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable full enabled winner source preflight')
 report=run();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
