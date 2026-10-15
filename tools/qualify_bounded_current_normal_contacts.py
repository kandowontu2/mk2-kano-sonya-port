"""Retain basic action/recovery gates; require actual native damage per normal."""
from pathlib import Path
import verify_native_source_sync as sync
prior=Path(__file__).with_name('qualify_bounded_current_basic_controls.py')
source=prior.read_text().replace('audit_bounded_current_basic_controls_checked','audit_bounded_current_normal_contacts_checked')
source=source.replace('audit_bounded_current_basic_controls_{move}','audit_bounded_current_normal_contacts_{move}')
marker="        assert int(rows['FINAL'][0]['frame'])==start+500"
assert source.count(marker)==1
source=source.replace(marker,marker+'''
        contactDamage={}
        for age,name in [(112,'HP'),(176,'LP'),(240,'HK'),(304,'LK')]:
            hits=[r for r in rows.get('HEALTH',[]) if r['slot']==str(3-side) and start+age<=int(r['frame'])<start+age+40 and int(r['after'])<int(r['before'])]
            assert hits and all(r['pc']=='FF836700' for r in hits),(move,side,name,'no native contact')
            contactDamage[name]=sum(int(r['before'])-int(r['after']) for r in hits)
''')
source=source.replace('terminal=terminal,logSHA256=', 'terminal=terminal,normalContactDamage=contactDamage,logSHA256=')
source=source.replace('Not collision coverage for all normals,', 'Four actual standing normal contacts versus Kitana. Not all normal/victim collisions,')
source=source.replace('checkerSHA256=sync.sha(Path(__file__)),','checkerSHA256=sync.sha(Path(__file__)),predecessorSHA256=sync.sha(prior),')
exec(compile(source,__file__,'exec'),dict(__file__=__file__,prior=prior))
