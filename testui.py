import tkinter as tk
from tkinter import ttk
import time

class DebouncedEntry(tk.Entry):
    def __init__(self, *args, **kwargs):
        self.delay = kwargs.pop('delay', 20)  # debounce delay in milliseconds
        super().__init__(*args, **kwargs)
        self.var = tk.StringVar()
        self.var.trace_add('write', self.on_change)
        self.config(textvariable=self.var)
        self.after_id = None

    def on_change(self, *args):
        if self.after_id is not None:
            self.after_cancel(self.after_id)
        self.after_id = self.after(self.delay, self.perform_search)

    def perform_search(self):
        query = self.var.get()
        print(f"Searching for: {query}")
        # Perform your search logic here

root = tk.Tk()
entry = DebouncedEntry(root, delay=500)  # 500ms debounce delay
entry.pack(padx=20, pady=20)

root.mainloop()