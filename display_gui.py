import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import messagebox, scrolledtext
from extraction_tool_gui import list_of_files
import os
import sys


#Need to add 3 buttons 1 for selections 1 for clearing 1 for submittiing
#need to add abilitity to view selections in a list
#input field for indexes
#drop down or checkbox for the desired output types
#add the ability to overide the name of the file if it already exists
#add the ability to save under the same name or increment the number for each new saved pdf.

class MyDisplay:

    def __init__(self):
        self.save_as_entry = None
        self.save_as_label = None
        self.label_optional_f = None
        self.file_menu_top = None
        self.menubar = None
        self.m = None
        self.top_frame = None
        self.root = tk.Tk()

        self.root.geometry("700x600")
        self.root.title("Extraction")


        self.user_entry_fields()
        #Frame for the label/textbox
        self.frame = tk.Frame(self.root, height=400, background="bisque")
        self.frame.pack(expand=True, fill='both')
        #Frame for the buttons
        self.bottom_frame = tk.Frame(self.root, height=400)
        self.bottom_frame.pack(side=tk.BOTTOM)

        self.label = tk.Label(self.frame, text="Paths List", font=("Arial", 16), background="bisque")
        self.label.pack(padx=5, pady=5)

        self.check_state = tk.IntVar()

        self.textbox1 = scrolledtext.ScrolledText(self.frame, height=5, font=('Arial', 10), undo=True)
        self.textbox1.configure(background='#4D4D4D')
        self.textbox1.pack(padx=10, pady=10, expand=True, fill='both')

        self.select_btn = ttk.Button(self.bottom_frame, text="Open a file", command=self.select_file)
        self.select_btn.pack(side=tk.LEFT, padx=15, pady=10, expand=True)

        self.select_all_btn = ttk.Button(self.bottom_frame, text="Open Directory", command=self.select_all_files)
        self.select_all_btn.pack(side=tk.LEFT, padx=20, pady=10, expand=True)

        self.clear_window_btn = ttk.Button(self.bottom_frame, text="Clear", command=lambda: self.textbox1.delete(1.0, tk.END))
        self.clear_window_btn.pack(side=tk.LEFT, padx=25, pady=10, expand=True)

        self.submit_button = ttk.Button(self.bottom_frame, text="Submit", command=self.submit_files)
        self.submit_button.pack(side=tk.LEFT, padx=25, pady=12, expand=True)
        #self.submit_button.pack(expand=True)
        self.close_button = ttk.Button(self.bottom_frame, text="Close", command=self.root.destroy)
        self.close_button.pack(side=tk.LEFT, padx=25, pady=14, expand=True)

        self.top_menu()
        self.right_click_menu()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.mainloop()

    def select_file(self):
        filetype = (
            ('PDF files', '*.pdf'),
            ('Text files', '*.txt'),
            ('PNG files', '*.png'),
            ('All files', '*.*')
        )
        self.textbox1.delete(1.0, tk.END)
        file_paths = fd.askopenfilenames(title='Open file', initialdir='\\', filetypes=filetype)
        for file_path in file_paths:
            self.textbox1.insert(tk.END, file_path + '\n')

    def select_all_files(self):
        folder_path = fd.askdirectory(title="Select Folder")
        if folder_path:
            for dirpath, dirnames, filenames in os.walk(folder_path):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    self.textbox1.insert(tk.END, file_path + '\n')

    def submit_files(self):
        file_paths = self.textbox1.get("1.0", tk.END).strip().split("\n")
        file_name_txt = self.save_as_txt_entry.get().strip()
        file_name_xml = self.save_as_entry.get().strip()
        path_save = self.save_location_entry.get().strip()
        trial_run_enable = self.trial_var.get()
        data_indexes = self.data_indx_entry.get()

        list_of_files(file_paths, file_name_txt, file_name_xml, path_save, trial_run_enable, data_indexes)

    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="Do you really want to quit?"):
            self.root.destroy()

    def right_click_menu(self):
        self.m = tk.Menu(self.frame, tearoff=0)
        self.m.add_command(label="Cut")
        self.m.add_command(label="Copy")
        self.m.add_command(label="Paste")
        self.m.add_separator()
        self.m.add_command(label="Select all")
        self.m.entryconfigure("Cut", command=lambda: self.textbox1.event_generate("<<Cut>>"))
        self.m.entryconfigure("Copy", command=lambda: self.textbox1.event_generate("<<Copy>>"))
        self.m.entryconfigure("Paste", command=lambda: self.textbox1.event_generate("<<Paste>>"))
        self.m.entryconfigure("Select all", command=lambda: self.textbox1.select_range("select_range(0, 'end')"))

        def do_popup(e):
            try:
                self.m.tk_popup(e.x_root, e.y_root)
            finally:
                self.m.grab_release()

        self.textbox1.bind("<Button-3>", do_popup)

    def top_menu(self):
        self.menubar = tk.Menu(self.root)
        self.file_menu_top = tk.Menu(self.menubar, tearoff=0)
        self.file_menu_top.add_command(label="Undo", command=self.textbox1.edit_undo)
        self.file_menu_top.add_command(label="Redo", command=self.textbox1.edit_redo)
        self.file_menu_top.add_command(label="Close", command=self.on_closing)
        self.file_menu_top.add_separator()
        self.file_menu_top.add_command(label="Close Without Question", command=self.root.destroy)
        self.menubar.add_cascade(menu=self.file_menu_top, label="File")
        self.root.config(menu=self.menubar)

    def user_entry_fields(self):
        save_as_var = tk.StringVar()
        save_as_txt = tk.StringVar()
        save_directory_loc = tk.StringVar()
        self.trial_var = tk.IntVar()
        data_index = tk.StringVar()

        #Frame Title
        self.top_frame = tk.Frame(self.root, height=200, bg="grey")
        self.top_frame.pack(fill='x')
        self.label_optional_f = tk.Label(self.top_frame, text="Optional Fields", font=("Arial", 16), bg="grey")
        self.label_optional_f.pack(padx=5, pady=5)

        #Frame 1
        self.frame_1 = tk.Frame(self.root, bg="grey")
        self.frame_1.pack(anchor="n", fill="x")
        self.trial_label = tk.Label(self.frame_1 , text='Trial Run', font=('Arial', 10, 'bold'))
        self.trial_label.pack(side=tk.LEFT, padx=10, pady=5)
        self.c1 = tk.Checkbutton(self.frame_1, variable=self.trial_var, onvalue=1, offvalue=0, activebackground='grey')
        self.c1.config(bg="grey")
        self.c1.pack(side=tk.LEFT, padx=10)

        # Frame 3
        self.frame_3 = tk.Frame(self.root, bg="grey")
        self.frame_3.pack(anchor="n", fill="x")
        self.save_as_txt_label = tk.Label(self.frame_3, text='File Name txt', font=('Arial', 10, 'bold'))
        self.save_as_txt_entry = tk.Entry(self.frame_3, textvariable=save_as_txt, width=40, font=('Arial', 10, 'normal'))
        self.save_as_txt_ex = tk.Label(self.frame_3, text='IE: bob.txt', font=('Arial', 10, 'bold'), bg="#51E2F5")
        self.save_as_txt_label.pack(side=tk.LEFT, padx=10, pady=5)
        self.save_as_txt_entry.pack(side=tk.LEFT)
        self.save_as_txt_ex.pack(side=tk.LEFT, padx=10)


        # Frame 4
        self.frame_4 = tk.Frame(self.root, bg="grey")
        self.frame_4.pack(anchor="n", fill="x")
        self.save_location_label = tk.Label(self.frame_4, text='Save Location', font=('Arial', 10, 'bold'))
        self.save_location_entry = tk.Entry(self.frame_4, textvariable=save_directory_loc, width=40, font=('Arial', 10, 'normal'))
        self.save_location_entry_ex = tk.Label(self.frame_4, text='IE: \\Personal-Projects\\PDF-Scraper', font=('Arial', 10, 'bold'), bg="#51E2F5")
        self.save_location_label.pack(side=tk.LEFT, padx=10, pady=5)
        self.save_location_entry.pack(side=tk.LEFT)
        self.save_location_entry_ex.pack(side=tk.LEFT, padx=10)


        # Frame Title
        self.mid_frame = tk.Frame(self.root, height=200, bg="grey")
        self.mid_frame.pack(fill='x')
        self.label_req_f = tk.Label(self.mid_frame, text="Required Fields", font=("Arial", 16), bg="grey")
        self.label_req_f.pack(padx=5, pady=5)

        #Frame 2
        self.frame_2 = tk.Frame(self.root, bg="grey")
        self.frame_2.pack(anchor="n", fill="x")
        self.save_as_label = tk.Label(self.frame_2, text='Save as', font=('Arial', 10, 'bold'))
        self.save_as_entry = tk.Entry(self.frame_2, textvariable=save_as_var, width=40, font=('Arial', 10, 'normal'))
        self.save_as_entry_ex = tk.Label(self.frame_2, text='IE: nice', font=('Arial', 10, 'bold'), bg="#51E2F5")
        self.save_as_label.pack(side=tk.LEFT, padx=10, pady=5)
        self.save_as_entry.pack(side=tk.LEFT)
        self.save_as_entry_ex.pack(side=tk.LEFT, padx=10)

        #Frame 5

        self.frame_5 = tk.Frame(self.root, bg="grey")
        self.frame_5.pack(anchor="n", fill="x")
        self.data_indx_label = tk.Label(self.frame_5, text='Pub Name & Authors Index', font=('Arial', 10, 'bold'))
        self.data_indx_entry = tk.Entry(self.frame_5, textvariable=data_index, width=40, font=('Arial', 10, 'normal'))
        self.data_indx_ex = tk.Label(self.frame_5, text='IE: 0 1', font=('Arial', 10, 'bold'), bg="#51E2F5")
        self.data_indx_label.pack(side=tk.LEFT, padx=10, pady=5)
        self.data_indx_entry.pack(side=tk.LEFT)
        self.data_indx_ex.pack(side=tk.LEFT, padx=10)





