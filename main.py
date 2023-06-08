import tkinter as tk

from fillpdf import fillpdfs
from tkinter import messagebox

pdf = 'forms/anexa_1_inregistrare_fiscala.pdf'

class FormFiller:
    def __init__(self, pdf_path):
        self.path = pdf_path
        self.output_path = pdf_path[:-4] + '-filled.pdf'
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
            print(field)
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

        self.data_frame = tk.LabelFrame(self.frame, text = "Informatii: ")

        self.label_nume = tk.Label(self.data_frame, text = 'Nume: ')
        self.label_prenume = tk.Label(self.data_frame, text = 'Prenume: ')
        self.label_cnp = tk.Label(self.data_frame, text = 'CNP: ')

        self.box_nume = tk.Entry(self.data_frame)
        self.box_prenume = tk.Entry(self.data_frame)
        self.box_cnp = tk.Entry(self.data_frame)

    def collect_data(self):
        prenume = self.box_prenume.get()
        nume = self.box_nume.get()
        cnp = self.box_cnp.get()
        
        if not prenume.isalpha():
            tk.messagebox.showwarning(title='Atentie!', message='Prenume invalid!')
            self.box_prenume.delete(0, tk.END)
        elif not nume.isalpha():
            tk.messagebox.showwarning(title='Atentie!', message='Nume invalid!')
            self.box_nume.delete(0, tk.END)
        elif not len(cnp) == 13 or not cnp.isnumeric():
            tk.messagebox.showwarning(title='Atentie!', message='CNP invalid!')
            self.box_cnp.delete(0, tk.END)
        else:
            self.collected_data['nume'] = nume
            self.collected_data['prenume'] = prenume
            self.collected_data['cnp'] = cnp
            tk.messagebox.showinfo(title='Receptionat!', message='Date Introduse Corect!')
            self.window.quit()


    def params(self):
        self.window.title("Formular Introducere Date")
        
        self.data_frame.grid(row=0, column=0, padx=20, pady=20)
        self.label_nume.grid(row=0, column=0)
        self.label_prenume.grid(row=0, column=1)
        self.label_cnp.grid(row=2, column=0)
        self.box_nume.grid(row=1, column=0)
        self.box_prenume.grid(row=1, column=1)
        self.box_cnp.grid(row=3, column=0)

        for widget in self.data_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        button = tk.Button(self.frame, text="Trimite", command=self.collect_data)
        button.grid(row=1, column=0)
        button.grid_configure(padx=20, pady=10)
        
    def get_collected_data(self):
        return self.collected_data

    def start(self):
        self.params()
        self.window.mainloop()

if __name__ == '__main__':
    gui = Gui()
    gui.start()
    form = FormFiller(pdf)

    info = gui.get_collected_data()
    for entry in info:
        fieldname = form.identify_field(entry)
        if fieldname != '-':
            form.change_field(fieldname, info[entry])
        else:
            print(f"Nu se gaseste casuta de completat ({entry})")

    form.commit_changes()
