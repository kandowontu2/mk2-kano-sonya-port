"""Use the complete quoted sample list, then omit its *mk2ks set marker."""
import inspect
import audit_campaign_source_conservation_v2 as previous


def main():
    source = inspect.getsource(previous.main)
    before = "names = re.findall(r'\"([^\"*][^\"]*)\"', block)"
    after = "names = [name for name in re.findall(r'\"([^\"]+)\"', block) if not name.startswith('*')]"
    previous.original.need(source.count(before) == 1, 'Exact quoted-list parser correction only')
    source = source.replace(before, after, 1)
    before = "OUT=original.ROOT / 'audit_campaign_source_conservation_v2'"
    previous.original.need(source.count(before) == 1, 'Fresh immutable successor output')
    source = source.replace(before, "OUT=original.ROOT / 'audit_campaign_source_conservation_v3'", 1)
    scope = dict(vars(previous), __file__=__file__)
    exec(compile(source, __file__ + '::whole_shared_sample_audit_quoted_list_fix', 'exec'), scope)
    scope['main']()


if __name__ == '__main__':
    main()
