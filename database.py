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
        return {"Website": self.website, "Email": self.email, "Password": self.password}

    @staticmethod
    def from_json(key: str, value: dict) -> "PasswordRecord":
        return PasswordRecord(key, value["Email"], value["Password"])


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


def upsert_password(password_record: PasswordRecord):
    existing_passwords = _load_passwords_to_dict()
    existing_passwords[password_record.website] = password_record.to_json()

    with open(PASSWORD_FILE, "w") as json_file:
        print("Writing to file: ", existing_passwords)
        json.dump(existing_passwords, json_file, indent=4)


def _load_passwords_to_dict() -> dict[str, dict]:
    with open(PASSWORD_FILE, "r") as json_file:
        try:
            passwords_dict = json.load(json_file)
        except json.decoder.JSONDecodeError:
            passwords_dict = {}
    return passwords_dict
