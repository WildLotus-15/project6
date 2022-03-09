document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('form').onsubmit = create_post

    load_posts("")
})

function load_posts(addon) {
    if (addon.includes("?")) {
        addon += ""
    } else {
        document.getElementById('profile').style.display = 'none'
    }
    fetch(`/load_posts${addon}`)
    .then(response => response.json())
    .then(response => {
        response.posts.forEach(post => build_post(post))

        console.log(response)
    })
}

function build_post(post) {
    const post_card = document.createElement('div')
    post_card.className = 'card'

    const post_body = document.createElement('div')
    post_body.className = 'card-body'
    post_body.id = `post_body_${post.id}`
    post_card.append(post_body)

    const header = document.createElement('h5')
    header.className = 'card-title'
    header.id = `post_header_${post.id}`
    header.innerHTML = post.author_username
    post_body.append(header)

    header.addEventListener('click', () => show_profile(post.author_id))

    const description = document.createElement('p')
    description.className = 'card-text'
    description.id = `post_description_${post.id}`
    description.innerHTML = post.description
    post_body.append(description)

    const timestamp = document.createElement('h6')
    timestamp.className = 'text-muted'
    timestamp.id = `post_timestamp_${post.id}`
    timestamp.innerHTML = post.timestamp
    post_body.append(timestamp)

    document.getElementById('posts').append(post_card)
}

function show_profile(author_id) {
    load_posts(`?profile=${author_id}`)
    document.getElementById('profile').style.display = 'unset'
    document.getElementById('newPost').style.display = 'none'
    fetch(`/profile/${author_id}`)
    .then(response => response.json())
    .then(profile => {
        document.getElementById('profile_username').innerHTML = profile.profile_username

        console.log(profile)
    })
}

function create_post() {
    const description = document.getElementById('description').value

    fetch('/create_post', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie("csrftoken")
        }, 
        body: JSON.stringify({
            "description": description
        })
    })
    .then(response => response.json())
    .then(response => {
        console.log(response.message)
    })
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}