import tkinter as tk
from tkinter import ttk, filedialog
from model import MeasurementModel

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Temperature Monitor Pro")
        self.model = MeasurementModel()

        self.tree = ttk.Treeview(root, columns=("Date", "Location", "Value", "RGB"), show='headings')
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Location", text="Место")
        self.tree.heading("Value", text="Темп.")
        self.tree.heading("RGB", text="Цвет")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.frame = tk.Frame(root)
        self.frame.pack()

        tk.Label(self.frame, text="Строка:").pack(side=tk.LEFT)
        self.entry = tk.Entry(self.frame, width=40)
        self.entry.pack(side=tk.LEFT)

        tk.Button(self.frame, text="Добавить", command=self.add).pack(side=tk.LEFT)
        tk.Button(self.frame, text="Удалить", command=self.delete).pack(side=tk.LEFT)
        tk.Button(root, text="Выполнить файл команд", command=self.load_commands).pack(fill=tk.X)

    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in self.model.items:
            self.tree.insert("", tk.END, values=(item.date, item.location, item.value, item.rgb))

    def add(self):
        if self.model.add_from_line(self.entry.get()):
            self.refresh_table()

    def delete(self):
        selected = self.tree.selection()
        if selected:
            idx = self.tree.index(selected[0])
            self.model.delete_item(idx)
            self.refresh_table()

    def load_commands(self):
        path = filedialog.askopenfilename()
        if path:
            if self.model.execute_commands_file(path):
                self.refresh_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()