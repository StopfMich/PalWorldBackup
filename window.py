import os
import sys

import BackUp
from tkinter import *
from tkinter import filedialog

#  some variables
stop_thread = False
documents_folder = os.path.expanduser("~/Documents")
save_folder = ""
backup_folder = ""
backup_time = 0
settings_file = os.path.join(os.path.expanduser('~'), "PalWorldBackup-settings.txt")  # File to save the settings

def btn_clicked():
    save_settings()
    global save_folder
    global backup_folder
    global backup_time
    save_folder = entry0.get()
    backup_folder = entry1.get()
    backup_time = int(entry2.get())
    BackUp.make_backup(save_folder, backup_folder, backup_time)

def on_window_close():
    BackUp.stop()
    window.destroy()


def save_folder_clicked(event):
    print("Save Folder Clicked")
    global save_folder
    save_folder = filedialog.askdirectory(
        initialdir="C:/Program Files (x86)/Steam/steamapps/common/PalServer/Pal/Saved/SaveGames")
    entry0.delete(0, END)
    entry0.insert(0, save_folder)


def backup_folder_clicked(event):
    print("Backup Folder Clicked")
    global backup_folder
    backup_folder = filedialog.askdirectory(initialdir=documents_folder)
    entry1.delete(0, END)
    entry1.insert(0, backup_folder)


def save_settings():
    with open(settings_file, 'w') as f:
        f.write(f"{entry0.get()}\n")
        f.write(f"{entry1.get()}\n")
        f.write(f"{entry2.get()}\n")


def load_settings():
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as f:
            lines = f.readlines()
            entry0.insert(0, lines[0].strip())
            entry1.insert(0, lines[1].strip())
            entry2.insert(0, lines[2].strip())
    else:
        # set default values
        entry0.insert(0, "C:/Program Files (x86)/Steam/steamapps/common/PalServer/Pal/Saved/SaveGames")  # save folder
        entry1.insert(0, documents_folder + "/PalBackUps")  # backup folder
        entry2.insert(0, "2")  # backup time


window = Tk()

window.geometry("1091x589")
window.configure(bg="#000000")
canvas = Canvas(
    window,
    bg="#000000",
    height=589,
    width=1091,
    bd=0,
    highlightthickness=0,
    relief="ridge")
canvas.place(x=0, y=0)

background_img = PhotoImage(file=BackUp.resource_path(f"img/background.png"))
background = canvas.create_image(
    533.5, 296.5,
    image=background_img)

entry0_img = PhotoImage(file=BackUp.resource_path(f"img/img_textBox0.png"))
entry0_bg = canvas.create_image(
    128.0, 147.0,
    image=entry0_img)

entry0 = Entry(
    bd=0,
    bg="#ffffff",
    highlightthickness=0)

entry0.place(
    x=16.0, y=136,
    width=224.0,
    height=20)

entry0.bind("<Button-1>", save_folder_clicked)

entry1_img = PhotoImage(file=BackUp.resource_path(f"img/img_textBox1.png"))
entry1_bg = canvas.create_image(
    128.0, 270.0,
    image=entry1_img)

entry1 = Entry(
    bd=0,
    bg="#ffffff",
    highlightthickness=0)

entry1.place(
    x=16.0, y=259,
    width=224.0,
    height=20)

entry1.bind("<Button-1>", backup_folder_clicked)

entry2_img = PhotoImage(file=BackUp.resource_path(f"img/img_textBox2.png"))
entry2_bg = canvas.create_image(
    136.5, 393.0,
    image=entry2_img)

entry2 = Entry(
    bd=0,
    bg="#ffffff",
    highlightthickness=0)

entry2.place(
    x=16.0, y=382,
    width=241.0,
    height=20)

img0 = PhotoImage(file=BackUp.resource_path(f"img/img0.png"))
b0 = Button(
    image=img0,
    borderwidth=0,
    highlightthickness=0,
    command=btn_clicked,
    relief="flat")

b0.place(
    x=32, y=472,
    width=277,
    height=88)

window.resizable(False, False)
load_settings()
window.protocol("WM_DELETE_WINDOW", on_window_close)
window.iconbitmap(BackUp.resource_path(f"img/PalWorldBackup.ico"))
window.title("PalWorld Backup")
window.mainloop()
