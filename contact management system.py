import tkinter as tk
from tkinter import ttk, messagebox
import json
import re

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Management System")
        self.root.geometry("800x600")
        
        # Load contacts from file
        self.contacts = self.load_contacts()
        
        # Create main container
        self.main_container = ttk.Frame(root, padding="20")
        self.main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure styles
        style = ttk.Style()
        style.configure('Header.TLabel', font=('Arial', 18, 'bold'))
        style.configure('Subheader.TLabel', font=('Arial', 12, 'bold'))
        
        # Create header
        ttk.Label(self.main_container, text="Contact Management System", 
                 style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Create left panel (Contact List)
        left_panel = ttk.LabelFrame(self.main_container, text="Contacts", padding="10")
        left_panel.grid(row=1, column=0, padx=(0, 10), sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Search frame
        search_frame = ttk.Frame(left_panel)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.search_contacts)
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(search_frame, text="🔍").pack(side=tk.LEFT, padx=5)
        
        # Contact listbox with scrollbar
        list_frame = ttk.Frame(left_panel)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.contact_listbox = tk.Listbox(list_frame, width=30, font=('Arial', 10))
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.contact_listbox.yview)
        self.contact_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.contact_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create right panel (Contact Details)
        right_panel = ttk.LabelFrame(self.main_container, text="Contact Details", padding="10")
        right_panel.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Contact details form
        details_frame = ttk.Frame(right_panel)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form fields
        ttk.Label(details_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(details_frame, textvariable=self.name_var, width=30).grid(row=0, column=1, pady=5)
        
        ttk.Label(details_frame, text="Phone:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.phone_var = tk.StringVar()
        ttk.Entry(details_frame, textvariable=self.phone_var, width=30).grid(row=1, column=1, pady=5)
        
        ttk.Label(details_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(details_frame, textvariable=self.email_var, width=30).grid(row=2, column=1, pady=5)
        
        ttk.Label(details_frame, text="Address:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.address_var = tk.StringVar()
        ttk.Entry(details_frame, textvariable=self.address_var, width=30).grid(row=3, column=1, pady=5)
        
        # Buttons frame
        button_frame = ttk.Frame(right_panel)
        button_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(button_frame, text="Add New", command=self.add_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update", command=self.update_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete", command=self.delete_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_fields).pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_var = tk.StringVar()
        ttk.Label(right_panel, textvariable=self.status_var, wraplength=300).pack(fill=tk.X)
        
        # Bind selection event
        self.contact_listbox.bind('<<ListboxSelect>>', self.on_select)
        
        # Initial list update
        self.update_contact_list()
        
    def load_contacts(self):
        try:
            with open('contacts.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
            
    def save_contacts(self):
        with open('contacts.json', 'w') as file:
            json.dump(self.contacts, file, indent=2)
            
    def validate_fields(self):
        # Validate name
        name = self.name_var.get().strip()
        if not name:
            self.status_var.set("Name is required!")
            return False
            
        # Validate phone
        phone = self.phone_var.get().strip()
        if not phone or not re.match(r'^\+?1?\d{9,15}$', phone):
            self.status_var.set("Invalid phone number!")
            return False
            
        # Validate email
        email = self.email_var.get().strip()
        if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            self.status_var.set("Invalid email format!")
            return False
            
        return True
            
    def add_contact(self):
        if not self.validate_fields():
            return
            
        name = self.name_var.get().strip()
        if name in self.contacts:
            self.status_var.set("Contact already exists!")
            return
            
        self.contacts[name] = {
            'phone': self.phone_var.get().strip(),
            'email': self.email_var.get().strip(),
            'address': self.address_var.get().strip()
        }
        
        self.save_contacts()
        self.update_contact_list()
        self.clear_fields()
        self.status_var.set(f"Contact '{name}' added successfully!")
        
    def update_contact(self):
        if not self.validate_fields():
            return
            
        selection = self.contact_listbox.curselection()
        if not selection:
            self.status_var.set("Please select a contact to update!")
            return
            
        old_name = self.contact_listbox.get(selection[0]).split(" (")[0]
        new_name = self.name_var.get().strip()
        
        if old_name != new_name and new_name in self.contacts:
            self.status_var.set("Contact name already exists!")
            return
            
        # Remove old contact if name changed
        if old_name != new_name:
            del self.contacts[old_name]
            
        # Update contact
        self.contacts[new_name] = {
            'phone': self.phone_var.get().strip(),
            'email': self.email_var.get().strip(),
            'address': self.address_var.get().strip()
        }
        
        self.save_contacts()
        self.update_contact_list()
        self.status_var.set(f"Contact '{new_name}' updated successfully!")
        
    def delete_contact(self):
        selection = self.contact_listbox.curselection()
        if not selection:
            self.status_var.set("Please select a contact to delete!")
            return
            
        name = self.contact_listbox.get(selection[0]).split(" (")[0]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{name}'?"):
            del self.contacts[name]
            self.save_contacts()
            self.update_contact_list()
            self.clear_fields()
            self.status_var.set(f"Contact '{name}' deleted successfully!")
            
    def clear_fields(self):
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.address_var.set("")
        self.status_var.set("")
        self.contact_listbox.selection_clear(0, tk.END)
        
    def on_select(self, event):
        selection = self.contact_listbox.curselection()
        if selection:
            name = self.contact_listbox.get(selection[0]).split(" (")[0]
            contact = self.contacts[name]
            
            self.name_var.set(name)
            self.phone_var.set(contact['phone'])
            self.email_var.set(contact['email'])
            self.address_var.set(contact['address'])
            
    def search_contacts(self, *args):
        search_term = self.search_var.get().lower()
        self.update_contact_list(search_term)
        
    def update_contact_list(self, search_term=""):
        self.contact_listbox.delete(0, tk.END)
        
        for name, details in sorted(self.contacts.items()):
            if (search_term in name.lower() or 
                search_term in details['phone'].lower()):
                self.contact_listbox.insert(tk.END, f"{name} ({details['phone']})")

def main():
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
