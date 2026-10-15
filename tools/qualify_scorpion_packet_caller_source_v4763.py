"""Whole qualified audio sources retained; one read-only stack tap added.

Actual caller source fidelity still requires native witnesses and independent
instruction qualification. This preflight never claims native audio success.
"""
import ast,json,re,subprocess
from pathlib import Path
import qualify_scorpion_secondary_audio_guard_source_v4665 as previous
import run_scorpion_packet_caller_ram_v4762 as capture
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v4764_scorpion_packet_caller_source_checked'
EXPECTED="""-- Retain every original read-only audio observer and earned physical input.
local file=assert(io.open('mk2ks_scorpion_secondary_audio_ram_v4663.lua','rb'))
local wrapper=file:read('a');file:close()
local marker="assert(load(source,'@entire4210_audio_only_Scorpion_origin_and_4534_controls_4657','t',_ENV))()"
local first,last=assert(wrapper:find(marker,1,true))
assert(not wrapper:find(marker,last+1,true),'Unique original wrapper execution')
local addition=[====[
once("emu.register_frame(function()",[==[
taps[#taps+1]=p:install_read_tap(0xffa13ba0,0xffa13baf,'actual native packet caller stack',function(at)
 if at~=0xffa13ba0 or cpu.PC.value~=at+16 or not active()then return end
 local a,m,sp=cpu.A8.value,cpu.A13.value,cpu.SP.value
 assert(valid(sp),'Actual native packet stack in guest RAM')
 log('PACKET_CALLER',string.format('entry=%08X a1=%08X a3=%08X a4=%08X a8=%08X a13=%08X sp=%08X return_pc=%08X id=%d owner=%08X',
  at,cpu.A1.value,cpu.A3.value,cpu.A4.value,a,m,sp,p:read_u32(sp),
  valid(a)and p:read_u16(a+0x1f0)or-1,valid(m)and p:read_u32(m+0xc0)or 0))
end)
emu.register_frame(function()
]==])
once("assert(#taps==15,'Every audio observer retained')","assert(#taps==16,'Every audio observer retained')")
]====]
wrapper=wrapper:sub(1,first-1)..addition..wrapper:sub(first)
assert(load(wrapper,'@whole4663_plus_readonly_packet_caller_4761','t',_ENV))()
"""

def boundary(wrapper=None,body=None):
    inherited=previous.boundary(body=body)
    wrapper=(ROOT/capture.LUA).read_text()if wrapper is None else wrapper
    need(wrapper==EXPECTED,'Exact whole4663 wrapper plus only read-only caller tap/count assertion')
    old=(ROOT/'mk2ks_scorpion_secondary_audio_ram_v4663.lua').read_text()
    marker="assert(load(source,'@entire4210_audio_only_Scorpion_origin_and_4534_controls_4657','t',_ENV))()"
    need(old.count(marker)==1,'Unique actual retained wrapper execution')
    addition=EXPECTED.split('local addition=[====[\n',1)[1].split(']====]\n',1)[0]
    observed=re.findall(r'^once\((.+)\)$',addition,re.M)
    need(len(observed)==1 and ast.literal_eval('('+observed[0]+')')==(
      "assert(#taps==15,'Every audio observer retained')","assert(#taps==16,'Every audio observer retained')"),
      'Original tap count changes only for actual extra read-only observer')
    tap=addition.split('[==[\n',1)[1].split(']==])',1)[0]
    code=re.sub(r"(['\"]).*?\1|--[^\n]*",'',tap)
    need(not re.search(r':write_|install_write_tap|\.value\s*=(?!=)|return\s+data|load_?state',code),
         'New observer cannot modify guest/register/native output')
    body=(ROOT/'mk2ks_jax_arms_audio_routes_ram_v4210.lua').read_text()
    need(body.count('emu.register_frame(function()')==1 and
         "local function active()return origin and frame<=origin+749 end"in body and
         "p:install_read_tap(entry,entry+15"in body,'Actual retained stack tap uses same native dispatcher/750-field scope')
    generated=capture.collector_source();ast.parse(generated)
    for token in("MK2KS_STOCK_COMMAND='dfff_hp_release'","MK2KS_STOCK_KILLER='scorpion'",'len(rgb)==62',
                  'No raw audio or ROM encoded data written to disk','stateGuestSHA256=state_guest'):
        need(token in generated,'Every inherited real-controller/whole PCM/state/guest/RGB boundary '+token)
    return dict(inherited,actualAudioTapsRetained=15,addedReadOnlyPacketStackTaps=1,
                totalNativeObserverTaps=16,originalNativeAudioRecordSchemasUnchanged=True,
                directPacketCallerSourceAccepted=False,nativeAudioAcceptance=False)

def main():
    need(not OUT.exists(),'Fresh immutable full source preflight')
    prior=ROOT/'audit_v4666_scorpion_secondary_audio_guard_source_checked/report.json'
    proof=json.loads(prior.read_text())
    need(proof['passed']and len(proof['actualSourceFaultsRejected'])==7 and
         all(sha(p)==h for p,h in proof['inputHashes'].items()),'All original source gates/faults/pinned compiled bytes retained')
    positive=boundary();faults=[];w=(ROOT/capture.LUA).read_text();b=(ROOT/'mk2ks_jax_arms_audio_routes_ram_v4210.lua').read_text()
    for label,wrongw,wrongb in(
      ('wrong_packet_entry',w.replace('0xffa13ba0,0xffa13baf','0xffa13b90,0xffa13b9f'),b),
      ('wrong_native_pc',w.replace('cpu.PC.value~=at+16','cpu.PC.value~=at+32'),b),
      ('wrong_stack_read',w.replace('p:read_u32(sp)','p:read_u32(sp+32)'),b),
      ('missing_caller_record',w.replace("log('PACKET_CALLER'","log('PACKET_IGNORED'"),b),
      ('shortened_audio_window',w,b.replace('origin+749','origin+99')),
      ('changed_original_packet',w,b.replace("and 'PACKET'or'QUEUE'","and 'PACKET_IGNORED'or'QUEUE'")),
      ('missing_DCS_tap',w,b.replace('0x3400,0x37ff','0x3401,0x37ff')),
      ('missing_PCM',w,b.replace('sound:get_samples()','sound:get_sample()')),
      ('added_native_write',w+"p:write_u16(0x01060280,1)\n",b)):
        need(wrongw!=w or wrongb!=b,'Real source fault')
        try:boundary(wrongw,wrongb)
        except (ValueError,AssertionError,SyntaxError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Actual source fault admitted '+label)
        need(boundary()==positive,'Whole original-plus-caller source restored')
    pins=dict(proof['inputHashes'])
    for p in(prior,Path(__file__).resolve(),Path(capture.__file__).resolve(),ROOT/capture.LUA,
             Path(previous.__file__).resolve(),ROOT/'tools/run_scorpion_secondary_audio_ram_v4664.py'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every original and new immutable source byte unchanged')
    report=dict(positive,actualSourceFaultsRejected=faults,originalSourceFaultsRetained=7,inputHashes=pins)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)

if __name__=='__main__':main()
