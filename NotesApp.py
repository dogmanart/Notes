import customtkinter as ctk
import nltk
from tkinter import messagebox
import warnings
warnings.filterwarnings("ignore", message=".*chardet.*")
warnings.filterwarnings("ignore", message=".*charset_normalizer.*")
import json
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer

def summarize():
    sumtext = textframe.get("1.0", "end-1c")
    if not sumtext.strip():
        return
    parser = PlaintextParser.from_string(sumtext, Tokenizer("english"))
    summarizer = LuhnSummarizer()
    summary = summarizer(parser.document, 1)
    clean_summary = " ".join([str(sentence) for sentence in summary])
    textframe.pack_forget()
    for widget in summaryframe.winfo_children():
        widget.destroy()
    sumlabel = ctk.CTkLabel(summaryframe, text=f"Summary:\n{clean_summary.lstrip()}", justify='left', wraplength=720)
    summaryframe.pack_forget()
    sumlabel.pack_forget()
    sumlabel.pack(padx=10, pady=10, anchor='nw')
    textframe.configure(height=400)
    textframe.pack(pady=10, padx=10)
    summaryframe.pack(pady=10, padx=10, fill='both', expand=True)
    window.update()

savefile = "savedata.json"

def save():
    data = {"names":notes,"text":notetext}
    with open(savefile, 'w') as f:
            json.dump(data, f)

def load():
    global notes, notetext
    try:
        with open(savefile, 'r') as f:
            data = json.load(f)
            notes = data.get("names", [])
            notetext = data.get("text", [])
    except (FileNotFoundError, json.JSONDecodeError):
        notes, notetext = [], []

notes = []
notetext = []

def destroywindow():
    save()
    window.destroy()

window = ctk.CTk()
window.title("Notes")
window.protocol("WM_DELETE_WINDOW", destroywindow)
window.geometry("1000x1000")

appframe = ctk.CTkFrame(window, width=1000, height=1000, fg_color="#181818")
appframe.pack(side='left', expand=True)
appframe.pack_propagate(False)

ctk.set_appearance_mode("dark")

notesframe = ctk.CTkScrollableFrame(appframe, height=980, width=200)
notesframe.pack(pady=10, padx=10, side='left', )

def newnote():
    notes.append(f"Note {len(notes)+1}")
    notetext.append("")
    refreshnotes()


newnotebut = ctk.CTkButton(notesframe, text="New Note", font=("Arial", 11,'bold'), height=60, width=190, fg_color="#10975D", hover_color="#0E7B4C", corner_radius=17, command=newnote)
newnotebut.pack(pady=5, padx=5, )

load()

def deletenote(index):
    global selectednote
    if messagebox.askyesno("Warning", "Do you really want to delete this note forever?"):
        notes.pop(index)
        notetext.pop(index)
        selectednote = 0
        refreshnotes()
    else: pass

selectednote = 0

def selectnote(index):
    global selectednote
    summaryframe.pack_forget()
    buttonframe.pack(pady=10, padx=10, side='top')
    textframe.pack(pady=10, padx=10, side='top', fill='both', expand=True)
    if selectednote != index:
        textframe.delete("1.0", "end")
        textframe.insert("1.0", notetext[index])
        selectednote = index
    else: 
        deletenote(index)
    save()
    refreshnotes()

def refreshnotes():
    for widget in notesframe.winfo_children():
        if widget != newnotebut:
            widget.destroy()
    for i in range(len(notes)):
        if i != selectednote:
            note = ctk.CTkButton(notesframe, text=notes[i], font=("Arial", 11,'bold'), height=60, width=190, fg_color="#333333", hover_color="#3F4D46", corner_radius=17, border_color="#ffffff", border_width=1, command=lambda i=i: selectnote(i))
        else:
            note = ctk.CTkButton(notesframe, text=notes[i], font=("Arial", 11,'bold'), height=60, width=190, fg_color="#257E4B", hover_color="#4E6A5C", corner_radius=17, border_color="#ffffff", border_width=1, command=lambda i=i: selectnote(i))

        note.pack(pady=5, padx=5)
    save()
refreshnotes()

buttonframe = ctk.CTkFrame(appframe, height=40, width=760, border_color="#10975D", border_width=2)
buttonframe.pack(pady=10, padx=10, side='top')
buttonframe.pack_propagate(False)

textframe = ctk.CTkTextbox(appframe, height=920, width=760, border_color="#10975D", border_width=2, wrap='word')
textframe.pack(pady=10, padx=10, side='top', fill='both', expand=True)

sumbutton = ctk.CTkButton(buttonframe, fg_color="#10975D", hover_color="#0E7B4C", text="Summarize", command=summarize)
sumbutton.pack(side='left', pady=5, padx=5)
summaryframe = ctk.CTkFrame(appframe, height=200, width=760, border_color="#10975D", border_width=2, fg_color="#1F1F1F")

if len(notes) < 1:
    notes.append("My Note")
    refreshnotes()

window.mainloop()
