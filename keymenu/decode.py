import json

class DuplicateKey( Exception ): pass

def _paircheck_hook( pairs ):
    """By default, pythons json module does not forbid redundant keys"""
    keys = list( map( lambda item: item[0], pairs ) )
    if 1 != max( map( keys.count, keys ) ):
            raise DuplicateKey()

    return dict( pairs )

def with_uniqueness_check( json_text ):
    return json.loads( json_text, object_pairs_hook=_paircheck_hook )
