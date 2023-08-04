from tkinter import messagebox
import pyperclip

from generator import generate_password
from database import PasswordRecord, upsert_password


def gen_button_click(entry):
    """Function to return inner function for purpose of assigning inner function to button command."""

    def apply_password_to_entry():
        entry.delete(0, "end")
        password = generate_password()
        pyperclip.copy(password)
        entry.insert(0, password)

    return apply_password_to_entry


def save_button_click(entry_dict: dict):
    """Function to return inner function for purpose of assigning inner function to button command."""

    def json_save():
        """Constructs an output_dict from strings entered in Tkinter Entry objects via .get(). Prompts the
        user with a messagebox to confirm the information they are saving. Then, if yes, updates an existing
        saved_passwords.json else creates and writes to a new saved_passwords.json. Then, empties the entries.
        """

        website = entry_dict[0].get()

        output_dict = {
            website: {
                "Email": entry_dict[1].get(),
                "Password": entry_dict[2].get(),
            }
        }

        submit = messagebox.askokcancel(
            title="Confirmation",
            message=f"You entered:\n\nWebsite: {website}"
            f"\nEmail: {output_dict[website]['Email']}"
            f"\nPassword: {output_dict[website]['Password']}",
        )

        if not submit:
            return

        upsert_password(PasswordRecord.from_json(website, output_dict[website]))

        for entry in [entry_dict[0], entry_dict[2]]:
            entry.delete(0, "end")

    return json_save


def make_handle_click_load(password_record: PasswordRecord, entries: dict):
    def handle():
        entries[0].delete(0, "end")
        entries[0].insert(0, password_record.website)

        entries[1].delete(0, "end")
        entries[1].insert(0, password_record.email)

        entries[2].delete(0, "end")
        entries[2].insert(0, password_record.password)

    return handle
