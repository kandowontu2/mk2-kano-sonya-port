"""Preserve original syntax failure; parenthesize Python boolean operands."""
from pathlib import Path

def main():
    original=Path(__file__).with_name('qualify_bounded_twohuman_counter_ports.py')
    source=original.read_text()
    for before,after in {
        '==not (9<=age<=20)':'==(not (9<=age<=20))',
        '==not (15<=age<=18)':'==(not (15<=age<=18))',
        '==not (1<=age<=8)':'==(not (1<=age<=8))',
        "'port_admission_check.json'":"'port_admission_boolean_check.json'",
    }.items():
        assert source.count(before)==1;source=source.replace(before,after)
    namespace={'__name__':'bounded_port_checker','__file__':__file__}
    exec(compile(source,__file__+'::boolean_operands','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
