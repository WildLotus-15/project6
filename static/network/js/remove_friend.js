document.addEventListener('DOMContentLoaded', () => {
    remove_friend_button = document.querySelector('#remove_friend_button')

    if (remove_friend_button) {
        let friend_request_id = remove_friend_button.dataset.friend_request_id

        remove_friend_button.addEventListener('click', () => remove_friend(friend_request_id))
    }
})

function remove_friend(friend_request_id) {
    fetch(`/remove_from_friends/${friend_request_id}`)
    .then(response => response.json())
    .then(response => {
        window.location.reload()

        console.log(response.message)
    })
}