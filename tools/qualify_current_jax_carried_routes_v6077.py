"""Complete6075 carried-victim gate, qualifying the two actual ID-router sites.

The original throw is unchanged except its existing Kano-only height and late
handoff routers. Verify their entire instructions; do not exclude byte ranges.
"""
import inspect,json,struct,traceback
from pathlib import Path
import qualify_current_jax_carried_victims_v6075 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v6078_current_jax_carried_routes_checked'

def source_contract(guest,payload):
 # Full same-source comparison with exactly the two known relocated sites.
 original=bytearray((ROOT/'mk2/mk2-maincpu.bin').read_bytes())
 struct.pack_into('<I',original,prior.native.prior.off(0xff8b7340),0xfffcac00)
 struct.pack_into('<HI',original,prior.native.prior.off(0xff8b7ac0),0xc080,0xfffff380)
 height=(0x098f,0x2000,0xb502,0x01f0,0x0b42,0xffee,0xcb01,0x5621,
         0x09af,0x0004,0xc080,0xcc20,0xff83)
 victim=(0xb500,0x01f0,0x0b40,0xffee,0xcb80,0xf450,0xffff,
         0x09e7,0xf580,0xffff,0xc080,0x7b20,0xff8b,
         0x09e7,0xa830,0xff8d,0x0d5f,0x2710,0xff84,0xc080,0x7b20,0xff8b)
 need(struct.unpack_from('<13H',guest,0xf9580)==height and
      struct.unpack_from('<22H',guest,0xffe70)==victim,
      'Entire actual ID17-only lowering bypass and non17 original Jax late-handoff instruction paths')
 source=inspect.getsource(prior.source_contract)
 before=" original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()"
 need(source.count(before)==1,'One whole original source image comparison')
 source=source.replace(before,' original=qualified_original',1)
 scope=dict(prior.source_contract.__globals__,qualified_original=original)
 exec(compile(source,__file__+'::entire_original_jax_source_with_explicit_native_ID_routes','exec'),scope)
 result=scope['source_contract'](guest,payload)
 result.update(completeNativeKanoOnlyHeightAndLateHandoffRoutersQualified=True)
 return result

def run():
 failed=prior.OUT/'report.json';failure=json.loads(failed.read_text())
 need(not failure['passed']and 'Whole original carried-throw'in failure['error'],
      'Executed original-byte assumption counterexample retained')
 scope=dict(prior.run.__globals__,source_contract=source_contract,__file__=__file__)
 exec(compile(inspect.getsource(prior.run),__file__+'::entire_six_current_living_victim_carries','exec'),scope)
 report=scope['run']()
 for p in(failed,Path(prior.__file__).resolve()):report['inputHashes'][str(p)]=sha(p)
 report.update(retainedWholeOriginalAssumptionFailure=str(failed),scope=__doc__)
 return report

if __name__=='__main__':
 need(not OUT.exists(),'Fresh whole native carried-victim route qualification')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases','actualSemanticFaultsRejected')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
