"""
AtomiKwiz
Static website quiz creator.

Usage:
    atomikwiz [options] <filename>

Arguments:
    <filename>    The file to be used as the quiz input

Options:
    -h --help     Show this screen.
    --version     Show version.

"""

from docopt import docopt

from atomikwiz import __app_name__, __version__

from .common import clear_screen, colorme, load_file


def create_quiz(frontmatter, questions):
    print(frontmatter)
    print(questions)


def cli():
    # Get the user input and create the quiz
    arguments = docopt(__doc__, version=__version__)

    frontmatter = []
    questions = []
    is_frontmatter = True
    is_question = False

    # Load the quiz specified by user
    quiz_data = load_file(arguments["<filename>"])

    # Separate the frontmatter from the questions
    for line in quiz_data[1:]:
        if line.startswith("---"):
            is_frontmatter = False
            is_question = True
            continue
        if is_frontmatter:
            frontmatter.append(line)
        if is_question:
            questions.append(line)

    # Create the quiz with given parameters
    create_quiz(frontmatter, questions)
