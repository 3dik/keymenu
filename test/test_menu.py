import unittest
from unittest import mock
import sys
import io

from keymenu import menu

ESC = '\x1b'
EMPTY = """The list is empty.
"""
CHOOSE = """
Choose: 
"""
ABORT = """aborted.
"""

class TestMenu( unittest.TestCase ):

    def setUp( self ):
        self._term_in = mock.Mock()
        self._term_out = io.StringIO()

    def test_init( self ):
        """ Just test for exceptions at initialization """
        c = self._create_blind_menu
        c( dict() )

        data = self._get_data()

        c( { 'a':data['full'] } ) #ok, one item
        c( { 'p':data['full'], 'b':data['full'] } ) #ok, duplicate item
        c( { ' ':data['full'], 'b':data['no_display'] } ) #ok, no display
        c( { 'Ü':data['no_display'], 'b':data['unknown'] } ) #ok, unknown

        self.assertRaises( menu.MissingReturnMember,
                           c, {'a':data['no_return'] } )

        c_with_key = lambda key: c({key:data['full']})
        invalids = [ None, '', 'ab', 3, 3.6, '\x1b' ]
        for key in invalids:
            self.assertRaises( menu.InvalidKey, c_with_key, key )
    
    def test_empty( self ):
        """test: escaping, empty keymap, typing unmapped key"""

        m = self._create_simu( dict(), 'a' + ESC + 'ignoreme' )
        val = m.ask()
        out = EMPTY+CHOOSE+self._get_notmapped('a')+EMPTY+CHOOSE+ABORT
        self.assertEqual( out, self._term_out.getvalue() )
        self.assertEqual( None, val )
        self.assertEqual( m._get_term_char.call_count, 2 )

    def test_listing( self ):
        """test:
        * listing normal items with both members
        * listing items without display
        * listing items with extra members
        * multiple calls of ask
        * selecting an item which has a display
        * selecting after typing unmapped keys
        * the last char is the selecting one
        """
        for i in range( 1, 3 ):
            data = self._get_data()
            keymap = { 'a':data['full'],
                       'b':data['no_display'],
                       'c':data['unknown'] }
            m = self._create_simu( keymap, 'lla' )
            val = m.ask()
            stuff = """[a] alpha
[b] drinking
[c] delta
"""
            out = stuff + CHOOSE + self._get_notmapped('l' )
            out += out + stuff + CHOOSE
            self.assertEqual( i*out, self._term_out.getvalue() )
            self.assertEqual( val, 'kissing' )
            self.assertEqual( m._get_term_char.call_count, 3 )

    def test_direct( self ):
        """test:
        * choosing an item which does not have a display
        * choosing without typing unmapped keys before
        """
        keymap = { 'a': {'display':'aha', 'return':'jeje' },
                   'b': {'return':'bla' } }
        m = self._create_simu( keymap, 'bi' )
        out = """[a] aha
[b] bla
"""
        out += CHOOSE
        val = m.ask()
        self.assertEqual( out, self._term_out.getvalue() )
        self.assertEqual( 'bla', val )
        self.assertEqual( m._get_term_char.call_count, 1 )


    def _get_notmapped( self, char ):
        return "\"{0}\" is not mapped.\n\n".format( char )

    def _create_simu( self, keymap, typed_chars ):
        """Create Menu instance and simulate typed characters

        I don't wanna fiddle with these term attributes, so I just mock
        the getter function."""
        smenu = menu.Menu( keymap, self._term_in, self._term_out )
        smenu._get_term_char = mock.Mock()
        smenu._get_term_char.side_effect = typed_chars
        return smenu

    def _create_blind_menu( self, keymap ):
        return menu.Menu( keymap, None, None )

    def _get_data( self ):
        full = { 'display':'alpha', 'return':'kissing' }
        no_display = { 'return':'drinking' }
        no_return = { 'display':'gamma' }
        unknown = { 'return':'delta', 'job':'rockstar' }

        return { 'full':full,
                 'no_display':no_display,
                 'no_return':no_return,
                 'unknown':unknown }
