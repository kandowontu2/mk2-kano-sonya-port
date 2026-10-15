"""Before-boot, exact old controllers plus read-only native ending renderer."""
import ast,hashlib,inspect,json,re,subprocess
from pathlib import Path
import qualify_kano_current_p2_campaign_source_v4482 as kano
import qualify_kintaro_pressure_guard_long_source_v4437 as sonya
import ending_display_ram_model_v4519 as model
import run_current_tomb_ram_matrix_v3648 as renderer
ROOT,need,sha=kano.ROOT,kano.need,kano.sha
OUT=ROOT/'audit_v4523_ending_display_source_preflight'
OBSERVER='mk2ks_ending_display_ram_v4518.lua'
LUA={'kano':'mk2ks_kano_ending_display_campaign_ram_v4520.lua',
     'sonya':'mk2ks_sonya_ending_display_campaign_ram_v4521.lua'}
TRANSITIVE_LUA=tuple(sorted(set(kano.TRANSITIVE_LUA+sonya.TRANSITIVE_LUA+tuple(LUA.values())+
    (OBSERVER,'mk2ks_native_tomb_ram_v3624.lua','mk2ks_native_tomb_display_v2062.lua'))))
TOKEN=r'''"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|\[\[[\s\S]*?\]\]'''

def literal(token):
    if token.startswith('[['):
        s=token[2:-2]
        return s[1:] if s.startswith('\n') else s
    return ast.literal_eval(token)

def observer_source(text):
    original=(ROOT/'mk2ks_native_tomb_display_v2062.lua').read_text()
    actions=[]
    pattern=r'\b(once|region)\(\s*('+TOKEN+r')\s*,\s*('+TOKEN+r')(?:\s*,\s*('+TOKEN+r'))?\s*\)'
    for m in re.finditer(pattern,text):
        actions.append((m[1],*[literal(t) for t in m.groups()[1:] if t is not None]))
    expected=[
      ('once',"dofile('mk2ks_stage_branch_provenance_v1722.lua')",''),
      ('once','local frame,command=0,nil','local frame,command,ending_completed,ending_ko,own_wins,seen_live=0,nil,nil,nil,0,false'),
      ('once',"local output=assert(os.getenv('MK2KS_STAGE_OUT'))","local output=assert(os.getenv('MK2KS_CAMPAIGN_OUT'))"),
      ('once',"local side=tonumber(assert(os.getenv('MK2KS_STAGE_SIDE')))","local side=tonumber(assert(os.getenv('MK2KS_CAMPAIGN_SIDE')));assert(side==2)"),
      ('once',"os.getenv('MK2KS_STAGE_WINNER')","os.getenv('MK2KS_TEST_FIGHTER')"),
      ('once','local function window_end()return retired.frame and retired.frame+30 or command and command+1000 end',
       'local function window_end()return ending_completed and ending_completed+300 or command and command+4000 end'),
      ('once','f>=command+1','f>=command'),
      ('once',"local f=assert(io.open(output..'/'..file,'wb'));f:write(raw);f:close()",'MK2KS_TOMB_RAM_SAVE(file,raw)'),
      ('once','screen:snapshot(file)','MK2KS_TOMB_RAM_PIXELS(file)'),
      ('region','local function actor(n)','-- The original helper allocates A10;','local function actor(n)return nil end\n\n')]
    need(actions[:10]==expected and len(actions)==11 and
         actions[10][:3]==('region','for _,address in ipairs({action_entry})do','-- Observe actual native sound-port writes;'),
         'Exactly declared original renderer/window/transport substitutions; no command or actor identity replacement')
    native=actions[10][3]
    for token in ('cpu.PC.value~=0xff8296b0','cpu.PC.value~=0xff836700','own_wins~=1','not seen_live',
                  'p:read_u16(at)<=0','mask~=0xffff','data~=0',
                  'p:read_u16(0x01061b30)==16','p:read_u16(0x01061b00)==side','roster==identity',
                  'p:read_u32(0x01060220)==0','p:read_u32(0x01060df0)==0','ensure_base()',
                  'frame-command>1200','ending_completed=frame'):
        need(token in native,'Native final-collision/own-winner/actor-retired ending/attract provenance: '+token)
    for action in actions:
        if action[0]=='once':
            _,before,after=action;need(original.count(before)==1,'Unique complete original renderer boundary')
            original=original.replace(before,after)
        else:
            _,first,last,new=action
            need(original.count(first)==original.count(last)==1,'Unique complete original renderer region')
            a,b=original.index(first),original.index(last,original.index(first)+len(first))
            original=original[:a]+new+original[b:]
    need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|set_value|clear_value|return\s+data|io\.open|snapshot\(|machine:exit|set_input',original),
         'Executed original video observer is strictly read-only; no native or control mutation or disk media')
    ram=(ROOT/'mk2ks_native_tomb_ram_v3624.lua').read_text().split('local handle=assert(io.open',1)[0]
    need(ram.count('io.stdout:write')==2 and not re.search(r'io\.open|:write_|write_u\d+|\.value\s*=(?!=)|snapshot\(',ram),
         'Whole original RAM delta/RGB transport functions only, no native or filesystem sink')
    for token in ('FLOOR_CPU','FLOOR_FLIP','FLOOR_SHIFT_LOAD','FLOOR_SHIFT_FILL','FLOOR_SHIFT',
                  'FLOOR_GFX','FLOOR_DMA','FLOOR_PRE_FRAME','FLOOR_LATCH','FLOOR_HELD','FLOOR_SNAP'):
        need(token in original,'Every complete original continuous native raster operation retained')
    return original,ram

def source_boundary(fighter):
    need(fighter in LUA,'Only unchanged accepted true P2 controls')
    parent=kano if fighter=='kano'else sonya;proof=parent.source_boundary()
    expected='-- Existing accepted controller unchanged; only a read-only video observer.\n'+\
      f"dofile('{parent.LUA}')\ndofile('{OBSERVER}')\n"
    need((ROOT/LUA[fighter]).read_text()==expected,'Exact accepted controller and one read-only renderer observer')
    observed=(ROOT/OBSERVER).read_text();executed,ram=observer_source(observed)
    need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|set_value|clear_value|return\s+data|machine:exit|set_input',observed),
         'Wrapper cannot mutate game, input policy or ending')
    return dict(passed=True,fighter=fighter,physicalSlot=2,originalControllerProof=proof,
      executedVideoObserverSHA256=hashlib.sha256(executed.encode()).hexdigest().upper(),
      originalRAMTransportFunctionSHA256=hashlib.sha256(ram.encode()).hexdigest().upper(),
      continuousModelSHA256=model.MODEL_SOURCE_SHA256,physicalInputsExactlyUnchanged=True,
      floorShadowBodyPaletteClassificationNotApplicableToThisEndingWindow=True,
      everyNativeCPUShiftDMAGraphicsVRAMRGBGateRetained=True,fullPortAcceptance=False)

def main():
    need(not OUT.exists(),'Fresh immutable ending video before-boot proof')
    contexts=[source_boundary(f) for f in LUA];faults=[]
    actual=(ROOT/OBSERVER).read_text()
    for label,before,after in (
      ('wrong_native_KO_PC','cpu.PC.value~=0xff836700','cpu.PC.value~=0xff836710'),
      ('missing_native_actor_retirement','p:read_u32(0x01060df0)==0','true'),
      ('shortened_complete_ending_window','ending_completed+300','ending_completed+30'),
      ('guest_ID_write',"command=frame;origin=frame;ensure_base()","command=frame;p:write_u16(0x01060e50,1);origin=frame;ensure_base()")):
        changed=actual.replace(before,after,1);need(changed!=actual,'Actual non-vacuous observer source fault')
        try:observer_source(changed)
        except ValueError as e:faults.append(dict(label=label,rejectedBy=str(e)))
        else:raise ValueError('Accepted ending observer fault: '+label)
    observer_source(actual)
    transport_control=renderer.protocol_control()
    files=[Path(__file__).resolve(),Path(model.__file__),Path(model.original.__file__),Path(renderer.__file__),
      ROOT/'tools/run_ending_display_campaign_ram_v4526.py',
      ROOT/'audit_v4488_kano_current_p2_whole_campaign_checked/report.json',
      ROOT/'audit_v4443_kintaro_pressure_guard_long_whole_campaign_checked/report.json',
      ROOT/'audit_v3635_current_native_tomb_ram_checked/report.json',
      Path(kano.__file__),Path(sonya.__file__)]+[ROOT/p for p in TRANSITIVE_LUA]
    for p in files[5:8]:need(json.loads(p.read_text())['passed'],'Qualified complete source/control/render evidence retained')
    report=dict(passed=True,contexts=contexts,actualObserverSourceFaultsRejected=faults,
      originalRAMTransportControl=transport_control,inputHashes={str(p.resolve()):sha(p) for p in files},
      nativeEndingVideoAcceptance=False,fullPortAcceptance=False)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,
      'Compressed before proof writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='inputHashes'},indent=2),flush=True)

if __name__=='__main__':main()
