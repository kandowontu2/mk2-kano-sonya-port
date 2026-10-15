"""Original entire asset oracle, actual48kHz recording path to Windows NUL.

The sink activates original native48kHz generation without persisting a WAV
transport. Complete PCM remains in the RAM collector. Prior11k rejection stays.
"""
import inspect
import build_kano_launch_oracle_v6632 as original
OUT=original.ROOT/'audit_v6635_kano_launch_native48k'
source=inspect.getsource(original.run)
before="'-video','none','-sound','none','-samplerate','48000'"
original.need(source.count(before)==1,'Only actual native recording sink changes')
source=source.replace(before,"'-video','none','-sound','none','-samplerate','48000','-wavwrite','NUL'",1)
before="ROOT/'mk3/mk3-maincpu.bin',*list((ROOT/'mk3').glob('*music_spch*'))]"
original.need(source.count(before)==1,'Retain entire original collector and failed-format/source provenance')
source=source.replace(before,"ROOT/'mk3/mk3-maincpu.bin',Path(original.__file__),ROOT/'audit_v6633_kano_launch_donor_oracle/README.md',*list((ROOT/'mk3').glob('*music_spch*'))]",1)
namespace=dict(original.__dict__,__file__=__file__,OUT=OUT,original=original)
exec(compile(source,__file__+'::complete_native48k_oracle_collector','exec'),namespace)
source=inspect.getsource(original.main)
exec(compile(source,__file__+'::entire_original_source_audio_asset_model','exec'),namespace)
if __name__=='__main__':namespace['main']()
