"""Preserve6367 preflight; correct its non-runtime sample-source section end."""
import argparse,code,inspect,json,traceback
import capture_current_cpu_blade_knife_audio_v6367 as original
source=inspect.getsource(original.main)
before="source.index('void samples_device::start(')"
after="source.index('//  INTERNAL HELPERS',source.index('void samples_device::sound_stream_update'))"
original.need(source.count(before)==1,'Only passive source-slice endpoint repair')
source=source.replace(before,after,1)
scope=dict(original.__dict__,__file__=__file__)
exec(compile(source,__file__+'::whole6367_source_slice_fix','exec'),scope)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');parser.add_argument('--hold',action='store_true');args=parser.parse_args()
 try:scope['main'](args.preflight)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if original.OUT.exists():original.original.original.save(original.OUT/'failure.json',failure)
  print(json.dumps(failure,indent=2),flush=True)
  prepared=scope.get('SCOPE')
  if args.hold and prepared and 'LAST_CAPTURE'in prepared:
   code.interact(banner='Native terminal; actual PCM/DAC retained in RAM, no native rerun.',
                local=dict(capture=prepared['LAST_CAPTURE'],module=original,mix=original.original.mix))
  raise SystemExit(1)
