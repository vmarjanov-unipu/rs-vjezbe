import asyncio

async def dohvati_podatke():
    await asyncio.sleep(3)
    podaci = [i for i in range(1, 11)]
    return podaci

async def main():
	print("Dohvaćam podatke...")
	podaci = await dohvati_podatke()
	print("Podaci dohvaćeni.")
	print(podaci)

asyncio.run(main())
