function toRead(article_id) {

    window.location.href = "/api/read?article_id=" + article_id;

}

function makeBold(word, title) {

    console.log('word :' + word); //TE
    console.log('title :' + title);   //test

    let low_word = word.toLowerCase();
    let low_title = title.toLowerCase();

    let word_length = low_word.length; //2
    console.log('word_length :' + word_length);
    let word_index = low_title.search(low_word);//0
    console.log('word_index :' + word_index);
    let title_text = title.substr(word_index, word_length).bold(); //<b>t<b>
    console.log('title text :' + title_text);

    let front_word = title.substr(0, word_index)//''
    console.log('front_word :' + front_word);

    let back_word = title.substr(word_index + word_length, title.length - 1); //~~~~
    console.log('back_word :' + back_word);

    let full_word = front_word + title_text + back_word;
    console.log('full_word :' + full_word);

    return full_word;

}

function enterkey() {
    if (window.event.keyCode == 13) {
        goSearch();
    }
}

function goSearch() {

    var value = $('#searchWords').val();
    console.log('value : ' + value)

    $.ajax({
        type: "POST",
        url: "/api/search",
        data: {words_give: value},
        success: function (response) {
            console.log('success')
            let find_list = response['searched_list']
            console.log('search response : ' + find_list)
            $('#card_list').empty()
            for (let i = 0; i < find_list.length; i++) {
                let title = find_list[i]['title']
                let contents = find_list[i]['contents']
                let id = find_list[i]['_id']
                let count = find_list[i]['count']

                console.log("in for[" + i + "] : " + title + " , " + contents + " , " + id)

                let temp_html = `<div class="card w-100 mb-3">
                                            <div class="card-body article_body" onclick="toRead('${id}')">
                                                <h5 class="card-title title_ellipsis">${makeBold(value, title)}</h5>
                                                <p class="card-text contents_ellipsis">${contents}</p>
                                                <p class ="view_count">Hits :<span id="view_counting">${count}</span></p>
                                            </div>
                                         </div>`

                $('#card_list').append(temp_html)
            }
        }
    })

}

function toWrite() {
    //로그인 상태 구분하여 분기 구현
    //로그인시 글쓰기 페이지 이동, 비로그인시 로그인페이지 이동
    //글쓰기 페이지 이동시, ajax를 이용하여 _id값을 갖고 이동
    var user_id = $('#user_id').val()

    if (user_id === "") {
        alert('로그인이 필요합니다.')
        window.location.href = "/login";
    } else {
        window.location.href = "/write?user_id=" + user_id;
    }

}

function toLogin() {

    window.location.href = "/login";

}

function toLogout() {

    $.removeCookie('mytoken');
    window.location.href = '/'

}

function toMypage() {

    window.location.href = "/api/mypage";

}