const API_BASE = "http://127.0.0.1:5000"

const signupForm =
    document.getElementById("signupForm")

const messageDiv =
    document.getElementById("message")

signupForm.addEventListener(
    "submit",
    async function(e){

        e.preventDefault()

        const fullname =
            document.getElementById(
                "fullname"
            ).value

        const username =
            document.getElementById(
                "username"
            ).value

        const email =
            document.getElementById(
                "email"
            ).value

        const password =
            document.getElementById(
                "password"
            ).value

        try{

            const response = await fetch(
                API_BASE + "/signup",
                {
                    method:"POST",

                    headers:{
                        "Content-Type":"application/json"
                    },

                    body:JSON.stringify({
                        fullname,
                        username,
                        email,
                        password
                    })
                }
            )

            const data =
                await response.json()

            if(data.success){

                messageDiv.className =
                    "message success"

                messageDiv.innerText =
                    "Account created successfully 🚀"

                signupForm.reset()

            }else{

                messageDiv.className =
                    "message error"

                messageDiv.innerText =
                    data.message
            }

        }catch(error){

            messageDiv.className =
                "message error"

            messageDiv.innerText =
                "Server error"
        }
    }
)