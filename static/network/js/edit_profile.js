document.addEventListener('DOMContentLoaded', () => {
    let profile_id = document.querySelector("#edit_profile_bio").dataset.profile_id

    document.querySelector("#edit_profile_picture").addEventListener('click', () => edit_profile_picture(profile_id))

    document.querySelector("#edit_profile_bio").addEventListener('click', () => edit_profile_bio(profile_id))
})

function edit_profile_picture(profile_id) {
    const picture_div = document.querySelector("#new_picture_div")

    const edit_picture = document.querySelector('#edit_profile_picture')

    const edit_picture_div = document.querySelector('#profile_picture_edit_div') 

    const buttons_row = document.querySelector("#new_picture_buttons_div")

    const profile_picture = document.querySelector('#profile_picture')

    profile_picture.style.display = 'none'

    const new_picture_form = document.createElement('input')
    new_picture_form.type = "file"
    new_picture_form.style.width = "216px"
    new_picture_form.accept = "image/png, image/jpeg"
    picture_div.append(new_picture_form)

    new_picture_form.onchange = () => {
        if (new_picture_form.value == '') {
            save_button.disabled = true
        } else {
            save_button.disabled = false
        }
    }

    const public_logo = document.createElement('div')
    public_logo.innerHTML  = "<img src='/images/globe.svg'> Public"
    public_logo.className = "mr-2"
    buttons_row.append(public_logo)

    const cancel_button = document.createElement("button")
    cancel_button.id = "cancel"
    cancel_button.type = "button"
    cancel_button.className = "btn btn-secondary ml-2"
    cancel_button.innerHTML = "Cancel"
    buttons_row.append(cancel_button)

    cancel_button.addEventListener("click", () => {
        new_picture_form.remove()
        save_button.remove()
        cancel_button.remove()
        public_logo.remove()
        profile_picture.style.display = 'block'
        edit_picture_div.append(edit_picture)
    })

    const save_button = document.createElement("button")
    save_button.type = "button"
    save_button.className = "btn btn-primary ml-1"
    save_button.innerHTML = "Save"
    save_button.disabled = true
    buttons_row.append(save_button)
}

function edit_profile_bio(profile_id) {
    const edit_bio = document.querySelector("#edit_profile_bio")

    const bio = document.querySelector("#profile_bio")

    const bio_div = document.querySelector("#new_bio_div")

    const edit_bio_div = document.querySelector('#profile_bio_edit_div')

    const buttons_row = document.querySelector("#new_buttons_div")
    
    document.querySelector('#profile_bio').remove()
    document.querySelector('#edit_profile_bio').remove()

    const new_bio_form = document.createElement('input')
    new_bio_form.placeholder = "Describe who you are"
    new_bio_form.className = "form-control"
    new_bio_form.id = 'new_bio'
    new_bio_form.value = bio.innerHTML
    bio_div.append(new_bio_form)

    const public_logo = document.createElement('div')
    public_logo.innerHTML  = "<img src='/images/globe.svg'> Public"
    public_logo.className = "mr-2"
    buttons_row.append(public_logo)

    const cancel_button = document.createElement("button")
    cancel_button.id = "cancel"
    cancel_button.type = "button"
    cancel_button.className = "btn btn-secondary ml-2"
    cancel_button.innerHTML = "Cancel"
    buttons_row.append(cancel_button)

    cancel_button.addEventListener("click", () => {
        new_bio_form.remove()
        save_button.remove()
        cancel_button.remove()
        public_logo.remove()
        bio_div.append(bio)
        edit_bio_div.append(edit_bio)
    })

    const save_button = document.createElement("button")
    save_button.type = "button"
    save_button.className = "btn btn-primary ml-1"
    save_button.innerHTML = "Save"
    buttons_row.append(save_button)

    new_bio_form.onkeyup = () => {
        if (new_bio_form.value.length > 0) {
            save_button.disabled = false
        } else {
            save_button.disabled = true
        }
    }
    
    save_button.addEventListener('click', () => {
        const new_bio = document.querySelector('#new_bio').value

        const formData = new FormData()

        formData.append('new_bio', new_bio)
        formData.append('profile_id', profile_id)

        fetch(`/edit_profile/${profile_id}`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: formData
        })
        .then(response => response.json())
        .then(response => {
            document.querySelector('#cancel').click()

            document.querySelector('#profile_bio').innerHTML = new_bio
        })
    })
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}