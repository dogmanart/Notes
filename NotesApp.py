import customtkinter as ctk
import tkinter
import json

savefile = "savedata.json"

def save():
    data = {"names":notes, "text":notetext}
    with open(savefile, 'w') as f:
            json.dump(data, f)

def load():
    global notes, notetext
    try:
        with open(savefile, 'r') as f:
            data = json.load(f)
            notes = data.get("notes", ['New Note'])
            notetext = data.get("text", [])
    except FileNotFoundError:
        pass

window = ctk.CTk()
window.title("Notes")
window.geometry("1000x1000")

notes = ["My Note"]
notetext = [""]

appframe = ctk.CTkFrame(window, width=1000, height=1000, fg_color="#181818")
appframe.pack(side='left', expand=True)
appframe.pack_propagate(False)

ctk.set_appearance_mode("dark")

notesframe = ctk.CTkScrollableFrame(appframe, height=980, width=200)
notesframe.pack(pady=10, padx=10, side='left', )

def newnote():
    notes.append("Note")
    notetext.append("")
    refreshnotes()


newnotebut = ctk.CTkButton(notesframe, text="New Note", font=("Arial", 11,'bold'), height=60, width=190, fg_color="#10975D", hover_color="#0E7B4C", corner_radius=17, command=newnote)
newnotebut.pack(pady=5, padx=5, )

def refreshnotes():
    for widget in notesframe.winfo_children():
        if widget != newnotebut:
            widget.destroy()
    for i in range(len(notes)):
        note = ctk.CTkButton(notesframe, text=notes[i], font=("Arial", 11,'bold'), height=60, width=190, fg_color="#333333", hover_color="#3F4D46", corner_radius=17, border_color="#ffffff", border_width=1)
        note.pack(pady=5, padx=5)
    save()
refreshnotes()

buttonframe = ctk.CTkFrame(appframe, height=40, width=760, border_color="#10975D", border_width=2)
buttonframe.pack(pady=10, padx=10, side='top')
buttonframe.grid_propagate(False)

textframe = ctk.CTkTextbox(appframe, height=920, width=760, border_color="#10975D", border_width=2)
textframe.pack(pady=10, padx=10, side='right')

italicbutton = ctk.CTkButton(buttonframe, fg_color="#10975D", hover_color="#0E7B4C", text="Italic")
italicbutton.grid(row=0, column=0, pady=5, padx=5)

load()

window.mainloop()