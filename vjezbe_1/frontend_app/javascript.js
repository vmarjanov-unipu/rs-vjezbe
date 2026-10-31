const API_URL = "https://ghi-be.onrender.com";
const STATUS_CHECK_INTERVAL_MS = 50000;

// API zahtjev
async function apiRequest(path, body) {
  const options = body === undefined
    ? { method: "GET" }
    : {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      };

  let response;
  try {
    response = await fetch(API_URL + path, options);
  } catch (error) {
    throw new Error("Poslužitelj nije dostupan. Provjeri je li backend pokrenut.");
  }

  let data = null;
  try {
    data = await response.json();
  } catch (error) {
    // Odgovor nije JSON; poruka o grešci složit će se iz statusnog koda.
  }

  if (!response.ok) {
    throw new Error(formatError(response.status, data));
  }
  return data;
}

// FastAPI greške validacije (422) vraća kao listu, npr.
// [{ "loc": ["body", "ime"], "msg": "..." }], pa ih spajamo u jednu poruku.
function formatError(status, data) {
  if (status === 422 && data && Array.isArray(data.detail)) {
    return data.detail
      .map((item) => {
        const field = (item.loc || []).filter((part) => part !== "body").join(" ");
        return field ? `${field}: ${item.msg}` : item.msg;
      })
      .join(" ");
  }
  if (data && typeof data.detail === "string") {
    return data.detail;
  }
  return `Poslužitelj je vratio grešku ${status}.`;
}

// Svakih 5 sekundi provjeravamo je li poslužitelj živ

const statusDot = document.getElementById("status-dot");
const statusText = document.getElementById("status-text");

async function checkStatus() {
  try {
    const data = await apiRequest("/status");
    const isOnline = data && data.status === "ok";
    statusDot.className = "status-dot " + (isOnline ? "online" : "offline");
    statusText.textContent = isOnline ? "Poslužitelj radi" : "Poslužitelj ne odgovara ispravno";
  } catch (error) {
    statusDot.className = "status-dot offline";
    statusText.textContent = "Poslužitelj nije dostupan";
  }
}

// Dohvatimo sva polja za generiranje hakerskog imena i zovemo poslužitelj
// plus ponešto pomoćnih funkcija

const form = document.getElementById("name-form");
const submitButton = document.getElementById("submit-button");
const errorElement = document.getElementById("error");
const resultElement = document.getElementById("result");
const resultPerson = document.getElementById("result-person");
const hackerName = document.getElementById("hacker-name");

function showError(message) {
  errorElement.textContent = message;
  errorElement.hidden = false;
}

function hideError() {
  errorElement.textContent = "";
  errorElement.hidden = true;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  hideError();
  resultElement.hidden = true;

  const firstName = document.getElementById("first-name").value.trim();
  const lastName = document.getElementById("last-name").value.trim();

  if (!firstName || !lastName) {
    showError("Upiši i ime i prezime.");
    return;
  }

  submitButton.disabled = true;
  try {
    const data = await apiRequest("/hakersko-ime", { ime: firstName, prezime: lastName });
    resultPerson.textContent = `${data.ime} ${data.prezime} je`;
    hackerName.textContent = data.hakersko_ime;
    resultElement.hidden = false;
  } catch (error) {
    showError(error.message);
  } finally {
    submitButton.disabled = false;
  }
});

// Vežemo se i polijećemo!

checkStatus();
setInterval(checkStatus, STATUS_CHECK_INTERVAL_MS);
