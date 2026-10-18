"""Authoritative current graphics generation for runtime receipt qualifiers."""
import hashlib
import json
from pathlib import Path
PORT=Path(__file__).resolve().parent

def graphics_directory():
    """Current emitted sockets; consumers must still verify graphics_metadata()."""
    return PORT/'generated_ending'
def graphics_metadata():
    folder=PORT/'generated_impale'
    metadata=json.loads((folder/'IMPALE_DATA.json').read_text())
    prefix=(PORT/'generated_nut/fighter_ui_finish_nut_graphics.bin').read_bytes()
    sha=lambda b:hashlib.sha256(b).hexdigest().upper()
    assert sha(prefix)==metadata['prefixSHA256']
    assert (folder/'fighter_ui_finish_impale_graphics.bin').read_bytes().startswith(prefix)
    for name,digest in metadata['sockets'].items():assert sha((folder/name).read_bytes())==digest
    arm_folder=PORT/'generated_arm_rip'
    arm=json.loads((arm_folder/'ARM_RIP_DATA.json').read_text())
    previous=(folder/'fighter_ui_finish_impale_graphics.bin').read_bytes()
    packed=(arm_folder/'fighter_ui_finish_arm_graphics.bin').read_bytes()
    assert sha(previous)==arm['prefixSHA256'] and packed.startswith(previous)
    assert sha(packed)==arm['packedSHA256'] and arm['socketsEmitted']
    for name,digest in arm['sockets'].items():assert sha((arm_folder/name).read_bytes())==digest
    inflation_folder=PORT/'generated_inflation_v3'
    inflation=json.loads((inflation_folder/'INFLATION_DATA.json').read_text())
    previous=packed
    packed=(inflation_folder/'fighter_ui_finish_inflate_graphics.bin').read_bytes()
    assert sha(previous)==inflation['prefixSHA256'] and packed.startswith(previous)
    assert sha(packed)==inflation['packedSHA256'] and inflation['socketsEmitted']
    assert not inflation['artBoundaryIssues']
    for name,digest in inflation['sockets'].items():assert sha((inflation_folder/name).read_bytes())==digest
    ingest_folder=PORT/'generated_ingestion'
    ingest=json.loads((ingest_folder/'INGESTION_DATA.json').read_text())
    previous=packed
    packed=(ingest_folder/'fighter_ui_finish_ingest_graphics.bin').read_bytes()
    assert sha(previous)==ingest['prefixSHA256'] and packed.startswith(previous)
    assert sha(packed)==ingest['packedSHA256'] and ingest['socketsEmitted']
    for name,digest in ingest['sockets'].items():assert sha((ingest_folder/name).read_bytes())==digest
    split_folder=PORT/'generated_split'
    split=json.loads((split_folder/'SPLIT_DATA.json').read_text())
    previous=packed
    packed=(split_folder/'fighter_ui_finish_split_graphics.bin').read_bytes()
    assert sha(previous)==split['prefixSHA256'] and packed.startswith(previous)
    assert sha(packed)==split['packedSHA256'] and split['socketsEmitted']
    for name,digest in split['sockets'].items():assert sha((split_folder/name).read_bytes())==digest
    morph_folder=PORT/'generated_morph'
    morph=json.loads((morph_folder/'MORPH_DATA.json').read_text())
    previous=packed
    packed=(morph_folder/'fighter_ui_finish_morph_graphics.bin').read_bytes()
    assert sha(previous)==morph['prefixSHA256'] and packed.startswith(previous)
    assert sha(packed)==morph['packedSHA256'] and morph['socketsEmitted']
    for name,digest in morph['sockets'].items():assert sha((morph_folder/name).read_bytes())==digest
    ending_folder=graphics_directory()
    ending=json.loads((ending_folder/'ENDING_ART.json').read_text())
    previous=packed
    packed=(ending_folder/'fighter_ui_finish_ending_graphics.bin').read_bytes()
    assert sha(previous)==ending['prefixSHA256'] and packed.startswith(previous)
    assert sha(packed)==ending['packedSHA256'] and ending['socketsEmitted']
    assert sha((ending_folder/'KSENDART.ASM').read_bytes())==ending['sourceSHA256']
    for name,digest in ending['sockets'].items():assert sha((ending_folder/name).read_bytes())==digest
    return ending

def verify_archive_sockets(archive):
    """Pin runtime graphics to the current full image, not an older prefix build."""
    metadata=graphics_metadata()
    for name,digest in metadata['sockets'].items():
        assert hashlib.sha256(archive.read(name)).hexdigest().upper()==digest,name
