document.addEventListener('DOMContentLoaded', () => {
    room_checkbox = document.querySelectorAll('.update_room_checkbox')
    
    room_checkbox.forEach((checkbox) => {
        if (checkbox) {
            let room_id = checkbox.dataset.room_id
            
            checkbox.addEventListener('click', () => update_room(room_id))
        }    
    })

    var room_save_button = document.querySelector('#room_save_button')

    room_save_button.addEventListener('click', () => {
        window.location.href = "/chat/"
    })
})

function update_room(room_id) {
    fetch(`/chat/update_room/${room_id}/`)
    .then(response => response.json())
    .then(response => {
        console.log(response.message)
    })
}