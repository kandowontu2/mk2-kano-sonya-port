"""Split pose is a terminated descriptor-pointer list, not a raw descriptor."""
import inspect
import prepare_bounded_kung_lao_split_descriptors as previous

def main():
    tail=previous.TAIL
    before='local descriptor=first+index*64';assert tail.count(before)==1
    tail=tail.replace(before,'local pose=first+index*64\n   local descriptor=p:read_u32(pose)\n   assert(p:read_u32(pose+32)==0)')
    tail=tail.replace('pointer=%08X width=', 'pose=%08X pointer=%08X width=')
    tail=tail.replace('ident,index,descriptor,p:read_u16(descriptor)', 'ident,index,pose,descriptor,p:read_u16(descriptor)')
    source=inspect.getsource(previous.main).replace('audit_bounded_kung_lao_split_descriptors_preparation','audit_bounded_kung_lao_split_descriptor_lists_preparation').replace('audit_bounded_kung_lao_split_descriptors_runtime','audit_bounded_kung_lao_split_descriptor_lists_runtime')
    namespace=dict(previous.__dict__);namespace.update(__file__=__file__,TAIL=tail)
    exec(compile(source,__file__+'::terminated_pose_lists','exec'),namespace);namespace['main']()

if __name__=='__main__':main()
