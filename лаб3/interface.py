import tkinter as tk
from tkinter import ttk, messagebox
from model import MeasurementModel

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Temperature Monitor 3.0")
        self.model = MeasurementModel()
        self.model.load_from_file("data.txt")

        self.tree = ttk.Treeview(self.root, columns=("1", "2", "3", "4"), show="headings")
        for i, text in enumerate(["Дата", "Локация", "Значение", "RGB"], 1):
            self.tree.heading(str(i), text=text)
        self.tree.pack()

        self.entries = [tk.Entry(self.root) for _ in range(4)]
        for e in self.entries: e.pack()

        tk.Button(self.root, text="Добавить", command=self.add).pack()
        tk.Button(self.root, text="Удалить", command=self.delete).pack()

        self.refresh_table()

    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for obj in self.model.items:
            self.tree.insert("", "end", values=(obj.date, obj.location, obj.value, obj.rgb))

    def add(self):
        raw = f'Entry {self.entries[0].get()} "{self.entries[1].get()}" {self.entries[2].get()} {self.entries[3].get()}'
        success = self.model.add_from_line(raw)
        
        if success:
            self.refresh_table()
        else:
            messagebox.showerror("Ошибка", "Не удалось добавить запись. Проверьте лог в консоли.")

    def delete(self):
        sel = self.tree.selection()
        if sel:
            idx = self.tree.index(sel[0])
            self.model.delete_item(idx)
            self.refresh_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()