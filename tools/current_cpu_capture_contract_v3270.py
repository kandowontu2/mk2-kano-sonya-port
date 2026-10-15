"""Original full CPU capture contract, only collision-free snapshot addressing added."""
import inspect, json, ntpath
from pathlib import Path
import verify_native_cpu_square_inventory_v2998 as original
ROOT=original.ROOT; need=original.need; assembly=original.assembly

def pin_snapshot(folder,file,wanted,pin):
    mapping_path=folder/'source_snapshot_paths.json'
    mapping=json.loads(mapping_path.read_text(encoding='utf-8-sig'))
    before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
    selected={p for p in before if Path(p).suffix in ('.lua','.ps1','.json')}
    need(set(mapping)==selected and len({ntpath.normcase(ntpath.normpath(p)) for p in mapping.values()})==len(mapping),'All original snapshots distinct and complete, no basename aliases for JSON')
    expected=(folder/'input_sources/tree'/Path(file).resolve().relative_to(ROOT.resolve())).resolve()
    actual=Path(mapping[file]).resolve()
    need(actual==expected and actual.is_relative_to((folder/'input_sources/tree').resolve()),'Exact immutable before-run original-source hierarchy')
    pin(actual,wanted); pin(mapping_path)

def capture(folder,build,player,approach,policy,pins):
    # The old executable and byte-level runtime contracts are not relaxed.
    # This exact function is checked below against its immutable source with
    # only the file-snapshot address expression changed.
    source=inspect.getsource(original.capture)
    before="if Path(file).suffix in('.lua','.ps1','.json'):pin(folder/'input_sources'/Path(file).name,wanted)"
    after="if Path(file).suffix in('.lua','.ps1','.json'):pin_snapshot(folder,file,wanted,pin)"
    need(source.count(before)==1,'Exactly one old flat snapshot address')
    namespace=dict(vars(original)); namespace['pin_snapshot']=pin_snapshot
    exec(compile(source.replace(before,after),str(Path(__file__).resolve())+'::original_capture_snapshot_address_only','exec'),namespace)
    meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    need(meta.get('snapshot_schema')==2,'Actually executed collision-free runner schema, never synthesized later')
    return namespace['capture'](folder,build,player,approach,policy,pins)
