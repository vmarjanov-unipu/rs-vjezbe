"""Liste riječi od kojih se slaže hakersko ime."""

MASCULINE = "m"
FEMININE = "z"
NEUTER = "s"

# Svaki pridjev u sva tri roda: (muški, ženski, srednji).
ADJECTIVES = [
    ("usplahireni", "usplahirena", "usplahireno"),
    ("pospani", "pospana", "pospano"),
    ("zbunjeni", "zbunjena", "zbunjeno"),
    ("nervozni", "nervozna", "nervozno"),
    ("lijeni", "lijena", "lijeno"),
    ("mrzovoljni", "mrzovoljna", "mrzovoljno"),
    ("zaboravni", "zaboravna", "zaboravno"),
    ("tvrdoglavi", "tvrdoglava", "tvrdoglavo"),
    ("sramežljivi", "sramežljiva", "sramežljivo"),
    ("dramatični", "dramatična", "dramatično"),
    ("pričljivi", "pričljiva", "pričljivo"),
    ("znatiželjni", "znatiželjna", "znatiželjno"),
    ("sumnjičavi", "sumnjičava", "sumnjičavo"),
    ("smeteni", "smetena", "smeteno"),
    ("veseli", "vesela", "veselo"),
    ("razigrani", "razigrana", "razigrano"),
    ("nasmijani", "nasmijana", "nasmijano"),
    ("zaljubljeni", "zaljubljena", "zaljubljeno"),
    ("ushićeni", "ushićena", "ushićeno"),
    ("nestašni", "nestašna", "nestašno"),
    ("šarmantni", "šarmantna", "šarmantno"),
    ("hrabri", "hrabra", "hrabro"),
]

# Indeks oblika pridjeva u n-torki za svaki rod.
GENDER_INDEX = {MASCULINE: 0, FEMININE: 1, NEUTER: 2}

# Svaka imenica s oznakom roda.
NOUNS = [
    # Ženski rod
    ("funkcija", FEMININE),
    ("varijabla", FEMININE),
    ("petlja", FEMININE),
    ("konstanta", FEMININE),
    ("lozinka", FEMININE),
    ("iznimka", FEMININE),
    ("baza", FEMININE),
    ("tipkovnica", FEMININE),
    ("memorija", FEMININE),
    ("aplikacija", FEMININE),
    ("mreža", FEMININE),
    ("tablica", FEMININE),
    ("konzola", FEMININE),
    ("rekurzija", FEMININE),
    ("klasa", FEMININE),
    ("metoda", FEMININE),
    # Muški rod
    ("procesor", MASCULINE),
    ("kompajler", MASCULINE),
    ("pokazivač", MASCULINE),
    ("algoritam", MASCULINE),
    ("poslužitelj", MASCULINE),
    ("miš", MASCULINE),
    ("ključ", MASCULINE),
    ("piksel", MASCULINE),
    ("monitor", MASCULINE),
    ("čip", MASCULINE),
    ("objekt", MASCULINE),
    ("vatrozid", MASCULINE),
    ("upit", MASCULINE),
    ("direktorij", MASCULINE),
    ("terminal", MASCULINE),
    ("program", MASCULINE),
    # Srednji rod
    ("sučelje", NEUTER),
    ("stablo", NEUTER),
    ("polje", NEUTER),
    ("računalo", NEUTER),
    ("rješenje", NEUTER),
    ("spremište", NEUTER),
    ("okruženje", NEUTER),
    ("zaglavlje", NEUTER),
    ("sklopovlje", NEUTER),
    ("čvorište", NEUTER),
    ("kućište", NEUTER),
    ("napajanje", NEUTER),
    ("proširenje", NEUTER),
    ("ažuriranje", NEUTER),
    ("upozorenje", NEUTER),
    ("šifriranje", NEUTER),
]
