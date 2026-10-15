"""Actual compiled mirror-finisher state/fullpalette/activation fault qualification."""
import json
import re
import struct
from pathlib import Path
import run_natural_mirror_complete_audio_v3715 as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v3714_natural_mirror_audio_state_faults_checked'

def run():
    need(not OUT.exists(),'Fresh current mirror fault report')
    report_path=prior.OUT/'report.json';report=json.loads(report_path.read_text())
    need(report['passed']and report['candidate']==prior.NAME and report['naturalMirrorBothCharactersBothSlotsSelectionIndividualDirectCueMixAccepted'],
         'Actual completed new-host mirror audio/state gate')
    contract,contract_sha=prior.physical_contract();cases=[]
    pins={str(report_path):sha(report_path),str(Path(prior.__file__).resolve()):sha(prior.__file__),str(Path(__file__).resolve()):sha(__file__)}
    for case in report['cases']:
        folder=ROOT/case['capture'];path=folder/'run.log';log=path.read_text();guest=(folder/'guest_maincpu.bin').read_bytes()
        need(sha(path)==report['inputHashes'][str(path)]and contract_sha==case['physicalContractSHA256'],'Exact source-qualified runtime contract and actual log')
        fighter,side=case['fighter'],case['side'];positive=contract(log,fighter,side,folder,guest);faults=[]
        data=prior.prior.physical.rows(log)
        action=next(row for tag,row in data if tag=='ACTION')
        def reject(label,mutate):
            changed=mutate(log);need(changed!=log,'Fault actually changes captured metadata')
            try:contract(changed,fighter,side,folder,guest)
            except ValueError as error:faults.append(dict(fault=label,rejectedBy=str(error)))
            else:raise ValueError('Current mirror state fault accepted: '+label)
            need(contract(log,fighter,side,folder,guest)==positive,'Exact positive restored after each actual fault')
        def edit(tag,field,value,match=lambda row:True):
            def mutate(text):
                lines=text.splitlines();changed=False
                for i,line in enumerate(lines):
                    if not line.startswith('MK2_NATURAL_MIRROR_FINISH_V1166_'+tag+' '):continue
                    row=dict(re.findall(r'(\w+)=([^\s]+)',line))
                    if not changed and match(row):
                        lines[i]=re.sub(r'\b'+field+r'=\S+',field+'='+str(value),line,count=1);changed=True
                need(changed,'Actual targeted runtime row exists')
                return '\n'.join(lines)+'\n'
            return mutate
        reject('wrong native health writer',edit('HEALTH','pc','FF807F80'))
        reject('borrowed finisher routine',edit('ACTION','address','FFFAB200'if fighter=='kano'else'FFFAAE00'))
        reject('proxy confirmed roster identity',edit('CONFIRM','roster','1'))
        reject('proxy finisher-body identity',edit('FINISH_STATE','id','1'))
        reject('wrong owned finisher actor',edit('FINISH_STATE','owner','01000000'))
        reject('native choreographic completion age',edit('WRAP','age','232'if fighter=='kano'else'230'))
        reject('wrong full hardware primary palette source',edit('PALETTE','file','mirror_palette_p2.bin',lambda r:r['slot']=='1'))
        reject('native cache overrun falsely accepted',edit('RESULT','cache_errors','1'))
        def remove_native_alt(text):
            return '\n'.join(line for line in text.splitlines()if not(line.startswith('MK2_NATURAL_MIRROR_FINISH_V1166_FLAG_WRITE ')and 'pc=FF895450' in line))+'\n'
        reject('missing original native alternate assignment',remove_native_alt)
        table=0xf56c0 if fighter=='kano'else 0xf5740
        pose=struct.unpack_from('<I',guest,table)[0]
        def omit_owned_pose(text):
            return '\n'.join(line for line in text.splitlines()if not(line.startswith('MK2_NATURAL_MIRROR_FINISH_V1166_FINISH_FIFO ')and
                  'actor='+action['actor']+' 'in line and 'pose='+f'{pose:08X}'+' 'in line))+'\n'
        reject('missing actual required own finisher FIFO group',omit_owned_pose)
        cases.append(dict(fighter=fighter,side=side,rejectedActualFaults=faults,positiveFullHardwarePaletteSamples=positive['fullHardwarePaletteSamples']))
        pins[str(path)]=sha(path)
        for p,h in positive['inputHashes'].items():need(sha(p)==h,'Actual palette/source unchanged');pins[p]=h
    need(len(cases)==4 and sum(len(c['rejectedActualFaults'])for c in cases)==40,'Four true mirror contexts, forty actual qualified faults')
    return dict(passed=True,candidate=prior.NAME,cases=cases,totalQualifiedActualStatePaletteFaults=40,
      fullContractSHA256=contract_sha,inputHashes=pins,newRuntimeOrDiskPCMCopies=0,fullPortAcceptance=False)

if __name__=='__main__':
    report=run();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes')},indent=2))
