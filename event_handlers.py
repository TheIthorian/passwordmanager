from tkinter import messagebox, Entry
import pyperclip
from dataclasses import dataclass

from generator import generate_password
from database import PasswordRecord, upsert_password


@dataclass
class Entries:
    """Dataclass to hold Tkinter Entry objects."""

    website: Entry
    email: Entry
    password: Entry


def gen_button_click(entry):
    """Function to return inner function for purpose of assigning inner function to button command."""

    def apply_password_to_entry():
        entry.delete(0, "end")
        password = generate_password()
        pyperclip.copy(password)
        entry.insert(0, password)

    return apply_password_to_entry


def save_button_click(entries: Entries):
    """Function to return inner function for purpose of assigning inner function to button command."""

    def json_save():
        """Constructs an output_dict from strings entered in Tkinter Entry objects via .get(). Prompts the
        user with a messagebox to confirm the information they are saving. Then, if yes, updates an existing
        saved_passwords.json else creates and writes to a new saved_passwords.json. Then, empties the entries.
        """
        website = entries.website.get()
        email = entries.email.get()
        password = entries.password.get()

        submit = messagebox.askokcancel(
            title="Confirmation",
            message=f"You entered:\n\nWebsite: {website}"
            f"\nEmail: {email}"
            f"\nPassword: {password}",
        )

        if not submit:
            return

        print(f"Saving {website} {email} {password}")
        upsert_password(PasswordRecord(website, email, password))

        entries.website.delete(0, "end")
        entries.password.delete(0, "end")

    return json_save


def make_handle_click_load(password_record: PasswordRecord, entries: Entries):
    def handle():
        entries.website.delete(0, "end")
        entries.website.insert(0, password_record.website)

        entries.email.delete(0, "end")
        entries.email.insert(0, password_record.email)

        entries.password.delete(0, "end")
        entries.password.insert(0, password_record.password)

    return handle
