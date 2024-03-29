document.addEventListener("DOMContentLoaded", () => {
    block_button = document.querySelector('#block_button')

    let profile_id = block_button.dataset.profile_id

    block_button.addEventListener('click', () => update_block(profile_id))
})

function update_block(profile_id) {
    fetch(`/profile/${profile_id}/update_block`)
    .then(response => response.json())
    .then(response => {
        console.log(response.message)

        window.location.pathname = "/blocked_users"
    })
}