"""Actual original CALLA/CALLR origins for all secondary-finisher packets.

Retains the complete previous PCM/channel/voice/selector/queue/DCS gate and
requires new native paired RAM captures. Caller witnesses do not substitute
for whole waveform comparison, independent stock audio or universal coverage.
"""
import copy,json,re,struct,subprocess,traceback
from pathlib import Path
import verify_scorpion_secondary_native_audio_v4700 as previous
import run_scorpion_packet_caller_ram_v4762 as capture
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_v4768_scorpion_packet_callers_checked'
CASES=[]
COUNTS={'FFA13070':1,'FF8CDC10':1,'FFA12B90':24,'FF8CDD90':1,'FF82CB70':1}

def instruction(pc,guest,stock):
    need(pc%16==0 and 0xff800040<=pc<=0xfffffff0,'Actual aligned native caller return in original program')
    offset=(pc-0xff800000)//8
    need(guest[offset-24:offset+8]==stock[offset-24:offset+8],
         'Complete actual caller instruction window unchanged from original ROM')
    absolute=struct.unpack_from('<HI',guest,offset-6)
    relative=struct.unpack_from('<Hh',guest,offset-4)
    if absolute[0]>>4==0x0d5:
        opcode,target=absolute;start=pc-48;kind='CALLA'
    else:
        opcode,delta=relative
        need(opcode>>4==0x0d3,'Actual native stack return has CALLR or CALLA, not arbitrary original-ROM PC')
        target=(pc+(delta<<4))&0xffffffff;start=pc-32;kind='CALLR'
    need(target==0xffa13ba0,'Executed original call reaches actual observed native packet dispatcher')
    return dict(returnPC=f'{pc:08X}',callPC=f'{start:08X}',opcode=f'{opcode:04X}',
                kind=kind,target=f'{target:08X}',originalCallerWindow=guest[offset-24:offset+8].hex().upper())

def semantics():
    ops=ROOT/'mame-mkp/src/devices/cpu/tms34010/34010ops.hxx'
    cpu=ROOT/'mame-mkp/src/devices/cpu/tms34010/tms34010.cpp'
    table=ROOT/'mame-mkp/src/devices/cpu/tms34010/34010tbl.hxx'
    text=ops.read_text();core=cpu.read_text();dispatch=table.read_text()
    need('PUSH(m_pc+0x10);'in text and 'm_pc += (PARAM_WORD_NO_INC()<<4)+0x10;'in text and
         'PUSH(m_pc+0x20);'in text and 'm_pc = PARAM_LONG_NO_INC();'in text,
         'Native CALLR signed-word target/return and CALLA absolute-long target/return semantics')
    need('SP() -= 0x20;'in core and 'WLONG(SP(), data);'in core and '#define SP()          AREG(15)'in core,
         'Native calls push actual32-bit return to real A15 stack observed read-only')
    body=dispatch.split('s_opcode_table[65536 >> 4] =',1)[1].split('};',1)[0]
    entries=re.findall(r'&tms34010_device::(\w+)',body)
    need(len(entries)==4096 and entries[0x0d3]=='callr'and entries[0x0d5]=='calla',
         'Actual native dispatch table decodes executed CALLR/CALLA opcode classes')
    return [ops,cpu,table]

def caller_gate(text,baseline,guest,stock,positive):
    calls=capture.caller_inventory(text,baseline)
    need({pc:sum(r['return_pc']==pc for r in calls)for pc in COUNTS}==COUNTS and
         all(r['return_pc']in COUNTS for r in calls),'Every actual original caller count; no arbitrary or unaccounted return PC')
    need(all(int(r['sp'],16)%16==0 for r in calls),'Actual bit-addressed caller stack alignment')
    instructions={pc:instruction(int(pc,16),guest,stock)for pc in COUNTS}
    selectors=positive['actualSourceBoundSelectors'];extra=positive['actualDirectNativePackets']
    keys=('frame','seconds','writes','assistance','entry','a1','a3','a4','a8','a13')
    def owner(packet):
        matches=[r for r in calls if all(r[k]==packet[k]for k in keys)]
        need(len(matches)==1,'One actual stack witness per exact dispatcher packet')
        return matches[0]
    for binding in selectors:
        call=owner(binding['packet']);route=binding['call']
        need(call['return_pc']=='FFA12B90'and call['id']==route['id']and call['owner']==route['owner'],
             'All24 actual admitted native selectors reach original queue CALLR with genuine task owner/identity')
    direct=[]
    begin=capture.previous.rows(text,'BEGIN')[0];origin=int(begin['origin'])
    for packet,pc,command,age in zip(extra,('FFA13070','FF8CDC10','FF8CDD90','FF82CB70'),(0,0x34,0x35,0x38),(0,2,96,None)):
        call=owner(packet)
        need(call['return_pc']==pc and int(call['a3'],16)==command,
             'Every actual direct native packet bound to its own original caller, not an admitted selector')
        if age is not None:
            need(int(call['frame'])==origin+age and call['id']=='10'and
                 call['a8']==call['owner']==begin['a8'],'Actual Scorpion10 direct effect owns original winner task/phase')
        else:need(call['id']=='-1'and call['a8']==call['owner'],
                  'Original post-finisher ROM task packet is not an added-character proxy')
        direct.append(dict(packet=packet,caller=call,instruction=instructions[pc]))
    return dict(passed=True,actualStackWitnesses=28,originalQueueCallers=24,actualDirectPacketCallers=direct,
                sourceQualifiedOriginalCallInstructions=instructions,directPacketCallerOriginsAccepted=True,
                wholeOriginalPCMChannelsVoiceQueuesDSPRetained=True,stockWholeWaveformReferenceAccepted=False,
                allFinisherVictimAudioAccepted=False,fullPortAcceptance=False)

def run():
    sourcefiles=semantics();guest=capture.state.source.current.expected();stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    previous.source_contract(guest)
    oldproofpath=ROOT/'audit_v4701_scorpion_secondary_native_audio_checked/report.json'
    oldproof=json.loads(oldproofpath.read_text())
    need(oldproof['passed']and oldproof['actualContexts']==4 and oldproof['actualRowFaultsRejected']==72 and
         all(sha(p)==h for p,h in oldproof['inputHashes'].items()),'Every original complete voice/queue/DCS/PCM gate and72real faults retained')
    pins=dict(oldproof['inputHashes'])
    for p in[Path(__file__).resolve(),Path(capture.__file__).resolve(),Path(previous.__file__).resolve(),oldproofpath,*sourcefiles]:
        pins[str(p.resolve())]=sha(p)
    for fighter,side in(('kano',1),('kano',2),('sonya',1),('sonya',2)):
        f=ROOT/f'audit_v4765_scorpion_secondary_{fighter}_p{side}_packet_caller_samples'
        b=ROOT/f'audit_v4765_scorpion_secondary_{fighter}_p{side}_packet_caller_nosamples'
        reportpath=ROOT/f'audit_v4766_scorpion_secondary_{fighter}_p{side}_packet_caller_observed/report.json'
        proof=json.loads(reportpath.read_text());pins[str(reportpath)]=sha(reportpath)
        need(proof['passed']and proof['completeMixedPCMEqualSamplesOnOff']and proof['everyOriginalColdStateAndRGBEventUnchanged']and
             proof['everyNativePacketCallerObserved']and len(proof['actualPacketCallerWitnesses'])==28,
             'Actual new paired native terminal0, full non-silent PCM bytes, true state/RGB and all packet stack witnesses')
        for p,h in proof['inputHashes'].items():need(p not in pins or pins[p]==h,'Consistent executed audio/source inputs');pins[p]=h
        text=(f/'run.log').read_text();baseline=(b/'run.log').read_text()
        meta=json.loads((f/'result.json').read_text());oldmeta=json.loads((b/'result.json').read_text())
        for folder,enabled in((f,'samples'),(b,'nosamples')):
            reference=ROOT/f'audit_v4667_scorpion_secondary_{fighter}_p{side}_audio_{enabled}'
            original=lambda t:[r for r in t.splitlines()if r.startswith(('MK2_MAUDIO_','MK2_BBAUDIO_PCM_DIGEST '))and not r.startswith('MK2_MAUDIO_PACKET_CALLER ')]
            need(original((folder/'run.log').read_text())==original((reference/'run.log').read_text()),
                 'All original native voice/channel/queue/packet/DCS/full PCM digest records byte-exact after added read-only stack observer')
        native=previous.gate(text,baseline,meta,oldmeta,guest,fighter,side)
        positive=caller_gate(text,baseline,guest,stock,native);faults=[]
        first=capture.previous.rows(text,'PACKET_CALLER')[0]
        line=next(l for l in text.splitlines()if l.startswith('MK2_MAUDIO_PACKET_CALLER ')and dict(re.findall(r'(\w+)=([^\s]+)',l))==first)
        def reject(label,t=text,bt=baseline,g=guest):
            try:caller_gate(t,bt,g,stock,native)
            except (ValueError,KeyError,struct.error)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
            else:raise ValueError('Actual native caller fault admitted '+label)
            need(caller_gate(text,baseline,guest,stock,native)==positive,'Whole actual caller positive restored after fault')
        for key,value in(('return_pc','FFF00000'),('return_pc','FF8CDC10'),('sp','00000000'),('sp','010FFF51'),
                          ('a3','00000001'),('id','1'),('owner','01000000'),('frame',str(origin:=int(first['frame'])+1)),
                          ('seconds','0.0'),('writes','1'),('assistance','forced'),('entry','FFA13BB0')):
            changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
            need(n==1 and changed!=line,'Actual caller record non-vacuous fault')
            reject('caller_'+key+'_'+value,text.replace(line,changed,1),baseline.replace(line,changed,1))
        reject('missing_actual_caller',text.replace(line+'\n','',1),baseline.replace(line+'\n','',1))
        reject('duplicate_actual_caller',text.replace(line,line+'\n'+line,1),baseline.replace(line,line+'\n'+line,1))
        for pc in(0xffa13070,0xff8cdc10,0xffa12b90,0xff8cdd90,0xff82cb70):
            item=instruction(pc,guest,stock);offset=(int(item['callPC'],16)-0xff800000)//8
            bad=bytearray(guest);bad[offset]^=1
            reject('actual_original_caller_instruction_'+f'{pc:08X}',g=bytes(bad))
        CASES.append(dict(fighter=fighter,side=side,identity=17 if fighter=='kano'else 18,
          wholeOriginalNativeAudio=native,callerProof=positive,actualCallerFaultsRejected=faults,
          everyOriginalAudioAndPCMRecordUnchanged=True))
        print(f'{fighter}P{side}: all28 actual packet callers source-qualified; {len(faults)} real caller/instruction faults rejected',flush=True)
    need(all(sha(p)==h for p,h in pins.items()),'All original and new executed source/evidence bytes unchanged')
    return dict(passed=True,actualContexts=4,actualNativeStackWitnesses=112,actualDirectOriginalPacketCallers=16,
                actualQueueOriginalPacketCallers=96,directPacketCallerOriginsAccepted=True,
                actualCallerFaultsRejected=sum(len(c['actualCallerFaultsRejected'])for c in CASES),
                wholeOriginal72AudioFaultsRetained=True,everyOriginalAudioAndPCMRecordUnchanged=True,
                cases=CASES,inputHashes=pins,stockWholeWaveformReferenceAccepted=False,
                allFinisherVictimAudioAccepted=False,fullPortAcceptance=False,rawMediaFilesWritten=0,newBuilds=0,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable complete native caller qualification')
    need(all((ROOT/f'audit_v4766_scorpion_secondary_{fighter}_p{side}_packet_caller_observed/report.json').exists()
             for fighter,side in(('kano',1),('kano',2),('sonya',1),('sonya',2))),
         'Require actual paired native terminals before whole caller verification')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completed=CASES,fullPortAcceptance=False)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases','completed')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
