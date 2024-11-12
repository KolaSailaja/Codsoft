import tkinter as tk
from tkinter import ttk
import random
import string
import pyperclip  # For clipboard functionality

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # Style configuration
        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 11))
        style.configure('TButton', font=('Arial', 10))
        style.configure('Header.TLabel', font=('Arial', 14, 'bold'))
        
        # Main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        ttk.Label(self.main_frame, text="Secure Password Generator", 
                 style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=10)
        
        # Password length
        ttk.Label(self.main_frame, text="Password Length:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.length_var = tk.StringVar(value="12")
        self.length_entry = ttk.Entry(self.main_frame, textvariable=self.length_var, width=10)
        self.length_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Character type checkboxes
        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(self.main_frame, text="Uppercase Letters (A-Z)", 
                       variable=self.uppercase_var).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
        ttk.Checkbutton(self.main_frame, text="Lowercase Letters (a-z)", 
                       variable=self.lowercase_var).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        ttk.Checkbutton(self.main_frame, text="Numbers (0-9)", 
                       variable=self.numbers_var).grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5)
        ttk.Checkbutton(self.main_frame, text="Special Characters (!@#$%^&*)", 
                       variable=self.symbols_var).grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Generated password display
        ttk.Label(self.main_frame, text="Generated Password:").grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(20,5))
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self.main_frame, textvariable=self.password_var, width=40)
        self.password_entry.grid(row=7, column=0, columnspan=2, pady=5)
        
        # Buttons frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=20)
        
        # Generate and Copy buttons
        ttk.Button(button_frame, text="Generate Password", 
                  command=self.generate_password).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Copy to Clipboard", 
                  command=self.copy_to_clipboard).grid(row=0, column=1, padx=5)
        
        # Password strength indicator
        self.strength_var = tk.StringVar()
        ttk.Label(self.main_frame, text="Password Strength:").grid(row=9, column=0, sticky=tk.W, pady=5)
        self.strength_label = ttk.Label(self.main_frame, textvariable=self.strength_var)
        self.strength_label.grid(row=9, column=1, sticky=tk.W, pady=5)
        
    def generate_password(self):
        try:
            length = int(self.length_var.get())
            if length <= 0:
                self.password_var.set("Invalid length")
                return
            
            # Create character pool based on selections
            chars = ''
            if self.uppercase_var.get():
                chars += string.ascii_uppercase
            if self.lowercase_var.get():
                chars += string.ascii_lowercase
            if self.numbers_var.get():
                chars += string.digits
            if self.symbols_var.get():
                chars += string.punctuation
                
            if not chars:
                self.password_var.set("Please select at least one character type")
                return
                
            # Generate password
            password = ''.join(random.choice(chars) for _ in range(length))
            
            # Ensure at least one character from each selected type
            if self.uppercase_var.get() and not any(c.isupper() for c in password):
                password = self.replace_random_char(password, string.ascii_uppercase)
            if self.lowercase_var.get() and not any(c.islower() for c in password):
                password = self.replace_random_char(password, string.ascii_lowercase)
            if self.numbers_var.get() and not any(c.isdigit() for c in password):
                password = self.replace_random_char(password, string.digits)
            if self.symbols_var.get() and not any(c in string.punctuation for c in password):
                password = self.replace_random_char(password, string.punctuation)
                
            self.password_var.set(password)
            self.evaluate_password_strength(password)
            
        except ValueError:
            self.password_var.set("Please enter a valid number")
            
    def replace_random_char(self, password, char_set):
        if len(password) > 0:
            replace_index = random.randint(0, len(password) - 1)
            password_list = list(password)
            password_list[replace_index] = random.choice(char_set)
            return ''.join(password_list)
        return password
            
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password and password not in ["Invalid length", "Please select at least one character type", "Please enter a valid number"]:
            pyperclip.copy(password)
            
    def evaluate_password_strength(self, password):
        score = 0
        feedback = ""
        
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
            
        if any(c.isupper() for c in password):
            score += 1
        if any(c.islower() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in string.punctuation for c in password):
            score += 1
            
        if score >= 5:
            feedback = "Strong"
            self.strength_label.configure(foreground="green")
        elif score >= 3:
            feedback = "Moderate"
            self.strength_label.configure(foreground="orange")
        else:
            feedback = "Weak"
            self.strength_label.configure(foreground="red")
            
        self.strength_var.set(feedback)

def main():
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
