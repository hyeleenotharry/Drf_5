

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

    books.forEach(element => {
        temp_html = `<div>
            ${element}
        </div>`
        $('#books').append(temp_html)
    });

    console.log(response_json.data[0])  // 책
    console.log(response_json.data[1])  // 리뷰
    console.log(response_json.data[2])  // 태그
}

// 가장 많이 좋아한 리뷰

// 태그들