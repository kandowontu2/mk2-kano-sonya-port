"""Keep each physical slot's actual source-clock playback position."""
import inspect
import qualify_bounded_twohuman_square_rise_cleanup as previous

def main():
    gate=inspect.getsource(previous.gate)
    gate=gate.replace('def gate(rows,side,length):','def gate(rows,side,length):\n    stopped=5464 if side==1 else 5471')
    gate=gate.replace("r['pos']=='5464.00000000'","Decimal(r['pos'])==stopped")
    gate=gate.replace('0<5464<length','0<stopped<length').replace('stoppedSample=5464,unplayedSamples=length-5464','stoppedSample=stopped,unplayedSamples=length-stopped')
    source=inspect.getsource(previous.main).replace('audit_bounded_twohuman_square_rise_cleanup_checked','audit_bounded_twohuman_square_slot_positions_checked')
    source=source.replace("['pos']='5465.00000000'","['pos']=str((5464 if side==1 else 5471)+1)")
    source=source.replace('unplayedSamples=length-5464','results={key:value["unplayedSamples"] for key,value in results.items()}')
    namespace=dict(previous.__dict__);namespace['__file__']=__file__
    exec(compile(gate+'\n'+source,__file__+'::actual_slot_positions','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
