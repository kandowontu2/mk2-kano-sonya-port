"""Read-only stock TMS code/call sites; disassembly remains in memory."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def disassemble():
    result = subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'), str(ROOT/'mk2/mk2-maincpu.bin'),
                             '-arch', 'tms34010', '-basepc', '0xff800000', '-count', '8388608', '-norawbytes'],
                            capture_output=True, text=True, check=True)
    return result.stdout.splitlines()


if __name__ == '__main__':
    lines = disassemble()
    for index, line in enumerate(lines):
        if any(target.upper() in line.split(':', 1)[-1].upper() for target in (sys.argv[1:] or ('FFA0BA10H', 'FFA0B880H'))):
            print('\n'.join(lines[max(0,index-12):index+8]))
