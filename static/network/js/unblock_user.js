document.addEventListener("DOMContentLoaded", () => {
    unblock_button = document.querySelector("#unblock_button")
    
    if (unblock_button) {
        let profile_id = unblock_button.dataset.profile_id

        document.querySelector('#unblock_button').addEventListener("click", () => update_block(profile_id))
    }
})

function update_block(profile_id) {
    fetch(`/profile/${profile_id}/update_block`)
    .then(response => response.json())
    .then(response => {
        console.log(response.message)

        window.location.reload()
    })
}