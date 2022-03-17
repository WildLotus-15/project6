document.addEventListener('DOMContentLoaded', () => {
    send_friend_request_button = document.querySelector('#send_friend_request_button')

    if (send_friend_request_button) {
        let profile_id = send_friend_request_button.dataset.profile_id

        send_friend_request_button.addEventListener('click', () => send_friend_request(profile_id))    
    }
})

function send_friend_request(profile_id) {
    fetch(`/send_friend_request/${profile_id}`)
    .then(response => response.json())
    .then(response => {
        console.log(response.message)

        window.location.reload()
    })
}
