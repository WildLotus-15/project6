document.addEventListener('DOMContentLoaded', () => {
    room_checkbox = document.querySelectorAll('#update_room_checkbox').forEach((checkbox) => {
        if (checkbox) {
            let room_id = checkbox.dataset.room_id
            
            checkbox.addEventListener('click', () => update_room(room_id))
        }    
    })
})

function update_room(room_id) {
    fetch(`/chat/update_room/${room_id}/`)
    .then(response => response.json())
    .then(response => {
        console.log(response.message)
    })
}