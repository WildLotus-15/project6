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

    const by_default_visibility = document.querySelector(`#post_edit_form__${post_id}`).dataset.default_visibility_default

    save_button.disabled = true

    const form_group = document.querySelector(`#post_${post_id}_form_group`)

    let last_selected_radio = document.createElement('input')
    last_selected_radio.type = "hidden"
    last_selected_radio.id = `hidden_input_${post_id}`
    last_selected_radio.dataset.by_default_visibility = by_default_visibility

    form_group.onchange = (e) => {
        last_selected_radio.dataset.by_default_visibility = e.target.dataset.visibility

        if (by_default_visibility !== e.target.dataset.visibility || edit_input.value !== edit_input.dataset.default_value) {
            if (edit_input.value.length > 0) {
                save_button.disabled = false
            }
        } else {
            save_button.disabled = true
        }
    }

    edit_input.addEventListener('keyup', (event) => manage_post_update(event, save_button, edit_input.dataset.default_value, post_id, edit_input, last_selected_radio, by_default_visibility))
    edit_input.addEventListener('paste', (event) => manage_post_paste(event, save_button, edit_input.dataset.default_value, edit_input))

    save_button.addEventListener('click', () => save_changes(post_id, edit_input.value))
}

function manage_post_update(event, save_button, default_value, post_id, edit_input, last_selected_radio, by_default_visibility) {
    const new_value = event.target.value


    const edit_only_me = document.querySelector(`#edit_only_me_${post_id}`)
    const edit_only_friends = document.querySelector(`#edit_only_friends_${post_id}`)

    // console.log((edit_only_friends.checked && edit_input.dataset.default_visibility == "only_friends" && new_value !== default_value) || (edit_only_me.checked && edit_input.dataset.default_visibility == "only_me" && new_value !== default_value))

    /* if ((edit_only_friends.checked && edit_input.dataset.default_visibility == "only_friends" || edit_only_me.checked && edit_input.dataset.default_visibility == "only_me") && new_value !== default_value) {
        if (new_value !== default_value && new_value.length > 0) {
            console.log('A')
        }
    } */

    /* document.querySelectorAll(`.edit_post_radio_${post_id}`).forEach(radio => {
        console.log(radio.hasAttribute("data-default_visibility"))
        if (radio.hasAttribute("data-default_visibility") && new_value !== default_value && new_value.length > 0) {
            save_button.disabled = true
        } else {
            save_button.disabled = false
        }
    }) */

    if ((new_value !== default_value || last_selected_radio.dataset.by_default_visibility !== by_default_visibility) && new_value.length > 0) {
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

            document.querySelector(`#post_edit_form__${post_id}`).dataset.default_visibility_default = response.newVisibility
            document.querySelector(`#edit_post_form_${post_id}`).dataset.default_value = description
            document.querySelector(`#post_description_${post_id}`).innerHTML = description
            document.querySelector(`#close_modal_${post_id}`).click()
        })
}