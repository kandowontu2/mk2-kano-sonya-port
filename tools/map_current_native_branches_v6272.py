"""Current constructor's final air-throw consumer and close-action entry.

Keep the failed6271 static assumption. The stock air table is selected inside
the final Kano/Jax router, not directly by the displaced original MOVI.
Choke's action is FFF91400; its parser FFF91000 is a different entry.
No native game or playable byte is changed by this audit correction.
"""
from pathlib import Path
import struct
import map_current_native_branches_v6270 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v6273_current_native_branch_inventory'

def air_router_gate(raw):
 r=0xf80d0;a=prior.addr
 words=(0xb500,0x01f0,0x0b40,0xffee,0xcb80,a(r+0x1a)&65535,a(r+0x1a)>>16,
        0x09e0,a(0xf8080)&65535,a(0xf8080)>>16,0xc080,0x7430,0xff8b,
        0x09e0,a(0xffdc0)&65535,a(0xffdc0)>>16,0xc080,0x7430,0xff8b)
 need(raw[r:r+38]==struct.pack('<19H',*words),'Every final native attacker-ID Kano/Jax air-offset router opcode and target')
 need(struct.unpack_from('<H',raw,prior.at(0xff8b7400))[0]==0xc080 and prior.u32(raw,prior.at(0xff8b7410))==a(r),'Actual original consumer jumps to final actor-specific router')
 need(struct.unpack_from('<38h',raw,0xf8080)==(41,-3)*19,'Complete compiled-source Kano catch offset table for every victim ID')

def run():
 failed=ROOT/'audit_v6271_current_native_branch_inventory/failure.json'
 need(failed.exists()and not prior.json.loads(failed.read_text())['passed'],'Keep actual static-consumer failure')
 source=Path(prior.__file__).read_text()
 changes={
  "OUT=ROOT/'audit_v6271_current_native_branch_inventory'":"OUT=ROOT/'audit_v6273_current_native_branch_inventory'",
  "0xff8b7d20,(0xff8b7410,),17,None":"0xff8b7d20,(addr(0xf80d0+0x1c),),17,None",
  "('kano',0xf78c0,0xf2200,'choke')":"('kano',0xf78c0,0xf2280,'choke')",
  'tables=[table_gate(guest,stock,spec)for spec in specs];ladders=ladder_gate(guest,stock);branches=ai_gate(guest)':
   'air_router_gate(guest);tables=[table_gate(guest,stock,spec)for spec in specs];ladders=ladder_gate(guest,stock);branches=ai_gate(guest)',
  "for branch in branches:\n  altered=bytearray(guest)":
   "for label,offset in (('air native original consumer',at(0xff8b7410)),('air router stock victim table',0xf80d0+0x1c),('air router Kano victim table',0xf8080)):\n  altered=bytearray(guest);altered[offset]^=1;reject(label,air_router_gate,altered)\n for branch in branches:\n  altered=bytearray(guest)",
  'PARENT,proofpath,SOURCE,stockpath,Path(__file__).resolve(),Path(current.__file__)':
   'PARENT,proofpath,SOURCE,stockpath,Path(prior.__file__),failed,Path(__file__).resolve(),Path(current.__file__)',
 }
 for before,after in changes.items():
  need(source.count(before)==1,'Exact final-source static inventory correction: '+before[:100]);source=source.replace(before,after,1)
 scope=dict(prior.__dict__,__name__='qualified_current_branch_inventory',__file__=__file__,prior=prior,failed=failed,air_router_gate=air_router_gate)
 exec(compile(source,__file__+'::whole_original_inventory_final_native_consumers','exec'),scope)
 scope['run']()

if __name__=='__main__':run()
