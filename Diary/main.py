import tkinter as tk
from tkcalendar import Calendar
import sqlite3
import datetime

conn = sqlite3.connect('diary.db', isolation_level=None)
c = conn.cursor()

c.execute("PRAGMA journal_mode=WAL")

c.execute('''
          CREATE TABLE IF NOT EXISTS diary_entries
          (id INTEGER PRIMARY KEY, date TEXT UNIQUE, entry TEXT)
          ''')

class DiaryManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Diary")

        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.current_date = self.cal.selection_get().strftime("%Y-%m-%d")
        self.update_entry()

    def create_widgets(self):
        self.cal = Calendar(self, selectmode='day', year=datetime.datetime.now().year, 
                            month=datetime.datetime.now().month, day=datetime.datetime.now().day)
        self.cal.grid(row=0, column=0, padx=0, pady=0, sticky='ns')
        self.cal.bind("<<CalendarSelected>>", self.date_changed)

        self.entry_text = tk.Text(self, wrap=tk.WORD, font=("Arial", 12))
        self.entry_text.grid(row=0, column=1, padx=(10, 0), pady=0, sticky='nsew')

        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.entry_text.yview)
        self.entry_text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=2, sticky='ns')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def update_entry(self):
        self.entry_text.delete(1.0, tk.END)
        c.execute("SELECT entry FROM diary_entries WHERE date = ?", (self.current_date,))
        entry = c.fetchone()
        if entry:
            self.entry_text.insert(tk.END, entry[0])

    def save_entry(self):
        entry_text = self.entry_text.get(1.0, tk.END).strip()
        if entry_text:
            c.execute("SELECT id FROM diary_entries WHERE date = ?", (self.current_date,))
            entry = c.fetchone()
            if entry:
                c.execute("UPDATE diary_entries SET entry = ? WHERE id = ?", (entry_text, entry[0]))
            else:
                c.execute("INSERT INTO diary_entries (date, entry) VALUES (?, ?)", (self.current_date, entry_text))
        else:
            c.execute("DELETE FROM diary_entries WHERE date = ?", (self.current_date,))

    def date_changed(self, event):
        self.save_entry()
        self.current_date = self.cal.selection_get().strftime("%Y-%m-%d")
        self.update_entry()

    def on_closing(self):
        self.save_entry()
        conn.commit()
        self.destroy()

if __name__ == "__main__":
    app = DiaryManager()
    app.mainloop()