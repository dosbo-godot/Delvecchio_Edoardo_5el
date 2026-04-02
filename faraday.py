import tkinter as tk
from tkinter import ttk
import json

GREY = '#e8e8e8'
LARGHEZZA_LATERALE = 300

class GestoreDialogo:
    def __init__(self) -> None:
        with open('diapositive.json', encoding='utf-8') as f:
            self.config_dialogo = json.load(f)
        self.esperimento = 'Scegli un esperimento!'
        self.index_diapositiva = 0
        self.diapositive : list[dict[str:str]]= self.config_dialogo[self.esperimento]
    
    def diapositivaSucc(self):
        if self.index_diapositiva < len(self.diapositive):
            self.index_diapositiva += 1
            self.svuotaRoot(self.root)
            self.caricaContenuto(self.root)
    
    def diapositivaPrec(self):
        if self.index_diapositiva < len(self.diapositive):
            self.index_diapositiva -= 1
            self.svuotaRoot(self.root)
            self.caricaContenuto(self.root)

    def cambioEsperimento(self, scelta : str):
        self.esperimento = scelta
        self.diapositive = self.config_dialogo[self.esperimento]
        self.index_diapositiva = 0
        self.svuotaRoot(self.root)
        self.caricaContenuto(self.root)

    def svuotaRoot(self, root):
        for widget in root.winfo_children():
            widget.destroy()
    
    def caricaContenuto(self, root : tk.Frame):
        self.root = root
        widgets = self.diapositive[self.index_diapositiva]
        root.columnconfigure(0, weight=1)
        for i in range(len(widgets)):
            root.rowconfigure(i, weight=1)
        i = 0
        for tipo_widget, configurazione in widgets.items():
            if tipo_widget[0] == 'L':
                widget = tk.Label(root, wraplength=LARGHEZZA_LATERALE-30, bg=GREY, **configurazione)
            elif tipo_widget[0] == 'S':
                widget = tk.Scale(root, bg=GREY, **configurazione)
            elif tipo_widget[0] == 'B':
                widget = tk.Button(root, bg=GREY, **configurazione)
            elif tipo_widget[0] == 'F':
                widget = tk.Frame(root, **configurazione)
            widget.grid(row = i, column = 0)
            i+=1

def caricaRadice() -> tk.Tk:
    radice = tk.Tk()
    radice.geometry('1100x700')

    # CONFIGURAZIONE RADICE
    radice.columnconfigure(0, weight=1) 
    #radice.rowconfigure(0, weight=1)
    radice.rowconfigure(1, weight=10)

    caricaFrameSuperiore(radice, radice)
    caricaFrameInferiore(radice, radice)

    return radice

def caricaFrameSuperiore(root, global_root : tk.Tk):
    frame_superiore = tk.Frame(root, bg=GREY)
    # CONFIGURAZIONE FRAME SUP
    frame_superiore.rowconfigure(0, weight=1)
    frame_superiore.grid(row=0, column=0, sticky='nsew')

    scelta  = tk.StringVar(root)
    scelta.set(gestore_dialogo.esperimento)
    opzioni = [f'{x}° Esperimento' for x in range(1,5)]
    menu = tk.OptionMenu(frame_superiore, scelta, *opzioni, command=gestore_dialogo.cambioEsperimento)
    menu.grid(row=0, column=0)

def caricaFrameInferiore(root, global_root):
    frame_inferiore = tk.Frame(root, bg=GREY)

    # CONFIGURAZIONE FRAME INF
    frame_inferiore.rowconfigure(0, weight=1)
    frame_inferiore.columnconfigure(0, weight=1)
    frame_inferiore.grid(row=1, column=0, sticky='nsew')

    caricaFrameLaterale(frame_inferiore, global_root)
    canvas = tk.Canvas(frame_inferiore, bg='white')

    canvas.grid(row=0, column=0, sticky='nsew')

def caricaFrameLaterale(root, global_root):  
    frame_laterale = tk.Frame(root, bg=GREY, width=LARGHEZZA_LATERALE)

    # CONFIGURAZIONE FRAME LATERALE
    frame_laterale.grid_propagate(False)
    frame_laterale.rowconfigure(0, weight=1)
    frame_laterale.rowconfigure(1, weight=0)
    frame_laterale.columnconfigure(0, weight=1)

    frame_laterale.grid(row=0, column =1, sticky='nsew')

    caricaFrameDialogo(frame_laterale, global_root)
    caricaFrameNavigazione(frame_laterale, global_root)

def caricaFrameDialogo(root, global_root):
    frame_dialogo = tk.Frame(root, bg=GREY)
    # CONFIGURAZIONE FRAME DIALOGO, NAVIG
    frame_dialogo.columnconfigure(0, weight=1)

    frame_dialogo.grid(row=0, column=0, sticky='nswe')

    gestore_dialogo.caricaContenuto(frame_dialogo)


def caricaFrameNavigazione(root, global_root):
    frame_navigazione = tk.Frame(root, bg=GREY)

    frame_navigazione.columnconfigure(0, weight=1)
    frame_navigazione.columnconfigure(1, weight=1)
    frame_navigazione.columnconfigure(2, weight=1)
    frame_navigazione.rowconfigure(0, weight=1)

    frame_navigazione.grid(row=1, column=0, sticky='nswe')

    bottone_sx = tk.Button(frame_navigazione, bg = GREY, text='<', command=gestore_dialogo.diapositivaPrec)
    bottone_dx = tk.Button(frame_navigazione, bg = GREY, text='>', command=gestore_dialogo.diapositivaSucc)

      
    diapositiva = tk.StringVar(global_root)
    diapositiva.set(f'{gestore_dialogo.index_diapositiva+1}/{len(gestore_dialogo.diapositive)}')
    contatore_diapositive = tk.Label(frame_navigazione, textvariable=diapositiva, bg=GREY) # DOVREBBE ENTRARE IN COMUNICAZIONE CON CLASSE

    bottone_sx.grid(row=0, column=0, sticky='nswe')
    contatore_diapositive.grid(row=0, column=1, sticky='nswe')
    bottone_dx.grid(row=0, column=2, sticky='nswe')

gestore_dialogo = GestoreDialogo()
main = caricaRadice()
main.mainloop()