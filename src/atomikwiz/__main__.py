#!/usr/bin/env python3
"""
Date: 10-05-2024
Purpose: A simple app to create a static quiz website
Description: You make a plain text file of questions and answers following
             a specific format. Then you run this script pointing it to your
             desired file and it will create a website package for you. Open
             the website package folder and click on the start.html file.

             See README.md for more details.

"""

from atomikwiz import cli


def main():
    cli.cli()


if __name__ == "__main__":
    main()
