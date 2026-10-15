"""Entire original1014 Baraka native input/ownership/rotation/floor contract.

Only actual current identity/ROM version and RAM transport replace obsolete
file sinks. Old best-location50% matching is replaced by a separate exact
foreground/scanout gate, not treated as artwork acceptance here.
"""
import inspect,textwrap
from pathlib import Path
import verify_rolling_heads_v1014 as original
import current_payload_metadata_context_v5229 as current
import current_reptile_victims_ram_v5477 as source_model

ROOT,need,sha=current.ROOT,current.need,current.sha


def source_art(guest,payload,pins):
    reference,gfx=source_model.corrected_art(guest,payload,pins)
    by_source={}
    for fighter,data in reference['fighters'].items():
        for frame in data['frames']:
            by_source[int(frame['graphics'],16)]=dict(fighter=fighter,kind=frame['kind'],pose=frame['pose'],
              size=frame['size'],descriptor=frame['descriptor'])
    need(len(by_source)==28,'Every source-bound current owned body and native rotating-head descriptor')
    reference['by_source']=by_source
    for p in(Path(__file__),Path(original.__file__),Path(source_model.__file__),
             ROOT/'tools/current_reptile_victims_ram_v5470.py',ROOT/'tools/current_reptile_victims_ram_v5473.py',
             ROOT/'tools/current_reptile_victims_ram_v5467.py'):
        pins[str(p.resolve())]=sha(p)
    return reference,gfx


def physical_contract():
    full=inspect.getsource(original.verify)
    first='    for case,text in texts.items():';last="    for filename in ('mk2ks_stock_head_victim_v921.lua'"
    need(full.count(first)==full.count(last)==1,'Entire original1014 physical/FIFO/head/body/floor/retirement contract boundaries')
    body=full[full.index(first):full.index(last)].replace(first+'\n','',1)
    body=textwrap.dedent(body)
    edits={
     "directory=ROOT/case;result=json.loads((directory/'result.json').read_text(encoding='utf-8-sig'))":'directory=None # Actual native process result supplied.',
     'if len(actions)!=1 or len(wraps)!=1 or len(stops)!=1:continue':
     "if len(actions)!=1 or len(wraps)!=1 or len(stops)!=1:raise ValueError('Invalid original Baraka action/wrap/terminal chronology')",
     "(directory/'guest_maincpu.bin').read_bytes()==guest":"ram['guest_maincpu.bin']==guest",
     "(directory/'native_death_gfx.bin').read_bytes()":"ram['native_death_gfx.bin']",
     "palette_path=directory/dump['file']":"palette_path=dump['file']",
     'palette_path.is_file() and palette_path.stat().st_size==256':'palette_path in ram and len(ram[palette_path])==256',
     'if not palette_path.is_file():continue':'if palette_path not in ram:continue',
     'palette_path.read_bytes()':'ram[palette_path]',
     'path=directory/\'snap\'/f"head_pose_{snap[\'actor_pose\']}_{snap[\'frame\']}.png"':
     'path=f"head_pose_{snap[\'actor_pose\']}_{snap[\'frame\']}.png"',
     'path.is_file() and Image.open(path).size==(400,254)':'path in images and images[path].shape==(254,400,3)',
     'if not path.is_file():continue':'if path not in images:continue',
     "path=directory/'snap'/f'stock_head_{start}_{age:03d}.png'":"path=f'stock_head_{start}_{age:03d}.png'",
     'if check_files and path.is_file():pins[str(path)]=digest(path)':'# Requested actual whole scene pixels stay inRAM.',
     "if check_files:\n    for filename in ('run.log','result.json','guest_maincpu.bin','native_death_gfx.bin'):\n        path=directory/filename;pins[str(path)]=digest(path)":'# No obsolete raw sink files or restored old runtime replay.',
    }
    for before,after in edits.items():
        count=body.count(before);expected=2 if before=='path.is_file() and Image.open(path).size==(400,254)'else 1
        need(count==expected,'Exact whole current/RAM-only transport adaptation: '+before)
        body=body.replace(before,after)
    first="    match=pixel_match(path,indices,palette,bool(int(dma['command'],16)&16))"
    last="    if check_files:pins[str(path)]=digest(path);pins[str(palette_path)]=digest(palette_path)"
    need(body.count(first)==body.count(last)==1,'Only original fuzzy image matcher replaced; all14 native palette/next-field/DMA bindings retained')
    a=body.index(first);b=body.index(last)+len(last)
    body=body[:a]+"    matches.append(dict(kind=asset['kind'],pose=asset['pose'],snapshot=path,exactRasterGateRequired=True))"+body[b:]
    function='def contract(text,result,guest,payload,reference,images,ram):\n    errors=[];pins={};summaries={};check_files=False;case="actual_current_baraka"\n    by_source=reference["by_source"]\n    def need(ok,message):\n        if not ok:errors.append(message)\n'+textwrap.indent(body,'    ')+"    if errors:raise ValueError(' | '.join(errors))\n    return summaries[case]\n"
    scope=dict(original.__dict__,CANDIDATE=current.NAME,EXE=current.EXE_SHA,PAYLOAD=current.PAYLOAD_SHA)
    exec(compile(function,__file__+'.entire_original1014_native_physical_rotation_floor_and_retirement','exec'),scope)
    return scope['contract'],original.hashlib.sha256(function.encode()).hexdigest().upper()
