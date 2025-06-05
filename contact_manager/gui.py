import tkinter as tk
from tkinter import ttk, messagebox
from contacts import ContactManager

class ContactApp:
    def __init__(self, root):
        self.manager = ContactManager()
        self.root = root
        self.root.title("Contact Manager")

        # Entry fields
        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.search_var = tk.StringVar()

        self.setup_widgets()
        self.load_table()

    def setup_widgets(self):
        # Entry Form
        form_frame = tk.Frame(self.root)
        form_frame.pack(padx=10, pady=5)

        tk.Label(form_frame, text="Name").grid(row=0, column=0)
        tk.Entry(form_frame, textvariable=self.name_var).grid(row=0, column=1)

        tk.Label(form_frame, text="Phone").grid(row=0, column=2)
        tk.Entry(form_frame, textvariable=self.phone_var).grid(row=0, column=3)

        tk.Label(form_frame, text="Email").grid(row=0, column=4)
        tk.Entry(form_frame, textvariable=self.email_var).grid(row=0, column=5)

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Add", command=self.add_contact).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Edit", command=self.edit_contact).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete", command=self.delete_contact).grid(row=0, column=2, padx=5)

        # Search
        tk.Entry(btn_frame, textvariable=self.search_var).grid(row=0, column=3)
        tk.Button(btn_frame, text="Search", command=self.search_contacts).grid(row=0, column=4, padx=5)
        tk.Button(btn_frame, text="Clear", command=self.load_table).grid(row=0, column=5)

        # Table
        self.tree = ttk.Treeview(self.root, columns=("Name", "Phone", "Email"), show="headings")
        for col in ("Name", "Phone", "Email"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(padx=10, pady=5)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def load_table(self, contacts=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        data = contacts if contacts is not None else self.manager.contacts
        for idx, contact in enumerate(data):
            self.tree.insert("", "end", iid=idx, values=(contact['name'], contact['phone'], contact['email']))

    def get_selected_index(self):
        selected = self.tree.selection()
        return int(selected[0]) if selected else None

    def on_select(self, event):
        idx = self.get_selected_index()
        if idx is not None:
            contact = self.manager.contacts[idx]
            self.name_var.set(contact['name'])
            self.phone_var.set(contact['phone'])
            self.email_var.set(contact['email'])

    def add_contact(self):
        name, phone, email = self.name_var.get(), self.phone_var.get(), self.email_var.get()
        if not name or not phone:
            messagebox.showerror("Error", "Name and Phone are required.")
            return
        self.manager.add_contact({"name": name, "phone": phone, "email": email})
        self.clear_entries()
        self.load_table()

    def edit_contact(self):
        idx = self.get_selected_index()
        if idx is None:
            messagebox.showerror("Error", "Select a contact to edit.")
            return
        name, phone, email = self.name_var.get(), self.phone_var.get(), self.email_var.get()
        self.manager.update_contact(idx, {"name": name, "phone": phone, "email": email})
        self.clear_entries()
        self.load_table()

    def delete_contact(self):
        idx = self.get_selected_index()
        if idx is None:
            messagebox.showerror("Error", "Select a contact to delete.")
            return
        self.manager.delete_contact(idx)
        self.clear_entries()
        self.load_table()

    def search_contacts(self):
        keyword = self.search_var.get()
        results = self.manager.search_contacts(keyword)
        self.load_table(results)

    def clear_entries(self):
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.search_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()
