import tkinter as tk
import tkinter.font as tkfont

from PIL import Image, ImageTk

INSTRUCTIONS = ["", "BOX", "FUEL", "SLOW", "GAZZZ"]


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


class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.input_buffer = ""

        self.grid(sticky="nsew")

        screen_height = self.winfo_screenheight()
        screen_width = self.winfo_screenwidth()

        logo_height = int(screen_height / 3)
        logo = Image.open("logo.png")
        logo.thumbnail((screen_width, logo_height))
        logo_tk = ImageTk.PhotoImage(logo)
        self.logo = tk.Label(self, image=logo_tk, bg="white")
        # Keep a reference to avoid garbage collection
        self.logo.image = logo_tk

        self.instruction = FontAdjustingLabel(
            logo_height, self, bg="black", fg="dark violet"
        )

        timing_height = screen_height - logo_height
        self.timing = FontAdjustingLabel(
            timing_height, self, text="00.0", bg="black", fg="yellow"
        )

        self.logo.grid(row=0, column=0, sticky="nw")
        self.instruction.grid(row=0, column=1, sticky="nsew")
        self.timing.grid(row=1, columnspan=2, sticky="nsew")

        self.columnconfigure(1, weight=1)

        self.bind("<Key>", self.cb_key)
        self.focus_set()

        self.flash()

    def cb_key(self, event):
        if not self.input_buffer and event.char in "*/-" or event.char.isdigit():
            self.input_buffer += event.char
        elif self.input_buffer and event.keysym in ("Return", "KP_Enter"):
            self.parse_command()

    def parse_command(self):
        command = self.input_buffer
        self.input_buffer = ""
        if command.startswith("*"):
            try:
                index = int(command[1:])
                self.instruction["text"] = INSTRUCTIONS[index]
            except (ValueError, IndexError):
                pass
        elif command.startswith("-"):
            if len(command[1:]) == 1:
                self.instruction["text"] = "T " + command
        elif command.startswith("/"):
            if 1 <= len(command[1:]) <= 2:
                self.instruction["text"] = "P " + command[1:]
        elif len(command) == 3:
            self.timing["text"] = ".".join((command[:2], command[2:]))

    def flash(self) -> None:
        bg = self.instruction["bg"]
        fg = self.instruction["fg"]
        if self.instruction["text"] or bg != "black":
            self.instruction.configure(bg=fg, fg=bg)
        self.after(500, self.flash)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("{}x{}".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.attributes("-fullscreen", True)
    root.columnconfigure(0, weight=1)
    board = App(root)
    board.mainloop()
