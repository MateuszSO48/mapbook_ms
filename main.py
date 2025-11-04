from mapbook_lib.controller import user_info, add_user, remove_user, update_user, get_map
from mapbook_lib.model import users

def main():

    while True:
        print("============================MENU====================================")
        print("0. Wyjście z programu")
        print("1. Wyświetlanie znajomego")
        print("2. Dodaj znajomego")
        print("3. Usuń znajomego")
        print("4. Aktualizuj znajomego")
        print("5. Generuj mapę")
        print("====================================================================")

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
            remove_user(users)
        if tmp_choice==4:
            print("wybrano funkcje aktualizowania znajomych")
            update_user(users)
        if tmp_choice==5:
            print("wybrano funkcje wyświetlania mapy")
            get_map(users)

if __name__ == "__main__":
    main()