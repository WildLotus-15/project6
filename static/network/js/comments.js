document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.comments').forEach(comment => {
        comment.onclick = (event) => {
            const post_id = event.target.dataset.post_id

            show_comments(post_id)
        }
    })
})

function show_comments(post_id) {
    const comments_placeholder = document.querySelector(`#comments_placeholder_${post_id}`)

    if (comments_placeholder.className === "d-none") {
        comments_placeholder.className = "d-block mt-2"
    } else {
        comments_placeholder.className = "d-none"
    }

    fetch(`/post/${post_id}/comments`)
    .then(response => response.json())
    .then(response => {
        console.log(response.comments)

        document.querySelector(`#comments_${post_id}`).innerHTML = ""

        const comment_input = document.querySelector(`#comment_input_${post_id}`)

        comment_input.onkeyup = (e) => {
            if (e.keyCode === 13 && comment_input.value.length > 0) {
                send_comment(comment_input.value, post_id)

                comment_input.value = ''
            }
        }

        response.comments.forEach(comment => {
            build_comment(comment, post_id)
        })
    })
}

function send_comment(comment, post_id) {
    fetch(`/post/${post_id}/comment`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            "comment": comment
        })
    })
    .then(response => response.json())
    .then(response => {
        console.log(response.message)

        document.querySelector(`#comments_amount_${post_id}`).innerHTML = `Comments ${response.newAmount}`
    })
}

function build_comment(comment, post_id) {
    const comments = document.querySelector(`#comments_${post_id}`)

    const commentWrapper = document.createElement('div')
    commentWrapper.className = "d-flex"
    commentWrapper.id = `comment_placeholder_${comment.id}`
    
    const author_picture = document.createElement('img')
    author_picture.src = comment.author_picture
    author_picture.className = "rounded-circle"
    author_picture.width = "32"
    author_picture.height = "32"
    
    const linkPlaceholder = document.createElement('div')
    linkPlaceholder.append(author_picture)
    
    const picture_link = document.createElement('a')
    picture_link.href = `/profile/${comment.author_id}`
    picture_link.append(linkPlaceholder)

    const picturePlaceholder = document.createElement('div')
    picturePlaceholder.className = "mr-1"
    picturePlaceholder.append(picture_link)

    commentWrapper.append(picturePlaceholder)

    const content = document.createElement('div')
    content.className = "d-flex flex-column"
    commentWrapper.append(content)

    const author_link = document.createElement('a')
    author_link.href = `/profile/${comment.author_id}`
    author_link.innerHTML = comment.author_username

    const author_username = document.createElement('div')
    author_username.append(author_link)

    content.append(author_username)

    const description = document.createElement('div')
    description.innerHTML = comment.description
    content.append(description)

    const timestamp = document.createElement('div')
    timestamp.className = 'text-muted ml-1'
    timestamp.innerHTML = `<small>${comment.timestamp}</small>`
    commentWrapper.append(timestamp)

    comments.append(commentWrapper)
}