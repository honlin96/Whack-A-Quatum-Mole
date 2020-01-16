# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 18:16:58 2020

@author: honlin
"""

import random as rd
import math
import tkinter as tk
import tkinter.messagebox
from PIL import Image, ImageTk

def main():
    # Create the entire GUI program
    program = WhackAMole()

    # Start the GUI event loop
    program.window.mainloop()

class WhackAMole:
    num_mole_across = 4
    status_background = "white"
    MIN_TIME_DOWN = 1000
    MAX_TIME_DOWN = 5000
    MIN_TIME_UP = 1000
    MAX_TIME_UP = 5000
    
    def __init__(self):
        self.window = tk.Tk()
        self.mole_frame, self.status_frame = self.create_frames()
        self.mole_photo = ImageTk.PhotoImage(Image.open("mole.png"))
        print(self.mole_photo)
        self.mole_cover_photo = ImageTk.PhotoImage(Image.open("mole_cover.png"))
        self.mole_button = self.create_moles()
        
        self.button_timers = {}
        self.timer, self.hit_counter, self.miss_counter, self.startbutton, self.endbutton = self.create_status_widget()
        
        self.game_is_running = False
        self.call_back()
        
    def create_frames(self):
        mole_frame = tk.Frame(self.window, bg='lightgreen', width=300, height=300)
        mole_frame.grid(row=1, column=1)

        status_frame = tk.Frame(self.window, bg='lightblue', width=100, height=300)
        status_frame.grid(row=1, column=2)

        return mole_frame, status_frame

    def create_moles(self):
        # Source of mole image: https://play.google.com/store/apps/details?id=genergame.molehammer
        mole_button = []
        for r in range(WhackAMole.num_mole_across):
            row_of_buttons = []
            for c in range(WhackAMole.num_mole_across):
                button = tk.Button(self.mole_frame, image = self.mole_photo,command = lambda r=r,c=c: self.button_call_back(r,c))
                button.image = self.mole_photo
                button.grid(row = r,column = c, padx=5, pady=5)
                row_of_buttons.append(button)
                print(button["image"])
            mole_button.append(row_of_buttons)
        return mole_button
    
    def create_status_widget(self):
        timertext = tk.Label(self.status_frame, text = "Elapsed Time", font = 'Times 12 bold', bg = "lightblue")
        timertext.pack(side = "top", expand = "True")
        
        timer = tk.Label(self.status_frame, text = " ")
        timer.pack(side = "top",expand="True")
        
        spacer = tk.Label(self.status_frame, bg = "lightblue")
        spacer.pack(side = "top",expand = "True")
        
        hit_counter_text = tk.Label(self.status_frame, text="Hit Counter", font='Times 12 bold', bg = "lightblue")
        hit_counter_text.pack(side = "top",expand = "True")
        
        hit_counter = tk.Label(self.status_frame, text = " ", bg = WhackAMole.status_background)
        hit_counter.pack(side = "top",expand = "True")
        
        spacer = tk.Label(self.status_frame, bg = "lightblue")
        spacer.pack(side = "top",expand = "True")
        
        miss_counter_text = tk.Label(self.status_frame, text = "Miss Counter", font ='Times 12 bold', bg = "lightblue")
        miss_counter_text.pack(side = "top",expand = "True")
        
        miss_counter = tk.Label(self.status_frame,text = " ", bg = WhackAMole.status_background)
        miss_counter.pack(side = "top", expand = "True")
        
        spacer = tk.Label(self.status_frame, bg = "lightblue")
        spacer.pack(side = "top",expand = "True")
        
        startbutton = tk.Button(self.status_frame, text = "Start",font ='Times 12 bold', fg = "white", bg = "darkblue")
        startbutton.pack(side = "top", expand = "True",ipadx = 10)
        
        spacer = tk.Label(self.status_frame, bg = "lightblue")
        spacer.pack(side = "top",expand = "True")
        
        endbutton = tk.Button(self.status_frame, text = "End",font ='Times 12 bold',fg = "white", bg = "red")
        endbutton.pack(side = "top",expand = "True",ipadx = 10)
        
        spacer = tk.Label(self.status_frame, bg = "lightblue")
        spacer.pack(side = "top",expand = "True")
        
        return  timer,hit_counter, miss_counter, startbutton,endbutton
    
    def call_back(self):
        
        self.startbutton["command"] = self.start
        
        self.endbutton["command"] = self.end
    
    def button_call_back(self,row,column):
         # Set the same callback for each mole button
        for r in range(WhackAMole.num_mole_across):
            for c in range(WhackAMole.num_mole_across):
                self.mole_hit(self.mole_button[row][column])
        
    def mole_hit(self,event_widget):
        
        if self.game_is_running:
            if str(event_widget["image"]) == str(self.mole_photo):
                #hit, update the hit counter
                print("Mole button hit")
                self.hit_counter['text'] = str(int(self.hit_counter['text']) + 1)
                # Remove the mole and don't update the miss counter
                self.put_down_mole(event_widget, False)
            else:
                #miss, update the miss counter
                self.miss_counter["text"] = str(int(self.miss_counter['text']) + 1)
                self.put_down_mole(event_widget, False)
        
    def put_down_mole(self,event_widget,timer_expired):
        if self.game_is_running:
            if timer_expired:
                # The mole is going down before it was clicked on, so update the miss counter
                self.miss_counter['text'] = str(int(self.miss_counter['text']) + 1)
            else:
                # The timer did not expire, so manually stop the timer
                event_widget.after_cancel(self.mole_timers[id(event_widget)])

            # Make the mole invisible
            event_widget['image'] = self.mole_cover_photo
            
            # Set a call to pop up the mole in the future
            time_down = rd.randint(WhackAMole.MIN_TIME_DOWN,
                                WhackAMole.MAX_TIME_DOWN)
            timer_object = event_widget.after(time_down, self.pop_up_mole, event_widget)
            # Remember the timer object so it can be canceled later, if need be
            self.button_timers[id(event_widget)] = timer_object
    
    def pop_up_mole(self, event_widget):
        # Show the mole on the screen
        event_widget['image'] = self.mole_photo

        if self.game_is_running:
            # Set a call to make the mole disappear in the future
            time_up = rd.randint(WhackAMole.MIN_TIME_UP, WhackAMole.MAX_TIME_UP)
            timer_object = event_widget.after(time_up, self.put_down_mole,
                                           event_widget, True)
            self.button_timers[id(event_widget)] = timer_object
            
    def start(self):
        if self.startbutton['text'] == 'Start':
            # Change all the mole images to a blank image and
            # set a random time for the moles to re-appear on each label.
            for r in range(WhackAMole.num_mole_across):
                for c in range(WhackAMole.num_mole_across):
                    button = self.mole_button[r][c]
                    button['image'] = self.mole_cover_photo
                    time_down = rd.randint(WhackAMole.MIN_TIME_DOWN,
                                        WhackAMole.MAX_TIME_DOWN)
                    timer_object = button.after(time_down,
                                                   self.pop_up_mole, button)
                    self.button_timers[id(button)] = timer_object

            self.game_is_running = True
            self.startbutton['text'] = "Stop"

            self.hit_counter['text'] = "0"
            self.miss_counter['text'] = "0"

        else:  # The game is running, so stop the game and reset everything
            # Show every mole and stop all the timers
            for r in range(WhackAMole.num_mole_across):
                for c in range(WhackAMole.num_mole_across):
                    button = self.mole_button[r][c]
                    # Show the mole
                    button['image'] = self.mole_photo
                    # Delete any timer that is associated with the mole
                    button.after_cancel(self.button_timers[id(button)])

            self.game_is_running = False
            self.startbutton['text'] = "Start"
            
    def end(self):
        print("End button hit")
        really_quit = tkinter.messagebox.askyesno("Quiting?", "Do you really want to quit?")
        if really_quit:
            self.window.destroy()
if __name__ == "__main__":
    main()