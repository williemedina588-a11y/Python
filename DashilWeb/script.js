const sesionActiva = localStorage.getItem("dashil_sesion");

if (sesionActiva !== "true") {
    window.location.href = "Login/login.html";
}

const profileButton =
    document.getElementById("profileButton");

const profileMenu =
    document.getElementById("profileMenu");

const logoutButton =
    document.getElementById("logoutButton");






/* ABRIR / CERRAR MENÚ */

if (profileButton && profileMenu) {

    profileButton.addEventListener("click", () => {

        profileMenu.classList.toggle("active");

    });

}


/* CERRAR SESIÓN */

if (logoutButton) {

    logoutButton.addEventListener("click", (event) => {

        event.preventDefault();

        localStorage.removeItem("dashil_sesion");
        localStorage.removeItem("dashil_usuario_id");
        localStorage.removeItem("dashil_nombre");
        localStorage.removeItem("dashil_email");
        localStorage.removeItem("dashil_chat_actual");

        const paginaLogin = new URL(
            "Login/login.html",
            window.location.href
        );

        window.location.replace(paginaLogin.href);

    });

}

const nombreUsuario =
    localStorage.getItem("dashil_nombre");

const userName =
    document.getElementById("userName");

const userAvatar =
    document.getElementById("userAvatar");


if (nombreUsuario) {

    if (userName) {
        userName.textContent = nombreUsuario;
    }

    if (userAvatar) {
        userAvatar.textContent =
            nombreUsuario.charAt(0).toUpperCase();
    }

}

const input = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");
const messages = document.getElementById("messages");
const welcome = document.getElementById("welcome");
const newChat = document.getElementById("newChat");

const historyContainer =
    document.querySelector(".history");

const pinnedChats =
    document.getElementById("pinnedChats");

const normalChats =
    document.getElementById("normalChats");

const pinnedSection =
    document.getElementById("pinnedSection");

const normalSection =
    document.getElementById("normalSection");


/* =========================
   VARIABLES
========================= */

let chatActual = null;

const CHAT_STORAGE_KEY =
    "dashil_chat_actual";

function obtenerEncabezadosUsuario(incluirJson = false) {

    const encabezados = {
        "X-Usuario-Id": localStorage.getItem(
            "dashil_usuario_id"
        ) || ""
    };

    if (incluirJson) {
        encabezados["Content-Type"] =
            "application/json";
    }

    return encabezados;
}


/* =========================
   INICIAR APLICACIÓN
========================= */

document.addEventListener(
    "DOMContentLoaded",
    async function() {

        await cargarConversaciones();

        const chatGuardado =
            localStorage.getItem(
                CHAT_STORAGE_KEY
            );


        if (chatGuardado) {

            await cargarConversacion(
                chatGuardado
            );

        } else {

            mostrarBienvenida();

        }

        ajustarAltura();
    }
);


/* =========================
   OBTENER CONVERSACIONES
========================= */

async function cargarConversaciones() {

    try {

        const respuesta = await fetch(
            "http://127.0.0.1:5000/api/conversaciones",
            {
                headers: obtenerEncabezadosUsuario()
            }
        );

        const conversaciones = await respuesta.json();

        pinnedChats.innerHTML = "";
        normalChats.innerHTML = "";

        conversaciones.forEach(
            conversacion => {
                crearElementoConversacion(conversacion);
            }
        );

        if (pinnedChats.children.length > 0) {

            pinnedSection.style.display = "block";

        } else {

            pinnedSection.style.display = "none";

        }

        if (normalChats.children.length > 0) {

            normalSection.style.display = "block";

        } else {

            normalSection.style.display = "none";

        }

    } catch (error) {

        console.error(
            "No se pudieron cargar las conversaciones:",
            error
        );

    }

}

/* =========================
   CREAR ELEMENTO HISTORIAL
========================= */

function crearElementoConversacion(
    conversacion
) {

    const elemento =
        document.createElement("div");


    elemento.className =
        "conversation";


    elemento.dataset.chatId =
        conversacion.id;


    /* =========================
       ICONO DE CHAT
    ========================= */

    const icono =
        document.createElement("span");

    icono.className =
        "conversation-icon";

    icono.textContent =
        "💬";


    /* =========================
       TITULO
    ========================= */

    const titulo =
        document.createElement("span");

    titulo.className =
        "conversation-title";

    titulo.textContent =
        conversacion.titulo;


    /* =========================
       ICONO DE FIJADO
    ========================= */

    const fijado =
        document.createElement("span");

    fijado.className =
        "conversation-pin";


    if (conversacion.fijado) {

        fijado.textContent =
            "📌";

    }


    /* =========================
       BOTÓN DE OPCIONES
    ========================= */

    const menu =
        document.createElement("button");

    menu.className =
        "conversation-menu";

    menu.textContent =
        "⋯";

    menu.title =
        "Opciones";


    /* =========================
       CONSTRUIR ELEMENTO
    ========================= */

    elemento.appendChild(
        icono
    );


    elemento.appendChild(
        titulo
    );


    elemento.appendChild(
        fijado
    );


    elemento.appendChild(
        menu
    );


    /* =========================
       ABRIR CONVERSACIÓN
    ========================= */

    elemento.addEventListener(
        "click",
        function(event) {

            if (
                event.target === menu
            ) {

                return;

            }


            cargarConversacion(
                conversacion.id
            );

        }
    );


    /* =========================
       MENÚ
    ========================= */

    menu.addEventListener(
        "click",
        function(event) {

            event.stopPropagation();


            mostrarMenuConversacion(
                elemento,
                conversacion
            );

        }
    );


    if (conversacion.fijado) {

        pinnedChats.appendChild(
            elemento
        );

    } else {

        normalChats.appendChild(
            elemento
        );

    }
}

/* =========================
   MONSTRAR MENU CONVERSACIÓN
========================= */
function mostrarMenuConversacion(
    elemento,
    conversacion
) {

    const menuAnterior =
        document.querySelector(
            ".conversation-options"
        );


    if (menuAnterior) {

        menuAnterior.remove();

    }


    const menu =
        document.createElement("div");


    menu.className =
        "conversation-options";


    const textoFijar =
        conversacion.fijado
            ? "📌 Desfijar"
            : "📌 Fijar";


    menu.innerHTML = `

        <button class="rename-chat">
            ✏️ Renombrar
        </button>

        <button class="pin-chat">
            ${textoFijar}
        </button>

        <button class="delete-chat">
            🗑️ Eliminar
        </button>

    `;


    elemento.appendChild(
        menu
    );


    /* =========================
       RENOMBRAR
    ========================= */

    menu.querySelector(
        ".rename-chat"
    ).addEventListener(
        "click",
        function(event) {

            event.stopPropagation();


            renombrarConversacion(
                conversacion.id,
                conversacion.titulo
            );


            menu.remove();

        }
    );


    /* =========================
       FIJAR
    ========================= */

    menu.querySelector(
        ".pin-chat"
    ).addEventListener(
        "click",
        function(event) {

            event.stopPropagation();


            fijarConversacion(
                conversacion.id
            );


            menu.remove();

        }
    );


    /* =========================
       ELIMINAR
    ========================= */

    menu.querySelector(
        ".delete-chat"
    ).addEventListener(
        "click",
        function(event) {

            event.stopPropagation();


            eliminarConversacion(
                conversacion.id
            );


            menu.remove();

        }
    );
}

/* =========================
   RENOMBRAR CONVERSACIÓN
========================= */

async function renombrarConversacion(
    chatId,
    tituloActual
) {

    const nuevoTitulo =
        prompt(
            "Nuevo nombre de la conversación:",
            tituloActual
        );


    if (
        nuevoTitulo === null
    ) {

        return;

    }


    const titulo =
        nuevoTitulo.trim();


    if (!titulo) {

        alert(
            "El nombre no puede estar vacío."
        );

        return;

    }


    try {

        const respuesta =
            await fetch(
                `http://127.0.0.1:5000/api/conversaciones/${chatId}`,
                {
                    method: "PUT",

                    headers: obtenerEncabezadosUsuario(true),

                    body: JSON.stringify({
                        titulo: titulo
                    })
                }
            );


        const datos =
            await respuesta.json();


        if (!respuesta.ok) {

            throw new Error(
                datos.error
            );

        }


        await cargarConversaciones();


    } catch (error) {

        console.error(
            "Error renombrando:",
            error
        );


        alert(
            "No se pudo renombrar la conversación."
        );

    }
}

/* =========================
   FIJAR CONVERSACIÓN
========================= */

async function fijarConversacion(
    chatId
) {

    try {

        const respuesta =
            await fetch(
                `http://127.0.0.1:5000/api/conversaciones/${chatId}/fijar`,
                {
                    method: "PUT",
                    headers: obtenerEncabezadosUsuario()
                }
            );


        const datos =
            await respuesta.json();


        if (!respuesta.ok) {

            throw new Error(
                datos.error
            );

        }


        await cargarConversaciones();


    } catch (error) {

        console.error(
            "Error fijando conversación:",
            error
        );


        alert(
            error.message ||
            "No se pudo cambiar el estado de la conversación."
        );

    }
}

/* =========================
   ELIMINAR CONVERSACIÓN
========================= */

async function eliminarConversacion(
    chatId
) {

    const confirmar =
        confirm(
            "¿Quieres eliminar esta conversación?"
        );


    if (!confirmar) {

        return;

    }


    try {

        const respuesta =
            await fetch(
                `http://127.0.0.1:5000/api/conversaciones/${chatId}`,
                {
                    method: "DELETE",
                    headers: obtenerEncabezadosUsuario()
                }
            );


        const datos =
            await respuesta.json();


        if (!respuesta.ok) {

            throw new Error(
                datos.error
            );

        }


        /*
           Si eliminamos el chat actual
        */

        if (
            chatActual === chatId
        ) {

            chatActual = null;


            localStorage.removeItem(
                CHAT_STORAGE_KEY
            );


            messages.innerHTML = "";


            mostrarBienvenida();

        }


        await cargarConversaciones();


    } catch (error) {

        console.error(
            "Error eliminando:",
            error
        );


        alert(
            "No se pudo eliminar la conversación."
        );

    }
}

/* =========================
   CREAR NUEVA CONVERSACIÓN
========================= */

async function crearNuevaConversacion() {

    try {

        const respuesta = await fetch(
            "http://127.0.0.1:5000/api/conversaciones",
            {
                method: "POST",
                headers: obtenerEncabezadosUsuario()
            }
        );


        const datos =
            await respuesta.json();


        chatActual =
            datos.id;


        localStorage.setItem(
            CHAT_STORAGE_KEY,
            chatActual
        );


        messages.innerHTML = "";

        mostrarBienvenida();

        input.value = "";

        ajustarAltura();


        await cargarConversaciones();


    } catch (error) {

        console.error(
            "No se pudo crear la conversación:",
            error
        );

    }
}


/* =========================
   CARGAR CONVERSACIÓN
========================= */

async function cargarConversacion(
    chatId
) {

    try {

        const respuesta = await fetch(
            `http://127.0.0.1:5000/api/conversaciones/${chatId}`,
            {
                headers: obtenerEncabezadosUsuario()
            }
        );


        if (!respuesta.ok) {

            throw new Error(
                "La conversación no existe."
            );

        }


        const chat =
            await respuesta.json();


        chatActual =
            chatId;


        localStorage.setItem(
            CHAT_STORAGE_KEY,
            chatId
        );


        messages.innerHTML = "";


        if (
            !chat.mensajes ||
            chat.mensajes.length === 0
        ) {

            mostrarBienvenida();

            return;

        }


        welcome.style.display =
            "none";


        chat.mensajes.forEach(
            mensaje => {

                if (
                    mensaje.rol === "usuario"
                ) {

                    agregarMensaje(
                        "Tú",
                        "Tú",
                        mensaje.contenido,
                        false
                    );

                } else {

                    agregarMensaje(
                        "Dashil",
                        "D",
                        mensaje.contenido,
                        false
                    );

                }

            }
        );


        desplazarseAbajo();


    } catch (error) {

        console.error(
            "Error cargando conversación:",
            error
        );

    }
}


/* =========================
   MOSTRAR BIENVENIDA
========================= */

function mostrarBienvenida() {

    welcome.style.display =
        "flex";

}


/* =========================
   ENVIAR MENSAJE
========================= */

async function enviarMensaje() {

    const texto =
        input.value.trim();


    if (texto === "") {

        return;

    }


    // Si no tenemos conversación,
    // crear una automáticamente

    if (!chatActual) {

        try {

            const respuesta =
                await fetch(
                    "http://127.0.0.1:5000/api/conversaciones",
                    {
                        method: "POST",
                        headers: obtenerEncabezadosUsuario()
                    }
                );


            const datos =
                await respuesta.json();


            chatActual =
                datos.id;


            localStorage.setItem(
                CHAT_STORAGE_KEY,
                chatActual
            );

        } catch (error) {

            console.error(
                "No se pudo crear el chat:",
                error
            );

            return;

        }

    }


    welcome.style.display =
        "none";


    agregarMensaje(
        "Tú",
        "Tú",
        texto
    );


    input.value = "";

    ajustarAltura();

    desplazarseAbajo();


    sendButton.disabled =
        true;


    const pensando =
        document.createElement("div");


    pensando.className =
        "message";


    pensando.id =
        "dashilPensando";


    pensando.innerHTML = `
        <div class="message-avatar">
            D
        </div>

        <div class="message-content">

            <div class="message-name">
                Dashil
            </div>

            <div>
                Dashil está pensando...
            </div>

        </div>
    `;


    messages.appendChild(
        pensando
    );


    desplazarseAbajo();


    try {

        const respuesta =
            await fetch(
                "http://127.0.0.1:5000/api/chat",
                {
                    method: "POST",

                    headers: obtenerEncabezadosUsuario(true),

                    body: JSON.stringify({

                        mensaje: texto,

                        chat_id:
                            chatActual

                    })

                }
            );


        const datos =
            await respuesta.json();


        pensando.remove();


        if (!respuesta.ok) {

            throw new Error(
                datos.error ||
                "Error del servidor."
            );

        }


        agregarMensaje(
            "Dashil",
            "D",
            datos.respuesta
        );


        // Actualizar historial

        await cargarConversaciones();


    } catch (error) {

        pensando.remove();


        agregarMensaje(
            "Dashil",
            "D",
            "No pude conectarme con mi servidor."
        );


        console.error(
            "Error:",
            error
        );

    }


    sendButton.disabled =
        false;


    desplazarseAbajo();
}


/* =========================
   CREAR MENSAJE
========================= */

function agregarMensaje(
    nombre,
    avatar,
    texto,
    guardar = true
) {

    const message =
        document.createElement("div");


    message.className =
        "message";


    const contenidoSeguro =
        escaparHTML(texto)
        .replace(/\n/g, "<br>");


    message.innerHTML = `
        <div class="message-avatar">
            ${avatar}
        </div>

        <div class="message-content">

            <div class="message-name">
                ${nombre}
            </div>

            <div>
                ${contenidoSeguro}
            </div>

        </div>
    `;


    messages.appendChild(
        message
    );


    desplazarseAbajo();
}


/* =========================
   PROTEGER HTML
========================= */

function escaparHTML(
    texto
) {

    const div =
        document.createElement(
            "div"
        );


    div.textContent =
        texto;


    return div.innerHTML;
}


/* =========================
   BOTÓN ENVIAR
========================= */

sendButton.addEventListener(
    "click",
    enviarMensaje
);


/* =========================
   ENTER
========================= */

input.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            enviarMensaje();

        }

    }
);


/* =========================
   TEXTAREA
========================= */

input.addEventListener(
    "input",
    ajustarAltura
);


function ajustarAltura() {

    input.style.height =
        "auto";


    input.style.height =
        Math.min(
            input.scrollHeight,
            180
        ) + "px";

}


/* =========================
   SCROLL
========================= */

function desplazarseAbajo() {

    messages.lastElementChild?.scrollIntoView({
        behavior: "smooth"
    });

}


/* =========================
   NUEVA CONVERSACIÓN
========================= */

newChat.addEventListener(
    "click",
    crearNuevaConversacion
);

