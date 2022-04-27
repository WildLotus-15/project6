document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.reaction').forEach(reaction => {
        reaction.onclick = (event) => {
            const post_id = event.target.dataset.post_id
            const reaction = event.target.dataset.reaction

            update_reaction(post_id, reaction, event)
        }

        // Using JS to change elements hover property

        /* reaction.onmouseover = (event) => {
            event.target.style.cursor = "pointer"
        } */
    })
})

function update_reaction(post_id, reaction, event) {
    fetch(`/post/${post_id}/update_reaction`, {
        method: "POST",
        headers: {
            'X-CSRFToken': getCookie("csrftoken")
        },
        body: JSON.stringify({
            "reaction": reaction
        })
    })
        .then(response => response.json())
        .then(response => {
            console.log(response.message)

            // If a new reaction was being added to the post filled icon with a new amount will be displayed
            if (response.newStatus) {
                if (reaction == "like") {
                    event.target.src = "/images/like_fill.png"
                } else {
                    event.target.src = "/images/dislike_fill.png"
                }
            } else {
                // If an existing reaction was being removed from the post icon with a new amount will be displayed
                if (reaction == "like") {
                    event.target.src = "/images/like.png"
                } else {
                    event.target.src = "/images/dislike.png"
                }
            }

            if (response.newAmount !== 0) {
                document.querySelector(`#post_${post_id}_reaction_amount`).innerHTML = response.newAmount
            } else {
                document.querySelector(`#post_${post_id}_reaction_amount`).innerHTML = ''
            }
        })
}