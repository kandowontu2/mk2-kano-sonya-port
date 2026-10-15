"""Partition expensive effect pixels without omitting a native action field."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_p2_jax_effect_pixels_preparation'
    out=sync.ROOT/'audit_bounded_p2_kano_jax_effect_windows_preparation';assert not out.exists();out.mkdir()
    original=(old/'prepared_observer.lua').read_text()
    reports=[]
    for label,first,last in [('opening',1,100),('completion',101,188)]:
        text=original
        needle='frame-ready>=1 and frame-ready<=188';assert text.count(needle)==2
        text=text.replace(needle,f'frame-ready>={first} and frame-ready<={last}')
        needle=f'((frame-ready)%8~=0 and not(frame-ready>={first} and frame-ready<={last}))'
        assert text.count(needle)==1
        text=text.replace(needle,f'(frame-ready<{first} or frame-ready>{last})')
        needle='frame-ready<1 or frame-ready>188';assert text.count(needle)==1
        text=text.replace(needle,f'frame-ready<{first} or frame-ready>{last}')
        target=out/f'{label}.lua';target.write_text(text)
        runner=(old/'run_kano.ps1').read_text().replace(old.name+'/prepared_observer.lua',out.name+'/'+target.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace('audit_bounded_p2_kano_jax_effect_pixels_runtime',f'audit_bounded_p2_kano_jax_effect_{label}_runtime')
        (out/f'run_{label}.ps1').write_text(runner)
        reports.append(dict(label=label,firstAge=first,lastAge=last,observerSha256=sync.sha(target)))
    assert set(range(1,101))|set(range(101,189))==set(range(1,189))
    (out/'report.json').write_text(json.dumps(dict(prepared=True,windows=reports,acceptance=False),indent=2)+'\n')

if __name__=='__main__':main()
