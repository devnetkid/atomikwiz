"""
AtomiKwiz
Static website quiz creator.

Usage:
    atomikwiz [options] <filename>

Options:
    -h --help     Show this screen.
    --version     Show version.


"""

from docopt import docopt

from atomikwiz import __app_name__, __version__


def cli():
    arguments = docopt(__doc__, version=__version__)
    print(arguments)
