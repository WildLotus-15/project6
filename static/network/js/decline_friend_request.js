document.addEventListener('DOMContentLoaded', () => {
    decline_friend_request_button = document.querySelector('#decline_friend_request_button')

    if (decline_friend_request_button) {
        let request_id = decline_friend_request_button.dataset.friend_request_id

        decline_friend_request_button.addEventListener('click', (event) => decline_friend_request(event, request_id))
    }
})

function decline_friend_request(event, request_id) {
    // Preventing "Delete request" dropdown link from redirecting to a another page
    event.preventDefault();

    fetch(`/decline_friend_request/${request_id}`)
        .then(response => response.json())
        .then(response => {
            console.log(response.message)

            let friend_request_header = document.querySelector(`#friend_request_header_${request_id}`)
            friend_request_header.remove()

            // If user will not have any active friend requests message comes up indticating that state
            if (response.newAmount === 0) {
                document.querySelector('#empty_friend_requests_wrapper').className = "d-flex align-items-center justify-content-center flex-column"
                document.querySelector('.card-header').className = 'card-header border-bottom-0'
            }
        })
}