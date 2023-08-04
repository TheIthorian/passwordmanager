from tkinter.ttk import Combobox
from constants import FONTS, LABEL_LIST, STYLES, META_BUTTONS, DEFAULT_EMAIL_LIST
from event_handlers import gen_button_click, save_button_click, load_button_click
from tkinter import Entry, Label, Button, Frame, Tk, SW, W, Toplevel
import json


class Gui:
    def __init__(self):
        self.load_window = None
        self.main = None
        self.title = None
        self.bottom = None
        self.root = None
        self.entries = None
        self.gen_button = None
        self.meta_buttons: list = []
        self.load_button_dict: dict = {}
        self.saved_accounts: dict = {}

    def create_root(self):
        """Creates Tkinter root."""
        self.root = Tk()
        self.root.title("Password Manager")
        self.root.config(padx=30, pady=20)

    def create_frames(self):
        """Creates Tkinter frames for laying out GUI features. Places bottom frame at bottom row for meta buttons."""
        self.main = Frame(self.root)
        self.main.grid()
        self.bottom = Frame(self.root)
        self.bottom.grid(row=4, sticky=SW)

    def create_labels(self):
        """Creates all Tkinter Label objects."""
        self.title = Label(
            self.main, text="PASSWORD MANAGER", pady=STYLES.PAD_Y, font=FONTS.TITLE
        )
        self.title.grid(columnspan=3)
        for index, label in enumerate(LABEL_LIST):
            Label(
                self.main,
                text=f"{label}: ",
                font=FONTS.LABEL,
                width=STYLES.LABEL_WIDTH,
                pady=STYLES.PAD_Y,
                anchor=STYLES.LABEL_ANCHOR,
            ).grid(row=index + 1)

    def create_entries(self):
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

        self.entries = {0: website, 1: email, 2: password}

    def add_buttons(self):
        """Creates all Tkinter Button objects. Meta buttons populate the bottom frame.
        Assigns generator command to gen_button Button."""
        self.gen_button = Button(
            self.main,
            text="Generate",
            width=STYLES.BUTTON_WIDTH,
            font=FONTS.BUTTON,
            padx=STYLES.PAD_X,
            command=gen_button_click(self.entries[2]),
        )
        self.gen_button.grid(row=3, column=2)
        for column, button in META_BUTTONS.items():
            self.meta_buttons.append(
                Button(self.bottom, text=button, font=FONTS.BUTTON)
            )
            self.meta_buttons[column].grid(row=4, column=column)

    def create_load_window(self):
        """Creates the Tkinter Toplevel pop-up window and populates it with named buttons to allow the user to
        load in data from saved_passwords.json. Each button is a Tkinter Button object and is the key in a
        load_button_dict dict. Each button has a value pair consisting of the website, email and password information
        from saved_passwords.json as a list. Then, calls load_button_click in a for loop on that dictionary to
        target each button and load in the corresponding information from the key : value pairs.
        """
        self.load_window = Toplevel(self.main)
        self.load_window.title("Saved Accounts")
        self.load_window.config(padx=100, pady=30)
        with open("saved_passwords.json") as json_file:
            self.saved_accounts = json.load(json_file)
            for account, details in self.saved_accounts.items():
                input_list = [account, details["Email"], details["Password"]]
                self.load_button_dict.update(
                    {
                        Button(
                            self.load_window,
                            text=account,
                            width=STYLES.BUTTON_WIDTH,
                            pady=STYLES.PAD_Y,
                        ): input_list
                    }
                )
            for button, details in self.load_button_dict.items():
                button.config(command=load_button_click(details, self.entries))
                button.pack()

    def add_meta_functions(self):
        """Creates save, load and quit functions for the meta buttons."""
        self.meta_buttons[0].config(command=save_button_click(self.entries))
        self.meta_buttons[1].config(command=self.create_load_window)
        self.meta_buttons[2].config(command=self.root.destroy)

    def run_main_loop(self):
        """Runs the GUI."""
        self.create_root()
        self.create_frames()
        self.create_labels()
        self.create_entries()
        self.add_buttons()
        self.add_meta_functions()
        self.root.mainloop()
