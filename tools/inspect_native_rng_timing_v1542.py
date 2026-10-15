"""Source-bound native RNG timing mechanism, not runtime causality acceptance."""
import json,subprocess
from pathlib import Path
import verify_active_launch_timer_v1520 as source
ROOT=source.ROOT;OUT=ROOT/'audit_v1542_native_rng_timing'
def inspect():
 pins={}
 def pin(p):pins[str(p)]=source.sha(p)
 guestfile=ROOT/'audit_v1519_channels_square_p1/guest_maincpu.bin'
 guest=guestfile.read_bytes();old=source.sound.prior.expected_guest()[0]
 at=(0xff80e980-0xff800000)//8;end=(0xff80eae0-0xff800000)//8
 assert guest[at:end]==old[at:end],'Original RNG routine must be unchanged'
 pin(guestfile)
 core=ROOT/'mame-mkp/src/devices/cpu/tms34010/tms34010.cpp'
 header=ROOT/'mame-mkp/src/devices/cpu/tms34010/tms34010.h'
 pin(core);pin(header);text=core.read_text();h=header.read_text()
 enum=h.split('REG_HESYNC = 0,',1)[1].split('};',1)[0]
 regs=['REG_HESYNC']+[line.strip().strip(',')for line in enum.splitlines()if line.strip().startswith('REG_')]
 assert regs.index('REG_HCOUNT')==28
 assert 'map(0xc0000000, 0xc00001ff).rw(FUNC(tms34010_device::io_register_r)'in text
 handler=text.split('case REG_HCOUNT:',1)[1].split('case REG_REFCNT:',1)[0]
 assert 'screen().hpos()'in handler,'Native RNG IO source is actual horizontal beam position'
 disassembler=ROOT/'mame-mkp/unidasm.exe';pin(disassembler)
 r=subprocess.run([str(disassembler),str(guestfile),'-arch','tms34010','-basepc','0xff80e980','-skip','0x1d30','-count','352','-norawbytes'],capture_output=True,text=True,check=True)
 assert 'MOVE   @C00001C0h,A1,0'in r.stdout and 'RL     A1,A0'in r.stdout and 'MOVE   @105B950h,A0,1'in r.stdout
 pin(__file__)
 return dict(passed=True,originalRNGRoutineUnchanged=True,seedAddress='0105B950',nativeTimingReadAddress='C00001C0',nativeTimingReadRegister='HCOUNT',nativeTimingSource='screen().hpos()',rngRotatesByNativeBeamPosition=True,disassembly=r.stdout,actualCoreHCountHandler=handler,inputHashes=pins,interpretation='Additional native cue instructions can shift the hardware beam position sampled by original RNG, so changed CPU choices after a launch need not imply an ID/proxy or AI freeze. Actual paired old/new RNG values must still be captured before attributing the observed frame-2141 divergence to this mechanism.',runtimeCauseProven=False,repeatedCPUAccepted=False,fullPortAccepted=False,scope=__doc__)
if __name__=='__main__':
 assert not OUT.exists()
 report=inspect();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(passed=True,nativeRNGTimingRegister=report['nativeTimingReadRegister'],runtimeCauseProven=False)),flush=True)
