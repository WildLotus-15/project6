new Autocomplete('#autocomplete', {
    search: input => {
        return new Promise(resolve => {
            if (input.length < 1) {
                return [
                    fetch('/recent_searches')
                        .then(response => response.json())
                        .then(response => {
                            resolve(response)
                        })
                ]
            }
            const url = `/search?q=${input}`

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    console.log(data)

                    resolve(data.query_list)
                })
        })
    },

    getResultValue: result => `${result.username
        ? `${result.username}`
        : `${result.content}`
        }`,

    renderResult: (result, props) =>
    `
    ${result.username
            ? `
        <li ${props}>
            <div class="d-flex align-items-center">
                <div>
                    <img src="${result.picture}" width=36 height=36 style="border-radius: 50%">  
                </div>
                <div class="d-flex flex-column ml-1">
                    <div>
                        ${result.username}
                    </div>
                    <div class="text-muted">
                        ${result.currently_friended
                ? "<small>Friend</small>"
                : ""
            }
                    </div>
                </div>
            </div>
        </li>
        `
            : `
        <li ${props}>
            <div class="d-flex align-items-center">
                <div>
                    ${result.picture !== null
                ? `<img src="${result.picture}" width=36 height=36 style="border-radius: 50%">`
                : ''
            }  
                </div>
                <div class="ml-1">
                    ${result.content}
                </div>
            </div>
        </li>
        `
        }
    `,
    onSubmit: result => {
        if (result.username) {
            window.location.href = "/search_results" + "?q=" + result.username
        } else {
            window.location.href = "/search_results" + "?q=" + result.content
        }
    },
})
