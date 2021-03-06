#!/usr/bin/env python3.7
import random
import subprocess
import tkinter as tk
import tkinter.font as tkfont
from pathlib import Path

from PIL import Image, ImageTk

INSTRUCTIONS = ["", "BOX", "S&G", "LIGHT", "✌"]  # ᗡ⚟
INITIAL_TOP = "#44"


def demo_command():
    while True:
        yield str(random.randint(400, 599))
        yield "/{}".format(random.randint(1, 30))
        yield str(random.randrange(1, len(INSTRUCTIONS)))
        yield "-{}".format(random.randint(1, 9))


class FontAdjustingLabel(tk.Label):
    def __init__(self, ht, master, **kwargs):
        super().__init__(master=master, **kwargs)
        self.font = tkfont.Font(
            family="Liberation Sans", weight="bold", size=-(ht // 2)
        )
        self.configure(font=self.font)
        while self.winfo_reqheight() < ht:
            self.font["size"] -= 1
            self.update_idletasks()
        self.optimal_font_size = self.font["size"]

    def reset_font_size(self):
        self.font["size"] = self.optimal_font_size
        self.update_idletasks()


class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.input_buffer = ""
        self.demo_generator = demo_command()

        self.grid(sticky="nsew")

        screen_height = self.winfo_screenheight()
        screen_width = self.winfo_screenwidth()

        logo_height = screen_height // 4
        logo = Image.open(Path(__file__).parent / "logo.png")
        logo.thumbnail((screen_width, logo_height))
        logo_tk = ImageTk.PhotoImage(logo)
        self.logo = tk.Label(self, image=logo_tk, bg="white")
        # Keep a reference to avoid garbage collection
        self.logo.image = logo_tk

        self.topline = FontAdjustingLabel(
            logo_height, self, text=INITIAL_TOP, bg="dark violet", fg="black"
        )

        bottomline_height = screen_height - logo_height
        self.bottomline_text = tk.StringVar()
        self.bottomline_text.set(INSTRUCTIONS[-1])
        self.bottomline_text.trace("w", self.cb_bottomline_text)
        self.bottomline = FontAdjustingLabel(
            bottomline_height,
            self,
            textvariable=self.bottomline_text,
            bg="black",
            fg="yellow",
        )

        self.logo.grid(row=0, column=0, sticky="nw")
        self.topline.grid(row=0, column=1, sticky="nsew")
        self.bottomline.grid(row=1, columnspan=2, sticky="nsew")
        self.grid_rowconfigure(1, minsize=bottomline_height)

        self.columnconfigure(1, weight=1)

        self.bind_all("<Key>", self.cb_key)

        self.flash()

    def cb_bottomline_text(self, *args):
        self.bottomline.reset_font_size()
        width = self.bottomline.winfo_width()
        pady = 0
        while self.bottomline.winfo_reqwidth() > width:
            self.bottomline.font["size"] += 4
            pady += 2
            self.bottomline.update_idletasks()
        self.bottomline.grid(row=1, columnspan=2, ipady=pady, sticky="nsew")

    def cb_key(self, event):
        if not self.input_buffer and event.char in "*/-" or event.char.isdigit():
            self.input_buffer += event.char
        elif self.input_buffer and event.keysym in ("Return", "KP_Enter"):
            self.parse_command()

    def parse_command(self):
        command = self.input_buffer
        self.input_buffer = ""
        if command == "*9998":
            subprocess.run(["sudo", "-n", "reboot"])
        elif command == "*9999":
            subprocess.run(["sudo", "-n", "poweroff"])
        elif command == "*8888":
            self.unbind_all("<Key>")
            self.demo()
        elif command == "*0":
            self.topline["text"] = INITIAL_TOP
        elif command.startswith("-"):
            if len(command[1:]) == 1:
                self.topline["text"] = "T " + command
        elif command.startswith("/"):
            if 1 <= len(command[1:]) <= 2:
                self.topline["text"] = "P " + command[1:]
        elif len(command) == 1:
            try:
                index = int(command)
                self.bottomline_text.set(INSTRUCTIONS[index])
            except (ValueError, IndexError):
                pass
        elif len(command) == 3:
            self.bottomline_text.set(".".join((command[:2], command[2:])))

    def flash(self) -> None:
        bg = self.bottomline["bg"]
        fg = self.bottomline["fg"]
        if self.bottomline_text.get() in INSTRUCTIONS[1:-1] or bg != "black":
            self.bottomline.configure(bg=fg, fg=bg)
        self.after(500, self.flash)

    def demo(self):
        self.input_buffer = next(self.demo_generator)
        self.parse_command()
        self.after(3000, self.demo)


if __name__ == "__main__":
    root = tk.Tk()
    scrwidth = root.winfo_screenwidth()
    scrheight = root.winfo_screenheight()
    root.geometry("{}x{}".format(scrwidth, scrheight))
    root.attributes("-fullscreen", True)
    root.columnconfigure(0, weight=1)
    root.bind_all("<Quadruple-BackSpace>", lambda e: root.destroy())
    wait_label = tk.Label(text="\uf017", font=("FontAwesome", scrheight // 5))
    wait_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    board = App(root)
    wait_label.destroy()
    board.mainloop()
