import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import font
from tkinter import messagebox
import compiler.project2.main as compiler


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pashm Script IDE")
        # self.geometry()
        # self.minsize(535 ,600)

        self.current_directory = ""

        menubar = tk.Menu(self)
        self.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff="false")
        file_menu.add_command(label="Open project               shift+O" ,command=self.open)
        file_menu.add_command(label="New project                shift+N" ,command=self.new)
        file_menu.add_command(label="Save project               shift+S" ,command=self.save)
        file_menu.add_separator()
        file_menu.add_command(label="Exit" ,command=self.destroy)
        build_menu = tk.Menu(menubar, tearoff="false")
        build_menu.add_command(label="Compile               F5" ,command=self.compile)
        settings_menu = tk.Menu(menubar, tearoff="false")
        settings_menu.add_command(label="Change background" ,command=self.background_change)
        settings_menu.add_command(label="Change font" ,command=self.font_change)
        help_menu = tk.Menu(menubar, tearoff="false")
        help_menu.add_command(label="Guide" ,command=lambda: tk.messagebox.showinfo("Hints" ,"-Press F5 to compile."))
        help_menu.add_command(label="About" ,command=lambda: tk.messagebox.showinfo("About" ,"Hello from Madani UNI !"))
        menubar.add_cascade(label="File" ,menu=file_menu)
        menubar.add_cascade(label="Build" ,menu=build_menu)
        menubar.add_cascade(label="Settings" ,menu=settings_menu)
        menubar.add_cascade(label="Help" ,menu=help_menu)

        lf = tk.LabelFrame(self)
        self.editor = tk.Text(lf)
        self.editor.pack(side=tk.LEFT ,fill=tk.BOTH ,expand=True)
        editor_scrl = ttk.Scrollbar(lf ,command=self.editor.yview)
        self.editor.config(yscrollcommand=editor_scrl.set)
        editor_scrl.pack(side=tk.RIGHT ,fill=tk.Y)
        lf.pack(side=tk.TOP ,fill=tk.BOTH ,expand=True)

        self.message = tk.Label(self ,text="Welcome" ,fg="purple")
        self.message.pack(side=tk.BOTTOM)

        self.editor.bind("<<Modified>>" ,lambda e: self.on_modification())
        self.bind("<F5>" ,lambda e: self.compile())
        self.bind("<Control-n>" ,lambda e: self.new())
        self.bind("<Control-N>" ,lambda e: self.new())
        self.bind("<Control-o>" ,lambda e: self.open())
        self.bind("<Control-O>" ,lambda e: self.open())
        self.bind("<Control-S>" ,lambda e: self.save())
        self.bind("<Control-s>" ,lambda e: self.save())

    def compile(self):
        if not self.current_directory or self.editor.compare("end-1c", "==", "1.0"):
            self.message.config(text="Nothing to compile." ,fg="red")
            return

        self.save()

        output_path = os.path.splitext(self.current_directory)[0]
        try:
            content = open(self.current_directory).read()
            result = compiler.code(self.current_directory)

            self.message.config(text="Compiled succesfully." ,fg="green")

            # print(self.current_directory ,output_path+".pashm")
            self.create_top(output_path ,result)

        except Exception as err:
            self.message.config(text="Failed to compile." ,fg="red")
            messagebox.showerror("Compiler Error" ,str(err))

    def open(self):
        if not self.editor.compare("end-1c", "==", "1.0"):
            if not self.new():
                return

        self.current_directory = filedialog.askopenfilename(title="Select file" ,filetypes=(("pashm files","*.pashm") ,("all files","*.*")))
        self.title("Pashm Script IDE"+"--"+self.current_directory)
        code = ""
    
        with open(self.current_directory) as my_file:
            code = my_file.read()

        self.editor.insert(tk.INSERT ,code)
        self.message.config(text="File loaded." ,fg="green")

    def new(self):
        if messagebox.askyesno("Are you sure?" ,"You are going to clear project from memory. Do you want to proceed?"):
            self.current_directory = ""
            self.editor.delete("1.0" ,tk.END)
            return True
        
        return False

    def save(self):
        if not self.current_directory:
            self.current_directory = filedialog.asksaveasfilename(title="Save as" ,filetypes=(("text files" ,"*.txt") ,("all files" ,"*.*")))

        code = self.editor.get("1.0" ,tk.END)
        with open(self.current_directory ,'w') as my_file:
            my_file.write(code)
            self.message.config(text="File saved." ,fg="green")

        if self.title()[-1] != '*':
            return
        else:
            self.title(self.title()[:-1])

    def on_modification(self):
        if self.title()[-1] != '*':
            self.title(self.title() + '*')

    def background_change(self):
        color = colorchooser.askcolor(title ="Choose color")
        self.editor.config(background=color[1])

    def font_change(self):
        top = tk.Toplevel(self)
        top.title("Select Font")
        top.geometry("250x350")
        textfont = font.Font(family='arial')
        self.editor.config(font=textfont)
        
        fc = tk.Listbox(top)
        fc.pack(side=tk.LEFT ,fill=tk.BOTH ,expand=True)
        for f in font.families():
            fc.insert('end', f)

        fc.bind('<ButtonRelease-1>', lambda e: textfont.config(family=fc.get(fc.curselection())))
        
        vsb = tk.Scrollbar(top)
        vsb.pack(side=tk.RIGHT ,fill=tk.Y)
        
        fc.configure(yscrollcommand=vsb.set)
        vsb.configure(command=fc.yview)

    def create_top(self ,output_path ,compiled_code):
        top = tk.Toplevel(self)
        top.title("Pashm Script IDE--"+output_path+".pashm")
        self.wm_attributes("-disabled", True)
        top.transient(self)
        top.protocol("WM_DELETE_WINDOW", lambda t=top: self.destroy_top(top))

        lf = tk.LabelFrame(top)
        editor = tk.Text(lf)
        editor.pack(side=tk.LEFT ,fill=tk.BOTH ,expand=True)
        editor_scrl = ttk.Scrollbar(lf ,command=editor.yview)
        editor.config(yscrollcommand=editor_scrl.set)
        editor_scrl.pack(side=tk.RIGHT ,fill=tk.Y)
        lf.pack(side=tk.TOP ,fill=tk.BOTH ,expand=True)

        editor.insert(tk.INSERT ,compiled_code)
        editor.config(state="disable")

    def destroy_top(self ,top):
        self.wm_attributes("-disabled", False)
        top.destroy()
        self.deiconify()


if __name__ == "__main__":
    App().mainloop()
