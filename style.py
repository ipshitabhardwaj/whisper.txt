# style.py

# 🧶 Color Palette (soft, comforting)
BG_COLOR = "#f8f4f0"        # main background (beige-pink)
ACCENT_COLOR = "#e8e0dc"    # button background
TEXT_COLOR = "#5c4b51"      # warm gray-brown
BUTTON_HOVER = "#d8d0cb"    # hover shade

# 📚 Fonts
TITLE_FONT = ("Georgia", 24, "italic")
BODY_FONT = ("Georgia", 12)
WHISPER_FONT = ("Georgia", 12, "italic")
TEXTBOX_FONT = ("Georgia", 11)

# 🎀 Button Style (dictionary for easy unpacking)
button_style = {
    "font": BODY_FONT,
    "bg": ACCENT_COLOR,
    "fg": TEXT_COLOR,
    "activebackground": BUTTON_HOVER,
    "relief": "flat",
    "width": 20,
    "padx": 10,
    "pady": 8
}
