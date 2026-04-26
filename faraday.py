import tkinter as tk
import json
import random
import math

########################
FPS = 30
########################

GREY = '#e8e8e8'
LARGHEZZA_LATERALE = 300
PI = 3.1415
E = 2.71828
MU0 = 4*3.1415*(10**-7)

class GestoreCanvas:
    def __init__(self):
        self.canvas : tk.Canvas = None
        self.fps = FPS
        self.intervallo = 1000//self.fps
        self.mult_tempo = tk.DoubleVar(value=1)
        self.delta = self.intervallo*self.mult_tempo.get()

        # PARAMETRI GENERICI
        self.tempo = 0
        self.fem = tk.DoubleVar(value=0.7)
        self.resistenza = 0.1
        self.corrente_potenziale = 0
        self.corrente = tk.DoubleVar(value=0)
        self.corrente_max = self.fem.get() / self.resistenza
        self.corrente_indotta = 0
        self.induttanza = 0.5
        self.campo_magnetico = 0
        # PARAMETRI 1°
        self.img_galvanometro = tk.PhotoImage(file='galvanometroMK2.gif')
        self.img_esperimento1 = tk.PhotoImage(file='esperimento1.gif')
        self.img_interr_aperto = tk.PhotoImage(file='interruttoreAperto.gif')
        self.img_interr_chiuso = tk.PhotoImage(file='interruttoreChiuso.gif')
        self.img_formula_flusso = tk.PhotoImage(file='formulaFlusso.gif')

        self.resistenza_solenoide = 1 # ohm
        self.N_spire_solenoide = 70
        self.L_solenoide = 0.45 #m
        self.raggio_solenoide = 0.01 #m
        self.area_solenoide = self.raggio_solenoide*(PI**2)
        # PARAMETRI 2°
        self.circuito1 = tk.PhotoImage(file='circuito1.gif')
        self.circuito2 = tk.PhotoImage(file='circuito2.gif')
        self.w = 0
        # PARAMETRI 3°
        self.calamita = tk.PhotoImage(file='calamita.gif')
        # PARAMETRI 4°
        self.vettore = 0
        self.campo4 = tk.PhotoImage(file='campo4.gif').subsample(2,2)
        self.circuito4 = tk.PhotoImage(file='circuito4.gif').subsample(2,2)
        # PARAMETRI 5°
        self.spira5 = tk.PhotoImage(file='spira5.gif')
        self.prospettiva = tk.PhotoImage(file='prospettiva5.gif')

    # =================================== PRIMO ===================================
    def disegnaPrimo(self):
        larghezza = self.canvas.winfo_width()
        altezza = self.canvas.winfo_height()
        self.canvas.delete('all')

        # creazione iniziale di oggetti grafici
        esp = self.canvas.create_image(larghezza//2, altezza//2, image=self.img_esperimento1)
        self.bottone_interruttore = tk.Button(radice, image=self.img_interr_aperto, command=self.interruttorePremuto)
        self.bottone_interruttore.aperto = 1
        interruttore = self.canvas.create_window(larghezza//2, altezza//2, window=self.bottone_interruttore)
        galva = self.canvas.create_image(0,0, image = self.img_galvanometro)
        ago = self.canvas.create_line(0, 0, 0, 0, fill='red', width=4)

        self.loopPrimo(esp, interruttore, galva, ago)

    def loopPrimo(self, espID, interruttoreID, galvaID, agoID):
        self.delta = self.intervallo*self.mult_tempo.get()
        if self.delta != 0.0:
            larghezza = self.canvas.winfo_width()
            altezza = self.canvas.winfo_height()

            # aggiornamento oggetti grafici
            self.canvas.coords(espID, (larghezza//2, altezza//2))
            self.canvas.coords(interruttoreID, (larghezza//2-145, altezza//2-167))
            self.aggiornaGalvanometro(larghezza, galvaID, agoID)

            self.calcoliFisici1()

        if gestore_dialogo.esperimento == '1° Esperimento':
            self.canvas.after(self.intervallo, self.loopPrimo, espID, interruttoreID, galvaID, agoID)
        else: return 0
        self.tempo += (self.delta)

    # 180x150
    def aggiornaGalvanometro(self, larghezza, galvaID, agoID):
        LARGHEZZA_GALVANOMETRO = 180
        ALTEZZA_GALVANOMETRO = 150
        RAGGIO = 113

        PADX = 10
        PADY = 10
        
        XCENTRO = larghezza-100
        YCENTRO = 146
        RAD_META = PI*(3/2)
        RAD_MAX =  5.62225
        RAD_MIN = 3.8025
        self.canvas.coords(galvaID, (larghezza-(LARGHEZZA_GALVANOMETRO//2) - PADX, ALTEZZA_GALVANOMETRO//2 + PADY))
        
        k = (RAD_MAX - RAD_MIN) / (6 * 1e-6)
        alfa = RAD_META + self.corrente_indotta * k
        if alfa > RAD_MAX : alfa = RAD_MAX
        elif alfa < RAD_MIN : alfa = RAD_MIN

        x = math.cos(alfa)*RAGGIO
        y = math.sin(alfa)*RAGGIO
        
        self.canvas.coords(agoID, (XCENTRO, YCENTRO, XCENTRO+x, YCENTRO+y))


    def interruttorePremuto(self):
        self.tempo = 0
        if self.bottone_interruttore.aperto:
            self.bottone_interruttore.aperto = 0
            self.bottone_interruttore.config(image=self.img_interr_chiuso)
        else:
            self.bottone_interruttore.aperto = 1
            self.bottone_interruttore.config(image=self.img_interr_aperto)
    
    def calcoliFisici1(self):
        if self.bottone_interruttore.aperto:
            i1 = (self.fem.get()/self.resistenza)*(E**(-self.tempo*self.resistenza/self.induttanza))
        else:
            i1 = (self.fem.get()/self.resistenza)*(1-E**(-self.tempo*self.resistenza/self.induttanza))
        b = (MU0*i1*self.N_spire_solenoide)/self.L_solenoide
        delta_flusso_b = -(self.N_spire_solenoide*self.area_solenoide*(self.campo_magnetico-b))
        self.corrente_indotta = delta_flusso_b/(self.resistenza_solenoide*self.delta)
        self.campo_magnetico = b
        self.corrente.set(i1)

    # =================================== SECONDO ===================================
    def disegnaSecondo(self):
        self.canvas.delete('all')
        larghezza = self.canvas.winfo_width()
        altezza = self.canvas.winfo_height()
        c1 = self.canvas.create_image(larghezza//2 - 200, altezza//2, image=self.circuito1)
        c2 = self.canvas.create_image(larghezza//2 + 200, altezza//2, image=self.circuito2)
        self.loopSecondo(c2)

    def loopSecondo(self, c2id):
        larghezza = self.canvas.winfo_width()
        altezza = self.canvas.winfo_height()
        self.delta = self.intervallo*self.mult_tempo.get()
        self.canvas.coords(c2id, (larghezza//2 + 200 + 100*(math.sin(self.w*self.tempo)), altezza//2))
        if gestore_dialogo.esperimento == '2° Esperimento':
            self.canvas.after(self.intervallo, self.loopSecondo, c2id)
        else: return 0
        self.tempo += (self.delta * 0.001)
    
    def avviaMovimento(self):
        self.w = 2

    def fermaMovimento(self):
        self.w = 0
    # =================================== TERZO ===================================
    def disegnaTerzo(self):
        self.canvas.delete('all')
        larghezza = self.canvas.winfo_width()
        altezza = self.canvas.winfo_height()
        cala = self.canvas.create_image(larghezza//2 - 200, altezza//2, image=self.calamita)
        c2 = self.canvas.create_image(larghezza//2 + 200, altezza//2, image=self.circuito2)
        self.loopTerzo(c2)

    def loopTerzo(self, c2id):
        larghezza = self.canvas.winfo_width()
        altezza = self.canvas.winfo_height()
        self.delta = self.intervallo*self.mult_tempo.get()
        self.canvas.coords(c2id, (larghezza//2 + 200 + 100*(math.sin(self.w*self.tempo)), altezza//2))
        if gestore_dialogo.esperimento == '3° Esperimento':
            self.canvas.after(self.intervallo, self.loopTerzo, c2id)
        else: return 0
        self.tempo += (self.delta * 0.001)
    # =================================== QUARTO ===================================
    def disegnaQuarto(self):
        self.canvas.delete('all')
        larghezza = self.canvas.winfo_width()
        altezza = self.canvas.winfo_height()
        campo4 = self.canvas.create_image(larghezza//2, altezza//2, image=self.campo4)
        c4 = self.canvas.create_image(larghezza//2+220, altezza//2, image=self.circuito4)
        self.loopQuarto(c4)

    def loopQuarto(self, c4id):
        larghezza = self.canvas.winfo_width()
        altezza = self.canvas.winfo_height()
        self.delta = self.intervallo*self.mult_tempo.get()
        if self.canvas.coords(c4id):
            x = self.canvas.coords(c4id)[0]
            if x < larghezza//2-220 or x > larghezza//2+220:
                self.vettore *= -1
            self.canvas.coords(c4id, x + self.vettore, altezza//2)
        if gestore_dialogo.esperimento == '4° Esperimento':
            self.canvas.after(self.intervallo, self.loopQuarto, c4id)
        else: return 0
        self.tempo += (self.delta * 0.001)
    
    def avviaMovimento4(self):
        if self.vettore:
            self.vettore = 5 * (self.vettore/abs(self.vettore))
        else: self.vettore = 5
    # =================================== QUINTO ===================================
    def disegnaQuinto(self):
        larghezza = self.canvas.winfo_width()
        altezza = self.canvas.winfo_height()
        self.canvas.delete('all')
        self.canvas.create_image(larghezza//2+250, altezza//2, image=self.calamita)
        self.canvas.create_image(larghezza//2-250, altezza//2, image=self.calamita)
        self.canvas.create_image(larghezza//2, altezza//2, image=self.spira5)
        self.canvas.create_image(130, 120, image=self.prospettiva)

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
        pass
        for widget in root.winfo_children():
            widget.destroy()
    
    def registraDiapositiva(self, link : tk.StringVar):
        self.labelDiapositiva = link

    def aggiornaContoDiapositiva(self):
        self.labelDiapositiva.set(f'{self.index_diapositiva+1}/{len(self.diapositive)}')
    
    def caricaContenuto(self, root : tk.Frame, id = None):
        if not id: self.root = root
        widgets = self.diapositive[self.index_diapositiva]
        if id: widgets = self.diapositive[self.index_diapositiva][id]
        root.columnconfigure(0, weight=1)
        for i in range(len(widgets)):
            root.rowconfigure(i, weight=1)
        i = 0
        for tipo_widget, configurazione in widgets.items():
            widget = None
            if tipo_widget[0] == 'L':
                widget = tk.Label(root, wraplength=LARGHEZZA_LATERALE-30, bg=GREY, **configurazione)
            elif tipo_widget[0] == 'S':
                if 'variable' in list(configurazione.keys()):
                    var : tk.DoubleVar = getattr(gestore_canvas, configurazione['variable'])
                    del configurazione['variable']
                    widget = tk.Scale(root, bg=GREY, variable=var,**configurazione)
                else:
                    widget = tk.Scale(root, bg=GREY, **configurazione)
            elif tipo_widget[0] == 'B':
                if 'funzione' in list(configurazione.keys()):
                    func_str = configurazione['funzione']
                    func = getattr(gestore_canvas, func_str)
                    del configurazione['funzione']
                    widget = tk.Button(root, bg=GREY, command=func,**configurazione)
                    configurazione['funzione'] = func_str
                else:
                    widget = tk.Button(root, bg=GREY,**configurazione)
            elif tipo_widget[0] == 'F':
                widget = tk.Frame(root, bg=GREY)
                self.caricaContenuto(widget, tipo_widget)
            elif tipo_widget[0] == 'I':
                img = getattr(gestore_canvas, configurazione['nome'])
                widget = tk.Label(root, image=img)
            if not id:
                widget.grid(row = i, column = 0)
            else:
                widget.pack(side = tk.LEFT)
            i+=1

def caricaRadice(radice) -> tk.Tk:
    radice.geometry('1100x710')

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
    frame_superiore.columnconfigure(0, weight=1)
    frame_superiore.columnconfigure(1, weight=1)
    frame_superiore.grid(row=0, column=0, sticky='nsew')

    scelta  = tk.StringVar(root)
    scelta.set(gestore_dialogo.esperimento)
    opzioni = [f'{x}° Esperimento' for x in range(1,6)]
    menu = tk.OptionMenu(frame_superiore, scelta, *opzioni, command=gestore_dialogo.cambioEsperimento)

    frame_tempo = tk.Frame(frame_superiore, bg=GREY)
    label_tempo = tk.Label(frame_tempo, text=f'Velocità tempo (Nx): ', bg=GREY)
    scale_tempo = tk.Scale(frame_tempo, variable=gestore_canvas.mult_tempo, from_=0, to=1, orient='horizontal', resolution=0.01, bg=GREY, length=180)
    label_tempo.grid(row=0, column=1)
    scale_tempo.grid(row=0, column=2)

    menu.grid(row=0, column=0, stick='w')
    frame_tempo.grid(row=0, column=1, stick='e')

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

radice = tk.Tk()
gestore_canvas = GestoreCanvas()
gestore_dialogo = GestoreDialogo()
main = caricaRadice(radice)
main.mainloop()


