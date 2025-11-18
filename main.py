from tkinter import *
import tkintermapview


root = Tk()
root.title("mapbook")
root.geometry("1025x760")


ramka_lista_obiektow = Frame(root)
ramka_formularz = Frame(root)
ramka_szczegoly_obiektu = Frame(root)
ramka_mapa=Frame(root)

ramka_lista_obiektow.grid(row=0,column=0)
ramka_formularz.grid(row=0,column=1)
ramka_szczegoly_obiektu.grid(row=1,column=0)
ramka_mapa.grid(row=2,column=0)

#RAMKA LISTA OBIEKTÓW
label_lista_obiektow=Label(ramka_lista_obiektow, text="Lista obiektów")
label_lista_obiektow.grid(row=0,column=0, columnspan=3)

listbox_lista_obiektow=Listbox(ramka_lista_obiektow)
listbox_lista_obiektow.grid(row=1,column=0, columnspan=3)

button_pokaz_szczegoly=Button(ramka_lista_obiektow, text="Pokaż szczegóły")
button_pokaz_szczegoly.grid(row=2,column=0)

button_usun_obiekt=Button(ramka_lista_obiektow, text="Usuń obiekt")
button_usun_obiekt.grid(row=2,column=1)

button_edytuj_obiekt=Button(ramka_lista_obiektow, text="Edytuj obiekt")
button_edytuj_obiekt.grid(row=2,column=2)



#RAMKA FORMULARZ
label_formularz=Label(ramka_formularz, text="Formularz: ")
label_formularz.grid(row=0,column=0, columnspan=2)

label_imie=Label(ramka_formularz, text="Imie: ")
label_imie.grid(row=1,column=0, sticky=W)

label_lokalizacja=Label(ramka_formularz, text="Lokalizacja: ")
label_lokalizacja.grid(row=2,column=0, sticky=W)

label_posty=Label(ramka_formularz, text="Posty: ")
label_posty.grid(row=3,column=0, sticky=W)

label_img_url=Label(ramka_formularz, text="Obrazek: ")
label_img_url.grid(row=4,column=0, sticky=W)

entry_name=Entry(ramka_formularz)
entry_name.grid(row=1,column=1)

entry_lokalizacja=Entry(ramka_formularz)
entry_lokalizacja.grid(row=2,column=1)

entry_posty=Entry(ramka_formularz)
entry_posty.grid(row=3,column=1)

entry_img_url=Entry(ramka_formularz)
entry_img_url.grid(row=4,column=1)

button_dodaj_obiekt=Button(ramka_formularz, text="Dodaj obiekt")
button_dodaj_obiekt.grid(row=5,column=0, columnspan=2)





#RAMKA SZCZEGÓŁY OBIEKTÓW
label_szczegoly_obietku=Label(ramka_szczegoly_obiektu, text="Szczegoly obiektu")
label_szczegoly_obietku.grid(row=0,column=0, sticky=W)

label_imie_szczegoly_obietku=Label(ramka_szczegoly_obiektu, text="Imie: ")
label_imie_szczegoly_obietku.grid(row=1,column=0)

label_imie_szczegoly_obietku_wartosc=Label(ramka_szczegoly_obiektu, text="....")
label_imie_szczegoly_obietku_wartosc.grid(row=1,column=1)

label_lokalizacja_szczegoly_obiektu=Label(ramka_szczegoly_obiektu, text="Lokalizacja")
label_lokalizacja_szczegoly_obiektu.grid(row=1,column=2)

label_lokalizacja_szczegoly_obiektu=Label(ramka_szczegoly_obiektu, text="....")
label_lokalizacja_szczegoly_obiektu.grid(row=1,column=3)


label_posty_szczegoly_obietku_wartosc=Label(ramka_szczegoly_obiektu, text="Posty")
label_posty_szczegoly_obietku_wartosc.grid(row=1,column=4)

label_posty_szczegoly_obietku_wartosc=Label(ramka_szczegoly_obiektu, text="....")
label_posty_szczegoly_obietku_wartosc.grid(row=1,column=5)

#RAMKA MAPY
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1025, height=600, corner_radius=0)
map_widget.set_position(52.0, 21.0)
map_widget.set_zoom(6)
map_widget.grid(row=0,column=0)


root.mainloop()