document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('form').onsubmit = create_post 
})

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