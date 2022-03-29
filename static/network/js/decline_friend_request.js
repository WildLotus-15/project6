document.addEventListener('DOMContentLoaded', () => {
    decline_friend_request_button = document.querySelector('#decline_friend_request_button')

    if (decline_friend_request_button) {
        let request_id = decline_friend_request_button.dataset.friend_request_id

        decline_friend_request_button.addEventListener('click', () => decline_friend_request(request_id))    
    }
})

function decline_friend_request(request_id) {
    fetch(`/decline_friend_request/${request_id}`)
    .then(response => response.json())
    .then(response => {
        console.log(response.message)

        window.location.reload()
    })
}