import asyncio
import random

# Broj je paran ukoliko nema ostatka pri dijeljenju s 2
async def provjeri_parnost(broj):
    await asyncio.sleep(2)
    if broj % 2 == 0:
        return f"Broj {broj} je paran."
    return f"Broj {broj} je neparan."

# Ovo nije dio zadatka, ali u nekim bi situacijama bilo zgodno ispisati pripadajući
# Fibonaccijev broj; dakako, korištenje rekurzije f(n-1) + f(n-2) ovdje ne dolazi u 
# obzir zbog eskponencijalne složenosti
async def fibonacci(n):
    await asyncio.sleep(2)
    if n < 0:
        raise ValueError("Broj mora biti nenegativan.")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return f"F({n}) = {a}"

async def main():
    brojevi = [random.randint(1, 100) for _ in range(10)]
    zadaci = [asyncio.create_task(provjeri_parnost(broj)) for broj in brojevi]
    rezultati = await asyncio.gather(*zadaci)
    for rezultat in rezultati:
        print(rezultat)

asyncio.run(main())
