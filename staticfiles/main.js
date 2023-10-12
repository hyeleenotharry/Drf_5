

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
    let i = 0

    books.forEach(element => {

        temp_html = `
        <div class="book_bar">
            <h4>${JSON.stringify(element['title'])}</h4>
            <img src="/media/${element.cover}" style="width: 30px; height: 50px;">
            <div>
                ${JSON.stringify(element['author'])}
            </div>
        </div>`
        $('#books').append(temp_html)
        i++
    });
    reviews.forEach(element => {
        temp_html = `<div>
            <h4>${JSON.stringify(element['title'])}</h4>
            <div>${JSON.stringify(element['content'])}</div>
        </div>`
        $('#reviews').append(temp_html)


    });

    // console.log(response_json.data[0])  // 책
    // console.log(response_json.data[1])  // 리뷰
    // console.log(response_json.data[2])  // 태그
}

