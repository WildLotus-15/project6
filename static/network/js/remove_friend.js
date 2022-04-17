document.addEventListener('DOMContentLoaded', () => {
    remove_friend_button = document.querySelectorAll('.remove_friend_button')

    if (remove_friend_button) {
        remove_friend_button.forEach(button => {
            let friend_request_id = button.dataset.friend_request_id

            button.addEventListener('click', () => remove_friend(friend_request_id))
        })
    }
})

function remove_friend(friend_request_id) {
    fetch(`/remove_from_friends/${friend_request_id}`)
    .then(response => response.json())
    .then(response => {
        document.querySelector(`#friend_card_${friend_request_id}`).remove()
        document.querySelector('#close').click()

        console.log(response.newAmount)

        // If the user will not have any friends page's content will indicate that
        if (response.newAmount === 0) {
            document.querySelector('#empty_friends_wrapper').className = "d-flex align-items-center justify-content-center flex-column" 
            document.querySelector('#card-header').className = 'card-header border-bottom-0'
        }

        console.log(response.message)
    })
    .catch((error) => {
        console.log("Error:", error);
    })
}