"""Three input-free fields: finite boss-tail/callback/context dependencies."""
import json,struct
import verify_native_source_sync as sync
sync.verify();root=sync.ROOT;base=root/'audit_current_loaded_dispatch_boundaries_preparation'
out=root/'audit_current_loaded_campaign_transitions_preparation';assert not out.exists()
stockpath=root/'mk2/mk2-maincpu.bin';stock=stockpath.read_bytes();assert sync.sha(stockpath)=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'
def u16(at):return struct.unpack_from('<H',stock,(at-0xff800000)//8)[0]
def u32(at):return struct.unpack_from('<I',stock,(at-0xff800000)//8)[0]
def pc(byte):return 0xff800000+byte*8
expected=[]
def add(kind,index,at,width,value):expected.append(dict(kind=kind,index=index,at=at,width=width,value=value))
insertion=((0,5),(0,7),(2,8),(3,9),(1,6),(0,8))
add('operand',0,0xff8a11f0,32,pc(0xf4580))
for order,(first,second)in enumerate(insertion):
    origin=u32(0xff8a1260+order*32);assert origin==0xff8a1320+order*0x100
    destination=pc(0xf4600+order*0x30);add('schedule_pointer',order,pc(0xf4580)+order*32,32,destination)
    old=0
    for slot in range(18):
        if slot<13:
            if slot==first:value=18 if order&1 else 17
            elif slot==second:value=17 if order&1 else 18
            else:value=u16(origin+old*16);old+=1
        else:value=u16(origin+(11+slot-13)*16)
        add('schedule_row',order*18+slot,destination+slot*16,16,value)
    assert old==11
for kind,origin,destination,count in [('damage',0xff8367b0,pc(0xfe100),19),('boss_ai',0xff9b1db0,pc(0xf4400),19),('round_ai',0xff9b2210,pc(0xf4500),19),('special_ai',0xff9b76d0,pc(0xf4800),24)]:
    for index in range(count):value=u32(origin+index*32)if index<17 else (0 if kind=='damage'else 0xff9b20d0 if kind=='boss_ai'else 0xff9b91b0);add(kind,index,destination+index*32,32,value)
for index,(at,value)in enumerate({0xff836750:pc(0xfe100),0xff9b1d60:pc(0xf4400),0xff9b21c0:pc(0xf4500),0xff9b7680:pc(0xf4800)}.items()):add('callback_operand',index,at,32,value)
for index,(at,value)in enumerate({0xff844700:0x270,0xff8448a0:0x270,0xff844720:0x170,0xff844970:0x170,0xff844740:0x190,0xff844ab0:0x190,0xff844760:0x1b0,0xff844b40:0x1b0}.items()):add('ending_context_operand',index,at,16,value)
lines=['local p=manager.machine.devices[":maincpu"].spaces.program','local frame=0','emu.register_frame_done(function()frame=frame+1;if frame~=3 then return end']
for row in expected:lines.append(f"print(string.format('MK2_CAMPAIGN_DEP kind={row['kind']} index={row['index']} at={row['at']:08X} width={row['width']} value=%08X writes=0 inputs=0 assistance=none',p:read_u{row['width']}(0x{row['at']:08x})))")
lines+=['print("MK2_CAMPAIGN_DEP_DONE fields=3 inputs=0 writes=0 assistance=none")','manager.machine:exit()','end)']
lua='\n'.join(lines)+'\n';assert all(x not in lua for x in [':write_',':set_value(',':snapshot('])
out.mkdir();path=out/'tables.lua';path.write_text(lua)
(out/'expected.json').write_text(json.dumps(dict(values=expected,stockSHA256=sync.sha(stockpath),sourceConservationReportSHA256=sync.sha(root/'audit_current_campaign_transition_dependencies_checked/report.json')),indent=2))
runner=(base/'run.ps1').read_text().replace(base.name+'/tables.lua',out.name+'/tables.lua').replace(sync.sha(base/'tables.lua'),sync.sha(path)).replace('audit_current_loaded_dispatch_boundaries_runtime','audit_current_loaded_campaign_transitions_runtime').replace('Elapsed.TotalSeconds -gt 90','Elapsed.TotalSeconds -gt 12')
(out/'run.ps1').write_text(runner)
(out/'source.json').write_text(json.dumps(dict(preparedNotRun=True,LuaSHA256=sync.sha(path),fields=3,inputs=0,guestWrites=0,media=0,readRecords=len(expected),limits='12sec320MiB10MiB',scope='Actualloaded6schedules18rows/boss-tailstockbytes, damage/stockbossAI/round/specialcallbacks and endingcontext operands. No ending force/gameplay/wholefourcampaign/actualsecretlifecycle/heardmix claim.'),indent=2))
print(out,sync.sha(path),len(expected))
