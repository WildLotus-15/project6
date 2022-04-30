document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.post_edit_button').forEach(button => {
        button.onclick = () => {
            const post_id = button.dataset.post_id

            manage_post_edit(post_id)
        }
    })
})

function manage_post_edit(post_id) {
    const edit_input = document.querySelector(`#edit_post_form_${post_id}`)

    const save_button = document.querySelector(`#post_save_button_${post_id}`)

    save_button.disabled = true

    edit_input.addEventListener('keyup', (event) => manage_post_update(event, save_button, edit_input.dataset.default_value))
    edit_input.addEventListener('keydown', (event) => manage_post_update(event, save_button, edit_input.dataset.default_value))
    edit_input.addEventListener('paste', (event) => manage_post_paste(event, save_button, edit_input.dataset.default_value, edit_input))

    save_button.addEventListener('click', () => save_changes(post_id, edit_input.value))
}

function manage_post_update(event, save_button, default_value) {
    const new_value = event.target.value

    if (new_value !== default_value && new_value.length > 0) {
        save_button.disabled = false
    } else {
        save_button.disabled = true
    }
}

function manage_post_paste(event, save_button, default_value, edit_input) {
    let paste = (event.clipboardData || window.clipboardData).getData('text')

    edit_input.value = paste

    if (paste.length > 0 && paste.indexOf(' ') !== 0 && paste !== default_value) {
        save_button.disabled = false
    } else {
        save_button.disabled = true
    }

    event.preventDefault();
}

function save_changes(post_id, description) {
    const only_friends = document.querySelector('#only_friends').checked
    const only_me = document.querySelector('#only_me').checked

    fetch(`/post/${post_id}/edit`, {
        method: "PUT",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            "description": description,
            "only_friends": only_friends,
            "only_me": only_me
        })
    })
    .then(response => response.json())
    .then(response => {
        console.log(response.message)

        document.querySelector(`#post_description_${post_id}`).innerHTML = description
        document.querySelector(`#close_modal_${post_id}`).click()
    })
}