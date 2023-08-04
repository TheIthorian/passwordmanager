from random import *
import pyperclip

password_characters = {"al_list": list(map(chr, range(97, 123))),
                       "al_list_upper": [letter.upper() for letter in list(map(chr, range(97, 123)))],
                       "num_list": list(range(0, 9)),
                       "spec_list": list('~`!@#$%^&*()_-+={[}]|\:;"<,>.?/')
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
    password = ''.join(password_list)
    return password


def gen_button_click(entry):
    """Function to return inner function for purpose of assigning inner function to button command."""
    def apply_password_to_entry():
        entry.delete(0, 'end')
        password = generate_password()
        pyperclip.copy(password)
        entry.insert(0, password)

    return apply_password_to_entry
