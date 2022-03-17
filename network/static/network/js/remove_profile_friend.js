document.addEventListener('DOMContentLoaded', () => {
    profile_button = document.querySelector('#remove_friend_button')

    if (profile_button) {
        let profile_id = profile_button.dataset.profile_id

        profile_button.addEventListener('click', () => remove_profile_friend(profile_id))    
    }
})

function remove_profile_friend(profile_id) {
    fetch(`/remove_profile_friend/${profile_id}`)
    .then(response => response.json())
    .then(response => {
        console.log(response.message)
    
        window.location.reload()
    })
}