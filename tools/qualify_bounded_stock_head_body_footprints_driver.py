"""Compare every baseline driver record; separately allow observer STOP."""
import qualify_bounded_stock_head_body_footprints_scoped as scoped

def driver_states(folder,fighter):
    return [(tag,row) for tag,row in scoped.driver_states(folder,fighter) if tag!='STOP']

if __name__=='__main__':
    scoped.original.states=driver_states
    scoped.original.main()
