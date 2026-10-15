"""Reuse earned-Pit gates on the full-range physical controller successor."""
from pathlib import Path
import qualify_current_native_pit_case as base

def main():
    source=Path(base.__file__).read_text()
    source=source.replace('audit_current_native_pit_kano_p1_runtime','audit_current_native_pit_longkick_kano_p1_runtime')
    source=source.replace('audit_current_native_pit_kano_p1_checked','audit_current_native_pit_longkick_kano_p1_checked')
    source=source.replace('audit_current_native_pit_preparation/stage.lua','audit_current_native_pit_longkick_preparation/stage.lua')
    source=source.replace('Physical standingHK/paid-rematch','Physical full-range standingHK/paid-rematch')
    exec(compile(source,str(Path(base.__file__)),'exec'),{'__name__':'__main__'})

if __name__=='__main__':main()
