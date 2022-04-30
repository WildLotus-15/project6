document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.post_edit_button').forEach(button => {
        button.onclick = () => {
            const post_id = button.dataset.post_id

            manage_post_edit(post_id)
        }
    })
})

function manage_post_edit(post_id) {
    // Getting the whole form which contains input and radio buttons
    const edit_form = document.querySelector(`#edit_post_form_${post_id}`)

    // Getting the edit post input to perform actions on UI
    const edit_input = document.querySelector(`#edit_post_input_${post_id}`)

    // By default save button is disabled
    const save_button = document.querySelector(`#post_save_button_${post_id}`)
    save_button.disabled = true

    // Getting default description which was specified when creating queried post
    const default_description = edit_form.dataset.default_description

    // Getting default visibility which was specified when creating queried post. Choises were: 1. Friends 2. Only me
    const default_visibility = edit_form.dataset.default_visibility

    // Creating hidden input which value will change after selected visibility radio button dataset
    // initially it is equal to default_visibility
    const last_selected_radio = document.createElement('input')
    last_selected_radio.type = "hidden"
    last_selected_radio.id = `hidden_input_${post_id}`
    last_selected_radio.dataset.manual_visibility = default_visibility

    // Getting form group which contains radio buttons for post visibility
    const form_group = document.querySelector(`#post_form_group_${post_id}`)

    // When toggling between radio buttons hidden input initial visibility dataset changes after their visibility dataset values
    form_group.onchange = (e) => {
        last_selected_radio.dataset.manual_visibility = e.target.dataset.visibility

        // New description's value length must be greater than 0
        // New description must not be equal to default description if visibility stays the same
        if (default_visibility !== e.target.dataset.visibility || edit_input.value !== default_description && edit_input.value.length > 0) {
            save_button.disabled = false
        } else {
            save_button.disabled = true
        }
    }

    edit_input.addEventListener('keydown', (event) => manage_post_update(event, save_button, default_description, last_selected_radio, default_visibility))
    edit_input.addEventListener('keyup', (event) => manage_post_update(event, save_button, default_description, last_selected_radio, default_visibility))
    edit_input.addEventListener('paste', (event) => manage_post_paste(event, save_button, default_description, edit_input))

    save_button.addEventListener('click', () => save_changes(post_id, edit_input.value))
}

function manage_post_update(event, save_button, default_value, last_selected_radio, default_visibility) {
    const new_value = event.target.value

    if ((new_value !== default_value || last_selected_radio.dataset.manual_visibility !== default_visibility) && new_value.length > 0) {
        save_button.disabled = false
    } else {
        save_button.disabled = true
    }
}

function manage_post_paste(event, save_button, default_description, edit_input) {
    let paste = (event.clipboardData || window.clipboardData).getData('text')

    edit_input.value = paste

    if (paste.length > 0 && paste.indexOf(' ') !== 0 && paste !== default_description) {
        save_button.disabled = false
    } else {
        save_button.disabled = true
    }

    event.preventDefault();
}

function save_changes(post_id, description) {
    const only_friends = document.querySelector(`#edit_only_friends_${post_id}`).checked
    const only_me = document.querySelector(`#edit_only_me_${post_id}`).checked

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

            // Changing form dataset attributes by specified values so it will update dynamically without requiring the page refreshing
            document.querySelector(`#edit_post_form_${post_id}`).dataset.default_visibility = response.newVisibility
            document.querySelector(`#edit_post_form_${post_id}`).dataset.default_description = description

            // Changing post's default description by a new one 
            document.querySelector(`#post_description_${post_id}`).innerHTML = description

            // Closing edit post modal
            document.querySelector(`#close_edit_post_modal_${post_id}`).click()
        })
}