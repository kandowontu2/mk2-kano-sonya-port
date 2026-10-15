"""Exact source-function unit execution, not emulator interruption acceptance."""
import json, subprocess
import verify_native_source_sync as sync
sync.verify()
path=sync.ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'
source=path.read_text()
stop=source[source.index('void midtunit_state::mk2ks_finish_audio_stop('):source.index('\nint midtunit_state::mk2ks_finish_audio_start(')]
frame=source[source.index('void midtunit_state::mk2ks_finish_audio_frame('):source.index('\nvoid midtunit_state::mk2ks_finish_audio_marker(')]
out=sync.ROOT/'audit_current_laser_cleanup_cpp'
assert not out.exists();out.mkdir()
prefix=r'''
#include <cstdint>
#include <cassert>
#include <map>
#include <vector>
#include <iostream>
#define AS_PROGRAM 0
#define logerror(...) ((void)0)
struct mem {std::map<uint32_t,uint16_t> words;
 uint16_t read_word(uint32_t a){return words[a];}
 void set32(uint32_t a,uint32_t v){words[a]=v;words[a+16]=v>>16;}};
struct cpu {mem memory;mem &space(int){return memory;}};
struct voices {std::vector<unsigned> stopped;void stop(unsigned c){stopped.push_back(c);}};
struct midtunit_state {cpu processor;cpu *m_maincpu=&processor;voices device;
 voices *m_mk2ks_voices=&device;
 uint32_t m_mk2ks_finish_audio_actor=0x01030000,m_mk2ks_finish_audio_main=0x01040000;
 uint16_t m_mk2ks_finish_audio_slot=0;
 uint16_t m_mk2ks_finish_audio_priority[5]={0x50,0x50,0x42,0x50,0x50};
 uint16_t m_mk2ks_finish_audio_remaining[5]={2,2,2,2,2};
 void mk2ks_finish_audio_stop(const char*);void mk2ks_finish_audio_frame(int);
 void setup(unsigned slot,uint16_t mode){m_mk2ks_finish_audio_slot=slot;
 auto &m=processor.memory;m.words[0x010601d0]=mode;
 m.set32(slot?0x01060df0:0x01060220,m_mk2ks_finish_audio_actor);
 m.set32(slot?0x01060e30:0x01060260,m_mk2ks_finish_audio_main);
 m.set32(m_mk2ks_finish_audio_main+0xc0,m_mk2ks_finish_audio_actor);
 m.words[m_mk2ks_finish_audio_actor+0x1f0]=17;}
};
'''
tests=r'''
void cleared(midtunit_state &s){assert(s.device.stopped==std::vector<unsigned>({14,15,16,17,18}));
 assert(!s.m_mk2ks_finish_audio_actor && !s.m_mk2ks_finish_audio_main && !s.m_mk2ks_finish_audio_slot);
 for(int i=0;i<5;i++)assert(!s.m_mk2ks_finish_audio_priority[i] && !s.m_mk2ks_finish_audio_remaining[i]);}
int main(){int cases=0;
 for(unsigned slot=0;slot<2;slot++)for(uint16_t mode=0;mode<10;mode++){
 midtunit_state s;s.setup(slot,mode);s.mk2ks_finish_audio_frame(1);
 if(mode==2 || mode==5){assert(s.device.stopped.empty());assert(s.m_mk2ks_finish_audio_remaining[0]==1);
 assert(s.m_mk2ks_finish_audio_remaining[4]==2);
 s.mk2ks_finish_audio_frame(1);assert(s.device.stopped.empty());
 assert(s.m_mk2ks_finish_audio_remaining[4]==1);assert(!s.m_mk2ks_finish_audio_priority[3]);}
 else cleared(s);cases++;}
 for(unsigned slot=0;slot<2;slot++)for(int change=0;change<4;change++){
 midtunit_state s;s.setup(slot,2);auto &m=s.processor.memory;
 if(change==0)m.set32(slot?0x01060df0:0x01060220,0x01050000);
 if(change==1)m.set32(slot?0x01060e30:0x01060260,0x01050000);
 if(change==2)m.set32(s.m_mk2ks_finish_audio_main+0xc0,0x01050000);
 if(change==3)m.words[s.m_mk2ks_finish_audio_actor+0x1f0]=18;
 s.mk2ks_finish_audio_frame(1);cleared(s);cases++;}
 midtunit_state invalid;invalid.m_mk2ks_finish_audio_slot=2;invalid.mk2ks_finish_audio_frame(1);cleared(invalid);cases++;
 midtunit_state edge;edge.setup(0,2);edge.mk2ks_finish_audio_frame(0);
 assert(edge.device.stopped.empty() && edge.m_mk2ks_finish_audio_remaining[0]==2);cases++;
 std::cout<<"PASS "<<cases<<" exact-function cleanup/timer cases\n";
}
'''
cpp=out/'cleanup.cpp';cpp.write_text(prefix+stop+frame+tests)
exe=out/'cleanup.exe'
build=subprocess.run(['C:/Strawberry/c/bin/g++.exe','-std=c++17','-O0',str(cpp),'-o',str(exe)],capture_output=True,text=True,timeout=30)
(out/'compile.log').write_text(build.stdout+build.stderr)
assert build.returncode==0,build.stderr
run=subprocess.run([str(exe)],capture_output=True,text=True,timeout=10)
(out/'run.log').write_text(run.stdout+run.stderr)
assert run.returncode==0 and run.stdout.startswith('PASS 30')
report=dict(passed=True,cases=30,sourceSHA256=sync.sha(path),harnessSHA256=sync.sha(cpp),
 exactCurrentFunctionsExecuted=True,bothSlots=True,modes=list(range(10)),
 timerExpiryDoesNotStopPCM=True,fourthSlotPostponesFifth=True,
 runtimeInterruptionAccepted=False,heardMixAccepted=False,fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2))
print(run.stdout)
