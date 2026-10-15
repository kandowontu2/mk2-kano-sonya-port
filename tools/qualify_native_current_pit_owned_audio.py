"""Current native movie/Main owners and whole original queue/RNG algorithm.

Add to the complete current19 waveform, never replace it. Reuse all36 actual
RNG/queue faults; true opposite17/18 voice selectors replace stock8 context.
"""
import gzip
import inspect
import json
import re
import struct
import textwrap
from decimal import Decimal
from pathlib import Path
import run_native_current_cross_pit_19_owned_audio as host
import qualify_current_pit_queue_rng_boundary_v5969 as original_rng

ROOT, need, sha, once = host.ROOT, host.need, host.sha, host.once


def rng_functions():
    body=original_rng.gate.source
    before="origin=int(begin['frame']);identity=17 if fighter=='kano'else 18"
    body=once(body,before,before+';victim=35-identity')
    body=once(body,"[r['base']for r in selectors if r['kind']=='VOICE']==[0xcb,0xcc]",
        "[r['base']for r in selectors if r['kind']=='VOICE']==([0xcd,0xce]if victim==18 else[0xcb,0xcc])")
    body=once(body,'actualOriginalVictimID=8','actualOriginalVictimID=victim')
    scope=dict(original_rng.gate.__globals__,__file__=__file__)
    exec(compile(body,__file__+'::whole_original_native_RNG_priority_true_cross_voice','exec'),scope)
    gate=scope['gate']
    start=original_rng.run.source.index('   good=gate(')
    stop=original_rng.run.source.index('   good.update(actualFaultsRejected=',start)
    faults='def qualify_rng(text,guest,stock,fighter,side):\n'+textwrap.indent(textwrap.dedent(original_rng.run.source[start:stop]),'    ')
    faults+="    good['actualFaultsRejected']=faults\n    return good\n"
    namespace=dict(original_rng.run.__globals__,__file__=__file__,gate=gate)
    exec(compile(faults,__file__+'::entire_original36_actual_RNG_queue_faults','exec'),namespace)
    return namespace['qualify_rng'],body,faults


def owner_gate(text,guest,fighter,side):
    rs=host.original.pit.inventory(text)
    get=lambda n:rs.get(n,[])
    pit=lambda n:get('MK2_PIT140_'+n)
    audio=lambda n:get('MK2_MAUDIO_'+n)
    own=17 if fighter=='kano'else 18;victim=35-own
    need(len(pit('BEGIN'))==len(pit('RESULT'))==len(pit('CONSTRUCTOR'))==1, 'One actual own admission/constructor/terminal')
    begin,end,ctor=pit('BEGIN')[0],pit('RESULT')[0],pit('CONSTRUCTOR')[0]
    first=get('MK2_STAGE_FIELD')[0];origin=int(begin['frame'])
    need(begin['id']==first['id']==str(own) and first['victim_id']==str(victim) and
         begin['actor']==first['own'] and begin['main']==first['main'] and begin['arena']=='6' and
         end['origin']==str(origin) and int(end['frame'])==origin+1101 and end['raw_files']=='0', 'True selected actors and full original1101 native terminal')
    need(ctor['a0']==f'{victim:08X}' and ctor['a11']==first['victim'] and ctor['a8']=='00000000' and ctor['mode']=='9', 'Original constructor carries actual defeated physical actor and true ID')
    look,draw,fields=pit('LOOKUP'),pit('DRAW'),pit('FIELD')
    need(len(look)==2 and len(draw)==22, 'Own synchronous preload, twenty falling draws, impact and both lookups')
    actor,main=look[0]['actor'],look[0]['main'];enter,impact=int(look[0]['frame']),int(look[1]['frame'])
    need(actor not in(first['own'],first['victim']) and main==ctor['a13'] and enter==int(ctor['frame']) and impact==enter+59, 'Separate native cinematic actor/Main ancestry and exact original fall cadence')
    seq=0xff181000+(victim-17)*0x200;group=0xff182000+(victim-17)*384
    off=lambda a:(a-0xff800000)//8
    need(struct.unpack_from('<I',guest,off(0xff85c4a0))[0]==0xff180800 and
         struct.unpack_from('<HI',guest,off(0xff838790))==(0xc080,0xfffe0800), 'Compiled native extended sequence table and composite entry hook')
    for r in look:
        need(r['at']==f'{0xff180800+victim*32:08X}' and int(r['low'],16)|(int(r['high'],16)<<16)==seq and
             r['mask']=='FFFF' and r['pc']=='FF83B850' and r['actor']==r['owner140']==actor and r['main']==main and r['id']==str(victim), 'Actual own sequence fetch and directly read Main140 self-owner')
    for i,r in enumerate(draw):
        phase=0 if i==0 else((i-1)%5 if i<=20 else 5)
        frame=enter if i==0 else(enter+1+3*(i-1)if i<=20 else impact)
        previous=0 if i==0 else(group if i==1 else group+((i-2)%5)*64)
        need(int(r['frame'])==frame and int(r['group'],16)==group+phase*64 and int(r['pose'],16)==previous and
             r['actor']==r['owner140']==actor and r['main']==main and r['id']==str(victim) and
             r['body']=='0002' and r['bank']=='0202' and r['cache']==('0105ED30'if 3-side==1 else'0105F230'), 'All own preload/fall/impact groups, preceding pose, body/bank/cache and exact native cadence')
        if i:need(r['x']=='192' and r['y']=='64', 'Native centered movie origin after synchronous preload')
    need([int(r['age'])for r in fields]==list(range(1101)) and
         [int(r['frame'])for r in fields]==list(range(origin,origin+1101)) and fields[-1]['mode']=='3', 'Whole consecutive native owner field window and actual next-screen mode')
    active=[r for r in fields if enter<int(r['frame'])<=impact]
    need(len(active)==59 and all(r['mode']=='9' and r['cine_actor']==r['owner140']==actor and
         r['cine_main']==main and r['id']==str(victim) and r['body']=='0002' and r['p1']==r['p2']=='00000000'for r in active), 'Direct Main140 owns true cinematic victim after independent physical retirement')
    direct=get('MK2_PIT_OWNER_ROUTE');base=audio('ROUTE')
    need(len(direct)==len(base) and all(all(a[k]==b[k]for k in('frame','seconds','entry','a0','a1','a2','a8','a13','id','return_pc','writes','assistance'))for a,b in zip(direct,base,strict=True)), 'Every direct native voice route binds the complete actual core audio observation')
    female=victim==18;gender='FFA123B0'if female else'FFA122D0';voice=0xce if female else 0xcc
    initial=[r for r in direct if r['return_pc']in('FF8EB5B0','FF8EB610')]
    cinematic=[r for r in direct if r['return_pc']in('FF85C5B0','FF85C610')]
    for rows,a,m,caller,word,packed,cue in ((initial,first['victim'],initial[0]['a13'],'FF8EB610',0x1b,0xcbcbcbcd,voice-1),
                                          (cinematic,actor,main,'FF85C610',0xcf,0xccccccce,voice)):
        need([r['entry']for r in rows]==['FFA12530','FFA12220',gender,'FFA123D0','FFA12530'] and
             all(r['a8']==r['ownerC0']==a and r['a13']==m and r['id']==str(victim) and r['mode']=='9' and
                 r['writes']=='0' and r['assistance']=='none'for r in rows) and
             all(Decimal(a['seconds'])<Decimal(b['seconds'])for a,b in zip(rows,rows[1:])), 'Full native literal/packed/gender/role/selected-cue route belongs to true victim')
        need(int(rows[0]['a0'],16)==word and int(rows[1]['a0'],16)==int(rows[2]['a0'],16)==int(rows[3]['a0'],16)==1 and
             int(rows[1]['a1'],16)==int(rows[2]['a1'],16)==packed and int(rows[2]['a2'],16)==victim and
             int(rows[3]['a1'],16)==int(rows[4]['a0'],16)==int(rows[4]['a1'],16)==cue and
             all(r['return_pc']==caller for r in rows[1:]), 'Original literal/packed bytes, true gender ID and one native selected voice variant')
    need(all(r['owner140']==actor and r['frame']==str(impact)for r in cinematic), 'Direct cinematic Main140 owns impact and every voice call')
    queues=[r for r in audio('QUEUE')if r['a8']==actor and r['a13']==main]
    packets=[r for r in audio('PACKET')if r['a8']==actor and r['a13']==main]
    sounds=[r for r in audio('SOUND')if r['a8']==actor and r['a13']==main]
    need(len(queues)==len(packets)==2 and len(sounds)==4, 'Exactly owned native impact/voice admissions, packets and both port bytes')
    additions={'FFA12A10':0,'FFA12A80':1,'FFA12B00':2}
    for i,(q,p)in enumerate(zip(queues,packets,strict=True)):
        word=int(q['a3'],16)+additions[q['entry']];stores=sounds[2*i:2*i+2]
        need(int(p['a3'],16)==word and q['a1']==p['a1'] and q['a4']==p['a4'] and
             q['frame']==p['frame']==str(impact) and p['entry']=='FFA13BA0' and
             Decimal(cinematic[0 if i==0 else 4]['seconds'])<Decimal(q['seconds'])<Decimal(p['seconds']) and
             [int(r['word'],16)for r in stores]==[0xff00|(word>>8),0xff00|(word&255)] and
             [r['pc']for r in stores]==['FFA13C90','FFA13D60'] and
             all(r['mask']=='FFFF' and r['frame']==str(impact)for r in stores), 'Whole actual owned queue-slot addition, packet and full native port bytes')
    return dict(passed=True,ownID=own,victimID=victim,origin=origin,terminal=int(end['frame']),enter=enter,impact=impact,
                cinematicActor=actor,cinematicMain=main,directOwnerFields=59,ownMovieDraws=22,trueGenderVoiceRoutes=10,
                initialNativeVoice=voice-1,cinematicNativeVoice=voice,fullPortAcceptance=False)


def qualify(ram):
    folder=ram['folder'];meta=json.loads((folder/'result.json').read_text());report=ram['report']
    need(report['passed'] and report['currentCrossPit19ChannelFiniteAudioAccepted'] and not host.original.census.census(), 'Same complete current19 normally terminal audio capture')
    with gzip.open(folder/'run.log.gz','rt')as reader:text=reader.read()
    guest=ram['guest'];fighter,side=meta['fighter'],meta['side'];stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    rng,rng_source,fault_source=rng_functions();queue=rng(text,guest,stock,fighter,side)
    good=owner_gate(text,guest,fighter,side);faults=[]
    def reject(label,bad,bad_guest=guest):
        need(bad!=text or bad_guest!=guest,'Actual nonvacuous direct owner mutation')
        try:owner_gate(bad,bad_guest,fighter,side)
        except(ValueError,KeyError,IndexError)as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Corrupted true victim ownership admitted '+label)
        need(owner_gate(text,guest,fighter,side)==good,'Complete original owner positive restored after each fault')
    actor=good['cinematicActor'];impact=good['impact'];enter=good['enter']
    for tag,key,value,where in (
        ('MK2_PIT140_CONSTRUCTOR','a0','00000000',''),('MK2_PIT140_CONSTRUCTOR','a11','00000000',''),
        ('MK2_PIT140_LOOKUP','owner140','00000000',''),('MK2_PIT140_LOOKUP','main','00000000',''),
        ('MK2_PIT140_LOOKUP','id','0',''),('MK2_PIT140_LOOKUP','low','0000',''),
        ('MK2_PIT140_DRAW','group','00000000',''),('MK2_PIT140_DRAW','body','0000',''),
        ('MK2_PIT140_DRAW','bank','0000',''),('MK2_PIT140_DRAW','cache','00000000',''),
        ('MK2_PIT140_DRAW','owner140','00000000',''),
        ('MK2_PIT140_FIELD','owner140','00000000',f'frame={enter+1} '),
        ('MK2_PIT140_FIELD','cine_main','00000000',f'frame={enter+1} '),
        ('MK2_PIT140_FIELD','p1','01034020',f'frame={enter+1} '),
        ('MK2_PIT_OWNER_ROUTE','owner140','00000000','return_pc=FF85C5B0'),
        ('MK2_PIT_OWNER_ROUTE','a8','00000000','return_pc=FF85C610'),
        ('MK2_PIT_OWNER_ROUTE','id','0','return_pc=FF85C610'),
        ('MK2_PIT_OWNER_ROUTE','a0','00000000','return_pc=FF85C5B0'),
        ('MK2_MAUDIO_PACKET','a3','00000000',f'a8={actor} ')):
        line=next(l for l in text.splitlines()if l.startswith(tag+' ')and where in l)
        changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(n==1 and changed!=line,'Actual owner row/key changes');reject(tag+'/'+key,text.replace(line,changed,1))
    line=[l for l in text.splitlines()if l.startswith('MK2_PIT140_DRAW ')][-1]
    reject('missing own impact draw',text.replace(line+'\n','',1))
    for address in (0xff85c4a0,0xff838790):
        bad=bytearray(guest);bad[(address-0xff800000)//8]^=1;reject('native source '+hex(address),text,bytes(bad))
    need(len(faults)==22 and len(queue['actualFaultsRejected'])==36,'Entire actual22 true-owner and original36 queue/RNG faults rejected')
    path=folder/'current_19_owned_voice_queue_rng_report.json'
    need(not path.exists(),'Never overwrite owned audio proof')
    pins=dict(meta['input_hashes'])
    for p in(Path(__file__),Path(original_rng.__file__),Path(original_rng.executed_contract.__file__),
             folder/'current_19_audio_report.json',folder/'result.json',folder/'run.log.gz'):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Whole compiled/input/native/source/model bytes remain frozen')
    result=dict(passed=True,fighter=fighter,side=side,actualNativeMovieAndVoiceOwnership=good,
                actualOwnerFaultsRejected=faults,wholeOriginalQueueRNG=queue,inputHashes=pins,
                fullCurrent19WaveformAnd29FaultsRetained=True,allNativePitCuePriorityAndRNGAccepted=False,
                nativeSuppressionAndSpecial71Accepted=False,allMirrorsAndStockVictimsAccepted=False,
                fullPortAcceptance=False,newNativeBoots=0,newBuilds=0,newRawMedia=0,publicPlayableChanged=False)
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(passed=True,fighter=fighter,side=side,ownedVoiceRoutes=10,ownerFaults=22,
                         queueRNGFaults=36,newNativeBoots=0,fullPortAcceptance=False)),flush=True)
    return result
