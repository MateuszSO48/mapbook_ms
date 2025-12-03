from tkinter import *
import tkintermapview
import psycopg2
import requests
from bs4 import BeautifulSoup

db_engine = psycopg2.connect(
    user="postgres",
    database="postgres",
    password="postgres",
    port="5432",
    host="localhost"
)

users: list = []


class User:
    def __init__(self, id, name: str, location: str, posts: int, img_url: str, coords=None):
        self.id = id
        self.name = name
        self.location = location
        self.posts = posts
        self.img_url = img_url
        if coords:
            self.coords = coords
        else:
            self.coords = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coords[0], self.coords[1], text=self.name)

    def get_coordinates(self):
        url: str = f'https://pl.wikipedia.org/wiki/{self.location}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response_html = BeautifulSoup(response.text, 'html.parser')
        latitude = float(response_html.select('.latitude')[1].text.replace(',', '.'))
        longitude = float(response_html.select('.longitude')[1].text.replace(',', '.'))
        return [latitude, longitude]


def add_user(users_data: list, db_engine=db_engine) -> None:
    cursor = db_engine.cursor()
    name: str = entry_name.get()
    location: str = entry_lokalizacja.get()
    posts: int = int(entry_posty.get())
    img_url: str = entry_img_url.get()

    # Tymczasowo tworzymy obiekt aby pobrać współrzędne
    temp_user = type('obj', (object,), {
        'location': location,
        'get_coordinates': lambda self: User.get_coordinates(self)
    })()
    coords = temp_user.get_coordinates()

    SQL = f"INSERT INTO public.users(name, location, posts, img_url, geometry) VALUES ('{name}', '{location}', {posts}, '{img_url}', 'SRID=4326;POINT({coords[0]} {coords[1]})') RETURNING id;"
    cursor.execute(SQL)
    user_id = cursor.fetchone()[0]
    db_engine.commit()

    user = User(id=user_id, name=name, location=location, posts=posts, img_url=img_url, coords=coords)
    users_data.append(user)

    user_info(users_data)
    entry_name.delete(0, END)
    entry_lokalizacja.delete(0, END)
    entry_posty.delete(0, END)
    entry_img_url.delete(0, END)
    entry_name.focus()


def user_info(users_data_list, db_engine=db_engine):
    global users
    listbox_lista_obiektow.delete(0, END)

    # Usuń stare markery
    for user in users:
        if hasattr(user, 'marker'):
            user.marker.delete()

    users.clear()

    SQL = "SELECT *, ST_AsEWKT(geometry) FROM public.users;"
    cursor = db_engine.cursor()
    cursor.execute(SQL)
    users_data = cursor.fetchall()

    for idx, user_db in enumerate(users_data):
        # user_db: [0]=id, [1]=name, [2]=location, [3]=posts, [4]=img_url, [5]=geometry(EWKT)
        coords = list(map(float, user_db[-1][16:-1].split()))
        user_obj = User(id=user_db[0], name=user_db[1], location=user_db[2],
                        posts=user_db[3], img_url=user_db[4], coords=coords)
        users.append(user_obj)
        listbox_lista_obiektow.insert(idx, f"{user_db[1]} {user_db[2]} {user_db[3]}")


def delete_user(users_data: list, db_engine=db_engine):
    i = listbox_lista_obiektow.index(ACTIVE)
    if i < len(users_data):
        user_id = users_data[i].id
        cursor = db_engine.cursor()
        SQL = f"DELETE FROM public.users WHERE id = {user_id};"
        cursor.execute(SQL)
        db_engine.commit()

        users_data[i].marker.delete()
        users_data.pop(i)
        user_info(users_data)


def user_details(users_data: list):
    i = listbox_lista_obiektow.index(ACTIVE)
    if i < len(users_data):
        label_imie_szczegoly_obiektu_wartosc.config(text=users_data[i].name)
        label_lokalizacja_szczegoly_obiektu_wartosc.config(text=users_data[i].location)
        label_posty_szczegoly_obiektu_wartosc2.config(text=users_data[i].posts)
        map_widget.set_position(users_data[i].coords[0], users_data[i].coords[1])
        map_widget.set_zoom(14)


def edit_user(users_data: list):
    i = listbox_lista_obiektow.index(ACTIVE)
    if i < len(users_data):
        entry_name.delete(0, END)
        entry_lokalizacja.delete(0, END)
        entry_posty.delete(0, END)
        entry_img_url.delete(0, END)

        entry_name.insert(0, users_data[i].name)
        entry_lokalizacja.insert(0, users_data[i].location)
        entry_posty.insert(0, users_data[i].posts)
        entry_img_url.insert(0, users_data[i].img_url)

        button_dodaj_obiekt.config(text="Zapisz zmiany", command=lambda: update_user(users_data, i))


def update_user(users_data: list, i, db_engine=db_engine):
    users_data[i].name = entry_name.get()
    users_data[i].location = entry_lokalizacja.get()
    users_data[i].posts = int(entry_posty.get())
    users_data[i].img_url = entry_img_url.get()

    users_data[i].coords = users_data[i].get_coordinates()
    users_data[i].marker.set_position(users_data[i].coords[0], users_data[i].coords[1])
    users_data[i].marker.set_text(text=users_data[i].name)

    # Aktualizuj w bazie danych
    cursor = db_engine.cursor()
    SQL = f"UPDATE public.users SET name='{users_data[i].name}', location='{users_data[i].location}', posts={users_data[i].posts}, img_url='{users_data[i].img_url}', geometry='SRID=4326;POINT({users_data[i].coords[0]} {users_data[i].coords[1]})' WHERE id={users_data[i].id};"
    cursor.execute(SQL)
    db_engine.commit()

    user_info(users_data)

    button_dodaj_obiekt.config(text="Dodaj obiekt", command=lambda: add_user(users_data))
    entry_name.delete(0, END)
    entry_lokalizacja.delete(0, END)
    entry_posty.delete(0, END)
    entry_img_url.delete(0, END)
    entry_name.focus()


root = Tk()
root.title("mapbook")
root.geometry("1025x760")

ramka_lista_obiektow = Frame(root)
ramka_formularz = Frame(root)
ramka_szczegoly_obiektu = Frame(root)
ramka_mapa = Frame(root)

ramka_lista_obiektow.grid(row=0, column=0)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly_obiektu.grid(row=1, column=0, columnspan=2)
ramka_mapa.grid(row=2, column=0, columnspan=2)

# RAMKA LISTA OBIEKTÓW
label_lista_obiektow = Label(ramka_lista_obiektow, text="Lista obiektów")
label_lista_obiektow.grid(row=0, column=0, columnspan=3)

listbox_lista_obiektow = Listbox(ramka_lista_obiektow)
listbox_lista_obiektow.grid(row=1, column=0, columnspan=3)

button_pokaz_szczegoly = Button(ramka_lista_obiektow, text="Pokaż szczegóły",
                                command=lambda: user_details(users_data=users))
button_pokaz_szczegoly.grid(row=2, column=0)

button_usun_obiekt = Button(ramka_lista_obiektow, text="Usuń obiekt", command=lambda: delete_user(users))
button_usun_obiekt.grid(row=2, column=1)

button_edytuj_obiekt = Button(ramka_lista_obiektow, text="Edytuj obiekt", command=lambda: edit_user(users))
button_edytuj_obiekt.grid(row=2, column=2)

# RAMKA FORMULARZ
label_formularz = Label(ramka_formularz, text="Formularz: ")
label_formularz.grid(row=0, column=0, columnspan=2)

label_imie = Label(ramka_formularz, text="Imie: ")
label_imie.grid(row=1, column=0, sticky=W)

label_lokalizacja = Label(ramka_formularz, text="Lokalizacja: ")
label_lokalizacja.grid(row=2, column=0, sticky=W)

label_posty = Label(ramka_formularz, text="Posty: ")
label_posty.grid(row=3, column=0, sticky=W)

label_img_url = Label(ramka_formularz, text="Obrazek: ")
label_img_url.grid(row=4, column=0, sticky=W)

entry_name = Entry(ramka_formularz)
entry_name.grid(row=1, column=1)

entry_lokalizacja = Entry(ramka_formularz)
entry_lokalizacja.grid(row=2, column=1)

entry_posty = Entry(ramka_formularz)
entry_posty.grid(row=3, column=1)

entry_img_url = Entry(ramka_formularz)
entry_img_url.grid(row=4, column=1)

button_dodaj_obiekt = Button(ramka_formularz, text="Dodaj obiekt", command=lambda: add_user(users))
button_dodaj_obiekt.grid(row=5, column=0, columnspan=2)

# RAMKA SZCZEGÓŁY OBIEKTÓW
label_szczegoly_obiektu = Label(ramka_szczegoly_obiektu, text="Szczegoly obiektu")
label_szczegoly_obiektu.grid(row=0, column=0, sticky=W)

label_imie_szczegoly_obiektu = Label(ramka_szczegoly_obiektu, text="Imie: ")
label_imie_szczegoly_obiektu.grid(row=1, column=0)

label_imie_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektu, text="....")
label_imie_szczegoly_obiektu_wartosc.grid(row=1, column=1)

label_lokalizacja_szczegoly_obiektu = Label(ramka_szczegoly_obiektu, text="Lokalizacja: ")
label_lokalizacja_szczegoly_obiektu.grid(row=1, column=2)

label_lokalizacja_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektu, text="....")
label_lokalizacja_szczegoly_obiektu_wartosc.grid(row=1, column=3)

label_posty_szczegoly_obiektu = Label(ramka_szczegoly_obiektu, text="Posty: ")
label_posty_szczegoly_obiektu.grid(row=1, column=4)

label_posty_szczegoly_obiektu_wartosc2 = Label(ramka_szczegoly_obiektu, text="....")
label_posty_szczegoly_obiektu_wartosc2.grid(row=1, column=5)

# RAMKA MAPY
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1025, height=600, corner_radius=0)
map_widget.set_position(52.0, 21.0)
map_widget.set_zoom(6)
map_widget.grid(row=0, column=0)

# Załaduj dane przy starcie
user_info(users)

root.mainloop()