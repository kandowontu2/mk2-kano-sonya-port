"""Complete original980 source-PNG/component/control model against current data.

No missing historical payload/report restore: original52 native control words
come from the immutable MK2 program; independently coded blood-guide coverage
is cross-checked with the complete original977 classification. RAM only.
"""
import inspect, struct, textwrap
from pathlib import Path
from PIL import Image
import verify_native_torso_art_v980 as original
import current_payload_metadata_context_v5229 as current

ROOT,need,sha=current.ROOT,current.need,current.sha


def source_art(guest,payload,pins):
    assets=original.assets
    donor=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    need(assets.sha(donor)==assets.death.DONOR_SHA.upper()and assets.sha(stock)==assets.death.STOCK_SHA.upper(),
         'Immutable original donor palettes and native control program')
    report=dict(fighters={})
    for fighter,name in enumerate(('kano','sonya')):
        upper=Image.open(ROOT/'art_native_torso_v951'/f'{name}-upper-torsos.png').convert('RGBA')
        lower=Image.open(ROOT/'art_native_torso_v951/lower-stumps.png').convert('RGBA')
        parts=[assets.crop_cell(upper,(pose%3*512,pose//3*512,(pose%3+1)*512,(pose//3+1)*512))for pose in range(6)]
        parts+=[assets.crop_cell(lower,(fighter*627,0,(fighter+1)*627,1254))]
        counts=[]
        if fighter==0:
            ug=Image.open(ROOT/'art_native_torso_blood_v976/kano-upper-blood-guide.png').convert('RGBA')
            lg=Image.open(ROOT/'art_native_torso_blood_v976/lower-blood-guide.png').convert('RGBA')
            normal=assets.colors.palette(donor,0x92bbc);alternate=assets.colors.palette(donor,0x92c3e)
            for pose,(image,crop)in enumerate(parts):
                factor=76/parts[0][0].height if pose<6 else 94/image.height
                size=(round(image.width*factor),round(image.height*factor))
                guide=ug.crop((pose%3*512,pose//3*512,(pose%3+1)*512,(pose//3+1)*512))if pose<6 else lg.crop((0,0,627,1254))
                _,blood,_=assets.quantize_blood(image.resize(size,Image.Resampling.LANCZOS),guide.crop(tuple(crop)).resize(size,Image.Resampling.LANCZOS),normal,alternate)
                counts.append(dict(blood_pixels=int(blood.sum())))
        else:counts=[dict(blood_pixels=0)for _ in parts]
        report['fighters'][name]=dict(poses=counts)
    source=bytearray(payload)
    native=struct.unpack_from('<52I',stock,(0xff92aef0-0xff800000)//8)
    for fighter,stream in enumerate(assets.STREAMS):
        words=list(native);words[2]=(0xff013360,0xff033480)[fighter]
        struct.pack_into('<52I',source,assets.death.offset(stream),*words)
    full=inspect.getsource(original.verify)
    first='    byte_count = struct.unpack_from';last='    need(set(texts) == set(cases)'
    need(full.count(first)==full.count(last)==1,'Entire original980 independent source-PNG/28-component/native52word model boundaries')
    body=textwrap.dedent(full[full.index(first):full.index(last)])
    function='def verify_source(payload,source,donor,report,pins):\n    profile="current"\n'+textwrap.indent(body,'    ')+'    return by_source,palette_colors,byte_count\n'
    scope=dict(original.__dict__);scope['need']=need
    exec(compile(function,__file__+'.entire_original980_source_art_components_and_control_grammar','exec'),scope)
    by_source,palettes,count=scope['verify_source'](payload,source,donor,report,pins)
    need(len(by_source)==28 and guest[assets.ROM_DESCRIPTORS:assets.ROM_DESCRIPTORS+560]==payload[assets.DESCRIPTORS:assets.DESCRIPTORS+560]and
         guest[assets.ROM_GROUPS:assets.ROM_GROUPS+168]==payload[assets.GROUPS:assets.GROUPS+168],
         'Every actual compiled current Cage descriptor/component group exactly source-derived')
    paths=(Path(__file__).resolve(),Path(original.__file__),Path(assets.__file__),Path(assets.colors.__file__),
           Path(assets.codec.__file__),Path(assets.death.__file__),ROOT/'mk2/mk2-maincpu.bin',ROOT/'mk3/mk3-maincpu.bin')
    for p in paths:pins[str(p.resolve())]=sha(p)
    return dict(by_source=by_source,palette_colors=palettes,pixel_bytes=count,
                originalSourceModelSHA256=assets.sha(function.encode()),originalBloodGuideCoverage=report,
                currentAll28ComponentsSourceExact=True,entireNativeMain57ControlGrammarPreserved=True),payload[assets.PIXELS:assets.PIXELS+count]


def physical_contract():
    full=inspect.getsource(original.verify)
    first='    for case, text in texts.items():';last="    for file in ('mk2ks_stock_head_victim_v921.lua'"
    need(full.count(first)==full.count(last)==1,'Whole original980 native controller/art/palette/floor/cleanup contract boundaries')
    body=full[full.index(first):full.index(last)]
    body=body.replace('    for case, text in texts.items():\n','',1)
    body=textwrap.dedent(body)
    substitutions={
      'directory = ROOT / case':'directory=None',
      "result = json.loads((directory / 'result.json').read_text(encoding='utf-8-sig'))":'# Actual process result passed from current capture.',
      'if len(actions) != 1 or len(wraps) != 1 or len(terminal) != 1:\n    continue':
      "if len(actions) != 1 or len(wraps) != 1 or len(terminal) != 1:raise ValueError('Invalid native Cage action/wrap/terminal chronology')",
      "for age in range(0, 601, 10):\n    picture = directory / 'snap' / f'stock_head_{start}_{age:03d}.png'\n    need(picture.is_file() and Image.open(picture).size == (400, 254), case + ': actual scene image')\n    if picture.is_file():\n        pins[str(picture)] = digest(picture)":
      "need(all(f'stock_head_{start}_{age:03d}.png'in images and images[f'stock_head_{start}_{age:03d}.png'].shape==(254,400,3)for age in range(0,601,10)),case+': all61 actual original scene frames inRAM')",
      "(directory / 'guest_maincpu.bin').read_bytes() == expected_guest(payload)":"ram['guest_maincpu.bin'] == guest",
      "(directory / 'native_torso_gfx.bin').read_bytes()":"ram['native_torso_gfx.bin']",
      "path = directory / row['file']\n    need(path.is_file() and path.stat().st_size == 256, case + ': actual hardware palette dump')\n    if path.is_file() and path.stat().st_size == 256:\n        need(list(struct.unpack('<64I', path.read_bytes()))[1:] == palette_colors[int(row['source'], 16)][1:],\n             case + ': actual native costume/blood RGB pens')\n        pins[str(path)] = digest(path)":
      "need(row['file']in ram and len(ram[row['file']])==256 and list(struct.unpack('<64I',ram[row['file']]))[1:]==palette_colors[int(row['source'],16)][1:],case+': all actual native64-pen costume/blood palettes inRAM')",
      "for row in snapshots:\n    picture = directory / 'snap' / f\"torso_pose_{row['actor_pose']}_{row['frame']}.png\"\n    need(picture.is_file() and Image.open(picture).size == (400, 254), case + ': displayed section snapshot')\n    if picture.is_file():\n        pins[str(picture)] = digest(picture)":
      "for row in snapshots:\n    picture=f\"torso_pose_{row['actor_pose']}_{row['frame']}.png\"\n    need(picture in images and images[picture].shape==(254,400,3),case+': actual whole presented section inRAM')",
      "for file in ('run.log', 'result.json', 'guest_maincpu.bin', 'native_torso_gfx.bin'):\n    pins[str(directory / file)] = digest(directory / file)":'# Original raw sink filenames are only RAM labels.',
      "picture_matches = pictures.check_case(case, version, payload, records) if profile == 'current' else []\nif profile == 'current':\n    need(len(picture_matches) == 6 and {r['pose'] for r in picture_matches} == {0, 1, 2, 3, 5, 6}\n         and min((r['score'] for r in picture_matches), default=0) >= 0.5,\n         case + ': presented PNG matches actual encoded native section pixels, not prior page')":
      "picture_matches=[] # Full native pixel/occlusion contract is separate, never replace it with old best-location50% score.",
    }
    for before,after in substitutions.items():
        need(body.count(before)==1,'Only current version/RAM transport or separately strengthened raster model adaptation: '+before.splitlines()[0])
        body=body.replace(before,after,1)
    function='def contract(text,result,guest,payload,reference,images,ram):\n    errors=[];pins={};summaries={};case="actual_current_cage";check_files=False;version=979\n    by_source=reference["by_source"];palette_colors=reference["palette_colors"];byte_count=reference["pixel_bytes"]\n    executable_sha=current.EXE_SHA;payload_sha=current.PAYLOAD_SHA\n    def need(ok,message):\n        if not ok:errors.append(message)\n'+textwrap.indent(body,'    ')+"    if errors:raise ValueError(' | '.join(errors))\n    return summaries[case]\n"
    scope=dict(original.__dict__,current=current)
    exec(compile(function,__file__+'.entire_original980_physical_FIFO_owner_palette_ground_and_retirement','exec'),scope)
    return scope['contract'],original.assets.sha(function.encode())
