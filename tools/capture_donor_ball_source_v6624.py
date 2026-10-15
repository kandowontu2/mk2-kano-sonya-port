"""Native donor source disassembly, whole-ROM RAM equality, no media transport."""
import json,hashlib,subprocess,ctypes,re,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'audit_v6623_donor_ball_startup_source'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def need(v,m):
 if not v:raise ValueError(m)
def main():
 need(not OUT.exists(),'Fresh read-only donor evidence')
 exe=ROOT.parent/'mame0289/mame.exe';lua=ROOT/'mk3_cannonball_startup_source_v6622.lua'
 rom=ROOT/'mk3/mk3-maincpu.bin';pins={str(p.resolve()):sha(p)for p in [exe,lua,rom,Path(__file__)]}
 OUT.mkdir();subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True,check=True)
 args=[str(exe),'mk3','-rompath',str(ROOT)+';'+str(ROOT.parent/'mame0289/roms'),'-nocheat',
  '-skip_gameinfo','-video','none','-sound','none','-nothrottle','-str','8','-debug','-debugger','none',
  '-autoboot_delay','0','-inipath',str(OUT),'-cfg_directory',str(OUT/'cfg'),'-nvram_directory',str(OUT/'nvram'),
  '-snapshot_directory',str(OUT/'snap'),'-autoboot_script',str(lua)]
 process=subprocess.Popen(args,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',errors='replace')
 print('Actual donor source PID',process.pid,flush=True)
 output,stderr=process.communicate();proof=None;lines=[]
 for line in output.splitlines():
  if line.startswith('MK3_BALL_DONOR_ROM '):
   q=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(q['hex'])
   need(len(raw)==int(q['bytes'])==1048576 and raw==rom.read_bytes(),'Every actual donor program byte matches independent whole original ROM')
   proof=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest().upper(),everyActualByteComparedInRAM=True)
  else:lines.append(line)
 (OUT/'run.log').write_text('\n'.join(lines)+'\n');(OUT/'stderr.log').write_text(stderr)
 result=dict(passed=False,exitCode=process.returncode,command=args,pid=process.pid,wholeNativeROM=proof,
  inputHashes=pins,newBuilds=0,newROMCopies=0,guestStateWrites=0,fullPortAcceptance=False,
  observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  need(process.returncode==0 and proof and not stderr.strip()and
       any(l=='MK3_BALL_DONOR_SOURCE_TERMINAL fields=30 writes=0'for l in lines),'Natural read-only donor terminal')
  need((OUT/'cannonball.asm').exists()and all(sha(p)==h for p,h in pins.items()),'Actual native disassembly and every original input intact')
  result['passed']=True
 except Exception as error:result['error']=repr(error)
 (OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 for p in OUT.rglob('*'):
  if p.is_file():
   before=sha(p);subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True,check=True)
   need(sha(p)==before,'Exact compressed donor evidence')
 print(json.dumps(dict(passed=result['passed'],exitCode=process.returncode,error=result.get('error'),wholeNativeROM=proof)),flush=True)
 need(result['passed'],'Donor source inspection failed; retain evidence')
if __name__=='__main__':main()
