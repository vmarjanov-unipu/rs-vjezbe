"""Generator hakerskih imena – REST API."""

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from generator import generate_hacker_name
from models import HackerNameRequest, HackerNameResponse, StatusResponse

app = FastAPI(
    title="Generator hakerskih imena",
    description="Iz imena i prezimena osobe vraća njezino šaljivo hakersko ime.",
    version="1.0.0",
)

# Frontend radi na drugoj adresi, pa dopuštamo sva ishodišta.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hrvatske poruke za ugrađene greške validacije (naše vlastite već su na hrvatskom).
_VALIDATION_MESSAGES = {
    "missing": "Polje je obavezno.",
    "string_type": "Vrijednost mora biti tekst.",
    "json_invalid": "Tijelo zahtjeva nije ispravan JSON.",
    "model_attributes_type": "Tijelo zahtjeva mora biti JSON objekt.",
    "dict_type": "Tijelo zahtjeva mora biti JSON objekt.",
}
_OWN_ERROR_TYPES = {"prazno", "predugo", "nedopusteni_znakovi", "bez_slova"}

_HTTP_MESSAGES = {
    404: "Tražena putanja ne postoji.",
    405: "Metoda nije dopuštena za ovu putanju.",
}


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        error_type = error.get("type", "")
        if error_type in _OWN_ERROR_TYPES:
            message = error["msg"]
        else:
            message = _VALIDATION_MESSAGES.get(error_type, "Neispravna vrijednost.")
        errors.append({"type": error_type, "loc": error.get("loc", []), "msg": message})
    return JSONResponse(status_code=422, content=jsonable_encoder({"detail": errors}))


@app.exception_handler(StarletteHTTPException)
async def http_error_handler(request: Request, exc: StarletteHTTPException):
    message = _HTTP_MESSAGES.get(exc.status_code, "Došlo je do greške.")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": message},
        headers=getattr(exc, "headers", None),
    )


@app.post("/hakersko-ime", response_model=HackerNameResponse)
def create_hacker_name(person: HackerNameRequest) -> HackerNameResponse:
    """Izračunava hakersko ime za jednu osobu."""
    return HackerNameResponse(
        ime=person.ime,
        prezime=person.prezime,
        hakersko_ime=generate_hacker_name(person.ime, person.prezime),
    )


@app.get("/status", response_model=StatusResponse)
def get_status() -> StatusResponse:
    """Provjera je li servis živ."""
    return StatusResponse(status="ok")
