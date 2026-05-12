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

document.getElementById(
    "welcomeText"
).innerText =
    `Welcome, ${currentUser.fullname}`

const imageFileInput =
    document.getElementById(
        "imageFile"
    )

const previewImage =
    document.getElementById(
        "previewImage"
    )

imageFileInput.addEventListener(
    "change",
    function(){

        const file =
            imageFileInput.files[0]

        if(file){

            previewImage.src =
                URL.createObjectURL(file)

            previewImage.style.display =
                "block"
        }
    }
)

function escapeHtml(text){

    if(text === null || text === undefined){

        return ""
    }

    const s = String(text)

    return s
        .replace(/&/g,"&amp;")
        .replace(/</g,"&lt;")
        .replace(/>/g,"&gt;")
        .replace(/"/g,"&quot;")
}

function formatTimeAgo(
    dateInput
){

    if(
        dateInput === null ||
        dateInput === undefined
    ){

        return ""
    }

    const d = new Date(
        dateInput
    )

    const t = d.getTime()

    if(Number.isNaN(t)){

        return ""
    }

    let seconds = Math.floor(
        (Date.now() - t) / 1000
    )

    if(seconds < 0){

        seconds = 0
    }

    if(seconds < 10){

        return "just now"
    }

    if(seconds < 60){

        return "moments ago"
    }

    const minutes = Math.floor(
        seconds / 60
    )

    if(minutes < 60){

        return minutes === 1
            ? "1 minute ago"
            : `${minutes} minutes ago`
    }

    const hours = Math.floor(
        minutes / 60
    )

    if(hours < 24){

        return hours === 1
            ? "1 hour ago"
            : `${hours} hours ago`
    }

    const days = Math.floor(
        hours / 24
    )

    if(days < 7){

        return days === 1
            ? "1 day ago"
            : `${days} days ago`
    }

    const weeks = Math.floor(
        days / 7
    )

    if(weeks < 5){

        return weeks === 1
            ? "1 week ago"
            : `${weeks} weeks ago`
    }

    const months = Math.floor(
        days / 30
    )

    if(months < 12){

        return months === 1
            ? "1 month ago"
            : `${months} months ago`
    }

    const years = Math.floor(
        days / 365
    )

    return years === 1
        ? "1 year ago"
        : `${years} years ago`
}

function renderCommentNode(c){

    const name =
        c.author_fullname ||
        c.author_username ||
        "User"

    const timeLabel =
        formatTimeAgo(
            c.createdat
        )

    const kids = (
        c.replies || []
    )
        .map(
            renderCommentNode
        )
        .join("")

    return `

        <div
            class="comment-node"
            data-comid="${c.comid}"
        >

            <div class="comment-head">

                <strong>
                    ${escapeHtml(name)}
                </strong>

                <span class="comment-time">
                    ${escapeHtml(timeLabel)}
                </span>

            </div>

            <div class="comment-body">
                ${escapeHtml(c.commtxt)}
            </div>

            <button
                type="button"
                class="comment-reply-btn"
            >
                Reply
            </button>

            <div
                class="comment-reply-form"
                style="display:none"
            >

                <textarea
                    class="reply-input"
                    placeholder="Write a reply..."
                ></textarea>

                <div class="reply-actions">

                    <button
                        type="button"
                        class="reply-submit-btn small-reply-btn"
                    >
                        Post reply
                    </button>

                    <button
                        type="button"
                        class="reply-cancel-btn small-reply-btn"
                    >
                        Cancel
                    </button>

                </div>

            </div>

            <div class="comment-replies">
                ${kids}
            </div>

        </div>

    `
}

function bindCommentListClicks(
    list,
    postid,
    card
){

    list.dataset.postid =
        postid

    list.onclick = function(
        event
    ){

        const t =
            event.target

        if(
            !t ||
            !t.classList
        ){

            return
        }

        if(
            t.classList.contains(
                "comment-reply-btn"
            )
        ){

            const node =
                t.closest(
                    ".comment-node"
                )

            const form =
                node.querySelector(
                    ".comment-reply-form"
                )

            const open =
                form.style.display !==
                "block"

            form.style.display =
                open
                    ? "block"
                    : "none"

            if(open){

                form.querySelector(
                    ".reply-input"
                ).focus()
            }

            return
        }

        if(
            t.classList.contains(
                "reply-cancel-btn"
            )
        ){

            const form =
                t.closest(
                    ".comment-reply-form"
                )

            form.style.display =
                "none"

            form.querySelector(
                ".reply-input"
            ).value = ""

            return
        }

        if(
            t.classList.contains(
                "reply-submit-btn"
            )
        ){

            const form =
                t.closest(
                    ".comment-reply-form"
                )

            const node =
                t.closest(
                    ".comment-node"
                )

            const parentComid =
                node.dataset.comid

            const ta =
                form.querySelector(
                    ".reply-input"
                )

            submitReply(
                postid,
                parentComid,
                card,
                ta,
                form
            )
        }
    }
}

async function loadPosts(){

    const feed =
        document.getElementById("feed")

    feed.innerHTML = `
        <div class="empty-feed">
            Loading posts…
        </div>
    `

    async function parseJsonSafe(
        r
    ){

        try{

            return await r.json()
        }catch(
            e
        ){

            return null
        }
    }

    try{

        let primaryUrl =
            API_BASE +
            "/posts"

        if(viewerId){

            primaryUrl +=
                "?viewer_userid=" +
                encodeURIComponent(
                    viewerId
                )
        }

        let response =
            await fetch(
                primaryUrl
            )

        let data =
            await parseJsonSafe(
                response
            )

        if(
            !response.ok ||
            (
                data &&
                data.success === false
            )
        ){

            response =
                await fetch(
                    API_BASE +
                    "/posts"
                )

            data =
                await parseJsonSafe(
                    response
                )
        }

        feed.innerHTML = ""

        if(!response.ok){

            feed.innerHTML = `
                <div class="empty-feed">
                    Could not reach the API (HTTP ${response.status}).<br><br>
                    Start the Flask server from the project folder:<br>
                    <code style="background:#eee;padding:4px 8px;border-radius:8px;display:inline-block;margin-top:8px;">python backend/app.py</code>
                </div>
            `

            return
        }

        if(
            !data ||
            data.success === false
        ){

            const msg =
                (
                    data &&
                    data.message
                ) ||
                "Could not load posts."

            feed.innerHTML = `
                <div class="empty-feed">
                    ${escapeHtml(msg)}
                </div>
            `

            return
        }

        if(
            !data.posts ||
            data.posts.length === 0
        ){

            feed.innerHTML = `
                <div class="empty-feed">
                    No posts yet 🚀
                </div>
            `

            return
        }

        data.posts.forEach(post => {

            const likeCount =
                post.like_count !== undefined
                    ? post.like_count
                    : 0

            const commentCount =
                post.comment_count !== undefined
                    ? post.comment_count
                    : 0

            const liked =
                Boolean(post.liked)

            feed.innerHTML += `

                <div
                    class="post-card"
                    data-postid="${post.postid}"
                >

                    <div class="post-header">

                        <div class="avatar"></div>

                        <div class="user-info">

                            <h3>
                                ${escapeHtml(post.fullname)}
                            </h3>

                            <p>
                                @${escapeHtml(post.username || "cooluser")}
                            </p>

                        </div>

                    </div>

                    <img
                        src="${post.imageurl}"
                        class="post-image"
                        alt=""
                    >

                    <div class="post-content">

                        <div class="caption">
                            ${escapeHtml(post.caption)}
                        </div>

                        <div class="engagement-row">

                            <span class="like-count-label">
                                ❤️ ${likeCount} likes
                            </span>

                            <span class="comment-count-label">
                                💬 ${commentCount} comments
                            </span>

                        </div>

                        <div class="post-actions">

                            <button
                                type="button"
                                class="action-btn like-btn${liked ? " liked" : ""}"
                                data-liked="${liked ? "1" : "0"}"
                            >
                                ${liked ? "❤️ Liked" : "🤍 Like"}
                            </button>

                            <button
                                type="button"
                                class="action-btn comment-toggle-btn"
                            >
                                💬 Comment
                            </button>

                        </div>

                        <div class="comments-panel">

                            <div
                                class="comments-list"
                            ></div>

                            <textarea
                                class="comment-input"
                                placeholder="Write a comment..."
                            ></textarea>

                            <button
                                type="button"
                                class="post-comment-btn"
                            >
                                Post comment
                            </button>

                        </div>

                    </div>

                </div>

            `
        })

        feed.querySelectorAll(
            ".post-card"
        ).forEach(bindPostCardEvents)

    }catch(error){

        console.log(error)

        feed.innerHTML = `
            <div class="empty-feed">
                Network error loading posts. Is <code style="background:#eee;padding:2px 6px;border-radius:6px;">python backend/app.py</code> running on port 5000?<br><br>
                <small>${escapeHtml(error.message || "")}</small>
            </div>
        `
    }
}

function bindPostCardEvents(card){

    const postid =
        card.dataset.postid

    const likeBtn =
        card.querySelector(".like-btn")

    const toggleBtn =
        card.querySelector(
            ".comment-toggle-btn"
        )

    const panel =
        card.querySelector(
            ".comments-panel"
        )

    const postCommentBtn =
        card.querySelector(
            ".post-comment-btn"
        )

    likeBtn.addEventListener(
        "click",
        function(){

            toggleLike(
                postid,
                card
            )
        }
    )

    toggleBtn.addEventListener(
        "click",
        function(){

            const open =
                panel.classList.toggle(
                    "open"
                )

            if(open){

                loadCommentsForPost(
                    postid,
                    card
                )
            }
        }
    )

    postCommentBtn.addEventListener(
        "click",
        function(){

            submitComment(
                postid,
                card
            )
        }
    )
}

async function toggleLike(
    postid,
    card
){

    const likeBtn =
        card.querySelector(".like-btn")

    const countLabel =
        card.querySelector(
            ".like-count-label"
        )

    let liked =
        likeBtn.dataset.liked === "1"

    likeBtn.disabled = true

    try{

        const url = liked
            ? API_BASE + "/unlike-post"
            : API_BASE + "/like-post"

        const options = liked
            ? {
                method:"DELETE",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({
                    postid,
                    userid:viewerId
                })
            }
            : {
                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({
                    postid,
                    userid:viewerId
                })
            }

        const response =
            await fetch(
                url,
                options
            )

        const data =
            await response.json()

        if(!data.success){

            alert(
                data.message ||
                "Could not update like"
            )

            return
        }

        liked = !liked

        likeBtn.dataset.liked =
            liked ? "1" : "0"

        likeBtn.classList.toggle(
            "liked",
            liked
        )

        likeBtn.innerText =
            liked
                ? "❤️ Liked"
                : "🤍 Like"

        let n = parseInt(
            countLabel.innerText.replace(
                /\D/g,
                ""
            ),
            10
        )

        if(Number.isNaN(n)){

            n = 0
        }

        n += liked ? 1 : -1

        if(n < 0){

            n = 0
        }

        countLabel.innerText =
            `❤️ ${n} likes`

    }catch(error){

        console.log(error)

        alert(
            "Could not update like"
        )
    }finally{

        likeBtn.disabled = false
    }
}

async function loadCommentsForPost(
    postid,
    card
){

    const list =
        card.querySelector(
            ".comments-list"
        )

    list.innerHTML = `
        <div class="comment-item">
            Loading comments…
        </div>
    `

    try{

        const response = await fetch(
            API_BASE +
            "/get-comments/" +
            encodeURIComponent(postid)
        )

        const data =
            await response.json()

        if(!data.success){

            list.innerHTML = `
                <div class="comment-item">
                    ${escapeHtml(
                        data.message ||
                        "Could not load comments"
                    )}
                </div>
            `

            return
        }

        list.innerHTML = ""

        if(
            !data.comments ||
            data.comments.length === 0
        ){

            list.innerHTML = `
                <div class="comment-item">
                    No comments yet.
                </div>
            `

            bindCommentListClicks(
                list,
                postid,
                card
            )

            return
        }

        list.innerHTML =
            data.comments
                .map(
                    renderCommentNode
                )
                .join("")

        bindCommentListClicks(
            list,
            postid,
            card
        )

    }catch(error){

        console.log(error)

        list.innerHTML = `
            <div class="comment-item">
                Could not load comments.
            </div>
        `

        bindCommentListClicks(
            list,
            postid,
            card
        )
    }
}

async function submitReply(
    postid,
    parentComid,
    card,
    textarea,
    form
){

    const commtxt =
        textarea.value.trim()

    if(!commtxt){

        return
    }

    const buttons =
        form.querySelectorAll(
            "button"
        )

    buttons.forEach(
        b => {
            b.disabled = true
        }
    )

    try{

        const response = await fetch(
            API_BASE + "/add-comment",
            {
                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({
                    postid,
                    userid:viewerId,
                    commtxt,
                    parent_comid:parentComid
                })
            }
        )

        const data =
            await response.json()

        if(!data.success){

            alert(
                data.message ||
                "Could not post reply"
            )

            return
        }

        textarea.value = ""

        form.style.display =
            "none"

        const countLabel =
            card.querySelector(
                ".comment-count-label"
            )

        let n = parseInt(
            countLabel.innerText.replace(
                /\D/g,
                ""
            ),
            10
        )

        if(Number.isNaN(n)){

            n = 0
        }

        countLabel.innerText =
            `💬 ${n + 1} comments`

        await loadCommentsForPost(
            postid,
            card
        )

    }catch(error){

        console.log(error)

        alert(
            "Could not post reply"
        )
    }finally{

        buttons.forEach(
            b => {
                b.disabled = false
            }
        )
    }
}

async function submitComment(
    postid,
    card
){

    const textarea =
        card.querySelector(
            ".comment-input"
        )

    const btn =
        card.querySelector(
            ".post-comment-btn"
        )

    const commtxt =
        textarea.value.trim()

    if(!commtxt){

        return
    }

    btn.disabled = true

    try{

        const response = await fetch(
            API_BASE + "/add-comment",
            {
                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({
                    postid,
                    userid:viewerId,
                    commtxt
                })
            }
        )

        const data =
            await response.json()

        if(!data.success){

            alert(
                data.message ||
                "Could not post comment"
            )

            return
        }

        textarea.value = ""

        const countLabel =
            card.querySelector(
                ".comment-count-label"
            )

        let n = parseInt(
            countLabel.innerText.replace(
                /\D/g,
                ""
            ),
            10
        )

        if(Number.isNaN(n)){

            n = 0
        }

        countLabel.innerText =
            `💬 ${n + 1} comments`

        await loadCommentsForPost(
            postid,
            card
        )

    }catch(error){

        console.log(error)

        alert(
            "Could not post comment"
        )
    }finally{

        btn.disabled = false
    }
}

async function createPost(){

    const imageFile =
        imageFileInput.files[0]

    const caption =
        document.getElementById(
            "caption"
        ).value

    const message =
        document.getElementById(
            "message"
        )

    if(!imageFile){

        message.innerText =
            "Please select an image"

        return
    }

    try{

        message.innerText =
            "Uploading image..."

        const formData = new FormData()

        formData.append(
            "image",
            imageFile
        )

        const uploadResponse = await fetch(
            API_BASE + "/upload-image",
            {
                method:"POST",
                body:formData
            }
        )

        const uploadData =
            await uploadResponse.json()

        if(!uploadData.success){

            message.innerText =
                uploadData.message

            return
        }

        const imageurl =
            uploadData.imageurl

        message.innerText =
            "Creating post..."

        const postResponse = await fetch(
            API_BASE + "/create-post",
            {
                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({

                    userid:
                    viewerId,

                    fullname:
                    currentUser.fullname,

                    imageurl,
                    caption
                })
            }
        )

        const postData =
            await postResponse.json()

        if(postData.success){

            message.innerText =
                "Post created successfully 🚀"

            document.getElementById(
                "caption"
            ).value = ""

            imageFileInput.value = ""

            previewImage.style.display =
                "none"

            loadPosts()

        }else{

            message.innerText =
                postData.message
        }

    }catch(error){

        message.innerText =
            "Server error"
    }
}

function logout(){

    localStorage.removeItem(
        "user"
    )

    window.location.href =
        "login.html"
}

function goToProfile(){

    window.location.href =
        "profile.html"
}

const defaultAvatar =
    "https://images.unsplash.com/photo-1500648767791-00dcc994a43e"

async function searchData(){

    const value =
        document.getElementById(
            "searchBox"
        ).value.trim()

    const card =
        document.getElementById(
            "searchResultsCard"
        )

    const body =
        document.getElementById(
            "searchResultsBody"
        )

    if(!value){

        card.classList.remove("visible")
        body.innerHTML = ""
        return
    }

    body.innerHTML = `
        <div class="search-results-empty">
            Searching…
        </div>
    `

    card.classList.add("visible")

    try{

        const response = await fetch(
            API_BASE +
            "/search-users?q=" +
            encodeURIComponent(value)
        )

        const data =
            await response.json()

        if(!data.success){

            body.innerHTML = `
                <div class="search-results-error">
                    ${data.message || "Search failed"}
                </div>
            `

            return
        }

        if(
            !data.users ||
            data.users.length === 0
        ){

            body.innerHTML = `
                <div class="search-results-empty">
                    No profiles match “${value}”.
                </div>
            `

            return
        }

        body.innerHTML = ""

        data.users.forEach(user => {

            const pic =
                user.profpicurl ||
                defaultAvatar

            const safeName =
                user.fullname ||
                user.username

            const row =
                document.createElement(
                    "div"
                )

            row.className =
                "search-result-row"

            row.innerHTML = `

                <img
                    src="${pic}"
                    alt=""
                    class="search-result-avatar"
                >

                <div class="search-result-meta">

                    <h4>
                        ${safeName}
                    </h4>

                    <p>
                        @${user.username || "user"}
                    </p>

                </div>

            `

            row.addEventListener(
                "click",
                function(){

                    window.location.href =
                        "profile.html?userid=" +
                        encodeURIComponent(
                            user.userid
                        )
                }
            )

            body.appendChild(row)
        })

    }catch(error){

        console.log(error)

        body.innerHTML = `
            <div class="search-results-error">
                Could not reach server.
            </div>
        `
    }
}

document.getElementById(
    "searchBox"
).addEventListener(
    "keydown",
    function(event){

        if(event.key === "Enter"){

            event.preventDefault()
            searchData()
        }
    }
)

loadPosts()