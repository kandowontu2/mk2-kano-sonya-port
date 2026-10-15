"""Keep asset-constructor rejection; include its complete original proof prefix."""
import json
from pathlib import Path
import qualify_native_selector_sonya_cpu_air_channels as rejected

FAILURE=rejected.OUT/'failure.json'
rejected.need(json.loads(FAILURE.read_text())['error']=="NameError(\"name 'qualified' is not defined\")",
              'Actual full source-event constructor omitted its original asset proof prefix; preserve failure')
source=Path(rejected.__file__).read_text()
for before,after in (
    ("OUT=ROOT/'audit_native_selector_sonya_cpu_air_channels_checked'",
     "OUT=ROOT/'audit_native_selector_sonya_cpu_air_channels_assets_checked'"),
    ("first=source.index(' events=[]')", "first=source.index(' qualified=json.loads(')"),
    ('for p in (Path(__file__),parent,Path(packets.__file__),',
     'for p in (Path(__file__),Path(rejected.__file__),FAILURE,parent,Path(packets.__file__),'),
    ('completeRecorded19ChannelClocksAccepted=True,',
     'completeRecorded19ChannelClocksAccepted=True,originalAssetProofPrefixRejectionPreserved=True,')):
    rejected.need(source.count(before)==1,'Only whole original asset proof prefix and failure preservation boundary')
    source=source.replace(before,after,1)
exec(compile(source,__file__+'::whole_original_event_asset_proof_prefix','exec'))
