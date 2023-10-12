

window.onload = () => {
    BookView()

}

// 메인페이지
async function BookView() {

    const response = await fetch('http://127.0.0.1:8000/book/mainpage/', {
        method: 'GET',
    })
    response_json = await response.json()


    books = response_json.data[0]
    reviews = response_json.data[1]

    books.forEach(element => {

        temp_html = `
        <a href="/book/${element['id']}">
            <div class="card" style="240px; margin-left: 90px;">
            <img class="card-img-top" src="/media/${element.cover}" alt="Card image cap" style="width: 240px; height: 300px;">
                <div class="card-body">
                    <h5 class="card-title">${element['title']}</h5>
                    <p class="card-text" style="color: rgb(110, 110, 110);">${element['author']}</p>

                </div>
            </div>
        </a>`
        $('#books').append(temp_html)

    });

    reviews.forEach(element => {
        let star = ''
        for (let i = 0; i < element['star']; i++) {
            star += '⭐'; // 문자열에 별 이모티콘을 추가
        }

        temp_html = `
        <div class="card" style="width: 30rem; box-shadow: 5px 5px 5px;margin-bottom: 40px; margin-left: 30px">
            <div class="card-body">
                <h5 class="card-title">${element['title']}</h5>
                <h6 class="card-subtitle mb-2 text-muted">${element['author']}</h6>
                <p class="card-text">${element['content']}</p>
                <p>${star}</p>
            </div>
        </div>
        `
        $('#reviews').append(temp_html)


    });

    // console.log(response_json.data[0])  // 책
    // console.log(response_json.data[1])  // 리뷰
    // console.log(response_json.data[2])  // 태그
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


}

