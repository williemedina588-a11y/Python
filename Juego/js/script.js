// 1. Referencias a los elementos del HTML
const campoNumero = document.getElementById("campoNumero");
const btnAdivinar = document.getElementById("btnAdivinar");
const btnNueva = document.getElementById("btnNueva");
const mensaje = document.getElementById("mensaje");
const intentos = document.getElementById("intentos");

// 2. Variables del juego
let numeroSecreto;
let intentosRestantes;
let terminada;

// 3. Función que deja el juego listo para empezar
function nuevaPartida() {
  numeroSecreto = Math.floor(Math.random() * 10) + 1;
  intentosRestantes = 3;
  terminada = false;

  campoNumero.value = "";
  campoNumero.disabled = false;
  btnAdivinar.disabled = false;
  intentos.textContent = intentosRestantes;
  mensaje.textContent = "Escribe un número y pulsa Adivinar.";
  mensaje.className = "";

  console.log("Número secreto (solo para pruebas):", numeroSecreto);
}

// Muestra un mensaje; "clase" puede ser "ok" (verde) o "mal" (rojo)
function mostrar(texto, clase) {
  mensaje.textContent = texto;
  mensaje.className = clase || "";
}

// Termina la partida: ya no se puede seguir adivinando
function terminar() {
  terminada = true;
  campoNumero.disabled = true;
  btnAdivinar.disabled = true;
}

// Se ejecuta al pulsar "Adivinar"
function adivinar() {
  if (terminada) return;

  const texto = campoNumero.value.trim();
  const numero = Number(texto);

  // Campo vacío: no consume intentos
  if (texto === "") {
    mostrar("Debes ingresar un número", "mal");
    return;
  }

  // Debe ser un entero entre 1 y 10: tampoco consume intentos
  if (!Number.isInteger(numero) || numero < 1 || numero > 10) {
    mostrar("Ingresa un número entero entre 1 y 10", "mal");
    campoNumero.value = "";
    return;
  }

  // Cada respuesta válida consume un intento
  intentosRestantes--;
  intentos.textContent = intentosRestantes;

  // Primero se comprueba el acierto, aunque sea el último intento
  if (numero === numeroSecreto) {
    mostrar("¡Felicidades! Adivinaste el número secreto", "ok");
    terminar();
  } else if (intentosRestantes === 0) {
    mostrar("Has perdido. El número secreto era " + numeroSecreto, "mal");
    terminar();
  } else if (numero < numeroSecreto) {
    mostrar("El número secreto es mayor.");
  } else {
    mostrar("El número secreto es menor.");
  }

    campoNumero.value = "";
  if (!terminada) campoNumero.focus();
}

// 4. El botón "Nueva partida" y el inicio automático
btnNueva.addEventListener("click", nuevaPartida);
nuevaPartida();

btnAdivinar.addEventListener("click", adivinar);
campoNumero.addEventListener("keydown", function (e) {
  if (e.key === "Enter") adivinar();
});

btnAdivinar.addEventListener("click", adivinar);
campoNumero.addEventListener("keydown", function (e) {
  if (e.key === "Enter") adivinar();
});