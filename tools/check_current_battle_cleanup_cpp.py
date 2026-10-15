"""Execute exact current battle cleanup functions; not runtime/audio acceptance."""
import json
import subprocess
import verify_native_source_sync as sync

sync.verify()
path = sync.ROOT / 'mame-mkp/src/mame/midway/midtunit_m.cpp'
source = path.read_text()
functions = source[source.index('void midtunit_state::mk2ks_battle_audio_stop('):source.index('\nuint16_t midtunit_state::midtunit_sound_state_r()')]
out = sync.ROOT / 'audit_current_battle_cleanup_cpp'
assert not out.exists()
out.mkdir()
prefix = r'''
#include <cstdint>
#include <cassert>
#include <map>
#include <vector>
#include <iostream>
#define AS_PROGRAM 0
#define logerror(...) ((void)0)
#define TIMER_CALLBACK_MEMBER(name) void name()
struct attotime {static constexpr int never=-1;};
struct timer {int calls=0;void adjust(int v){assert(v==-1);calls++;}};
struct mem {std::map<uint32_t,uint16_t> words;
 uint16_t read_word(uint32_t a){return words[a];}
 void set32(uint32_t a,uint32_t v){words[a]=v;words[a+16]=v>>16;}};
struct cpu {mem memory;mem &space(int){return memory;}};
struct voices {bool active[19]={};std::vector<unsigned> stopped;
 void stop(unsigned c){stopped.push_back(c);active[c]=false;}
 bool playing(unsigned c){return active[c];}};
struct midtunit_state {cpu processor;cpu *m_maincpu=&processor;
 voices device;voices *m_mk2ks_voices=&device;timer clock;
 timer *m_mk2ks_battle_audio_timer=&clock;
 uint32_t m_mk2ks_battle_actor[2]={},m_mk2ks_battle_main[2]={};
 uint16_t m_mk2ks_battle_health[2]={},m_mk2ks_battle_id[2]={},m_mk2ks_battle_mode[2]={};
 void mk2ks_battle_audio_stop(unsigned,const char*);void mk2ks_battle_audio_tick();
 void setup(unsigned slot,unsigned mode){auto &m=processor.memory;
 uint32_t a=0x01030000+slot*0x1000,b=0x01040000+slot*0x1000;
 m_mk2ks_battle_actor[slot]=a;m_mk2ks_battle_main[slot]=b;
 m_mk2ks_battle_health[slot]=161;m_mk2ks_battle_id[slot]=17+slot;
 m_mk2ks_battle_mode[slot]=mode;m.words[0x010601d0]=mode;
 m.set32(slot?0x01060df0:0x01060220,a);m.set32(slot?0x01060e30:0x01060260,b);
 m.set32(b+0xc0,a);m.words[a+0x1f0]=17+slot;
 m.words[slot?0x01060ec0:0x010602f0]=161;device.active[10+2*slot]=true;}
};
'''
tests = r'''
void cleared(midtunit_state &s,unsigned slot){
 assert(s.device.stopped==std::vector<unsigned>({10+2*slot,11+2*slot}));
 assert(!s.m_mk2ks_battle_actor[slot] && !s.m_mk2ks_battle_main[slot]);
 assert(!s.m_mk2ks_battle_health[slot] && !s.m_mk2ks_battle_id[slot] && !s.m_mk2ks_battle_mode[slot]);
 assert(s.clock.calls==1);}
int main(){int cases=0;
 for(unsigned slot=0;slot<2;slot++)for(unsigned mode=0;mode<10;mode++){
 midtunit_state s;s.setup(slot,mode);s.mk2ks_battle_audio_tick();
 if(mode==1 || mode==2){assert(s.device.stopped.empty());assert(s.clock.calls==0);}
 else cleared(s,slot);cases++;}
 for(unsigned slot=0;slot<2;slot++)for(int change=0;change<8;change++){
 midtunit_state s;s.setup(slot,2);auto &m=s.processor.memory;
 auto a=s.m_mk2ks_battle_actor[slot],b=s.m_mk2ks_battle_main[slot];
 if(change==0)m.words[0x010601d0]=1;
 if(change==1)m.set32(slot?0x01060df0:0x01060220,a+0x100);
 if(change==2)m.set32(slot?0x01060e30:0x01060260,b+0x100);
 if(change==3)m.set32(b+0xc0,a+0x100);
 if(change==4)m.words[a+0x1f0]=6;
 if(change==5)m.words[slot?0x01060ec0:0x010602f0]=160;
 if(change==6)m.words[slot?0x01060ec0:0x010602f0]=0;
 if(change==7)s.device.active[10+2*slot]=false;
 s.mk2ks_battle_audio_tick();cleared(s,slot);cases++;}
 for(unsigned slot=0;slot<2;slot++)for(unsigned mode=1;mode<=2;mode++){
 midtunit_state s;s.setup(slot,mode);s.processor.memory.words[0x01061990]=1;
 s.mk2ks_battle_audio_tick();if(mode==1)cleared(s,slot);
 else assert(s.device.stopped.empty());cases++;}
 for(unsigned slot=0;slot<2;slot++){
 midtunit_state s;s.setup(slot,2);s.device.active[10+2*slot]=false;
 s.device.active[11+2*slot]=true;s.mk2ks_battle_audio_tick();
 assert(s.device.stopped.empty());cases++;
 midtunit_state both;both.setup(0,2);both.setup(1,2);
 both.mk2ks_battle_audio_stop(slot,"test");assert(both.clock.calls==0);
 assert(both.m_mk2ks_battle_actor[1-slot] && both.device.active[10+2*(1-slot)]);
 both.mk2ks_battle_audio_stop(1-slot,"test");assert(both.clock.calls==1);cases++;}
 midtunit_state idle;idle.mk2ks_battle_audio_tick();assert(idle.device.stopped.empty());cases++;
 midtunit_state absent;absent.setup(0,2);absent.m_mk2ks_voices=nullptr;
 absent.mk2ks_battle_audio_stop(0,"test");assert(!absent.m_mk2ks_battle_actor[0]);
 assert(absent.clock.calls==1);cases++;
 std::cout<<"PASS "<<cases<<" exact-function battle cleanup cases\n";}
'''
cpp = out / 'cleanup.cpp'
cpp.write_text(prefix + functions + tests)
exe = out / 'cleanup.exe'
build = subprocess.run(['C:/Strawberry/c/bin/g++.exe', '-std=c++17', '-O0', str(cpp), '-o', str(exe)], capture_output=True, text=True, timeout=30)
(out / 'compile.log').write_text(build.stdout + build.stderr)
assert build.returncode == 0, build.stderr
run = subprocess.run([str(exe)], capture_output=True, text=True, timeout=10)
(out / 'run.log').write_text(run.stdout + run.stderr)
assert run.returncode == 0 and run.stdout.startswith('PASS 46 '), run.stdout + run.stderr
(out / 'report.json').write_text(json.dumps(dict(passed=True, cases=46, sourceSHA256=sync.sha(path), harnessSHA256=sync.sha(cpp), exactCurrentFunctionsExecuted=True, bothSlots=True, modes=list(range(10)), healthAndOwnershipChanges=True, remainingPlayerKeepsTimer=True, runtimeInterruptionAccepted=False, heardMixAccepted=False, fullPortAccepted=False), indent=2))
print(run.stdout)
