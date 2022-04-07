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
    new_picture_form.id = 'new_picture'
    new_picture_form.style.width = "216px"
    new_picture_form.accept = "image/png, image/jpeg"
    picture_div.append(new_picture_form)

    new_picture_form.onchange = () => {
        const new_picture_value = document.querySelector('#new_picture').value

        const idxDot = new_picture_value.lastIndexOf(".") + 1;

        const extFile = new_picture_value.substr(idxDot, new_picture_value.length).toLowerCase();
        if (new_picture_form.value == '' || extFile == 'mp4') {
            console.log(extFile)
            save_button.disabled = true
        } else {
            save_button.disabled = false
        }
    }

    const public_logo = document.createElement('div')
    public_logo.innerHTML = "<img src='/images/globe.svg'> Public"
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
        document.querySelector('#message_div').innerHTML = ""
        edit_picture_div.append(edit_picture)
    })

    const save_button = document.createElement("button")
    save_button.type = "button"
    save_button.className = "btn btn-primary ml-1"
    save_button.innerHTML = "Save"
    save_button.disabled = true
    buttons_row.append(save_button)

    save_button.addEventListener('click', () => {
        const new_picture = document.querySelector('#new_picture')

        const formData = new FormData()

        formData.append('new_picture', new_picture.files[0])

        const extn = new_picture.files[0].type.split('/')[1]
        const size = new_picture.files[0].size
        const maxSize = 4000000; // 4 mb

        const valid = ["png", "jpg", "jpeg"]

        if (valid.includes(extn) && size < maxSize && new_picture.clientWidth <= 220 && new_picture.clientHeight <= 220) {
            fetch(`/edit_profile_picture/${profile_id}`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: formData
            })
                .then(response => response.json())
                .then(response => {
                    document.querySelector('#cancel').click()

                    document.querySelector('#profile_picture').src = response.new_picture_url

                    document.querySelector('#default_profile_picture').src = response.new_picture_url

                    document.querySelector('#logged_in_picture').src = response.new_picture_url

                    console.log(response.message)
                })
        } else {
            const message = document.createElement('div')
            message.innerHTML = "The file must be an image smaller than 4 MB and should be at least 160 x 160 pixels."
            document.querySelector('#message_div').append(message)
            save_button.disabled = true
        }
    })
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

    const char_left = document.createElement('p')
    char_left.className = "text-right"
    char_left.id = "char_left"
    char_left.innerHTML = `<small>${101 - bio.innerHTML.length} characters remaining</small>`
    document.querySelector('#char_left_div').append(char_left)

    const public_logo = document.createElement('div')
    public_logo.innerHTML = "<img src='/images/globe.svg'> Public"
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
        char_left.remove()
        bio_div.append(bio)
        edit_bio_div.append(edit_bio)
    })

    const save_button = document.createElement("button")
    save_button.id = "bio_save_btn"
    save_button.type = "button"
    save_button.className = "btn btn-primary ml-1"
    save_button.innerHTML = "Save"
    buttons_row.append(save_button)

    new_bio_form.onkeydown = aleko
    new_bio_form.onkeyup = aleko
    new_bio_form.addEventListener('paste', (event) => {
        let paste = (event.clipboardData || window.clipboardData).getData('text')

        new_bio_form.value = paste

        document.querySelector('#char_left').innerHTML = `<small>${101 - paste.length} characters remaining</small>`

        if (paste.length > 0) {
            save_button.disabled = false
        } else {
            save_button.disabled = true
        }

        event.preventDefault();
    })

    save_button.addEventListener('click', () => {
        const new_bio = document.querySelector('#new_bio').value

        const formData = new FormData()

        formData.append('new_bio', new_bio)

        fetch(`/edit_profile_bio/${profile_id}`, {
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

                document.querySelector("#default_profile_bio").innerHTML = new_bio

                console.log(response.message)
            })
    })
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function aleko(event) {
    document.querySelector('#char_left').innerHTML = `<small>${101 - event.target.value.length} characters remaining</small>`
    const button = document.querySelector('#bio_save_btn')

    if (101 - event.target.value.length <= 0 || event.target.value.length == 0) {
        button.disabled = true
    } else {
        button.disabled = false
    }
}