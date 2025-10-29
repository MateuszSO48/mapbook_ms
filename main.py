users:list=[
    {"name":"Kasia", "location":"Warszawa", "posts":3},
    {"name":"Asia", "location":"Krakow", "posts":5},
    {"name":"Basia", "location":"Wroclaw", "posts":7},
]


for user in users:
    print(f"Twoj znajomy {user["name"]} z miejscowosci {user["location"]} opublikowal {user["posts"]} posty")