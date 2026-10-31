# Generator hakerskih imena

Jednostavna web aplikacija koja iz imena i prezimena osobe izračunava njezino 
šaljivo "hakersko ime" oblika **pridjev + imenica**, npr. *Usplahirena Funkcija*, 
*Pospani Poslužitelj* ili *Nestašna Konstanta*. 

Backend je REST API napisan u Pythonu (FastAPI), a frontend je obična HTML stranica 
koja ga poziva.

## Kako radi

1. **Normalizacija**: ime i prezime pretvaraju se u mala slova, uklanjaju se suvišni 
razmaci i dijakritici. Slovo đ se mapira u d, pa zato "Đurđa Šimić" i "durda simic" 
daju isto hakersko ime.
2. **Hash**: nad nizom `ime|prezime` računa se SHA-256.
3. **Odabir riječi**: prvih 8 bajtova hasha bira imenicu, idućih 8 bajtova pridjev 
(indeks = broj modulo duljina liste).
4. **Slaganje roda**: pridjev se uzima u obliku koji odgovara rodu imenice 
(*usplahireni procesor*, *usplahirena funkcija*, *usplahireno sučelje*).

Važno je napomenuti da je postupak deterministički. Dakle, ista osoba uvijek 
dobiva isto ime. Servis ništa ne sprema (stateless je), pa bi svaka njegova 
kopija za isti ulaz vratila isti rezultat, bez ikakve međusobne sinkronizacije.

Liste sadrže 22 pridjeva i 48 imenica, što daje 1056 mogućih hakerskih imena.

## API

| Metoda | Putanja | Opis |
|---|---|---|
| POST | `/hakersko-ime` | Izračunava hakersko ime za jednu osobu |
| GET | `/status` | Provjera radi li servis |

Ime i prezime šalju se u JSON tijelu zahtjeva, a ne u URL-u, kako osobni podaci 
ne bi završavali u logovima poslužitelja i povijesti preglednika.

**Zahtjev:**

```json
{"ime": "Đurđa", "prezime": "Šimić"}
```

**Odgovor:**

```json
{"ime": "Đurđa", "prezime": "Šimić", "hakersko_ime": "Usplahireni Kompajler"}
```

**Validacija:** ime i prezime su obavezni, najviše 50 znakova, dopuštena su slova, 
razmak, crtica i apostrof. Neispravan ulaz vraća status `422`.

Interaktivna dokumentacija (Swagger UI) dostupna je na `http://localhost:8000/docs`.

## Struktura projekta

**Backend:**

- `main.py` – FastAPI aplikacija i endpointi
- `models.py` – modeli zahtjeva i odgovora
- `generator.py` – normalizacija, hash i slaganje pridjeva s imenicom
- `words.py` – liste pridjeva i imenica
- `requirements.txt` – ovisnosti

**Frontend:**

- `index.html`
- `style.css`
- `javascript.js` – manje-više, ovo je komunikacija s backendom; adresa backenda 
je u konstanti `API_URL`

## Pokretanje

Pullati projekt na lokalno računalo. U folderu `vjezbe_1/backend_app` izvršiti ove 
naredbe:

**Backend:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
.venv/bin/uvicorn main:app --port 8000
```

Nakon ovoga se poslužitelj nalazi na `http://localhost:8000`.

**Frontend:**

U folderu `vjezbe_1/frontend_app` dvokliknuti na index.html

## Ručno testiranje

### Status poslužitelja

```bash
curl http://localhost:8000/status
```

Očekivano: `{"status":"ok"}`

### Jedna osoba

```bash
curl -X POST "http://localhost:8000/hakersko-ime" \
  -H "Content-Type: application/json" \
  -d '{"ime": "Ivan", "prezime": "Horvat"}'
```

Očekivano hakersko ime: **Nestašno Upozorenje**

### Normalizacija

Sljedeća dva zahtjeva moraju vratiti isto ime, **Usplahireni Kompajler**:

```bash
curl -X POST "http://localhost:8000/hakersko-ime" \
  -H "Content-Type: application/json" \
  -d '{"ime": "Đurđa", "prezime": "Šimić"}'

curl -X POST "http://localhost:8000/hakersko-ime" \
  -H "Content-Type: application/json" \
  -d '{"ime": "  DURDA ", "prezime": "simic"}'
```

### Crtica i apostrof

```bash
curl -X POST "http://localhost:8000/hakersko-ime" \
  -H "Content-Type: application/json" \
  -d '{"ime": "Ana-Marija", "prezime": "D'"'"'Angelo"}'
```

Očekivano hakersko ime: **Sumnjičavo Stablo**. 

### Neispravan ulaz

Svaki od ovih zahtjeva mora vratiti status `422`. Opcija `-i` ispisuje i HTTP 
zaglavlja, pa se vidi statusni kod.

```bash
# brojevi u imenu
curl -i -X POST "http://localhost:8000/hakersko-ime" \
  -H "Content-Type: application/json" \
  -d '{"ime": "Ivan123", "prezime": "Horvat"}'

# prazno ime
curl -i -X POST "http://localhost:8000/hakersko-ime" \
  -H "Content-Type: application/json" \
  -d '{"ime": "", "prezime": "Horvat"}'

# nedostaje prezime
curl -i -X POST "http://localhost:8000/hakersko-ime" \
  -H "Content-Type: application/json" \
  -d '{"ime": "Ivan"}'
```

Odgovor nakon prvog upita bi trebao izgledati ovako nekako:

```bash
HTTP/1.1 422 Unprocessable Content
date: Sat, 31 Oct 2026 18:05:40 GMT
server: uvicorn
content-length: 125
content-type: application/json
vary: Origin

{"detail":[{"type":"nedopusteni_znakovi","loc":["body","ime"],"msg":"Dopuštena su samo slova, razmak, crtica i apostrof."}]}
```

## Provjera kolizija

Kod ovakvih stvari je uvijek potrebno na neki način doći do zaključka dolazi li 
do kolizija, koliko često i s kojom raspodjelom. Ovdje je jedan heuristički pristup.
Budući da ima svega 1056 hakerskih imena, pribavljena je dovoljno velika kolekcija 
od 100 najčešćih hrvatskih imena i 100 najčešćih hrvatskih prezimena, preuzetih 
iz članka sa 
[srednja.hr](https://www.srednja.hr/novosti/vijesti/33441/imamo-novi-popis-31419-prezimena-i-5249-imena-u-hrvatskoj-i-koliko-ih-ljudi-nosi-evo-stanja-po-zupanijama/vijest).

Kombiniranjem svakog od imena sa svakim od prezimena dobije se 10000 jedinstvenih
kombinacija, a kako je svega 1056 hakerskih imena, za očekivati je da svako hakersko
ime ima cca 10 ljudi.

Napisana Python skripta `provjera_imena.py`, dakle, kombinira najčešća hrvatska 
imena i prezimena, te za svaku osobu (zapravo kombinaciju imena i prezimena) pita 
backend za hakersko ime, a na kraju ispisuje tablicu svih hakerskih imena, 
sortirano po broju osoba koje ga imaju te njihova imena i prezimena. Dakako,
ispisuje i moju poziciju u tablici. 

Ovdje je skraćeni popis, prvih nekoliko s najviše osoba, redak u kojem je autor 
ovog uratka, te nekoliko zadnjih redova, odnosno redova s hakerkim imenima koje 
posjeduje najmanje osoba. Nije teško primijetiti da raspodjela nije niti blizu 
uniformne.

| Hakersko ime | Broj osoba | Osobe |
|---|---|---|
| Mrzovoljna Iznimka | 20 | Tomislav Šimić, Tomislav Matijević, Mirjana Brkić, Damir Lukić, Vesna Popović, Martina Nikolić, Marica Tadić, Marijan Posavec, Katica Kovačić, Karlo Jurišić, Igor Pavić, Vladimir Matić, Željka Milić, Jadranka Vidović, Danijela Vukelić, Ružica Šarić, Mia Jurić, Mia Jovanović, Dragan Pavlović, Marta Martinović |
| Hrabro Sučelje | 19 | Ivan Babić, Ana Živković, Ivica Đurić, Ante Vučković, Damir Marjanović, Branko Mitrović, Mladen Ivanković, Gordana Božić, Zoran Blažević, Karlo Klarić, Davor Grgić, Anka Nikolić, Lana Matić, Mira Jovanović, Danijela Klarić, Jakov Ivanković, Mia Marković, Boris Marinović, Sandra Pavičić |
| Nervozni Algoritam | 19 | Ivan Miletić, Marija Novaković, Ivana Jurišić, Tomislav Ćosić, Mario Lučić, Maja Vučković, Milan Ivanović, Mladen Petrović, Marijan Kolar, Kata Matijević, Nikolina Jovanović, Josipa Jovanović, Miroslav Babić, Nevenka Posavec, Mia Živković, Valentina Filipović, Marta Cindrić, Mihael Bogdan, Zdenka Stanić |
| Sumnjičavi Ključ | 19 | Marija Barišić, Marija Petrić, Ana Lučić, Marko Nikolić, Željko Martinović, Željko Ivić, Ante Kos, Marica Perković, Ljubica Lončar, Matija Popović, Sara Perković, Branka Petrović, Branka Tadić, Mara Burić, Dražen Grubišić, Hrvoje Ivančić, Nevenka Božić, Ema Kovačević, Matea Novak |
| Tvrdoglavi Direktorij | 19 | Josip Tomić, Stjepan Marjanović, Stjepan Novaković, Mirjana Poljak, Katarina Jozić, Nada Ilić, Filip Mikulić, Filip Šimunović, Filip Štimac, Kristina Bačić, Jelena Vučković, Marijan Matijević, Katica Posavec, Antonio Pavić, Davor Herceg, Matej Horvat, Branka Jozić, Ankica Perković, Jasna Šarić |
| Tvrdoglavi Ključ | 19 | Ana Vukelić, Nikola Ilić, Petra Pavlović, Martina Brajković, Dragica Knežević, Jelena Jukić, Marijan Herceg, Katica Tadić, Zoran Marjanović, Kata Kralj, Marin Barić, Robert Šimić, Ljiljana Petrić, Miroslav Šimunović, Željka Mitrović, Željka Ivić, Slavica Bačić, Marta Marjanović, Mateo Tomić |
| Lijena Metoda | 18 | Ivana Ivanović, Mario Stanić, Vesna Radić, Martina Martinović, Sanja Pavičić, Branko Babić, Karlo Vuković, Davor Petrić, Vladimir Martinović, Ivanka Ivančić, Sara Popović, Sara Lučić, Matej Barišić, Ankica Horvat, Mira Matijević, Hrvoje Poljak, Boris Pavlović, Jasna Bačić |
| Mrzovoljno Polje | 18 | Petar Kovačić, Vesna Petrović, Vesna Grubišić, Marina Grubišić, Iva Bogdan, Gordana Marjanović, Marijan Klarić, Ivanka Šimić, Franjo Katić, Matej Vidović, Matej Kralj, Danijel Tomić, Zdravko Martinović, Dario Jerković, Sandra Kovačević, Sandra Tomić, Milka Vidović, Kristijan Barišić |
| Šarmantna Mreža | 18 | Josip Mitrović, Ivana Grgić, Željko Perić, Ante Blažević, Nikola Rukavina, Maja Vukelić, Kata Bačić, Nikolina Posavec, Igor Topić, Danijel Matković, Dražen Novosel, Nevenka Ivanović, Dario Ivić, Danica Bašić, Sandra Mandić, Kristijan Poljak, Zdenka Jelić, Mateo Ivić |
| ... | itd | ... |
| Nestašna Konstanta | 10 | **Vladimir Marjanović**, Marko Matijević, Marica Ivić, Jelena Ivanković, Nikolina Cindrić, Anka Lučić, Nevenka Varga, Anica Vukelić, Marta Mitrović, Matea Perković |
| ... | itd | ... |
| Dramatično Rješenje | 2 | Željka Martinović, Dario Šimić |
| Tvrdoglavi Procesor | 2 | Marijana Lukić, Matej Janković |
| Ushićeno Sklopovlje | 2 | Tomislav Varga, Lucija Brkić |
| Usplahirena Mreža | 2 | Vesna Miletić, Jakov Kovačić |
| Zaboravni Miš | 2 | Damir Bačić, Antonio Vidaković |
| Zaboravno Sklopovlje | 2 | Igor Matić, Dragan Petrović |
| Šarmantna Funkcija | 2 | Ljiljana Pavičić, Sara Špoljarić |
| Usplahireno Kućište | 1 | Stjepan Babić |
