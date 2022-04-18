document.addEventListener('DOMContentLoaded', () => {
    accept_friend_request_buttons = document.querySelectorAll('.accept_friend_request_button')

    if (accept_friend_request_buttons) {
        accept_friend_request_buttons.forEach(button => {
            let request_id = button.dataset.friend_request_id

            button.addEventListener('click', () => accept_friend_request(request_id))
        })
    }

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
            if (document.querySelector(`#friend_request_card_${request_id}`)) {
                document.querySelector(`#friend_request_card_${request_id}`).remove()

                // If the user will not have any active friend requests page's content will indicate that
                if (response.newAmount === 0) {
                    document.querySelector('#empty_friend_requests_wrapper').className = "d-flex align-items-center justify-content-center flex-column min-vh-100"
                }
            // If the user is on the profile page when accepting a friend request page is being reloaded 
            } else {
                window.location.reload()
            }

            console.log(response.message)
        })
        .catch((error) => {
            console.log("Error:", error);
        })
}