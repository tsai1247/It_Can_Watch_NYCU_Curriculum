#!/usr/bin/python3
# -*- coding: utf-8 -*-

import threading
from time import sleep
import tkinter as tk
import tkinter.ttk as ttk
from It_Can_Watch_NYCU_Curriculum import getCurriculum
from os.path import isfile
import json
from typing import List, Dict

font = ('Arial', 10)
week_keywords = 'UMTWRFS'
time_keywords = 'yz1234n56789abcd'
def getlocation(key: str):
    dateandtime = key.split('-')[0]
    date, time = dateandtime[0], dateandtime[1:]
    
    row = time_keywords.find(time[0]) + 1
    column = week_keywords.find(date) + 1
    rowspan = len(time)
    columnspan = 1

    return row, column, rowspan, columnspan

def readCurriculum():
    global Curriculums
    for curriculum in Curriculums:
        curriculum.grid_forget()
    
    Curriculums.clear()
    try:
        data: List[Dict] = json.loads(open('data.json', 'r', encoding='utf-8').read())
    except:
        return False

    for curriculum in data:
        row, column, rowspan, columnspan = getlocation(curriculum['上課時間/教室'])
        curriculum_frame = tk.Frame(frame)
        empty = tk.Label(curriculum_frame, width=15*columnspan, height=3*rowspan, background='lightgreen', borderwidth=1.5, relief='solid')
        empty.grid(row=0, column=0, rowspan=3, columnspan=1)
        curriculum_frame.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, padx=1, pady=1)
        Curriculums.append(curriculum_frame)
        print(curriculum['課程名稱'], row, column)

        cos_name = tk.Label(curriculum_frame, text=curriculum['課程名稱'], background='lightgreen', wraplength=85)
        cos_name.grid(row=0, column=0)
        tea_name = tk.Label(curriculum_frame, text=curriculum['授課教師'], background='lightgreen', wraplength=85)
        tea_name.grid(row=1, column=0)
        cos_credit = tk.Label(curriculum_frame, text=curriculum['學分數'], background='lightgreen', wraplength=85)
        cos_credit.grid(row=2, column=0)
    
    canvas.config(width=600, height=600)
    canvas.config(scrollregion=canvas.bbox("all"))

def task():
    issuccess = getCurriculum()
    if issuccess:
        readCurriculum()

def confirmed():
    open('account', 'w', encoding='utf-8').write(f'{acnt_var.get()}\n{pwd_var.get()}\n')
    window.destroy()

def on_closing():
    window.destroy()
    exit()

font_title = ('標楷體', 14, 'bold')
font_content = ('微軟正黑體', 12)

if not isfile('account') or len(open('account', 'r', encoding='utf-8').read()) == 0:
    window = tk.Tk()
    window.title('第一次使用')
    frame = tk.Frame(window)
    frame.grid(padx=8, pady=8)

    title = tk.Label(frame, text='第一次使用請先輸入帳號密碼', font=font_title, pady=5)
    title.grid(row=0, column=0, columnspan=2, sticky='w')

    account_label = tk.Label(frame, text='帳號：', font=font_content, pady=5)
    password_label = tk.Label(frame, text='密碼：', font=font_content, pady=5)
    account_label.grid(row=1, column=0)
    password_label.grid(row=2, column=0)

    acnt_var = tk.StringVar()
    account = tk.Entry(frame, textvariable=acnt_var, font=font_content)
    account.grid(row=1, column=1)
    pwd_var = tk.StringVar()
    password = tk.Entry(frame, textvariable=pwd_var, show='*', font=font_content)
    password.grid(row=2, column=1)
    
    confirm = tk.Button(frame, text='確認', command=confirmed, font=font_content, padx=15, pady=3)
    confirm.grid(row=3, column=0, columnspan=2)

    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()

window = tk.Tk()
window.title('你的課表')
window.attributes('-topmost', True)
window.resizable(False, False)

# label = tk.Label(window, text='開始爬成績...\n', font=font_title, justify='left')
# label.grid(row=0, column=0, padx=5, pady=5)


canvas = tk.Canvas(window)
canvas.grid(sticky='news')

frame = tk.Frame(canvas)

weeklist = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
timelist = ['06:00','07:00','08:00','09:00','10:10','11:10','12:20','13:20','14:20','15:30','16:30','17:30','18:30','19:30','20:30','21:30']

for j in range(len(weeklist)):
    week = tk.Label(frame, text=weeklist[j], font=font)
    week.grid(row=0, column=j+1, padx=5, pady=5)


for i in range(len(timelist)):
    time = tk.Label(frame, text=timelist[i], font=font)
    time.grid(row=i+1, column=0, padx=5, pady=5, sticky='n')

for j in range(len(weeklist)+1):
    ttk.Separator(frame, orient='vertical').grid(row=0, column=j, rowspan=len(timelist)+1, sticky='wns')

for i in range(len(timelist)):
    ttk.Separator(frame, orient='horizontal').grid(row=i, column=0, columnspan=len(weeklist)+1, sticky='sew')

btn_refresh = tk.Button(frame, text='Update', command=task)
btn_refresh.grid(row=0, column=0, padx=1, pady=1)

Curriculums: List[tk.Frame] = []

# threading.Thread(target=readCurriculum).start()
readCurriculum()

# scrollbar=tk.Scrollbar(window, orient="vertical", width=15, command=canvas.yview)
# xscrollbar=tk.Scrollbar(window, orient="horizontal", width=15, command=canvas.xview)
# canvas.configure(yscrollcommand=scrollbar.set) 
# canvas.configure(xscrollcommand=xscrollbar.set) 
# scrollbar.grid(row=0, column=1, sticky='ns')
# xscrollbar.grid(row=1, column=0, sticky='ew')
# canvas.create_window((0, 0), window=frame, anchor='nw')

# canvas.config(width=600, height=600)
# canvas.config(scrollregion=canvas.bbox("all"))
frame.grid()

window.mainloop()