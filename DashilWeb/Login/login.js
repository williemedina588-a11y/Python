const loginForm =
    document.getElementById("loginForm");

loginForm.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();

        const email =
            document
                .getElementById("email")
                .value
                .trim()
                .toLowerCase();

        const password =
            document
                .getElementById("password")
                .value;

        try {

            const respuesta =
                await fetch(
                    "http://127.0.0.1:5000/api/login",
                    {
                        method: "POST",

                        credentials: "include",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            email: email,

                            password: password

                        })
                    }
                );


            const datos =
                await respuesta.json();


            if (!respuesta.ok) {

                alert(
                    datos.error ||
                    "Correo o contraseña incorrectos."
                );

                return;
            }


            const usuario =
                datos.usuario;


            localStorage.setItem(
                "dashil_sesion",
                "true"
            );

            localStorage.setItem(
                "dashil_usuario_id",
                usuario.id
            );

            localStorage.setItem(
                "dashil_nombre",
                usuario.nombre
            );

            localStorage.setItem(
                "dashil_email",
                usuario.email
            );


            window.location.href =
                "../index.html";


        } catch (error) {

            console.error(
                "Error iniciando sesión:",
                error
            );

            alert(
                "No se pudo conectar con el servidor."
            );

        }

    }
);