import tkinter as tk
import tkinter.font as tkfont

from PIL import Image, ImageTk


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
            logo_height, self, text="BOX", bg="black", fg="dark violet"
        )

        timing_height = screen_height - logo_height
        self.timing = FontAdjustingLabel(
            timing_height, self, text="00.0", bg="black", fg="yellow"
        )

        self.logo.grid(row=0, column=0, sticky="nw")
        self.instruction.grid(row=0, column=1, sticky="nsew")
        self.timing.grid(row=1, columnspan=2, sticky="nsew")

        self.columnconfigure(1, weight=1)

        self.flash()

    def flash(self) -> None:
        bg = self.instruction["bg"]
        fg = self.instruction["fg"]
        if self.instruction["text"] or bg != "black":
            self.instruction.configure(bg=fg, fg=bg)
        self.after(500, self.flash)


if __name__ == "__main__":
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.attributes("-fullscreen", 1)
    board = App(root)
    board.mainloop()
