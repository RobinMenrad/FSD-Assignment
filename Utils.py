import re

GRADE_ORDERING_KEYS = ['NA', 'F', 'P', 'C', 'D', 'HD'] # TODO: Are we meant to display students if they haven't enrolled?
GRADE_ORDERING = {key: i for i, key in enumerate(GRADE_ORDERING_KEYS)}

EMAIL_REGEX = r'\w+[.]\w+@university[.]com'
PASSWORD_REGEX = r'[A-Z][A-Za-z]{5,}\d{3,}'

MAX_ENROLLED_SUBJECTS = 4
INDENT = "        "

class StudentAlreadyExistsException(Exception):
    pass


def email_check(email: str) -> bool:
    """Assert email passes email regex

    Args:
        email (str): input email to validate

    Returns:
        bool: True if pass. False if fail.
    """
    if re.match(EMAIL_REGEX, email):
        return True
    return False


def password_check(password: str) -> bool:
    """Assert password passes password regex

    Args:
        password (str): input password to validate

    Returns:
        bool: True if pass. False if fail.
    """
    if re.match(PASSWORD_REGEX, password):
        return True
    return False


def mark_to_grade(mark: int) -> str:
    """From mark return grade.

    Args:
        mark (int): mark

    Returns:
        str: string representation of mark
    """
    if mark == -1:  # TODO: Are we meant to display students if they haven't enrolled?
        return 'N/A'

    if mark <= 50:
        return 'F'

    elif mark >= 50 and mark < 65:
        return 'P'

    elif mark >= 65 and mark < 75:
        return 'C'

    elif mark >= 75 and mark < 85:
        return 'D'

    elif mark >= 85:
        return 'HD'

# Coloured print and input functions
def print_red(value, indents=1): print(f"\033[91m{INDENT * indents}{value}\033[00m")
def print_green(value, indents=1): print(f"\033[92m{INDENT * indents}{value}\033[00m")
def print_yellow(value, indents=1): print(f"\033[93m{INDENT * indents}{value}\033[00m")
def print_white(value, indents=1):print(f"{INDENT * indents }{value}")

def input_red(value, indents=1): return input(f"\033[91m{INDENT * indents}{value}\033[00m")
def input_white(value, indents=1): return input(f"{INDENT * indents}{value}")
def input_cyan(value, indents=1): return input(f"\033[96m{INDENT * indents}{value}\033[00m")
