import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

# 🎀 Import styles
from style import (
    BG_COLOR, ACCENT_COLOR, TEXT_COLOR, BUTTON_HOVER,
    TITLE_FONT, BODY_FONT, WHISPER_FONT, TEXTBOX_FONT,
    button_style
)

FEELINGS_FILE = 'feelings.txt'
BURNED_FILE = 'burned_log.txt'

# 🌸 Save a full whisper
def leave_feeling(from_name, to_name, message):
    tag_from = f"from: {from_name.strip()}" if from_name else "from: anonymous"
    tag_to = f"to: {to_name.strip()}" if to_name else "to: unnamed"
    full_entry = f"[{tag_from}] [{tag_to}] {message.strip()}"
    with open(FEELINGS_FILE, 'a', encoding='utf-8') as f:
        f.write(full_entry + "\n")

# 💬 Load a random unburned whisper
def get_random_whisper():
    if not os.path.exists(FEELINGS_FILE):
        return None
    with open(FEELINGS_FILE, 'r', encoding='utf-8') as f:
        whispers = [line.strip() for line in f if line.strip()]

    if os.path.exists(BURNED_FILE):
        with open(BURNED_FILE, 'r', encoding='utf-8') as b:
            burned = set(line.strip() for line in b if line.strip())
        whispers = [w for w in whispers if w not in burned]

    return random.choice(whispers) if whispers else None

def symbolically_burn(whisper):
    with open(BURNED_FILE, 'a', encoding='utf-8') as f:
        f.write(whisper.strip() + '\n')

# 🌠 Placeholder root
root = None

# 🌙 Splash screen
def show_splash():
    splash = tk.Tk()
    splash.title("whisper.txt")
    splash.geometry("360x240")
    splash.configure(bg=BG_COLOR)
    splash.overrideredirect(True)

    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    x = (screen_width - 360) // 2
    y = (screen_height - 240) // 2
    splash.geometry(f"+{x}+{y}")

    msg = tk.Label(
        splash,
        text="a quiet place for the words you never said.",
        font=("Georgia", 13, "italic"),
        bg=BG_COLOR,
        fg=TEXT_COLOR,
        wraplength=320,
        justify="center"
    )
    msg.pack(expand=True)

    splash.after(2500, lambda: (splash.destroy(), show_main_window()))

# 🌷 Main app window
def show_main_window():
    global root
    root = tk.Tk()
    root.title("whisper.txt")
    root.geometry("400x500")
    root.resizable(False, False)

    bg_image = Image.open("assets/bg.png").resize((400, 500))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def show_about(event):
        messagebox.showinfo("about 🌙", "every feeling here is safe, anonymous, and seen.")

    candle_img = Image.open("assets/candle.png").resize((40, 40))
    candle_photo = ImageTk.PhotoImage(candle_img)
    candle = tk.Label(root, image=candle_photo, bg="white", bd=0, cursor="hand2")
    candle.place(x=340, y=430)
    candle.bind("<Enter>", lambda e: candle.config(bg="#ffe"))
    candle.bind("<Leave>", lambda e: candle.config(bg="white"))
    candle.bind("<Button-1>", show_about)

    title = tk.Label(root, text="whisper.txt", font=TITLE_FONT, bg=BG_COLOR, fg=TEXT_COLOR)
    title.place(relx=0.5, y=50, anchor="center")

    def make_button(text, y, command):
        tk.Button(root, text=text, command=command, **button_style).place(relx=0.5, y=y, anchor="center")

    # 💌 leave whisper
    def open_leave_screen():
        leave_window = tk.Toplevel(root)
        leave_window.title("leave a whisper")
        leave_window.geometry("350x350")
        leave_window.configure(bg=BG_COLOR)

        tk.Label(leave_window, text="from (name or leave blank):", bg=BG_COLOR, fg=TEXT_COLOR, font=BODY_FONT).pack(pady=(10, 0))
        from_entry = tk.Entry(leave_window, font=TEXTBOX_FONT)
        from_entry.pack(pady=(0, 10))

        tk.Label(leave_window, text="to (a name, a feeling, anyone):", bg=BG_COLOR, fg=TEXT_COLOR, font=BODY_FONT).pack()
        to_entry = tk.Entry(leave_window, font=TEXTBOX_FONT)
        to_entry.pack(pady=(0, 10))

        tk.Label(leave_window, text="your whisper:", bg=BG_COLOR, fg=TEXT_COLOR, font=BODY_FONT).pack()
        message_box = tk.Text(leave_window, height=6, wrap="word", bg="#fef6f3", fg=TEXT_COLOR, font=TEXTBOX_FONT)
        message_box.insert("1.0", "say the thing you couldn't say...")
        message_box.bind("<FocusIn>", lambda e: message_box.delete("1.0", "end") if message_box.get("1.0", "end-1c").startswith("say the") else None)
        message_box.pack(padx=20, pady=10)

        def submit():
            from_name = from_entry.get()
            to_name = to_entry.get()
            message = message_box.get("1.0", "end-1c")
            if not message.strip() or message.strip().startswith("say the thing"):
                messagebox.showinfo("oops", "your whisper is empty 😔")
                return
            leave_feeling(from_name, to_name, message)
            messagebox.showinfo("💌", "your whisper has been tucked safely into the archive.")
            leave_window.destroy()

        tk.Button(leave_window, text="leave it here", command=submit, **button_style).pack(pady=10)

    # ✨ receive whisper
    def open_receive_screen():
        whisper = get_random_whisper()
        if not whisper:
            messagebox.showinfo("💭", "the archive is quiet right now.")
            return

        parts = whisper.split("]")
        msg_only = whisper
        if len(parts) >= 3:
            msg_only = "]".join(parts[2:]).strip()

        recv_window = tk.Toplevel(root)
        recv_window.title("a whisper for you")
        recv_window.geometry("350x250")
        recv_window.configure(bg=BG_COLOR)

        msg_label = tk.Label(recv_window, text="", wraplength=300,
                             font=WHISPER_FONT, bg=BG_COLOR, fg=TEXT_COLOR, justify="center")
        msg_label.pack(pady=30, padx=20)

        def fade_in(text, index=0):
            if index <= len(text):
                msg_label.config(text=text[:index])
                msg_label.after(20, lambda: fade_in(text, index + 1))

        fade_in(f"“{msg_only}”")

        def burn_it():
            symbolically_burn(whisper)
            messagebox.showinfo("🕯️", "this whisper has been gently released.")
            recv_window.destroy()

        tk.Button(recv_window, text="burn this whisper", command=burn_it, **button_style).pack()

    def quick_burn():
        whisper = get_random_whisper()
        if not whisper:
            messagebox.showinfo("💭", "there’s nothing left to burn.")
            return
        symbolically_burn(whisper)
        messagebox.showinfo("🕯️", "a whisper was burned, softly and silently.")

    make_button("leave a whisper", 150, open_leave_screen)
    make_button("receive a whisper", 200, open_receive_screen)
    make_button("burn a whisper", 250, quick_burn)

    # 🎀 Archive Stats
    total = 0
    burned = 0
    if os.path.exists(FEELINGS_FILE):
        with open(FEELINGS_FILE, 'r', encoding='utf-8') as f:
            total = len([line for line in f if line.strip()])
    if os.path.exists(BURNED_FILE):
        with open(BURNED_FILE, 'r', encoding='utf-8') as f:
            burned = len([line for line in f if line.strip()])

    tk.Label(root, text=f"🌸 whispers: {total}  |  🕯️ burned: {burned}",
             font=("Georgia", 9), bg=BG_COLOR, fg=TEXT_COLOR).place(relx=0.5, rely=0.95, anchor="center")

    root.bg_photo = bg_photo
    root.candle_photo = candle_photo
    root.mainloop()

# 🚀 Launch with splash
if __name__ == "__main__":
    show_splash()
