import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

TASKS_FILE = "tasks.json"

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.tasks = []

        # Listbox
        self.task_listbox = tk.Listbox(root, width=60, height=15)
        self.task_listbox.pack(pady=10)

        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack()

        buttons = [
            ("Add Task", self.add_task),
            ("Edit Task", self.edit_task),
            ("Delete Task", self.delete_task),
            ("Mark as Done", self.mark_done),
            ("Save", self.save_tasks),
            ("Load", self.load_tasks)
        ]

        for i, (text, command) in enumerate(buttons):
            tk.Button(button_frame, text=text, width=12, command=command).grid(row=0, column=i, padx=5)

        self.load_tasks()

    def add_task(self):
        title = simpledialog.askstring("New Task", "Enter task title:")
        if title:
            priority = simpledialog.askstring("Priority", "Enter priority (Low/Medium/High):")
            due_date = simpledialog.askstring("Due Date", "Enter due date (YYYY-MM-DD):")
            self.tasks.append({
                "title": title,
                "priority": priority,
                "due": due_date,
                "done": False
            })
            self.update_listbox()

    def edit_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to edit.")
            return
        index = selected[0]
        task = self.tasks[index]

        new_title = simpledialog.askstring("Edit Task", "Edit title:", initialvalue=task["title"])
        new_priority = simpledialog.askstring("Edit Priority", "Edit priority:", initialvalue=task.get("priority", ""))
        new_due = simpledialog.askstring("Edit Due Date", "Edit due date:", initialvalue=task.get("due", ""))

        if new_title:
            self.tasks[index] = {
                "title": new_title,
                "priority": new_priority,
                "due": new_due,
                "done": task["done"]
            }
            self.update_listbox()

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to delete.")
            return
        del self.tasks[selected[0]]
        self.update_listbox()

    def mark_done(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a task to mark as done.")
            return
        self.tasks[selected[0]]["done"] = True
        self.update_listbox()

    def update_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✔" if task["done"] else "❌"
            prio = f"[{task['priority']}]" if task.get("priority") else ""
            due = f"(Due: {task['due']})" if task.get("due") else ""
            self.task_listbox.insert(tk.END, f"{status} {task['title']} {prio} {due}")

    def save_tasks(self):
        try:
            with open(TASKS_FILE, "w") as f:
                json.dump(self.tasks, f, indent=4)
            messagebox.showinfo("Success", "Tasks saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving tasks: {e}")

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            try:
                with open(TASKS_FILE, "r") as f:
                    self.tasks = json.load(f)
                self.update_listbox()
            except Exception as e:
                messagebox.showerror("Error", f"Error loading tasks: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
