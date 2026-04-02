import tkinter as tk
from tkinter import ttk
import json

GREY = '#e8e8e8'

def cambioEsperimento(scelta):
    esperimento = config_dialogo[scelta]

def caricaRadice():
    radice = tk.Tk()
    radice.geometry('1100x700')

    # CONFIGURAZIONE RADICE
    radice.columnconfigure(0, weight=1) 
    #radice.rowconfigure(0, weight=1)
    radice.rowconfigure(1, weight=10)

    caricaFrameSuperiore(radice, radice)
    caricaFrameInferiore(radice, radice)

    return radice

def caricaFrameSuperiore(root, global_root):
    frame_superiore = tk.Frame(root, bg=GREY)
    # CONFIGURAZIONE FRAME SUP
    frame_superiore.rowconfigure(0, weight=1)
    frame_superiore.grid(row=0, column=0, sticky='nsew')

    scelta  = tk.StringVar(root)
    scelta.set('Scegli un esperimento!')
    opzioni = [f'{x}° Esperimento' for x in range(1,5)]
    menu = tk.OptionMenu(frame_superiore, scelta, *opzioni, command=cambioEsperimento)
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
    LARGHEZZA_LATERALE = 250   
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

    caricaContenutoDialogo(frame_dialogo, global_root)

def caricaContenutoDialogo(root, global_root): pass


def caricaFrameNavigazione(root, global_root):
    def avanti():
        diapositiva.set()

    def indietro():
        diapositiva.set()

    frame_navigazione = tk.Frame(root, bg=GREY)

    frame_navigazione.columnconfigure(0, weight=1)
    frame_navigazione.columnconfigure(1, weight=1)
    frame_navigazione.columnconfigure(2, weight=1)
    frame_navigazione.rowconfigure(0, weight=1)

    frame_navigazione.grid(row=1, column=0, sticky='nswe')

    bottone_sx = tk.Button(frame_navigazione, bg = GREY, text='<', command=avanti)
    bottone_dx = tk.Button(frame_navigazione, bg = GREY, text='>', command=indietro)

      
    diapositiva = tk.StringVar(global_root)
    diapositiva.set(f'{index_dialogo+1}')
    contatore_diapositive = tk.Label(frame_navigazione, textvariable=diapositiva, bg=GREY)

    bottone_sx.grid(row=0, column=0, sticky='nswe')
    contatore_diapositive.grid(row=0, column=1, sticky='nswe')
    bottone_dx.grid(row=0, column=2, sticky='nswe')

with open('diapositive.json') as f:
    config_dialogo = json.load(f)
index_dialogo = 0
main = caricaRadice()
main.mainloop()