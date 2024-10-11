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

import jinja2
import os
import sys

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


def process_images(frontmatter, img_counter):
    
    # Extract the needed image data from the frontmatter
    img_prefix = frontmatter["img_prefix"]
    img_suffix = frontmatter["img_suffix"]
    img_path = frontmatter["quiz_path"]

    # Separate the prefix into the name and numbered parts
    prefix_name, prefix_number = img_prefix.split("_")

    # Increment the numbered prefix by img_counter and recombine with name
    incremented_prefix = int(prefix_number) + img_counter
    post_img_prefix = prefix_name + "_" + str(incremented_prefix).zfill(5)
    src_image = post_img_prefix + "." + img_suffix

    return "<img src=\"" + img_path + "website/images/" + src_image + "\" />"


def extract_options(option_content):
    options = []
    id_count = 0
    multi_count = 0
    for line in option_content:
        if line[7] == "=":
            new_line = line.replace("=", "", 1).strip()
            options.append({"opt": new_line, "opt_count": id_count, "type": "radio", "right": "correct"})
            id_count += 1
            multi_count += 1
        else:
            options.append({"opt": line.strip(), "opt_count": id_count, "type": "radio", "right": "incorrect"})
            id_count += 1
    if multi_count > 1:
        for option in options:
            option["type"] = "checkbox"
    return options


def gather_questions(questions_content, frontmatter):
    """
    Evaluate each line forming a dictionary of questions
    """

    question = {}
    questions = []
    tempq = []
    options = []
    option_content = []
    in_options = False
    img_counter = 0
    shuffle = False

    for line in questions_content:
        # Ignore blank lines if we are not in the options
        if not line.strip() and not in_options:
            continue
        # When we are at the end of the options, toggle flag to indicate a new
        # question then add current question to the questions bundle
        elif not line.strip() and in_options:
            question["quiz_title"] = frontmatter["quiz_title"]
            question["legend"] = "Question"
            if shuffle:
                random.shuffle(option_content)
            options = extract_options(option_content)
            question["quizq"] = tempq
            question["quizo"] = options
            questions.append(question)
            question = {}
            tempq = []
            option_content = []
            in_options = False
        # Format images
        elif line.strip() == "::IMG::":
            image = process_images(frontmatter, img_counter)
            tempq.append(image)
            img_counter += 1
        # Gather options
        elif line.startswith("    "):
            option_content.append(line)
            in_options = True
        # If none of the above matched, assume it is part of the question text
        else:
            tempq.append(line)
        
    
    # Done processing questions
    return questions


def render_quiz(frontmatter, quiz):
    # Load template
    file_loader = jinja2.FileSystemLoader("templates")
    env = jinja2.Environment(loader=file_loader)
    start = env.get_template("start.html")
    end = env.get_template("end.html")
    questions = env.get_template("questions.html")

    # Get location and confirm path exists
    quiz_path = frontmatter["quiz_path"] + "website"
    if not os.path.isdir(quiz_path):
        os.mkdir(quiz_path)

    # Create the start page
    start_page = {}
    start_page["quiz_title"] = frontmatter["quiz_title"]
    start_page["quiz_date"] = frontmatter["quiz_date"] 
    start_page["quiz_status"] = frontmatter["quiz_status"]
    start_page["first_question"] = quiz_path + "/questions/q1.html"
    rendered_start = start.render(config=start_page)
    start_filename = quiz_path + "/start.html"
    with open(start_filename, mode="w") as output:
        output.write(rendered_start)

    # Create the end page
    end_page = {}
    end_page["quiz_title"] = frontmatter["quiz_title"]
    rendered_end = end.render(config=end_page)
    end_filename = quiz_path + "/questions/end.html"
    with open(end_filename, mode="w") as output:
        output.write(rendered_end)

    for count, each_quiz in enumerate(quiz, start=1):
        filename = quiz_path + "/questions" + "/q" + str(count) + ".html"
        next_q = quiz_path + "/questions" "/q" + str(count + 1) + ".html"
        prev_q = quiz_path + "/questions" "/q" + str(count - 1) + ".html"
        if count == 1:
            prev_q = quiz_path + "/start.html"
        if count == len(quiz):
            next_q = quiz_path + "/questions/end.html"
        nav = {"next_question": next_q, "previous_question": prev_q}
        rendered_vlans = questions.render(config=each_quiz, nav=nav)
        with open(filename, mode="w") as output:
            output.write(rendered_vlans)


def create_quiz(frontmatter, questions):
    """Create the quiz"""

    # Get the frontmatter into a dictionary of key value pairs
    frontmatter_data = obtain_frontmatter(frontmatter)

    # pluck the questions
    question_data = gather_questions(questions, frontmatter_data)

    # Load and render the quiz
    render_quiz(frontmatter_data, question_data)


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
