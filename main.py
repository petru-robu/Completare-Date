import tkinter as tk
import os
from fillpdf import fillpdfs
from tkinter import messagebox

input_path = 'forms/'
output_path = 'filled-forms/'

class FormFiller:
    def __init__(self, pdf_path):
        self.path = pdf_path
        pdf_name = pdf_path[len(input_path):]

        self.output_path = output_path + pdf_name[:-4] + '-filled.pdf'
        self.data_dict = dict()

    def view_fields(self):
        fillpdfs.print_form_fields(self.path)
        
    def change_field(self, field_name, field_value):
        self.data_dict[field_name] = field_value

    def commit_changes(self):
        fillpdfs.write_fillable_pdf(self.path, self.output_path, self.data_dict)

    def identify_field(self, keyword):
        fields_dict = fillpdfs.get_form_fields(self.path)
        for field in fields_dict.keys():
            if field.lower().find(keyword) != -1:
                return field    
        return '-'

class Gui:
    def __init__(self):
        self.collected_data = dict()

        #gui elements
        self.window = tk.Tk()
        self.frame = tk.Frame(self.window)
        self.frame.pack()

        self.frame_CI = tk.LabelFrame(self.frame, text = "Informatii CI: ")
        self.frame_Loc = tk.LabelFrame(self.frame, text = "Informatii adresa:")

        self.labels = [tk.Label(self.frame_CI, text = 'Nume: '), 
            tk.Label(self.frame_CI, text = 'Prenume: '),
            tk.Label(self.frame_CI, text = 'CNP: '),
            tk.Label(self.frame_Loc, text = 'Strada: '),
            tk.Label(self.frame_Loc, text = 'Nr: '),
            tk.Label(self.frame_Loc, text = 'Tara: '),
            tk.Label(self.frame_Loc, text = 'Localitate: '),
            tk.Label(self.frame_Loc, text = 'Sector: '),
        ]

        self.boxes = [tk.Entry(self.frame_CI),
            tk.Entry(self.frame_CI),
            tk.Entry(self.frame_CI),
            tk.Entry(self.frame_Loc),
            tk.Entry(self.frame_Loc),
            tk.Entry(self.frame_Loc),
            tk.Entry(self.frame_Loc),
            tk.Entry(self.frame_Loc)
        ]

    def collect_data(self):
        prenume = self.boxes[1].get()
        nume = self.boxes[0].get()
        cnp = self.boxes[2].get()
        std = self.boxes[3].get()
        nr = self.boxes[4].get()
        tara = self.boxes[5].get()
        loc = self.boxes[6].get()
        sect = self.boxes[7].get()

        if not prenume.isalpha():
            tk.messagebox.showwarning(title='Atentie!', message='Prenume invalid!')
            self.boxes[1].delete(0, tk.END)
        elif not nume.isalpha():
            tk.messagebox.showwarning(title='Atentie!', message='Nume invalid!')
            self.boxes[0].delete(0, tk.END)
        elif not len(cnp) == 13 or not cnp.isnumeric():
            tk.messagebox.showwarning(title='Atentie!', message='CNP invalid!')
            self.boxes[2].delete(0, tk.END)
        else:
            self.collected_data['nume'] = nume
            self.collected_data['prenume'] = prenume
            self.collected_data['cnp'] = cnp
            self.collected_data['strada'] = std
            self.collected_data['nr'] = nr
            self.collected_data['tara'] = tara
            self.collected_data['localitate'] = loc
            self.collected_data['sector'] = sect
            tk.messagebox.showinfo(title='Receptionat!', message='Date Introduse Corect!')
            self.window.quit()


    def params(self):
        self.window.title("Formular Introducere Date")
        
        self.frame_CI.grid(row=0, column=0, padx=20, pady=20)
        self.frame_Loc.grid(row=1, column=0, padx=20, pady=20)

        self.labels[0].grid(row=0, column=0)
        self.labels[1].grid(row=0, column=1)
        self.labels[2].grid(row=2, column=0)

        self.labels[3].grid(row=0, column=0)
        self.labels[4].grid(row=0, column=1)
        self.labels[5].grid(row=0, column=2)
        self.labels[6].grid(row=0, column=3)
        self.labels[7].grid(row=2, column=0)

        self.boxes[0].grid(row=1, column=0)
        self.boxes[1].grid(row=1, column=1)
        self.boxes[2].grid(row=3, column=0)

        self.boxes[3].grid(row=1, column=0)
        self.boxes[4].grid(row=1, column=1)
        self.boxes[5].grid(row=1, column=2)
        self.boxes[6].grid(row=1, column=3)
        self.boxes[7].grid(row=3, column=0)

        for widget in self.frame_CI.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        for widget in self.frame_Loc.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        button = tk.Button(self.frame, text="Trimite", command=self.collect_data)
        button.grid(row=4, column=0)
        button.grid_configure(padx=20, pady=10)
        
    def get_collected_data(self):
        return self.collected_data

    def start(self):
        self.params()
        self.window.mainloop()

if __name__ == '__main__':
    gui = Gui()
    gui.start()
    info = gui.get_collected_data()
    print(info)

    for filename in os.listdir(input_path):
        pdf = input_path + filename
        form = FormFiller(pdf)
        for entry in info:
            fieldname = form.identify_field(entry)
            if fieldname != '-':
                form.change_field(fieldname, info[entry])
            else:
                print(f"Nu se gaseste casuta de completat ({entry})")
        form.commit_changes()