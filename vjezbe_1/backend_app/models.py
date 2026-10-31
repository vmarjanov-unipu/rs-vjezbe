"""Modeli zahtjeva i odgovora."""

import re

from pydantic import BaseModel, field_validator
from pydantic_core import PydanticCustomError

MAX_NAME_LENGTH = 50

# Dopuštena su slova (uključujući hrvatska), razmak, crtica i apostrof.
# [^\W\d_] je "bilo koje Unicode slovo".
_ALLOWED_NAME = re.compile(r"(?:[^\W\d_]|[ '\-])+")
_HAS_LETTER = re.compile(r"[^\W\d_]")


def _validate_name(value: str) -> str:
    value = value.strip()
    if not value:
        raise PydanticCustomError("prazno", "Polje ne smije biti prazno.")
    if len(value) > MAX_NAME_LENGTH:
        raise PydanticCustomError(
            "predugo",
            "Polje smije imati najviše {max} znakova.",
            {"max": MAX_NAME_LENGTH},
        )
    if not _ALLOWED_NAME.fullmatch(value):
        raise PydanticCustomError(
            "nedopusteni_znakovi",
            "Dopuštena su samo slova, razmak, crtica i apostrof.",
        )
    if not _HAS_LETTER.search(value):
        raise PydanticCustomError("bez_slova", "Polje mora sadržavati barem jedno slovo.")
    return value


class HackerNameRequest(BaseModel):
    ime: str
    prezime: str

    @field_validator("ime", "prezime")
    @classmethod
    def check_name(cls, value: str) -> str:
        return _validate_name(value)


class HackerNameResponse(BaseModel):
    ime: str
    prezime: str
    hakersko_ime: str


class StatusResponse(BaseModel):
    status: str
