"""Bounded passive floor-anchor review of the completed actual low-kick case."""
def send():
    import hashlib,json,os,socket,struct,sys,traceback
    answer=dict(hostPID=os.getpid(),gameWrites=0,newGames=0)
    try:
        assert os.getpid()==5752
        prepared=sys.modules['prepare_native_selector_lowkick_after_host_exit_scoped']
        held=prepared.NATIVE_HANDLES[prepared.SCOPE['KEY']]
        assert held['identity']['ProcessId']==21456 and held['process'].poll()==0
        guest=prepared.STATE['guest']; offset=(0xff907f70-0xff800000)//8
        pointer=struct.unpack_from('<I',guest,offset)[0]
        table=struct.unpack_from('<19H',guest,(pointer-0xff800000)//8)
        assert table[17:]==(134,135)
        fields=sys.modules['__main__'].control_fields
        assert len(fields)==1063
        for r in fields:
            assert (r['vid'],r['id'])==(17,18)
            assert r['vfloor']+table[r['vid']]==r['stage_floor']
            assert r['floor']+table[r['id']]==r['stage_floor']
        answer.update(passed=True,nativeIdentity=held['identity'],currentWholeGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),
            actualFloorTablePointer=hex(pointer),actualFloorTable=list(table),actualLiveCallbacks=len(fields),
            bothPhysicalFloorAnchorsAgreeWithStageBaseline=True,
            graphicalSoleParityAccepted=False,allStagesAccepted=False,fullPortAcceptance=False)
    except Exception: answer.update(passed=False,error=traceback.format_exc())
    packet=json.dumps(answer).encode(); assert len(packet)<10000
    try:
        with socket.create_connection(('127.0.0.1',51465),timeout=5) as conn:
            conn.sendall(struct.pack('<I',len(packet))+packet)
    except OSError: pass
send()
