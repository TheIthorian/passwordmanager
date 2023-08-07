from tkinter import Entry, Label, Button, Frame, Tk, SW, W, Toplevel
from tkinter.ttk import Combobox

from constants import FONTS, LABEL_LIST, STYLES, DEFAULT_EMAIL_LIST
from event_handlers import (
    gen_button_click,
    save_button_click,
    make_handle_click_load,
    Entries,
)
import database


class Gui:
    def __init__(self):
        self.load_window = None
        self.main = None
        self.bottom = None
        self.root = None
        self.entries: Entries = None

    def run_main_loop(self):
        """Runs the GUI."""
        self._create_root()
        self._create_frames()
        self._create_labels()
        self._create_entries()
        self._add_buttons()
        self.root.mainloop()

    def _create_root(self):
        """Creates Tkinter root."""
        self.root = Tk()
        self.root.title("Password Manager")
        self.root.config(padx=30, pady=20)

    def _create_frames(self):
        """Creates Tkinter frames for laying out GUI features. Places bottom frame at bottom row for meta buttons."""
        self.main = Frame(self.root)
        self.main.grid()
        self.bottom = Frame(self.root)
        self.bottom.grid(row=4, sticky=SW)

    def _create_labels(self):
        """Creates all Tkinter Label objects."""
        title = Label(
            self.main, text="PASSWORD MANAGER", pady=STYLES.PAD_Y, font=FONTS.TITLE
        )
        title.grid(columnspan=3)

        for index, label in enumerate(LABEL_LIST):
            Label(
                self.main,
                text=f"{label}: ",
                font=FONTS.LABEL,
                width=STYLES.LABEL_WIDTH,
                pady=STYLES.PAD_Y,
                anchor=STYLES.LABEL_ANCHOR,
            ).grid(row=index + 1)

    def _create_entries(self):
        """Creates all Tkinter Entry and Combobox objects. Adjusts column span for bottom entry to make room for
        generator button."""
        website = Entry(self.main, bd=STYLES.BORDER, width=STYLES.ENTRY_WIDTH)
        website.grid(row=1, column=1, columnspan=2, sticky=W)

        email = Combobox(self.main, width=STYLES.COMBOBOX_WIDTH)
        email["values"] = DEFAULT_EMAIL_LIST
        email.insert(0, DEFAULT_EMAIL_LIST[0])
        email.grid(row=2, column=1, columnspan=2, sticky=W)

        password = Entry(self.main, bd=STYLES.BORDER)
        password.grid(row=3, column=1, sticky=W)

        self.entries = Entries(website, email, password)

    def _add_buttons(self):
        """Creates all Tkinter Button objects. Meta buttons populate the bottom frame.
        Assigns generator command to gen_button Button."""
        gen_button = Button(
            self.main,
            text="Generate",
            width=STYLES.BUTTON_WIDTH,
            font=FONTS.BUTTON,
            padx=STYLES.PAD_X,
            command=gen_button_click(self.entries.password),
        )
        gen_button.grid(row=3, column=2)

        def make_button(text: str, command: callable, column: int) -> Button:
            button = Button(
                self.bottom,
                text=text,
                font=FONTS.BUTTON,
                width=STYLES.BUTTON_WIDTH,
                command=command,
            )
            button.grid(row=4, column=column)
            return button

        make_button("Save", save_button_click(self.entries), 1)
        make_button("Load", self.create_load_window, 2)
        make_button("Quit", self.root.destroy, 3)

    def _create_load_window(self):
        """Creates the Tkinter Toplevel pop-up window and populates it with named buttons to allow the user to
        load in data from database.
        """
        self.load_window = Toplevel(self.main)
        self.load_window.title("Saved Accounts")
        self.load_window.config(padx=100, pady=30)

        existing_passwords = database.get_all_passwords()
        for password_record in existing_passwords.values():
            button = Button(
                self.load_window,
                text=password_record.website,
                width=STYLES.BUTTON_WIDTH,
                pady=STYLES.PAD_Y,
            )

            button.config(command=make_handle_click_load(password_record, self.entries))
            button.pack()