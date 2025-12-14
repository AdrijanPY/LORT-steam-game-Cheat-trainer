import pymem
import pymem.process
import tkinter as tk
from tkinter import ttk

# =========================
# KONFIG
# =========================

PROCESS_NAME = "LortGame-Win64-Shipping.exe"
BASE_OFFSET = 0x09489720

MONEY_OFFSETS = [0x30, 0x2D8, 0x210, 0x8, 0x98, 0x2B8, 0x350]
RUNE_OFFSETS  = [0x1E8, 0x190, 0x8, 0x30, 0x108]

BG = "#0f1115"
CARD = "#161a22"
ACCENT = "#f5c542"
TEXT = "#eaeaea"
MUTED = "#8a8f98"
SUCCESS = "#4caf50"
ERROR = "#e05f5f"

# =========================
# MEMORY
# =========================

def get_process():
    try:
        return pymem.Pymem(PROCESS_NAME)
    except:
        return None

def resolve_pointer(pm, offsets):
    module = pymem.process.module_from_name(pm.process_handle, PROCESS_NAME)
    addr = module.lpBaseOfDll + BASE_OFFSET
    for off in offsets:
        addr = pm.read_longlong(addr) + off
    return addr

def set_value(offsets, value):
    pm = get_process()
    if not pm:
        raise Exception("Game not running")
    pm.write_int(resolve_pointer(pm, offsets), value)

def read_value(offsets):
    pm = get_process()
    if not pm:
        raise Exception("Game not running")
    return pm.read_int(resolve_pointer(pm, offsets))

# =========================
# SPLASH / BOOT (UNVERÄNDERT)
# =========================

class Splash(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.overrideredirect(True)
        self.geometry("420x220+600+300")
        self.configure(bg=BG)

        tk.Label(
            self,
            text="ACheese",
            fg=ACCENT,
            bg=BG,
            font=("Segoe UI", 26, "bold")
        ).pack(pady=(50, 5))

        tk.Label(
            self,
            text="initializing trainer...",
            fg=MUTED,
            bg=BG,
            font=("Segoe UI", 11)
        ).pack()

        self.progress = ttk.Progressbar(self, mode="indeterminate")
        self.progress.pack(fill="x", padx=60, pady=30)
        self.progress.start(10)

        self.attributes("-alpha", 0.0)
        self.fade_in()

    def fade_in(self):
        a = self.attributes("-alpha")
        if a < 1:
            self.attributes("-alpha", a + 0.05)
            self.after(30, self.fade_in)

# =========================
# MAIN GUI
# =========================

class ACheeseGUI:
    def __init__(self, root):
        self.root = root
        root.title("ACheese")
        root.geometry("420x500")
        root.configure(bg=BG)
        root.resizable(False, False)
        root.attributes("-alpha", 0.0)

        self.fade_in()

        self.card = tk.Frame(root, bg=CARD)
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=360, height=440)

        # Header
        tk.Label(
            self.card,
            text="ACheese Trainer",
            bg=CARD,
            fg=TEXT,
            font=("Segoe UI", 18, "bold")
        ).pack(pady=(15, 5))

        self.status = tk.Label(
            self.card,
            text="● Not connected",
            fg=ERROR,
            bg=CARD,
            font=("Segoe UI", 10)
        )
        self.status.pack(pady=(0, 15))

        # MONEY
        self.build_section("Money", self.set_money)
        self.money_label = tk.Label(self.card, text="Current Money: -", fg=MUTED, bg=CARD)
        self.money_label.pack(pady=(5, 15))

        # RUNE JUICE
        self.build_section("Rune Juice", self.set_rune)
        self.rune_label = tk.Label(self.card, text="Current Rune Juice: -", fg=MUTED, bg=CARD)
        self.rune_label.pack(pady=5)

        self.update_status()

    # =========================
    # UI HELPERS
    # =========================

    def build_section(self, title, command):
        tk.Label(
            self.card, text=title,
            fg=MUTED, bg=CARD, font=("Segoe UI", 10)
        ).pack(anchor="w", padx=30)

        entry = tk.Entry(
            self.card,
            font=("Segoe UI", 13),
            bg=BG,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat"
        )
        entry.pack(fill="x", padx=30, pady=(5, 8), ipady=6)

        btn = tk.Button(
            self.card,
            text=f"SET {title.upper()}",
            bg=ACCENT,
            fg="black",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            command=lambda e=entry: command(e)
        )
        btn.pack(fill="x", padx=30, ipady=6, pady=(0, 10))

    # =========================
    # ANIMATION
    # =========================

    def fade_in(self):
        a = self.root.attributes("-alpha")
        if a < 1:
            self.root.attributes("-alpha", a + 0.05)
            self.root.after(20, self.fade_in)

    # =========================
    # LOGIK
    # =========================

    def update_status(self):
        pm = get_process()
        if pm:
            self.status.config(text="● Connected", fg=SUCCESS)
            try:
                self.money_label.config(text=f"Current Money: {read_value(MONEY_OFFSETS)}")
                self.rune_label.config(text=f"Current Rune Juice: {read_value(RUNE_OFFSETS)}")
            except:
                pass
        else:
            self.status.config(text="● Not connected", fg=ERROR)

        self.root.after(1500, self.update_status)

    def set_money(self, entry):
        try:
            value = int(entry.get())
            set_value(MONEY_OFFSETS, value)
            self.money_label.config(text=f"Current Money: {value}")
        except:
            self.money_label.config(text="Error setting money")

    def set_rune(self, entry):
        try:
            value = int(entry.get())
            set_value(RUNE_OFFSETS, value)
            self.rune_label.config(text=f"Current Rune Juice: {value}")
        except:
            self.rune_label.config(text="Error setting rune juice")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    splash = Splash(root)
    root.after(2200, splash.destroy)
    root.after(2200, root.deiconify)

    app = ACheeseGUI(root)
    root.mainloop()
