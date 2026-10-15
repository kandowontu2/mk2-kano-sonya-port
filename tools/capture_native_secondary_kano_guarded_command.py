"""Original guarded button command; failed unguarded attempt conserved."""
import code
import inspect
import json
import capture_native_secondary_kano_command_checked as command

command.previous.OUT=command.previous.ROOT/'audit_native_secondary_kano_guarded_command'
command.previous.LUA=command.previous.ROOT/'mk3_native_secondary_kano_guarded_command.lua'

def run():
    previous=command.previous
    path=previous.ROOT/'audit_native_secondary_kano_command_checked/report.json'
    record=json.loads(path.read_text())
    previous.need(record['passed'] and record['transportOnlyAccepted'] and not record['finisherAccepted'] and
                  record['nativeExit']==0 and all(previous.sha(p)==h for p,h in record['inputHashes'].items()),
                  'Actual unguarded physically earned command attempt terminal0, failed action not promoted')
    before='local ca=frame-command'
    after="local ca=frame-command\n   if ca>=6 and ca<14 then press('block')end\n   for _,at in ipairs({4,14,24,34,44,70})do if ca==at then pending[#pending+1]='command_age_'..ca end end"
    wrapper=previous.LUA.read_text()
    previous.need('physical_guarded_command' in wrapper and 'if ca>=6 and ca<14' in wrapper,
                  'Only original physical Block before LP plus passive command-phase rasters')
    source=inspect.getsource(command.run)
    old="('if gap>20 then press(forward)','if gap>65 then press(forward)')]"
    new="('if gap>20 then press(forward)','if gap>65 then press(forward)'),("+repr(before)+','+repr(after)+')]'
    previous.need(source.count(old)==1,'Unique explicit fourth physical/passive replacement')
    source=source.replace(old,new)
    literal="old in wrapper and new in wrapper"
    checked="old in wrapper and (new in wrapper or new.replace(chr(10),chr(92)+'n') in wrapper)"
    previous.need(source.count(literal)==1,'Unique exact Lua newline-literal provenance check')
    source=source.replace(literal,checked)
    oldpins="ROOT/'audit_native_secondary_kano_raster_checked/report.json']"
    newpins="ROOT/'audit_native_secondary_kano_raster_checked/report.json', ROOT/'audit_native_secondary_kano_command_checked/report.json', ROOT/'tools/capture_native_secondary_kano_command_checked.py']"
    previous.need(source.count(oldpins)==1,'Unique actual failed command provenance extension')
    source=source.replace(oldpins,newpins)
    scope=dict(vars(command),__file__=__file__)
    exec(compile(source,__file__+'::physical_guard_only','exec'),scope)
    return scope['run']()

if __name__=='__main__':
    capture=run()
    code.interact(banner='Original guarded command terminal; original raster buffers in RAM.',local=dict(capture=capture))
