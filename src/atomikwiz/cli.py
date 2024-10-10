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


def obtain_frontmatter(frontmatter):
    """Process the frontmatter"""

    # Declare vars to avoid UnboundLocalError
    quiz_title = ""
    quiz_date = ""
    quiz_status = ""
    quiz_path = ""
    img_prefix = ""
    img_suffix = ""

    for line in frontmatter:
        # check if line has more than one : and raise error if so
        line_check = line.split(":")
        if len(line_check) > 2:
            sys.exit("There can only be one colon per line in the frontmatter")

        # Extract the data into defined variables
        if line.startswith("title:"):
            quiz_title = line.split(":")[-1].strip()
        if line.startswith("date:"):
            quiz_date = line.split(":")[-1].strip()
        if line.startswith("status:"):
            quiz_status = line.split(":")[-1].strip()
        if line.startswith("img_prefix:"):
            img_prefix = line.split(":")[-1].strip()
        if line.startswith("img_suffix:"):
            img_suffix = line.split(":")[-1].strip()
        if line.startswith("quiz_path:"):
            quiz_path = line.split(":")[-1].strip()

    # If everything checks out then return the formatted frontmatter
    if not (
        quiz_title
        and quiz_date
        and quiz_status
        and img_prefix
        and img_suffix
        and quiz_path
    ):
        sys.exit("Missing required parameters in the frontmatter")
    return {
        "quiz_title": quiz_title,
        "quiz_date": quiz_date,
        "quiz_status": quiz_status,
        "quiz_path": quiz_path,
        "img_prefix": img_prefix,
        "img_suffix": img_suffix,
    }


def create_quiz(frontmatter, questions):
    """Create the quiz"""

    # Get the frontmatter into a dictionary of key value pairs
    frontmatter_data = obtain_frontmatter(frontmatter)
    print(frontmatter_data)


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
