import tkinter as tk

def creaParticella(tipo, x, y):
    colore = info_particelle[tipo][0]
    raggio = info_particelle[tipo][1]
    massa = info_particelle[tipo][2]
    carica = info_particelle[tipo][3]

    particella = canvas.create_oval(x -raggio, y-raggio, x+raggio, y+raggio, fill=colore)
    particelle.append({'id':particella,
                       'x':x,
                       'y':y,
                       'vx':0,
                       'vy':0,
                       'q':carica,
                       'm':massa,
                       'r':raggio})
    
def onClick(event):
    window_x = event.x
    window_y = event.y

    canvas_x = canvas.canvasx(window_x)
    canvas_y = canvas.canvasy(window_y)

    creaParticella(particella, canvas_x, canvas_y)

def selectParticle(event):
    global particella
    key = event.char
    if key == '1':
        particella = 'C'
    elif key == '2':
        particella = 'Cl'
    elif key == '3':
        particella = 'H'
    elif key == '4':
        particella = 'O'
    elif key == '5':
        particella = 'e'

def aggiorna():
    for p1 in particelle:
        forza_totale_x = 0
        forza_totale_y = 0

        carica_1 = p1['q']
        x1, y1 = p1['x'], p1['y']
        massa_1 = p1['m']

        for p2 in particelle:
            if p1 == p2: continue
            x2, y2 = p2['x'], p2['y']
            d = ((x2-x1)**2 + (y2-y1)**2)**0.5
            if d < RAGGIO_INTERESSE or d==0: continue

            carica_2 = p2['q']
            
            forza_x = (K*carica_1*carica_2*(x1-x2))/d**3
            forza_y = (K*carica_1*carica_2*(y1-y2))/d**3

            forza_totale_x += forza_x
            forza_totale_y += forza_y

        accellerazione_x = forza_totale_x/massa_1
        accellerazione_y = forza_totale_y/massa_1

        p1['vx'] += accellerazione_x
        p1['vy'] += accellerazione_y

        p1['x'] += p1['vx']
        p1['y'] += p1['vy']

        canvas.move(p1["id"], p1["vx"]*DELTA, p1["vy"]*DELTA)
    radice.after(DELTA, aggiorna)

        

#==============================================================

SCALA = 2
RAGGIO_INTERESSE = 60*SCALA
K = 9
DELTA = 16
LARGHEZZA = 800
ALTEZZA = 800
particella = 'C'
# NOMINATIVO : (COLORE, RAGGIO, MASSA, CARICA)
info_particelle = {'C':('grey', 7*SCALA, 12, 1),
                   'H':('white', 5.3*SCALA, 1, 1),
                   'Cl':('green', 10*SCALA, 35, 1),
                   'O': ('red', 6*SCALA, 16, 1),
                   'e':('yellow', 1*SCALA, 0.1, -1)}

particelle = []

radice = tk.Tk()
canvas = tk.Canvas(radice, width = LARGHEZZA, height = ALTEZZA, bg = 'white')

canvas.bind("<Button-1>", onClick)
radice.bind('<Key>', selectParticle)
canvas.pack()

aggiorna()
radice.mainloop()
