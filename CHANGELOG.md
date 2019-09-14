# Changelog

## 0.2 - 2019/09/14 - Last Python Version

**The project has moved**
from [GitHub](https://github.com/3dik/keymenu)
to [Sourcehut](https://git.sr.ht/~edik/keymenu).
The GitHub repository will not receive updates any longer.

This version is probably the last written in Python. An ncurses-based
reimplementation in C should be released soon.

**Security Notice:**

* Both, this and the first release, are vulnerable to ANSI escape sequence
  attacks.
* Both releases are also vulnerable to script spoofing.

**Backwards Incompatibilities:**

* A trailing newline is not added to the output anymore.

Documentation Corrections:

* The first release's readme file stated that the JSON input should be encoded
  in UTF-8, UTF-16 or UTF-32. Actually, the required encoding depends on the
  platform and/or the current locale, see
  [sys.stdin](https://docs.python.org/3/library/sys.html#sys.stdin)
  and
  [locale.getpreferredencoding](https://docs.python.org/3/library/locale.html#locale.getpreferredencoding).
  For the same reason, the readme's "Requirements" section was wrong about the
  required locale since locales with codesets other than UTF-8 are supported as
  well.

Development Stuff:

* documentation of the test system

## 0.1 - 2018/04/14 - Initial Release

This is the initial release. The following stuff is introduced:

* user interface
* usage of standard streams for the communication with the outside world
* usage of /dev/tty for the communication with the user
* JSON keymap parsing

Developement Stuff:

* a few (unit?) tests which test most of the code
* initial readme file
* initial changelog file
* GPLv3 licensed
