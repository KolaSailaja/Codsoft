import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class ToDoList:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("600x700")
        
        # Task storage
        self.tasks = []
        
        # Load saved tasks
        self.load_tasks()
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(self.main_frame, text="To-Do List", 
                              font=('Arial', 24, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Task entry
        self.task_var = tk.StringVar()
        self.task_entry = ttk.Entry(self.main_frame, textvariable=self.task_var, 
                                  width=40, font=('Arial', 12))
        self.task_entry.grid(row=1, column=0, padx=5, pady=5)
        
        # Add task button
        add_button = ttk.Button(self.main_frame, text="Add Task", 
                              command=self.add_task)
        add_button.grid(row=1, column=1, padx=5, pady=5)
        
        # Task list frame
        task_frame = ttk.Frame(self.main_frame)
        task_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(task_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Task listbox
        self.task_listbox = tk.Listbox(task_frame, width=50, height=15,
                                     font=('Arial', 12),
                                     selectmode=tk.SINGLE,
                                     yscrollcommand=scrollbar.set)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.task_listbox.yview)
        
        # Buttons frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Action buttons
        ttk.Button(button_frame, text="Complete Task", 
                  command=self.complete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit Task", 
                  command=self.edit_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Task", 
                  command=self.delete_task).pack(side=tk.LEFT, padx=5)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(self.main_frame, text="Statistics", padding="10")
        stats_frame.grid(row=4, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))
        
        self.total_tasks_var = tk.StringVar(value="Total Tasks: 0")
        self.completed_tasks_var = tk.StringVar(value="Completed Tasks: 0")
        self.pending_tasks_var = tk.StringVar(value="Pending Tasks: 0")
        
        ttk.Label(stats_frame, textvariable=self.total_tasks_var).pack()
        ttk.Label(stats_frame, textvariable=self.completed_tasks_var).pack()
        ttk.Label(stats_frame, textvariable=self.pending_tasks_var).pack()
        
        # Bind events
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        self.task_listbox.bind('<Double-Button-1>', lambda e: self.edit_task())
        
        # Initial update
        self.update_listbox()
        self.update_stats()

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        with open('tasks.json', 'w') as file:
            json.dump(self.tasks, file)

    def add_task(self):
        task_text = self.task_var.get().strip()
        if task_text:
            new_task = {
                'text': task_text,
                'completed': False,
                'date_added': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.tasks.append(new_task)
            self.task_var.set("")
            self.update_listbox()
            self.update_stats()
            self.save_tasks()

    def complete_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            self.tasks[index]['completed'] = not self.tasks[index]['completed']
            self.update_listbox()
            self.update_stats()
            self.save_tasks()

    def edit_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            task = self.tasks[index]
            
            # Create edit window
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Task")
            edit_window.geometry("400x150")
            
            # Add entry field
            edit_var = tk.StringVar(value=task['text'])
            edit_entry = ttk.Entry(edit_window, textvariable=edit_var, width=40)
            edit_entry.pack(padx=20, pady=20)
            
            def save_edit():
                new_text = edit_var.get().strip()
                if new_text:
                    task['text'] = new_text
                    self.update_listbox()
                    self.save_tasks()
                    edit_window.destroy()
            
            # Add save button
            ttk.Button(edit_window, text="Save", command=save_edit).pack()

    def delete_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
                index = selection[0]
                del self.tasks[index]
                self.update_listbox()
                self.update_stats()
                self.save_tasks()

    def update_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            prefix = "✓ " if task['completed'] else "○ "
            text = prefix + task['text']
            self.task_listbox.insert(tk.END, text)
            
            # Set color based on completion status
            if task['completed']:
                self.task_listbox.itemconfig(tk.END, fg='gray')

    def update_stats(self):
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task['completed'])
        pending = total - completed
        
        self.total_tasks_var.set(f"Total Tasks: {total}")
        self.completed_tasks_var.set(f"Completed Tasks: {completed}")
        self.pending_tasks_var.set(f"Pending Tasks: {pending}")

def main():
    root = tk.Tk()
    app = ToDoList(root)
    root.mainloop()

if __name__ == "__main__":
    main()
