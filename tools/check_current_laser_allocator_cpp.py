"""Execute the actual current allocator body with a recording sample device."""
import json, subprocess
import verify_native_source_sync as sync
sync.verify()
path=sync.ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'
source=path.read_text()
start=source.index('int midtunit_state::mk2ks_finish_audio_start(')
end=source.index('\nvoid midtunit_state::mk2ks_finish_audio_frame',start)
body=source[start:end]
out=sync.ROOT/'audit_current_laser_allocator_cpp'
assert not out.exists();out.mkdir()
prefix=r'''
#include <cstdint>
#include <cassert>
#include <iostream>
struct voices {int calls=0; unsigned channel=99,sample=99; bool loop=true;
 void start(unsigned c,unsigned s,bool l){calls++;channel=c;sample=s;loop=l;}};
struct midtunit_state { uint16_t m_mk2ks_finish_audio_priority[5]={};
 uint16_t m_mk2ks_finish_audio_remaining[5]={}; voices device;
 voices *m_mk2ks_voices=&device;
 int mk2ks_finish_audio_start(unsigned,uint16_t,uint16_t);};
'''
tests=r'''
int main(){
 midtunit_state a;
 for(int i=0;i<5;i++){assert(a.mk2ks_finish_audio_start(17+i,0x50,56+i)==i);
 assert(a.device.channel==14u+i && a.device.sample==17u+i && !a.device.loop);
 assert(a.m_mk2ks_finish_audio_remaining[i]==56+i);}
 assert(a.mk2ks_finish_audio_start(22,0x42,203)==-1 && a.device.calls==5);
 assert(a.mk2ks_finish_audio_start(22,0x50,99)==0 && a.device.calls==6);
 midtunit_state b; assert(b.mk2ks_finish_audio_start(1,0x31,20)==0);
 assert(b.mk2ks_finish_audio_start(2,0x31,40)==-1 && b.device.calls==1);
 assert(b.m_mk2ks_finish_audio_remaining[0]==20);
 midtunit_state c; assert(c.mk2ks_finish_audio_start(1,0x41,20)==0);
 assert(c.mk2ks_finish_audio_start(2,0x41,40)==0 && c.device.calls==2);
 assert(c.m_mk2ks_finish_audio_remaining[0]==40);
 midtunit_state d; uint16_t priorities[]={0x50,0x42,0x41,0x50,0x50};
 for(int i=0;i<5;i++)d.m_mk2ks_finish_audio_priority[i]=priorities[i];
 assert(d.mk2ks_finish_audio_start(19,0x43,203)==2);
 assert(d.device.channel==16 && d.device.sample==19);
 std::cout << "PASS: free slots, channel mapping, duplicate rejection, same-class replacement, least-priority replacement, low-priority rejection\n";
}
'''
cpp=out/'allocator.cpp';cpp.write_text(prefix+body+tests)
exe=out/'allocator.exe'
compiler='C:/Strawberry/c/bin/g++.exe'
build=subprocess.run([compiler,'-std=c++17','-O0',str(cpp),'-o',str(exe)],capture_output=True,text=True,timeout=30)
(out/'compile.log').write_text(build.stdout+build.stderr)
assert build.returncode==0,build.stderr
run=subprocess.run([str(exe)],capture_output=True,text=True,timeout=10)
(out/'run.log').write_text(run.stdout+run.stderr)
assert run.returncode==0 and run.stdout.startswith('PASS:')
report=dict(passed=True,sourceSHA256=sync.sha(path),extractedFunctionSHA256=sync.sha(cpp),
 actualCurrentFunctionExecuted=True,emulatorRuntimeCoverage=False,heardMixAccepted=False,
 fullPortAccepted=False,compiler=compiler)
(out/'report.json').write_text(json.dumps(report,indent=2))
print(run.stdout)
