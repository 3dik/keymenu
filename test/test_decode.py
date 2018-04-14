import unittest

from keymenu import decode

class TestDecode( unittest.TestCase ):
    def test_with_uniqueness_check( self ):
        text_begin = """{
"a":"first",
"b":[1,2]"""

        #quickly check if basic parsing still works
        data = decode.with_uniqueness_check( text_begin + '}' )
        cmp_dict = { 'a':'first', 'b':[1,2] }
        self.assertEqual( cmp_dict, data )

        broken = text_begin + ',"a":777}'
        self.assertRaises( decode.DuplicateKey,
                           decode.with_uniqueness_check, broken )
