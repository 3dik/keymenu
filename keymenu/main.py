#!/usr/bin/env python3

import sys
import argparse

import menu
import decode

def main():
    descr = 'dynamic keymap menu for the terminal'
    long_descr = 'It Reads a JSON keymap from stdin and lists all entries ' \
                 'until the user presses one of the mapped keys. ' \
                 'The value of the chosen item is written to stdout.'
    parser = argparse.ArgumentParser( description=descr, epilog=long_descr )
    parser.add_argument( '--version', action='version',
                         version='keymenu 0.0' )
    parser.parse_args()

    keymap = decode.with_uniqueness_check( sys.stdin.read() )
    sys.stdin.close()

    term = '/dev/tty'
    with open( term ) as term_in, open( term, 'w' ) as term_out:
        my_menu = menu.Menu( keymap, term_in, term_out )
        value = my_menu.ask()

    if value:
        print( value )

if '__main__' == __name__:
    main()
