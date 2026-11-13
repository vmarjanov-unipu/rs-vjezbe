import asyncio, time

async def fetch_data(param):
    print(f"Nešto radim s {param}...")
    await asyncio.sleep(param)
    print(f'Dovršio sam s {param}.')
    return f"Rezultat za {param}"

async def main():
    task1 = asyncio.create_task(fetch_data(1))  # schedule
    task2 = asyncio.create_task(fetch_data(2))  #schedule
    result1 = await task1
    print("Fetch 1 uspješno završen.")
    # task1 je završio nakon cca 1 sekunde, a task2 treba još cca 1 sekundu,
    # pa je nekako najjednostavnije da "spavamo" 1 sekundu i taman kada se probudimo 
    # task2 je već stigao i to je to. Dakako, ovakve stvari ne radimo na produkciji...
    await asyncio.sleep(1)
    return [result1]

t1 = time.perf_counter()
results = asyncio.run(main()) # pokretanje event loop-a
t2 = time.perf_counter()
print(results)
print(f"Vrijeme izvođenja {t2 - t1:.2f} sekunde")
