from dataclasses import dataclass
import json
import os

PASSWORD_FILE = "saved_passwords.json"


@dataclass
class PasswordRecord:
    website: str
    email: str
    password: str

    def to_json(self) -> str:
        return {[self.website]: {"Email": self.email, "Password": self.password}}

    def from_json(self, key: str, value: dict) -> "PasswordRecord":
        self.website = key
        self.email = value["Email"]
        self.password = value["Password"]


def init():
    if not os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "w") as json_file:
            json.dump({}, json_file, indent=4)


def get_all_passwords() -> dict[str, PasswordRecord]:
    passwords = _load_passwords_to_dict()
    return {
        key: PasswordRecord.from_json(key, value) for key, value in passwords.items()
    }


def get_password_by_website(website_name: str):
    passwords = get_all_passwords()
    return passwords[website_name]


def add_password(passwordRecord: PasswordRecord):
    return _upsert_password(passwordRecord)


def update_password(passwordRecord: PasswordRecord):
    return _upsert_password(passwordRecord)


def _upsert_password(passwordRecord: PasswordRecord):
    passwords = _load_passwords_to_dict()
    with open(PASSWORD_FILE) as json_file:
        existing_passwords = json.load(json_file)
        existing_passwords[passwordRecord.website] = passwordRecord.to_json()
        json.dump(passwords, json_file, indent=4)


def _load_passwords_to_dict() -> dict[str, dict]:
    with open(PASSWORD_FILE) as json_file:
        passwords_dict = json.load(json_file)
    return passwords_dict
