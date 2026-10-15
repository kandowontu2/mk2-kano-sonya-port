"""Real muted native Kano roll and Sonya dual Bicycle: whole silent output.

This proves suppression in the observed native mute windows, not audible Kano,
all mute interruptions, or full port acceptance. Evidence faults never touch
the emulator. Raw audio remains RAM-only except one tiny lossless zero carrier.
"""
import gzip
import hashlib
import json
import struct
import subprocess
import sys
from decimal import Decimal
from pathlib import Path
import numpy as np
import native_ai_response_context as current
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha

def rows(text,tag):
    found=[]
    for line in text.splitlines():
        if line.startswith(tag+' '):
            pairs=re.findall(r'(\w+)=([^\s]+)',line);row=dict(pairs)
            need(len(row)==len(pairs),'Unique entire native source metadata')
            found.append(row)
    return found

import re

def gate(c):
    sounds=rows(c['text'],'MK2_ATTRACT_SOUND')
    need([r['word'] for r in sounds]==['6B03','6B01','6B02'], 'Actual complete muted Kano roll and dual Bicycle marker history')
    for r,(identity,action,pc) in zip(sounds,[(17,523,'FFFFDEC0'),(18,516,'FFF9A4C0'),(18,516,'FFF9A520')]):
        need(r['pc']==pc and r['mode']=='1' and r['mute']=='1' and r['writes']=='0' and r['assistance']=='none' and
            r['p1_roster']==r['p1_id']==str(identity) and r['p1_action']==str(action) and
            r['a8']==r['p1_actor']==r['p1_owner'] and r['a13']==r['p1_main'] and 0<int(r['p1_hp'])<=161,
            'Every actual suppressed launch belongs to a live true native CPU actor/Main/signature action')
    pcm=c['pcm'];dac=c['dac'];headers=c['dacHeaders']
    need(len(pcm)==len(dac)==len(headers)==514, 'All actual PCM and original native DAC callbacks')
    for index,(record,raw,h) in enumerate(zip(pcm,dac,headers),1):
        p=record['header'];data=record['pixels']
        need(p['frame']==h['frame'] and p['seconds']==h['seconds'] and h['index']==str(index) and
            len(data)==3840 and hashlib.sha256(data).hexdigest().upper()==p['sha256'] and data==bytes(3840),
            'Every complete actual stereo960-frame output is exactly silent, no omitted first or tail')
        need(h['writes']=='0' and h['assistance']=='none' and h['prefix']=='4' and h['ring']=='32768' and
            h['element_bytes']=='4' and h['consumed']=='625' and len(raw)==629*4 and
            hashlib.sha256(raw).hexdigest().upper()==h['sha256'] and raw==bytes(629*4) and
            (int(h['current_out'])-int(h['previous_out']))%32768==625 and
            Decimal(h['seconds'])-Decimal(h['previous_seconds'])==Decimal('.02'),
            'Entire original native DAC ring interval and prefix are silent and accounted')
    channel_rows=rows(c['text'],'MK2_TOMB_MIX_CHANNEL')
    need(len(channel_rows)==514*14 and {(int(r['index']),int(r['channel'])) for r in channel_rows}==
        {(index,ch) for index in range(1,515) for ch in range(14)}, 'All fourteen channels at every actual speaker callback')
    for r in channel_rows:
        h=pcm[int(r['index'])-1]['header']
        need(r['frame']==h['frame'] and r['seconds']==h['seconds'] and r['writes']=='0' and r['assistance']=='none' and
            r['sample']=='4294967295' and r['length']=='0' and float(r['position'])==0 and
            r['bits']==struct.pack('<d',0.0).hex().upper() and r['loop']==r['paused']=='0',
            'Every actual source remains entirely unstarted, including names, effects and both physical startup slots')
    inputs=rows(c['text'],'MK2_ATTRACT_INPUT')
    need([(int(r['frame']),r['value'],r['button']) for r in inputs]==
        [(f,'1','HighPunch') for f in range(481,485)]+[(485,'0','HighPunch')], 'Only the actual ordinary configured acknowledgement and release')
    dip=rows(c['text'],'MK2_ATTRACT_DIP');policy=rows(c['text'],'MK2_ATTRACT_MUTE_POLICY')
    need(len(dip)==1 and dip[0]['mask']==dip[0]['default']==dip[0]['configured']=='1000' and dip[0]['actual']=='FC7D',
        'Actual default Attract Sound On setting; no forced guest mute flag')
    need(any(r['pc']=='FF843960' and r['value']=='1' and Decimal(r['seconds'])<Decimal(sounds[0]['seconds']) for r in policy),
        'Original native late-sequence mute policy actually precedes the suppressed launches')
    need(not rows(c['text'],'MK2_ATTRACT_RESET') and not rows(c['text'],'MK2_ATTRACT_ERROR_ENTRY'), 'No reset or executed native error in the full run')
    return dict(passed=True,comparedStereoFrames=514*960,preciseChannelStates=len(channel_rows),
        silentNativeDACSamples=514*625,actualSuppressedMarkers=sounds,
        audibleKanoAttractRollAccepted=False,allMuteInterruptionsAccepted=False,fullPortAcceptance=False)

def finish(c):
    folder=c['folder'];output=folder/'native_muted_launch_sources.json'
    need(not output.exists() and not native.census() and c['terminal']['nativeExit']==0 and c['guest']==current.expected(),
        'Same actual terminal native run; whole independently compiled guest identity unchanged')
    report=json.loads((folder/'report.json').read_text())
    need(report['passed'] and report['requestedConfigurationAccepted'], 'Actual correct physical configuration and error-free terminal')
    positive=gate(c);faults=[]
    for label,index in [('first full speaker buffer',0),('last full speaker buffer',-1)]:
        broken=list(c['pcm']);record=dict(broken[index]);data=bytearray(record['pixels']);data[0]^=1
        record['pixels']=bytes(data);broken[index]=record
        try:gate(dict(c,pcm=broken))
        except ValueError as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Nonzero/mismatched native speaker buffer admitted')
    altered=list(c['dac']);raw=bytearray(altered[0]);raw[0]^=1;altered[0]=bytes(raw)
    try:gate(dict(c,dac=altered))
    except ValueError as error:faults.append(dict(fault='actual native DAC buffer changed',rejectedBy=str(error)))
    else:raise ValueError('Bad actual DAC source admitted')
    tests=[('last stereo buffer omitted',dict(c,pcm=c['pcm'][:-1]))]
    first=next(line for line in c['text'].splitlines() if line.startswith('MK2_TOMB_MIX_CHANNEL '))
    tests.append(('active channel source',dict(c,text=c['text'].replace(first,re.sub(r'\blength=\S+','length=55465',first,count=1),1))))
    marker=next(line for line in c['text'].splitlines() if line.startswith('MK2_ATTRACT_SOUND '))
    for key,value in [('p1_id','1'),('p1_owner','00000000'),('mute','0'),('pc','FFA13C90')]:
        tests.append(('real launch '+key+' altered',dict(c,text=c['text'].replace(marker,
            re.sub(r'\b'+key+r'=\S+',key+'='+value,marker,count=1),1))))
    for label,bad in tests:
        try:gate(bad)
        except ValueError as error:faults.append(dict(fault=label,rejectedBy=str(error)))
        else:raise ValueError('Invalid actual native mute evidence admitted: '+label)
    need(gate(c)==positive,'Entire actual positive restored after all evidence counterexamples')
    for name,buffers in [('native_silent_pcm.pcm.gz',[r['pixels'] for r in c['pcm']]),('native_silent_dac.f32.gz',c['dac'])]:
        path=folder/name;need(not path.exists(),'One tiny compressed original silence carrier, never raw media copies')
        with gzip.open(path,'wb') as f:
            for data in buffers:f.write(data)
        with gzip.open(path,'rb') as f:need(all(f.read(len(data))==data for data in buffers) and not f.read(), 'Every actual original zero byte preserved')
    sources={}
    for module in tuple(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename and Path(filename).resolve().is_relative_to(ROOT/'tools'):
            path=Path(filename).resolve();sources[str(path)]=dict(sha256=sha(path),text=path.read_text())
    with gzip.open(folder/'executed_muted_qualification_sources.json.gz','wt',encoding='utf-8') as f:json.dump(sources,f)
    result=dict(**positive,nativeTerminal=c['terminal'],faultsRejected=faults,
        entirePCMHeaders=[r['header'] for r in c['pcm']],entireDACHeaders=c['dacHeaders'],
        previousGoalTurnClassification='progress: full current selection/ladder/match and 32 special activation/recovery cycles',
        thisGoalTurnClassification='progress: actual native Kano roll and both Sonya Bicycle sources remain suppressed under original late-demo mute; all514 complete speaker/DAC buffers and7196 precise source-channel states checked',
        originalRemainingScope=json.loads((ROOT/'audit_native_dual_roll_progress_storage/report.json').read_text())['remaining'],
        nextAction='Audible natural Kano demo launch remains unproved; focus a fresh physical phase yielding an early own demo, then final scene-boundary, integration and matching CMD/ZIP checks.',
        goalStatus='active',publicPlayableChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        inputHashes={**report['inputHashes'],str(Path(__file__).resolve()):sha(__file__)})
    output.write_text(json.dumps(result,indent=2)+'\n')
    storage=[]
    for path in [p for p in folder.rglob('*') if p.is_file()]:
        need(path.resolve().is_relative_to(ROOT) and not path.is_symlink(),'Exact bounded original proof leaf')
        digest=sha(path)
        subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True,check=True)
        need(sha(path)==digest,'All original source/evidence bytes unchanged')
        storage.append(dict(path=str(path),sha256=digest,allocatedBytes=allocated(path)))
    (folder/'storage_receipt.json').write_text(json.dumps(dict(passed=True,exactFiles=storage,newBuilds=0,newROMCopies=0,newZIPs=0),indent=2)+'\n')
    print(json.dumps(dict(passed=True,stereoFrames=positive['comparedStereoFrames'],preciseChannels=positive['preciseChannelStates'],
        effectiveFaults=len(faults),allocatedEvidenceBytes=sum(r['allocatedBytes'] for r in storage),audibleKanoAccepted=False)),flush=True)
    return result
