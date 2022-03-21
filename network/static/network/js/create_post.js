document.addEventListener('DOMContentLoaded', () => {
    if (!document.querySelector('#profile')) {
        document.querySelector('#newPost').addEventListener('click', () => force_login())
    }

    document.querySelector('#post_submit').addEventListener('click', () => create_post())

    document.querySelector('#post_submit').disabled = true
    
    document.querySelector('#post_content').onkeyup = function() {
        if (document.querySelector('#post_content').value.length > 0) {
            document.querySelector('#post_submit').disabled = false
        } else {
            document.querySelector('#post_submit').disabled = true
        }
    }
})

function force_login() {
    document.querySelector('#login').click()
}

function create_post() {
    const description = document.querySelector('#post_content').value

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

        window.location.reload()
    
        return false;    
    })
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}