import os
import sys
import tkinter as tk
from tkinter import font
import pygame

score = 0
played = False

# Window setup #
window = tk.Tk()
window.title("Minesweeper Menu")
font_status = font.Font(family="Helvetica", size=24)
font_button = font.Font(family="Helvetica", size=16)

# Functions # 
def on_end():
    global score
    print("Score: ", score)
    

def on_start():
    global played
    if played:
        os.execv(sys.executable, ['python'] + sys.argv)
    global score
    import main
    score, won = main.main()
    status_text = "You won" if won else "You lost"
    lbl_title.config(text=status_text+" with a score of: " + str(score))
    pygame.quit()
    on_end()

# Widgets #
# Title label
lbl_title = tk.Label(window, text="Minesweeper Main Menu", font=font_status)
lbl_title.pack()

# Start button
btn_start = tk.Button(window, text="Start Game", command=on_start, font=font_button)
btn_start.pack()

# Settings button
btn_settings = tk.Button(window, text="Settings", command=lambda: print("Settings"), font=font_button)
btn_settings.pack()

# Quit button
btn_quit = tk.Button(window, text="Quit", command=lambda: window.quit(), font=font_button)
btn_quit.pack()

# Run window
window.mainloop()