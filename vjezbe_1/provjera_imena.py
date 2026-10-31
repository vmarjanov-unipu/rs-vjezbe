"""
Kombinira najčešća hrvatska imena i prezimena (svako sa svakim),
za svaku kombinaciju pita backend za hakersko ime i ispisuje tablicu svih
hakerskih imena, od onih s najviše osoba prema onima s najmanje. Nakon tablice
ispisuje u kojem se retku nalazi autor (MY_FIRST_NAME, MY_LAST_NAME).

Tablica se ispisuje u Markdown obliku, pa se može izravno zalijepiti u README.

Backend mora biti pokrenut. Pokretanje:
    python3 provjera_imena.py
"""

import json
import urllib.error
import urllib.request
from collections import defaultdict

API_URL = "http://localhost:8000/hakersko-ime"
POSSIBLE_NAMES = 22 * 48  # broj pridjeva × broj imenica

MY_FIRST_NAME = "Vladimir"
MY_LAST_NAME = "Marjanović"

# Najčešća imena prema popisu stanovništva 2021. (DZS), redom po učestalosti.
# Izvor: srednja.hr
FIRST_NAMES = [
    "Ivan", "Marija", "Ana", "Josip", "Marko", "Ivana", "Luka", "Tomislav",
    "Stjepan", "Željko", "Ivica", "Ante", "Mario", "Nikola", "Mirjana",
    "Petar", "Katarina", "Damir", "Vesna", "Nada", "Marina", "Petra", "Goran",
    "Martina", "Lucija", "Maja", "Filip", "Iva", "Dragica", "Marica",
    "Ljubica", "Kristina", "Milan", "Sanja", "Branko", "Darko", "Jelena",
    "Mladen", "Gordana", "Matija", "Marijan", "Katica", "Zoran", "Antonio",
    "Snježana", "Karlo", "Kata", "Nikolina", "Igor", "Davor", "Vladimir",
    "Ivanka", "Zlatko", "Marijana", "Marin", "Franjo", "Robert", "Ljiljana",
    "Josipa", "David", "Sara", "Matej", "Branka", "Miroslav", "Mara", "Anka",
    "Ankica", "Anita", "Lana", "Danijel", "Mirko", "Željka", "Dražen",
    "Antun", "Jadranka", "Mira", "Hrvoje", "Zdravko", "Danijela", "Nevenka",
    "Ružica", "Jakov", "Mia", "Anica", "Boris", "Slavica", "Valentina",
    "Dario", "Danica", "Ema", "Dragan", "Marta", "Sandra", "Milka", "Matea",
    "Mihael", "Kristijan", "Zdenka", "Jasna", "Mateo",
]

# Najčešća prezimena prema popisu stanovništva 2021. (DZS), redom po učestalosti.
# Izvor: srednja.hr
LAST_NAMES = [
    "Horvat", "Kovačević", "Babić", "Marić", "Jurić", "Novak", "Kovačić",
    "Knežević", "Vuković", "Matić", "Marković", "Petrović", "Tomić",
    "Pavlović", "Kovač", "Božić", "Grgić", "Blažević", "Perić", "Pavić",
    "Radić", "Šarić", "Jukić", "Lovrić", "Vidović", "Filipović", "Bošnjak",
    "Perković", "Nikolić", "Bašić", "Barišić", "Popović", "Šimić", "Klarić",
    "Mandić", "Lončar", "Brkić", "Živković", "Martinović", "Galić", "Barić",
    "Jurković", "Bilić", "Kos", "Stanić", "Lukić", "Kralj", "Matijević",
    "Matković", "Ćosić", "Novosel", "Janković", "Mihaljević", "Miletić",
    "Jurišić", "Jelić", "Katić", "Ivanović", "Tadić", "Lučić", "Marinović",
    "Jerković", "Mikulić", "Posavec", "Bogdan", "Ilić", "Poljak", "Ivanković",
    "Šimunović", "Ivančić", "Marušić", "Herceg", "Milić", "Marjanović",
    "Vidaković", "Cindrić", "Vučković", "Topić", "Jovanović", "Jozić",
    "Rukavina", "Delić", "Špoljarić", "Grubišić", "Varga", "Pavičić",
    "Brajković", "Dujmović", "Đurić", "Bačić", "Petrić", "Novaković", "Burić",
    "Štimac", "Vukelić", "Kolarić", "Kolar", "Mitrović", "Petković", "Ivić",
]


def fetch_hacker_name(first_name, last_name):
    """Šalje POST zahtjev backendu i vraća hakersko ime."""
    body = json.dumps({"ime": first_name, "prezime": last_name}).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read())["hakersko_ime"]


def collect_groups(people):
    """Za svaku osobu dohvaća hakersko ime i grupira osobe po imenu."""
    groups = defaultdict(list)
    total = len(people)

    for done, (first_name, last_name) in enumerate(people, start=1):
        person = f"{first_name} {last_name}"
        try:
            groups[fetch_hacker_name(first_name, last_name)].append(person)
        except urllib.error.HTTPError as error:
            print(f"  Greška za {person}: HTTP {error.code}")
        if done % 1000 == 0:
            print(f"  {done}/{total}")

    return groups


def print_table(rows):
    """Ispisuje retke kao Markdown tablicu."""
    print("| # | Hakersko ime | Broj osoba | Osobe |")
    print("|---|---|---|---|")
    for label, name, people in rows:
        print(f"| {label} | {name} | {len(people)} | {', '.join(people)} |")


def main():
    assert len(set(FIRST_NAMES)) == len(FIRST_NAMES), "Imena se ne smiju ponavljati"
    assert len(set(LAST_NAMES)) == len(LAST_NAMES), "Prezimena se ne smiju ponavljati"

    people = [(first, last) for first in FIRST_NAMES for last in LAST_NAMES]

    print(f"Provjeravam {len(FIRST_NAMES)} imena × {len(LAST_NAMES)} prezimena "
          f"= {len(people)} osoba...")
    try:
        groups = collect_groups(people)
    except urllib.error.URLError:
        print("\nPoslužitelj nije dostupan. Je li backend pokrenut?")
        return

    # Skupine od najveće prema manjima; kod jednake veličine abecedno.
    ranked = sorted(groups.items(), key=lambda item: (-len(item[1]), item[0]))
    rows = [(str(place), name, members)
            for place, (name, members) in enumerate(ranked, start=1)]

    print()
    print(f"Osoba: {len(people)}, različitih hakerskih imena: {len(groups)} "
          f"od {POSSIBLE_NAMES} mogućih.\n")
    print_table(rows)

    me = f"{MY_FIRST_NAME} {MY_LAST_NAME}"
    my_row = next((row for row in rows if me in row[2]), None)
    print()
    if my_row is None:
        print(f"{me} nije među provjerenim osobama.")
    else:
        place, name, members = my_row
        print(f"{me} je u retku {place}: {name} "
              f"(broj osoba s tim imenom: {len(members)}).")


if __name__ == "__main__":
    main()
