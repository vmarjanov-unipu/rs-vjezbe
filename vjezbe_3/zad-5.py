import asyncio

osjetljivi_podaci = [
    {'prezime': 'Ivić', 'broj_kartice': '1234567812345678', 'CVV': '123'},
    {'prezime': 'Anić', 'broj_kartice': '8765432187654321', 'CVV': '456'},
    {'prezime': 'Marić', 'broj_kartice': '1111222233334444', 'CVV': '789'}
]

# hash() je zabavan jer svaki put vraća drugu vrijednost :-) 
async def secure_data(podaci):
    await asyncio.sleep(3)
    return {
        'prezime': podaci['prezime'],
        'broj_kartice': str(hash(podaci['broj_kartice'])),
        'CVV': str(hash(podaci['CVV']))
    }

async def main():
    zadaci = [asyncio.create_task(secure_data(podaci)) for podaci in osjetljivi_podaci]
    rezultati = await asyncio.gather(*zadaci)
    for rezultat in rezultati:
        print(rezultat)

asyncio.run(main())
