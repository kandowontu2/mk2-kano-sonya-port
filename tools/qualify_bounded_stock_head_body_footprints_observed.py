"""Observed ages 1..30 only: action callback occurred after age-zero DMA."""
import qualify_bounded_stock_head_body_footprints_driver as driver

original=driver.scoped.original
raw_gate=original.pixel_gate

def observed_gate(summaries,opaque,fifo,ready,lo,hi):
    assert (lo,hi)==(0,30)
    return raw_gate(summaries,opaque,fifo,ready,1,30)

if __name__=='__main__':
    original.states=driver.driver_states
    original.pixel_gate=observed_gate
    original.main()
