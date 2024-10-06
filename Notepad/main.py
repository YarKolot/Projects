import tkinter as tk
from tkinter import filedialog, colorchooser

def open_file():
    filepath = filedialog.askopenfilename()
    if filepath:
        with open(filepath, "r", encoding="utf-8") as file:
            editor.delete(1.0, tk.END)
            editor.insert(1.0, file.read())

def save_file():
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if filepath:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(editor.get(1.0, tk.END))

def change_background_color():
    new_color = colorchooser.askcolor()[1]
    if new_color:
        editor.config(bg=new_color)

def change_font_color():
    new_color = colorchooser.askcolor()[1]
    if new_color:
        editor.config(fg=new_color)

def change_cursor_color():
    new_color = colorchooser.askcolor()[1]
    if new_color:
        editor.config(insertbackground=new_color)

def copy_text(event=None):
    try:
        editor.clipboard_clear()
        editor.clipboard_append(event.widget.selection_get())
    except tk.TclError:
        pass

root = tk.Tk()
root.title("Fucking God Damn Awesome Notepad")

editor = tk.Text(root, font=("Helvetica", 15))
editor.pack(fill="both", expand=True)

menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=False)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Quit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

settings_menu = tk.Menu(menu_bar, tearoff=False)
settings_menu.add_command(label="Change background color", command=change_background_color)
settings_menu.add_command(label="Change font color", command=change_font_color)
settings_menu.add_command(label="Change cursor color", command=change_cursor_color)
menu_bar.add_cascade(label="Settings", menu=settings_menu)

root.config(menu=menu_bar)

root.bind('<Control-c>', copy_text)

root.mainloop()