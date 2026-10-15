"""Before boot: frozen whole controllers/renderer plus native hardware binding.

Actual41-field hardware timing proof is retained, not substituted for full
ending video. All original source/transport gates and exclusions retained.
"""
import copy,inspect,json,re,subprocess
from pathlib import Path
import qualify_ending_display_source_v4541 as previous
import ending_display_ram_model_v4612 as model
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_v4624_ending_display_latch_source_checked'
OBSERVER='mk2ks_ending_display_ram_v4613.lua'
LUA={'kano':'mk2ks_kano_ending_display_latch_campaign_ram_v4620.lua',
     'sonya':'mk2ks_sonya_ending_display_latch_campaign_ram_v4621.lua'}
TRANSITIVE_LUA=tuple(sorted(set(previous.TRANSITIVE_LUA+(OBSERVER,)+tuple(LUA.values()))))
ADAPTER=r'''-- Entire frozen4542 read-only observer, plus actual scanout registers only.
local h=assert(io.open('mk2ks_ending_display_ram_v4542.lua','r'))
local source=h:read('a');h:close()
local boundary="assert(not source:find('io.open',1,true)"
local insertion=[[once("log('FLOOR_DISPLAY',", "log('FLOOR_SCANOUT',string.format('epoch=1 start=%04X dpyadr=%04X control=%04X tap=%04X vcount=%d vsblnk=%d veblnk=%d',p:read_u16(0xc0000090),p:read_u16(0xc00001e0),p:read_u16(0xc0000080),p:read_u16(0xc00001b0),p:read_u16(0xc00001d0),p:read_u16(0xc0000060),p:read_u16(0xc0000050)))\n log('FLOOR_DISPLAY',")
]]
local at=assert(source:find(boundary,1,true),'One original read-only observer boundary')
assert(not source:find(boundary,at+#boundary,true),'Unique original read-only observer boundary')
source=source:sub(1,at-1)..insertion..source:sub(at)
assert(load(source,'@entire4542_ending_with_actual_native_scanout_4613','t',_ENV))()
'''
SCANOUT="log('FLOOR_SCANOUT',string.format('epoch=1 start=%04X dpyadr=%04X control=%04X tap=%04X vcount=%d vsblnk=%d veblnk=%d',p:read_u16(0xc0000090),p:read_u16(0xc00001e0),p:read_u16(0xc0000080),p:read_u16(0xc00001b0),p:read_u16(0xc00001d0),p:read_u16(0xc0000060),p:read_u16(0xc0000050)))"

def observer_source(text):
    need(text==ADAPTER,'Exactly one read-only actual native hardware metadata insertion, no other adapter change')
    original,ram=previous.observer_source((ROOT/previous.OBSERVER).read_text())
    boundary="log('FLOOR_DISPLAY',"
    need(original.count(boundary)==1,'Unique original palette/display field boundary')
    executed=original.replace(boundary,SCANOUT+'\n '+boundary)
    need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|set_value|clear_value|return\s+data|io\.open|snapshot\(|machine:exit|set_input',executed),
         'Entire generated hardware/video observer strictly read-only and RAM-only')
    return executed,ram

scope=dict(vars(previous),OBSERVER=OBSERVER,LUA=LUA,model=model,observer_source=observer_source)
exec(compile(inspect.getsource(previous.source_boundary),__file__+'::entire4541_physical_source_boundary','exec'),scope)
source_boundary=scope['source_boundary']

def hardware_control():
    path=ROOT/'audit_v4615_ending_native_latch_timing_checked/report.json'
    proof=json.loads(path.read_text())
    need(proof['passed']and proof['actualNativeVBLANKLatchCauseEstablished']and
         not proof['fullEndingRendererVideoAccepted']and len(proof['actualHardwareFaultsRejected'])==4,
         'Actual hardware cause and original scope/fault exclusions preserved')
    need(all(sha(p)==h for p,h in proof['inputHashes'].items()),'All actual source/native hardware timing inputs unchanged')
    records=json.loads((ROOT/'audit_v4608_kano_ending_latch_probe_ram/ending_latch_probe_records.json').read_text())
    def contract(rows):
        need(len(rows)==41,'All41 actual native timing fields, including original failed field')
        derived=[]
        for row,qualified in zip(rows,proof['hardwareDerivedVisibleFields'],strict=True):
            native=row['native']
            line='MK2_NAT_CAMPAIGN_FLOOR_SCANOUT epoch=1 '+' '.join(k+'='+native[k]for k in ('frame','start','dpyadr','control','tap','vcount','vsblnk','veblnk'))
            tag,scan=model.parse(line)
            display={k:scan[k]for k in ('epoch','frame','start','control','tap')}
            start=model.visible_start(scan,display,scan['frame'])
            need(tag=='FLOOR_SCANOUT'and scan['frame']==qualified['frame']and start==qualified['derivedLatchedVisibleStart'],
                 'Same independently source-derived actual hardware address, not image match selection')
            derived.append(start)
        return derived
    positive=contract(records);faults=[]
    address=copy.deepcopy(records);address[20]['native']['dpyadr']='F01C'
    phase=copy.deepcopy(records);phase[20]['native']['vcount']='272'
    stride=copy.deepcopy(records);stride[20]['native']['control']='F020'
    for label,rows in [('wrong_actual_DP YADR'.replace(' ',''),address),('wrong_actual_beam_phase',phase),
                       ('wrong_actual_DUDATE',stride),('missing_actual_failed_field',records[:20]+records[21:])]:
        try:contract(rows)
        except ValueError as error:faults.append(dict(label=label,rejectedBy=str(error)))
        else:raise ValueError('Accepted actual hardware fault: '+label)
        need(contract(records)==positive,'All41 unchanged actual positive fields restored after every fault')
    return dict(passed=True,actualFields=41,actualHardwareFaultsRejected=faults,fullEndingRendererVideoAccepted=False)

def main():
    need(not OUT.exists(),'Fresh immutable before-boot hardware/video qualification')
    contexts=[source_boundary(f)for f in LUA];faults=[]
    actual=(ROOT/previous.OBSERVER).read_text()
    for label,before,after in (
      ('wrong_native_KO_PC','cpu.PC.value~=0xff836700','cpu.PC.value~=0xff836710'),
      ('missing_native_actor_retirement','p:read_u32(0x01060df0)==0','true'),
      ('shortened_complete_ending_window','ending_completed+300','ending_completed+30'),
      ('guest_ID_write','command=frame;origin=frame;ensure_base()','command=frame;p:write_u16(0x01060e50,1);origin=frame;ensure_base()')):
        changed=actual.replace(before,after,1);need(changed!=actual,'Actual original observer source fault')
        try:previous.observer_source(changed)
        except ValueError as error:faults.append(dict(label=label,rejectedBy=str(error)))
        else:raise ValueError('Accepted inherited source fault: '+label)
        previous.observer_source(actual)
    adapter=(ROOT/OBSERVER).read_text()
    for label,before,after in [('wrong_DP YADR_address'.replace(' ',''),'0xc00001e0','0xc0000090'),
                             ('wrong_scanline_register','0xc00001d0','0xc00001b0'),
                             ('missing_hardware_metadata','dpyadr=%04X','omitted=%04X')]:
        changed=adapter.replace(before,after,1);need(changed!=adapter,'Actual adapter source fault')
        try:observer_source(changed)
        except ValueError as error:faults.append(dict(label=label,rejectedBy=str(error)))
        else:raise ValueError('Accepted hardware metadata source fault: '+label)
        observer_source(adapter)
    hardware=hardware_control();transport=previous.renderer.protocol_control()
    import run_ending_display_latch_campaign_ram_v4617 as capture
    for fighter in LUA:
        names=capture.collector(fighter).__code__.co_varnames
        need('errors'in names and 'scene_errors'in names,'Generated full native stderr and model error locals remain distinct')
    files={Path(__file__).resolve(),Path(model.__file__),Path(model.previous.__file__),Path(model.previous.original.__file__),
           Path(previous.__file__),Path(capture.__file__),Path(capture.previous.__file__),
           ROOT/'audit_v4615_ending_native_latch_timing_checked/report.json',
           ROOT/'tools/verify_ending_native_latch_timing_v4614.py'}|{ROOT/p for p in TRANSITIVE_LUA}
    for leaf in ('audit_v4546_ending_display_source_preflight/report.json','audit_v4615_ending_native_latch_timing_checked/report.json'):
        p=ROOT/leaf;proof=json.loads(p.read_text());need(proof['passed'],'Whole original qualified source/hardware proof')
        need(all(sha(q)==h for q,h in proof['inputHashes'].items()),'Every inherited qualified input unchanged')
        files.add(p);files.update(map(Path,proof['inputHashes']))
    report=dict(passed=True,contexts=contexts,actualObserverSourceFaultsRejected=faults,
                hardwareBindingControl=hardware,originalRAMTransportControl=transport,
                generatedCollectorStderrAndModelErrorLocalsAreDistinct=True,
                inputHashes={str(p.resolve()):sha(p)for p in files},
                nativeEndingVideoAcceptance=False,fullPortAcceptance=False,scope=__doc__)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)

if __name__=='__main__':main()
