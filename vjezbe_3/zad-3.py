import asyncio

baza_korisnika = [
    {'korisnicko_ime': 'mirko123', 'email': 'mirko123@gmail.com'},
    {'korisnicko_ime': 'maja_0x', 'email': 'majaaaaa@gmail.com'},
    {'korisnicko_ime': 'ana_anic', 'email': 'aanic@gmail.com'},
    {'korisnicko_ime': 'zdeslav032', 'email': 'deso032@gmail.com'}
]

baza_lozinka = [
    {'korisnicko_ime': 'mirko123', 'lozinka': 'super_teska_lozinka'},
    {'korisnicko_ime': 'maja_0x', 'lozinka': 's324SDFfdsj234'},
    {'korisnicko_ime': 'ana_anic', 'lozinka': 'super_teska_lozinka'},
    {'korisnicko_ime': 'zdeslav032', 'lozinka': 'deso123'}
]

async def autorizacija(korisnik_iz_baze, lozinka):
    await asyncio.sleep(2)
    korisnicko_ime = korisnik_iz_baze['korisnicko_ime']
    for zapis in baza_lozinka:
        if zapis['korisnicko_ime'] == korisnicko_ime and zapis['lozinka'] == lozinka:
            return f"Korisnik {korisnicko_ime}: Autorizacija uspješna."
    return f"Korisnik {korisnicko_ime}: Autorizacija neuspješna."

async def autentifikacija(korisnik):
    await asyncio.sleep(3)
    for korisnik_iz_baze in baza_korisnika:
        if (korisnik_iz_baze['korisnicko_ime'] == korisnik['korisnicko_ime']
                and korisnik_iz_baze['email'] == korisnik['email']):
            return await autorizacija(korisnik_iz_baze, korisnik['lozinka'])
    return f"Korisnik {korisnik['korisnicko_ime']} nije pronađen."

# Dodao sam da se, osim slanja ispravnih podataka, pošalju i neispravni podaci
# te na taj način testiraju i ostale funkcionalnosti
async def main():
    korisnik = {
        'korisnicko_ime': 'ana_anic',
        'email': 'aanic@gmail.com',
        'lozinka': 'super_teska_lozinka'
    }
    rezultat = await autentifikacija(korisnik)
    print(rezultat)
    # pogrešno korisničko ime
    korisnik = {
        'korisnicko_ime': 'ana-anic',
        'email': 'aanic@gmail.com',
        'lozinka': 'super_teska_lozinka'
    }
    rezultat = await autentifikacija(korisnik)
    print(rezultat)
    # pogrešna lozinka
    korisnik = {
        'korisnicko_ime': 'ana_anic',
        'email': 'aanic@gmail.com',
        'lozinka': 'super-teska-lozinka'
    }
    rezultat = await autentifikacija(korisnik)
    print(rezultat)

asyncio.run(main())
