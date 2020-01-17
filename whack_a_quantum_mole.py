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

from qiskit import(
  QuantumCircuit,
  ClassicalRegister,
  execute,
  Aer)

def measurement_result(outputstate,measured_register,qubitnumber):
    for index,element in enumerate(outputstate):
        if element != 0:
            ket = bin(index)[2:].zfill(qubitnumber)
            #print("The ket is |"+str(ket) +"> with probability amplitude " + str(element))
            result = ket[qubitnumber-measured_register-1] #the ket is read from right to left(|987654321>)
            break #break the iteration since we have obtained the result
    #print("The qubit collapsed to " + result)
    return result


def braket_notation(outputstate,qubitnumber):
    #print out the wavefunction in braket notation.
    #binary reads from right to left
    ket = ''
    for index,element in enumerate(outputstate):
        if element != 0:
            if ket == '':
            #only print out states with non-zero probability amplitude
                ket += str(element)+'|'+ bin(index)[2:].zfill(qubitnumber) +'>'
               # print(index)
            else:
                ket = ket + ' + ' + str(element)+'|'+ bin(index)[2:].zfill(qubitnumber) +'>'
               # print(index)
    return ket


def main():
    # Create the entire GUI program
    program = WhackAMole()
    # Start the GUI event loop
    program.window.mainloop()

class WhackAMole:
    num_mole_across = 3
    status_background = "white"
    MIN_TIME_DOWN = 3000
    MAX_TIME_DOWN = 5000
    MIN_TIME_UP = 3000
    MAX_TIME_UP = 5000
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("WhackAQuantumMole")
        self.mole_frame, self.status_frame = self.create_frames()
        
        self.mole_photo = ImageTk.PhotoImage(Image.open("mole.png"))
        self.mole_cover_photo = ImageTk.PhotoImage(Image.open("mole_cover.png"))
        self.mole_button = self.create_moles()
        
        self.quantum_mole_photo = ImageTk.PhotoImage(Image.open("quantum_mole.png"))
        # Use Aer's statevector simulator
        self.simulator = Aer.get_backend('statevector_simulator')
        
        self.button_timers = {}
        self.timer, self.hit_counter, self.miss_counter, self.startbutton, self.quantumstartbutton,self.endbutton = self.create_status_widget()
        
        self.game_is_running = False
        self.is_quantum = False
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
        
        quantumstartbutton = tk.Button(self.status_frame, text = "Go Quantum!",font ='Times 12 bold', fg = "white", bg = "darkblue")
        quantumstartbutton.pack(side = "top", expand = "True",ipadx = 10)
        
        spacer = tk.Label(self.status_frame, bg = "lightblue")
        spacer.pack(side = "top",expand = "True")
        
        endbutton = tk.Button(self.status_frame, text = "End",font ='Times 12 bold',fg = "white", bg = "red")
        endbutton.pack(side = "top",expand = "True",ipadx = 10)
        
        spacer = tk.Label(self.status_frame, bg = "lightblue")
        spacer.pack(side = "top",expand = "True")
        
        return  timer,hit_counter, miss_counter, startbutton, quantumstartbutton, endbutton
    
    def create_quantum_circuit(self):
        if self.is_quantum:
            classicalregister = ClassicalRegister(1)
            circuit = QuantumCircuit(WhackAMole.num_mole_across*WhackAMole.num_mole_across,1)
        return circuit,classicalregister
    
    def call_back(self):
        
        self.startbutton["command"] = self.start
        self.quantumstartbutton["command"] = self.quantumstart
        self.endbutton["command"] = self.end
    
    def button_call_back(self,row,column):
         # Set the same callback for each mole button
        self.mole_hit(self.mole_button[row][column],row*WhackAMole.num_mole_across + column )
        
    def mole_hit(self,event_widget,register_num):     
        if self.game_is_running and self.is_quantum == False:
            #classical game
            if str(event_widget["image"]) == str(self.mole_photo):
                #hit, update the hit counter
                self.hit_counter['text'] = str(int(self.hit_counter['text']) + 1)
                # Remove the mole and don't update the miss counter
                self.put_down_mole(event_widget, False,register_num)
            else:
                #miss, update the miss counter
                self.miss_counter["text"] = str(int(self.miss_counter['text']) + 1)
                self.put_down_mole(event_widget, False,register_num)
                
        elif self.game_is_running and self.is_quantum:
            if str(event_widget["image"]) == str(self.mole_photo):
                #hit, update the hit counter
                print("hit, update the hit counter")
                self.hit_counter['text'] = str(int(self.hit_counter['text']) + 1)
                # Remove the mole and don't update the miss counter
                self.put_down_mole(event_widget, False,register_num)
            elif str(event_widget["image"]) == str(self.mole_cover_photo):
                #miss, update the miss counter
                print("miss, update the miss counter")
                self.miss_counter["text"] = str(int(self.miss_counter['text']) + 1)
                self.put_down_mole(event_widget, False,register_num)
            elif str(event_widget["image"]) == str(self.quantum_mole_photo):
                self.measure(event_widget,register_num)
            
    def put_down_mole(self,event_widget,timer_expired,register_num):
        if self.game_is_running:
            if timer_expired:
                # The mole is going down before it was clicked on, so update the miss counter
                print("Time expired, update miss counter")
                self.miss_counter['text'] = str(int(self.miss_counter['text']) + 1)
            else:
                # The timer did not expire, so manually stop the timer
                print("Manually stop the timer")
                event_widget.after_cancel(self.button_timers[id(event_widget)])
            # Make the mole invisible
            event_widget['image'] = self.mole_cover_photo

            if self.is_quantum:    
                # Set a call to pop up the mole in the future
                time_down = rd.randint(WhackAMole.MIN_TIME_DOWN,
                                    WhackAMole.MAX_TIME_DOWN)
                timer_object = event_widget.after(time_down, self.pop_up_Qmole, event_widget,register_num)
                # Remember the timer object so it can be canceled later, if need be
                self.button_timers[id(event_widget)] = timer_object
            else:
                # Set a call to pop up the mole in the future
                time_down = rd.randint(WhackAMole.MIN_TIME_DOWN,
                                    WhackAMole.MAX_TIME_DOWN)
                timer_object = event_widget.after(time_down, self.pop_up_mole, event_widget,0)
                # Remember the timer object so it can be canceled later, if need be
                self.button_timers[id(event_widget)] = timer_object
        
    def pop_up_mole(self, event_widget,register_num):
        # Show the mole on the screen
        event_widget['image'] = self.mole_photo

        if self.game_is_running:
            # Set a call to make the mole disappear in the future
            time_up = rd.randint(WhackAMole.MIN_TIME_UP, WhackAMole.MAX_TIME_UP)
            timer_object = event_widget.after(time_up, self.put_down_mole,
                                           event_widget, True,register_num)
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
                                                   self.pop_up_mole, button,0)
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
            
    def quantumstart(self):
        #quantum version
        if self.quantumstartbutton["text"] == 'Go Quantum!': 
            self.is_quantum = True
            self.quantum_circuit,self.classical_register = self.create_quantum_circuit() 
            # Change all the mole images to a blank image and
            # set a random time for the quantum moles to re-appear on each label.
            for r in range(WhackAMole.num_mole_across):
                for c in range(WhackAMole.num_mole_across):
                    button = self.mole_button[r][c]
                    button['image'] = self.mole_cover_photo
                    time_down = rd.randint(WhackAMole.MIN_TIME_DOWN,
                                        WhackAMole.MAX_TIME_DOWN)
                    register_num = r*WhackAMole.num_mole_across + c
                    timer_object = button.after(time_down,
                                                   self.pop_up_Qmole, button, register_num)
                    self.button_timers[id(button)] = timer_object
            
            self.game_is_running = True
            
            self.quantumstartbutton["text"] = "Stop"

            self.hit_counter['text'] = "0"
            self.miss_counter['text'] = "0"
        else:  # The game is running, so stop the game and reset everything
            # Show every mole and stop all the timers
            for r in range(WhackAMole.num_mole_across):
                for c in range(WhackAMole.num_mole_across):
                    button = self.mole_button[r][c]
                    # Show the mole
                    print("Change the photo")
                    button['image'] = self.mole_photo
                    # Delete any timer that is associated with the mole
                    button.after_cancel(self.button_timers[id(button)])

            self.game_is_running = False
            self.is_quantum = False
            self.quantumstartbutton['text'] = "Go Quantum!"
    
    def pop_up_Qmole(self,event_widget,register_num):
        #Show up the Quantum Mole pic
        event_widget["image"] = self.quantum_mole_photo
        #Change the quantum state of the mole from |0> to (|0> + |1>)/sqrt(2)
        self.quantum_circuit.h(register_num)
        if self.game_is_running and self.is_quantum:
            # Set a call to measure the mole in the future
            time_up = rd.randint(WhackAMole.MIN_TIME_UP, WhackAMole.MAX_TIME_UP)
            timer_object = event_widget.after(time_up, self.measure,
                                           event_widget, register_num)
            self.button_timers[id(event_widget)] = timer_object
    
    def measure(self,event_widget,register_num):
        print("Perform measurement on register {}".format(register_num))
        self.quantum_circuit.measure(register_num,0)
        job = execute(self.quantum_circuit,self.simulator)
        result = job.result()
        outputstate = result.get_statevector()
        state = measurement_result(outputstate,register_num,WhackAMole.num_mole_across*WhackAMole.num_mole_across)
        print(int(state))
        if int(state) == 0:
            print("put down mole")
            self.put_down_mole(event_widget,True,register_num)
        elif int(state) == 1:
            print("pop up mole")
            self.pop_up_mole(event_widget,register_num)
           
    def end(self):
        print("End button hit")
        really_quit = tkinter.messagebox.askyesno("Quiting?", "Do you really want to quit?")
        if really_quit:
            self.window.destroy()
if __name__ == "__main__":
    main()