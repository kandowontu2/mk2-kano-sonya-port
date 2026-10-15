"""Preserve6215 failure; original sample inactivity is source_num==-1.

samples.cpp deliberately retains source_len and position when the stream
ends. Full original source code and all other callback/PCM gates retained.
"""
import argparse,inspect,json,traceback
import capture_current_subzero_enabled_audio_v6215 as prior
original=prior.original
ROOT,need,sha=original.ROOT,original.need,original.sha

def run(fighter,side):
 source_path=ROOT/original.current.NAME/'input_sources/mame-mkp/src/devices/sound/samples.cpp'
 if not source_path.exists():source_path=ROOT/'mame-mkp/src/devices/sound/samples.cpp'
 source=source_path.read_text()
 need('chan.source = nullptr;\n\t\t\t\t\t\t\tchan.source_num = -1;'in source and
      'chan.source_len = sample.data.size();'in source,
      'Whole original end-of-stream pointer/number invalidation retains length')
 code=inspect.getsource(prior.adapted_run)
 def replace(before,after):
  nonlocal code
  need(code.count(before)==1,'Only exact enabled-source lifetime repair')
  code=code.replace(before,after,1)
 replace('audit_v6216_current_subzero_','audit_v6218_current_subzero_')
 replace("r['length']=='0'and r['loop']=='0'","r['sample']=='4294967295'and r['loop']=='0'")
 replace('Path(original.__file__),Path(current.__file__),Path(model.__file__),',
         'Path(original.__file__),Path(prior.__file__),source_path,Path(current.__file__),Path(model.__file__),')
 replace("scope=dict(original.run.__globals__,original=original,__file__=__file__)",
         "scope=dict(original.run.__globals__,original=original,prior=prior,source_path=source_path,__file__=__file__)")
 namespace=dict(vars(prior),prior=prior,source_path=source_path,__file__=__file__)
 exec(compile(code,__file__+'::entire6215_native_source_inactivity','exec'),namespace)
 return namespace['adapted_run']()(fighter,side)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 try:run(args.fighter,args.side)
 except Exception as error:
  folder=ROOT/f'audit_v6218_current_subzero_{args.fighter}_p{args.side}_native_audio'
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if folder.exists():original.save(folder/'failure.json',failure)
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
