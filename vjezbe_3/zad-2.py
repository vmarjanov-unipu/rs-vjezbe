import asyncio
import time
import json

async def dohvati_korisnike():
    await asyncio.sleep(3)
    return [
        {'id': 1, 'ime': 'Ivan', 'prezime': 'Ivić', 'email': 'iivic@example.com'},
        {'id': 2, 'ime': 'Ana', 'prezime': 'Anić', 'email': 'aanic@example.com'},
        {'id': 3, 'ime': 'Marko', 'prezime': 'Marković', 'email': 'mmaric@example.com'},
    ]

async def dohvati_proizvode():
    await asyncio.sleep(5)
    return [
        {'id': 1, 'naziv': 'Laptop', 'cijena': 1599.99},
        {'id': 2, 'naziv': 'Miš', 'cijena': 19.99},
        {'id': 3, 'naziv': 'Tipkovnica', 'cijena': 49.99},
    ]

# Dodao sam json.dumps(json, indent=4) za prettyprint JSON-a.
# Zbog json.dumps() bi print ispisao Unicode sekvence umjesto hrvatskih palatala, 
# a da se to spriječi se kao parametar doda ensure_ascii=False
async def main():
    print("Dohvaćam podatke...")
    korisnici, proizvodi = await asyncio.gather(dohvati_korisnike(), dohvati_proizvode())
    print("\nKORISNICI")
    print(json.dumps(korisnici, indent=4, ensure_ascii=False))
    print("\nPROIZVODI")
    print(json.dumps(proizvodi, indent=4, ensure_ascii=False))

# Osim što ćemo pokrenuti, pokazat ćemo i da se zbilja izvršava cca 5 sekundi
t1 = time.perf_counter()
asyncio.run(main())
t2 = time.perf_counter()
print(f"\nVrijeme izvođenja: {t2 - t1:.4f} sekundi")
