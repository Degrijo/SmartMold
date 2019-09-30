import tkinter as tk


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("960x540+300+150")
        self.root.minsize(700, 300)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.toolbar = tk.Frame(self.root, highlightthickness=1, highlightbackground='black', width=300, height=300)
        self.toolbar.grid(row=0, column=3, rowspan=4, sticky='ns', padx=(10, 0), pady=0)
        self.field = tk.Canvas(self.root, width=1000, height=600, highlightthickness=1, highlightbackground='black', relief='ridge', scrollregion=(0, 0, 1170, 745))
        self.field.grid(row=0, column=0, rowspan=2, columnspan=2, sticky='nswe', padx=(0, 10), pady=(0, 10))
        self.buttonbar = tk.Frame(self.root, highlightbackground='black', width=200, height=70, highlightthickness=1)
        self.buttonbar.grid(row=3, column=0, columnspan=2, rowspan=1, sticky='we', padx=(0, 10), pady=(10, 0))
        self.buttonbar.grid_rowconfigure(0, weight=1)
        self.buttonbar.grid_columnconfigure(0, weight=30)
        self.buttonbar.grid_columnconfigure(1, weight=1)
        self.buttonbar.grid_columnconfigure(2, weight=1)
        self.buttons = [tk.Button(self.buttonbar, text='Play', command=self.play, bg='#098B00', activebackground='#097002', activeforeground='white', width=10).grid(row=0, column=1, pady=(10, 3), sticky='we'),
                        tk.Button(self.buttonbar, text='Pause', command=self.pause, bg='#8B0000', activebackground='#700202', activeforeground='white', width=10).grid(row=1, column=1, pady=(3, 10), sticky='we')]
        self.state = True
        self.run = False
        self.sqr_number_x = 150
        self.sqr_number_y = 100
        # for x in range(self.sqr_number_x):
        #     for y in range(self.sqr_number_y):
        #         sqr = self.field.create_rectangle(x * 10, y * 10, (x + 1) * 10, (y + 1) * 10, fill='blue')
        xbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL)
        ybar = tk.Scrollbar(self.root)
        ybar.grid(row=0, column=2, rowspan=3, sticky='ns')
        xbar.grid(row=2, column=0, columnspan=2, sticky='we')
        self.field.configure(xscrollcommand=xbar.set, yscrollcommand=ybar.set)
        xbar.config(command=self.field.xview)
        ybar.config(command=self.field.yview)
        self.root.attributes("-fullscreen", self.state)
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.end_fullscreen)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.root.attributes("-fullscreen", self.state)

    def end_fullscreen(self, event=None):
        self.state = False
        self.root.attributes("-fullscreen", False)

    def play(self):
        self.run = True

    def pause(self):
        self.run = False

    def start(self):
        self.root.mainloop()


if __name__ == '__main__':
    w = MainWindow()
    w.start()
