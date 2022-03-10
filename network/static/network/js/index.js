document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('form').onsubmit = create_post

    if (document.getElementById("requests")) {
        document.getElementById("requests").addEventListener('click', () => load_requests())
    } else {
        document.getElementById('newPost').addEventListener('click', () => force_login())
    }

    load_posts("")
})

function force_login() {
    document.getElementById('login').click()
}

function load_requests() {
    document.getElementById('request_cards').style.display = 'block'
    document.getElementById('newPost').style.display = 'none'
    document.getElementById('posts').style.display = 'none'
    document.getElementById('profile').style.display = 'none'
    fetch('/requests')
    .then(response => response.json())
    .then(response => {
        data = JSON.parse(response)
        data.forEach(request => build_request(request))

        console.log(data)
    })
}

function build_request(request) {
    const request_card = document.createElement('div')
    request_card.className = 'card'

    const header = document.createElement('div')
    header.className = 'card-header'
    header.style.display = 'flex'
    header.id = `friend_request_header_${request.id}`
    request_card.append(header)

    const id = document.createElement('div')
    id.innerHTML = request.id
    id.style.flex = '1'
    header.append(id)

    const from_user = document.createElement('div')
    from_user.innerHTML = request.from_user
    id.style.flex = '1'
    header.append(from_user)

    const accept_button = document.createElement('button')
    accept_button.type = 'button'
    accept_button.className = 'btn btn-primary'
    accept_button.innerHTML = 'Accept Friend Request'
    header.append(accept_button)

    accept_button.addEventListener('click', () => accept_friend_request(request))

    const decline_button = document.createElement('button')
    decline_button.type = 'button'
    decline_button.className = 'btn btn-danger'
    decline_button.innerHTML = 'Decline Friend Request'
    header.append(decline_button)

    decline_button.addEventListener('click', () => decline_friend_request(request))

    document.getElementById('request_cards').append(request_card)
}

function accept_friend_request(request) {
    fetch(`/accept_friend_request/${request.id}`)
    .then(response => response.json())
    .then(response => {
        console.log(response.message)

        document.getElementById(`friend_request_header_${request.id}`).remove()
    })
}


function decline_friend_request(request) {
    fetch(`/decline_friend_request/${request.id}`)
    .then(response => response.json())
    .then(response => {
        console.log(response.message)

        document.getElementById(`friend_request_header_${request.id}`).remove()
    })
}


function load_posts(addon) {
    if (addon.includes("?")) {
        addon += ""
    } else {
        document.getElementById('profile').style.display = 'none'
        document.getElementById('request_cards').style.display = 'block'
    }
    fetch(`/load_posts${addon}`)
    .then(response => response.json())
    .then(response => {
        document.getElementById('posts').innerHTML = ''
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
    friend_request_button = document.getElementById('friend_request_button') 
    friend_request_button.style.display = 'none'
    fetch(`/profile/${author_id}`)
    .then(response => response.json())
    .then(profile => {
        document.getElementById('profile_username').innerHTML = profile.profile_username

        if (profile.friend_request_available) {
            friend_request_button.style.display = 'unset'
            if (profile.currently_friended) {
                friend_request_button.innerHTML = 'Unfriend'
            } else {
                friend_request_button.innerHTML = 'Friend'
            }
        }

        console.log(profile)
    })
}

function send_friend_request(author_id) {
    fetch(`/send_friend_request/${author_id}`)
    .then(response => response.json())
    .then(response => {
        console.log(response)
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