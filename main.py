import tkinter as tk
from tkinter import messagebox
import pygame         #For alarm
import json

try:
    data = {
        'work_timer_length': 1500,
        'rest_timer_length': 300, 
        }
    with open("data.json", "x") as file:
        json.dump(data, file)
        
    with open("data.json", "r") as file:
        data = json.load(file)
except:
    with open("data.json", "r") as file:
        data = json.load(file)

dark_theme_color = '#121212'
work_timer_length = data['work_timer_length']   # time is in seconds
rest_timer_length = data['rest_timer_length']

root = tk.Tk()
root.title("Pomodoro_helper")
root.geometry('350x400')
root.config(bg=dark_theme_color)
settings_icon = tk.PhotoImage(file='data/settings-32x32.png')
checkmark_icon = tk.PhotoImage(file='data/checkmark-16x16.png')
app_icon = tk.PhotoImage(file="data/tomato-32x32.png")
root.iconphoto(False, app_icon)
pygame.mixer.init()
pygame.mixer.music.load("data/alarm.MP3")    

def save_data():
    with open('data.json', 'w') as file:
        json.dump(data, file)

def start_timer():
    start_timer_button.config(state="disabled")
    start_work_session()

def start_rest_session():
    global rest_timer_length, start_timer_button
    start_timer_button.config(state="disabled")
    if rest_timer_length > 0:
        rest_timer_length -= 1
        minutes_left, seconds_left = divmod(rest_timer_length, 60)
        update_timer_text(minutes_left, seconds_left)
        root.after(1000, start_rest_session)
    else:
        play_alarm()
        tk.messagebox.showinfo("Notification", "Rest session is over")
        start_timer_button.config(text="Start pomodoro", command=start_timer, state='normal')

def start_work_session():
    global work_timer_length
    if work_timer_length > 0:
        work_timer_length -= 1
        minutes_left, seconds_left = divmod(work_timer_length, 60)
        update_timer_text(minutes_left, seconds_left)
        root.after(1000, start_work_session)
    else:
        play_alarm()
        tk.messagebox.showinfo("Notification", "Work session is over")
        start_timer_button.config(text="Start rest", command=start_rest_session, state="normal")       

def play_alarm():
    pygame.mixer.music.play()

def update_timer_text(minutes, seconds):
    timer_text.config(text=f"{minutes:02}:{seconds:02}")
    
def set_work_time():
    work_time_entry_value = work_time_entry.get()
    if work_time_entry_value.isdigit:
        if work_time_entry_value < 61:
            data['work_timer_length'] = work_time_entry_value * 60

def open_settings():
    global work_time_entry
    settings = tk.Toplevel(root)
    settings.title("Settings")
    settings.geometry('350x400')
    settings.config(bg=dark_theme_color)
    settings.iconbitmap("data/tomato-32x32.ico")
    settings.grab_set()

    #Objects in settings window
    work_time_label = tk.Label(settings, text=f"Current work time length is {int(work_timer_length / 60)} minutes.", bg=dark_theme_color, fg='white', font=("Arial", 12), )
    work_time_label.place(relx=0, rely=0.1, anchor='w')

    work_time_entry = tk.Entry(settings, bg=dark_theme_color, fg='white', font=('Arial', 10))
    work_time_entry.place(relx=0.05, rely=0.15, anchor='w', width=30)
    
    work_confirm_button = tk.Button(settings, image=checkmark_icon,bg=dark_theme_color ,relief='flat' ,command=set_work_time)
    work_confirm_button.place(relx=0.15, rely=0.15, anchor='w')

#Objects in root window    
settings_button = tk.Button(root, image=settings_icon, bg=dark_theme_color ,relief='flat' ,command=open_settings)
settings_button.place(relx=0.9, rely=0.1, anchor=tk.CENTER)

start_timer_button = tk.Button(root, text="Start pomodoro", command=start_timer)
start_timer_button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

timer_text = tk.Label(root, font=("Arial", 24), bg=dark_theme_color, fg="white")
timer_text.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

root.mainloop()
