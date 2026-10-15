"""Complete unchanged four-case selection/ladder/first-match gates, current EXE."""
import code
import json
import traceback
from pathlib import Path
import capture_launch_candidate_ui as original
import native_ai_response_full_context as current

if __name__=='__main__':
    original.current=current
    original.BASE=current.ROOT/'audit_native_current_ui_ram'
    original.OUT=current.ROOT/'audit_native_current_ui_checked'
    try:
        accepted=original.run()
    except Exception as error:
        failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                     completedCases=original.COMPLETED,fullPortAcceptance=False)
        current.need(not original.OUT.exists(),'Never overwrite an earlier executed result')
        original.OUT.mkdir();original.save(original.OUT/'failure.json',failure)
        print(json.dumps(dict(passed=False,error=repr(error))),flush=True)
    code.interact(banner='Same current-build UI jobs terminal; all original images and logs retained in RAM.',
                  local=dict(ui=original,captures=original.RAM_CASES))
