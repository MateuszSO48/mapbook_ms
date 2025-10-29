users:list=[
    {"name":"Kasia", "location":"Warszawa", "posts":3},
    {"name":"Asia", "location":"Krakow", "posts":5},
    {"name":"Basia", "location":"Wroclaw", "posts":7},
]

def user_info(users_data:list)->None:
    for user in users_data:
        print(f"Twoj znajomy {user["name"]} z miejscowosci {user["location"]} opublikowal {user["posts"]} posty")


def add_user(users_data)->None:
    name:str=input("Podaj imie nowego znajomego: ")
    location:str=input("Podaj nazwe miejscowosci: ")
    posts:int=int(input("Podaj liczbe postow: "))
    users_data.append({"name":name, "location":location, "posts":posts})


def remove_users(users_data)->None:
    tmp_name:str=input("Podaj imie uzytkownika do usuniecia ze znajomych: ")
    for user in users_data:
        if user["name"]==tmp_name:
            users.remove(user)


while True:
    tmp_choice:int=int(input("wybierz opcje menu:"))
    if tmp_choice==0:
        break
    if tmp_choice==1:
        print("wybrano funkcje wyswietlania aktywnosci znajomych")
        user_info(users)
    if tmp_choice==2:
        print("wybrano funkcje dodawania znajomego")
        add_user(users)
    if tmp_choice==3:
        print("wybrano funkcje usuwania znajomych")
        remove_users(users)
    if tmp_choice==4:
        print("wybrano funkcje aktualizowania znajomych")

