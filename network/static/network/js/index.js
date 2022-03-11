document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('form').onsubmit = create_post

    if (document.getElementById("logged_profile")) {
        const user_id = document.getElementById('userID').value

        document.getElementById("requests").addEventListener('click', () => load_requests())
        document.getElementById("logged_profile").addEventListener('click', () => show_profile(user_id))
        document.getElementById('friends').addEventListener('click', () => load_friends(user_id))
    } else {
        document.getElementById('newPost').addEventListener('click', () => force_login())
    }

    load_posts("")
})

function load_friends(user_id) {
    document.getElementById('request_cards').innerHTML = ''
    document.getElementById('request_cards').style.display = 'block'
    document.getElementById('newPost').style.display = 'none'
    document.getElementById('posts').innerHTML = ''
    document.getElementById('profile').style.display = 'none'
    fetch(`/friends/${user_id}`)
    .then(response => response.json())
    .then(response => {
        response.friends.forEach(request => build_friend(request))

        console.log(response)
    })
}

function build_friend(request) {
    const request_card = document.createElement('div')
    request_card.className = 'card'

    const header = document.createElement('div')
    header.className = 'card-header'
    header.style.display = 'flex'
    header.id = `friend_request_header_${request.id}`
    request_card.append(header)

    const from_user = document.createElement('div')
    from_user.style.flex = '1'
    from_user.innerHTML = request.from_user
    header.append(from_user)

    from_user.addEventListener('click', () => show_profile(request.from_user_id))

    const buttons_row = document.createElement('div')
    buttons_row.style.flex = '1'
    buttons_row.className = 'text-right'
    header.append(buttons_row)

    const remove_button = document.createElement('button')
    remove_button.type = 'button'
    remove_button.className = 'btn btn-danger'
    remove_button.innerHTML = 'Remove'
    buttons_row.append(remove_button)

    remove_button.addEventListener('click', () => remove_friend(request))

    document.getElementById('request_cards').append(request_card)
}

function remove_friend(request) {
    fetch(`remove_from_friends/${request.id}`)
    .then(response => response.json())
    .then(response => {
        document.getElementById(`friend_request_header_${request.id}`).remove()

        console.log(response.message)
    })
}

function force_login() {
    document.getElementById('login').click()
}

function load_requests() {
    document.getElementById('request_cards').innerHTML = ''
    document.getElementById('request_cards').style.display = 'block'
    document.getElementById('newPost').style.display = 'none'
    document.getElementById('posts').innerHTML = ''
    document.getElementById('profile').style.display = 'none'
    fetch('/requests')
    .then(response => response.json())
    .then(response => {
        document.getElementById('request_cards').innerHTML = ''
        response.requests.forEach(request => build_request(request))

        console.log(response)
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

    const from_user = document.createElement('div')
    from_user.style.flex = '1'
    from_user.innerHTML = `Pending friend request from ${request.from_user}`
    header.append(from_user)

    from_user.addEventListener('click', () => show_profile(request.from_user_id))

    const buttons_row = document.createElement('div')
    buttons_row.style.flex = '1'
    buttons_row.className = 'text-right'
    header.append(buttons_row)

    const accept_button = document.createElement('button')
    accept_button.type = 'button'
    accept_button.className = 'btn btn-primary'
    accept_button.innerHTML = 'Accept'
    buttons_row.append(accept_button)

    accept_button.addEventListener('click', () => accept_friend_request(request))

    const decline_button = document.createElement('button')
    decline_button.type = 'button'
    decline_button.className = 'btn btn-danger'
    decline_button.innerHTML = 'Decline'
    buttons_row.append(decline_button)

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
    document.getElementById('request_cards').style.display = 'none'
    friend_request_button = document.getElementById('friend_request_button') 
    friend_request_button.style.display = 'none'
    fetch(`/profile/${author_id}`)
    .then(response => response.json())
    .then(profile => {
        document.getElementById('profile_username').innerHTML = profile.profile_username
        document.getElementById('friends_amount').innerHTML = profile.friends_amount

        if (profile.friend_request_available || profile.self_in_friend_request || profile.currently_friended) {
            friend_request_button.style.display = 'unset'
            if (profile.currently_friended) {
                friend_request_button.innerHTML = 'Friend'
                friend_request_button.addEventListener('click', () => remove_profile_friend(author_id))
            } else if (profile.self_in_friend_request) {
                friend_request_button.innerHTML = 'Friend request has been sent'
                friend_request_button.addEventListener('click', () => unsend_friend_request(author_id))
            } else {
                friend_request_button.innerHTML = 'Send friend request'
                friend_request_button.addEventListener('click', () => send_friend_request(author_id))
            }       
        }
        window.scrollTo(0, 0)

        console.log(profile)
    })
}

function unsend_friend_request(author_id) {
    fetch(`/unsend_friend_request/${author_id}`)
    .then(response => response.json())
    .then(response => {
        console.log(response.message)

        window.location.reload()
    })
}

function remove_profile_friend(author_id) {
    fetch(`/remove_profile_friend/${author_id}`)
    .then(response => response.json())
    .then(response => {
        console.log(response.message)

        window.location.reload()
    })
}

function send_friend_request(author_id) {
    fetch(`/send_friend_request/${author_id}`)
    .then(response => response.json())
    .then(response => {
        console.log(response.message)

        window.location.reload()
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