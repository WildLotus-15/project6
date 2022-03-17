document.addEventListener('DOMContentLoaded', () => {
    accept_friend_request_button = document.querySelector('#accept_friend_request_button')

    if (accept_friend_request_button) {
        let request_id = accept_friend_request_button.dataset.friend_request_id

        accept_friend_request_button.addEventListener('click', () => accept_friend_request(request_id))    
    }
})

function accept_friend_request(request_id) {
    fetch(`/accept_friend_request/${request_id}`)
    .then(response => response.json())
    .then(response => {
        console.log(response.message)

        window.location.reload()
    })
}