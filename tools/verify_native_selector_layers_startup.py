"""Verify all native initialized windows for the CSS-only layering successor."""
import code,inspect,json,struct,traceback
from pathlib import Path
import verify_native_shang_drain_startup as initial
import verify_native_shang_drain_anchors_startup as predecessor

ROOT=initial.ROOT
NAME='diagnostic_native_selector_layers_long'
OUT=ROOT/'audit_native_selector_layers_startup'
BUILD_GUARD=ROOT/'audit_native_selector_layers_long_source/report.json'
RAM={}

def expected(folder):
    wanted=predecessor.expected(folder)
    high=bytearray(wanted['high'])
    address=lambda b:0xff800000+b*8
    photo,number=0xf95a0,0xf95f0
    initial.need(high[photo:0xf9600]==b'\xff'*96,'Whole reviewed helper reservation unused')
    words=(0x0b65,0xd7ff,0,0xca80,address(photo+24)&65535,address(photo+24)>>16,
           0x0b65,0xd6ff,0,0xcb80,address(photo+32)&65535,address(photo+32)>>16,
           0x09c0,0x51,0xb208,0xc0,0xc080,0xf610,0xff83)
    struct.pack_into('<19H',high,photo,*words)
    struct.pack_into('<7H',high,number,0x09c0,0x52,0xb208,0xc0,0xc080,0xf610,0xff83)
    for operand,target in ((0xff894020,photo),(0xff8965e0,number)):
        at=(operand-0xff800000)//8
        initial.need(struct.unpack_from('<I',high,at)[0]==0xff83f610,'Original CSS-only sorted registration target')
        struct.pack_into('<I',high,at,address(target))
    initial.need(sum(a!=b for a,b in zip(wanted['high'],high))==52,'Exactly52 CSS layer initializer bytes changed')
    wanted['high']=bytes(high)
    proof=json.loads(BUILD_GUARD.read_text())
    initial.need({k:initial.digest(v)for k,v in wanted.items()}==dict(high=proof['proposedGuestSHA256'],owned=proof['proposedOwnedSHA256'],graphics=proof['proposedNewGraphicsSHA256']),'All whole independent models equal source-qualified contract')
    return wanted

def run():
    source=inspect.getsource(initial.run)
    changes=(("guard['bothQualifiedFragmentsApplied'] and not guard['nativeRepairAccepted']",
              "guard['sourceOnlyAccepted'] and not guard['nativeRuntimeAccepted']"),
             ("meta['prior_candidate'] == old.NAME", "meta['prior_candidate'] == 'diagnostic_native_shang_drain_anchors'"),
             ("guard['expectedOwnedWindowSHA256']","guard['proposedOwnedSHA256']"),
             ("guard['expectedGraphicsReservationSHA256']","guard['proposedNewGraphicsSHA256']"),
             ('paths = [Path(__file__), LUA, meta_path, BUILD_GUARD,',
              'paths = [Path(__file__), Path(initial.__file__), Path(predecessor.__file__), LUA, meta_path, BUILD_GUARD,'))
    for before,after in changes:
        initial.need(source.count(before)==1,'Exact original full native startup boundary '+before)
        source=source.replace(before,after,1)
    scope=dict(vars(initial),initial=initial,predecessor=predecessor,expected=expected,NAME=NAME,OUT=OUT,BUILD_GUARD=BUILD_GUARD,RAM=RAM,__file__=__file__)
    exec(compile(source,__file__+'::whole_actual_native_css_layer_windows','exec'),scope)
    return scope['run']()

if __name__=='__main__':
    try:run()
    except Exception as error:
        failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
        if OUT.exists():
            path=OUT/'failure.json';initial.need(not path.exists(),'Preserve actual native startup failure')
            path.write_text(json.dumps(failure,indent=2)+'\n')
        print(json.dumps(failure,indent=2),flush=True)
        code.interact(banner='Same original startup bytes/handle retained; do not restart on timeout.',local=dict(RAM=RAM))
