# keymenu

Keymenu is a keymap based menu for the terminal. It reads a JSON encoded keymap
from standard input and displays a list of all entries and their key bindings.
When the user presses one of the defined keys, the string mapped by this key is
written to standard output.

Keymenu is highly inspired by tools like
[dmenu](https://tools.suckless.org/dmenu/) and
[slmenu](https://bitbucket.org/rafaelgg/slmenu). There are [plenty of other
similar tools](https://github.com/D630/doc/wiki/Apps%3A-Menus%2C-Picker-etc).
However, in contrast to them, this program is intended to be used only for
small lists. This enables keymenu to use key bindings instead of prefix
matching for the selection of the list entries. As a consequence, the user has
less to type. Furthermore, the key bindings do not have to be memorized since
they are listed at program startup.

See also the section "Project Informations".

## Usage

To start keymenu, invoke "keymenu/main.py" directly or create a symbolic link
of that file first.

Currently, there are no special command line parameters. Just redirect or pipe
the streams. For example, if your keymap is saved in a file "my-keymap.json",
you can start keymenu and save your selection by executing the following shell
command in the terminal:

```shell
keymenu < my-keymap.json > my-selection.txt
```

On startup, keymenu prints each list entry together with its key binding on the
terminal. After that, it reads a character from the terminal. If this character
matches with one of the key bindings, keymenu prints the return value of the
corresponding list entry on standard output and exits. If the escape character
is read, keymenu exits without printing anything on standard output. In all
other cases, keymenu reads the next character and begins again.

Keymenu uses /dev/tty for user interaction so that you do not have to worry
about garbage in the streams. If an error occurs, the error messages are, as
usual, printed on standard error.

## Requirements

* Python 3
* POSIX style tty control must be supported, see
  [Pythons termios module](https://docs.python.org/3/library/termios.html)
* A UTF-8 locale might be a requirement, I don't know

## Keymap Format

The keymap must be a
[UTF-8 ( or UTF-16 or UTF-32)](https://docs.python.org/3/library/json.html#character-encodings)
encoded
[JSON](https://tools.ietf.org/html/rfc8259) object with the structure described
below. Note, that words which have a special meaning in JSON context are
emphasized ( e.g. *object* ).

The root structure must be an *object*. Its *members* represent the list
entries. The *name* of each list entry specifies the key the user has to press
to select this entry. This *name* must be unique and have the length 1. All
UTF-8 characters are allowed, except the ASCII escape character ( hexadecimal:
1B ). It is up to the user to set characters which can be sent through the
terminal. The *value* of each entry must be an *object* again, which must/may
contain the following *members*:

* return: This *member* specifies the *string* which is written to stdout when
  its entry is chosen by the user. This member is mandatory.
* display: This *member* determines the *string* which is printed on the
  terminal when all entries are listed. This member is optional. If it is not
  defined, the *value* of the *member* "return" is used instead.

If an entry contains *members* which are not listed above, they are ignored.

## Example

Let's say you have the following JSON structure:

```json
{
  "g": { "display":"good", "return":"today was a good day" },
  "o": { "return":"I'm fine" },
  "b": { "display":"bad", "return":"please kill me with fire" }
}
```

If you start keymenu with this keymap, its entries are listed as follows:

```
[g] good
[o] I'm fine
[b] bad
```

If you press the key "g" now, "today was a good day" is printed on standard
output. If you press "o" instead, "I'm fine" is printed.

## Project Informations

This program is still at an early stage. Odds are that its interface will
change.

This version is probably the last written in Python. An ncurses-based
reimplementation in C should be released soon.

### Current Limitations

The "UI" is extremly simple:

* It is easy to break the UI's layout using characters such as newline.
* Instead of "refreshing" the UI after a non-matching key has been typed, this
  program just reprints the keymap below the old output. Before keymenu quits,
  it does not restore the previous "content" of the terminal. Thus, if you
  press a few non-matching keys and quit keymenu then, you see nothing but
  menus.

### About the maintainer

Edgard Schmidt ( https://edik.ch/ )

Email: schmidt (ATT) edik.ch ( replace " (ATT) " with "@" )

Official Repository URL: https://github.com/3dik/keymenu

## License

> This program is free software: you can redistribute it and/or modify
> it under the terms of the GNU General Public License as published by
> the Free Software Foundation, either version 3 of the License, or
> (at your option) any later version.
> 
> This program is distributed in the hope that it will be useful,
> but WITHOUT ANY WARRANTY; without even the implied warranty of
> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
> GNU General Public License for more details.
> 
> You should have received a copy of the GNU General Public License
> along with this program.  If not, see <http://www.gnu.org/licenses/>.
