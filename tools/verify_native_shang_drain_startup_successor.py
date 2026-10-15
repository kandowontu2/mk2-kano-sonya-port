"""Correct the omitted predecessor low-window initialization, using SAME RAM.

Never launches a game, changes a ROM, rewrites an earlier receipt, or accepts
gameplay. Called inside the retained original startup host. Source extracted
from the actual compiled driver is executed separately from the Python model.
"""
import hashlib
import json
import re
import struct
import subprocess
from pathlib import Path

import check_native_shang_owned_reaction_source as reaction
import native_process_census_v6647 as identity

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit_native_shang_drain_startup_successor'
NAME = 'diagnostic_native_shang_owned_drain'
COMPILER = Path('C:/Strawberry/c/bin/g++.exe')
SOURCE = ROOT / NAME / 'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
AIR_WORDS = (0xfe828e80, 0xfe828ec0, 0xfe828f00, 0xfe828f00,
             0xfe828f00, 0xfe828f00, 0, 0xfe828f00, 0xfe828f00, 0)


def need(value, reason):
    if not value:
        raise ValueError(reason)


def digest(data):
    return hashlib.sha256(data).hexdigest().upper()


def sha(path):
    return digest(Path(path).read_bytes())


def expected_owned(physical):
    """Independent complete low-window model: old air throw THEN new lead-in."""
    need(len(physical) == 0x200000, 'Full original physical window')
    need(physical[0x10011c:0x100120] == bytes(4) and
         physical[0x102920:0x102948] == b'\xff' * 40,
         'Original root empty and complete ten-word air storage unused')
    prior = bytearray(physical)
    struct.pack_into('<I', prior, 0x10011c, 0xff014900)
    struct.pack_into('<10I', prior, 0x102920, *AIR_WORDS)
    need(sum(a != b for a, b in zip(physical, prior)) == 43,
         'Exactly 43 EXISTING air-throw initialized bytes')
    after, rows = reaction.proposed_data(bytes(prior))
    need(sum(a != b for a, b in zip(prior, after)) == 24 and
         sum(a != b for a, b in zip(physical, after)) == 67,
         'Exactly 24 new lead-in bytes; complete initialization delta 67')
    return after, rows


def snippets():
    source = SOURCE.read_text()
    prior = (ROOT / 'source_native_paired_stumble_table/midtunit_m.cpp').read_text()
    first = '\t// Isolated Kano air-throw experiment:'
    last = '\t// The airborne throw\'s victim alignment table'
    need(source.count(first) == source.count(last) == prior.count(first) == prior.count(last) == 1,
         'Unique actual compiled predecessor block boundaries')
    air = source[source.index(first):source.index(last)]
    need(air == prior[prior.index(first):prior.index(last)], 'Existing air block byte-identical to predecessor')
    lead = (ROOT / 'tools/native_shang_owned_reaction.inc').read_text()
    need(source.count(lead.rstrip()) == 1, 'Entire reviewed new lead-in occurs once in actual compiled driver')
    stores = re.findall(r'\bdonor\[[^\]]+\]\s*=(?!=)[^;]+;', source)
    need(len(stores) == 2 and all(s in air for s in stores),
         'All mutable donor-array stores in full actual driver are in old block')
    need(source.count('uint8_t *const donor = memregion("mk3data")->base();') == 1 and
         source.count('uint8_t *const shang_owned_data = memregion("mk3data")->base();') == 1 and
         source.count('memregion("mk3data")->base()') == 3 and
         'uint8_t const *const morph_data = memregion("mk3data")->base();' in source,
         'Only two mutable low-region bindings; remaining morph binding const')
    return air, lead


def harness(air, lead):
    return r'''
#include <cstdint>
#include <cstring>
#include <iostream>
#include <stdexcept>
#include <vector>
#include <io.h>
#include <fcntl.h>
struct region {
 std::vector<uint8_t> data;
 uint8_t *base(){return data.data();}
 unsigned bytes() const {return unsigned(data.size());}
};
region low{{std::vector<uint8_t>(0x200000)}};
region *memregion(char const *name){
 if(std::strcmp(name,"mk3data"))throw std::runtime_error("unexpected region");
 return &low;
}
void fatalerror(char const *s){throw std::runtime_error(s);}
int main(){
 _setmode(_fileno(stdin),_O_BINARY);_setmode(_fileno(stdout),_O_BINARY);
 std::vector<uint8_t> high(0x100000);
 std::cin.read(reinterpret_cast<char*>(high.data()),high.size());
 std::cin.read(reinterpret_cast<char*>(low.base()),low.bytes());
 if(!std::cin)return 2;
 uint8_t *const donor=low.base();
 auto rom_offset=[](uint32_t pc){return (pc-0xff800000U)/8;};
 auto read32=[&](unsigned at){return uint32_t(high.at(at))|(uint32_t(high.at(at+1))<<8)|
  (uint32_t(high.at(at+2))<<16)|(uint32_t(high.at(at+3))<<24);};
 auto write32=[&](unsigned at,uint32_t value){for(unsigned i=0;i<4;i++)high.at(at+i)=value>>(i*8);};
 auto donor32=[&](unsigned at){return uint32_t(low.data.at(at))|(uint32_t(low.data.at(at+1))<<8)|
  (uint32_t(low.data.at(at+2))<<16)|(uint32_t(low.data.at(at+3))<<24);};
 try{
''' + air + lead + r'''
 }catch(std::exception const &e){std::cerr<<e.what();return 5;}
 std::cout.write(reinterpret_cast<char*>(high.data()),high.size());
 std::cout.write(reinterpret_cast<char*>(low.base()),low.bytes());
 return std::cout ? 0 : 3;
}
'''


def verify(ram):
    need(not OUT.exists() and ram['job'].poll() == ram['nativeExit'] == 0 and
         not ram['stderr'] and not identity.census(),
         'Original same host RAM and native terminal; no replay')
    for p, h in ram['pins'].items():
        need(sha(p) == h, 'Original startup pins unchanged: ' + p)
    meta = json.loads((ROOT / NAME / 'build-info.json').read_text(encoding='utf-8-sig'))
    guard = json.loads((ROOT / 'audit_native_shang_drain_build_source/report.json').read_text())
    need(sha(SOURCE) == guard['stagedSourceHashes']['midtunit_m.cpp'] ==
         '8CF0E0540E63E354D08CD4F1226DFD99F6CCFF6754A68A802FF7AC0F10B3E71B',
         'Exact complete compiled qualified source')
    physical_path = ROOT / NAME / 'roms/mk2ks/mk2ks.mdata'
    physical = physical_path.read_bytes()
    need(digest(physical) == meta['payload_sha256'], 'Unchanged physical payload')
    owned, rows = expected_owned(physical)
    wanted = dict(ram['wanted'], owned=owned)
    omitted = [i for i, (a, b) in enumerate(zip(ram['wanted']['owned'], owned)) if a != b]
    need(omitted == [i for i, (a, b) in enumerate(zip(ram['observed']['owned'], ram['wanted']['owned'])) if a != b],
         'All and only the prior 43 omitted bytes explain original failed comparison')
    air, lead = snippets()
    cpp = harness(air, lead)
    OUT.mkdir()
    probe = OUT / 'low_initializer_probe.exe'
    built = subprocess.run([str(COMPILER), '-std=c++17', '-O1', '-Wall', '-Wextra', '-Werror',
                            '-x', 'c++', '-', '-o', str(probe)], input=cpp, text=True, capture_output=True)
    need(built.returncode == 0 and not built.stdout and not built.stderr,
         'Exact old/new C++ low-window stores compile warning-free')
    probe_hash = sha(probe)
    result = subprocess.run([str(probe)], input=wanted['high'] + physical, capture_output=True)
    need(result.returncode == 0 and not result.stderr and result.stdout == wanted['high'] + owned,
         'Actual extracted C++ blocks match independent complete low model; high conserved')
    faults = []
    for label, at in [('air_root', 0x10011c), ('air_first', 0x102920), ('air_last', 0x102947),
                      ('kano_lead', 0x101626), ('sonya_lead', 0x105626)]:
        # The fragment's exact pointer locations are independently taken from
        # typed root records; no synthetic input is ever supplied to the game.
        if label.endswith('lead'):
            at = (reaction.SCRIPTS[0 if label.startswith('kano') else 1] - reaction.BASE)//8 + 24
        bad = bytearray(physical); bad[at] ^= 1
        rejected = subprocess.run([str(probe)], input=wanted['high'] + bad, capture_output=True)
        need(rejected.returncode == 5 and rejected.stderr and not rejected.stdout,
             'Actual compiled pre-write guard rejects altered input: ' + label)
        faults.append(label)
    need(ram['observed'] == wanted, 'Every ORIGINAL actual high/owned/new-GFX byte matches corrected independent models')
    observation_faults = []
    for kind, raw in ram['observed'].items():
        for label, at in [('first', 0), ('middle', len(raw)//2), ('last', len(raw)-1)]:
            bad = bytearray(raw); bad[at] ^= 1
            need(bytes(bad) != wanted[kind], 'Reject changed native observation')
            observation_faults.append(kind + '_' + label)
        need(raw[:-1] != wanted[kind], 'Reject omitted byte')
        observation_faults.append(kind + '_omitted_last')
    paths = [Path(__file__), SOURCE, ROOT / 'source_native_paired_stumble_table/midtunit_m.cpp',
             Path(reaction.__file__), ROOT / 'tools/native_shang_owned_reaction.inc', COMPILER,
             ROOT / 'audit_native_shang_drain_startup/failure.json', ROOT / NAME / 'build-info.json']
    pins = dict(ram['pins'], **{str(p.resolve()): sha(p) for p in paths})
    need(probe.resolve().parent == OUT.resolve() and sha(probe) == probe_hash,
         'Exact temporary compiler output, terminal and unchanged before retirement')
    probe_bytes = probe.stat().st_size
    probe.unlink()
    need(not probe.exists() and all(sha(p) == h for p, h in pins.items()), 'Probe retired; all frozen sources/public playable unchanged')
    report = dict(passed=True, actualNativeInitializedWindowsAccepted=True,
        originalNativeCaptureReusedWithoutReplay=True, actualWindowHashes={k:digest(v) for k,v in wanted.items()},
        actualWindowBytes={k:len(v) for k,v in wanted.items()}, actualNativeIdentity=ram['actual'], nativeExit=ram['nativeExit'],
        originalFullNativeStdoutSHA256=digest(ram['stdout'].encode()), actualChunks=ram['chunks'],
        metadataExpectedOwnedModelIncomplete=True, priorExistingAirThrowBytesOmitted=43,
        newOwnedLeadInByteDelta=24, totalInitializedOwnedByteDelta=67, omittedOffsets=[hex(i) for i in omitted],
        originalFailurePreserved=True, exactExtractedCppSHA256=digest(cpp.encode()),
        actualCppWholeHighLowConservationAccepted=True, actualCppInputFaultsRejected=faults,
        observationFaultsRejected=observation_faults, ownTypedReactionRows=rows,
        retiredTemporaryCompilerOutputBytes=probe_bytes, inputHashes=pins,
        originalNaturalIntegrationRequirements=guard['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=guard['originalRemainingWorkGroups'],
        nativeGameplayRepairAccepted=False, artworkRuntimeAccepted=False, audioAccepted=False, fullPortAcceptance=False,
        fullCurrentGraphicsRegionNotExported=True, fullNewGraphicsReservationVerified=True,
        physicalInputs=0, gameWrites=0, newROMCopies=0, newRawGameplayMedia=0, newZIPs=0,
        publicPlayableChanged=False, rawNativeBytesKeptInOriginalRAMOnly=True, goalStatus='active')
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    # Release only after the original whole observation and source receipts exist.
    ram.clear()
    print(json.dumps(dict(passed=True, actualNativeInitializedWindowsAccepted=True,
                         actualWindowHashes=report['actualWindowHashes'], priorOmittedBytes=43,
                         originalRAMReleased=True, nativeGameplayRepairAccepted=False)), flush=True)
    return report
