import json
import os

class ContactManager:
    def __init__(self, filename="contacts.json"):
        self.filename = filename
        self.contacts = []
        self.load_contacts()

    def load_contacts(self):
        if not os.path.exists(self.filename):
            self.contacts = []
            return
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.contacts = json.load(f)
        except (json.JSONDecodeError, IOError):
            self.contacts = []

    def save_contacts(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.contacts, f, indent=4)

    def add_contact(self, contact):
        self.contacts.append(contact)
        self.save_contacts()

    def update_contact(self, index, new_contact):
        self.contacts[index] = new_contact
        self.save_contacts()

    def delete_contact(self, index):
        del self.contacts[index]
        self.save_contacts()

    def search_contacts(self, name_query):
        return [c for c in self.contacts if name_query.lower() in c['name'].lower()]
