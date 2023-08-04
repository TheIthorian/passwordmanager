from random import *
import pyperclip

password_characters = {
    "al_list": list(map(chr, range(97, 123))),
    "al_list_upper": [letter.upper() for letter in list(map(chr, range(97, 123)))],
    "num_list": list(range(0, 9)),
    "spec_list": list('~`!@#$%^&*()_-+={[}]|\:;"<,>.?/'),
}


def generate_password():
    letters: list = []
    num_spec: list = []
    for key, value in password_characters.items():
        if "al_list" in key:
            letters.append([choice(value) for _ in range(randint(4, 6))])
        else:
            num_spec.append([choice(value) for _ in range(randint(2, 4))])
    password_list = [str(char) for sublist in (letters + num_spec) for char in sublist]
    shuffle(password_list)
    password = "".join(password_list)
    return password


ALPHABET = list(map(chr, range(97, 123)))
ALPHABET_UPPER = [letter.upper() for letter in ALPHABET]
NUMBERS = [str(n) for n in list(range(0, 9))]
SPECIAL = list('~`!@#$%^&*()_-+={[}]|\:;"<,>.?/')


def generate_password_new():
    password = ""
    password += "".join(select_random_elements(ALPHABET, 4, 6))
    password += "".join(select_random_elements(ALPHABET_UPPER, 2, 4))
    password += "".join(select_random_elements(NUMBERS, 2, 4))
    password += "".join(select_random_elements(SPECIAL, 2, 4))

    password_list = list(password)
    shuffle(password_list)
    return "".join(password_list)


def select_random_elements(
    list_of_elements: list,
    min_elements: int,
    max_elements: int = None,
):
    return [
        choice(list_of_elements)
        for _ in range(randint(min_elements, max_elements or min_elements))
    ]
