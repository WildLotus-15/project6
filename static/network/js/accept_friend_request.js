document.addEventListener('DOMContentLoaded', () => {
    accept_friend_request_links = document.querySelectorAll('.accept_friend_request_link')

    if (accept_friend_request_links) {
        accept_friend_request_links.forEach(link => {
            let request_id = link.dataset.friend_request_id

            link.addEventListener('click', (event) => accept_friend_request(event, request_id))
        })
    }

    accept_friend_request_button = document.querySelector('#accept_friend_request_button')

    if (accept_friend_request_button) {
        let request_id = accept_friend_request_button.dataset.friend_request_id

        accept_friend_request_button.addEventListener('click', (event) => accept_friend_request(event, request_id))    
    }
})

function accept_friend_request(event, request_id) {
    // Preventing the "Confirm" dropdown link from redirecting to an another page
    event.preventDefault();

    fetch(`/accept_friend_request/${request_id}`)
        .then(response => response.json())
        .then(response => {
            if (document.querySelector(`#friend_request_card_${request_id}`)) {
                document.querySelector(`#friend_request_card_${request_id}`).remove()

                // If the user will not have any active friend requests page's content will indicate that
                if (response.newAmount === 0) {
                    document.querySelector('#empty_friend_requests_wrapper').className = "d-flex align-items-center justify-content-center flex-column"
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