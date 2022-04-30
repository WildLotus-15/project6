document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.delete_post_button').forEach(button => {
        button.onclick = () => {
            const post_id = button.dataset.post_id

            delete_post(post_id)
        }
    })
})

function delete_post(post_id) {
    fetch(`/post/${post_id}/delete`, {
        method: "DELETE",
        headers: {
            'X-CSRFToken': getCookie("csrftoken")
        },
    })
    .then(response => response.json())
    .then(response => {
        document.querySelector(`#post_${post_id}`).remove()

        document.querySelector(`#close_delete_post_modal_${post_id}`).click()

        console.log(response.message)
    })
}