"""Run exact response faults from three retained completed native logs."""
import gzip
import check_cross_continue_controls as controls


if __name__=='__main__':
    for fighter,side,target in (('kano',1,'sonya'),('kano',2,'sonya'),('sonya',1,'kano')):
        folder=controls.ROOT/f'audit_cross_continue_adaptive_{fighter}_p{side}_to_{target}'
        with gzip.open(folder/'run.log.gz','rt',encoding='utf-8')as f:text=f.read()
        controls.check(folder,text,fighter,side,target)
