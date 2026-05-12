const currentUser = JSON.parse(
    localStorage.getItem("user")
)

if(!currentUser){

    window.location.href =
        "login.html"
}

const API_BASE = "http://127.0.0.1:5000"

const viewerId =
    currentUser.userid ||
    currentUser.userId

const profileParams =
    new URLSearchParams(
        window.location.search
    )

const profileUserIdParam =
    profileParams.get("userid")

let profileUser =
    currentUser

let viewingOther =
    false

function applyProfileToPage(){

    document.getElementById(
        "username"
    ).innerText =
        profileUser.username

    document.getElementById(
        "fullname"
    ).innerText =
        profileUser.fullname

    document.getElementById(
        "bio"
    ).innerText =
        profileUser.bio ||
        "No bio yet ✨"

    document.getElementById(
        "profilePic"
    ).src =
        profileUser.profpicurl ||
        "https://images.unsplash.com/photo-1500648767791-00dcc994a43e"
}

async function initProfile(){

    if(profileUserIdParam){

        if(
            String(profileUserIdParam) !==
            String(viewerId)
        ){

            viewingOther =
                true

            try{

                const response =
                    await fetch(
                        API_BASE +
                        "/user/" +
                        encodeURIComponent(
                            profileUserIdParam
                        )
                    )

                const data =
                    await response.json()

                if(!data.success){

                    alert(
                        data.message ||
                        "Could not load profile"
                    )

                    window.location.href =
                        "home.html"

                    return
                }

                profileUser =
                    data.user

            }catch(error){

                console.log(error)

                alert(
                    "Could not load profile"
                )

                window.location.href =
                    "home.html"

                return
            }
        }
    }

    applyProfileToPage()

    if(viewingOther){

        document.getElementById(
            "editProfileBtn"
        ).style.display =
            "none"

        document.getElementById(
            "postsSectionTitle"
        ).innerText =
            "Posts"
    }

    await loadUserPosts()
}

async function loadUserPosts(){

    try{

        const response = await fetch(
            API_BASE + "/posts"
        )

        const data =
            await response.json()

        const postsGrid =
            document.getElementById(
                "postsGrid"
            )

        postsGrid.innerHTML = ""

        const userPosts =
            data.posts.filter(post => {

                return (
                    post.userid ===
                    profileUser.userid
                )
            })

        document.getElementById(
            "postCount"
        ).innerText =
            userPosts.length

        if(userPosts.length === 0){

            postsGrid.innerHTML = `
                <div class="empty-posts">
                    No posts yet 🚀
                </div>
            `

            return
        }

        userPosts.forEach(post => {

            postsGrid.innerHTML += `

                <div class="post-card">

                    <img
                        src="${post.imageurl}"
                        class="post-image"
                    >

                    <div class="post-content">

                        <div class="caption">
                            ${post.caption}
                        </div>

                    </div>

                </div>

            `
        })

    }catch(error){

        console.log(error)
    }
}

function openEditModal(){

    document.getElementById(
        "editModal"
    ).style.display = "flex"

    document.getElementById(
        "editUsername"
    ).value =
        currentUser.username || ""

    document.getElementById(
        "editFullname"
    ).value =
        currentUser.fullname || ""

    document.getElementById(
        "editBio"
    ).value =
        currentUser.bio || ""
}

function closeEditModal(){

    document.getElementById(
        "editModal"
    ).style.display = "none"
}

async function saveProfile(){

    try{

        let profpicurl =
            currentUser.profpicurl

        const profilePicFile =
            document.getElementById(
                "editProfilePic"
            ).files[0]

        if(profilePicFile){

            const formData =
                new FormData()

            formData.append(
                "image",
                profilePicFile
            )

            const uploadResponse =
                await fetch(
                    API_BASE + "/upload-image",
                    {
                        method:"POST",
                        body:formData
                    }
                )

            const uploadData =
                await uploadResponse.json()

            if(uploadData.success){

                profpicurl =
                    uploadData.imageurl
            }
        }

        const response = await fetch(
            API_BASE + "/update-profile",
            {
                method:"PUT",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({

                    userid:
                    viewerId,

                    username:
                    document.getElementById(
                        "editUsername"
                    ).value.trim(),

                    fullname:
                    document.getElementById(
                        "editFullname"
                    ).value,

                    bio:
                    document.getElementById(
                        "editBio"
                    ).value,

                    profpicurl
                })
            }
        )

        const data =
            await response.json()

        if(data.success){

            localStorage.setItem(
                "user",
                JSON.stringify(data.user)
            )

            alert(
                "Profile updated successfully 🚀"
            )

            location.reload()
        }else{

            alert(
                data.message ||
                "Failed to update profile"
            )
        }

    }catch(error){

        console.log(error)

        alert(
            "Failed to update profile"
        )
    }
}

function logout(){

    localStorage.removeItem(
        "user"
    )

    window.location.href =
        "login.html"
}

function goHome(){

    window.location.href =
        "home.html"
}

initProfile()