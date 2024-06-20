import os
import json
import random

import subprocess
import sys
from tkinter import StringVar
from functools import partial
from tkinter import Tk, Button
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


class Question(object):
    text = ''
    var_a = ''
    var_b = ''
    var_c = ''
    var_ok = ''

    def __init__(self):
        pass

    def __init__(self,text, var_a, var_b, var_c, var_ok):
        self.var_a = var_a
        self.var_b = var_b
        self.var_c = var_c
        self.var_ok = var_ok
        self.text = text


class Runners(object):

    hits = 0
    fails = 0
    max_question_count = 0
    current_question_count = 0
    intrebari = {}

    window = tk.Tk()
    window.title = "Test RU"
    window.geometry("1080x560")
    window.columnconfigure(0, weight=1,minsize=250)
    window.rowconfigure([0, 1, 2, 3], weight=1,minsize=100)
    window.configure(bg='lightblue')

    q_test = StringVar()
    var_a = StringVar()
    var_b = StringVar()
    var_c = StringVar()
    hits_var = IntVar()
    fails_var = IntVar()
    curr_q_count = StringVar()

    frm_q = tk.Frame(master=window, height=100)
    lbl_q = tk.Label(master=frm_q, textvariable=q_test, font=("Arial", 20), wraplength=900, justify="center", bg='lightblue' ).pack()

    frm_ans = tk.Frame(master=window, bg='lightblue')
    frm_ans.rowconfigure([0,1,2], weight=1, minsize=80)
    frm_ans.columnconfigure(0, weight=1, minsize=230)

    btn_a = Button(master=frm_ans, textvariable=var_a, font=("Helvetica",10,'bold'),wraplength=900, justify="center")
    btn_b = Button(master=frm_ans, textvariable=var_b, font=("Helvetica",10,'bold'),wraplength=900, justify="center")
    btn_c = Button(master=frm_ans, textvariable=var_c, font=("Helvetica",10,'bold'),wraplength=900, justify="center")

    frm_next = tk.Frame(master=window)
    btn_next = Button(master=frm_next, text="Next", state="disabled", bg='blue')

    frm_summary = tk.Frame(master=window)
    frm_summary.rowconfigure(0, weight=1, minsize=80)
    frm_summary.columnconfigure([0,1,2], weight=1, minsize=230)
    lbl_curr = tk.Label(master=frm_summary, bg='lightblue', font=("Arial 10 bold"), textvariable=curr_q_count)
    lbl_hits = tk.Label(master=frm_summary, fg="green", font=("Arial 15 bold"), textvariable=hits_var, bg='lightblue')
    lbl_fails = tk.Label(master=frm_summary, fg="red", font=("Arial 15 bold"), textvariable=fails_var, bg='lightblue')


    lbl_initial = tk.Label(master=window, text="Numarul de intrebari:", font=('Helvetica 30 bold') )
    entry= ttk.Entry(window,font=('Arial 12'),width=15)
    btn_start = ttk.Button(master=window, text="Start", style="TButton")
    
    initial_screen = [lbl_initial, entry, btn_start]

    buttons = [btn_a, btn_b, btn_c]

    def __init__(self):
        with open(os.path.join(os.getcwd(), 'intrebari.json')) as f:
            self.text_json = json.load(f)
        self.intrebari = self.text_json['intrebari']
        random.shuffle(self.intrebari)
    
    def draw_initial_screen(self):
        self.lbl_initial.pack(fill=tk.Y)
        self.entry.pack(pady = 30, fill=tk.Y)
        self.btn_start.pack(pady = 30, fill=tk.Y)

        self.entry.insert(0,"20")
        self.btn_start.configure(command=self.start)
        self.window.mainloop()

    def start(self):
        nr_q = self.entry.get()
        if str.isdigit(nr_q):
            self.max_question_count = int(nr_q)
            self.start_test()
        else:
            self.lbl_initial.configure(text="DOAR NUMERE!", bg='red')

    def start_test(self):
        self.draw_test_layout()
        self.show_question()
        self.window.mainloop()
    
    def next_question(self, a):
        self.btn_next["state"] = "disabled"
        self.show_question()

    def draw_test_layout(self):

        for wg in self.initial_screen:
            wg.destroy()

        self.btn_a.grid(row=0,sticky="nsew", padx=5, pady=5)
        self.btn_b.grid(row=1,sticky="nsew", padx=5, pady=5)
        self.btn_c.grid(row=2,sticky="nsew", padx=5, pady=5)

        self.frm_q.grid(row=0,column=0,sticky='n')
        self.frm_ans.grid(row=1,column=0,sticky='n')

        self.btn_next.pack(fill=tk.BOTH)
        self.frm_next.grid(row=2,column=0,sticky='ew')
        self.btn_next.bind("<Button-1>", self.next_question)

        self.lbl_hits.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.lbl_fails.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        self.lbl_curr.grid(row=0, column=1, padx=5,pady=5, sticky="nsew")
        self.frm_summary.grid(row=3,column=0, sticky='n')


    def stub(self):pass

    def lock_options(self):
        self.btn_a.configure(command=self.stub)
        self.btn_b.configure(command=self.stub)
        self.btn_c.configure(command=self.stub)
        self.btn_next["state"] = "normal"
        
    def show_question(self):
        self.current_question_count+=1
        self.curr_q_count.set(f'Intrebarea {self.current_question_count}/{self.max_question_count}')
        for button in self.buttons:
            button.configure(bg="white")

        intrebare = self.intrebari.pop(0)
        question = Question(intrebare['intrebare'],intrebare['var_A'],intrebare['var_B'],intrebare['var_C'],intrebare['var_corecta'])

        def check_answer(answer):
            if answer == question.var_ok:
                self.hits+=1
            else:
                self.fails+=1

            self.hits_var.set(self.hits)
            self.fails_var.set(self.fails)

            for button in self.buttons:
                if button["text"][0] == question.var_ok:
                    button.configure(bg="green")
                else:
                    button.configure(bg="red")
                self.lock_options()
            if self.current_question_count >= self.max_question_count:
                self.finish()

        self.q_test.set(question.text)
        self.var_a.set(f'A. {question.var_a}')
        self.var_b.set(f'B. {question.var_b}')
        self.var_c.set(f'C. {question.var_c}')

        self.btn_a.configure(command=partial(check_answer, 'A'))
        self.btn_b.configure(command=partial(check_answer, 'B'))
        self.btn_c.configure(command=partial(check_answer, 'C'))

    def finish(self):
        for child in self.window.winfo_children():
            child.destroy()
        lbl_end = tk.Label(master=self.window, text="Final!", font =("Arial 35 bold"), bg='lightblue')
        lbl_end.grid(row=1, column=0, sticky='n')
        lbl_end = tk.Label(master=self.window, text=f"Raspunsuri corecte: {self.hits}||Raspunsuri gresite: {self.fails}", font =("Arial 35 bold"), bg='lightblue')
        lbl_end.grid(row=2, column=0, sticky='n')
        self.write_results()

        # btn_restart = tk.Button(master=self.window, text='Restart', command=self.draw_initial_screen)
        # btn_restart.grid(row=3, column=0, sticky='n')

    def write_results(self):
        if os.path.exists(os.path.join(os.getcwd(), 'rezultate.txt')):
            with open(os.path.join(os.getcwd(), 'rezultate.txt'), 'a') as f:
                f.write(f"Rasp corecte: {self.hits} - Rasp gresite: {self.fails}\n")
        else:
            with open(os.path.join(os.getcwd(), 'rezultate.txt'), 'w+') as f:
                f.write(f"Rasp corecte: {self.hits} - Rasp gresite: {self.fails}\n")



if __name__ == '__main__':
    tester = Runners()
    tester.draw_initial_screen()
    # tester.start_test()

