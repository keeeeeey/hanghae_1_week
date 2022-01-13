$(document).ready(function () {

    $('#read_reply').css('display', 'flex')
    $('#modify_reply').css('display', 'none')

});

function outArticle() {

    window.location.href = "/";

}

function deleteArticle() {
    let article_id = $('#article_id').val();
    if (confirm("정말 삭제하시겠습니까?") == true) {
        $.ajax({
            type: "POST",
            url: "/api/delete",
            data: {articleID_give: article_id},
            success: function (response) {
                if (response['result'] == 'success') {
                    alert(response["msg"])
                    window.location.href = '/'
                } else {
                    alert(response["msg"])
                }
            }
        })
    } else {
        return;
    }

}

function goLike(reply_id, checker) {
    console.log('goLike: reply_id : ' + reply_id)

    $.ajax({
        type: "POST",
        url: "/api/like",
        data: {
            'id_give': reply_id,
            'checker': checker
        },
        success: function (response) {
            if (response["result"] == "success") {
                window.location.reload();
                console.log('after response checker : ' + checker)

                if (checker) {
                    change_color("gray_green", "arrow_down")
                    change_color("black", "arrow_up")
                } else {
                    change_color("gray_green", "arrow_up")
                    change_color("black", "arrow_down")
                }
            }
        }
    })
}

function setReply() {

    let article_id = $('#article_id').val()
    let data = $('#replyData').val()

    $.ajax({
        type: "POST",
        url: "/api/setReply",
        data: {articleID_give: article_id, reply_give: data},
        success: function (response) {
            alert(response['msg'])
            window.location.reload();

            fnMove(article_id)

        }
    })

}

function fnMove(seq) {
    var offset = $(seq).offset();
    $('html, body').animate({scrollTop: offset.top}, 400);
}

function change_color(val, id) {
    var element = document.getElementById(id);
    $('#arrow_up2').style.borderColor = "#8FB"
    $('#arrow_up2').style.color = "#8FB"
    $('#arrow_up2').style.borderTopColor = "#8FB"
    $('#arrow_up2').style.borderRightColor = "#8FB"
    if (val == "black") element.style.borderColor = "#000";
    else if (val == "gray_green") element.style.borderColor = "#8FBC8F";
}

//update
function update_posting() {
    let id = $('#article_id').val();
    console.log(id);
    let title = $('#input-title').val();
    let content = $('#textarea-content').val();
    $.ajax({
        type: "POST",
        url: "/api/update",
        data: {
            id_give: id,
            title_give: title,
            content_give: content
        },
        success: function (response) {
            alert("success")
            window.location.replace('/')
        }
    })
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

function deleteReply(id) {
    if (confirm('정말 삭제하시겠습니까?') == true) {

        $.ajax({
            type: "POST",
            url: "/api/deleteReply",
            data: {reply_id_give: id},
            success: function (response) {
                alert(response['msg'])
                window.location.reload();
                fnMove(article_id)

            }
        })
    } else {
        return;
    }

}

function modifyReply(id) {
    $('#modify_reply' + id).show()
    $('#read_reply' + id).hide()
    $('#modify_' + id).hide()
    $('#delete_' + id).hide()


    var temp = 'modify_reply' + id
    fnMove(temp)
}

function init_hide(id) {
    $('#' + id).hide()
}

function goModifyReply(id) {

    modify_value = $('#modify_value_reply' + id).val()

    $.ajax({
        type: "POST",
        url: "/api/modifyReply",
        data: {
            reply_id_give: id,
            modify_value: modify_value
        },
        success: function (response) {
            alert(response['msg'])
            window.location.reload();
            fnMove(article_id)

        }
    })
}

function cancelModify(id) {
    $('#modify_reply' + id).hide()
    $('#read_reply' + id).show()
    $('#modify_' + id).show()
    $('#delete_' + id).show()

}