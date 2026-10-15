"""Consecutive actual move scenes and native composite publication provenance.

All eight moves in both slots, plus two actual airborne square contacts.
This does not certify every pixel/shadow/erase/audio or all victims/arenas.
"""
import argparse,hashlib,json,re
from collections import defaultdict
from pathlib import Path
from PIL import Image,ImageDraw
import verify_native_ground_throw_source_v1598 as current
import verify_human_special_matrix as human
from verify_cpu_pair_display_v635_v3 import group
ROOT=current.ROOT
HEX={'actor','main','owner','pose','cache','facing','body','flags','vx','vy','gravity','row','source','size','xy','command','palette','pc'}

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb')as stream:
        for block in iter(lambda:stream.read(1048576),b''):h.update(block)
    return h.hexdigest().upper()

def rows(text,tag):
    result=[]
    for line in text.splitlines():
        if not line.startswith('MK2_HPHASE_'+tag+' '):continue
        r=dict(re.findall(r'(\w+)=([^\s]+)',line))
        for key,value in tuple(r.items()):
            if key in HEX and not(tag=='RESULT'and key=='command'):r[key]=int(value,16)
            elif re.fullmatch(r'-?\d+',value):r[key]=int(value)
        result.append(r)
    return result

def check_observer(text):
    start='-- BEGIN v1758 read-only consecutive move-phase observer\n'
    end='-- END v1758 read-only consecutive move-phase observer\n'
    assert text.count(start)==text.count(end)==1
    first=text.index(start);last=text.index(end)+len(end)
    baseline=(ROOT/'mk2ks_human_special_matrix_v3.lua').read_text()
    assert sha(ROOT/'mk2ks_human_special_matrix_v3.lua')=='374EFA1A16F9EEACC8F458F814DFFD29C144AAB972FDEB20973BD3EB94180EFF'
    assert text[:first]+text[last:]==baseline,'Every physical input and native activation/recovery/follow-up observer remains byte-exact'
    block=text[first:last]
    assert not re.search(r':write_|set_value|clear_value|load_?state|dofile|\.value\s*=',block)
    assert "frame<=command+416"in block and 'frame<=recovered+12'in block
    assert "install_read_tap(0xff804410,0xff80441f"in block

def verify_case(folder,guest,payload,pins,text_override=None):
    result=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    build=json.loads((ROOT/current.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    move,side,air=result['move'],result['side'],result['air']
    assert result['exit_code']==0 and result['candidate']==current.NAME
    assert result['executable_sha256']==build['executable_sha256']=='9D2E9849CA3A98AA06018DB2EF3EE65397A5C9EC95C466CFD999C9091237B695'
    assert result['payload_sha256']==build['payload_sha256']=='5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D'
    assert result['cheats_enabled']is False and result['assistance']=='none'and result['victim']=='sub_zero'
    assert before==result['input_hashes']and all(before.get(p)==h for p,h in build['input_hashes'].items())
    for p,h in before.items():
        assert sha(p)==h,'Executed source changed: '+p;pins[p]=h
        if Path(p).suffix in('.ps1','.lua','.json'):
            frozen=folder/'input_sources'/Path(p).name
            assert sha(frozen)==h;pins[str(frozen)]=h
    check_observer((folder/'input_sources/mk2ks_human_special_phases_v1758.lua').read_text())
    text=text_override if text_override is not None else(folder/'run.log').read_text(encoding='utf-8-sig')
    assert not re.search(r'LUA ERROR|Lua error|WRONG CHECKSUMS|fatal error|access violation',text,re.I)
    baseline=ROOT/f'audit_v1620_human_{move}{"_air"if air else""}_p{side}'
    old=(baseline/'run.log').read_text(encoding='utf-8-sig');pins[str(baseline/'run.log')]=sha(baseline/'run.log')
    events=lambda t:[re.sub(r'\bbank=[0-9A-F]+','bank=NATIVE_ALLOCATION',line)for line in t.splitlines()if line.startswith('MK2_HSPECIAL_')]
    assert events(text)==events(old),'Every actual native input, pose, health, contact and recovery event must remain unchanged'
    state=human.verify_log(text,move,side,air)
    chronology=human.rows(text,'RESULT')[0]
    snapshots=rows(text,'SNAP');actors=rows(text,'ACTOR');queues=rows(text,'QUEUE');final=rows(text,'RESULT')
    all_rows=snapshots+actors+queues+final
    assert all(r['move']==move and r['side']==side and r['writes']==0 and r['assistance']=='none'for r in all_rows)
    expected=list(range(chronology['command'],chronology['recovered']+13))
    assert [r['frame']for r in snapshots]==expected,'Every consecutive command, special and 12-field cleanup scene'
    assert len(final)==1 and final[0]['command']==expected[0]and final[0]['recovered']==chronology['recovered']and final[0]['snaps']==len(expected)
    assert final[0]['rasterAcceptance']==final[0]['fullPortAcceptance']=='false'
    by={(r['frame'],r['slot']):r for r in actors}
    assert len(by)==len(actors)==len(expected)*2 and set(by)=={(f,s)for f in expected for s in(1,2)}
    identity=human.SPECS[move][0];ids={side:identity,3-side:8}
    own=human.rows(text,'FIELD');owners={s:(own[0 if s==1 else 1]['actor'],own[0 if s==1 else 1]['main'])for s in(1,2)}
    for r in actors:
        s=r['slot'];assert r['id']==r['roster']==ids[s]and(r['actor'],r['main'])==owners[s]and r['owner']==r['actor']
        assert r['arena']==0 and r['floor']==r['stageY']-{17:134,18:135,8:131}[ids[s]],'Character-owned floor throughout the special'
        assert 0<=r['hp']<=161 and 0x01000000<=r['cache']<0x01100000
    publications=defaultdict(list)
    for q in queues:
        assert q['frame']in expected and q['slot']in(1,2)
        s=q['slot'];assert(q['actor'],q['main'])==owners[s]and q['owner']==q['actor']and q['id']==q['roster']==ids[s]
        assert q['pc']==0xff804420 and q['row']==q['cache']+q['part']*112 and 0<=q['part']<12
        composition=group(q,payload,guest);e=composition[q['part']]
        assert(q['source'],q['size'],q['command'])==(e['source'],e['width']|(e['height']<<16),(e['command']|0x8002)<<16),'Native publication must match its real source composite'
        publications[q['frame'],s].append(q['part'])
    assert queues and all(sorted(parts)==list(range(len(parts)))for parts in publications.values()),'Complete native multipart publications'
    for filename in('special_before.png','special_recovered.png','special_final.png'):
        path=folder/'snap'/filename;oldpath=baseline/'snap'/filename
        assert path.read_bytes()==oldpath.read_bytes(),'Prior complete before/recovered/final scenes remain byte-exact'
        pins[str(oldpath)]=sha(oldpath)
    for r in snapshots:
        assert r['file']==f'phase_{r["frame"]:05d}.png'and r['age']==r['frame']-chronology['command']
        path=folder/'snap'/r['file']
        with Image.open(path)as image:assert image.size==(400,254)
    assert{p.name for p in(folder/'snap').glob('phase_*.png')}=={r['file']for r in snapshots}
    selected=[];previous=None
    for r in snapshots:
        a,b=by[r['frame'],side],by[r['frame'],3-side]
        key=(a['pose'],b['pose'],a['body'],b['body'],a['action'],b['action'])
        if key!=previous or r['frame']==expected[-1]:selected.append(r)
        previous=key
    for path in folder.rglob('*'):
        if path.is_file():pins[str(path)]=sha(path)
    return dict(case=folder.name,move=move,side=side,air=air,consecutiveScenes=len(snapshots),nativeCompositeParts=len(queues),
                ownDistinctPoses=len({r['pose']for r in actors if r['slot']==side}),state=state,
                selectedScenes=selected,fullRasterAcceptance=False,allMoveGroundShadowAccepted=False,fullPortAcceptance=False)

def contact_sheets(case,out):
    folder=ROOT/case['case'];sheets=[];entries=case['selectedScenes']
    for page in range((len(entries)+15)//16):
        section=entries[page*16:(page+1)*16];sheet=Image.new('RGB',(1600,((len(section)+3)//4)*278),(24,24,24));draw=ImageDraw.Draw(sheet)
        for n,r in enumerate(section):
            image=Image.open(folder/'snap'/r['file']).convert('RGB');x,y=n%4*400,n//4*278
            sheet.paste(image,(x,y+24));draw.text((x+4,y+5),f'{case["move"]} P{case["side"]} air={case["air"]} age={r["age"]} field={r["frame"]}',fill='white')
        path=out/f'{case["move"]}{"_air"if case["air"]else""}_p{case["side"]}_{page+1}.png';sheet.save(path)
        sheets.append(dict(file=str(path),sha256=sha(path)))
    return sheets

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'audit_v1761_human_special_phases_checked');args=parser.parse_args()
    assert not args.output.exists(),'Never overwrite executed evidence'
    pins={};cases=[]
    proofpath=current.OUT/'report.json';proof=json.loads(proofpath.read_text());assert proof['passed']and proof['wholeActualGuestExactlyTwoPatches']
    for p,h in proof['inputHashes'].items():assert sha(p)==h;pins[p]=h
    pins[str(proofpath)]=sha(proofpath);guest,_,payload=current.expected()
    try:
        for move,side,air in[(m,s,False)for m in human.SPECS for s in(1,2)]+[('square',s,True)for s in(1,2)]:
            folder=ROOT/f'audit_v1760_human_{move}{"_air"if air else""}_p{side}'
            case=verify_case(folder,guest,payload,pins);cases.append(case);print(case['case']+' consecutive scenes and source-composite publication accepted',flush=True)
        report=dict(passed=True,candidate=current.NAME,cases=cases,totalConsecutiveScenes=sum(c['consecutiveScenes']for c in cases),nativeCompositeParts=sum(c['nativeCompositeParts']for c in cases),
                    everyNativeBaselineEventUnchanged=True,allEightMovesBothSlots=True,airborneSquareBothSlots=True,
                    fullRasterAcceptance=False,allMoveGroundShadowAccepted=False,artisticReviewPending=True,audioAcceptance=False,fullPortAcceptance=False,scope=__doc__)
    except Exception as error:report=dict(passed=False,error=repr(error),completedCases=cases,fullPortAcceptance=False)
    args.output.mkdir()
    if report['passed']:
        for case in cases:case['contactSheets']=contact_sheets(case,args.output)
    for path in(Path(__file__),ROOT/'tools/verify_human_special_matrix.py',ROOT/'tools/verify_cpu_pair_display_v635_v3.py'):pins[str(path)]=sha(path)
    report['inputHashes']=pins;(args.output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases','completedCases')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
