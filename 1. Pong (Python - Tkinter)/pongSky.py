from tkinter import *
import random
import time
import winsound

# X = szerokość
# Y = wysokość
# pozycja = [ X1,Y1 , X2 , Y2 ]
# ideksowanie - numeracja elementów w listach zaczyna się od 0!
# pozycja[0] = X1
# pozycja[1] = Y1

ilośćPrzegranych = 0
highScore = 0

class Piłka:
    def __init__(self,płótno_przekazane, kolor_przekazany, rakietka_przekazana):
        self.rakietka = rakietka_przekazana
        self.płótno = płótno_przekazane
        self.id = płótno.create_oval(10,10,25,25,fill=kolor_przekazany)
        self.płótno.move(self.id, 245, 100)
        początek = [-3,-2,-1,0,1,2,3]
        random.shuffle(początek)
        self.x = początek[0]
        self.y = -3
        self.wysokość_płótna = self.płótno.winfo_height()
        self.szerokość_płótna = self.płótno.winfo_width()
        self.upadek = False
        self.punkty = 0

    def rysuj(self):
        self.płótno.move(self.id,self.x,self.y)
        pozycja = self.płótno.coords(self.id)
        if pozycja[1] <= 0:
            self.y = 3
        if pozycja[3] >= self.wysokość_płótna:
            self.y = 0
            self.x = 0
            self.upadek = True
        if self.trafienie_w_piłkę(pozycja) == True:
            winsound.PlaySound("odbicie.wav", winsound.SND_ASYNC | winsound.SND_ALIAS)
            self.y = - 3
            self.punkty = self.punkty + 1
            

        if pozycja[0] <= 0:
            self.x = 3
        if pozycja[2] >= self.szerokość_płótna:
            self.x = -3

    def trafienie_w_piłkę(self,pozycja):
        pozycja_rakietki = self.płótno.coords(self.rakietka.id)
        if pozycja[2] >= pozycja_rakietki[0] and pozycja[0] <= pozycja_rakietki[2]:
            if pozycja[3] >= pozycja_rakietki[1] and pozycja[3] <= pozycja_rakietki[3]:
                return True
            return False

class Rakietka:
    def __init__(self, płótno_przekazane , kolor_przekazany):
        self.płótno = płótno_przekazane
        self.id = płótno.create_rectangle(0,0,100,10, fill=kolor_przekazany, outline="black")
        self.płótno.move(self.id,200,300)
        self.x = 0
        self.szerokość_płótna = self.płótno.winfo_width()
        self.płótno.bind_all('<KeyPress-Left>',self.w_lewo)
        self.płótno.bind_all('<KeyPress-Right>',self.w_prawo)

    def rysuj(self):
        self.płótno.move(self.id, self.x, 0)
        pozycja = self.płótno.coords(self.id)
        if pozycja[0] <= 0:
            self.x = 0
        if pozycja[2] >= self.szerokość_płótna:
           self.x = 0

    def w_lewo(self,zdarzenie):
        self.x = -4

    def w_prawo(self,zdarzenie):
        self.x = 4


okno = Tk()
okno.title(":) PONG")
okno.resizable(0,0)
okno.wm_attributes("-topmost",1)
while True:
    płótno = Canvas(okno,width=500,height=500,bd=0,highlightthickness=0,bg="black")
    płótno.pack()
    okno.update()


    rakietka = Rakietka(płótno,'blue')
    piłka = Piłka(płótno,"red",rakietka)

    aktualnyStan = płótno.create_text(120,30,text="Punkty: " + str(piłka.punkty), font=("Times",30), fill="white")
    najwyższyStan = płótno.create_text(360, 30, text="Rekord: " + str(highScore), font=("Times", 30), fill="white")

    while True:
        if piłka.upadek == False:
            piłka.rysuj()
            rakietka.rysuj()
            okno.update_idletasks()
            okno.update()
            time.sleep(0.001)
        if piłka.upadek == True:
            winsound.PlaySound("przegrana.wav", winsound.SND_ASYNC | winsound.SND_ALIAS)

            ilośćPrzegranych = ilośćPrzegranych + 1
            print(f"Przegrałeś! Ilość Twoich przegranych to: {ilośćPrzegranych}")
            for widget in okno.winfo_children():
                widget.destroy()
            time.sleep(0.5)
            break
        płótno.itemconfigure(aktualnyStan , text="Punkty: " + str(piłka.punkty), font=("Times",30))
        if piłka.punkty > highScore:
            highScore = piłka.punkty
            płótno.itemconfigure(najwyższyStan, text="Rekord: " + str(highScore), font=("Times",30))

okno.mainloop()