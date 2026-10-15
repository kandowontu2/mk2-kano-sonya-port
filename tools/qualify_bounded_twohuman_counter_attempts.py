"""Keep all three naturally losing counters as target-absence evidence."""
import inspect,json
import qualify_bounded_twohuman_bicycle_command as previous

def main():
    results={}
    for policy in ('early','approach','uppercut'):
        source=inspect.getsource(previous.main)
        source=source.replace('audit_bounded_twohuman_bicycle_counter_runtime',f'audit_bounded_twohuman_bicycle_{policy}_counter_runtime')
        source=source.replace("'command_check.json'","'target_absence_check.json'")
        source=source.replace('840','842')
        namespace=dict(previous.__dict__);namespace['__file__']=__file__
        exec(compile(source,__file__+'::'+policy,'exec'),namespace);namespace['main']()
        path=previous.sync.ROOT/f'audit_bounded_twohuman_bicycle_{policy}_counter_runtime/target_absence_check.json'
        results[policy]=dict(report=str(path),sha256=previous.sync.sha(path))
    out=previous.sync.ROOT/'audit_bounded_twohuman_counter_attempts_checked';assert not out.exists()
    out.mkdir();(out/'report.json').write_text(json.dumps(dict(passed=True,results=results,incomingInterruptionAccepted=False,fullGoalComplete=False),indent=2)+'\n')

if __name__=='__main__':main()
