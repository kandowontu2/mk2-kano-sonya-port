from pathlib import Path
source=Path(__file__).with_name('audit_current_sonya_p1_kintaro_low_airkick_witness.py').read_text()
source=source.replace('audit_current_sonya_p1_kintaro_low_airkick','audit_current_sonya_p1_kintaro_deferred_observers').replace('8830F9E2E7923869B3620A720B75B01814536F945D6D42E128B3A7A7FCA8417E','0EAC9DDCE9464F17C186E3A9B809F057B43E7B63C3146B987C83009A7BD969C7')
exec(compile(source,__file__,'exec'))
