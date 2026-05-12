const existingUser = JSON.parse(
    localStorage.getItem("user")
)

if(existingUser){

    window.location.href =
        "home.html"
}

const API_BASE = "http://127.0.0.1:5000"

const loginForm =
    document.getElementById("loginForm")

const messageDiv =
    document.getElementById("message")

loginForm.addEventListener(
    "submit",
    async function(e){

        e.preventDefault()

        const username_or_email =
            document.getElementById(
                "username_or_email"
            ).value

        const password =
            document.getElementById(
                "password"
            ).value

        try{

            const response = await fetch(
                API_BASE + "/login",
                {
                    method:"POST",

                    headers:{
                        "Content-Type":"application/json"
                    },

                    body:JSON.stringify({
                        username_or_email,
                        password
                    })
                }
            )

            const responseType =
                response.headers.get("content-type") || ""

            const data = responseType.includes("application/json")
                ? await response.json()
                : {
                    success:false,
                    message:`Request failed with status ${response.status}`
                }

            if(response.ok && data.success){

                localStorage.setItem(
                    "user",
                    JSON.stringify(data.user)
                )

                messageDiv.className =
                    "message success"

                messageDiv.innerText =
                    "Login successful 🚀"

                setTimeout(() => {

                    window.location.href =
                        "home.html"

                },1000)

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
                `Server error: ${error.message || "Unable to reach API"}`
        }
    }
)