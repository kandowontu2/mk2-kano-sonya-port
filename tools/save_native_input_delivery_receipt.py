"""Retain the real input-address correction without claiming an interruption.

The existing full recovery qualifier is executed unchanged and its actual
failure retained. A bit-delivery pass is separate from gameplay acceptance.
Raw guest/GFX/PCM/DAC/RGB buffers stay in the original live RAM carrier.
"""
import json,re,subprocess,traceback
from pathlib import Path
import qualify_ground_input_delivery_v6712 as delivery
ROOT,need,sha=delivery.ROOT,delivery.need,delivery.sha

def save(carrier):
    out=ROOT/'audit_native_input_delivery_address_correction'
    need(not out.exists(), 'Fresh immutable correction receipt')
    need(carrier['terminal']['nativeExit']==0 and not carrier['decodeErrors'], 'Actual retained terminal')
    proof=delivery.delivered(carrier['text'])
    faults=[]
    for tag in ('MK2_INTERRUPT_IO','MK2_INTERRUPT_LOW_IO'):
        line=next(s for s in carrier['text'].splitlines() if s.startswith(tag+' '))
        value=re.search(r'\bvalue=(\w+)',line)[1]
        for label,bad in [('changed real input bit',carrier['text'].replace(line,line.replace('value='+value,'value='+format(int(value,16)^1,'04X'),1),1)),
                          ('omitted native IRQ field',carrier['text'].replace(line+'\n','',1))]:
            try: delivery.delivered(bad)
            except ValueError as error: faults.append(dict(tag=tag,fault=label,rejectedBy=str(error)))
            else: raise ValueError('Actual input fault admitted')
    try: delivery.qualify(carrier)
    except ValueError as error:
        rejection=dict(passed=False,error=str(error),traceback=traceback.format_exc(),executedSource=str(Path(delivery.__file__).resolve()),sourceSHA256=sha(delivery.__file__))
    else: raise ValueError('Expected existing strict follow-up rejection changed')
    need(rejection['error']=='Post-special movement, jump and native punch actually activate', 'Exact actual strict standing-jab assumption remains rejected')
    compiled=ROOT/delivery.model.current.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
    source=compiled.read_text()
    for statement in ('map(0x01600000, 0x0160000f).portr("IN0");','map(0x01600020, 0x0160002f).portr("IN2");',
                      'map(0x01d00000, 0x01d0001f).r(FUNC(midtunit_state::midtunit_sound_state_r));'):
        need(source.count(statement)==1, 'Actual compiled address map')
    pins=dict(carrier['pins'])
    for p in (Path(__file__),Path(delivery.__file__),compiled,ROOT/'mame-mkp/src/emu/ioport.cpp',*carrier['folder'].rglob('*')):
        if p.is_file(): pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()), 'Executed candidate and evidence unchanged')
    report=dict(passed=True,scope='Complete IN0/IN2 bit delivery only; not an accepted whole recovery or interruption test',
                nativeTerminal=carrier['terminal'],nativeInputDelivery=proof,actualInputFaultsRejected=faults,
                unchangedWholeRecoveryQualifier=rejection,inputHashes=pins,
                priorObserverCorrection='01D00000 is DCS status, not IN0. Prior Square proofs did not accept bit isolation; their input-read descriptions were incorrect.',
                priorAcceptedSquareCoreEvidenceUnchanged=True,wholeRecoveryAcceptance=False,gameplayInterruptionAccepted=False,
                sourceWaveformAccepted=False,fullPortAcceptance=False,goalStatus='active',newBuilds=0,newROMCopies=0,newZIPs=0,newRawMedia=0)
    out.mkdir()
    p=out/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
    need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Lossless exact receipt')
    print(json.dumps(dict(passed=True,nativeInputDelivery=proof,actualFaults=len(faults),wholeRecoveryAccepted=False)),flush=True)
    return report
