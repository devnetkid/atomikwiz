"""Common file operations"""

import json
import logging
import os
import platform
import sys
from datetime import datetime

import tomlkit


def load_file(filename, rtype="readlines"):
    """Opens a file to be read

    Args:
        filename (str): The name of the file to be opened
        rtype (str): The return type for the data being returned

    Returns:
        Depends on the rtype
            if read: returns a string of entire contents
            if readlines: returns a list with each line as an element
            if json: returns a json structure
            if toml: returns a toml structure
    """

    try:
        with open(filename, "r", encoding="UTF-8") as file:
            if rtype == "read":
                return file.read()
            elif rtype == "readlines":
                return file.readlines()
            elif rtype == "json":
                return json.load(file)
            elif rtype == "toml":
                return tomlkit.load(file)
            else:
                sys.exit(
                    f"Invalid return type requested. Change {rtype} to valid value"
                )
    except FileNotFoundError:
        sys.exit(f"Could not find file {filename}")


def clear_screen():
    if platform.system().lower() == "windows":
        cmd = "cls"
    else:
        cmd = "clear"
    os.system(cmd)


def colorme(msg, color):
    if color == "red":
        wrapper = "\033[91m"
    elif color == "blue":
        wrapper = "\033[94m"
    elif color == "green":
        wrapper = "\033[92m"
    else:
        # Defaults to white if invalid color is given
        wrapper = "\033[47m"
    return wrapper + msg + "\033[0m"


