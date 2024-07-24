import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from DataModel import miabis_schema, sprec_schema, omop_person_schema, condition_occurrence_schema, procedure_occurrence_schema

def clear_form(entries):
    for field in entries.values():
        field.delete(0, tk.END)

class BiobankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Biobank Data Entry and Exploration")

        # Create tabs
        self.tab_control = ttk.Notebook(root)
        self.miabis_tab = ttk.Frame(self.tab_control)
        self.sprec_tab = ttk.Frame(self.tab_control)
        self.omop_tab = ttk.Frame(self.tab_control)
        self.condition_tab = ttk.Frame(self.tab_control)
        self.procedure_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.miabis_tab, text='MIABIS')
        self.tab_control.add(self.sprec_tab, text='SPREC')
        self.tab_control.add(self.omop_tab, text='OMOP Person')
        self.tab_control.add(self.condition_tab, text='Condition Occurrence')
        self.tab_control.add(self.procedure_tab, text='Procedure Occurrence')
        self.tab_control.pack(expand=1, fill='both')

        # Initialize data storage
        self.miabis_data = []
        self.sprec_data = []
        self.omop_data = []
        self.condition_data = []
        self.procedure_data = []

        # Create form fields for MIABIS
        self.create_miabis_form()
        # Create form fields for SPREC
        self.create_sprec_form()
        # Create form fields for OMOP Person
        self.create_omop_form()
        # Create form fields for Condition Occurrence
        self.create_condition_form()
        # Create form fields for Procedure Occurrence
        self.create_procedure_form()

        # Add buttons
        self.save_button = tk.Button(root, text="Save to CSV", command=self.save_to_csv)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.load_button = tk.Button(root, text="Load from CSV", command=self.load_from_csv)
        self.load_button.pack(side=tk.LEFT, padx=10, pady=10)

    def create_table(self, parent, columns):
        container = ttk.Frame(parent)
        container.grid(row=0, column=0, columnspan=parent.grid_size()[0], sticky='nsew')

        table = ttk.Treeview(container, columns=list(columns), show='headings')
        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=100)
        table.grid(row=0, column=0, sticky='nsew')

        scrollbar_x = ttk.Scrollbar(container, orient='horizontal', command=table.xview)
        table.configure(xscrollcommand=scrollbar_x.set)
        scrollbar_x.grid(row=1, column=0, sticky='ew')

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Bind the <Configure> event to update the total width
        table.bind('<Configure>', lambda e: self.update_total_width(container, table, scrollbar_x))

        return table

    def update_total_width(self, container, table, scrollbar_x):
        total_width = sum(table.column(col, width=None) for col in table['columns'])
        container.configure(width=total_width + scrollbar_x.winfo_width())
        table.configure(xscrollcommand=scrollbar_x.set)
        # Reload the table to ensure the horizontal scrollbar works
        table.update_idletasks()

    def add_miabis_entry(self):
        entry = {field: self.miabis_entries[field].get() for field in miabis_schema.keys()}
        print("MIABIS Entry:", entry)  # Debug print
        self.miabis_data.append(entry)
        self.update_table(self.miabis_table, self.miabis_data)
        clear_form(self.miabis_entries)
        messagebox.showinfo("Info", "MIABIS entry added")

    def add_sprec_entry(self):
        entry = {field: self.sprec_entries[field].get() for field in sprec_schema.keys()}
        entry["person_id"] = self.person_id_entry.get()
        print("SPREC Entry:", entry)  # Debug print
        self.sprec_data.append(entry)
        self.update_table(self.sprec_table, self.sprec_data)
        clear_form(self.sprec_entries)
        messagebox.showinfo("Info", "SPREC entry added")

    def add_omop_entry(self):
        entry = {field: self.omop_entries[field].get() for field in omop_person_schema.keys()}
        entry["person_id"] = self.omop_person_id_entry.get()
        print("OMOP Entry:", entry)  # Debug print
        self.omop_data.append(entry)
        self.update_table(self.omop_table, self.omop_data)
        clear_form(self.omop_entries)
        messagebox.showinfo("Info", "OMOP Person entry added")

    def add_condition_entry(self):
        entry = {field: self.condition_entries[field].get() for field in condition_occurrence_schema.keys()}
        entry["person_id"] = self.condition_person_id_entry.get()
        print("Condition Entry:", entry)  # Debug print
        self.condition_data.append(entry)
        self.update_table(self.condition_table, self.condition_data, filter_person_id=entry["person_id"])
        clear_form(self.condition_entries)
        messagebox.showinfo("Info", "Condition entry added")

    def add_procedure_entry(self):
        entry = {field: self.procedure_entries[field].get() for field in procedure_occurrence_schema.keys()}
        entry["person_id"] = self.procedure_person_id_entry.get()
        print("Procedure Entry:", entry)  # Debug print
        self.procedure_data.append(entry)
        self.update_table(self.procedure_table, self.procedure_data, filter_person_id=entry["person_id"])
        clear_form(self.procedure_entries)
        messagebox.showinfo("Info", "Procedure entry added")


    def update_table(self, table, data, filter_person_id=None):
        for row in table.get_children():
            table.delete(row)
        for entry in data:
            if filter_person_id is None or entry.get('person_id') == filter_person_id:
                table.insert('', 'end', values=list(entry.values()))

    def create_miabis_form(self):
        self.miabis_entries = {}
        fields = list(miabis_schema.keys())
        num_fields = len(fields)

        for i, field in enumerate(fields):
            row = i // 2
            col = (i % 2) * 2
            tk.Label(self.miabis_tab, text=field).grid(row=row, column=col, padx=10, pady=5)
            entry = tk.Entry(self.miabis_tab)
            entry.grid(row=row, column=col + 1, padx=10, pady=5)
            self.miabis_entries[field] = entry

        self.add_miabis_button = tk.Button(self.miabis_tab, text="Add MIABIS Entry", command=self.add_miabis_entry)
        self.add_miabis_button.grid(row=(num_fields // 2) + 1, column=0, columnspan=4, pady=10)

        self.miabis_table = self.create_table(self.miabis_tab, miabis_schema.keys())
        self.update_table(self.miabis_table, self.miabis_data)
        self.miabis_table.grid(row=(num_fields // 2) + 2, column=0, columnspan=4, sticky='nsew')

        # Configure grid to expand the table
        self.miabis_tab.grid_rowconfigure((num_fields // 2) + 2, weight=1)
        self.miabis_tab.grid_columnconfigure(0, weight=1)
        self.miabis_tab.grid_columnconfigure(1, weight=1)
        self.miabis_tab.grid_columnconfigure(2, weight=1)
        self.miabis_tab.grid_columnconfigure(3, weight=1)

    def create_sprec_form(self):
        self.sprec_entries = {}
        for i, field in enumerate(sprec_schema.keys()):
            tk.Label(self.sprec_tab, text=field).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(self.sprec_tab)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.sprec_entries[field] = entry

        # Add person_id field
        tk.Label(self.sprec_tab, text="person_id").grid(row=len(sprec_schema), column=0, padx=10, pady=5)
        self.person_id_entry = tk.Entry(self.sprec_tab)
        self.person_id_entry.grid(row=len(sprec_schema), column=1, padx=10, pady=5)
        self.sprec_entries["person_id"] = self.person_id_entry

        # Button to open OMOP Person form
        self.open_omop_button = tk.Button(self.sprec_tab, text="Open OMOP Person Form", command=self.open_omop_form)
        self.open_omop_button.grid(row=len(sprec_schema) + 1, column=1, columnspan=1, pady=10)

        self.add_sprec_button = tk.Button(self.sprec_tab, text="Add SPREC Entry", command=self.add_sprec_entry)
        self.add_sprec_button.grid(row=len(sprec_schema) + 1, column=0, columnspan=1, pady=10)

        self.sprec_table = self.create_table(self.sprec_tab, list(sprec_schema.keys()) + ['person_id'])
        self.update_table(self.sprec_table, self.sprec_data)
        # Configure grid to expand the table
        self.sprec_tab.grid_rowconfigure(len(sprec_schema) + 3, weight=1)
        self.sprec_tab.grid_columnconfigure(0, weight=1)
        self.sprec_tab.grid_columnconfigure(1, weight=1)

    def create_omop_form(self):
        self.omop_entries = {}
        fields = list(omop_person_schema.keys())
        num_fields = len(fields)

        for i, field in enumerate(fields):
            row = i // 2
            col = (i % 2) * 2
            tk.Label(self.omop_tab, text=field).grid(row=row, column=col, padx=10, pady=5)
            entry = tk.Entry(self.omop_tab)
            entry.grid(row=row, column=col + 1, padx=10, pady=5)
            self.omop_entries[field] = entry

        # Add person_id field at the end
        tk.Label(self.omop_tab, text="person_id").grid(row=(num_fields // 2) + 1, column=0, padx=10, pady=5)
        self.omop_person_id_entry = tk.Entry(self.omop_tab)
        self.omop_person_id_entry.grid(row=(num_fields // 2) + 1, column=1, padx=10, pady=5)
        self.omop_entries["person_id"] = self.omop_person_id_entry

        # Button to open Condition and Procedure forms
        self.open_condition_button = tk.Button(self.omop_tab, text="Open Condition Form",
                                               command=self.open_condition_form)
        self.open_condition_button.grid(row=(num_fields // 2) + 2, column=0, columnspan=1, pady=10)
        self.open_procedure_button = tk.Button(self.omop_tab, text="Open Procedure Form",
                                               command=self.open_procedure_form)
        self.open_procedure_button.grid(row=(num_fields // 2) + 2, column=1, columnspan=1, pady=10)

        self.add_omop_button = tk.Button(self.omop_tab, text="Add OMOP Person Entry", command=self.add_omop_entry)
        self.add_omop_button.grid(row=(num_fields // 2) + 3, column=0, columnspan=2, pady=10)

        self.omop_table = self.create_table(self.omop_tab, omop_person_schema.keys())
        self.update_table(self.omop_table, self.omop_data)
        self.omop_table.grid(row=(num_fields // 2) + 4, column=0, columnspan=4, sticky='nsew')

        # Configure grid to expand the table
        self.omop_tab.grid_rowconfigure((num_fields // 2) + 4, weight=1)
        self.omop_tab.grid_columnconfigure(0, weight=1)
        self.omop_tab.grid_columnconfigure(1, weight=1)
        self.omop_tab.grid_columnconfigure(2, weight=1)
        self.omop_tab.grid_columnconfigure(3, weight=1)

    def create_condition_form(self):
        self.condition_entries = {}
        row_index = 0
        for field in condition_occurrence_schema.keys():
            if field != "person_id":  # Skip person_id as it will be handled separately
                tk.Label(self.condition_tab, text=field).grid(row=row_index, column=0, padx=10, pady=5)
                entry = tk.Entry(self.condition_tab)
                entry.grid(row=row_index, column=1, padx=10, pady=5)
                self.condition_entries[field] = entry
                row_index += 1

        # Add person_id field at the end
        tk.Label(self.condition_tab, text="person_id").grid(row=row_index, column=0, padx=10, pady=5)
        self.condition_person_id_entry = tk.Entry(self.condition_tab)
        self.condition_person_id_entry.grid(row=row_index, column=1, padx=10, pady=5)
        self.condition_entries["person_id"] = self.condition_person_id_entry

        self.add_condition_button = tk.Button(self.condition_tab, text="Add Condition Entry", command=self.add_condition_entry)
        self.add_condition_button.grid(row=row_index + 1, column=0, columnspan=2, pady=10)

        self.condition_table = self.create_table(self.condition_tab, list(condition_occurrence_schema.keys()) + ['person_id'])
        self.update_table(self.condition_table, self.condition_data)

        self.condition_tab.grid_rowconfigure(len(condition_occurrence_schema) + 1, weight=1)
        self.condition_tab.grid_columnconfigure(0, weight=1)
        self.condition_tab.grid_columnconfigure(1, weight=1)

    def create_procedure_form(self):
        self.procedure_entries = {}
        row_index = 0
        for field in procedure_occurrence_schema.keys():
            if field != "person_id":  # Skip person_id as it will be handled separately
                tk.Label(self.procedure_tab, text=field).grid(row=row_index, column=0, padx=10, pady=5)
                entry = tk.Entry(self.procedure_tab)
                entry.grid(row=row_index, column=1, padx=10, pady=5)
                self.procedure_entries[field] = entry
                row_index += 1

        # Add person_id field at the end
        tk.Label(self.procedure_tab, text="person_id").grid(row=row_index, column=0, padx=10, pady=5)
        self.procedure_person_id_entry = tk.Entry(self.procedure_tab)
        self.procedure_person_id_entry.grid(row=row_index, column=1, padx=10, pady=5)
        self.procedure_entries["person_id"] = self.procedure_person_id_entry

        self.add_procedure_button = tk.Button(self.procedure_tab, text="Add Procedure Entry", command=self.add_procedure_entry)
        self.add_procedure_button.grid(row=row_index + 1, column=0, columnspan=2, pady=10)

        self.procedure_table = self.create_table(self.procedure_tab, list(procedure_occurrence_schema.keys()) + ['person_id'])
        self.update_table(self.procedure_table, self.procedure_data)
        self.procedure_table.grid(row=row_index + 2, column=0, columnspan=2, sticky='nsew')

        self.procedure_tab.grid_rowconfigure(len(procedure_occurrence_schema) + 1, weight=1)
        self.procedure_tab.grid_columnconfigure(0, weight=1)
        self.procedure_tab.grid_columnconfigure(1, weight=1)

    def open_omop_form(self):
        person_id = self.person_id_entry.get()
        self.omop_person_id_entry.delete(0, tk.END)
        self.omop_person_id_entry.insert(0, person_id)
        self.tab_control.select(self.omop_tab)
        self.update_table(self.condition_table, self.condition_data, filter_person_id=person_id)
        self.update_table(self.procedure_table, self.procedure_data, filter_person_id=person_id)

    def open_condition_form(self):
        person_id = self.omop_person_id_entry.get()
        self.condition_person_id_entry.delete(0, tk.END)
        self.condition_person_id_entry.insert(0, person_id)
        self.tab_control.select(self.condition_tab)
        self.update_table(self.condition_table, self.condition_data, filter_person_id=person_id)

    def open_procedure_form(self):
        person_id = self.omop_person_id_entry.get()
        self.procedure_person_id_entry.delete(0, tk.END)
        self.procedure_person_id_entry.insert(0, person_id)
        self.tab_control.select(self.procedure_tab)
        self.update_table(self.procedure_table, self.procedure_data, filter_person_id=person_id)

    def save_to_csv(self):
        try:
            pd.DataFrame(self.miabis_data).to_csv('miabis_data.csv', sep=';', index=False)
            pd.DataFrame(self.sprec_data).to_csv('sprec_data.csv', sep=';', index=False)
            pd.DataFrame(self.omop_data).to_csv('omop_person_data.csv', sep=';', index=False)
            pd.DataFrame(self.condition_data).to_csv('condition_occurrence_data.csv', sep=';', index=False)
            pd.DataFrame(self.procedure_data).to_csv('procedure_occurrence_data.csv', sep=';', index=False)
            messagebox.showinfo("Info", "Data saved to CSV files")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")

    def load_from_csv(self):
        try:
            self.miabis_data = pd.read_csv('miabis_data.csv', sep=';').to_dict(orient='records')
            self.sprec_data = pd.read_csv('sprec_data.csv', sep=';').to_dict(orient='records')
            self.omop_data = pd.read_csv('omop_person_data.csv', sep=';').to_dict(orient='records')
            self.condition_data = pd.read_csv('condition_occurrence_data.csv', sep=';').to_dict(orient='records')
            self.procedure_data = pd.read_csv('procedure_occurrence_data.csv', sep=';').to_dict(orient='records')
            self.update_table(self.miabis_table, self.miabis_data)
            self.update_table(self.sprec_table, self.sprec_data)
            self.update_table(self.omop_table, self.omop_data)
            self.update_table(self.condition_table, self.condition_data)
            self.update_table(self.procedure_table, self.procedure_data)
            messagebox.showinfo("Info", "Data loaded from CSV files")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BiobankApp(root)
    root.mainloop()