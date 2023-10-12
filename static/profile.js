window.onload = function () {
    showProfile()
}

async function showProfile() {
    let user_id = JSON.parse(localStorage.getItem('payload'))['user_id']
    const url = `http://127.0.0.1:8000/user/profile/${user_id}`
    const accessToken = localStorage.getItem("access")
    const response = await fetch(url, {
        headers: {
            "Authorization": "Bearer " + accessToken,
        },
        method: 'GET',
    })

    if (response.status === 200) {
        window.location.href = url
    }

}