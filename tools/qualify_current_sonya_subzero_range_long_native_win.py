"""Preserve failed zero-win checker; admit only the actual native earned win."""
from pathlib import Path

if __name__=='__main__':
 source=Path(__file__).with_name('qualify_current_sonya_subzero_range_long.py').read_text()
 old="assert not [r for r in rows['WIN'] if r['slot']=='2' and r['stage']=='1']"
 assert source.count(old)==1
 source=source.replace(old,"wins=[r for r in rows['WIN'] if r['slot']=='2' and r['stage']=='1'];assert len(wins)==1 and wins[0]['pc']=='FF8296B0' and wins[0]['id']=='18' and wins[0]['health']=='0,7'")
 source=source.replace("'audit_current_sonya_subzero_range_long_checked'","'audit_current_sonya_subzero_range_long_native_win_checked'")
 source=source.replace("'subzeroOwnRoundWins':0","'subzeroOwnRoundWins':1,'nativeRoundWin':wins[0]")
 source=source.replace('SubZero clearance failed','one native earned round win, match clearance failed')
 exec(compile(source,__file__+'::native win','exec'),{'__name__':'__main__'})
