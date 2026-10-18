"""Read-only source audit; never equate bounded table safety with a campaign win."""
import hashlib
import json
from pathlib import Path
import re
import zipfile
from ending_source import winner as extend_winner,story as extend_story,cast as extend_cast
from prepare_game_candidate import ZIP

PORT=Path(__file__).resolve().parent
SRC=PORT.parent/'baseline/mk2-rebuild-main/srcp'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
end=(SRC/'MKEND.ASM').read_text()
unzip=(SRC/'UNZIP.ASM').read_text()
def rows(text,start,stop):
    body=text.split('\n'+start+'\n',1)[1].split('\n'+stop,1)[0]
    return [line.split(';',1)[0].strip().split(None,1)[1].split(',')
            for line in body.splitlines() if line.strip().startswith('.long')]
winner=[v.strip() for row in rows(end,'end_winner_text','ew_hh') for v in row]
first=rows(unzip,'end_text_1','end_text_2')
second=rows(unzip,'end_text_2','pf_hh_end_1a')
assert all(len(row)==3 for row in first+second)
assert 'addi\tend_winner_text,a0' in end
assert 'addi\tend_text_1,a0' in unzip and 'addi\tend_text_2,a0' in unzip
assert '\tjsrp\tshow_a0_ending' in end
cases=[]
with zipfile.ZipFile(ZIP) as archive:
    original={name:archive.read('mk2-rebuild-main/src/'+name).decode('cp437').replace('\r\n','\n')
              for name in ('MKEND.ASM','UNZIP.ASM')}
source_dispatch_verified=(extend_cast(extend_winner(original['MKEND.ASM'])).rstrip()==end.rstrip()
                          and extend_story(original['UNZIP.ASM']).rstrip()==unzip.rstrip())
for identity,name in ((17,'Kano'),(18,'Sonya')):
    cases.append(dict(character=name,identity=identity,
        originalFallbackWinnerPointer=winner[identity] if identity<len(winner) else None,
        dedicatedWinnerAndStorySourceVerified=source_dispatch_verified,
        firstStoryRowInBounds=identity<len(first),secondStoryRowInBounds=identity<len(second),
        firstZipIndex=16+identity*2,secondZipIndex=17+identity*2))
report=dict(scope='Direct-index native campaign-ending source audit, not runtime completion',
    sourceSHA256={name:sha((SRC/name).read_bytes()) for name in ('MKEND.ASM','UNZIP.ASM')},
    winnerPointerEntries=len(winner),firstStoryRows=len(first),secondStoryRows=len(second),
    cases=cases,dedicatedDispatchMatchesGenerator=source_dispatch_verified,
    originalFallbackTablesStillNotValidForAddedIDs=True,
    addedCharacterEndingsRuntimeVerified=False,campaignVerified=False,releaseReady=False)
(PORT/'CAMPAIGN_ENDING_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
