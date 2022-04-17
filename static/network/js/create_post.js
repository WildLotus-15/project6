document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#post_submit').addEventListener('click', () => create_post())

    const submit = document.querySelector('#post_submit')

    submit.disabled = true

    const content = document.querySelector('#post_content')

    const postModalButton = document.querySelector('#postModal')
    
    content.onkeydown = newPostHandle
    content.onkeyup = newPostHandle

    content.addEventListener('paste', (event) => {
        let paste = (event.clipboardData || window.clipboardData).getData('text')

        content.value = paste

        // value length must not be equal to 0 and whitespaces are not accepted
        if (paste.length > 0 && paste.indexOf(' ') !== 0) {
            submit.disabled = false
            postModalButton.innerHTML = paste
        }

        event.preventDefault();
    })
})

function create_post() {
    const description = document.querySelector('#post_content').value
    const only_friends = document.querySelector('#only_friends').checked
    const only_me = document.querySelector('#only_me').checked

    fetch('/create_post', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie("csrftoken")
        },
        body: JSON.stringify({
            "description": description,
            "only_friends": only_friends,
            "only_me": only_me
        })
    })
    .then(response => response.json())
    .then(response => {
        console.log(response.message)
    
        window.location.reload()

        return false;
    })
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function newPostHandle(event) {
    const content = document.querySelector('#post_content')
    const submit = document.querySelector('#post_submit')
    const postModal = document.querySelector('#postModal')
    const hiddenUsername = document.querySelector('#loggedInUsername').value

    content.innerHTML = event.target.value

    if (event.target.value.length > 0 && event.target.value.indexOf(' ') !== 0) {
        postModal.innerHTML = event.target.value
        submit.disabled = false
    } else {
        if (window.location.pathname === "/") {
            postModal.innerHTML = `What's on your mind, ${hiddenUsername}?`
        } else {
            postModal.innerHTML = `What's on your mind?`
        }

        submit.disabled = true
    }
}