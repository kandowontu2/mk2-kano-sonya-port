"""Same kiss pixel gate; supply the anchored state parser in generated scope."""
import inspect,sys
import qualify_bounded_kitana_kiss_body_pixels as previous
from qualify_bounded_stock_head_body_footprints import PREFIX

def main(side):
    source=inspect.getsource(previous.main)
    assert source.count('namespace.update(')==1
    source=source.replace('namespace.update(','namespace.update(PREFIX=prefix,')
    source=source.replace('audit_bounded_kitana_kiss_body_pixels_p{requested_side}_checked','audit_bounded_kitana_kiss_body_pixels_scoped_p{requested_side}_checked')
    namespace=dict(previous.__dict__);namespace.update(prefix=PREFIX,__file__=__file__)
    exec(compile(source,__file__+'::parser_scope_only','exec'),namespace);namespace['main'](side)

if __name__=='__main__':main(int(sys.argv[1]))
