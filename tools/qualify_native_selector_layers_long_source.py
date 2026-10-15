"""Correct actual decoded source register, never accept the rejected pointer write."""
import inspect,json,subprocess
from pathlib import Path
import qualify_native_selector_layers_source as original

OUT=original.ROOT/'audit_native_selector_layers_long_source'
STAGE=original.ROOT/'source_native_selector_layers_long'

def main():
    wrong=original.OUT/'selector-layer-helpers.bin'
    decoded=subprocess.run([str(original.ROOT/'mame-mkp/unidasm.exe'),str(wrong),'-arch','tms34010','-basepc',hex(original.addr(original.PHOTO)),'-norawbytes'],capture_output=True,text=True)
    original.need(decoded.returncode==0 and decoded.stdout.count('MOVE   A8,*A8(C0h),1')==2 and 'MOVE   A0,*A8(C0h),1'not in decoded.stdout,'Preserve actual rejected source-register decode')
    main_source=inspect.getsource(original.main)
    original.need(main_source.count('0xb308')==2,'Both independent opcode models corrected')
    main_source=main_source.replace('0xb308','0xb208')
    before='codepath,depth_path,failure,'
    original.need(main_source.count(before)==1,'Exact source proof provenance boundary')
    main_source=main_source.replace(before,"codepath,depth_path,failure,wrong,Path(original.__file__),*(original.STAGE/leaf for leaf in ('midtunit_m.cpp','midtunit.cpp','midtunit.h')),",1)
    before='sourceAdditiveOnly=True,allOtherDriverBytesUnchanged=True'
    original.need(main_source.count(before)==1,'Original rejected opcode recorded in successor proof')
    main_source=main_source.replace(before,'sourceAdditiveOnly=True,allOtherDriverBytesUnchanged=True,earlierActualA8PointerDepthOpcodeRejected=True',1)
    execute_source=inspect.getsource(original.execute)
    original.need(execute_source.count('0xb308')==1,'Actual long-depth model only accepts corrected native source register')
    execute_source=execute_source.replace('0xb308','0xb208')
    scope=dict(vars(original),original=original,OUT=OUT,STAGE=STAGE,wrong=wrong,__file__=__file__)
    exec(compile(execute_source+'\n'+main_source,__file__+'::correct_long_A0_depth_not_A8_pointer','exec'),scope)
    scope['main']()

if __name__=='__main__':main()
