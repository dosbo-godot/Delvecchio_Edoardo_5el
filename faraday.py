import tkinter as tk
from tkinter import ttk
import json
import random
import math

GREY = '#e8e8e8'
LARGHEZZA_LATERALE = 300
PI = 3.1415

class GestoreCanvas:
    def __init__(self):
        self.canvas : tk.Canvas = None

        # PARAMETRI GENERICI
        self.delta_potenziale = 0
        self.resistenza = 0
        self.corrente_potenziale = 0
        self.corrente = -100
        self.corrente_max = 100
        self.corrente_indotta = 0
        self.fps = 10
        self.delta = 1000//self.fps
        # PARAMETRI 1°
        # PARAMETRI 2°
        # PARAMETRI 3°
        # PARAMETRI 4°
        # PARAMETRI 5°

 
    def disegna(self):
        x = random.randint(0, 400)
        self.canvas.create_oval(x+20, x+20,x-20,x-20, fill='red')

    # 150x180
    def disegnaGalvanometro(self):
        larghezza = self.canvas.winfo_width()
        LARGHEZZA_GALVANOMETRO = 180
        ALTEZZA_GALVANOMETRO = 150
        RAGGIO = 113

        PADX = 10
        PADY = 10
        
        XCENTRO = larghezza-100
        YCENTRO = 146
        #RAD_INIZIO = 0.66 + PI
        RAD_INIZIO = PI*(3/2)
        self.img = tk.PhotoImage(file='galvanometroMK2.gif')
        self.canvas.create_image(larghezza-(LARGHEZZA_GALVANOMETRO//2) - PADX, ALTEZZA_GALVANOMETRO//2 + PADY, image = self.img)
        
        alfa = (RAD_INIZIO + ((0.91*self.corrente)/self.corrente_max))

        x = math.cos(alfa)*RAGGIO
        y = math.sin(alfa)*RAGGIO
        
        self.canvas.create_line(XCENTRO, YCENTRO, XCENTRO+x, YCENTRO+y, fill='red', width=4)


    def disegnaPrimo(self):
        self.canvas.delete('all')

        x = random.randint(0, 400)
        self.canvas.create_oval(x+20, x+20,x-20,x-20, fill='grey')
        
        self.disegnaGalvanometro()
        if gestore_dialogo.esperimento == '1° Esperimento':
            self.canvas.after(1000//self.fps, self.disegnaPrimo)
        else: return 0

    def disegnaSecondo(self):
        self.canvas.delete('all')

        x = random.randint(0, 400)
        self.canvas.create_oval(x+20, x+20,x-20,x-20, fill='yellow')
        if gestore_dialogo.esperimento == '2° Esperimento':
            self.canvas.after(self.delta, self.disegnaSecondo)
        else: return 0

    def disegnaTerzo(self):
        self.canvas.delete('all')

        x = random.randint(0, 400)
        self.canvas.create_oval(x+20, x+20,x-20,x-20, fill='blue')
        if gestore_dialogo.esperimento == '3° Esperimento':
            self.canvas.after(self.delta, self.disegnaTerzo)
        else: return 0

    def disegnaQuarto(self):
        self.canvas.delete('all')

        x = random.randint(0, 400)
        self.canvas.create_oval(x+20, x+20,x-20,x-20, fill='black')
        if gestore_dialogo.esperimento == '4° Esperimento':
            self.canvas.after(self.delta, self.disegnaQuarto)
        else: return 0

    def disegnaQuinto(self):
        self.canvas.delete('all')

        x = random.randint(0, 400)
        self.canvas.create_oval(x+20, x+20,x-20,x-20, fill='green')
        if gestore_dialogo.esperimento == '5° Esperimento':
            self.canvas.after(self.delta, self.disegnaQuinto)
        else: return 0

class GestoreDialogo:
    def __init__(self) -> None:
        with open('diapositive.json', encoding='utf-8') as f:
            self.config_dialogo = json.load(f)
        self.esperimento = 'Scegli un esperimento!'
        self.index_diapositiva = 0
        self.diapositive : list[dict[str:str]]= self.config_dialogo[self.esperimento]
    
    def diapositivaSucc(self) -> None:
        if self.index_diapositiva < len(self.diapositive)-1:
            self.index_diapositiva += 1
            self.aggiornaContoDiapositiva()

            self.svuotaRoot(self.root)
            self.caricaContenuto(self.root)

    
    def diapositivaPrec(self) -> None:
        if self.index_diapositiva != 0:
            self.index_diapositiva -= 1
            self.aggiornaContoDiapositiva()

            self.svuotaRoot(self.root)
            self.caricaContenuto(self.root)

    def cambioEsperimento(self, scelta : str):
        self.esperimento = scelta
        self.diapositive = self.config_dialogo[self.esperimento]
        self.index_diapositiva = 0
        self.aggiornaContoDiapositiva()
        self.svuotaRoot(self.root)
        self.caricaContenuto(self.root)

        if scelta == '1° Esperimento':
            gestore_canvas.disegnaPrimo()
        elif scelta == '2° Esperimento':
            gestore_canvas.disegnaSecondo()
        elif scelta == '3° Esperimento':
            gestore_canvas.disegnaTerzo()
        elif scelta == '4° Esperimento':
            gestore_canvas.disegnaQuarto()
        elif scelta == '5° Esperimento':
            gestore_canvas.disegnaQuinto()

    def svuotaRoot(self, root : tk.Frame):
        for widget in root.winfo_children():
            widget.destroy()
    
    def registraDiapositiva(self, link : tk.StringVar):
        self.labelDiapositiva = link

    def aggiornaContoDiapositiva(self):
        self.labelDiapositiva.set(f'{self.index_diapositiva+1}/{len(self.diapositive)}')
    
    def caricaContenuto(self, root : tk.Frame):
        self.root = root
        widgets = self.diapositive[self.index_diapositiva]
        root.columnconfigure(0, weight=1)
        for i in range(len(widgets)):
            root.rowconfigure(i, weight=1)
        i = 0
        for tipo_widget, configurazione in widgets.items():
            widget = None
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
    gestore_canvas.canvas = canvas

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
    gestore_dialogo.registraDiapositiva(diapositiva)
    contatore_diapositive = tk.Label(frame_navigazione, textvariable=diapositiva, bg=GREY)

    bottone_sx.grid(row=0, column=0, sticky='nswe')
    contatore_diapositive.grid(row=0, column=1, sticky='nswe')
    bottone_dx.grid(row=0, column=2, sticky='nswe')

gestore_canvas = GestoreCanvas()
gestore_dialogo = GestoreDialogo()
main = caricaRadice()
main.mainloop()
