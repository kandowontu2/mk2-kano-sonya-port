"""Exactly the prior physical secret/return/attract policy on repaired build."""
import argparse
import code
from pathlib import Path
import capture_natural_smoke_route as host
import stock_slideshow_row40_context as current


def run(attempt='stock_row40_repair_full_route'):
    host.current=current
    host.GRAPHICS_PROBE=current.ROOT/'mk2ks_stock_slideshow_row40_regression.lua'
    return host.run('sonya',2,attempt,2400,True,extra_pin_paths=(Path(__file__).resolve(),))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--hold',action='store_true')
    p.add_argument('--attempt',default='stock_row40_repair_full_route');args=p.parse_args()
    capture=run(args.attempt)
    if args.hold:
        code.interact(banner='Same repaired candidate native terminal; original screen bytes retained in RAM.',
                      local=dict(capture=capture))
