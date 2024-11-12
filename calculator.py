import tkinter as tk
from tkinter import ttk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Calculator")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        
        # Variable to store current calculation
        self.current = ""
        
        # Create display
        self.display = ttk.Entry(root, justify="right", font=("Arial", 20))
        self.display.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        
        # Button layout
        self.create_buttons()
        
        # Configure grid
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)

    def create_buttons(self):
        # Button styling
        style = ttk.Style()
        style.configure('Calculator.TButton', font=('Arial', 14))
        
        # Button texts
        button_texts = [
            'C', '←', '%', '/',
            '7', '8', '9', '*',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '0', '.', '±', '='
        ]
        
        # Create and place buttons
        row = 1
        col = 0
        for text in button_texts:
            btn = ttk.Button(
                self.root,
                text=text,
                style='Calculator.TButton',
                command=lambda t=text: self.button_click(t)
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            col += 1
            if col > 3:
                col = 0
                row += 1
    
    def button_click(self, value):
        if value == 'C':
            # Clear display
            self.current = ""
            self.display.delete(0, tk.END)
            
        elif value == '←':
            # Backspace
            self.current = self.current[:-1]
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.current)
            
        elif value == '±':
            # Change sign
            try:
                if self.current and self.current[0] == '-':
                    self.current = self.current[1:]
                else:
                    self.current = '-' + self.current
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, self.current)
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
                
        elif value == '=':
            # Calculate result
            try:
                result = str(eval(self.current))
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, result)
                self.current = result
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
                self.current = ""
                
        else:
            # Add number or operator to current calculation
            self.current += value
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.current)

def main():
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
