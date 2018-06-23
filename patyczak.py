from tkinter import *
import random
import time

class Gra:
    def __init__(self):
        self.tk = Tk()
        self.tk.title('Pan Patyczak pędzi do wyjścia')
        self.tk.resizable(0, 0)
        self.tk.wm_attributes('-topmost', 1)
        self.plotno = Canvas(self.tk, width = 500, height = 500, highlightthickness = 0)
        self.plotno.pack()
        self.tk.update()
        self.wysokosc_plotna = 500
        self.szerokosc_plotna = 500
        self.tlo = PhotoImage(file = "tlo.gif")
        sze = self.tlo.width()
        wys = self.tlo.height()
        for x in range(0, 5):
            for y in range(0,5):
                self.plotno.create_image(x * sze, y * wys, image = self.tlo, anchor = 'nw')
        self.duszki = []
        self.biegnie = True

    def pętlaGłówna(self):
        while 1:
            if self.biegnie == True:
                for duszek in self.duszki:
                    duszek.move()
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)
            
class Coords:
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

def na_osi_x(wsp1, wsp2):
    if (wsp1.x1 > wsp2.x1 and wsp1.x1 < wsp2.x2)\
       or (wsp1.x2 > wsp2.x1 and wsp1.x2 < wsp2.x2)\
       or (wsp2.x1 > wsp1.x1 and wsp2.x1 < wsp1.x2)\
       or (wsp2.x2 > wsp1.x1 and wsp2.x2 < wsp1.x2):
        return True
    else:
        return False

def na_osi_y(wsp1, wsp2):
    if (wsp1.y1 > wsp2.y1 and wsp1.y1 < wsp2.y2)\
       or (wsp1.y2 > wsp2.y1 and wsp1.y2 < wsp2.y2)\
       or (wsp2.y1 > wsp1.y1 and wsp2.y1 < wsp1.y2)\
       or (wsp2.y2 > wsp1.y1 and wsp2.y2 < wsp1.y2):
        return True
    else:
        return False

def kolizja_lewa(wsp1, wsp2):
    if na_osi_y(wsp1, wsp2):
        if wsp1.x1 <= wsp2.x2 and wsp1.x1 >= wsp2.x1:
            return True
    return False

def kolizja_prawa(wsp1, wsp2):
    if na_osi_y(wsp1, wsp2):
        if wsp1.x2 >= wsp2.x1 and wsp1.x2 <= wsp2.x2:
            return True
    return False

def kolizja_gora(wsp1, wsp2):
    if na_osi_x(wsp1, wsp2):
        if wsp1.y1 <= wsp2.y2 and wsp1.y1 >= wsp2.y1:
            return True
    return False

def kolizja_dol(y, wsp1, wsp2):
    if na_osi_x(wsp1, wsp2):
        oblicz_y = wsp1.y2 + y
        if oblicz_y >= wsp2.y1 and oblicz_y <= wsp2.y2:
            return True
    return False


class Duszek:
    def __init__(self, gra):
        self.gra = gra
        self.koniecGry = False
        self.wspolrzedne = None
    def move(self):
        pass
    def coords(self):
        return self.wspolrzedne

class DuszekPlatforma(Duszek):
    def __init__(self, gra, obrazek, x, y, szerokosc, wysokosc):
        Duszek.__init__(self, gra)
        self.obrazek = obrazek
        self.image = gra.plotno.create_image(x, y, image = self.obrazek, anchor = 'nw')
        self.wspolrzedne = Coords(x, y, x + szerokosc, y + wysokosc)

class DuszekPatyczak(Duszek):
    def __init__(self, gra):
        Duszek.__init__(self, gra)
        self.obrazki_lewa = [PhotoImage(file="patyczak_L1.gif"), PhotoImage(file="patyczak_L2.gif"), PhotoImage(file="patyczak_L3.gif")]
        self.obrazki_prawa = [PhotoImage(file="patyczak_P1.gif"), PhotoImage(file="patyczak_P2.gif"), PhotoImage(file="patyczak_P3.gif")]
        self.image = gra.plotno.create_image(200, 470, image = self.obrazki_lewa[0], anchor = 'nw')
        self.x = -2
        self.y = 0
        self.biezacy_obrazek = 0
        self.biezacy_obrazek_dodaj = 1
        self.licznik_skokow = 0
        self.ostatni_czas = time.time()
        self.wspolrzedne = Coords()
        gra.plotno.bind_all('<KeyPress-Left>', self.obrot_w_lewo)
        gra.plotno.bind_all('<KeyPress-Right>', self.obrot_w_prawo)
        gra.plotno.bind_all('<space>', self.skok)

    def obrot_w_lewo(self, zdarzenie):
        if self.y == 0:
            self.x = -2

    def obrot_w_prawo(self, zdarzenie):
        if self.y == 0:
            self.x = 2

    def skok(self, zdarzenie):
        if self.y == 0:
            self.y = -4
            self.licznik_skokow = 0

    def animuj(self):
        if self.x != 0 and self.y == 0:
            if time.time() - self.ostatni_czas > 0.1:
                self.ostatni_czas = time.time()
                self.biezacy_obrazek += self.biezacy_obrazek_dodaj
                if self.biezacy_obrazek >= 2:
                    self.biezacy_obrazek_dodaj = -1
                if self.biezacy_obrazek <= 0:
                    self.biezacy_obrazek_dodaj = 1
        if self.x < 0:
            if self.y != 0:
                self.gra.plotno.itemconfig(self.image, image=self.obrazki_lewa[2])
            else:
                self.gra.plotno.itemconfig(self.image, image=self.obrazki_lewa[self.biezacy_obrazek])
        elif self.x > 0:
            if self.y != 0:
                self.gra.plotno.itemconfig(self.image, image=self.obrazki_prawa[2])
            else:
                self.gra.plotno.itemconfig(self.image, image=self.obrazki_prawa[self.biezacy_obrazek])

    def coords(self):
        xy = self.gra.plotno.coords(self.image)
        self.wspolrzedne.x1 = xy[0]
        self.wspolrzedne.y1 = xy[1]
        self.wspolrzedne.x2 = xy[0] + 27
        self.wspolrzedne.y2 = xy[1] + 30
        return self.wspolrzedne

    def move(self):
        self.animuj()
        if self.y <0:
            self.licznik_skokow += 1
            if self.licznik_skokow > 20:
                self.y = 4
        if self.y > 0:
            self.licznik_skokow -= 1
        wsp = self.coords()
        lewa = True
        prawa = True
        gora = True
        dol = True
        spadanie = True

        if self.y > 0 and wsp.y2 >= self.gra.wysokosc_plotna:
            self.y = 0
            dol = False
        elif self.y < 0 and wsp.y1 <= 0:
            self.y = 0
            gora = False
        if self.x > 0 and wsp.x2 >= self.gra.szerokosc_plotna:
            self.x = 0
            prawa = False
        elif self.x < 0 and wsp.x1 <= 0:
            self.x = 0
            lewa = False
        for duszek in self.gra.duszki:
            if duszek == self:
                continue
            duszek_wsp = duszek.coords()
            if gora and self.y < 0 and kolizja_gora(wsp, duszek_wsp):
                self.y = -self.y
                gora = False
            if dol and self.y > 0 and kolizja_dol(self.y, wsp, duszek_wsp):
                self.y = duszek_wsp.y1 - wsp.y2
                if self.y < 0:
                    self.y = 0
                dol = False
                gora = False
            if dol and spadanie and self.y == 0 and wsp.y2 < self.gra.wysokosc_plotna and kolizja_dol(1, wsp, duszek_wsp):
                spadanie = False
            if lewa and self.x < 0 and kolizja_lewa(wsp, duszek_wsp):
                self.x = 0
                lewa = False
                if duszek.koniecGry:
                    self.gra.biegnie = False
            if prawa and self.x > 0 and kolizja_prawa(wsp, duszek_wsp):
                self.x = 0
                prawa = False
                if duszek.koniecGry:
                    self.gra.biegnie = False
        if spadanie and dol and self.y == 0 and wsp.y2 < self.gra.wysokosc_plotna:
            self.y = 4
        self.gra.plotno.move(self.image, self.x, self.y )

class DuszekDrzwi(Duszek):
    def __init__(self, gra, obrazek, x, y, szerokosc, wysokosc):
        Duszek.__init__(self, gra)
        self.obrazek = obrazek
        self.image = gra.plotno.create_image(x, y, image=self.obrazek, anchor='nw')
        self.wspolrzedne = Coords(x, y, x + (szerokosc / 2), y + wysokosc)
        self.koniecGry = True

g = Gra()
platforma1 = DuszekPlatforma(g, PhotoImage(file = "platforma1.gif"), 0, 480, 100, 10)
platforma2 = DuszekPlatforma(g, PhotoImage(file = "platforma1.gif"), 150, 440, 100, 10)
platforma3 = DuszekPlatforma(g, PhotoImage(file = "platforma1.gif"), 300, 400, 100, 10)
platforma4 = DuszekPlatforma(g, PhotoImage(file = "platforma1.gif"), 300, 160, 100, 10)
platforma5 = DuszekPlatforma(g, PhotoImage(file = "platforma2.gif"), 175, 350, 66, 10)
platforma6 = DuszekPlatforma(g, PhotoImage(file = "platforma2.gif"), 50, 300, 66, 10)
platforma7 = DuszekPlatforma(g, PhotoImage(file = "platforma2.gif"), 170, 120, 66, 10)
platforma8 = DuszekPlatforma(g, PhotoImage(file = "platforma2.gif"), 45, 60, 66, 10)
platforma9 = DuszekPlatforma(g, PhotoImage(file = "platforma3.gif"), 170, 250, 32, 10)
platforma10 = DuszekPlatforma(g, PhotoImage(file = "platforma3.gif"), 230, 200, 32, 10)
g.duszki.append(platforma1)
g.duszki.append(platforma2)
g.duszki.append(platforma3)
g.duszki.append(platforma4)
g.duszki.append(platforma5)
g.duszki.append(platforma6)
g.duszki.append(platforma7)
g.duszki.append(platforma8)
g.duszki.append(platforma9)
g.duszki.append(platforma10)
drzwi = DuszekDrzwi(g, PhotoImage(file="drzwi1.gif"), 45, 30, 40, 35)
g.duszki.append(drzwi)
sf = DuszekPatyczak(g)
g.duszki.append(sf)
g.pętlaGłówna()
