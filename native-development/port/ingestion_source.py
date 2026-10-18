"""Own native ingestion animation dispatch, preserving original roster rows."""
from arm_rip_source import lookup

OLD, NEW = lookup('sucked_in_anis', 'get_char_long', 'ks_kano_ingested',
                  'ks_sonya_ingested', 'ingest')


def integrate(text):
    assert text.count(OLD) == 1
    text = text.replace(OLD, NEW)
    assert text.count('\nr_body_suck\n') == 1
    return text.replace('\nr_body_suck\n',
        '\n\t.ref ks_kano_ingested,ks_sonya_ingested\nr_body_suck\n')
