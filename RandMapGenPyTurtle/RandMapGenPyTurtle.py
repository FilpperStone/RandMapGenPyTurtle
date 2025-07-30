from dis import Instruction
import tkinter
#from tkinter import ttk
#from tkinter import *
#from tkinter.ttk import *
import random
import os
from tkinter import messagebox
#from tkinter import simpledialog, Toplevel
#from tkinter import filedialog
#import TKinterModernThemes as TKMT
import customtkinter
from customtkinter import CTkCheckBox, CTkSwitch
from customtkinter import *
#import CTkListbox
#from CTkListbox import CTkListbox
from customtkinter.windows.widgets import CTkLabel, CTkOptionMenu, ctk_textbox#, CTkListbox
import turtle
from turtle import *
import time

#Comando per buildare: python -m PyInstaller --onefile RandMapGenPyTurtle.py -i dice.ico -n "MapRoller" -w

# Dizionario di traduzioni
translations = {
    "English": {
        "Save": "Save",
        "New": "New",
        "Load": "Load",
        "Add": "Add",
        "Print": "Print",
        "Program": "Program",
        "Reset": "Reset",
        "Close": "Close",
        "Add direction": "Add direction",
        "Add structure": "Add structure",
        "Eliminate": "Eliminate",
        "Cancel": "Cancel",
        "Delete": "Delete",
        "Autorun": "Autorun",
        "Generate": "Generate",
        "Turns": "Turns",
        "Direction": "Direction",
        "Structures": "Structures",
        "Directions": "Directions",
        "Structure": "Structure",
        "Light": "Light",
        "Dark": "Dark",
        "Execute": "Execute",
        "Repeat": "Repeat",
        "Theme": "Theme",
        "Language": "Language",
        "Scenery": "Scenery",
        "Skip": "Skip",
        "deletes": "deletes",
        "skips": "skips",
        "Edit": "Edit",
        "Settings": "Settings",
    },
    "Italiano": {
        "Save": "Salva",
        "New": "Nuovo",
        "Load": "Carica",
        "Add": "Aggiungi",
        "Print": "Stampa",
        "Program": "Programma",
        "Reset": "Resetta",
        "Close": "Chiudi",
        "Add direction": "Aggiungi direzione",
        "Add structure": "Aggiungi struttura",
        "Eliminate": "Elimina",
        "Cancel": "Annulla",
        "Delete": "Cancella",
        "Autorun": "Esegui automaticamente",
        "Generate": "Genera",
        "Turns": "Turni",
        "Direction": "Direzione",
        "Structure": "Struttura",
        "Structures": "Strutture",
        "Directions": "Direzioni",
        "Light": "Chiaro",
        "Dark": "Scuro",
        "Execute": "Esegui",
        "Repeat": "Ripeti", 
        "Theme": "Tema",
        "Language": "Lingua",
        "Scenery": "Scenario",
        "Skip": "Salta",
        "deletes": "cancella",
        "skips": "salta",
        "Edit": "Modifica",
        "Settings": "Impostazioni",


    }
}

def set_lang(value):
    global langvalue, themevalue
    langvalue = value
    recreate_widgets()
    update_direction_labels()
    update_structure_labels()
    setup()

def set_theme(value):
    global themevalue
    themevalue = value
    if value == "Chiaro" or value == "Light":
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("dark-blue")
    elif value == "Scuro" or value == "Dark":
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")
    recreate_widgets()
    update_direction_labels()
    update_structure_labels()
    setup()

def recreate_widgets():
    global mainframe, direzione_entry, struttura_entry, segmented_button, optionmenu, langoptionmenu, themevalue, langvalue, genbutt

    for widget in mainframe.winfo_children():
        widget.destroy()

    direzione_entry = customtkinter.CTkEntry(mainframe, width=200)
    direzione_entry.grid(column=2, row=3, sticky=(customtkinter.W, customtkinter.E), padx=5, pady=5)
    direzione_entry.grid_propagate(False)

    struttura_entry = customtkinter.CTkEntry(mainframe, width=200)
    struttura_entry.grid(column=3, row=3, sticky=(customtkinter.W, customtkinter.E), padx=5, pady=5)
    struttura_entry.grid_propagate(False)

    segmented_button = customtkinter.CTkSegmentedButton(
        mainframe,
        values=[translations[langvalue]["Save"], translations[langvalue]["New"], translations[langvalue]["Load"],
                translations[langvalue]["Add"], translations[langvalue]["Delete"], translations[langvalue]["Print"], translations[langvalue]["Program"],
                translations[langvalue]["Settings"], translations[langvalue]["Reset"], translations[langvalue]["Close"]],
        command=segmented_button_callback
    )
    segmented_button.grid(column=1, row=0, columnspan=4, sticky=(customtkinter.W, customtkinter.E), padx=5, pady=5)
    segmented_button.grid_propagate(False)

    customtkinter.CTkButton(mainframe, text=translations[langvalue]["Add direction"], width=200, command=append).grid(column=2, row=4, sticky=customtkinter.N, padx=5, pady=5)
    customtkinter.CTkButton(mainframe, text=translations[langvalue]["Add structure"], width=200, command=appens).grid(column=3, row=4, sticky=customtkinter.N, padx=5, pady=5)
    customtkinter.CTkButton(mainframe, text=translations[langvalue]["Eliminate"], command=eliminate).grid(column=4, row=3, sticky=customtkinter.W, padx=5, pady=5)
    #customtkinter.CTkButton(mainframe, text=translations[langvalue]["Delete"], command=delete).grid(column=4, row=4, sticky=customtkinter.W, padx=5, pady=5)
    customtkinter.CTkButton(mainframe, text=translations[langvalue]["Autorun"], command=autorun).grid(column=4, row=1, sticky=customtkinter.W, padx=5, pady=5)
    genbutt=customtkinter.CTkButton(mainframe, text=translations[langvalue]["Generate"], command=generate)
    genbutt.grid(column=1, row=3, sticky=customtkinter.W, padx=5, pady=5)
    customtkinter.CTkButton(mainframe, text=translations[langvalue]["Turns"], command=turn).grid(column=1, row=1, sticky=customtkinter.W, padx=5, pady=5)

    customtkinter.CTkLabel(mainframe, text=translations[langvalue]["Direction"]).grid(column=2, row=1, sticky=customtkinter.N, padx=5, pady=5)
    customtkinter.CTkLabel(mainframe, text=translations[langvalue]["Structure"]).grid(column=3, row=1, sticky=customtkinter.N, padx=5, pady=5)

folder_name = ""

def create():
    global loaded
    folder_name = folderwindow()

    print(folder_name)

    if os.path.exists(folder_name):
        messagebox.showerror("Error", "Folder already exists.")
    if strutture and direzioni:
        os.mkdir(folder_name)
        save()
        update_scenery()
        loaded = True
        return
    else:
        messagebox.showerror("Error", "Please enter at least one structure and one direction.")

def save():
    global folder_name
    if not loaded:
        folder_name = folderwindow(initialdir=os.path, title="Select file")
    else:
        directions_file = os.path.join(folder_name, "directions.txt")
        structures_file = os.path.join(folder_name, "structures.txt")

        if not os.path.exists(folder_name):
            messagebox.showerror("Error", "The folder does not exist.")
            return  # Exit the function if the folder does not exist

        with open(directions_file, "w") as f:
            for item in direzioni:
                f.write(item)  # Write each item in the list to a new line
        with open(structures_file, "w") as f:
            for item in strutture:
                f.write(item)  # Write each item in the list to a new line

def folderwindow():
    global folder_name_var, folder_name
    print(type(folder_name))
    folder_window_open = True
    # Create a window to enter the folder name
    folder_window = CTkInputDialog(title="Enter folder name", text="Scenery name:")
    folder_window.focus()
    folder_name=folder_window.get_input()
    
    return folder_name

def turnwindow():
    global turn_var, turn_window_open, turn_window, turn_entry
    turn_window_open.set(True)
    
    turn_window = customtkinter.CTkInputDialog(text="Type in a number:", title="Turns")
    turn_window.focus()
    
    #customtkinter.CTkLabel(turn_window, text="Number of turns:").grid(column=0, row=0, padx=20, pady=10)
    turn_var=int(turn_window.get_input())
    
    #turn_entry = customtkinter.CTkEntry(turn_window, width=200)
    #turn_entry.grid(column=1, row=0, padx=20, pady=10)


    #customtkinter.CTkButton(turn_window, text="OK", command=confirm).grid(column=0, row=1, columnspan=2, padx=20, pady=10)
    #customtkinter.CTkButton(turn_window, text="Cancel", command=turn_window.destroy).grid(column=0, row=2, columnspan=2, padx=20, pady=10)
        
def confirm():
    global turn_var, turn_window
    try:
        turn_var = turn_entry.get()
        turn_window.destroy()
        turn_window_open.set(False)
    except ValueError:
       messagebox.showerror("Error", "Please enter a valid number.")

'''
def turnwindow():
    global turn_var, turn_window_open
    turn_window_open = True

    # Ask for an integer input, store it directly in turn_var
    turn_var = simpledialog.askinteger("Enter number of turns", "Number of turns:")

    turn_window_open = False
'''

def load():
    global folder_name, loaded

    folder_name = filedialog.askdirectory(initialdir=os.path, title="Select folder")
    directions_file = os.path.join(folder_name, "directions.txt")
    structures_file = os.path.join(folder_name, "structures.txt")
    shapes_file = os.path.join(folder_name,"Shapes.txt")
    print(directions_file)
    if os.path.exists(directions_file) and os.path.exists(structures_file):
        with open(directions_file, "r") as f:
            direzioni.clear()
            direzioni.extend(f.readlines())
        update_direction_labels()
        direzione_entry.delete(0, END)

        with open(structures_file, "r") as f:
            strutture.clear()
            strutture.extend(f.readlines())
        update_structure_labels()
        struttura_entry.delete(0, END)
        loaded = True
        setup()
        update_scenery()

        current_group = []

        
        print("Caricamento file:", shapes_file)

        # Lettura del file e parsing delle forme
        with open(shapes_file, "r") as f:
            shapes.clear()
            
            for line in f:
                if line.strip() != "-":
                    current_group.append(line.strip())
                else:
                    if current_group:
                        shapes.append(current_group)
                        current_group = []
            if current_group:
                shapes.append(current_group)
        shapes_check()
    else:
        messagebox.showerror("Error", "The folder or files do not exist.")
def shapes_check():
    shapes_data.clear()
    for shape in shapes:
        dir_patterns=cont_check(shape)
        shapes_data.append(dir_patterns)

def shape_check(shape, shape_index):
    shapes[shape_index] = shape
    dir_patterns=cont_check(shape)
    shapes_data[shape_index]=dir_patterns

# Function to add the content of the file to the corresponding list
def add():
    file_path = filedialog.askopenfilename(initialdir=os.path, title="Select file", filetypes=(("Text files", "*.txt*"),))
    if not file_path:
        return

    file_name = os.path.basename(file_path)
    print(f"Selected file: {file_name}")

    if file_name == "structures.txt":
        strutture.clear()
        try:
            with open(file_path, "r") as f:
                strutture.extend(f.readlines())
            update_structure_labels()
            messagebox.showinfo("Success", f"Data has been loaded into 'structures'.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during loading: {e}")
    elif file_name == "directions.txt":
        direzioni.clear()
        try:
            with open(file_path, "r") as f:
                direzioni.extend(f.readlines())
            update_direction_labels()
            messagebox.showinfo("Success", f"Data has been loaded into 'directions'.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during loading: {e}")
    else:
        messagebox.showwarning("Warning", "The selected file is neither 'structures.txt' nor 'directions.txt'.")

def setup():
    global strutture, direzioni, struttura_bool, direzione_bool, once, langvalue, translations, RepeatSwitch, checkbox, EditButton, edit

    def switch_to_checkbox(column, row, text, variable):
        for widget in mainframe.winfo_children():
            if isinstance(widget, CTkLabel) and widget.winfo_ismapped():
                info = widget.grid_info()
                if info["column"] == column and info["row"] == row:
                    widget.grid_forget()
        checkbox = customtkinter.CTkCheckBox(mainframe, text=text, variable=variable, onvalue=True, offvalue=False, font=('Helvetica', 14))
        checkbox.grid(column=column, row=row, sticky=N, padx=5, pady=5)

    if strutture:
        switch_to_checkbox(3, 1, translations[langvalue]["Structures"], struttura_bool)
    if direzioni:
        switch_to_checkbox(2, 1, translations[langvalue]["Directions"], direzione_bool)
    if strutture or direzioni:
        CTkSwitch(mainframe, text=translations[langvalue]["Repeat"], variable=once, onvalue=True, offvalue=False, font=('Helvetica', 14)).grid(column=1, row=7, sticky=customtkinter.W, padx=5, pady=5)
        #EditButton=CTkButton(mainframe, text=translations[langvalue]["Edit"], font=('Helvetica', 14), command=updatetextboxes)
        TxTBoxSwitch = CTkSwitch(mainframe, text=translations[langvalue]["Edit"], variable=textbox, onvalue=True, offvalue=False, font=('Helvetica', 14), command=updatetextboxes)
        TxTBoxSwitch.grid(column=1, row=8, sticky=customtkinter.W, padx=5, pady=5)
        #edit = customtkinter.BooleanVar(value=False)
        #EditButton.grid(column=1, row=8, sticky=customtkinter.W, padx=5, pady=5)
    turtle.home()    
def updatetextboxes(value=None):
    #global edit  # Aggiungi questa linea per dichiarare edit come variabile globale

    #TxTBoxSwitch = CTkSwitch(mainframe, text=translations[langvalue]["Edit"], variable=textbox, onvalue=True, offvalue=False, font=('Helvetica', 14))
    
    if not textbox.get():  # Usa textbox.get() per leggere il valore
        print("editing")
        listbox_strutture.configure(state="normal")
        listbox_direzioni.configure(state="normal")
    else:
        print("disabled")
        listbox_strutture.configure(state="disabled")
        listbox_direzioni.configure(state="disabled")

def rollback():
    global folder_name, loaded, Output, turns, structure_bool, direction_bool, once, program, rules
    loaded = False
    turns = False
    strutture.clear()
    direzioni.clear()
    direzione_entry.delete(0, END)
    struttura_entry.delete(0, END)
    scenery_name=""
    programma.clear()
    if programma:
        update_rule_label()
    else:
        update_scenery()
    update_direction_labels()
    update_structure_labels()

    programma.clear()
    folder_name = ""
    
    for widget in mainframe.winfo_children():
        if isinstance(widget, CTkLabel) and widget.winfo_ismapped():
            info = widget.grid_info()
            if info["column"] == 4 and info["row"] == 4:
                widget.grid_forget()
    for widget in mainframe.winfo_children():
        if isinstance(widget, CTkSwitch) and widget.winfo_ismapped():
            info = widget.grid_info()
            if info["column"] == 1 and info["row"] == 7:
                widget.grid_forget()
                
    def switch_to_label(column, row, text, variable):
        for widget in mainframe.winfo_children():
            if isinstance(widget, CTkCheckBox) and widget.winfo_ismapped():
                info = widget.grid_info()
                if info["column"] == column and info["row"] == row:
                    widget.grid_forget()
        checkbox = customtkinter.CTkLabel(mainframe, text=text, font=('Helvetica', 14))
        checkbox.grid(column=column, row=row, sticky=N, padx=5, pady=5)
        
    switch_to_label(3, 1, translations[langvalue]["Structures"], struttura_bool)
    switch_to_label(2, 1, translations[langvalue]["Directions"], direzione_bool)
                
    if Outputs:
        OutputList.grid_forget()

def update_combobox1(*args):
    if type1.get() == "direction":
        Combo1.configure(values=direzioni)
    elif type1.get() == "structure":
        Combo1.configure(values=strutture)
    Combo1.set("Select")

def update_combobox2(*args):
    if type2.get() == "direction":
        Combo2.configure(values=direzioni)
    elif type2.get() == "structure":
        Combo2.configure(values=strutture)
    Combo2.set("Select")
    
def program():
    global program_window, Combo1, Combo2, Combo3, programma, type1, type2, rules
    program_window = CTkToplevel(root)
    program_window.title("Program")
    program_window.lift()  # Bring the window to the front
    program_window.focus_force()  # Force focus on the window
    programming = True
    
    CTkLabel(program_window, text="if").grid(column=1, row=1, sticky=(W, E))
    CTkLabel(program_window, text="then").grid(column=1, row=4, sticky=(W, E))

    type1 = StringVar()
    type1.trace("w", update_combobox1)  # Trace the variable to update combobox dynamically
    
    
    typebutton1 = CTkRadioButton(program_window, text=translations[langvalue]["Direction"], variable=type1, value="direction")
    typebutton1.grid(column=1, row=2, sticky=(W, E))
    typebutton2 = CTkRadioButton(program_window, text=translations[langvalue]["Structure"], variable=type1, value="structure")
    typebutton2.grid(column=1, row=3, sticky=(W, E))
    type2 = StringVar()
    type2.trace("w", update_combobox2)  # Trace the variable to update combobox dynamically

    typebutton3 = CTkRadioButton(program_window, text=translations[langvalue]["Direction"], variable=type2, value="direction")
    typebutton3.grid(column=1, row=6, sticky=(W, E))
    typebutton4 = CTkRadioButton(program_window, text=translations[langvalue]["Structure"], variable=type2, value="structure")
    typebutton4.grid(column=1, row=7, sticky=(W, E))

    # Scelte per elemento1
    Combo1 = CTkComboBox(program_window, state='readonly')  # Set combobox to read-only
    Combo1.grid(column=2, row=2, sticky=(W, E))

    # Scelte per elemento2
    Combo2 = CTkComboBox(program_window, state='readonly')  # Set combobox to read-only
    Combo2.grid(column=2, row=6, sticky=(W, E))

    # Scelte per elimina/salta
    Combo3 = CTkComboBox(program_window, state='readonly')
    Combo3.grid(column=2, row=4, sticky=(W, E))
    Combo3.configure(values=[translations[langvalue]["deletes"], translations[langvalue]["skips"]])  # Opzioni "elimina" o "salta"
    Combo3.set("Select")
    if programma:
        Rules=CTkTextbox(program_window, height=len(programma)*22, width=100, font=('Helvetica', 14), state="normal", border_width=3)
        Rules.grid(column=3, row=1, rowspan=len(programma)+1,  columnspan=1, sticky=(W, E))
        print(len(programma)+1)
        Rules.grid_propagate("False")
        for instruction in programma:
            Rules.insert("end", "● " + f"{instruction[0].strip()} {instruction[1]} {instruction[2].strip()}\n")

    # Pulsante per aggiungere nuove istruzioni
    addbutt=CTkButton(program_window, text=translations[langvalue]["Add"], command=add_instruction).grid(column=4, row=1, sticky=(W, E))
    delbutt=CTkButton(program_window, text=translations[langvalue]["Delete"], command=delete_instruction).grid(column=4, row=2, sticky=(W, E))


    # Pulsanti per salvare, caricare ed eseguire il programma
    CTkButton(program_window, text=translations[langvalue]["Save"], command=saveprogram).grid(column=2, row=8, sticky=(W, E))
    CTkButton(program_window, text=translations[langvalue]["Load"], command=loadprogram).grid(column=3, row=8, sticky=(W, E))
    CTkButton(program_window, text=translations[langvalue]["Execute"], command=execute).grid(column=4, row=8, sticky=(W, E))

    program_window.after(10, lambda: program_window.focus())  # Ensure the window is focused after it's fully initialized
    print(programming)

# Funzione per aggiungere un'istruzione come tupla
def add_instruction():
    global programma, Combo1, Combo2, Combo3
    instruction = (Combo1.get(), Combo3.get(), Combo2.get())  # Crea una tupla con (elemento1, azione, elemento2)
    programma.append(instruction)
    print("Istruzione aggiunta:", instruction)
    update_program_window()
    
# Funzione per eseguire il programma
def execute():
    global programma
    print("Programma eseguito:", programma)
    update_rule_label()
    
# Funzione per salvare il programma
def saveprogram():
    global folder_name, programma
    if not folder_name:
        folder_name = folderwindow()

    program_file = os.path.join(folder_name, "program.txt")
    with open(program_file, "w") as f:
        for instruction in programma:
            f.write(str(instruction) + "\n")  # Scrivi ogni tupla su una nuova riga
        messagebox.showinfo("Success", "salvataggio completato.")
    execute()

# Funzione per caricare il programma
def loadprogram():
    global programma
    folder_name = filedialog.askdirectory(initialdir=os.path, title="Select file")
    program_file = os.path.join(folder_name, "program.txt")
    with open(program_file, "r") as f:
        for line in f:
            programma.append(eval(line.strip()))  # Converti le stringhe in tuple
        print("Programma caricato:", programma)
    update_program_window()
    execute()

# Funzione per aggiornare l'etichetta delle regole
def update_rule_label():
    global programma
    Scenery.destroy()
    update_scenery()
    Scenery.configure(state="normal", width=100)
    Scenery.grid(rowspan=len(programma)+1)
    for instruction in programma:
        Scenery.insert("end","\n" + f"{instruction[0].strip()} {instruction[1]} {instruction[2].strip()}")
    Scenery.configure(state="disabled")
    programming = False
    program_window.destroy()
    
def update_program_window():
    program_window.destroy()
    program()
    
# Funzione per cancellare le istruzioni
def delete_instruction():
    global delete_instruction_window, selected_delete
    selected_delete=[]
    delete_instruction_window = customtkinter.CTkToplevel(root)
    delete_instruction_window.title("Delete values")
    delete_instruction_window.lift()
    delete_instruction_window.focus_force()

    for i, instruction in enumerate(programma):
        delete_var = BooleanVar()
        delete_checkbox = customtkinter.CTkCheckBox(delete_instruction_window, text=f"{instruction[0].strip()} {instruction[1]} {instruction[2].strip()}", variable=delete_var)
        delete_checkbox.grid(row=i, column=1, sticky="e")
        selected_delete.append(delete_var)


    confirm_button = customtkinter.CTkButton(delete_instruction_window, text="Confirm deletion", command=confirm_instruction_deletion)
    confirm_button.grid(row=len(direzioni) + 1, column=0, columnspan=4)
    delete_instruction_window.after(10, lambda: delete_instruction_window.focus())

# Funzione per confermare la cancellazione delle istruzioni
def confirm_instruction_deletion():
    global delete_window, selectedS_delete, selectedD_delete
    updated_programma = [programma[i] for i, var in enumerate(selected_delete) if not var.get()]
    programma.clear()
    programma.extend(updated_programma)
    update_program_window()
    delete_instruction_window.destroy()

# Funzione per cancellare i valori delle liste
def delete():
    global delete_window
    delete_window = customtkinter.CTkToplevel(root)
    delete_window.title("Delete values")
    delete_window.lift()  # Bring the window to the front
    delete_window.focus_force()  # Force focus on the window

    for i, x in enumerate(direzioni):
        delete_var_d = BooleanVar()
        delete_checkbox_d = customtkinter.CTkCheckBox(delete_window, text=x, variable=delete_var_d)
        delete_checkbox_d.grid(row=i, column=1, sticky="e")
        selectedD_delete.append(delete_var_d)

    for i, x in enumerate(strutture):
        delete_var_s = BooleanVar()
        delete_checkbox_s = customtkinter.CTkCheckBox(delete_window, text=x, variable=delete_var_s)
        delete_checkbox_s.grid(row=i, column=3, sticky="e")
        selectedS_delete.append(delete_var_s)

    confirm_button = customtkinter.CTkButton(delete_window, text="Confirm deletion", command=confirm_deletion)
    confirm_button.grid(row=len(direzioni) + 1, column=0, columnspan=4)
    
    delete_window.after(10, lambda: delete_window.focus())

# Funzione per confermare la cancellazione dei valori
def confirm_deletion():
    global delete_window, selectedS_delete, selectedD_delete
    updated_direzioni = [direzioni[i] for i, var in enumerate(selectedD_delete) if not var.get()]
    updated_strutture = [strutture[i] for i, var in enumerate(selectedS_delete) if not var.get()]

    direzioni.clear()
    direzioni.extend(updated_direzioni)
    strutture.clear()
    strutture.extend(updated_strutture)

    update_direction_labels()
    update_structure_labels()

    selectedD_delete.clear()
    selectedS_delete.clear()

    delete_window.destroy()

# Funzione per cancellare singolarmente un elemento
def deletesingle():
    global random_direzione, random_struttura
    if random_direzione in direzioni:
        direzioni.remove(random_direzione)
    update_direction_labels()
    if random_struttura in strutture:
        strutture.remove(random_struttura)
    update_structure_labels()

# Funzione per cancellare l'elemento selezionato
def deleteselected(value):
    global struttura, direzioni, type2, programma
    print("tryin'")
    print(value)
    for i in direzioni:
        if value==i:
            print("workin'")
            direzioni.remove(value)
            update_direction_labels()
    for i in strutture:
        if value==i:
            print("workin'")
            strutture.remove(value)
            update_structure_labels()

# Funzione per generare la mappa
def generate(offsets=[0,0]):
    #random.seed(time.gmtime)

    global turns, Outputs, selectedD, selectedS, random_direzione, random_struttura, programma, type1, type2, direzioni, strutture, OutputList

    for widget in mainframe.winfo_children():
        if isinstance(widget, customtkinter.CTkCheckBox) and widget.winfo_ismapped():
            info = widget.grid_info()
            if info["column"] == 4:
                widget.grid_forget()

    if strutture:
        random_struttura = random.choice(strutture)
    else:
        random_struttura = "\n"
    if direzioni:
        random_direzione = random.choice(direzioni)
        direzione_index=direzioni.index(random_direzione)
        print("params",params)
        if params:
            Fullfilled=roation_check(direzioni.index(random_direzione), params)
            while not Fullfilled:
                print("direzione non trovata, ruotazione in corso...")
                random_direzione = random.choice(direzioni)
                Fullfilled=roation_check(direzioni.index(random_direzione), params)
        #elif not first_time:
            
        shape = shapes[direzione_index]
        data = shapes_data[direzione_index]
        data.remove(invert_mat(chosen_dir, dir_mat))
        

    else:
        random_direzione = "\n"
 
    if not once.get():
        deletesingle()
    if programma:
        for i in programma:
            if i[0] == random_direzione or i[0] == random_struttura:
                print("triggered")
                if i[1] == "deletes":
                    print("elimina funziona")
                    deleteselected(i[2])
                if i[1] == "skips": #and (programma[0] == random_direzione.strip() or programma[0] == random_struttura.strip()):
                    print("salta funziona")
                    if i[2] == random_direzione:
                        while i[2] == random_direzione:
                            random_direzione = random.choice(direzioni)
                            print("skips")
                            messagebox.showinfo("skipped")
                            break
                    elif i[2] == random_struttura:
                        while i[2] == random_struttura:
                            random_struttura = random.choice(strutture)
                            print("skip")
                            messagebox.showinfo("skipped")
                            break
    if Outputs:
        prev_dir_index = direzioni.index(Outputs[len(Outputs) - 1][0]+"\n")
    else:
        prev_dir_index = 0
    Outputs.append(random_direzione+random_struttura)
   
    update_output_list()
    if turns:
        turnupdate()
    #draw_shape_for_direction(direzioni.index(random_direzione), prev_dir_index, offsets, chosen_dir, prev_pos)
    print("first time")
    draw_shape_for_direction(shape, data, offsets)



def roation_check(direzione_index, params):
    print("roation check")
    required_dirs=params[0]
    unrequired_dirs=params[1]
    shape = shapes[direzione_index]
    Fullfilled= False
    for i in range(4):
        req=0
        for l in shapes_data[direzione_index]:
            if  l in required_dirs or l not in unrequired_dirs:
                req+=1
                
        if req == len(required_dirs)+len(unrequired_dirs):
            Fullfilled=True
            break
        else:
            print("direzione non trovata, ruotazione in corso...")
            shape = rotate(shape)
            shape_check(shape, direzione_index)
    shapes[direzione_index] = shape
    for i in shapes[direzione_index]:
        print(i)
    shapes_data[direzione_index] = cont_check(shape)
    print("direzione trovata:", shapes_data[direzione_index])
    return Fullfilled
        

def draw_shape_for_direction(shape, data, offsets, cell_size=10):
    #global offset_x, offset_y
    global first_time
    if offsets is None:
        offsets = [0, 0]
    print("offsets:", offsets)
    first_time= False
    turtle.speed(0)
    offset_x, offset_y = 0, 0

    offset_x=int(offsets[0])*cell_size
    offset_y=int(offsets[1])*cell_size
    print("Disegno figura con offset:", offset_x, offset_y)
    # Sposta la figura
    turtle.penup()
    """    if offset_x==0 and offset_y == 0 and prev_shape:
        offsets=direct_set_direction_offset(chosen_dir)
        offset_x, offset_y = offsets[0], offsets[1]"""
    start_x, start_y = turtle.xcor() + offset_x, turtle.ycor() + offset_y
    
    for row_idx, row in enumerate(shape):
        for col_idx, cell in enumerate(row):
            if cell == "1":
                x = start_x + col_idx * cell_size
                y = start_y - row_idx * cell_size
                turtle.goto(x, y)
                turtle.pendown()
                turtle.begin_fill()
                for _ in range(4):
                    turtle.forward(cell_size)
                    turtle.right(90)
                turtle.end_fill()
                turtle.penup()
    turtle.goto(start_x, start_y)
    turtle.setheading(0)
    directions_window(shape, data, offsets)

def rotate(shape):
    """
    Ruota la figura di 90 gradi in senso orario.
    """
    print("Rotating shape")
    rotated_shape = []
    num_cols = len(shape[0])
    for col in range(num_cols):
        new_row = ""
        for row in reversed(shape):
            new_row += row[col]
        rotated_shape.append(new_row)
    for i in rotated_shape:
        print(i)
    return rotated_shape

def invert_mat(element, mat):
    """
    Inverte l'elemento nella matrice se è presente.
    """
    for i in range(len(mat)):
        if element in mat[i]:
            return mat[i][mat[i].index(element)-1]
    print("Elemento non trovato nella matrice:", element)

def cont_check(shape):
    draw_all= False
    dir_patterns=[]
    num_rows = len(shape)
    num_cols = len(shape[0])
    col_pattern_l = ""
    col_pattern_r = ""
    if shape[0] == "010010":
        #upper_pattern=True
        dir_patterns.append("upper")
        #offset_y= num_rows*cell_size   # Sposta verso l'alto di 5 celle
    # Cerca pattern riga inferiore
    if shape[num_cols-1] == "010010":
        #lower_pattern=True
        dir_patterns.append("lower")
        #offset_y= -num_rows*cell_size   # Sposta verso l'alto di 5 celle
    # Cerca pattern colonna sinistro e destro    
    for row in range(num_rows):
        col_pattern_l += (shape[row][0])
        col_pattern_r += (shape[row][num_cols-1])
        #print("col pattern: ",col_pattern_l)
    if col_pattern_l == "010010":
        #left_pattern=True
        dir_patterns.append("left")
        #offset_x = -num_cols*cell_size  # Sposta verso destra di 5 celle
    if col_pattern_r == "010010":
        #right_pattern=True
        dir_patterns.append("right")
        #offset_x = num_cols*cell_size  # Sposta verso destra di 5 celle"""
    """if dir_patterns:
        draw_all = True"""
    print("Pattern trovato:", dir_patterns)
    return dir_patterns
"""
def cont_check_pattern(patterns, pattern):
    if pattern == "upper":
        
    return offset_x, offset_y"""

def  directions_window(shape, dir_patterns, prev_pos):
    genbutt.configure(state="disabled")  # Disabilita il pulsante di generazione
    dir_window = CTkToplevel(root)
    dir_window.title("Choose a direction")
    dir_window.lift()  # Bring the window to the front
    dir_window.focus_force()  # Force focus on the window
    print(dir_patterns)
    for pattern in dir_patterns:
        button = CTkButton(dir_window, text=pattern)
        button.pack(pady=5)
        if pattern == "upper":
            button.configure(command=lambda: set_direction_offset([0, len(shapes[0])], dir_window, "upper", dir_patterns, prev_pos, shape))
            #button.configure(command=lambda: set_direction_offset([len(shapes[0]), 0], dir_window, "upper"))
        elif pattern == "lower":
            button.configure(command=lambda: set_direction_offset([0, -len(shapes[0])], dir_window, "lower", dir_patterns, prev_pos, shape))
            #button.configure(command=lambda: set_direction_offset([-len(shapes[0]), 0], dir_window, "lower"))
        elif pattern == "left":
            button.configure(command=lambda: set_direction_offset([-len(shapes[0]), 0], dir_window, "left", dir_patterns, prev_pos, shape))
            #button.configure(command=lambda: set_direction_offset([0, -len(shapes[0])], dir_window, "left"))
        elif pattern == "right":
            button.configure(command=lambda: set_direction_offset([len(shapes[0]), 0], dir_window, "right", dir_patterns, prev_pos, shape))
            #button.configure(command=lambda: set_direction_offset([0, len(shapes[0])], dir_window, "right"))


def set_direction_offset(offsets, window, chos_dir, dir_patterns, prev_pos, shape):
    #global offset_x, offset_y
    global params
    """
    Imposta l'offset di direzione in base alla lista di due interi fornita.
    offsets: lista di due interi [offset_x, offset_y]
    """
    if not isinstance(offsets, list) or len(offsets) != 2 or not all(isinstance(x, int) for x in offsets):
        raise ValueError("L'argomento deve essere una lista di due interi.")
    # Qui puoi implementare la logica per usare questi offset, ad esempio:
    chosen_dir = chos_dir
    x=prev_pos[0] + offsets[0]//len(shapes[0])
    y=prev_pos[1] + offsets[1]//len(shapes[0])
    Map_Matrix[x][y] = dir_patterns  # Aggiorna la matrice della mappa con la direzione scelta
    required_dirs= [invert_mat(chosen_dir, dir_mat)]
    unrequired_dirs=[]
    for i in range(-1,2):
        if i==0 or i==-offsets[0]/6 or i==-offsets[1]/6:
            continue
        if Map_Matrix[x+i][y] != []:
            if dir_mat[0][i-1] in dir_patterns:
                required_dirs.append(invert_mat(dir_mat[0][i-1], dir_mat))
            else:
                unrequired_dirs.append(invert_mat(dir_mat[0][i-1], dir_mat))
        if Map_Matrix[x][y+i] != []:
            if dir_mat[1][i-1] in dir_patterns:
                required_dirs.append(invert_mat(dir_mat[1][i-1], dir_mat))
            else:
                unrequired_dirs.append(invert_mat(dir_mat[1][i-1], dir_mat))
    params=[required_dirs, unrequired_dirs]
    print("params:", params)
    prev_pos=[x, y]
    #global offset_x, offset_y
    #offset_x, offset_y = offsets[0], offsets[1]
    window.destroy()  # Chiude la finestra delle direzioni

    print(f"Offset impostato a: x={offsets[0]}, y={offsets[1]}")
    #genbutt.configure(state="normal")
    generate(offsets)  # Chiama la funzione di generazione della mappa con i nuovi offset
    
def direct_set_direction_offset(chosen_dir):
    offsets=[]
    print("chosen_dir:", chosen_dir)
    if chosen_dir == "upper":
            offsets=[0, len(shapes[0])]
            #button.configure(command=lambda: set_direction_offset([len(shapes[0]), 0], dir_window, "upper"))
    elif chosen_dir == "lower":
        offsets=[0, -len(shapes[0])]
        #button.configure(command=lambda: set_direction_offset([-len(shapes[0]), 0], dir_window, "lower"))
    elif chosen_dir == "left":
        offsets=[-len(shapes[0]), 0]
        #button.configure(command=lambda: set_direction_offset([0, -len(shapes[0])], dir_window, "left"))
    elif chosen_dir == "right":
        offsets=[len(shapes[0]), 0]
        #button.configure(command=lambda: set_direction_offset([0, len(shapes[0])], dir_window, "right"))
    # Qui puoi implementare la logica per usare questi offset, ad esempio:
    return offsets

def update_output_list():
    global turns, turn_var, OutputList
    OutputList = CTkTextbox(mainframe, height=50, width=50, font=('Helvetica', 14), state="normal", border_width=3)
    OutputList.grid(column=1, row=4, sticky='WENS')
    OutputList.grid_propagate(False)
    if Outputs:
        OutputList.insert("0.0","Direzione: " + random_direzione)
        OutputList.insert("1.0","Struttura: " + random_struttura)
    if turn_var:
        OutputList.insert("3.0","Turni: " + str(turn_var))
    OutputList.configure(state="disabled")
    
# Funzione per aggiungere una direzione
def append():
    direzioni.append(direzione_entry.get() + "\n")
    update_direction_labels()
    setup()
    direzione_entry.delete(0, 'end')

# Funzione per aggiornare le direzioni usando una Listbox con scrollbar
def update_direction_labels():
    global direzione_bool, direzioni_button, listbox_direzioni, myscrollD
    
    for widget in mainframe.winfo_children():
        if isinstance(widget, CTkTextbox) and widget.winfo_ismapped():
            info = widget.grid_info()
            if info["column"] == 2 and info["row"] == 7:
                widget.grid_forget()
    
    listbox_direzioni = CTkTextbox(mainframe, state="normal", border_width=3, font=('Helvetica', 14))
    #listbox_direzioni.configure( border_color=("#126af0", "green"))
    listbox_direzioni.grid(column=2, row=7, rowspan=8, sticky='WENS')
    
    for i, x in enumerate(direzioni):
        listbox_direzioni.insert('end', "● " + x)
    
    listbox_direzioni.configure(state="disabled")
    
    root.update()

# Funzione per aggiungere una struttura
def appens():
    strutture.append(struttura_entry.get() + "\n")
    update_structure_labels()
    setup()
    struttura_entry.delete(0, 'end')

# Funzione per aggiornare le strutture usando una Listbox con scrollbar
def update_structure_labels():
    global struttura_bool, strutture_button, listbox_strutture, myscrollS
    
    # Rimuove la Listbox e la Scrollbar esistenti se presenti
    for widget in mainframe.winfo_children():
        if isinstance(widget, CTkTextbox) and widget.winfo_ismapped():
            info = widget.grid_info()
            if info["column"] == 3 and info["row"] == 7:
                widget.grid_forget()
    
    # Crea una nuova Listbox
    listbox_strutture = CTkTextbox(mainframe, state="normal", border_width=3, font=('Helvetica', 14))
    #listbox_strutture.configure(border_color=("#126af0", "green"))
    
    # Posiziona la Scrollbar e la Listbox
    listbox_strutture.grid(column=3, row=7, rowspan=8, sticky='WENS')
    # myscrollS.grid(column=4, row=7, rowspan=10, sticky='NS')

    # Aggiunge gli elementi alla Listbox
    for i, x in enumerate(strutture):
        listbox_strutture.insert('end', "● " + x)
        
    listbox_strutture.configure(state="disabled")
    
    root.update()    

def update_scenery():
    global Scenery, scenery_name
    if loaded:
        scenery_name = os.path.basename(folder_name)
        #customtkinter.CTkLabel(mainframe, text=f"Scenery: {scenery_name}", font=('Helvetica', 14)).grid(column=4, row=11, columnspan=1, sticky=customtkinter.W)
        Scenery=CTkTextbox(mainframe, height=len(programma)*25, width=50, font=('Helvetica', 14), state="normal", border_width=3)
        Scenery.grid(column=4, row=4, rowspan=1, columnspan=1, sticky='WENS')
        Scenery.grid_propagate(False)
        Scenery.insert("0.0",translations[langvalue]["Scenery"]+": "+scenery_name)
        Scenery.configure(state="disabled")
    else:
        Scenery.grid_forget()

def turn():
    global turns, turn_var
    turns = True
    turnwindow()
    turn_var = turn_var + 1
    turnupdate()

def turnupdate():
    global turn_var
    if turns:
        if turn_var:
            turn_var = turn_var - 1
            #customtkinter.CTkLabel(mainframe, text=turn_var, font=('Helvetica', 14)).grid(column=1, row=2, columnspan=1, sticky=customtkinter.W)
            update_output_list()

def prints():
    global Outputs, folder_name
    i = 0
    print("printing")
    if not loaded:
        folder_name = filedialog.askdirectory(initialdir=os.path, title="Select file")
    else:
        folder_name = folder_name
    if not os.path.exists(folder_name):
        messagebox.showerror("Error", "The folder doesn't exist.")
        return

    file_path = os.path.join(folder_name, "map.txt")
    with open(file_path, "a") as f:
        for x in Outputs:
            print(x)
            i += 1
            f.write(str(i) + ")" + "\n" + x + "\n")
    messagebox.showinfo("Success", f"Data saved in {file_path}")

def autorun():
    global turn_var, once, strutture, direzioni
    if once.get():
        print("workin'")
        turnwindow()
        print(turn_var)
        if turn_var > 0:
            for i in range(turn_var):
                generate()
            prints()
        
    if not once.get():
        print("workin'")
        a = len(strutture) - len(direzioni)
        print(a)
        if direzioni or strutture:
            if a >= 0:
                for i in range(len(strutture)):
                    generate()
            if a < 0:
                for i in range(len(direzioni)):
                    generate()
            prints()

def eliminate():
    global direzioni, strutture, struttura_bool, direzione_bool

    # Check if the checkbox for directions is selected
    if direzione_bool.get():
        direzioni.clear()  # Clear the contents of the directions list
        update_direction_labels()  # Update the direction labels
        # Remove the checkboxes for directions
        for widget in mainframe.winfo_children():
            if isinstance(widget, customtkinter.CTkCheckBox) and widget.winfo_ismapped():
                info = widget.grid_info()
                if info["column"] == 2 and info["row"] == 5:
                    widget.grid_forget()

    # Check if the checkbox for structures is selected
    if struttura_bool.get():
        strutture.clear()  # Clear the contents of the structures list
        update_structure_labels()  # Update the structure labels
        # Remove the checkboxes for structures
        for widget in mainframe.winfo_children():
            if isinstance(widget, customtkinter.CTkCheckBox) and widget.winfo_ismapped():
                info = widget.grid_info()
                if info["column"] == 3 and info["row"] == 5:
                    widget.grid_forget()
                    
def settingswindow():
    settings_window = CTkToplevel(root)
    settings_window.title("Program")
    settings_window.lift()  # Bring the window to the front
    settings_window.focus_force()  # Force focus on the window
    
    settingstabs = customtkinter.CTkTabview(settings_window)
    settingstabs.grid(column=1, row=1, sticky="WENS")
    settingstabs.add(translations[langvalue]["Language"])
    settingstabs.add(translations[langvalue]["Theme"])

    optionmenu = CTkOptionMenu(settingstabs.tab(translations[langvalue]["Theme"]), values=[translations[langvalue]["Light"], translations[langvalue]["Dark"]], command=set_theme)
    optionmenu.grid(column=1, row=2, columnspan=1, sticky=customtkinter.W)
    optionmenu.set(themevalue)
    CTkLabel(settingstabs.tab(translations[langvalue]["Theme"]), text=translations[langvalue]["Theme"]).grid(column=1, row=11, columnspan=1, sticky=customtkinter.W)
    langoptionmenu = CTkOptionMenu(settingstabs.tab(translations[langvalue]["Language"]), values=["Italiano", "English"], command=set_lang)
    langoptionmenu.grid(column=1, row=14, columnspan=1, sticky=customtkinter.W)
    langoptionmenu.set(langvalue)
    CTkLabel(settingstabs.tab(translations[langvalue]["Language"]), text=translations[langvalue]["Language"]).grid(column=1, row=13, columnspan=1, sticky=customtkinter.W)
    
    settings_window.after(10, lambda: settings_window.focus())  # Ensure the window is focused after it's fully initialized

def map_setup():
    # Prepara Map_Matrix come una matrice quadrata di dimensioni Map_Size x Map_Size
    for i in range(Map_Size):
        Map_Matrix.append(["Free"] * Map_Size)
    return Map_Size // 2
#, , , , , , 
def segmented_button_callback(value):
    if value == translations[langvalue]["Save"]:
        save()
    elif value == translations[langvalue]["New"]:
        create()
    elif value == translations[langvalue]["Load"]:
        load()
    elif value == translations[langvalue]["Add"]:
        add()
    elif value == translations[langvalue]["Delete"]:
        delete()
    elif value == translations[langvalue]["Print"]:
        prints()
    elif value == translations[langvalue]["Program"]:
        if loaded:
            program()
        else:
            messagebox.showerror("Load first")
    elif value == translations[langvalue]["Settings"]:
        settingswindow()
    elif value == translations[langvalue]["Reset"]:
        rollback()
    elif value==translations[langvalue]["Close"]:
        root.destroy()
    segmented_button.set(None)

# Initialize the main window
root = customtkinter.CTk()
root.title("Random Map Generator")
root.resizable(True, True)  # Allow the window to be resizable both horizontally and vertically

# Variabili
selectedD = []
selectedS = []
direzioni = []
strutture = []
shapes = []
shapes_data=[]
Outputs = []
Map_Matrix=[]
selectedD_delete = []
selectedS_delete = []
dir_mat=[["upper", "lower"], ["left", "right"]]
funzioni = ["eliminate", "skip"]
programma = []
prev_pos= [4, 0]  # Posizione iniziale
params=[]
turn_var = int()
Map_Size= 10
chosen_dir="upper"
Map_Center=map_setup()
once = customtkinter.BooleanVar(value=True)
"""offset_x=0
offset_y=0"""
editing = customtkinter.BooleanVar(value=True)
textbox = customtkinter.BooleanVar(value=True)
programming = customtkinter.BooleanVar(value=False)
direzione_bool = customtkinter.BooleanVar(value=False)
struttura_bool = customtkinter.BooleanVar(value=False)
turns = customtkinter.BooleanVar(value=False)
loaded = customtkinter.BooleanVar(value=False)
first_time=True
folder_window_open = customtkinter.BooleanVar()
turn_window_open = customtkinter.BooleanVar()
folder_name_var = customtkinter.StringVar()
aggiungi1 = customtkinter.IntVar()
aggiungi2 = customtkinter.IntVar()
deftheme="Dark"
deflang="english"


# Configurazione del layout principale
mainframe = customtkinter.CTkFrame(root)
mainframe.grid(column=0, row=0, sticky=(customtkinter.N, customtkinter.W, customtkinter.E, customtkinter.S))
mainframe.grid(column=0, row=0, sticky=(customtkinter.N, customtkinter.W, customtkinter.E, customtkinter.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=1)
mainframe.columnconfigure(2, weight=2)
mainframe.columnconfigure(3, weight=2)
mainframe.columnconfigure(4, weight=2)
mainframe.rowconfigure(0, weight=1)
mainframe.rowconfigure(1, weight=1)
mainframe.rowconfigure(2, weight=1)
mainframe.rowconfigure(3, weight=1)
mainframe.rowconfigure(4, weight=1)
langvalue="English"
set_theme("Dark")


#langoptionmenu.set("English")


# Imposta pesi per le colonne e righe per una ridimensionabilità ottimale
for i in range(4):
    mainframe.columnconfigure(i, weight=1)
for i in range(5):
    mainframe.rowconfigure(i, weight=1)

def on_enter(event):
    direzione_text = direzione_entry.get().strip()
    struttura_text = struttura_entry.get().strip()
    folder_text = folder_name_var.get().strip()

    if direzione_text and direzione_entry.focus_get():
        append()
    elif struttura_text and struttura_entry.focus_get():
        appens()
    elif folder_window_open.get():
        folder_window_open.set(False)
    elif turn_window_open.get():
        turn_window_open.set(False)
    elif textbox:
        widget_con_focus = mainframe.focus_get()
        if widget_con_focus == listbox_direzioni:
            print("direzioni")
            listbox_direzioni.insert("end", "● ")
        elif widget_con_focus == listbox_strutture:
            print("strutture")
            listbox_strutture.insert("end", "● ")
    else:
        generate()

def savebind(event):
    if programming:
        if program_window.focus_get():
            saveprogram()
    else:
        save()
def loadbind(event):
    if programming:
        loadprogram()
    else:
        load()

def createbind(event):
    if programming:
        create()
def addbind(event):
    if programming:
        if program_window.focus_get():
            add_instruction()
    else:
        add()
def deletebind(event):
    if programming:
        if program_window.focus_get():
            delete_instruction()
    else:
        delete()
def printbind(event):
    if programming:
        prints()
def programbind(event):
    if programming:
        program()
def resetbind(event):
    if programming:
        rollback()
def closebind(event):
    if programming:
        if program_window.focus_get():
            program_window.destroy()
    else:
        root.destroy()


root.bind("<s>", save)
root.bind("<l>", loadbind)
root.bind("<n>", createbind)
root.bind("<a>", addbind)
root.bind("<d>", deletebind)
root.bind("<Tab>", printbind)
root.bind("<p>", programbind)
root.bind("<r>", resetbind)
root.bind("<c>", closebind)

root.bind("<Return>", on_enter)
root.mainloop()
