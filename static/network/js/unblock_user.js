document.addEventListener("DOMContentLoaded", () => {
    unblock_buttons = document.querySelectorAll(".unblock_buttons")

    if (unblock_buttons) {
        unblock_buttons.forEach((button) => {
            let profile_id = button.dataset.profile_id

            button.addEventListener("click", () => update_block(profile_id)) 
        })
    }
})

function update_block(profile_id) {
    fetch(`/profile/${profile_id}/update_block`)
    .then(response => response.json())
    .then(response => {
        console.log(response.message)


        document.querySelector(`#close_modal_${profile_id}`).click()
        document.querySelector(`#blocked_user_card_${profile_id}`).remove()

        // If the user will not have any blocked users page content will indicate that
        if (response.newAmount === 0) {
            document.querySelector('#empty_blocked_users_wrapper').className = "d-flex align-items-center justify-content-center flex-column"
        }
    })
}