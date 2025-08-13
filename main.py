from Xlib import X, display
import tkinter as tk
import time

disp = display.Display()
typed_chars = []
PASSWORD = None

def grab_keyboard_and_pointer_on_tk():
    wid = root.winfo_id()
    win = disp.create_resource_object('window', wid)
    # Tastatura
    win.grab_keyboard(True, X.GrabModeAsync, X.GrabModeAsync, X.CurrentTime)
    # Miš
    win.grab_pointer(True, X.ButtonPressMask | X.ButtonReleaseMask | X.PointerMotionMask, X.GrabModeAsync, X.GrabModeAsync, X.NONE, X.NONE, X.CurrentTime)
    disp.flush()

def ungrab_keyboard_and_pointer():
    disp.ungrab_keyboard(X.CurrentTime)
    disp.ungrab_pointer(X.CurrentTime)
    disp.flush()

def handle_key_event(event):
    keysym = disp.keycode_to_keysym(event.detail, 0)
    if keysym:
        char = chr(keysym) if 32 <= keysym < 127 else ""
        if char:
            typed_chars.append(char)
            current_input = "".join(typed_chars[-len(PASSWORD):])
            label.config(text=current_input)
            print(f"Key pressed: {char}")

            if current_input == PASSWORD:
                ungrab_keyboard_and_pointer()
                reset_to_password_entry()

def start_lock():
    typed_chars.clear()
    countdown(5)
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.config(cursor="none")
    root.attributes("-alpha", 0)
    grab_keyboard_and_pointer_on_tk()
    root.after(20, x_event_loop)

def countdown(seconds):
    for i in range(seconds, -1, -1):
        alpha = i / seconds
        root.attributes("-alpha", alpha)
        root.update()
        label.config(text=f"Počinje za {i}...")
        time.sleep(1)
    label.config(text="")

def on_entry_key(event):
    global PASSWORD
    if event.keysym == "Return":
        PASSWORD = entry.get()
        entry.pack_forget()
        label.config(text="Priprema...")
        root.update()
        start_lock()

def reset_to_password_entry():
    root.attributes("-fullscreen", False)
    root.attributes("-topmost", False)
    root.config(cursor="")
    root.attributes("-alpha", 1.0)
    label.config(text="Enter password:")
    entry.delete(0, tk.END)
    entry.pack()
    entry.focus_set()

def x_event_loop():
    while disp.pending_events():
        e = disp.next_event()
        if e.type == X.KeyPress:
            handle_key_event(e)
    root.after(20, x_event_loop)

root = tk.Tk()
root.title("Set password")
root.geometry("800x200")
root.configure(bg="black")

label = tk.Label(root, text="Enter password", font=("Consolas", 40), fg="lime", bg="black")
label.pack(pady=20)

entry = tk.Entry(root, font=("Consolas", 40), fg="lime", bg="black", insertbackground="lime")
entry.pack()
entry.focus_set()
entry.bind("<Key>", on_entry_key)

root.mainloop()
