"""Whole guest, exact host source, real emitted helper words and C++ pool.

All probes are explicitly synthetic source qualification, not gameplay/PCM.
Original captured five-slot chronology supplies all39record and301timer cases.
Six assets are real full native48k source recordings, not fitted replacements.
"""
import gzip
import hashlib
import inspect
import json
import struct
import subprocess
import traceback
from pathlib import Path
import qualify_native_kano_laser_burst as prior
import review_native_kano_laser_original_audio_timer_path as audio

ROOT=prior.ROOT
STAGE=ROOT/'source_native_kano_laser_audio'
OUT=ROOT/'audit_native_kano_laser_audio_source'
need,sha,address=prior.need,prior.sha,prior.address
Assembly=prior.Assembly


def exact_sources():
    old={f:(prior.STAGE/f).read_text() for f in ('midtunit.cpp','midtunit.h','midtunit_m.cpp')}
    new={f:(STAGE/f).read_text() for f in old}
    header=new['midtunit.h'];first=header.index('\n\t// Original laser voices have a separate five-slot pool.')
    last=header.index('\n\n\t/* protection */',first)
    need(header[:first]+header[last:]==old['midtunit.h'],'Only new audio member/declaration block in whole header')
    config=new['midtunit.cpp']
    before='"sonya_square_launch", "sonya_bicycle_launch", "sonya_bicycle_cry", "kano_ball_launch", nullptr'
    after='"sonya_square_launch", "sonya_bicycle_launch", "sonya_bicycle_cry", "kano_ball_launch",\n\t"kano_laser_charge", "kano_laser_beam", "sonya_laser_scream", "kano_laser_scream",\n\t"kano_laser_burst_a", "kano_laser_burst_b", nullptr'
    config=config.replace(after,before).replace('set_channels(19)','set_channels(14)')
    callback='\n\tsubdevice<screen_device>("screen")->screen_vblank().set(FUNC(midtunit_state::mk2ks_finish_audio_frame));'
    need(config.count(callback)==1,'Only mk2ks owns new source audio frame callback');config=config.replace(callback,'')
    need(config==old['midtunit.cpp'],'Whole config conserves all old sample indices/routes/drivers; adds six names and five channels only')
    source=new['midtunit_m.cpp'];normalized=source
    first=source.index('void midtunit_state::mk2ks_finish_audio_stop(')
    last=source.index('void midtunit_state::mk2ks_battle_audio_stop(',first)
    host=source[first:last];normalized=normalized[:first]+normalized[last:]
    first=normalized.index('\n\t// Typed full-word markers are emitted only by these non-yielding helpers.')
    last=normalized.index('\n\t// KANO_LASER_BURST_END',first)
    helper=normalized[first:last];normalized=normalized[:first]+normalized[last:]
    constants='\n\tconstexpr unsigned kano_laser_audio_charge=0xb0e00, kano_laser_audio_beam=0xb0e20;\n\tconstexpr unsigned kano_laser_audio_victim=0xb0e40;\n\tconstexpr unsigned kano_laser_audio_burst_a=0xb0ea0, kano_laser_audio_burst_b=0xb0ec0;'
    saves=''.join('\n\tsave_item(NAME(m_mk2ks_finish_audio_'+field+'));' for field in ('actor','main','slot','priority','remaining'))
    dispatch='\n\t\t\t\tif (m_mk2ks_voices && !native_packet && data>=0x6b40 && data<=0x6b44)\n\t\t\t\t{\n\t\t\t\t\tmk2ks_finish_audio_marker(data);\n\t\t\t\t\tm_fake_sound_state=128;break;\n\t\t\t\t}'
    edits=[constants,saves,dispatch,'\n\tmk2ks_finish_audio_stop("reset");',
        '\n\tleg_call(native_address(kano_laser_audio_victim));',
        '\n\tleg_call(native_address(kano_laser_audio_charge));',
        '\n\tleg_call(native_address(kano_laser_audio_beam));',
        '\n\tleg_call(native_address(kano_laser_audio_burst_a));\n\tleg_call(native_address(kano_laser_audio_burst_b));']
    for addition in edits:
        need(normalized.count(addition)==1,'One exact new audio source insertion only')
        normalized=normalized.replace(addition,'')
    need(normalized==old['midtunit_m.cpp'],'Every old host/guest byte outside exact new audio functions/calls preserved')
    return new,host,helper,constants


def expected_guest(previous):
    expected=bytearray(previous)
    expected[0xb0900:0xb0c80]=b'\xff'*0x380
    text=inspect.getsource(prior.initial.contract)
    first=text.index('    a=Assembly(expected,0xb0900,0xb0b00)')
    last=text.index('    a=Assembly(expected,0xb0b00,0xb0c80)',first)
    victim=text[first:last]
    victim=victim.replace('a=Assembly(expected,0xb0900,0xb0b00)',
                         'a=Assembly(expected,0xb0900,0xb0b00);a.call(address(0xb0e40))')
    exec(compile('def emit_victim():\n'+victim+'    return expected\n',__file__+'::independent_victim_assembly','exec'),
         scope:=dict(vars(prior.initial),expected=expected))
    scope['emit_victim']()
    a=Assembly(expected,0xb0b00,0xb0c80)
    a.mov(1,1);a.mov(0,1);a.call(0xff8cd780);a.mov(0,20);a.call(0xff80dcc0);a.call(address(0xb0e00))
    a.cooperate(address(0xafa00));a.call(address(0xb0e20));a.mov(7,address(0xb0900));a.call(0xff842710)
    a.cooperate(address(0xafa40));a.code(0xa30f,0xb7a8,0x140,0x4d00);a.call(0xff838f60)
    a.call(address(0xb0ea0));a.call(address(0xb0ec0));a.call(address(0xb0d00));a.call(address(0xb0140));a.code(0x09af,0x100)
    a.code(0xb7a0,0x170);a.mov(7,0xff841ec0);a.call(0xff83f930)
    a.cooperate(address(0xafa80));a.call(address(0xaf290));a.call(0xff8cdc40);a.jump(0xffa14860)
    need(all(b==255 for b in previous[0xb0e00:0xb0ee0]),'Unused private audio helper allocation')
    for at,marker in ((0xb0e00,0x6b40),(0xb0e20,0x6b41),(0xb0ea0,0x6b43),(0xb0ec0,0x6b44)):
        a=Assembly(expected,at,at+32);a.code(0xa20f);a.mov(0,marker);a.code(0x0580,0x1030,0x1d0,0x97e0,0x0960)
    a=Assembly(expected,0xb0e40,0xb0ea0)
    a.code(0x098f,0xfe00,0xb500,0x1f0,0x0b40,0xffee)
    kano=a.at+2;a.jump(0,0xca80);a.code(0x0b40,0xffed);sonya=a.at+2;a.jump(0,0xca80)
    a.call(0xffa11fd0);stock=a.at+2;a.jump(0)
    struct.pack_into('<I',expected,kano,address(a.at));struct.pack_into('<I',expected,sonya,address(a.at))
    a.mov(0,0x6b42);a.code(0x0580,0x1030,0x1d0);struct.pack_into('<I',expected,stock,address(a.at))
    a.code(0x09af,0x007f,0x0960)
    return bytes(expected)


def controls(guest):
    class AudioControl(prior.initial.Control):
        def call(self,target):
            helpers={address(0xb0e00):20,address(0xb0e20):68,address(0xb0ea0):164,address(0xb0ec0):164,address(0xb0e40):68}
            if target in helpers:
                need(self.age==helpers[target],'No added sleep or moved logical audio cue')
                if target==address(0xb0e40):need(self.r[8]==self.victim and self.r[13]==self.vm,'True native victim audio context')
                elif target in (address(0xb0e00),address(0xb0e20)):need(self.r[8]==self.performer and self.r[13]==self.main,'True Kano own audio context')
                else:need(self.r[8]==self.victim and self.r[13]==self.main,'Burst sound belongs to current true victim, not own pose')
                return
            if target==address(0xb0d00):
                need(self.age==164 and self.r[8]==self.victim,'Existing true-victim burst retained')
                self.events.append((164,'burst'));self.poison();return
            return super().call(target)
    code=inspect.getsource(prior.initial.units)
    old="(164,'hide'),(164,'bones',32)";need(code.count(old)==1,'Exact previous full38controlcases')
    code=code.replace(old,"(164,'hide'),(164,'burst'),(164,'bones',32)")
    scope=dict(vars(prior.initial),Control=AudioControl);exec(compile(code,__file__+'::all_emitted_control_units','exec'),scope)
    return scope['units'](guest)


def helpers(guest):
    _,model=prior.auxiliary_model();scope,_,_=prior.prior.corrected_units()
    model=model.replace('class AuxiliaryWords:','class AudioWords:')
    old='elif op==0xa20f:self.push(15,r[0])'
    new='elif op==0x97e0:r[0]=self.pop(15)\n            elif op==0x0b40:\n                immediate=(~self.operand(16))&0xffff\n                self.zero=r[0]==immediate\n            '+old
    need(model.count(old)==1,'Exact actual audio word extensions');model=model.replace(old,new)
    exec(compile(model,__file__+'::actual_non_yielding_marker_words','exec'),scope)
    class CPU(scope['AudioWords']):
        def __init__(self,*args,**kw):super().__init__(*args,**kw);self.ports=[];self.stock=[]
        def store(self,at,value,width):
            if at==0x01d01030:self.ports.append(dict(pc=self.pc,value=value&65535,width=width));return
            return super().store(at,value,width)
        def external(self,target):
            need(target==0xffa11fd0,'Only original native stock-victim voice helper')
            ident=self.load(self.regs[8]+0x1f0,16);need(ident<17,'Stock victims never route through imported scream')
            self.stock.append(ident);self.poison()
    cases=[]
    for ident in range(19):
        for offset,marker in ((0xb0e00,0x6b40),(0xb0e20,0x6b41),(0xb0e40,0x6b42),(0xb0ea0,0x6b43),(0xb0ec0,0x6b44)):
            cpu=CPU(guest,offset);cpu.store(cpu.regs[8]+0x1f0,ident,16)
            saved=cpu.regs.copy();before=dict(cpu.mem);cpu.execute()
            need(cpu.done and cpu.regs==saved and cpu.age==0 and
                 all(cpu.mem[at]==v for at,v in before.items() if at<cpu.base_sp-256),
                 'All emitted audio helpers preserve every caller register, stacks, age and real actor fields')
            imported=offset!=0xb0e40 or ident>=17
            need(cpu.stock==([] if imported else [ident]) and cpu.ports==([dict(pc=address(offset)+(52 if offset==0xb0e40 else 14)*8,value=marker,width=16)] if imported else []),
                 'Exact actual port instruction PC/WORD marker, true stock voice branch, no fabricated native packet')
            cases.append(dict(victimID=ident,helper=f'{address(offset):08X}',portWrites=cpu.ports,stockVoice=cpu.stock))
    return cases,model


HOST_PREFIX=r'''
#include <cstdint>
#include <iostream>
#include <vector>
#include <unordered_map>
constexpr int AS_PROGRAM=0,TMS34010_A8=8,TMS34010_A13=13;
template<class... T> void logerror(const char*,T...){ }
struct Space {
 std::unordered_map<uint32_t,uint16_t> words;
 uint16_t read_word(uint32_t at){return words[at];}
 void set32(uint32_t at,uint32_t value){words[at]=value;words[at+16]=value>>16;}
};
struct CPU {Space memory;uint32_t nextpc=0,r8=0,r13=0;
 Space& space(int){return memory;}uint32_t pc(){return nextpc;}
 uint32_t state_int(int r){return r==8?r8:r13;}
};
struct Samples {std::vector<int> events;bool active[19]={};
 void start(unsigned channel,unsigned sample,bool){events.push_back(channel*1000+sample);active[channel]=true;}
 void stop(unsigned channel){active[channel]=false;}
};
struct Clock {double as_double(){return 0;}};
struct Machine {Clock time(){return {};}};
class midtunit_state {
public:
 CPU cpu;CPU* m_maincpu=&cpu;Samples samples;Samples* m_mk2ks_voices=&samples;
 uint32_t m_mk2ks_finish_audio_actor=0,m_mk2ks_finish_audio_main=0;
 uint16_t m_mk2ks_finish_audio_slot=0,m_mk2ks_finish_audio_priority[5]={},m_mk2ks_finish_audio_remaining[5]={};
 Machine machine(){return {};}
 void mk2ks_finish_audio_stop(const char*);void mk2ks_finish_audio_frame(int);
 void mk2ks_finish_audio_marker(uint16_t);int mk2ks_finish_audio_start(unsigned,uint16_t,uint16_t);
};
'''


HOST_MAIN=r'''
int main(){
 midtunit_state s;auto &mem=s.cpu.memory;
 const uint32_t a=0x01035000,b=0x01036000,m=0x01070000,v=0x01071000;
 auto setup=[&](unsigned side,unsigned victim){
  s.mk2ks_finish_audio_stop("fixture");mem.words.clear();
  const uint32_t actors[]={0x01060220,0x01060df0},mains[]={0x01060260,0x01060e30},ids[]={0x01060280,0x01060e50},hp[]={0x010602f0,0x01060ec0};
  mem.set32(actors[side],a);mem.set32(actors[1-side],b);mem.set32(mains[side],m);mem.set32(mains[1-side],v);
  mem.set32(m+0xc0,a);mem.set32(v+0xc0,b);mem.words[a+0x1f0]=17;mem.words[b+0x1f0]=victim;
  mem.words[ids[side]]=17;mem.words[ids[1-side]]=victim;mem.words[hp[side]]=161;mem.words[hp[1-side]]=0;mem.words[0x010601d0]=2;
 };
 setup(0,18);s.m_mk2ks_finish_audio_actor=a;s.m_mk2ks_finish_audio_main=m;
 char command;unsigned x,y,z;int selected=-2;
 while(std::cin>>command){
  selected=-2;
  if(command=='S'){std::cin>>x>>y>>z;selected=s.mk2ks_finish_audio_start(x,y,z);}
  else if(command=='T')s.mk2ks_finish_audio_frame(1);
  else if(command=='F'){std::cin>>x>>y;setup(x,y);}
  else if(command=='M'){
   std::cin>>x>>y;unsigned cue=x;const unsigned offsets[]={0xb0e00,0xb0e20,0xb0e40,0xb0ea0,0xb0ec0};
   s.cpu.nextpc=0xff800000U+offsets[cue]*8+(cue==2?52*8:14*8)+y;
   s.cpu.r8=cue<2?a:b;s.cpu.r13=cue==2?v:m;s.mk2ks_finish_audio_marker(0x6b40+cue);
  }
  else if(command=='D'){std::cin>>x;mem.words[0x010601d0]=x;s.mk2ks_finish_audio_frame(1);}
  else if(command=='B'){std::cin>>x>>y;mem.words[x]=y;}
  else if(command=='R'){std::cin>>x;s.mk2ks_finish_audio_marker(x);}
  else return 2;
  std::cout<<selected<<' '<<s.m_mk2ks_finish_audio_actor<<' '<<s.samples.events.size();
  for(unsigned i=0;i<5;i++)std::cout<<' '<<s.m_mk2ks_finish_audio_priority[i]<<' '<<s.m_mk2ks_finish_audio_remaining[i];
  std::cout<<'\n';
 }
}
'''


def host_units(host):
    code=HOST_PREFIX+host+HOST_MAIN;probe=OUT/'audio_pool_probe.exe'
    compile=subprocess.run([r'C:\Strawberry\c\bin\g++.exe','-std=c++17','-O1','-Wall','-Wextra','-Werror','-x','c++','-','-o',str(probe)],input=code,text=True,capture_output=True)
    (OUT/'audio_pool_compiler.log').write_text(compile.stdout+compile.stderr)
    need(compile.returncode==0,'Actual new four C++ host audio functions compile warning-free in explicit synthetic platform fixture')
    text=gzip.open(audio.prior.FOLDER/'run.log.gz','rt').read();commands=[];expected=[];state=[(0,0,0)]*5;events=0;records=0
    for row in audio.prior.rows(text,'AUDIO_CODE'):
        if row['at']=='FFAA6E00':
            record=int(row['record'],16);choice=audio.prior.choose(record,int(row['flag']),state)
            need(choice is not None,'Earned39record chronological fixture contains only admitted records')
            slot,priority,duration,command=choice;state[slot]=(priority,duration,0);records+=1;events+=1
            commands.append(f'S {records} {priority} {duration}');expected.append([-0 if slot==0 else slot,0x01035000,events,*[x for p,t,c in state for x in (p,t)]])
        elif row['at']=='FFAA80D0':
            next_state=list(state)
            for i,(p,t,c) in enumerate(state):
                next_state[i]=(0 if t==1 else p,max(0,t-1),0)
                if i==3 and t>1:break
            state=next_state;commands.append('T');expected.append([-2,0x01035000,events,*[x for p,t,c in state for x in (p,t)]])
    cases=[]
    for side in (0,1):
        for victim in (17,18):
            commands.append(f'F {side} {victim}');expected.append([-2,0,events,*([0]*10)])
            # Only fixture memory is assigned. No live emulator is attached.
            for cue in range(5):
                commands.append(f'M {cue} 0');events+=1
                priorities=[0x50,0x50,0x41 if victim==17 else 0x42,0,0]
                times=[56,76,193 if victim==17 else 203,0,0]
                if cue==0:priorities=[0x50,0,0,0,0];times=[56,0,0,0,0]
                elif cue==1:priorities=[0x50,0x50,0,0,0];times=[56,76,0,0,0]
                elif cue==3:priorities=[0x50,0x50,0x41 if victim==17 else 0x42,0x50,0];times=[56,76,193 if victim==17 else 203,102,0]
                elif cue==4:priorities=[0x50,0x50,0x41 if victim==17 else 0x42,0x50,0x50];times=[56,76,193 if victim==17 else 203,102,99]
                expected.append([-2,0x01035000,events,*[x for p,t in zip(priorities,times) for x in (p,t)]])
            # Same true owner survives native winner mode5; mode3 clears all.
            commands+=['D 5','D 3']
            for actor in (0x01035000,0):
                if actor:
                    times=[max(0,t-1) if i<4 else t for i,t in enumerate(times)]
                    expected.append([-2,actor,events,*[x for p,t in zip(priorities,times) for x in (p,t)]])
                else:expected.append([-2,0,events,*([0]*10)])
            # Wrong actual instruction PC must not start any sample/context.
            commands += [f'F {side} {victim}','M 0 16','R 0','R 65535']
            expected += [[-2,0,events,*([0]*10)]]*4
            cases.append(dict(side=side+1,trueVictimID=victim,markers=5,winnerModeSurvives=True,sceneModeClears=True,wrongPCRejected=True))
    run=subprocess.run([str(probe)],input='\n'.join(commands)+'\n',text=True,capture_output=True)
    actual=[list(map(int,line.split())) for line in run.stdout.splitlines()]
    need(run.returncode==0 and not run.stderr and actual==expected,
         'Whole actual C++ output for original39record/301timer replay plus both-slot typed-marker/winner/scene/rejection fixtures')
    probe.unlink();return dict(originalRecordOperations=39,originalTimerOperations=301,totalOperations=len(commands),typedOwnerCases=cases),code


def main():
    need(not OUT.exists(),'Fresh immutable audio source qualification');OUT.mkdir();harness=''
    try:
        parent=json.loads((prior.OUT/'report.json').read_text());assets_path=ROOT/'audit_native_kano_laser_original_samples/asset_report.json';assets=json.loads(assets_path.read_text())
        need(parent['passed'] and assets['passed'] and assets['hardwareOnlyNotGameplayAcceptance'] and not assets['portAudioAccepted'] and
             all(sha(p)==h for r in (parent,assets) for p,h in r['inputHashes'].items()),'Actual prior guest/source and all31source hardware jobs/sixfull assets conserved')
        source,host,helper,constants=exact_sources()
        harness=json.loads(gzip.open(prior.OUT/'executed_sources.json.gz','rt').read())['actualNewInitializerHarness']
        scope=dict(vars(prior.initial.gate.prior.phases),OUT=OUT/'previous');scope['OUT'].mkdir()
        exec(inspect.getsource(prior.initial.gate.prior.phases.compile_probe),scope)
        base,payload=prior.prior.capture.providers();previous,old_probe=scope['compile_probe'](harness,base,payload)
        need(hashlib.sha256(previous).hexdigest().upper()==parent['proposedGuestSHA256'],'Whole previous actual compiled initializer exactly conserved')
        edits=[('\tconstexpr unsigned kano_laser_burst_create=0xb0d00;', '\tconstexpr unsigned kano_laser_burst_create=0xb0d00;'+constants),
            ('\tleg_cursor=kano_laser_victim_action;leg_limit=kano_laser_action;', '\tleg_cursor=kano_laser_victim_action;leg_limit=kano_laser_action;\n\tleg_call(native_address(kano_laser_audio_victim));'),
            ('\tleg_movi(0,20);leg_call(0xff80dcc0);','\tleg_movi(0,20);leg_call(0xff80dcc0);\n\tleg_call(native_address(kano_laser_audio_charge));'),
            ('\tleg_cooperate(native_address(kano_laser_phase_entries[0]));','\tleg_cooperate(native_address(kano_laser_phase_entries[0]));\n\tleg_call(native_address(kano_laser_audio_beam));'),
            ('\tleg_code({0xa30f,0xb7a8,0x0140,0x4d00});leg_call(0xff838f60);','\tleg_code({0xa30f,0xb7a8,0x0140,0x4d00});leg_call(0xff838f60);\n\tleg_call(native_address(kano_laser_audio_burst_a));\n\tleg_call(native_address(kano_laser_audio_burst_b));'),
            ('\t// KANO_LASER_BURST_END',helper+'\n\t// KANO_LASER_BURST_END')]
        for old,new in edits:
            need(harness.count(old)==1,'Exact actual initializer audio insertion');harness=harness.replace(old,new)
        scope['OUT']=OUT;guest,probe=scope['compile_probe'](harness,base,payload)
        expected=expected_guest(previous);need(guest==expected,'Whole1MiB guest only exact five calls and five helpers; all other mechanics/IDs/bindings/graphics preserved')
        control=controls(guest);marker_units,model=helpers(guest);pool,host_probe=host_units(host)
        auxiliary,_=prior.auxiliary_units(guest)
        faults=[]
        for name,at in (('charge_call',0xb0b20),('victim_call',0xb0900),('charge_marker',0xb0e04),('stock_voice',0xb0e5e),
            ('marker_port_address',0xb0e0a),('victim_id_branch',0xb0e4a),('burst_marker',0xb0ea4),('unrelated_guest',0x12340)):
            bad=bytearray(guest);bad[at]^=1
            try:need(bytes(bad)==expected,'Whole exact independently emitted audio guest')
            except ValueError as error:faults.append(dict(name=name,rejected=str(error)))
            else:raise ValueError('Audio guest fault admitted '+name)
        paths=[Path(__file__),Path(prior.__file__),prior.OUT/'report.json',prior.OUT/'executed_sources.json.gz',audio.OUT/'report.json',assets_path,
            ROOT/'mk2/mk2-maincpu.bin',ROOT/'PLAY_LATEST_KANO_SONYA.cmd',*(STAGE/f for f in source)]
        report=dict(passed=True,sourceOnlyAccepted=True,nativeRuntimeAccepted=False,portAudioAccepted=False,fullPortAcceptance=False,
            proposedGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),initializedGuestByteDelta=sum(a!=b for a,b in zip(guest,previous)),
            controlUnitCases=control,markerWordUnitCases=marker_units,hostAudioUnitCases=pool,auxiliaryWordUnitCases=auxiliary,negativeFaultsRejected=faults,
            registeredSampleIndices={a['name']:17+i for i,a in enumerate(assets['assets'])},totalSampleChannels=19,old14ChannelsConserved=True,
            stagedSourceHashes={f:sha(STAGE/f) for f in source},audioAssets=assets['assets'],
            originalNaturalIntegrationRequirements=parent['originalNaturalIntegrationRequirements'],originalRemainingWorkGroups=parent['originalRemainingWorkGroups'],
            goalStatus='active',previousGoalTurnClassification='progress',inputHashes={str(p.resolve()):sha(p) for p in paths},
            newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,latestPlayableChanged=False,
            limitations=['Synthetic whole initializer/helper/host units only; no new MAME build/gameplay/PCM acceptance.',
                'Original core sound allocator semantics preserved in separate five sample voices; native bone impact DCS and native announcements remain unchanged, not simulated as imported MK3 commands.',
                'Stock victims use actual native FFA11FD0 dispatcher; true Kano/Sonya use original recordings. Earned all-victim/mirror/CPU/ownership/fullmix/scene tests required.',
                'Actual screen-vblank phase versus source timer entry must be tested in native game; source frame fixtures are not evidence about callback ordering.',
                'All original14requirements and6remaining groups remain; public CMD and ZIP unchanged.'])
        need(len(report['originalNaturalIntegrationRequirements'])==14 and len(report['originalRemainingWorkGroups'])==6,'Full natural-integration scope retained')
        with gzip.open(OUT/'executed_sources.json.gz','wt')as file:json.dump(dict(actualNewInitializerHarness=harness,actualMarkerWordModel=model,actualHostProbe=host_probe,actualHostSource=host),file)
        old_probe.unlink();probe.unlink()
        (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(dict(passed=True,sourceOnly=True,guest=report['proposedGuestSHA256'],controls=len(control),actualMarkerUnits=len(marker_units),hostOperations=pool['totalOperations'])))
    except Exception:
        (OUT/'failure.txt').write_text(traceback.format_exc())
        with gzip.open(OUT/'failed_executed_sources.json.gz','wt')as file:json.dump(dict(actualInitializerHarness=harness),file)
        raise


if __name__=='__main__':main()
