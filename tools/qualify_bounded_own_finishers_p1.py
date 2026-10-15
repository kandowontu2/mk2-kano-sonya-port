"""Retain original earned-damage/completion and effective fault gates."""
from pathlib import Path
import verify_native_source_sync as sync
prior=Path(__file__).with_name('qualify_bounded_stock_head_finisher.py')
source=prior.read_text()
for before,after in [
 ('audit_bounded_stock_head_finisher_checked','audit_bounded_own_finishers_p1_checked'),
 ("a['address']=='FF8CB4A0'","a['address']=={'kano':'FFFAAE00','sonya':'FFFAB200'}[fighter]"),
 ("x['own'].split(':')[-1]=='3' and x['victim'].split(':')[-1]==str(ident)","x['own'].split(':')[-1]==str(ident) and x['victim'].split(':')[-1]=='4'"),
 ("f'audit_bounded_{fighter}_stock_head_finisher_runtime'","f'audit_bounded_own_finisher_dispatch_{fighter}_p1_runtime'"),
 ("r['victim']==fighter and r['side']=='1' and r['killer']=='baraka'","r['victim']=='kitana' and r['side']=='2' and r['killer']==fighter")]:
    assert before in source
    source=source.replace(before,after)
source=source.replace('checkerSha256=sync.sha(Path(__file__)),','checkerSha256=sync.sha(Path(__file__)),predecessorSHA256=sync.sha(prior),scope=\'Two P1 owned primary finishers versus Kitana, genuine322damage/two wins/native own action/common wrap and120fields followthrough; no full raster/audio/all victims/secondary finishers acceptance\',')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,__name__='__main__',prior=prior))
