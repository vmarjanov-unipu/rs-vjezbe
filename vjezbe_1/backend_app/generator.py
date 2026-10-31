"""Normalizacija imena, hash i slaganje pridjeva s imenicom."""

import hashlib
import unicodedata

from words import ADJECTIVES, GENDER_INDEX, NOUNS

# NFKD ne rastavlja đ/Đ na osnovno slovo i kvačicu, pa ih mapiramo ručno.
_SPECIAL_LETTERS = str.maketrans({"đ": "d", "Đ": "d"})


def normalize(text: str) -> str:
    """Svodi ime na oblik neovisan o razmacima, velikim slovima i dijakriticima."""
    text = " ".join(text.split()).lower().translate(_SPECIAL_LETTERS)
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(char for char in decomposed if not unicodedata.combining(char))


def generate_hacker_name(first_name: str, last_name: str) -> str:
    """Vraća hakersko ime oblika 'Pridjev Imenica', uvijek isto za istu osobu."""
    key = f"{normalize(first_name)}|{normalize(last_name)}"
    # Ne koristimo ugrađeni hash() jer je za stringove randomiziran po procesu.
    digest = hashlib.sha256(key.encode("utf-8")).digest()

    noun_index = int.from_bytes(digest[0:8], "big") % len(NOUNS)
    adjective_index = int.from_bytes(digest[8:16], "big") % len(ADJECTIVES)

    noun, gender = NOUNS[noun_index]
    adjective = ADJECTIVES[adjective_index][GENDER_INDEX[gender]]

    return f"{adjective.capitalize()} {noun.capitalize()}"
