import tty
import termios

class MissingReturnMember( Exception ): pass
class InvalidKey( Exception ) : pass

class Menu():
    """User interface for the selection of an item with a keymap"""

    ESC = '\x1b'

    def __init__( self, keymap, term_in, term_out ):
        if not all( map( lambda key: 'return' in keymap[key], keymap ) ):
            raise MissingReturnMember()
        if not all( map( lambda key: self._is_valid_key(key), keymap ) ):
            raise InvalidKey()

        self._keymap = keymap
        self._term_in = term_in
        self._term_out = term_out

    def print_items( self ):
        if not len( self._keymap ):
            self._print( 'The list is empty.' )
        for key,item in self._keymap.items():
            name = item.get( 'display', item['return'] )
            line = "[{0}] {1}".format( key, name )
            self._print( line )

    def ask( self ):
        while( True ):
            self.print_items()

            #no _print because we delay the trailing \n
            self._term_out.write( "\nChoose: " )
            try:
                char = self._get_term_char()
            finally:
                self._term_out.write( "\n" )

            if self.ESC == char:
                self._print( "aborted." )
                return None
            if char in self._keymap:
                return self._keymap[char]['return']

            error = "\"{0}\" is not mapped.\n".format( char )
            #I don't think this should be put to stderr, it's rather feedback
            # for the user, not a "real" error.
            self._print( error )

    def _is_valid_key( self, key ):
        special = [ None, '', self.ESC ]
        if key in special:
            return False
        if not isinstance( key, str ):
            return False
        return 1 == len( key )

    def _print( self, obj ):
        print( obj, file=self._term_out )

    def _get_term_char( self ):
        """Read a single character from the terminal
        
        Does not wait for a newline.
        Compare: https://github.com/ActiveState/code/tree/master/recipes/Python/134892_getchlike_unbuffered_character_reading_stdboth
        """
        old_attr = termios.tcgetattr( self._term_in )
        try:
            tty.setraw( self._term_in )
            char = self._term_in.read( 1 )
        finally:
            termios.tcsetattr( self._term_in, termios.TCSADRAIN, old_attr )
        return char
