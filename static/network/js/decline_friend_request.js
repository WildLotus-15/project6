document.addEventListener('DOMContentLoaded', () => {
    decline_friend_request_links = document.querySelectorAll('.decline_friend_request_link')

    if (decline_friend_request_links) {
        decline_friend_request_links.forEach(link => {
            let request_id = link.dataset.friend_request_id

            link.addEventListener('click', (event) => decline_friend_request(event, request_id))
        })
    }
})

function decline_friend_request(event, request_id) {
    // Preventing the "Delete request" dropdown link from redirecting to an another page
    event.preventDefault();

    fetch(`/decline_friend_request/${request_id}`)
        .then(response => response.json())
        .then(response => {
            document.querySelector(`#friend_request_card_${request_id}`).remove()

            // If the user will not have any active friend requests page content will indicate that
            if (response.newAmount === 0) {
                document.querySelector('#empty_friend_requests_wrapper').className = "d-flex align-items-center justify-content-center flex-column"
            }

            console.log(response.message)
        })
        .catch((error) => {
            console.log("Error:", error);
        })
}