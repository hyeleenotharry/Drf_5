

async function showMock() {
    const accessToken = localStorage.getItem("access")
    const response = await fetch('http://127.0.0.1:8000/user/mock/', {
        headers: {
            "Authorization": "Bearer " + accessToken,
        },
        method: 'GET',

    })
    response_json = await response.json()

    console.log(response_json)

}

async function showProfile() {
    const accessToken = localStorage.getItem("access")
    let user_id = JSON.parse(localStorage.getItem('payload'))['user_id']
    const url = `http://127.0.0.1:8000/user/profile/${user_id}`
    const respnse = await fetch(url, {
        headers: {
            "Authorization": "Bearer " + accessToken,
        },
        method: 'GET',
    })
    response_json = await response.json()
    console.log("showProfile")
    console.log(response_json)
}

async function logout() {
    localStorage.clear();
    window.location.href = 'http://127.0.0.1:8000/user/login/'
}
