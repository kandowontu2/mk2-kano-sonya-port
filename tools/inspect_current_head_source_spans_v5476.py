"""Read-only distinction between owned corrected death spans and reused space."""
import inspect, struct, textwrap
import verify_rolling_heads_v1014 as original

source=inspect.getsource(original.verify_payload)
first="    artwork=ROOT/'art_native_rolling_heads_v998/sonya-diagonals-135-225-315.png'"
last="    assert bytes(wanted)==payload,'Whole payload differs from independently reconstructed intention'"
assert source.count(first)==source.count(last)==1
function='def rebuild(source):\n'+textwrap.indent(textwrap.dedent(source[source.index(first):source.index(last)]),'    ')+'    return bytes(wanted)\n'
scope=dict(original.__dict__)
exec(compile(function,__file__+'.whole_original1014_reference','exec'),scope)
base=(original.ROOT/'diagnostic_v978_owned_torso_invariant_blood/roms/mk2ks/mk2ks.mdata').read_bytes()
expected=scope['rebuild'](base)
actual=(original.ROOT/'diagnostic_v5219_current_payload_rom_metadata/roms/mk2ks/mk2ks.mdata').read_bytes()
diff=[i for i in range(0x160000,0x180000)if actual[i]!=expected[i]]
count=struct.unpack_from('<I',expected,0x160008)[0]
print(dict(differentBytes=len(diff),first=[hex(i)for i in diff[:12]],last=[hex(i)for i in diff[-12:]],
 headerExact=actual[0x160000:0x160028]==expected[0x160000:0x160028],
 all28DescriptorsExact=actual[0x160400:0x160630]==expected[0x160400:0x160630],
 allOwnedPixelsExact=actual[0x164000:0x164000+count]==expected[0x164000:0x164000+count],pixelBytes=count))
