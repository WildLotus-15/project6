document.addEventListener("DOMContentLoaded", () => {
    update_block_button = document.querySelector('#update_block_button')

    let profile_id = update_block_button.dataset.profile_id

    document.querySelector('#update_block').addEventListener('click', () => update_block(profile_id))
})

function update_block(profile_id) {
    fetch(`/profile/${profile_id}/update_block`)
    .then(response => response.json())
    .then(response => {
        console.log(response.message)

        window.location.reload()
    })
}