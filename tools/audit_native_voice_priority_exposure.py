"""Separate unchanged stock queue behavior from port-specific voice routing.

This is a source equivalence proof, NOT runtime coverage of unobserved sound
branches or acceptance of every finisher's body, voice, or sample lifetime.
"""
import hashlib
import json
import struct
import subprocess
from pathlib import Path
import kano_ball_launch_context_v6642 as current

ROOT, need = current.ROOT, current.need
OUT = ROOT/'audit_native_voice_priority_exposure'
off = lambda address: (address-0xff800000)//8
SPANS = (
    ('native random core', 0xff80e980, 0xff80eb70),
    ('both sound cue banks', 0xffa0ef20, 0xffa12180),
    ('packed selector', 0xffa12180, 0xffa122a0),
    ('male/female extraction and queue', 0xffa122d0, 0xffa12d90),
    ('Pit fall voice producer', 0xff8eb560, 0xff8eb620),
    ('Pit impact voice producer', 0xff85c560, 0xff85c620),
    ('Pit particle cue producer', 0xff9b0940, 0xff9b09a0),
)


def digest(raw):
    return hashlib.sha256(raw).hexdigest().upper()


def gate(guest, stock):
    need(len(guest) == len(stock) == 1048576, 'Complete actual-sized guest and stock sources')
    conserved = []
    for name, lo, hi in SPANS:
        raw = guest[off(lo):off(hi)]
        need(raw == stock[off(lo):off(hi)], 'Whole unchanged '+name)
        conserved.append(dict(name=name, firstPC=f'{lo:08X}', endPC=f'{hi:08X}',
                              bytes=len(raw), sha256=digest(raw)))
    # Exact TMS predicate extension: test Jade16 and Sonya18, preserve A2,
    # then rejoin the original female or male byte extraction. No proxy ID.
    site = off(0xffa122a0)
    opcode, destination = struct.unpack_from('<HI', guest, site)
    need(opcode == 0xc080 and destination % 16 == 0 and
         0xff800000 <= destination <= 0xffffff40, 'Native JA gender extension')
    wanted = (0x0b42, 0xffef, 0xca06, 0x0b42, 0xffed, 0xca03,
              0xc080, 0x22d0, 0xffa1, 0xc080, 0x23b0, 0xffa1)
    need(struct.unpack_from('<12H', guest, off(destination)) == wanted,
         'Exact nondestructive Jade16/Sonya18 compares and original male/female destinations')
    need(guest[site+6:off(0xffa122d0)] == stock[site+6:off(0xffa122d0)],
         'Only original final gender compare/branch replaced')
    voices = []
    for name, pc, packed in (('fall',0xff8eb5b0,0xcbcbcbcd),
                             ('impact',0xff85c5b0,0xccccccce)):
        need(struct.unpack_from('<6H', guest, off(pc)) ==
             (0x09e1, packed & 65535, packed >> 16, 0x0d5f, 0x2210, 0xffa1),
             'Exact original packed '+name+' producer')
        for identity in (17,18):
            for state in (0,1):
                # These are the exact unchanged shift sequences shown by
                # the conserved original extraction instructions.
                cue = (packed & 255) if identity == 18 else (packed >> (24 if state == 1 else 16)) & 255
                header, packet = struct.unpack_from('<HH', guest, off(0xffa0ef20)+cue*4)
                need(header >> 8 == 0x58 and header < 0x8000,
                     'Added victim Pit voices use original general priority58 cues')
                voices.append(dict(phase=name, actorID=identity, actorState=state,
                                   cue=f'{cue:02X}', priority=header >> 8,
                                   duration=header & 255, packet=packet))
    # General dispatch caps its bank at FFA10EE0. Priority71 resides only
    # in the separate direct bank; it is not one of these Pit voice cues.
    bank = guest[off(0xffa0ef20):off(0xffa10ee0)]
    direct = guest[off(0xffa10ee0):off(0xffa11a40)]
    need(not any(h >> 8 == 0x71 for h,p in struct.iter_unpack('<HH',bank)),
         'No general bank cue has priority71')
    special = [dict(address=f'{0xffa10ee0+i*32:08X}',header=h,packet=p)
               for i,(h,p) in enumerate(struct.iter_unpack('<HH',direct)) if h >> 8 == 0x71]
    need(len(special) == 23, 'All original direct-bank priority71 entries retained')
    return dict(passed=True, conservedSources=conserved, originalGenderExtension=destination,
                trueAddedVictimVoiceRoutes=voices, unchangedDirectBankPriority71Rows=special,
                nativeQueueAllInputSourceEquivalence=True,
                suppressionAndSpecial71RuntimeCoverage=False,
                allPitContextsExcludePriority71=False, allFinisherAudioAccepted=False,
                fullPortAcceptance=False)


def main():
    need(not OUT.exists(), 'Fresh source exposure audit')
    guest = current.expected()
    stockpath = ROOT/'mk2/mk2-maincpu.bin'
    stock = stockpath.read_bytes()
    result = gate(guest,stock)
    destination = result['originalGenderExtension']
    rejected = []
    for label, at in (('native suppression instruction',off(0xffa129d0)),
                      ('original cue table',off(0xffa0ef20)),
                      ('Sonya18 gender comparison',off(destination)+8),
                      ('original female destination',off(destination)+20)):
        altered = bytearray(guest)
        altered[at] ^= 1
        try:
            gate(altered,stock)
        except ValueError as error:
            rejected.append(dict(fault=label,rejected=str(error)))
        else:
            raise ValueError('Actual source corruption admitted: '+label)
    need(len(rejected) == 4 and gate(guest,stock) == result, 'Four actual source mutations rejected; full positive restored')
    result.update(actualSourceFaultsRejected=rejected, candidate=current.NAME,
                  entireGuestSHA256=digest(guest), stockSHA256=digest(stock),
                  sourceSHA256=digest(Path(__file__).read_bytes()),
                  nextAction='Retain unchanged queue semantics as source-equivalent; do not hunt stock priority71 during these priority58 Pit voice routes. Runtime-check concrete added-body/voice-owner/teardown and new launch-channel exposure, then final matching CMD/ZIP.',
                  newBuilds=0,newROMCopies=0,newRawMedia=0,newNativeBoots=0)
    OUT.mkdir()
    path = OUT/'report.json'
    path.write_text(json.dumps(result,indent=2)+'\n')
    before = digest(path.read_bytes())
    subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True,check=True)
    need(digest(path.read_bytes()) == before, 'Lossless bounded evidence compression')
    print(json.dumps(dict(passed=True, conservedSourceRanges=len(SPANS),
                         trueAddedVictimVoiceRoutes=len(result['trueAddedVictimVoiceRoutes']),
                         actualSourceFaultsRejected=len(rejected), runtimePriorityCoverage=False)))


if __name__ == '__main__':
    main()
