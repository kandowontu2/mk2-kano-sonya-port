"""Trace actual native announcer table routes before adding own speech slots."""
import hashlib
import json
from pathlib import Path
import re
import wave

PORT=Path(__file__).resolve().parent
ROOT=PORT.parents[1]
BUILD=PORT.parent/'baseline/mk2-rebuild-main'
source={name:(BUILD/'srcp'/name).read_text() for name in ('MKSOUND.ASM','MKSEL.ASM','MAIN.ASM')}
sound=source['MKSOUND.ASM']
section=sound.split('\ntriple_sndtab2\n',1)[1].split('\ntriple_end2\n',1)[0]
entries=[line.strip() for line in section.splitlines() if line.lstrip().startswith('.word')]
assert re.search(r'selsp3\s+addi\s+01cH,a10\s+move\s+a10,a0\s+calla\s+triple_sound2',source['MKSEL.ASM'])
winner=source['MAIN.ASM'].split('\nwinner_speech\n',1)[1].split('\nks_pf_kano_win\n',1)[0]
values=[]
for line in winner.splitlines():
    if line.lstrip().startswith('.word'):
        text=line.split('.word',1)[1].split(';',1)[0]
        for word in text.split(','):
            word=word.strip()
            values.append(int(word[:-1],16) if word.lower().endswith('h') else int(word))
assert len(values)==19 and values[17:]==[0,0]
routes=[]
for actor,name in ((17,'kano'),(18,'sonya')):
    index=0x1c+actor
    assert index<len(entries)
    clips=[]
    for suffix in ('select','wins'):
        clip=ROOT/f'samples/mk2ks/{name}_{suffix}.wav'
        with wave.open(str(clip),'rb') as wav:
            assert wav.getnchannels()==1 and wav.getsampwidth()==2
            clips.append(dict(file=str(clip),sha256=hashlib.sha256(clip.read_bytes()).hexdigest().upper(),
                rate=wav.getframerate(),frames=wav.getnframes()))
    routes.append(dict(actorID=actor,name=name,selectionTable='triple_sndtab2',
        selectionIndex=index,selectionEntry=entries[index],winnerIndex=values[actor],
        winnerSilent=True,ownSpeechImplemented=False,availableClips=clips))
assert 'flash cursor' in routes[0]['selectionEntry']
assert 'player joins in' in routes[1]['selectionEntry']
report=dict(scope='Native announcer routing source audit, not runtime voice acceptance',
    routes=routes,sourceSHA256={name:hashlib.sha256((BUILD/'srcp'/name).read_bytes()).hexdigest().upper() for name in source},
    requiredFix='Append own boss-voice entries to triple_sndtab2; explicitly map IDs17/18 in select_speech and winner_speech; build own DCS playlists.',
    existingMoveEntriesUseDifferentTable=True,releaseReady=False)
(PORT/'generated_dcs/ANNOUNCER_ROUTE_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
