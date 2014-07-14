# -*- coding:utf-8 -*-

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import calculate_class as cc
import os

def calculate(*args):
    mode = int(mode_entry.get())
    deep = int(deep_entry.get())
    degree = int(degree_entry.get())
    value = int(value_entry.get())
    price = int(price_entry.get())
    ratio = int(ratio_entry.get())

    if mode == "" or deep == "" or degree == "" or value == "" or price == "" or ratio == "":
        messagebox.showinfo(message='不要留空')
        return
    if 0 <= mode <= 5:
        messagebox.showinfo(message='注意：计算完成会在2秒后打开浏览器')
        cc.start(deep, degree, value, price, ratio, mode)
    else:
        pass


def delete(*args):
    target_files = ['result.txt', '0.html']
    for i in target_files:
        if os.path.isfile(i):
            os.remove(i)
    messagebox.showinfo(message='清除成功')

def center_window(w=300, h=200):
    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

root = Tk()
root.title("代理分销模型")
center_window(800, 300)

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

# 模式
mode = IntVar()
ttk.Label(mainframe, text="模式").grid(column=1, row=1, sticky=E)
mode_entry = ttk.Entry(mainframe, width=7, textvariable=mode)
mode_entry.grid(column=2, row=1, sticky=(W, E))
# 深度
deep = IntVar()
ttk.Label(mainframe, text="经销商深度").grid(column=1, row=2, sticky=E)
deep_entry = ttk.Entry(mainframe, width=7, textvariable=deep)
deep_entry.grid(column=2, row=2, sticky=(W, E))
# 度
degree = IntVar()
ttk.Label(mainframe, text="最大子经销商数").grid(column=1, row=3, sticky=E)
degree_entry = ttk.Entry(mainframe, width=7, textvariable=degree)
degree_entry.grid(column=2, row=3, sticky=(W, E))
# 节点值
value = IntVar()
ttk.Label(mainframe, text="最大卖出数量").grid(column=1, row=4, sticky=E)
value_entry = ttk.Entry(mainframe, width=7, textvariable=value)
value_entry.grid(column=2, row=4, sticky=(W, E))
# 商品价格
price = IntVar()
ttk.Label(mainframe, text="商品价格").grid(column=1, row=5, sticky=E)
price_entry = ttk.Entry(mainframe, width=7, textvariable=price)
price_entry.grid(column=2, row=5, sticky=(W, E))
# 商品利润率
ratio = IntVar()
ttk.Label(mainframe, text="单价商品利润率").grid(column=1, row=6, sticky=E)
ratio_entry = ttk.Entry(mainframe, width=7, textvariable=ratio)
ratio_entry.grid(column=2, row=6, sticky=(W, E))
ttk.Label(mainframe, text="%（输入整数）").grid(column=3, row=6, sticky=W)


ttk.Button(mainframe, text="开始计算", command=calculate).grid(column=3, row=3, sticky=W)
ttk.Button(mainframe, text="清除文件", command=delete).grid(column=3, row=4, sticky=W)

ttk.Label(mainframe, text="(4，5号模式建议先清除文件)").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="模式的值介绍：").grid(column=4, row=1, sticky=W)
ttk.Label(mainframe, text="0 表示不处理度和卖出数量").grid(column=4, row=2, sticky=W)
ttk.Label(mainframe, text="1 表示随机度，不随机卖出数量").grid(column=4, row=3, sticky=W)
ttk.Label(mainframe, text="2 表示随机卖出数量，不随机度").grid(column=4, row=4, sticky=W)
ttk.Label(mainframe, text="3 表示度和卖出数量都随机").grid(column=4, row=5, sticky=W)
ttk.Label(mainframe, text="4 表示不处理度，穷举卖出数量").grid(column=4, row=6, sticky=W)
ttk.Label(mainframe, text="5 表示不处理度，穷举卖出数量，并对每一个卖出数量穷举利润，利润步长为10").grid(column=4, row=7, sticky=W)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)
mode_entry.focus()
root.bind('<Return>', calculate)

root.mainloop();