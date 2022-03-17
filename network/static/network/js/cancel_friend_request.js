document.addEventListener('DOMContentLoaded', () => {
    cancel_friend_request_button = document.querySelector('#cancel_friend_request_button')

    if (cancel_friend_request_button) {
        let profile_id = cancel_friend_request_button.dataset.profile_id

        cancel_friend_request_button.addEventListener('click', () => cancel_friend_request(profile_id))    
    }
})

function cancel_friend_request(profile_id) {
    fetch(`/cancel_friend_request/${profile_id}`)
    .then(response => response.json())
    .then(response => {
        console.log(response.message)

        window.location.reload()
    })
}