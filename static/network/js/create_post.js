document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#post_submit').addEventListener('click', () => create_post())

    const submit = document.querySelector('#post_submit')

    submit.disabled = true

    const content = document.querySelector('#post_content')

    const postModalButton = document.querySelector('#postModal')

    const hiddenUsername = document.querySelector('#loggedInUsername').value
    
    content.onkeyup = function() {
        if (content.value.length > 0) {
            submit.disabled = false
            postModalButton.innerHTML = content.value
        } else {
            submit.disabled = true
            postModalButton.innerHTML = `What's on your mind, ${hiddenUsername}?`
        }
    }

    content.addEventListener('paste', (event) => {
        let paste = (event.clipboardData || window.clipboardData).getData('text')

        content.value = paste

        if (paste.length > 0) {
            submit.disabled = false
        } else {
            submit.disabled = true
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