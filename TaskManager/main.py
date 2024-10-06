import tkinter as tk
from tkinter import simpledialog, Scrollbar
from tkcalendar import Calendar
import sqlite3
import datetime

conn = sqlite3.connect('base.db')
c = conn.cursor()

c.execute('''
          CREATE TABLE IF NOT EXISTS tasks
          (id INTEGER PRIMARY KEY, date TEXT, task TEXT, completed BOOLEAN)
          ''')
conn.commit()

class TaskManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Manager")
        self.geometry("1012x300")
        self.resizable(False, False)
        
        self.create_widgets()
        self.update_tasks()

    def create_widgets(self):
        self.cal = Calendar(self, selectmode='day', year=datetime.datetime.now().year, 
                            month=datetime.datetime.now().month, day=datetime.datetime.now().day)
        self.cal.grid(row=0, column=0, padx=10, pady=10, rowspan=2)
        self.cal.bind("<<CalendarSelected>>", lambda event: self.update_tasks())

        self.task_frame = tk.Frame(self)
        self.task_frame.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky='ns')

        self.task_listbox = tk.Listbox(self.task_frame, width=100, height=10, font=("Arial", 9))
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar = Scrollbar(self.task_frame, orient="vertical")
        self.scrollbar.config(command=self.task_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky='ew')
        self.button_frame.columnconfigure([0, 1, 2], weight=1)

        self.create_task_button = tk.Button(self.button_frame, text="New Task", command=self.create_task)
        self.create_task_button.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.complete_task_button = tk.Button(self.button_frame, text="Complete Task", command=self.complete_task)
        self.complete_task_button.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.delete_task_button = tk.Button(self.button_frame, text="Delete Task", command=self.delete_task)
        self.delete_task_button.grid(row=0, column=2, padx=5, pady=5, sticky='ew')

        self.counter_frame = tk.Frame(self)
        self.counter_frame.grid(row=4, column=0, columnspan=2, pady=5, sticky='ew')
        self.counter_frame.columnconfigure([0, 1, 2], weight=1)

        self.total_tasks_label = tk.Label(self.counter_frame, text="Total Tasks: 0")
        self.total_tasks_label.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.completed_tasks_label = tk.Label(self.counter_frame, text="Completed Tasks: 0")
        self.completed_tasks_label.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.missed_tasks_label = tk.Label(self.counter_frame, text="Missed Tasks: 0")
        self.missed_tasks_label.grid(row=0, column=2, padx=5, pady=5, sticky='ew')

    def update_tasks(self):
        selected_date = self.cal.selection_get().strftime("%Y-%m-%d")
        self.task_listbox.delete(0, tk.END)

        c.execute("SELECT id, task, completed FROM tasks WHERE date = ?", (selected_date,))
        tasks = c.fetchall()

        for task_id, task, completed in tasks:
            display_text = task
            if completed:
                display_text += " (Completed)"
            self.task_listbox.insert(tk.END, display_text)
            if completed:
                self.task_listbox.itemconfig(tk.END, {'bg':'green', 'fg': 'white'})
            else:
                self.task_listbox.itemconfig(tk.END, {'bg':'red', 'fg': 'white'})
        
        self.update_counters()

    def create_task(self):
        selected_date = self.cal.selection_get().strftime("%Y-%m-%d")
        task_text = simpledialog.askstring("Input", f"Enter task for {selected_date}:")
        if task_text:
            c.execute("INSERT INTO tasks (date, task, completed) VALUES (?, ?, ?)", (selected_date, task_text, False))
            conn.commit()
            self.update_tasks()

    def complete_task(self):
        selected_date = self.cal.selection_get().strftime("%Y-%m-%d")
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            task_text = self.task_listbox.get(task_index)
            task_text = task_text.replace(" (Completed)", "")
            
            c.execute("SELECT id FROM tasks WHERE date = ? AND task = ?", (selected_date, task_text))
            task_id = c.fetchone()[0]
            
            c.execute("UPDATE tasks SET completed = ? WHERE id = ?", (True, task_id))
            conn.commit()
            self.update_tasks()

    def delete_task(self):
        selected_date = self.cal.selection_get().strftime("%Y-%m-%d")
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            task_text = self.task_listbox.get(task_index)
            task_text = task_text.replace(" (Completed)", "")
            
            c.execute("SELECT id FROM tasks WHERE date = ? AND task = ?", (selected_date, task_text))
            task_id = c.fetchone()[0]
            
            c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            self.update_tasks()

    def update_counters(self):
        c.execute("SELECT COUNT(*) FROM tasks")
        total_tasks = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM tasks WHERE completed = 1")
        completed_tasks = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM tasks WHERE completed = 0 AND date < ?", (datetime.datetime.now().strftime("%Y-%m-%d"),))
        missed_tasks = c.fetchone()[0]

        self.total_tasks_label.config(text=f"Total Tasks: {total_tasks}")
        self.completed_tasks_label.config(text=f"Completed Tasks: {completed_tasks}")
        self.missed_tasks_label.config(text=f"Missed Tasks: {missed_tasks}")

if __name__ == "__main__":
    app = TaskManager()
    app.mainloop()