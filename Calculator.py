import tkinter as tk
from tkinter import ttk, messagebox
import math
import sv_ttk
import ctypes as ct

root = tk.Tk()

root.title("Calculator")
root.iconbitmap("C:/Users/thoma/OneDrive/Afbeeldingen/favicon.ico")
root.geometry("325x500")
root.minsize(width=100, height=250)
sv_ttk.set_theme("dark")

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

frame = ttk.Frame(root)
frame.grid(row=0, column=0, sticky="nsew")

for i in range(8):
    frame.rowconfigure(i, weight=1, uniform="row")

for i in range(4):
    frame.columnconfigure(i, weight=1, uniform="col")

zero = False
c_text = "0"
sub = False
slic = 0
label = ttk.Label(frame, text=c_text, anchor=tk.W, font=("arial",30), foreground="white")
label.grid(row=0, column=0, columnspan=4, sticky="ew")

def dark_title_bar(window):
    window.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))

dark_title_bar(root)

def resize_label_text(event):

    max_size = int(event.width / 10)

    if max_size > 50:
        max_size = 50
    
    new_size = max(20, max_size)
    label.config(font=("Arial", new_size))

def button(button):

    global zero
    global sub
    global slic
    num = False
    c_text = label.cget("text")

    for i in range(0,10):
        if button == str(i):
            num = True
    
    if sub and num:
        subs = {
            "0": "\u2070", "1": "\u00b9", "2": "\u00b2",
            "3": "\u00b3", "4": "\u2074", "5": "\u2075",
            "6": "\u2076", "7": "\u2077", "8": "\u2078",
            "9": "\u2079"
            }
        button = subs.get(button, "")

        if button == "\u207B":
            c_text = slicing(c_text, str(button))
            label.config(text=c_text)
            sub = True
        elif button:
            c_text = slicing(c_text, str(button))
            label.config(text=c_text)
            sub = False
        else:
            sub = True
        num = False
        
    else:
        
        if button == "C":
            c_text = "0"
            label.config(text=c_text)
            slic = 0
            
        elif button == "⌫":
            c_text_point = c_text[:len(c_text)-slic]
            c_text = c_text_point[:-1] + c_text[len(c_text)-slic:]
            
            if c_text == "":
                c_text = "0"

            label.config(text=c_text)
            
        elif button == "x10ⁿ":
            button = "x10"
            sub = True
            c_text = slicing(c_text, str(button))
            label.config(text=c_text)

        elif button == "xⁿ":
            button = ""
            sub = True
            c_text = slicing(c_text, str(button))
            label.config(text=c_text)

        elif button == "x²":
            button = "²"
            c_text = slicing(c_text, str(button))
            label.config(text=c_text)
            
        elif button == "\u221A":
            button = "\u221A()"
            if c_text == "0":
                c_text = ""
                
            c_text = slicing(c_text, str(button))
            label.config(text=c_text)

            slic += 1
            
        elif button == "=":
            fault = False
            c_text = c_text.replace("x", "*")
            c_text = c_text.replace("%", "*0.01")
            c_text = c_text.replace(",", ".")
            c_text = c_text.replace("π", str(math.pi))

            c_text = power(c_text)
            
            if "\u221A(" in c_text:
                c_text, fault = square(c_text)

            if not fault:
                calculation(c_text)
            
        elif button == "0":
            zero = True
            if c_text == "0":
                c_text = ""
                
            c_text = slicing(c_text, str(button))
            label.config(text=c_text)
        else:
            if c_text == "0" and zero == False:
                c_text = ""
            zero = False
            c_text = slicing(c_text, str(button))
            label.config(text=c_text)

def square(c_text):

    i = c_text.count("\u221A(")

    try:
        for j in range(i):
            square_start = c_text.find("\u221A(")
            square_end = c_text.find(")", square_start)
            square = c_text[square_start + 2: square_end]
            c_text = c_text[:square_start] + str(math.sqrt(float(square))) + c_text[square_end + 1:]

        fault = False
        return c_text, fault
    
    except ValueError:
        messagebox.showwarning("Wiskunde fout", "Negatief getal onder de vierkantswortel")
        
        fault = True
        return c_text, fault
    
def power(c_text):
    subs = {
            "0": "\u2070", "1": "\u00b9", "2": "\u00b2",
            "3": "\u00b3", "4": "\u2074", "5": "\u2075",
            "6": "\u2076", "7": "\u2077", "8": "\u2078",
            "9": "\u2079"
            }
    
    for digit, sups in subs.items():
        while sups in c_text:
            
            for j in range(10):
            
                if -1 != c_text.find(subs.get(str(j))):
                    pow_end = c_text.find(subs.get(str(j)))
                    num = ""
                    
                    for k in range(pow_end):
                        if c_text[k].isdigit() or c_text[k] == ".":
                            num += c_text[k]
                        else:
                            num = ""

                    num = num.replace(",", ".")
                    pow_start = pow_end - len(num)
                    power = c_text[pow_start: pow_end]
                    c_text = c_text[:pow_start] + str(pow(float(num), j)) + c_text[pow_end + 1:]
                    
    return c_text
                
            
def calculation(c_input):

    global slic

    try:
        c_input = eval(c_input)
        c_input = round(float(c_input), 8)
        c_input = str(c_input).replace(".", ",")
        
    except SyntaxError:
        messagebox.showwarning("Syntax fout", "Syntax fout geregistreerd")
        
    except ZeroDivisionError:
        messagebox.showwarning("Wiskunde fout", "Je kan niet delen door nul")
        
    for i in range(len(str(c_input))):
        if "," in str(c_input):
            if str(c_input)[len(str(c_input)) - 1] == "0":
                c_input = str(c_input)[:-1]
            if str(c_input)[len(str(c_input)) - 1] == ",":
                c_input = str(c_input)[:-1]
            
    label.config(text=str(c_input))
    slic = 0

def slicing(c_text, button):
    global slic

    slic = min(slic, len(c_text))
    c_end = len(c_text) - slic
    c_output = c_text[:c_end] + button + c_text[c_end:]

    return c_output

def move_slic(option):
    global slic
    c_text = label.cget("text")

    if option == "left":
        if slic < len(c_text):
            slic += 1
    elif option == "right" and slic > 0:
        slic -= 1

root.bind("<Configure>", resize_label_text)
root.bind("<Left>", lambda e: move_slic("left"))
root.bind("<Right>", lambda e: move_slic("right"))
root.bind("1", lambda e: button("1"))
root.bind("2", lambda e: button("2"))
root.bind("3", lambda e: button("3"))
root.bind("4", lambda e: button("4"))
root.bind("5", lambda e: button("5"))
root.bind("6", lambda e: button("6"))
root.bind("7", lambda e: button("7"))
root.bind("8", lambda e: button("8"))
root.bind("9", lambda e: button("9"))
root.bind("0", lambda e: button("0"))
root.bind("*", lambda e: button("x"))
root.bind("x", lambda e: button("x"))
root.bind("/", lambda e: button("/"))
root.bind(":", lambda e: button("/"))
root.bind("-", lambda e: button("-"))
root.bind("(", lambda e: button("("))
root.bind(")", lambda e: button(")"))
root.bind("%", lambda e: button("%"))
root.bind(",", lambda e: button(","))
root.bind(".", lambda e: button(","))
root.bind("=", lambda e: button("="))
root.bind("c", lambda e: button("C"))
root.bind("C", lambda e: button("C"))
root.bind("<BackSpace>", lambda e: button("⌫"))
root.bind("<Return>", lambda e: button("="))

buttons = [
    ("0", 7, 0), ("1", 6, 0), ("2", 6, 1), ("3", 6, 2),
    ("4", 5, 0), ("5", 5, 1), ("6", 5, 2), ("7", 4, 0),
    ("8", 4, 1), ("9", 4, 2), ("+", 3, 3), ("-", 4, 3),
    ("x", 5, 3), ("/", 6, 3), ("=", 7, 2, 2), (",", 7, 1),
    ("x²", 3, 1), (("\u221A"), 3, 0), ("C", 1, 2, 2), ("(", 2, 0),
    (")", 2, 1), ("π", 2, 2), ("x10ⁿ", 1, 0), ("%", 1, 1),
    ("xⁿ", 3, 2), ("⌫", 2, 3)
    ]

for btn in buttons:
    text, row, col = btn[:3]
    colspan = btn[3] if len(btn) > 3 else 1
    ttk.Button(frame, text=text, command=lambda t=text: button(t)).grid(row=row, column=col, columnspan=colspan, sticky="nsew")

root.mainloop()






