from tkinter import messagebox
import json
import os


def save_button_click(entry_dict: dict):
    """Function to return inner function for purpose of assigning inner function to button command."""

    def json_save():
        """Constructs an output_dict from strings entered in Tkinter Entry objects via .get(). Prompts the
        user with a messagebox to confirm the information they are saving. Then, if yes, updates an existing
        saved_passwords.json else creates and writes to a new saved_passwords.json. Then, empties the entries.
        """
        output_dict = {
            entry_dict[0].get(): {
                "Email": entry_dict[1].get(),
                "Password": entry_dict[2].get(),
            }
        }
        submit = messagebox.askokcancel(
            title="Confirmation",
            message=f"You entered:\n\nWebsite: {entry_dict[0].get()}"
            f"\nEmail: {output_dict[entry_dict[0].get()]['Email']}"
            f"\nPassword: {output_dict[entry_dict[0].get()]['Password']}",
        )
        if submit:
            if os.path.isfile("saved_passwords.json"):
                with open("saved_passwords.json", "r") as json_file:
                    new_file = json.load(json_file)
                    new_file.update(output_dict)
                with open("saved_passwords.json", "w") as json_file:
                    json.dump(new_file, json_file, indent=4)
            else:
                with open("saved_passwords.json", "w") as json_file:
                    json.dump(output_dict, json_file, indent=4)
            for entry in [entry_dict[0], entry_dict[2]]:
                entry.delete(0, "end")

    return json_save


def load_button_click(info_to_enter: list, entry_dict: dict):
    """Function to return inner function for purpose of assigning inner function to button command."""

    def load_into_entries():
        """Loads entry from entry_dict into entry field based on its index. To use for load buttons, construct
        a dictionary containing button: list pairs where the button is a Tkinter Button object and the list
        contains the information to enter in sequence."""
        for index, entry in entry_dict.items():
            entry.delete(0, "end")
            entry.insert(0, info_to_enter[index])

    return load_into_entries
