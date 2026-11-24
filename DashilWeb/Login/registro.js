const registerForm =
    document.getElementById("registerForm");

registerForm.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();

        const name =
            document.getElementById(
                "name"
            ).value.trim();

        const email =
            document.getElementById(
                "email"
            ).value.trim().toLowerCase();

        const password =
            document.getElementById(
                "password"
            ).value;

        const confirmPassword =
            document.getElementById(
                "confirmPassword"
            ).value;


        if (password !== confirmPassword) {

            alert(
                "Las contraseñas no coinciden."
            );

            return;
        }


        if (password.length < 6) {

            alert(
                "La contraseña debe tener al menos 6 caracteres."
            );

            return;
        }


        try {

            const respuesta =
                await fetch(
                    "http://127.0.0.1:5000/api/registro",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            nombre: name,

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
                    "No se pudo crear la cuenta."
                );

                return;
            }


            alert(
                "Cuenta creada correctamente."
            );


            window.location.href =
                "login.html";


        } catch (error) {

            console.error(
                "Error registrando usuario:",
                error
            );


            alert(
                "No se pudo conectar con el servidor."
            );

        }

    }
);