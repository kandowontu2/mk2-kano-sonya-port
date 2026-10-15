"""Preboot source boundary for full audio observer and unchanged real inputs."""
import ast,json,re,struct,subprocess
from pathlib import Path
import run_scorpion_secondary_audio_ram_v4658 as capture
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v4660_scorpion_secondary_audio_source_checked'
CHANGES=[("dofile('mk2ks_stock_extended_earned_ram_v3958.lua')","dofile('mk2ks_scorpion_secondary_state_ram_v4534.lua')"),
         ('0xff8be240,0xff8be24f','0xff8bbfe0,0xff8bbfef'),
         ('actual native Jax arm-rip audio origin','actual native Scorpion secondary audio origin'),
         ('at~=0xff8be240','at~=0xff8bbfe0'),('p:read_u16(a+0x1f0)~=11','p:read_u16(a+0x1f0)~=10'),('id=11','id=10')]

def boundary(wrapper=None,body=None):
    wrapper=(ROOT/capture.LUA).read_text()if wrapper is None else wrapper
    body=(ROOT/'mk2ks_jax_arms_audio_routes_ram_v4210.lua').read_text()if body is None else body
    observed=re.findall(r'^once\((.+)\)$',wrapper,re.M)
    # These literals are plain quoted strings, so Python's literal parser and
    # Lua consume exactly the same arguments (no escape or computed strings).
    need([ast.literal_eval('('+x+')')for x in observed]==CHANGES,'Precisely six literal controller/origin/ID adapters')
    prefix="-- Entire existing audio observer; only native origin/ID and physical driver change.\nlocal file=assert(io.open('mk2ks_jax_arms_audio_routes_ram_v4210.lua','rb'))\nlocal source=file:read('a');file:close()\nlocal function once(before,after)\n local first,last=assert(source:find(before,1,true))\n assert(not source:find(before,last+1,true),'Unique audio role adapter')\n source=source:sub(1,first-1)..after..source:sub(last+1)\nend\n"
    suffix="assert(not source:find(':write_',1,true))\nassert(load(source,'@entire4210_audio_only_Scorpion_origin_and_4534_controls_4657','t',_ENV))()\n"
    need(wrapper.startswith(prefix)and wrapper.endswith(suffix)and len(wrapper.splitlines())==16,'Complete exact small read-only wrapper, no extra callsites')
    original=(ROOT/'mk2ks_jax_arms_audio_routes_ram_v4210.lua').read_text()
    need(body==original,'Every original15tap/PCM/guest/channel/packet/DSP/audio scope source byte retained')
    for before,after in CHANGES:
        need(body.count(before)==1,'Unique actual retained source role');body=body.replace(before,after)
    code=re.sub(r"(['\"]).*?\1|--[^\n]*",'',body)
    need(not re.search(r':write_|\.value\s*=(?!=)|return\s+data|load_?state',code),'No guest/register/native output overrides')
    capture.state.source.source_boundary()
    generated=capture.collector_source();ast.parse(generated)
    need('stateGuestSHA256=state_guest'in generated and 'len(rgb)==62'in generated and
         "MK2KS_STOCK_COMMAND='dfff_hp_release'"in generated and "MK2KS_STOCK_KILLER='scorpion'"in generated and
         'No raw audio or ROM encoded data written to disk'in generated,'Whole4212 capture retains original audio protocol and complete4534 RAM guest/RGB protocol')
    guest=capture.state.source.current.expected();stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for lo,hi in((0xff8bbfe0,0xff8bd040),(0xffa0ef20,0xffa10ee0),(0xffa11fd0,0xffa122a0),
                  (0xffa122d0,0xffa13df0)):
        a,b=(lo-0xff800000)//8,(hi-0xff800000)//8
        need(guest[a:b]==stock[a:b],'Complete original Scorpion/voice/queue/packet source '+hex(lo))
    need(struct.unpack_from('<12H',guest,0xfe040)==(0x0b42,0xffef,0xca06,0x0b42,0xffed,0xca03,0xc080,0x22d0,0xffa1,0xc080,0x23b0,0xffa1),
         'Exact true18 native female extension, no proxy identity')
    return dict(passed=True,actualAudioTapsRetained=15,originalEarnedControllerUnchanged=True,
                rawMediaFilesWritten=0,nativeAudioAcceptance=False,fullPortAcceptance=False)

def main():
    need(not OUT.exists(),'Fresh immutable preboot source result');positive=boundary();faults=[]
    w=(ROOT/capture.LUA).read_text();b=(ROOT/'mk2ks_jax_arms_audio_routes_ram_v4210.lua').read_text()
    for label,wrongw,wrongb in(
      ('wrong_origin',w.replace('0xff8bbfe0,0xff8bbfef','0xff8bbfd0,0xff8bbfdf'),b),
      ('proxy_id',w.replace("'id=10'","'id=1'"),b),
      ('wrong_controls',w.replace('mk2ks_scorpion_secondary_state_ram_v4534.lua','mk2ks_stock_extended_earned_ram_v3958.lua'),b),
      ('missing_dcs_tap',w,b.replace('0x3400,0x37ff','0x3401,0x37ff')),
      ('missing_pcm',w,b.replace('sound:get_samples()','sound:get_sample()')),
      ('shortened_audio_window',w,b.replace('origin+749','origin+99')),
      ('additional_native_write',w+"p:write_u16(0x01060280,1)\n",b)):
        need(wrongw!=w or wrongb!=b,'Non-vacuous actual source fault')
        try:boundary(wrongw,wrongb)
        except (ValueError,AssertionError,SyntaxError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Invalid source accepted '+label)
        need(boundary()==positive,'Whole source positive restored after each fault')
    files=[Path(__file__).resolve(),Path(capture.__file__).resolve(),Path(capture.previous.__file__).resolve(),
           Path(capture.state.__file__).resolve(),Path(capture.state.source.__file__).resolve(),ROOT/capture.LUA,
           ROOT/'mk2ks_jax_arms_audio_routes_ram_v4210.lua',ROOT/capture.state.source.LUA,ROOT/capture.state.source.CONTROL,
           ROOT/'mk2ks_arm_palette_trace_v1073.lua',ROOT/'mk2/mk2-maincpu.bin']
    build=json.loads((ROOT/capture.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    files.extend(Path(p)for p in build['input_hashes'])
    for p,h in build['input_hashes'].items():need(sha(p)==h,'Every compiled source unchanged')
    report=dict(positive,actualSourceFaultsRejected=faults,inputHashes={str(p.resolve()):sha(p)for p in files})
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2))

if __name__=='__main__':main()
