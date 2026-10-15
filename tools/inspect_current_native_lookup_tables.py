"""Read-only whole-stock direct live-ID lookup audit; no reachability inference."""
import re
import struct
import inspect_native_smoke_callers as disasm
import native_ai_response_context as current

def inspect():
    guest = current.expected()
    lines = disasm.disassemble()
    result = []
    for index,line in enumerate(lines):
        if not re.search(r'\bCALLA\s+FF83B7F0h$',line,re.I):
            continue
        call = int(line.split(':',1)[0],16)
        # A stock call may already be replaced by an owned-character router.
        # Do not report the preceding MOVI as a live current lookup in that case.
        call_offset = (call-0xff800000)//8
        if struct.unpack_from('<HI',guest,call_offset) != (0x0d5f,0xff83b7f0):
            continue
        for previous in reversed(lines[max(0,index-5):index]):
            match = re.fullmatch(r'([0-9a-f]+): MOVI\s+([0-9a-f]+)h,A0',previous,re.I)
            if not match:
                continue
            site,stock_table = [int(value,16) for value in match.groups()]
            offset = (site-0xff800000)//8
            if struct.unpack_from('<H',guest,offset)[0] != 0x09e0:
                break
            table = struct.unpack_from('<I',guest,offset+2)[0]
            if not 0xff800000 <= table <= 0xffffff00:
                break
            values = struct.unpack_from('<19I',guest,(table-0xff800000)//8)
            result.append(dict(call=f'{call:08X}',operand=f'{site+16:08X}',
                stockTable=f'{stock_table:08X}',currentTable=f'{table:08X}',
                relocated=stock_table!=table, rows17and18=[f'{v:08X}' for v in values[17:]]))
            break
    return result

if __name__=='__main__':
    import json
    print(json.dumps(dict(staticOnly=True, directImmediateTables=inspect()),indent=2))
