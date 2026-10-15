"""Reuse full earned-Pit assertions with explicit true identity/slot mappings."""
import argparse
from pathlib import Path
import qualify_current_native_pit_case as base

def main():
    parser=argparse.ArgumentParser();parser.add_argument('winner',choices=['kano','sonya']);parser.add_argument('side',type=int,choices=[1,2]);args=parser.parse_args()
    code=Path(base.__file__).read_text()
    if args.winner=='sonya':
        code=code.replace("r['winner']=='kano'","r['winner']=='sonya'").replace("'17,18'","'18,17'")
        code=code.replace("=='17'","=='TEMP'").replace("=='18'","=='17'").replace("=='TEMP'","=='18'")
    code=code.replace("r['side']=='1'",f"r['side']=='{args.side}'")
    code=code.replace('audit_current_native_pit_kano_p1_runtime',f'audit_current_native_pit_longkick_{args.winner}_p{args.side}_runtime')
    code=code.replace('audit_current_native_pit_kano_p1_checked',f'audit_current_native_pit_longkick_{args.winner}_p{args.side}_checked')
    code=code.replace('audit_current_native_pit_preparation/stage.lua','audit_current_native_pit_longkick_preparation/stage.lua')
    code=code.replace('Physical standingHK/paid-rematch','Physical full-range standingHK/paid-rematch').replace('real KanoP1/SonyaP2',f'real {args.winner}P{args.side} with reciprocal added victim')
    exec(compile(code,str(Path(base.__file__))+' [mapped role]','exec'),{'__name__':'__main__'})

if __name__=='__main__':main()
