"""Finite historical geometry dependency conservation; not fresh visible sole proof."""
import copy,hashlib,json
from pathlib import Path
import verify_native_source_sync as sync


def function(text,name):
    first=text.index('void midtunit_state::'+name+'(')
    opening=text.index('{',first);depth=1;end=opening+1
    while depth:
        depth+=(text[end]=='{')-(text[end]=='}');end+=1
    return text[first:end]


def main():
    verified=sync.verify();root=sync.ROOT
    old=root/'diagnostic_v5219_current_payload_rom_metadata'
    reportpath=root/'audit_v6022_current_ordinary_kitana_raw_checked/report.json'
    report=json.loads(reportpath.read_text());assert report['passed'] and report['candidate']==old.name
    meta=json.loads((old/'build-info.json').read_text(encoding='utf-8-sig'))
    current=json.loads((sync.BUILD/'build-info.json').read_text(encoding='utf-8-sig'))
    norm=lambda entries:{str(Path(k).resolve()):v for k,v in entries.items()}
    oldpins=norm(meta['canonical_source_hashes_at_compile']);newpins=norm(current['canonical_source_hashes_at_compile'])
    paths=['src/mame/midway/midtunit_v.cpp','src/mame/midway/midtunit_v.h',
           'src/devices/cpu/tms34010/tms34010.cpp','src/devices/cpu/tms34010/tms34010.h',
           'src/devices/cpu/tms34010/34010ops.hxx','src/devices/cpu/tms34010/34010gfx.hxx']
    observed={};expected={};dependencies=[];pins={}
    for rel in paths:
        actual=root/'mame-mkp'/rel;snapshot=old/'input_sources/mame-mkp'/rel;key=str(actual.resolve())
        assert oldpins[key]==newpins[key]==sync.sha(snapshot)==sync.sha(actual)
        assert actual.read_bytes()==snapshot.read_bytes()
        observed[key]=sync.sha(actual);expected[key]=newpins[key]
        dependencies.append(dict(source=str(actual),historicalSnapshot=str(snapshot),wholeBytesEqual=True,SHA256=expected[key]))
        pins[str(actual)]=sync.sha(actual);pins[str(snapshot)]=sync.sha(snapshot)
    a=root/'mame-mkp/src/mame/midway/midtunit.cpp';b=old/'input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
    maps={name:(function(a.read_text(),name),function(b.read_text(),name)) for name in ('main_map','mk2ks_map')}
    m=root/'mame-mkp/src/mame/midway/midtunit_m.cpp';n=old/'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
    start="\t// MKII's stage baseline is not the bottom of a standing sprite."
    end='\t// Keep true-ID winner announcements in the native table.'
    section=lambda text:text[text.index(start):text.index(end,text.index(start))]
    ground=(section(m.read_text()),section(n.read_text()))
    def gate(digests,map_regions,ground_regions):
        assert digests==expected
        assert all(x==y for x,y in map_regions.values())
        assert ground_regions[0]==ground_regions[1]
        assert 'mk2_ground_contact_extension = 5' in ground_regions[0]
        assert 'extend_parameters(0xff908010, { 0xff907f70 }, 139 - mk2_ground_contact_extension, 140 - mk2_ground_contact_extension)' in ground_regions[0]
    gate(observed,maps,ground);faults=[]
    for path in list(observed):
        bad=dict(observed);bad[path]='0'*64
        try:gate(bad,maps,ground)
        except AssertionError:faults.append(dict(kind='whole current rendering dependency',path=path))
        else:raise AssertionError('Dependency corruption admitted')
    for label,badmaps,badground in [('changed native floor contact5',maps,(ground[0].replace('extension = 5','extension = 6'),ground[1])),
                                   ('changed GFX ROM mapping',{'main_map':(maps['main_map'][0].replace('midtunit_gfxrom_r','midtunit_vram_r'),maps['main_map'][1]),'mk2ks_map':maps['mk2ks_map']},ground)]:
        try:gate(observed,badmaps,badground)
        except AssertionError:faults.append(dict(kind=label))
        else:raise AssertionError('Region mutation admitted')
    payload=sync.BUILD/'roms/mk2ks/mk2ks.mdata';assert sync.sha(payload)==report['payloadSHA256']==meta['payload_sha256']
    for p in (a,b,m,n,reportpath,old/'build-info.json',payload):pins[str(p)]=sync.sha(p)
    result=dict(passed=True,wholeVideoDMAAndTMSExecutionDependencies=dependencies,
                videoVRAMPaletteDMAControlGFXAndShadowAddressMapsNormalizedSourceEqual=True,
                importedNativeFloor134135AndEntrance20ParametersNormalizedSourceEqual=True,
                floorContactSource=ground[0],addressMaps={k:x for k,(x,y) in maps.items()},
                payloadIdentical=True,sourceSyncCompileInputs=verified['trackedCanonicalCompileInputs'],
                effectiveFaultsRejected=faults,inputHashes=pins,
                historicalBodyShadowKernelEvidenceRetained=True,
                currentGuestCameraPoseAndNativeDrawDependenciesFullyConserved=False,
                currentStandingVisibleOpaqueSoleParityProven=False,
                sourceChangeBoundary='Whole midtunit_m.cpp and midtunit.cpp are NOT equal: current additions alter selector layers, AI, finishers/cinematics and extra GFX allocations. Equal backend, maps, floor patch and payload do not independently bind actual current pose/camera/scanout opaque soles.',
                nextMinimalVerification='Four physical two-human cold cases: Kano/Sonya vs stock Kitana in both slots. First simultaneous grounded idle, bind true IDs/Main owners/floor/Y/pose/native screen/camera and compare actual visible opaque foot line, not only descriptor/floor rectangles. Proposed4PNG total256KiB, no rawRAM/GFX/PCM/video; no launch authorized by this source audit.',
                newEmulatorRuns=0,newMedia=0,fullPortAcceptance=False)
    out=root/'audit_current_standing_renderer_dependencies_checked';assert not out.exists();out.mkdir()
    (out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(passed=True,wholeDependencies=6,maps=2,faults=len(faults),currentVisibleSolesProven=False)))


if __name__=='__main__':main()
