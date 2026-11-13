# Zadatak 7

**Objasnite korak po korak kako se ponaša *event loop*** (kako se raspoređuju, izvršavaju i dovršavaju
korutine te koja su njihova stanja u različitim fazama izvođenja) na sljedećem primjeru:

```python
import asyncio

async def timer(name, delay):
    for i in range(delay, 0, -1):
        print(f'{name}: {i} sekundi preostalo...')
        await asyncio.sleep(1)
    print(f'{name}: Vrijeme je isteklo!')

async def main():
    timers = [
        asyncio.create_task(timer('Timer 1', 3)),
        asyncio.create_task(timer('Timer 2', 5)),
        asyncio.create_task(timer('Timer 3', 7))
    ]

    await asyncio.gather(*timers)

asyncio.run(main())
```

## 1. Pokretanje

`asyncio.run(main())` stvara novi event loop, od korutine `main()` napravi Task i zakaže ga. Event loop pokreće `main()`, stanje je **RUNNING**

## 2. Zakazivanje taskova (unutar `main`)

Tri poziva `asyncio.create_task(timer(...))` od korutina `timer('Timer 1', 3)`, `timer('Timer 2', 5)` i `timer('Timer 3', 7)` naprave Task objekte i stave ih u red event loopa. Taskovi su u stanju **PENDING** (zakazani, ali se još ne izvršavaju). `create_task` ne pokreće korutinu odmah, samo je zakazuje.

## 3. `await asyncio.gather(*timers)`

`gather` vraća awaitable koji čeka da svi taskovi završe. Na `await`-u `main()` predaje kontrolu event loopu i suspendira se. Nastavit će tek kada sva tri timera završe.

## 4. Izvršavanje po sekundama

### t = 0 s

Event loop redom pokreće zakazane taskove (redoslijedom kojim su zakazani). Svaki ispiše poruku, dođe do `await asyncio.sleep(1)`, suspendira se i vrati kontrolu loopu:

```
Timer 1: 3 sekundi preostalo...
Timer 2: 5 sekundi preostalo...
Timer 3: 7 sekundi preostalo...
```

Sva tri taska sada čekaju na `sleep`. Event loop nema ništa za izvršiti pa čeka da istekne prvi `sleep`.

### t = 1 s

Sva tri `sleep`-a istječu (gotovo) istovremeno. Event loop redom nastavlja (resume) svaki task od mjesta gdje je stao:

```
Timer 1: 2 sekundi preostalo...
Timer 2: 4 sekundi preostalo...
Timer 3: 6 sekundi preostalo...
```

Svaki ponovno dođe do `sleep(1)` i suspendira se.

### t = 2 s

```
Timer 1: 1 sekundi preostalo...
Timer 2: 3 sekundi preostalo...
Timer 3: 5 sekundi preostalo...
```

### t = 3 s

Timer 1 izlazi iz petlje. Korutina se vraća (`return None`), pa Task 1 prelazi u stanje **FINISHED** (DONE).

```
Timer 1: Vrijeme je isteklo!
Timer 2: 2 sekundi preostalo...
Timer 3: 4 sekundi preostalo...
```

`gather` i dalje čeka jer nisu svi taskovi gotovi.

### t = 4 s

```
Timer 2: 1 sekundi preostalo...
Timer 3: 3 sekundi preostalo...
```

### t = 5 s

Task 2 prelazi u stanje **FINISHED**.

```
Timer 2: Vrijeme je isteklo!
Timer 3: 2 sekundi preostalo...
```

### t = 6 s

```
Timer 3: 1 sekundi preostalo...
```

### t = 7 s

Task 3 prelazi u stanje **FINISHED**.

```
Timer 3: Vrijeme je isteklo!
```

Sada su svi taskovi gotovi, pa `gather` završava i vraća listu rezultata `[None, None, None]`. Event loop nastavlja `main()` nakon `await`-a.

## 5. Završetak

`main()` nema više koda pa vraća `None`, a main Task prelazi u stanje **FINISHED**. `asyncio.run()` zatvara event loop i program završava.

## Komentar

Pretpostavljam da je ovdje zadatak zapravo da se pokaže razumijevanje konkurentnog izvršavanja zadataka.

Ukupno trajanje je cca 7 sekundi (trajanje najdužeg timera), a ne 3 + 5 + 7 = 15 sekundi, jer se timeri izvršavaju konkurentno.

Konkurentnost je moguća jer svaki `await asyncio.sleep(1)` predaje kontrolu event loopu, koji u međuvremenu izvršava ostale taskove (kooperativni multitasking u jednoj dretvi).

Nadam se da nisam ništa promašio u objašnjenju.